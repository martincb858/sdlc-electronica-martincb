import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base
from app.dependencies import get_db
from app.main import app
from app.repositories.reading_repositorie import SqlAlchemyReadingRepository
from app.repositories.sensor_repository import SqlAlchemySensorRepository
from app.services.reading_service import ReadingService
from app.services.sensor_service import SensorService


@pytest.fixture
def db_session():
    
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    session = SessionLocal()

    yield session

    session.close()
    engine.dispose()


@pytest.fixture
def sensor_repo(db_session: Session) -> SqlAlchemySensorRepository:
    return SqlAlchemySensorRepository(db_session)


@pytest.fixture
def reading_repo(db_session: Session) -> SqlAlchemyReadingRepository:
    return SqlAlchemyReadingRepository(db_session)


@pytest.fixture
def sensor_service(sensor_repo: SqlAlchemySensorRepository) -> SensorService:
    return SensorService(sensor_repo)


@pytest.fixture
def reading_service(
    reading_repo: SqlAlchemyReadingRepository,
    sensor_repo: SqlAlchemySensorRepository,
) -> ReadingService:
    return ReadingService(reading_repo, sensor_repo)


@pytest.fixture
def client(db_session: Session):
    """TestClient de integración: la app real corre contra la misma
    sesión de base de datos en memoria, sustituyendo únicamente get_db.
    """

    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()