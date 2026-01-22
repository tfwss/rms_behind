import os
import shutil
from typing import Optional

from fastapi import UploadFile

from app.core.config import settings


def save_product_report_file(
    product_code: str, meeting_report: Optional[UploadFile]
) -> Optional[str]:
    if not meeting_report:
        return None

    safe_name = os.path.basename(meeting_report.filename)
    target_dir = os.path.join(settings.product_report_storage_dir, product_code)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, safe_name)

    with open(target_path, "wb") as destination:
        shutil.copyfileobj(meeting_report.file, destination)

    return target_path
