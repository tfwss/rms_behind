"""Routes for product full-process report submissions (operationcode 45)."""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product_report_models import ProductFullReport
from app.schemas.product_report_schemas import ProductFullReportResponse
from app.services.product_report_storage import save_product_report_file


# Group all product report endpoints under a shared prefix.
router = APIRouter(prefix="/product-reports", tags=["product-reports"])


@router.post("/full-report", response_model=ProductFullReportResponse)
def submit_full_report(
    token: Optional[str] = Form(default=None),
    operationcode: int = Form(default=45),
    rp_number: str = Form(...),
    creator: str = Form(...),
    product_name: str = Form(...),
    product_code: str = Form(...),
    creatorTime: date = Form(...),
    verification_man: str = Form(...),
    pro_leader: str = Form(...),
    recipe_leader: str = Form(...),
    meetingReport: Optional[UploadFile] = File(default=None),
    db: Session = Depends(get_db),
):
    """Persist the report payload and optional PDF; return success/fail status."""
    # Save the uploaded meeting report to disk and capture the saved path.
    file_path = save_product_report_file(product_code, meetingReport)
    # Build the ORM object matching the database columns.
    report = ProductFullReport(
        token=token,
        operationcode=operationcode,
        rp_number=rp_number,
        creator=creator,
        product_name=product_name,
        product_code=product_code,
        creator_time=creatorTime,
        verification_man=verification_man,
        pro_leader=pro_leader,
        recipe_leader=recipe_leader,
        file_name=file_path,
        is_delete=0,
    )

    try:
        # Write the row to the database.
        db.add(report)
        db.commit()
        return ProductFullReportResponse(operationcode=45, state="success")
    except Exception:
        # Roll back and return failure if anything goes wrong.
        db.rollback()
        return ProductFullReportResponse(operationcode=45, state="fail")
