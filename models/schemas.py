from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, timezone

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