from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.db import SensorModel
from app.dependencies import get_sensor_service
from app.schemas.sensor_schema import SensorCreate, SensorOut, SensorUpdate
from app.services.sensor_service import SensorAlreadyExistsError, SensorService

router = APIRouter(prefix="/sensors", tags=["sensors"])


@router.get("", response_model=list[SensorOut], status_code=status.HTTP_200_OK)
def list_sensors(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    service: SensorService = Depends(get_sensor_service),
) -> list[SensorModel]:
    return service.list_sensors(limit, offset)


@router.post("", response_model=SensorOut, status_code=status.HTTP_201_CREATED)
def create_sensor(
    sensor: SensorCreate,
    service: SensorService = Depends(get_sensor_service),
) -> SensorModel:
    try:
        return service.register(
            sensor.code,
            sensor.name,
            sensor.sensor_type,
            sensor.location,
            sensor.alert_threshold,
        )
    except SensorAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e


@router.get("/{sensor_code}", response_model=SensorOut, status_code=status.HTTP_200_OK)
def get_sensor(
    sensor_code: str,
    service: SensorService = Depends(get_sensor_service),
) -> SensorModel:

    sensor = service.get_sensor(sensor_code)
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sensor no encontrado"
        )
    return sensor


@router.patch(
    "/{sensor_code}", response_model=SensorOut, status_code=status.HTTP_200_OK
)
def update_sensor(
    sensor_code: str,
    sensor_update: SensorUpdate,
    service: SensorService = Depends(get_sensor_service),
) -> SensorModel:
    updated = service.update_sensor(
        sensor_code,
        sensor_update.name,
        sensor_update.location,
        sensor_update.alert_threshold,
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sensor no encontrado"
        )
    return updated


@router.delete("/{sensor_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(
    sensor_code: str, service: SensorService = Depends(get_sensor_service)
) -> None:
    success = service.delete_sensor(sensor_code)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sensor no encontrado"
        )
