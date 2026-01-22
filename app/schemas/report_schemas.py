"""Pydantic schemas for report types, reports, and attachments."""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ReportFieldBase(BaseModel):
    """Shared fields for report field schemas."""
    name: str = Field(..., examples=["device_model"])
    label: str = Field(..., examples=["设备型号"])
    field_type: str = Field(default="text")
    required: bool = Field(default=False)


class ReportFieldCreate(ReportFieldBase):
    """Payload used to create a report field."""


class ReportFieldRead(ReportFieldBase):
    """Response schema for a report field."""
    id: int

    class Config:
        from_attributes = True


class ReportTypeBase(BaseModel):
    """Shared fields for report type schemas."""
    name: str
    description: Optional[str] = None


class ReportTypeCreate(ReportTypeBase):
    """Payload used to create a report type."""


class ReportTypeRead(ReportTypeBase):
    """Response schema for a report type with its fields."""
    id: int
    fields: List[ReportFieldRead] = []

    class Config:
        from_attributes = True


class ReportCreate(BaseModel):
    """Payload used to create a report and its field values."""
    report_type_id: int
    title: str
    values: Dict[str, Optional[str]] = Field(
        default_factory=dict,
        description="字段 key 为 ReportField.name",
    )


class ReportAttachmentRead(BaseModel):
    """Response schema for a report attachment."""
    id: int
    filename: str
    storage_path: str
    content_type: Optional[str] = None

    class Config:
        from_attributes = True


class ReportRead(BaseModel):
    """Response schema for a report with values and attachments."""
    id: int
    report_type_id: int
    title: str
    created_at: datetime
    values: Dict[str, Optional[str]]
    attachments: List[ReportAttachmentRead]

    class Config:
        from_attributes = True
