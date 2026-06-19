from fastapi import APIRouter
from models.schemas import CategorizeRequest, CategorizeResponse
from engines.rule_engine import rule_engine
import time

router = APIRouter(prefix="/v1", tags=["Transaction Intelligence"])

@router.post("/categorize", response_model=CategorizeResponse)
async def categorize_transaction(request: CategorizeRequest):
    # Phase 11 Foresight: We can track latency here later
    start_time = time.time()
    
    # Process text through the Rule Engine
    result = rule_engine.categorize(request.text)
    
    process_time = time.time() - start_time
    # TODO: Log process_time to Prometheus for Latency metrics
    
    return result