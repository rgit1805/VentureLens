import logging

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import unhandled_exception_handler


setup_logging()

app = FastAPI(
    title=settings.app_name,
    description=(
        "AI-Powered Venture Capital Due Diligence "
        "and Investment Analysis Platform"
    ),
    version=settings.app_version,
)

app.add_exception_handler(
    Exception,
    unhandled_exception_handler,
)

app.include_router(
    api_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to VentureLens API"
    }