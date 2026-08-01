from datetime import datetime

from app.db import ReadingModel
from app.domain.sensor_types import SensorTypeRegistry, sensor_type_registry
from app.domain.validators import ValidatorRegistry, operational_registry
from app.repositories.reading_repositorie import SqlAlchemyReadingRepository
from app.repositories.sensor_repository import SqlAlchemySensorRepository


class SensorNotFoundError(Exception):
    """Se lanza al intentar registrar una lectura para un sensor inexistente."""


class ReadingService:
    def __init__(
        self,
        repo: SqlAlchemyReadingRepository,
        sensor_repo: SqlAlchemySensorRepository,
        operational_registry: ValidatorRegistry = operational_registry,
        sensor_type_registry: SensorTypeRegistry = sensor_type_registry,
    ) -> None:
        self._repo = repo
        self._sensor_repo = sensor_repo
    
        self._operational_registry = operational_registry
        self._sensor_type_registry = sensor_type_registry

    def record(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        unit = unit.upper()

        sensor = self._sensor_repo.get_by_code(sensor_id)
        if sensor is None:
            raise SensorNotFoundError(f"Sensor '{sensor_id}' no encontrado.")

        type_spec = self._sensor_type_registry.get_optional(sensor.sensor_type)
        if type_spec is not None and unit not in type_spec.accepted_units:
            accepted = ", ".join(sorted(type_spec.accepted_units))
            raise ValueError(
                f"Unidad '{unit}' no es valida para sensores de tipo "
                f"{sensor.sensor_type} (use: {accepted})."
            )

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