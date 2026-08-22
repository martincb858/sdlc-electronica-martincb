from unittest.mock import Mock

from app.repositories.alert_repository import SqlAlchemyAlertRepository
from app.repositories.reading_repositorie import SqlAlchemyReadingRepository
from app.repositories.sensor_repository import SqlAlchemySensorRepository
from app.services.metrics_service import MetricsService


def test_get_metrics_aggregates_counts_from_repositories() -> None:
    sensor_repo = Mock(spec=SqlAlchemySensorRepository)
    sensor_repo.count_total.return_value = 5
    sensor_repo.count_active.return_value = 4

    reading_repo = Mock(spec=SqlAlchemyReadingRepository)
    reading_repo.count_total.return_value = 120

    alert_repo = Mock(spec=SqlAlchemyAlertRepository)
    alert_repo.count_by_status.side_effect = lambda status: {
        "open": 2,
        "acknowledged": 1,
        "resolved": 3,
    }[status]

    service = MetricsService(sensor_repo, reading_repo, alert_repo)
    metrics = service.get_metrics()

    assert metrics.sensors_total == 5
    assert metrics.sensors_active == 4
    assert metrics.readings_total == 120
    assert metrics.alerts_open == 2
    assert metrics.alerts_acknowledged == 1
    assert metrics.alerts_resolved == 3
