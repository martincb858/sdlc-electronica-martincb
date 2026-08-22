from dataclasses import dataclass

from app.domain.alert_states import ACKNOWLEDGED, OPEN, RESOLVED
from app.repositories.alert_repository import SqlAlchemyAlertRepository
from app.repositories.reading_repositorie import SqlAlchemyReadingRepository
from app.repositories.sensor_repository import SqlAlchemySensorRepository


@dataclass(frozen=True)
class Metrics:
    sensors_total: int
    sensors_active: int
    readings_total: int
    alerts_open: int
    alerts_acknowledged: int
    alerts_resolved: int


class MetricsService:
    def __init__(
        self,
        sensor_repo: SqlAlchemySensorRepository,
        reading_repo: SqlAlchemyReadingRepository,
        alert_repo: SqlAlchemyAlertRepository,
    ) -> None:
        self._sensor_repo = sensor_repo
        self._reading_repo = reading_repo
        self._alert_repo = alert_repo

    def get_metrics(self) -> Metrics:
        return Metrics(
            sensors_total=self._sensor_repo.count_total(),
            sensors_active=self._sensor_repo.count_active(),
            readings_total=self._reading_repo.count_total(),
            alerts_open=self._alert_repo.count_by_status(OPEN),
            alerts_acknowledged=self._alert_repo.count_by_status(ACKNOWLEDGED),
            alerts_resolved=self._alert_repo.count_by_status(RESOLVED),
        )
