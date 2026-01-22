"""SQLAlchemy models for configurable report types and reports."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ReportType(Base):
    """Represents a configurable report type (e.g., device acceptance report)."""
    __tablename__ = "report_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    # Fields that define the structure of this report type.
    fields: Mapped[List["ReportField"]] = relationship(
        back_populates="report_type", cascade="all, delete-orphan"
    )


class ReportField(Base):
    """Defines a single configurable field for a report type."""
    __tablename__ = "report_fields"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_type_id: Mapped[int] = mapped_column(
        ForeignKey("report_types.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    field_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="text"
    )
    required: Mapped[bool] = mapped_column(default=False)

    # Parent report type.
    report_type: Mapped[ReportType] = relationship(back_populates="fields")


class Report(Base):
    """Concrete report instance created by users."""
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_type_id: Mapped[int] = mapped_column(
        ForeignKey("report_types.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    # Associated report type definition.
    report_type: Mapped[ReportType] = relationship()
    # Captured values for each configured field.
    values: Mapped[List["ReportFieldValue"]] = relationship(
        back_populates="report", cascade="all, delete-orphan"
    )
    # Attachments uploaded alongside the report.
    attachments: Mapped[List["ReportAttachment"]] = relationship(
        back_populates="report", cascade="all, delete-orphan"
    )


class ReportFieldValue(Base):
    """Stores a value for a specific report field within a report."""
    __tablename__ = "report_field_values"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id"), nullable=False, index=True
    )
    field_id: Mapped[int] = mapped_column(
        ForeignKey("report_fields.id"), nullable=False
    )
    value: Mapped[Optional[str]] = mapped_column(Text)

    # Parent report instance.
    report: Mapped[Report] = relationship(back_populates="values")
    # Field definition for this value.
    field: Mapped[ReportField] = relationship()


class ReportAttachment(Base):
    """Represents a file attachment stored in SQL Server FILETABLE."""
    __tablename__ = "report_attachments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id"), nullable=False, index=True
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    content_type: Mapped[Optional[str]] = mapped_column(String(100))

    # Parent report instance.
    report: Mapped[Report] = relationship(back_populates="attachments")
