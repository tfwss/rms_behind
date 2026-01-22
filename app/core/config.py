from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Report Management System"
    debug: bool = False

    database_url: str = Field(
        default=(
            "mssql+pyodbc://sa:YourStrong!Passw0rd@localhost:1433/"
            "rms?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
        ),
        description="SQL Server connection string",
    )
    odbc_connection_string: str = Field(
        default=(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=localhost,1433;"
            "DATABASE=rms;"
            "UID=sa;"
            "PWD=YourStrong!Passw0rd;"
            "TrustServerCertificate=yes;"
        ),
        description="ODBC connection string for FILETABLE operations",
    )


settings = Settings()
