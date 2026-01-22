"""API routes for creating and retrieving reports."""

import json
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.report_models import Report, ReportAttachment, ReportField, ReportFieldValue
from app.schemas.report_schemas import ReportRead
from app.services.storage_service import FileTableStorage

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("", response_model=ReportRead)
def create_report(
    report_type_id: int = Form(...),
    title: str = Form(...),
    values: str = Form("{}"),
    files: Optional[List[UploadFile]] = File(default=None),
    db: Session = Depends(get_db),
):
    """Create a report with field values and optional attachments."""
    try:
        values_data = json.loads(values)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON for values") from exc

    # Create the report row first to obtain the report ID.
    report = Report(report_type_id=report_type_id, title=title)
    db.add(report)
    db.flush()

    # Build a lookup map of field definitions by name.
    field_map = {
        field.name: field
        for field in db.query(ReportField)
        .filter(ReportField.report_type_id == report_type_id)
        .all()
    }

    # Persist each provided field value if the field exists for the type.
    for field_name, value in values_data.items():
        field = field_map.get(field_name)
        if not field:
            continue
        db.add(
            ReportFieldValue(
                report_id=report.id,
                field_id=field.id,
                value=str(value) if value is not None else None,
            )
        )

    # Save attachments to FILETABLE and store metadata.
    storage = FileTableStorage()
    attachments = storage.save_files(report.id, files or [])
    for attachment in attachments:
        db.add(
            ReportAttachment(
                report_id=report.id,
                filename=attachment["filename"],
                storage_path=attachment["storage_path"],
                content_type=attachment["content_type"],
            )
        )

    # Finalize transaction and return response schema.
    db.commit()
    db.refresh(report)
    return _report_to_read(report)


@router.get("/{report_id}", response_model=ReportRead)
def get_report(report_id: int, db: Session = Depends(get_db)):
    """Fetch a single report by ID."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return _report_to_read(report)


@router.get("", response_model=list[ReportRead])
def list_reports(db: Session = Depends(get_db)):
    """List all reports."""
    return [_report_to_read(report) for report in db.query(Report).all()]


def _report_to_read(report: Report) -> ReportRead:
    """Convert a Report ORM object into a ReportRead schema."""
    values = {value.field.name: value.value for value in report.values}
    return ReportRead(
        id=report.id,
        report_type_id=report.report_type_id,
        title=report.title,
        created_at=report.created_at,
        values=values,
        attachments=report.attachments,
    )
