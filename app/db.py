import os
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)


def get_database_url() -> str:
    
    url = os.getenv("DATABASE_URL", "sqlite:///sensorhub.db")
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://") and "+psycopg" not in url:
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


DATABASE_URL = get_database_url()

_connect_args = (
    {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

engine = create_engine(DATABASE_URL, echo=False, connect_args=_connect_args)


SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class SensorModel(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str]
    sensor_type: Mapped[str] = mapped_column(index=True)
    location: Mapped[str | None] = mapped_column(default=None)

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    readings: Mapped[list["ReadingModel"]] = relationship(
        back_populates="sensor", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Sensor(id={self.id}, code='{self.code}', type='{self.sensor_type}')>"


class ReadingModel(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True)

    sensor_id: Mapped[str] = mapped_column(
        ForeignKey("sensors.code"), index=True
    )

    value: Mapped[float]
    unit: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    sensor: Mapped["SensorModel"] = relationship(back_populates="readings")

    def __repr__(self) -> str:
        return (
            f"<Reading(id={self.id}, sensor='{self.sensor_id}', "
            f"val={self.value}{self.unit})>"
        )