from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import Base, SessionLocal, engine
from app.repositories.reading_repositorie import SqlAlchemyReadingRepository
from app.schemas.reading_schema import ReadingCreate, ReadingOut, ReadingUpdate
from app.services.reading_service import ReadingService

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SensorHub API", version="0.2.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_reading_service(db: Session = Depends(get_db)) -> ReadingService:
    repo = SqlAlchemyReadingRepository(db)
    return ReadingService(repo)

@app.get(
    "/sensors/{sensor_id}/readings", 
    response_model=list[ReadingOut], 
    status_code=status.HTTP_200_OK
)
def list_readings(
    sensor_id: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    service: ReadingService = Depends(get_reading_service)
):
    return service.get_history(sensor_id, limit, offset, from_date, to_date)

@app.post(
    "/sensors/{sensor_id}/readings", 
    response_model=ReadingOut, 
    status_code=status.HTTP_201_CREATED
)
def create_reading(
    sensor_id: str, 
    reading: ReadingCreate, 
    service: ReadingService = Depends(get_reading_service)
):
    try:
        return service.record(sensor_id, reading.value, reading.unit)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get(
    "/readings/{reading_id}", 
    response_model=ReadingOut, 
    status_code=status.HTTP_200_OK
)
def get_reading(
    reading_id: int, 
    service: ReadingService = Depends(get_reading_service)
    ):

    reading = service.get_reading(reading_id)
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Lectura no encontrada"
        )
    return reading

@app.patch(
    "/readings/{reading_id}", 
    response_model=ReadingOut, 
    status_code=status.HTTP_200_OK
)
def update_reading(
    reading_id: int, 
    reading_update: ReadingUpdate, 
    service: ReadingService = Depends(get_reading_service)
):
    try:
        updated = service.update_reading(
            reading_id, 
            reading_update.value, 
            reading_update.unit
        )
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Lectura no encontrada"
            )
        return updated
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )

@app.delete(
    "/readings/{reading_id}", 
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_reading(
    reading_id: int, 
    service: ReadingService = Depends(get_reading_service)
    ):
    success = service.delete_reading(reading_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Lectura no encontrada"
        )