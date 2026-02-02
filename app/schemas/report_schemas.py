# 模块级文档字符串：报表类型、报表与附件的 Pydantic Schema
"""Pydantic schemas for report types, reports, and attachments."""

# 导入日期时间类型
from datetime import datetime
# 导入类型注解
from typing import Dict, List, Optional

# 导入 Pydantic 基类与字段工具
from pydantic import BaseModel, Field


# 报表字段基础 Schema
class ReportFieldBase(BaseModel):
    # 类文档：报表字段通用字段
    """Shared fields for report field schemas."""
    # 字段名称
    name: str = Field(..., examples=["device_model"])
    # 字段标签
    label: str = Field(..., examples=["设备型号"])
    # 字段类型
    field_type: str = Field(default="text")
    # 是否必填
    required: bool = Field(default=False)


# 创建报表字段的请求 Schema
class ReportFieldCreate(ReportFieldBase):
    # 类文档：创建报表字段的请求体
    """Payload used to create a report field."""


# 报表字段的响应 Schema
class ReportFieldRead(ReportFieldBase):
    # 类文档：报表字段响应体
    """Response schema for a report field."""
    # 字段 ID
    id: int

    # Pydantic 配置
    class Config:
        # 允许从 ORM 属性读取
        from_attributes = True


# 报表类型基础 Schema
class ReportTypeBase(BaseModel):
    # 类文档：报表类型通用字段
    """Shared fields for report type schemas."""
    # 类型名称
    name: str
    # 类型描述
    description: Optional[str] = None


# 创建报表类型的请求 Schema
class ReportTypeCreate(ReportTypeBase):
    # 类文档：创建报表类型的请求体
    """Payload used to create a report type."""


# 报表类型的响应 Schema
class ReportTypeRead(ReportTypeBase):
    # 类文档：包含字段列表的报表类型响应体
    """Response schema for a report type with its fields."""
    # 报表类型 ID
    id: int
    # 字段列表
    fields: List[ReportFieldRead] = []

    # Pydantic 配置
    class Config:
        # 允许从 ORM 属性读取
        from_attributes = True


# 创建报表的请求 Schema
class ReportCreate(BaseModel):
    # 类文档：创建报表及字段值的请求体
    """Payload used to create a report and its field values."""
    # 报表类型 ID
    report_type_id: int
    # 报表标题
    title: str
    # 字段值映射
    values: Dict[str, Optional[str]] = Field(
        # 默认空字典
        default_factory=dict,
        # 描述字段 key 的含义
        description="字段 key 为 ReportField.name",
    )


# 附件的响应 Schema
class ReportAttachmentRead(BaseModel):
    # 类文档：报表附件响应体
    """Response schema for a report attachment."""
    # 附件 ID
    id: int
    # 文件名
    filename: str
    # 存储路径
    storage_path: str
    # MIME 类型
    content_type: Optional[str] = None

    # Pydantic 配置
    class Config:
        # 允许从 ORM 属性读取
        from_attributes = True


# 报表响应 Schema
class ReportRead(BaseModel):
    # 类文档：包含字段值与附件的报表响应体
    """Response schema for a report with values and attachments."""
    # 报表 ID
    id: int
    # 报表类型 ID
    report_type_id: int
    # 报表标题
    title: str
    # 创建时间
    created_at: datetime
    # 字段值
    values: Dict[str, Optional[str]]
    # 附件列表
    attachments: List[ReportAttachmentRead]

    # Pydantic 配置
    class Config:
        # 允许从 ORM 属性读取
        from_attributes = True
