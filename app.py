from fastapi import FastAPI
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from routers.v1 import router as v1_router 
from database.mongo import db
from database.milvus import vector_db
from pymilvus import connections

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
@app.get("/health", tags=["System"])
async def health_check():
    """
    Validates API operational status and database connectivity.
    """
    mongo_status = "connected" if db.client else "disconnected"
    milvus_status = "connected" if vector_db.client else "disconnected"

    return {
        "status": "healthy",
        "services": {
            "mongodb": mongo_status,
            "milvus": milvus_status
        }
    }


# Entry point for local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)