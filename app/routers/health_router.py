from fastapi import APIRouter, Depends

from app.dependencies import get_metrics_service
from app.schemas.metrics_schema import MetricsOut
from app.services.metrics_service import MetricsService

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/metrics", response_model=MetricsOut)
def get_metrics(
    metrics_service: MetricsService = Depends(get_metrics_service),
) -> MetricsOut:
    metrics = metrics_service.get_metrics()
    return MetricsOut(
        sensors_total=metrics.sensors_total,
        sensors_active=metrics.sensors_active,
        readings_total=metrics.readings_total,
        alerts_open=metrics.alerts_open,
        alerts_acknowledged=metrics.alerts_acknowledged,
        alerts_resolved=metrics.alerts_resolved,
    )
