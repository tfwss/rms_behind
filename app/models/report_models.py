from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ReportType(Base):
    __tablename__ = "report_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    fields: Mapped[List["ReportField"]] = relationship(
        back_populates="report_type", cascade="all, delete-orphan"
    )


class ReportField(Base):
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

    report_type: Mapped[ReportType] = relationship(back_populates="fields")


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_type_id: Mapped[int] = mapped_column(
        ForeignKey("report_types.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    report_type: Mapped[ReportType] = relationship()
    values: Mapped[List["ReportFieldValue"]] = relationship(
        back_populates="report", cascade="all, delete-orphan"
    )
    attachments: Mapped[List["ReportAttachment"]] = relationship(
        back_populates="report", cascade="all, delete-orphan"
    )


class ReportFieldValue(Base):
    __tablename__ = "report_field_values"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id"), nullable=False, index=True
    )
    field_id: Mapped[int] = mapped_column(
        ForeignKey("report_fields.id"), nullable=False
    )
    value: Mapped[Optional[str]] = mapped_column(Text)

    report: Mapped[Report] = relationship(back_populates="values")
    field: Mapped[ReportField] = relationship()


class ReportAttachment(Base):
    __tablename__ = "report_attachments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id"), nullable=False, index=True
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    content_type: Mapped[Optional[str]] = mapped_column(String(100))

    report: Mapped[Report] = relationship(back_populates="attachments")
