from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.db import AlertModel
from app.dependencies import get_alert_service, get_sensor_service
from app.domain.alert_states import VALID_STATES, InvalidAlertTransitionError
from app.schemas.alert_schema import AlertOut, AlertStatusUpdate
from app.services.alert_service import AlertNotFoundError, AlertService
from app.services.sensor_service import SensorService

router = APIRouter(tags=["alerts"])


def _responses(*codes: int) -> dict[int | str, dict[str, Any]]:
    descriptions = {
        status.HTTP_400_BAD_REQUEST: "Transicion de estado invalida",
        status.HTTP_404_NOT_FOUND: "Sensor o alerta no encontrada",
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
    alert_status: str | None = Query(
        None,
        alias="status",
        description="Filtra por estado: open, acknowledged o resolved",
    ),
    sensor_service: SensorService = Depends(get_sensor_service),
    alert_service: AlertService = Depends(get_alert_service),
) -> list[AlertModel]:
    sensor = sensor_service.get_sensor(sensor_code)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor '{sensor_code}' no encontrado.",
        )
    return alert_service.list_alerts(sensor_code, alert_status)


@router.patch(
    "/alerts/{alert_id}",
    response_model=AlertOut,
    status_code=status.HTTP_200_OK,
    responses=_responses(status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST),
)
def update_alert_status(
    status_update: AlertStatusUpdate,
    *,
    alert_id: int = Path(..., ge=1, description="ID de la alerta"),
    alert_service: AlertService = Depends(get_alert_service),
) -> AlertModel:
    if status_update.status not in VALID_STATES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Estado invalido: '{status_update.status}'.",
        )
    try:
        return alert_service.change_status(alert_id, status_update.status)
    except AlertNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except InvalidAlertTransitionError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
