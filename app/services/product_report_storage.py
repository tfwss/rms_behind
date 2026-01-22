"""Local file storage helpers for product full-process reports."""

import os
import shutil
from typing import Optional

from fastapi import UploadFile

from app.core.config import settings


def save_product_report_file(
    product_code: str, meeting_report: Optional[UploadFile]
) -> Optional[str]:
    """Save the meeting report file under D:\\pdf\\<product_code> and return its path."""
    # If no file is provided, do nothing.
    if not meeting_report:
        return None

    # Use basename to prevent directory traversal in filenames.
    safe_name = os.path.basename(meeting_report.filename)
    # Build the per-product subdirectory.
    target_dir = os.path.join(settings.product_report_storage_dir, product_code)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, safe_name)

    # Stream the upload into the destination file.
    with open(target_path, "wb") as destination:
        shutil.copyfileobj(meeting_report.file, destination)

    return target_path
