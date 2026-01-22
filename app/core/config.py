"""Application configuration backed by environment variables."""

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed settings with defaults for the RMS backend."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Application metadata used by FastAPI.
    app_name: str = "Report Management System"
    debug: bool = False

    # Installed ODBC driver name; must match the system driver list exactly.
    odbc_driver: str = Field(
        default="ODBC Driver 17 for SQL Server",
        description="ODBC driver name installed on the host",
    )
    # Primary SQLAlchemy connection string.
    database_url: str = Field(
        default="",
        description="SQL Server connection string",
    )
    # ODBC connection string used for FILETABLE operations.
    odbc_connection_string: str = Field(
        default="",
        description="ODBC connection string for FILETABLE operations",
    )
    # Local filesystem location for product full report attachments.
    product_report_storage_dir: str = Field(
        default=r"D:\pdf",
        description="Root folder for product full report attachments",
    )

    @model_validator(mode="after")
    def _set_connection_defaults(self) -> "Settings":
        """Populate connection strings using the configured ODBC driver."""
        if not self.database_url:
            driver_token = self.odbc_driver.replace(" ", "+")
            self.database_url = (
                "mssql+pyodbc://wangxu:6225112Wx..@localhost:1433/"
                f"rms?driver={driver_token}&TrustServerCertificate=yes"
            )
        if not self.odbc_connection_string:
            self.odbc_connection_string = (
                f"DRIVER={{{self.odbc_driver}}};"
                "SERVER=localhost,1433;"
                "DATABASE=rms;"
                "UID=wangxu;"
                "PWD=6225112Wx..;"
                "TrustServerCertificate=yes;"
            )
        return self


# Singleton settings instance used across the application.
settings = Settings()
