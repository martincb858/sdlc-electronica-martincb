from app.db import SensorModel
from app.repositories.sensor_repository import SqlAlchemySensorRepository


class SensorAlreadyExistsError(Exception):
    """Se lanza al intentar registrar un sensor con un `code` ya usado."""


class SensorService:
    def __init__(self, repo: SqlAlchemySensorRepository) -> None:
        self._repo = repo

    def register(
        self, code: str, name: str, sensor_type: str, location: str | None
    ) -> SensorModel:
        if self._repo.get_by_code(code) is not None:
            raise SensorAlreadyExistsError(
                f"Ya existe un sensor registrado con code '{code}'."
            )
        return self._repo.add(code, name, sensor_type, location)

    def list_sensors(self, limit: int = 50, offset: int = 0) -> list[SensorModel]:
        return self._repo.list_all(limit, offset)

    def get_sensor(self, code: str) -> SensorModel | None:
        return self._repo.get_by_code(code)

    def update_sensor(
        self, code: str, name: str | None, location: str | None
    ) -> SensorModel | None:
        return self._repo.update(code, name, location)

    def delete_sensor(self, code: str) -> bool:
        return self._repo.delete(code)