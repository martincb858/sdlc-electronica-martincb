from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.domain.alerts import DatabaseAlertStrategy
from app.repositories.alert_repository import SqlAlchemyAlertRepository
from app.repositories.reading_repositorie import SqlAlchemyReadingRepository
from app.repositories.sensor_repository import SqlAlchemySensorRepository
from app.services.anomaly_detector_service import AnomalyDetectorService
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


def get_alert_repository(db: Session = Depends(get_db)) -> SqlAlchemyAlertRepository:
    return SqlAlchemyAlertRepository(db)


def get_anomaly_detector_service(
    db: Session = Depends(get_db),
) -> AnomalyDetectorService:
    db_strategy = DatabaseAlertStrategy(db)
    return AnomalyDetectorService(alert_strategy=db_strategy)


def get_reading_service(
    db: Session = Depends(get_db),
    anomaly_detector: AnomalyDetectorService = Depends(get_anomaly_detector_service),
) -> ReadingService:
    return ReadingService(
        SqlAlchemyReadingRepository(db),
        SqlAlchemySensorRepository(db),
        anomaly_detector=anomaly_detector,
    )
