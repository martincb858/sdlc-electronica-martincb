from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

engine = create_engine("sqlite:///sensorhub.db", echo=True)


SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class ReadingModel(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True)

    sensor_id: Mapped[str] = mapped_column(index=True)

    value: Mapped[float]
    unit: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return (
            f"<Reading(id={self.id}, sensor='{self.sensor_id}', "
            f"val={self.value}{self.unit})>"
        )