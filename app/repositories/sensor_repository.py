from sqlalchemy.orm import Session

from app.db import SensorModel


class SqlAlchemySensorRepository:
    def __init__(self, db_session: Session) -> None:
        self._db = db_session

    def add(
        self, code: str, name: str, sensor_type: str, location: str | None
    ) -> SensorModel:

        sensor = SensorModel(
            code=code, name=name, sensor_type=sensor_type, location=location
        )

        self._db.add(sensor)
        self._db.commit()
        self._db.refresh(sensor)
        return sensor

    def list_all(self, limit: int, offset: int) -> list[SensorModel]:
        return self._db.query(SensorModel).offset(offset).limit(limit).all()

    def get_by_code(self, code: str) -> SensorModel | None:
        return (
            self._db.query(SensorModel)
            .filter(SensorModel.code == code.upper())
            .first()
        )

    def update(
        self, code: str, name: str | None, location: str | None
    ) -> SensorModel | None:

        sensor = self.get_by_code(code)
        if not sensor:
            return None

        if name is not None:
            sensor.name = name
        if location is not None:
            sensor.location = location

        self._db.commit()
        self._db.refresh(sensor)
        return sensor

    def delete(self, code: str) -> bool:
        sensor = self.get_by_code(code)
        if not sensor:
            return False
        self._db.delete(sensor)
        self._db.commit()
        return True