from unittest.mock import Mock

from app.domain.alerts import AlertStrategy
from app.services.anomaly_detector_service import AnomalyDetectorService


def test_process_reading_triggers_alert_when_value_exceeds_threshold() -> None:
    mock_strategy = Mock(spec=AlertStrategy)
    thresholds = {"TEMP-01": 30.0}
    service = AnomalyDetectorService(
        alert_strategy=mock_strategy, thresholds=thresholds
    )

    service.process_reading("TEMP-01", 35.5)

    mock_strategy.notify.assert_called_once_with("TEMP-01", 35.5, 30.0)


def test_process_reading_does_not_trigger_alert_when_value_below_threshold() -> None:
    mock_strategy = Mock(spec=AlertStrategy)
    thresholds = {"TEMP-01": 30.0}
    service = AnomalyDetectorService(
        alert_strategy=mock_strategy, thresholds=thresholds
    )

    service.process_reading("TEMP-01", 25.0)

    mock_strategy.notify.assert_not_called()


def test_process_reading_does_not_trigger_alert_when_value_equals_threshold() -> None:
    mock_strategy = Mock(spec=AlertStrategy)
    thresholds = {"TEMP-01": 30.0}
    service = AnomalyDetectorService(
        alert_strategy=mock_strategy, thresholds=thresholds
    )

    service.process_reading("TEMP-01", 30.0)

    mock_strategy.notify.assert_not_called()
