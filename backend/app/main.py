from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description=(
        "AI-Powered Venture Capital Due Diligence "
        "and Investment Analysis Platform"
    ),
    version=settings.app_version,
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
