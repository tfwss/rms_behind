"""Filesystem storage helpers for product report attachments."""

import os
import shutil
from typing import Optional

from fastapi import UploadFile

from app.core.config import settings


def save_product_report_file(
    product_code: str, meeting_report: Optional[UploadFile]
) -> Optional[str]:
    """Persist an uploaded meeting report to the configured storage directory."""
    if not meeting_report:
        return None

    # Ensure the filename is safe and scoped to the product code.
    safe_name = os.path.basename(meeting_report.filename)
    target_dir = os.path.join(settings.product_report_storage_dir, product_code)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, safe_name)

    # Stream the upload to disk.
    with open(target_path, "wb") as destination:
        shutil.copyfileobj(meeting_report.file, destination)

    return target_path
