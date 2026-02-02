# 模块级文档字符串：报表类型与报表的 SQLAlchemy 模型
"""SQLAlchemy models for configurable report types and reports."""

# 导入时间类型
from datetime import datetime
# 导入类型注解
from typing import List, Optional

# 导入 SQLAlchemy 列类型与外键
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
# 导入 ORM 映射工具
from sqlalchemy.orm import Mapped, mapped_column, relationship

# 导入声明式基类
from app.core.database import Base


# 报表类型模型
class ReportType(Base):
    # 类文档：可配置的报表类型
    """Represents a configurable report type (e.g., device acceptance report)."""
    # 对应数据库表名
    __tablename__ = "report_types"

    # 主键 ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # 类型名称
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    # 类型描述
    description: Mapped[Optional[str]] = mapped_column(String(255))

    # 定义该报表类型结构的字段列表
    fields: Mapped[List["ReportField"]] = relationship(
        # 反向回填字段名
        back_populates="report_type",
        # 级联删除配置
        cascade="all, delete-orphan",
    )


# 报表字段模型
class ReportField(Base):
    # 类文档：报表类型的单个字段定义
    """Defines a single configurable field for a report type."""
    # 对应数据库表名
    __tablename__ = "report_fields"

    # 主键 ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # 外键：所属报表类型
    report_type_id: Mapped[int] = mapped_column(
        # 指向 report_types 表
        ForeignKey("report_types.id"),
        # 不允许为空
        nullable=False,
        # 创建索引
        index=True,
    )
    # 字段内部名称
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # 展示名称（标签）
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    # 字段类型
    field_type: Mapped[str] = mapped_column(
        # 字段类型长度
        String(50),
        # 不允许为空
        nullable=False,
        # 默认字段类型为文本
        default="text",
    )
    # 是否必填
    required: Mapped[bool] = mapped_column(default=False)

    # 关联的父报表类型
    report_type: Mapped[ReportType] = relationship(back_populates="fields")


# 报表实例模型
class Report(Base):
    # 类文档：用户创建的具体报表
    """Concrete report instance created by users."""
    # 对应数据库表名
    __tablename__ = "reports"

    # 主键 ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # 外键：报表类型
    report_type_id: Mapped[int] = mapped_column(
        # 指向 report_types 表
        ForeignKey("report_types.id"),
        # 不允许为空
        nullable=False,
        # 创建索引
        index=True,
    )
    # 报表标题
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    # 创建时间
    created_at: Mapped[datetime] = mapped_column(
        # 使用带时区的时间类型
        DateTime(timezone=True),
        # 默认使用 UTC 时间
        default=datetime.utcnow,
    )

    # 关联的报表类型定义
    report_type: Mapped[ReportType] = relationship()
    # 报表字段对应的值集合
    values: Mapped[List["ReportFieldValue"]] = relationship(
        # 反向回填字段名
        back_populates="report",
        # 级联删除配置
        cascade="all, delete-orphan",
    )
    # 报表的附件列表
    attachments: Mapped[List["ReportAttachment"]] = relationship(
        # 反向回填字段名
        back_populates="report",
        # 级联删除配置
        cascade="all, delete-orphan",
    )


# 报表字段值模型
class ReportFieldValue(Base):
    # 类文档：存储报表中某个字段的值
    """Stores a value for a specific report field within a report."""
    # 对应数据库表名
    __tablename__ = "report_field_values"

    # 主键 ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # 外键：报表 ID
    report_id: Mapped[int] = mapped_column(
        # 指向 reports 表
        ForeignKey("reports.id"),
        # 不允许为空
        nullable=False,
        # 创建索引
        index=True,
    )
    # 外键：字段定义 ID
    field_id: Mapped[int] = mapped_column(
        # 指向 report_fields 表
        ForeignKey("report_fields.id"),
        # 不允许为空
        nullable=False,
    )
    # 字段值内容
    value: Mapped[Optional[str]] = mapped_column(Text)

    # 关联的报表实例
    report: Mapped[Report] = relationship(back_populates="values")
    # 关联的字段定义
    field: Mapped[ReportField] = relationship()


# 报表附件模型
class ReportAttachment(Base):
    # 类文档：存储在 SQL Server FILETABLE 的附件
    """Represents a file attachment stored in SQL Server FILETABLE."""
    # 对应数据库表名
    __tablename__ = "report_attachments"

    # 主键 ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # 外键：报表 ID
    report_id: Mapped[int] = mapped_column(
        # 指向 reports 表
        ForeignKey("reports.id"),
        # 不允许为空
        nullable=False,
        # 创建索引
        index=True,
    )
    # 文件名
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    # 存储路径
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    # 文件 MIME 类型
    content_type: Mapped[Optional[str]] = mapped_column(String(100))

    # 关联的报表实例
    report: Mapped[Report] = relationship(back_populates="attachments")
