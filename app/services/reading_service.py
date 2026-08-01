from datetime import datetime
from typing import Protocol

from app.db import ReadingModel


class ReadingRepository(Protocol):
    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel: ...
    def list_for_sensor(
        self, 
        sensor_id: str, 
        limit: int, 
        offset: int, 
        from_date: datetime | None, 
        to_date: datetime | None
    ) -> list[ReadingModel]: ...
    
    # Nuevos "pines" en nuestro contrato para soportar REST completo
    def get_by_id(self, reading_id: int) -> ReadingModel | None: ...
    def update(
        self, 
        reading_id: int, 
        value: float | None, 
        unit: str | None
        ) -> ReadingModel | None: ...
    def delete(self, reading_id: int) -> bool: ...


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

    def get_reading(
        self, 
        reading_id: int
        ) -> ReadingModel | None:

        return self._repo.get_by_id(reading_id)
        
    def update_reading(
        self, 
        reading_id: int, 
        value: float | None, 
        unit: str | None
        ) -> ReadingModel | None:

        if unit and unit.upper() == "C" and value is not None and value < -25:
            raise ValueError("Temperatura por debajo del cero absoluto")
        return self._repo.update(reading_id, value, unit)
        
    def delete_reading(self, reading_id: int) -> bool:
        return self._repo.delete(reading_id)
