from fastapi import APIRouter

from app.schemas.health import HealthRead

router = APIRouter(tags=["health"])


@router.get("/health", summary="Check API health")
def health_check() -> HealthRead:
    return HealthRead()
