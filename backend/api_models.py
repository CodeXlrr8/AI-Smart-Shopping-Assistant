from pydantic import BaseModel, Field
from typing import Optional

class ShoppingRequest(BaseModel):
    query: str = Field(min_length=2)

class AlertRequest(BaseModel):
    product_id: str
    target_price: float = Field(gt=0)
    email: Optional[str] = None
