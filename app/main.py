from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base, engine
from app.routers import report_types, reports


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    Base.metadata.create_all(bind=engine)

    app.include_router(report_types.router)
    app.include_router(reports.router)

    return app


app = create_app()
