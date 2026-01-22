"""Services for storing report attachments in SQL Server FILETABLE."""

import os
from typing import Iterable, List

import pyodbc
from fastapi import UploadFile

from app.core.config import settings


class FileTableStorage:
    """Encapsulates FILETABLE persistence logic."""

    def __init__(self, connection_string: str | None = None) -> None:
        """Initialize with an optional override for the ODBC connection string."""
        self.connection_string = connection_string or settings.odbc_connection_string

    def _get_raw_connection(self) -> pyodbc.Connection:
        """Open a raw pyodbc connection with autocommit enabled."""
        return pyodbc.connect(self.connection_string, autocommit=True)

    def save_files(self, report_id: int, files: Iterable[UploadFile]) -> List[dict]:
        """
        Save files into SQL Server FILETABLE.

        You need to:
        1. Enable FILESTREAM on SQL Server.
        2. Create FILETABLE (see scripts/sqlserver_init.sql).
        3. Grant INSERT/UPDATE permissions.
        """
        # No attachments supplied means nothing to save.
        if not files:
            return []

        saved: List[dict] = []
        with self._get_raw_connection() as connection:
            cursor = connection.cursor()
            for upload in files:
                # Normalize the filename and read file content.
                filename = os.path.basename(upload.filename)
                content = upload.file.read()

                # Insert binary data into FILETABLE and capture the path.
                cursor.execute(
                    """
                    INSERT INTO report_files (name, file_stream)
                    OUTPUT INSERTED.path_locator
                    VALUES (?, ?)
                    """,
                    filename,
                    pyodbc.Binary(content),
                )
                row = cursor.fetchone()
                storage_path = row[0]
                # Prepare metadata for ORM persistence.
                saved.append(
                    {
                        "filename": filename,
                        "storage_path": storage_path,
                        "content_type": upload.content_type,
                        "report_id": report_id,
                    }
                )

        return saved
