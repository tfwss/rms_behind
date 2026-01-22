"""Application configuration backed by environment variables."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed settings with defaults for the RMS backend."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Application metadata used by FastAPI.
    app_name: str = "Report Management System"
    debug: bool = False

    # Primary SQLAlchemy connection string.
    database_url: str = Field(
        default=(
            "mssql+pyodbc://wangxu:6225112Wx..@localhost:1433/"
            "rms?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
        ),
        description="SQL Server connection string",
    )
    # ODBC connection string used for FILETABLE operations.
    odbc_connection_string: str = Field(
        default=(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=localhost,1433;"
            "DATABASE=rms;"
            "UID=wangxu;"
            "PWD=6225112Wx..;"
            "TrustServerCertificate=yes;"
        ),
        description="ODBC connection string for FILETABLE operations",
    )
    # Local filesystem location for product full report attachments.
    product_report_storage_dir: str = Field(
        default=r"D:\pdf",
        description="Root folder for product full report attachments",
    )


# Singleton settings instance used across the application.
settings = Settings()
