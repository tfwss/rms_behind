"""Pydantic schemas for product report endpoints."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class ProductFullReportCreate(BaseModel):
    """Payload schema for creating a product full report."""
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
    """Response schema returned by the product report endpoint."""
    operationcode: int = 45
    state: str
