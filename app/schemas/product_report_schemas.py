# 模块级文档字符串：产品报表接口的 Pydantic Schema
"""Pydantic schemas for product report endpoints."""

# 导入日期类型
from datetime import date
# 导入可选类型注解
from typing import Optional

# 导入 Pydantic 基类与字段工具
from pydantic import BaseModel, Field


# 创建产品完整报表的请求 Schema
class ProductFullReportCreate(BaseModel):
    # 类文档：创建产品完整报表的请求体
    """Payload schema for creating a product full report."""
    # token 字段
    token: Optional[str] = None
    # 操作码字段
    operationcode: int = Field(default=45)
    # 报表编号
    rp_number: str
    # 创建人
    creator: str
    # 产品名称
    product_name: str
    # 产品编码
    product_code: str
    # 创建时间
    creatorTime: date
    # 复核人
    verification_man: str
    # 项目负责人
    pro_leader: str
    # 配方负责人
    recipe_leader: str


# 产品完整报表响应 Schema
class ProductFullReportResponse(BaseModel):
    # 类文档：产品报表接口返回体
    """Response schema returned by the product report endpoint."""
    # 操作码
    operationcode: int = 45
    # 状态字段
    state: str
