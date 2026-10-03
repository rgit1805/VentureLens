import logging

from fastapi import APIRouter

from app.api.v1.schemas import HealthResponse
from app.core.config import settings

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    logger.info("Health check requested")

    return HealthResponse(
        status="healthy",
        environment=settings.environment,
    )
