from fastapi import Depends, FastAPI, Request
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from routers.v1 import router as v1_router 
from database.mongo import db
from database.milvus import vector_db
from pymilvus import connections
from routers.memory import router as memory_router  # <-- 1. Add this import
from routers.analytics import router as analytics_router
from core.security import validate_api_key
from core.rate_limiter import setup_rate_limiting, limiter
from routers import v1, memory, analytics, rag
from routers.observability import router as observability_router
import logging

# Configure logging globally
logging.basicConfig(
    level=logging.DEBUG,  # DEBUG gives you the most detail
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB connections
    await db.connect()
    vector_db.connect()
    yield
    # Shutdown: Clean up connections
    await db.disconnect()
    vector_db.disconnect()

# Initialize FastAPI with metadata
app = FastAPI(
    title="Velar Transaction Intelligence API",
    description="Core engine for raw transaction ingestion and ML routing.",
    version="1.0.0",
    lifespan=lifespan
)

# Phase 11 Foresight: Initialize Prometheus Metrics Middleware
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
app.include_router(v1_router)
app.include_router(memory_router)  # <-- 2. Register the memory router here
app.include_router(analytics_router)
app.include_router(rag.router)
app.include_router(observability_router)
@app.post("/v1/categorize", dependencies=[Depends(validate_api_key)], tags=["Public API"])
@limiter.limit("50/minute")
async def public_categorize(request:Request, payload: dict):
    # Internal routing to Phase 2 -> 5 -> 9 Engine
    return {"status": "success", "message": "Transaction routed to Intelligence Engine."}
@app.get("/health", tags=["System"])
async def health_check():
    mongo_status = "connected" if db.client else "disconnected"
    milvus_status = "connected" if vector_db.client else "disconnected"

    logger.debug("Health check: MongoDB=%s, Milvus=%s", mongo_status, milvus_status)

    return {
        "status": "healthy" if mongo_status == "connected" and milvus_status == "connected" else "degraded",
        "services": {
            "mongodb": mongo_status,
            "milvus": milvus_status
        }
    }


# Entry point for local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)