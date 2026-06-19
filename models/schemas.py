from pydantic import BaseModel, Field, ConfigDict
from typing import Optional , List
from datetime import datetime, timezone ,  timedelta
from enum import Enum
class CoreModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

class Merchant(CoreModel):
    id: str = Field(alias="_id")
    name: str
    aliases: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Category(CoreModel):
    id: str = Field(alias="_id")
    name: str
    description: Optional[str] = None

class Transaction(CoreModel):
    id: Optional[str] = Field(alias="_id", default=None)
    raw_text: str
    merchant: Optional[str] = None
    amount: float
    category: Optional[str] = None
    source: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Feedback(CoreModel):
    id: Optional[str] = Field(alias="_id", default=None)
    transaction_id: str
    prediction: str
    corrected_category: str
    confidence: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CategorizeRequest(BaseModel):
    text: str = Field(..., description="Raw transaction SMS or bank statement text")

class CategorizeResponse(BaseModel):
    merchant: str
    category: str
    confidence: float

class ResolutionResult(BaseModel):
    raw_text: str
    cleaned_text: str
    canonical_merchant: str
    confidence: float
    is_resolved: bool
    resolution_method: str = Field(description="exact_alias, substring, rule_engine, or none")




class MemoryState(str, Enum):
    EPHEMERAL = "EPHEMERAL"
    TEMPORARY = "TEMPORARY"
    PERMANENT = "PERMANENT"
    ARCHIVED = "ARCHIVED"

class MerchantProfile(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    canonical_name: str
    display_name: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)
    entity_type: str = "Unknown"  # e.g., "Individual", "Business"
    
    # Phase 4 Core Variables
    memory_state: MemoryState = MemoryState.EPHEMERAL
    frequency: int = 1
    first_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    notes: Optional[str] = None
    confidence: float = 0.0
    category: Optional[str] = None
    subcategory: Optional[str] = None



class TransactionCategory(str, Enum):
    FOOD = "Food"
    TRAVEL = "Travel"
    ENTERTAINMENT = "Entertainment"
    BILLS = "Bills"
    FRIENDS = "Friends"
    EDUCATION = "Education"
    HEALTHCARE = "Healthcare"
    UNKNOWN = "Unknown"

class ConfidenceEvaluation(BaseModel):
    raw_category: str
    final_category: TransactionCategory
    confidence: float
    is_hallucination_risk: bool
    calibration_applied: str