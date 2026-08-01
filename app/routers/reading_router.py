from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.db import ReadingModel
from app.dependencies import get_reading_service
from app.schemas.reading_schema import ReadingCreate, ReadingOut, ReadingUpdate
from app.services.reading_service import ReadingService, SensorNotFoundError

router = APIRouter(tags=["readings"])


@router.get(
    "/sensors/{sensor_id}/readings",
    response_model=list[ReadingOut],
    status_code=status.HTTP_200_OK,
)
def list_readings(
    sensor_id: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    service: ReadingService = Depends(get_reading_service),
) -> list[ReadingModel]:
    return service.get_history(sensor_id, limit, offset, from_date, to_date)


@router.post(
    "/sensors/{sensor_id}/readings",
    response_model=ReadingOut,
    status_code=status.HTTP_201_CREATED,
)
def create_reading(
    sensor_id: str,
    reading: ReadingCreate,
    service: ReadingService = Depends(get_reading_service),
) -> ReadingModel:
    try:
        return service.record(sensor_id, reading.value, reading.unit)
    except SensorNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get(
    "/readings/{reading_id}", response_model=ReadingOut, status_code=status.HTTP_200_OK
)
def get_reading(
    reading_id: int, service: ReadingService = Depends(get_reading_service)
) -> ReadingModel:
    reading = service.get_reading(reading_id)
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lectura no encontrada"
        )
    return reading


@router.patch(
    "/readings/{reading_id}", response_model=ReadingOut, status_code=status.HTTP_200_OK
)
def update_reading(
    reading_id: int,
    reading_update: ReadingUpdate,
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
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.delete("/readings/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading(
    reading_id: int, service: ReadingService = Depends(get_reading_service)
) -> None:
    success = service.delete_reading(reading_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lectura no encontrada"
        )