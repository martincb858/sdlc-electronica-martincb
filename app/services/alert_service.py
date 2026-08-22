from app.db import AlertModel
from app.domain.alert_states import validate_transition
from app.repositories.alert_repository import SqlAlchemyAlertRepository


class AlertNotFoundError(Exception):
    """Se lanza al referenciar una alerta que no existe."""


class AlertService:
    def __init__(self, repo: SqlAlchemyAlertRepository) -> None:
        self._repo = repo

    def list_alerts(
        self, sensor_id: str, status: str | None = None
    ) -> list[AlertModel]:
        return self._repo.list_for_sensor(sensor_id, status)

    def change_status(self, alert_id: int, new_status: str) -> AlertModel:
        alert = self._repo.get_by_id(alert_id)
        if alert is None:
            raise AlertNotFoundError(f"Alerta {alert_id} no encontrada.")

        validate_transition(alert.status, new_status)
        return self._repo.update_status(alert_id, new_status)
