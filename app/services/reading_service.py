from datetime import datetime

from app.db import ReadingModel
from app.repositories.reading_repositorie import SqlAlchemyReadingRepository
from app.validator import ValidatorRegistry, operational_registry


class ReadingService:
    def __init__(
        self,
        repo: SqlAlchemyReadingRepository,
        operational_registry: ValidatorRegistry = operational_registry,
    ) -> None:
        self._repo = repo
        self._operational_registry = operational_registry

    def record(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        unit = unit.upper()
        validator = self._operational_registry.get_optional(unit)
        if validator is not None:
            validator.validate(value)

        return self._repo.add(sensor_id, value, unit)

    def get_history(
        self,
        sensor_id: str,
        limit: int = 10,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[ReadingModel]:

        return self._repo.list_for_sensor(sensor_id, limit, offset, from_date, to_date)

    def get_reading(self, reading_id: int) -> ReadingModel | None:
        return self._repo.get_by_id(reading_id)

    def update_reading(
        self,
        reading_id: int,
        value: float | None,
        unit: str | None,
    ) -> ReadingModel | None:

        return self._repo.update(reading_id, value, unit)

    def delete_reading(self, reading_id: int) -> bool:
        return self._repo.delete(reading_id)