from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class ProductFullReportCreate(BaseModel):
    token: Optional[str] = None
    operationcode: int = Field(default=45)
    rp_number: str
    creator: str
    product_name: str
    product_code: str
    creatorTime: date
    verification_man: str
    pro_leader: str
    recipe_leader: str


class ProductFullReportResponse(BaseModel):
    operationcode: int = 45
    state: str
