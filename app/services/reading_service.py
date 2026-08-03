from datetime import datetime

from app.db import ReadingModel
from app.domain.sensor_types import SensorTypeRegistry, sensor_type_registry
from app.domain.validators import (
    ValidatorRegistry,
    operational_registry,
    physics_registry,
)
from app.repositories.reading_repositorie import SqlAlchemyReadingRepository
from app.repositories.sensor_repository import SqlAlchemySensorRepository


class SensorNotFoundError(Exception):
    """Se lanza al referenciar un sensor que no existe (al crear o actualizar
    una lectura)."""


class ReadingService:
    def __init__(
        self,
        repo: SqlAlchemyReadingRepository,
        sensor_repo: SqlAlchemySensorRepository,
        physics_registry: ValidatorRegistry = physics_registry,
        operational_registry: ValidatorRegistry = operational_registry,
        sensor_type_registry: SensorTypeRegistry = sensor_type_registry,
    ) -> None:
        self._repo = repo
        self._sensor_repo = sensor_repo
        self._physics_registry = physics_registry
        self._operational_registry = operational_registry
        self._sensor_type_registry = sensor_type_registry

    def _validate_reading(self, sensor_id: str, value: float, unit: str) -> None:

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

        operational_validator = self._operational_registry.get_optional(unit)
        if operational_validator is not None:
            operational_validator.validate(value)

        physics_validator = self._physics_registry.get_optional(unit)
        if physics_validator is not None:
            physics_validator.validate(value)

    def record(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        unit = unit.upper()
        self._validate_reading(sensor_id, value, unit)
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

        existing = self._repo.get_by_id(reading_id)
        if existing is None:
            return None

        final_value = value if value is not None else existing.value
        final_unit = unit.upper() if unit is not None else existing.unit

        self._validate_reading(existing.sensor_id, final_value, final_unit)

        normalized_unit = unit.upper() if unit is not None else None
        return self._repo.update(reading_id, value, normalized_unit)

    def delete_reading(self, reading_id: int) -> bool:
        return self._repo.delete(reading_id)
