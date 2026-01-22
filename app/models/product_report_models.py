"""SQLAlchemy model for product full reports."""

from datetime import date
from typing import Optional

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ProductFullReport(Base):
    """Represents a product full report record."""
    __tablename__ = "product_full_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    token: Mapped[Optional[str]] = mapped_column(String(255))
    operationcode: Mapped[int] = mapped_column(Integer, default=45)
    rp_number: Mapped[str] = mapped_column(String(100), nullable=False)
    creator: Mapped[str] = mapped_column(String(100), nullable=False)
    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    product_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    # Column uses legacy naming "creatorTime" in the database.
    creator_time: Mapped[date] = mapped_column("creatorTime", Date, nullable=False)
    verification_man: Mapped[str] = mapped_column(String(100), nullable=False)
    pro_leader: Mapped[str] = mapped_column(String(100), nullable=False)
    recipe_leader: Mapped[str] = mapped_column(String(100), nullable=False)
    # Column uses legacy naming "FileName" in the database.
    file_name: Mapped[Optional[str]] = mapped_column("FileName", String(500))
    is_delete: Mapped[int] = mapped_column(Integer, default=0)
