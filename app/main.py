from fastapi import FastAPI

from app.api.errors import register_exception_handlers
from app.api.routes import customers, health
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="REST API for customer registration and status management.",
    )
    register_exception_handlers(application)
    application.include_router(health.router)
    application.include_router(customers.router)
    return application


app = create_app()
