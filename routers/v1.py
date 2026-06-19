from fastapi import APIRouter
from pydantic import BaseModel
from models.schemas import CategorizeRequest, CategorizeResponse , ResolutionResult
from engines.rule_engine import rule_engine
import time
from services.merchant_resolver import merchant_resolver
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

class ResolveRequest(BaseModel):
    text: str

@router.post("/resolve", response_model=ResolutionResult)
async def resolve_transaction_merchant(request: ResolveRequest):
    """
    Phase 3 Endpoint: Takes a raw UPI/Bank transaction string and resolves it to a canonical merchant.
    """
    result = await merchant_resolver.resolve(request.text)
    return result