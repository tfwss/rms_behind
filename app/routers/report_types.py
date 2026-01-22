from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.report_models import ReportField, ReportType
from app.schemas.report_schemas import (
    ReportFieldCreate,
    ReportFieldRead,
    ReportTypeCreate,
    ReportTypeRead,
)

router = APIRouter(prefix="/report-types", tags=["report-types"])


@router.post("", response_model=ReportTypeRead)
def create_report_type(payload: ReportTypeCreate, db: Session = Depends(get_db)):
    report_type = ReportType(name=payload.name, description=payload.description)
    db.add(report_type)
    db.commit()
    db.refresh(report_type)
    return report_type


@router.get("", response_model=list[ReportTypeRead])
def list_report_types(db: Session = Depends(get_db)):
    return db.query(ReportType).all()


@router.post("/{report_type_id}/fields", response_model=ReportFieldRead)
def create_report_field(
    report_type_id: int, payload: ReportFieldCreate, db: Session = Depends(get_db)
):
    report_type = db.query(ReportType).filter(ReportType.id == report_type_id).first()
    if not report_type:
        raise HTTPException(status_code=404, detail="Report type not found")

    field = ReportField(
        report_type_id=report_type_id,
        name=payload.name,
        label=payload.label,
        field_type=payload.field_type,
        required=payload.required,
    )
    db.add(field)
    db.commit()
    db.refresh(field)
    return field


@router.get("/{report_type_id}/fields", response_model=list[ReportFieldRead])
def list_report_fields(report_type_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ReportField)
        .filter(ReportField.report_type_id == report_type_id)
        .all()
    )
