from datetime import datetime
from typing import Protocol

from app.db import ReadingModel


class ReadingRepository(Protocol):
    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel: ...
    def list_for_sensor(self, sensor_id: str) -> list[ReadingModel]: ...


class ReadingService:
    def __init__(self, repo: ReadingRepository) -> None:
        self._repo = repo

    def record(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        if unit.upper() == "C" and value < -25.0:
            raise ValueError("Temperatura invalida")

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
