from datetime import datetime

from sqlalchemy.orm import Session

from app.db import ReadingModel


class SqlAlchemyReadingRepository:
    def __init__(self, db_session: Session) -> None:
        self._db = db_session

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:

        reading = ReadingModel(sensor_id=sensor_id, value=value, unit=unit)

        self._db.add(reading)
        self._db.commit()

        self._db.refresh(reading)
        return reading

    def list_for_sensor(
        self,
        sensor_id: str,
        limit: int,
        offset: int,
        from_date: datetime | None,
        to_date: datetime | None,
    ) -> list[ReadingModel]:

        query = self._db.query(ReadingModel).filter(ReadingModel.sensor_id == sensor_id)
        if from_date:
            query = query.filter(ReadingModel.created_at >= from_date)
        if to_date:
            query = query.filter(ReadingModel.created_at <= to_date)

        return query.offset(offset).limit(limit).all()

    def get_by_id(self, reading_id: int) -> ReadingModel | None:
        return (
            self._db.query(ReadingModel).filter(ReadingModel.id == reading_id).first()
        )

    def update(
        self,
        reading_id: int,
        value: float | None,
        unit: str | None,
    ) -> ReadingModel | None:

        reading = self.get_by_id(reading_id)
        if not reading:
            return None

        if value is not None:
            reading.value = value
        if unit is not None:
            reading.unit = unit

        self._db.commit()
        self._db.refresh(reading)
        return reading

    def delete(self, reading_id: int) -> bool:
        reading = self.get_by_id(reading_id)
        if not reading:
            return False
        self._db.delete(reading)
        self._db.commit()
        return True
