# 模块级文档字符串：产品完整报表模型
"""SQLAlchemy model for product full reports."""

# 导入日期类型
from datetime import date
# 导入可选类型注解
from typing import Optional

# 导入 SQLAlchemy 列类型
from sqlalchemy import Date, Integer, String
# 导入 ORM 映射工具
from sqlalchemy.orm import Mapped, mapped_column

# 导入声明式基类
from app.core.database import Base


# 产品完整报表模型
class ProductFullReport(Base):
    # 类文档：产品完整报表记录
    """Represents a product full report record."""
    # 对应数据库表名
    __tablename__ = "product_full_reports"

    # 主键 ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # 令牌字段
    token: Mapped[Optional[str]] = mapped_column(String(255))
    # 操作码
    operationcode: Mapped[int] = mapped_column(Integer, default=45)
    # 报表编号
    rp_number: Mapped[str] = mapped_column(String(100), nullable=False)
    # 创建人
    creator: Mapped[str] = mapped_column(String(100), nullable=False)
    # 产品名称
    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    # 产品编码（索引）
    product_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    # 数据库列名使用旧字段 creatorTime
    creator_time: Mapped[date] = mapped_column("creatorTime", Date, nullable=False)
    # 复核人
    verification_man: Mapped[str] = mapped_column(String(100), nullable=False)
    # 项目负责人
    pro_leader: Mapped[str] = mapped_column(String(100), nullable=False)
    # 配方负责人
    recipe_leader: Mapped[str] = mapped_column(String(100), nullable=False)
    # 数据库列名使用旧字段 FileName
    file_name: Mapped[Optional[str]] = mapped_column("FileName", String(500))
    # 删除标记
    is_delete: Mapped[int] = mapped_column(Integer, default=0)
