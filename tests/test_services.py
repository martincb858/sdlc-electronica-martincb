import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta, timezone

from app.services.reading_service import ReadingService
from app.repositories.reading_repositorie import SqlAlchemyReadingRepository
from app.db import Base, ReadingModel


@pytest.fixture
def db_session() -> Session:
    """Crea una base de datos SQLite en memoria para tests."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    session = SessionLocal()
    
    yield session
    
    session.close()  
    engine.dispose()  
    Base.metadata.drop_all(engine)  


@pytest.fixture
def service(db_session: Session) -> ReadingService:
    repo = SqlAlchemyReadingRepository(db_session)
    return ReadingService(repo)


def test_service_records_valid_reading(service: ReadingService) -> None:
    result = service.record("TEMP-01", 25.5, "C")
    
    assert result.sensor_id == "TEMP-01"
    assert result.value == 25.5


def test_service_raises_error_below_absolute_zero(service: ReadingService) -> None:
    with pytest.raises(ValueError, match="Temperatura invalida"):
        service.record("TEMP-01", -300.0, "C")


def test_service_can_list_sensor_history(service: ReadingService) -> None:
    service.record("SENSOR-A", 10.0, "C")
    service.record("SENSOR-A", 12.5, "C")
    service.record("SENSOR-B", 99.0, "C")
    
    history = service.get_history("SENSOR-A")
    assert len(history) == 2
    assert history[0].value == 10.0
    assert history[1].value == 12.5


def test_service_can_get_reading_by_id(service: ReadingService) -> None:
    reading = service.record("SENSOR-01", 20.0, "C")
    retrieved = service.get_reading(reading.id)
    
    assert retrieved is not None
    assert retrieved.id == reading.id
    assert retrieved.value == 20.0


def test_service_update_reading(service: ReadingService) -> None:
    reading = service.record("SENSOR-01", 20.0, "C")
    updated = service.update_reading(reading.id, value=22.0, unit=None)
    
    assert updated is not None
    assert updated.value == 22.0
    assert updated.unit == "C"  # Unit remains unchanged

def test_service_delete_reading(service: ReadingService) -> None:
    reading = service.record("SENSOR-01", 20.0, "C")
    deleted = service.delete_reading(reading.id)
    
    assert deleted is True
    assert service.get_reading(reading.id) is None

def test_service_list_sensor_history_with_date_filters(
        service: ReadingService,
        db_session: Session
    ) -> None:

    reading1 = service.record("SENSOR-A", 10.0, "C")
    reading2 = service.record("SENSOR-A", 12.5, "C")
    reading3 = service.record("SENSOR-A", 15.0, "C")

    now = datetime.now(timezone.utc)
    past = now - timedelta(days=1)
    

    history = service.get_history(
        "SENSOR-A", 
        from_date=past 
    )
    assert len(history) == 3
    
    history = service.get_history(
        "SENSOR-A",
        to_date=now + timedelta(days=1)  
    )
    assert len(history) == 3
    
    history = service.get_history(
        "SENSOR-A",
        from_date=now - timedelta(hours=1), 
        to_date=now + timedelta(hours=1)
    )

    assert len(history) >= 1


def test_service_update_nonexistent_reading(service: ReadingService) -> None:

    result = service.update_reading(999, value=22.0, unit=None)
    assert result is None

def test_service_update_reading_no_changes(service: ReadingService) -> None:

    reading = service.record("SENSOR-01", 20.0, "C")
    updated = service.update_reading(reading.id, value=None, unit=None)
    
    assert updated is not None
    assert updated.value == 20.0
    assert updated.unit == "C"

def test_service_delete_nonexistent_reading(service: ReadingService) -> None:

    result = service.delete_reading(999)
    assert result is False

def test_reading_model_repr() -> None:

    from datetime import datetime, timezone
    
    reading = ReadingModel(
        id=1,
        sensor_id="TEMP-01",
        value=25.5,
        unit="C",
        created_at=datetime.now(timezone.utc)
    )
    
    repr_str = repr(reading)
    assert "Reading(id=1" in repr_str
    assert "sensor='TEMP-01'" in repr_str
    assert "val=25.5C" in repr_str