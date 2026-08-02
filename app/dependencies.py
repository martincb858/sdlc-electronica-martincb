from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.repositories.reading_repositorie import SqlAlchemyReadingRepository
from app.repositories.sensor_repository import SqlAlchemySensorRepository
from app.services.reading_service import ReadingService
from app.services.sensor_service import SensorService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_sensor_service(db: Session = Depends(get_db)) -> SensorService:
    return SensorService(SqlAlchemySensorRepository(db))


def get_reading_service(db: Session = Depends(get_db)) -> ReadingService:
    return ReadingService(
        SqlAlchemyReadingRepository(db),
        SqlAlchemySensorRepository(db),
    )
