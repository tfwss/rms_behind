"""SQLAlchemy table mapping for product full-process reports."""

from datetime import date
from typing import Optional

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ProductFullReport(Base):
    """Database model that mirrors the product full-process report fields."""

    __tablename__ = "product_full_reports"

    # Primary key for internal use.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # Token supplied by the caller (optional).
    token: Mapped[Optional[str]] = mapped_column(String(255))
    # Operation code, expected to be 45 for this report type.
    operationcode: Mapped[int] = mapped_column(Integer, default=45)
    # Report number/code from the client.
    rp_number: Mapped[str] = mapped_column(String(100), nullable=False)
    # Creator name.
    creator: Mapped[str] = mapped_column(String(100), nullable=False)
    # Product name.
    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    # Product code used for grouping files.
    product_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    # Creation date; stored using the DB column name "creatorTime".
    creator_time: Mapped[date] = mapped_column("creatorTime", Date, nullable=False)
    # Verification leader.
    verification_man: Mapped[str] = mapped_column(String(100), nullable=False)
    # Process department leader.
    pro_leader: Mapped[str] = mapped_column(String(100), nullable=False)
    # Recipe leader.
    recipe_leader: Mapped[str] = mapped_column(String(100), nullable=False)
    # File path stored under DB column name "FileName".
    file_name: Mapped[Optional[str]] = mapped_column("FileName", String(500))
    # Soft-delete flag (0 = active, 1 = deleted).
    is_delete: Mapped[int] = mapped_column(Integer, default=0)
