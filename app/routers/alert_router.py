from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.db import AlertModel
from app.dependencies import get_alert_repository, get_sensor_service
from app.repositories.alert_repository import SqlAlchemyAlertRepository
from app.schemas.alert_schema import AlertOut
from app.services.sensor_service import SensorService

router = APIRouter(tags=["alerts"])


def _responses(*codes: int) -> dict[int | str, dict[str, Any]]:
    descriptions = {
        status.HTTP_404_NOT_FOUND: "Sensor no encontrado",
    }
    return {code: {"description": descriptions[code]} for code in codes}


@router.get(
    "/sensors/{sensor_code}/alerts",
    response_model=list[AlertOut],
    status_code=status.HTTP_200_OK,
    responses=_responses(status.HTTP_404_NOT_FOUND),
)
def list_sensor_alerts(
    sensor_code: str = Path(
        ...,
        min_length=1,
        max_length=50,
        description="Código del sensor",
    ),
    sensor_service: SensorService = Depends(get_sensor_service),
    alert_repo: SqlAlchemyAlertRepository = Depends(get_alert_repository),
) -> list[AlertModel]:
    sensor = sensor_service.get_sensor(sensor_code)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor '{sensor_code}' no encontrado.",
        )
    return alert_repo.list_for_sensor(sensor_code)
