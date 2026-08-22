from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.db import ReadingModel
from app.dependencies import get_reading_service
from app.domain.stats import ReadingStats
from app.schemas.reading_schema import (
    ReadingCreate,
    ReadingOut,
    ReadingUpdate,
    StatsOut,
)
from app.services.reading_service import (
    ReadingService,
    SensorInactiveError,
    SensorNotFoundError,
)

router = APIRouter(tags=["readings"])


def _responses(*codes: int) -> dict[int | str, dict[str, Any]]:
    descriptions = {
        status.HTTP_400_BAD_REQUEST: (
            "Datos invalidos (unidad incompatible, fuera de rango "
            "operacional, etc.)"
        ),
        status.HTTP_404_NOT_FOUND: "Sensor o lectura no encontrado",
        status.HTTP_409_CONFLICT: "El sensor esta desactivado",
    }
    return {code: {"description": descriptions[code]} for code in codes}


@router.get(
    "/sensors/{sensor_code}/readings",
    response_model=list[ReadingOut],
    status_code=status.HTTP_200_OK,
    responses=_responses(status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST),
)
def list_readings(
    *,
    sensor_code: str = Path(
        ...,
        min_length=1,
        max_length=50,
        description="Código del sensor",
    ),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    from_date: datetime | None = Query(
        None, 
        description="Fecha inicial del rango"
    ),
    to_date: datetime | None = Query(
        None, 
        description="Fecha final del rango"
    ),
    service: ReadingService = Depends(get_reading_service),
) -> list[ReadingModel]:
    if from_date and to_date and from_date > to_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="'from_date' no puede ser posterior a 'to_date'",
        )

    try:
        return service.get_history(
            sensor_code, 
            limit, offset, 
            from_date, 
            to_date
        )
    except SensorNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get(
    "/sensors/{sensor_code}/stats",
    response_model=StatsOut,
    status_code=status.HTTP_200_OK,
    responses=_responses(status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST),
)
def get_sensor_stats(
    *,
    sensor_code: str = Path(
        ...,
        min_length=1,
        max_length=50,
        description="Código del sensor",
    ),
    from_date: datetime | None = Query(
        None, description="Fecha inicial del periodo"
    ),
    to_date: datetime | None = Query(None, description="Fecha final del periodo"),
    service: ReadingService = Depends(get_reading_service),
) -> StatsOut:
    if from_date and to_date and from_date > to_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="'from_date' no puede ser posterior a 'to_date'",
        )

    try:
        stats: ReadingStats = service.get_stats(sensor_code, from_date, to_date)
    except SensorNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    return StatsOut(
        sensor_id=sensor_code.upper(),
        count=stats.count,
        minimum=stats.minimum,
        maximum=stats.maximum,
        average=stats.average,
    )


@router.post(
    "/sensors/{sensor_code}/readings",
    response_model=ReadingOut,
    status_code=status.HTTP_201_CREATED,
    responses=_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_409_CONFLICT,
    ),
)
def create_reading(
    reading: ReadingCreate,
    *,
    sensor_code: str = Path(
        ...,
        min_length=1,
        max_length=50,
        description="Código del sensor",
    ),
    service: ReadingService = Depends(get_reading_service),
) -> ReadingModel:
    try:
        return service.record(
            sensor_code,
            reading.value,
            reading.unit
        )
    except SensorNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except SensorInactiveError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get(
    "/readings/{reading_id}",
    response_model=ReadingOut,
    status_code=status.HTTP_200_OK,
    responses=_responses(status.HTTP_404_NOT_FOUND),
)
def get_reading(
    reading_id: int = Path(
        ...,
        ge=1, 
        description="ID de la lectura"
    ),
    service: ReadingService = Depends(get_reading_service),
) -> ReadingModel:
    reading = service.get_reading(reading_id)
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lectura no encontrada"
        )
    return reading


@router.patch(
    "/readings/{reading_id}",
    response_model=ReadingOut,
    status_code=status.HTTP_200_OK,
    responses=_responses(status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST),
)
def update_reading(
    reading_update: ReadingUpdate,
    *,
    reading_id: int = Path(
        ...,
        ge=1, 
        description="ID de la lectura"
    ),
    service: ReadingService = Depends(get_reading_service),
) -> ReadingModel:
    try:
        updated = service.update_reading(
            reading_id, reading_update.value, reading_update.unit
        )
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Lectura no encontrada"
            )
        return updated
    except SensorNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.delete(
    "/readings/{reading_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=_responses(status.HTTP_404_NOT_FOUND),
)
def delete_reading(
    reading_id: int = Path(
        ..., 
        ge=1, 
        description="ID de la lectura"
    ),
    service: ReadingService = Depends(get_reading_service),
) -> None:
    success = service.delete_reading(reading_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lectura no encontrada"
        )