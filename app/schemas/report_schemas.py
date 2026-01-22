from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ReportFieldBase(BaseModel):
    name: str = Field(..., examples=["device_model"])
    label: str = Field(..., examples=["设备型号"])
    field_type: str = Field(default="text")
    required: bool = Field(default=False)


class ReportFieldCreate(ReportFieldBase):
    pass


class ReportFieldRead(ReportFieldBase):
    id: int

    class Config:
        from_attributes = True


class ReportTypeBase(BaseModel):
    name: str
    description: Optional[str] = None


class ReportTypeCreate(ReportTypeBase):
    pass


class ReportTypeRead(ReportTypeBase):
    id: int
    fields: List[ReportFieldRead] = []

    class Config:
        from_attributes = True


class ReportCreate(BaseModel):
    report_type_id: int
    title: str
    values: Dict[str, Optional[str]] = Field(
        default_factory=dict,
        description="字段 key 为 ReportField.name",
    )


class ReportAttachmentRead(BaseModel):
    id: int
    filename: str
    storage_path: str
    content_type: Optional[str] = None

    class Config:
        from_attributes = True


class ReportRead(BaseModel):
    id: int
    report_type_id: int
    title: str
    created_at: datetime
    values: Dict[str, Optional[str]]
    attachments: List[ReportAttachmentRead]

    class Config:
        from_attributes = True
