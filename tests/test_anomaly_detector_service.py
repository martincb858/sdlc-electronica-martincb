from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.domain.alerts import (
    AlertStrategy,
    ConsoleAlertStrategy,
    DatabaseAlertStrategy,
)
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


def test_process_reading_with_multiple_strategies() -> None:
    mock_strategy_1 = Mock(spec=AlertStrategy)
    mock_strategy_2 = Mock(spec=AlertStrategy)
    thresholds = {"TEMP-01": 20.0}
    service = AnomalyDetectorService(
        alert_strategy=[mock_strategy_1, mock_strategy_2],
        thresholds=thresholds,
    )

    service.process_reading("TEMP-01", 25.0)

    mock_strategy_1.notify.assert_called_once_with("TEMP-01", 25.0, 20.0)
    mock_strategy_2.notify.assert_called_once_with("TEMP-01", 25.0, 20.0)


def test_process_reading_ignores_sensors_without_threshold() -> None:
    mock_strategy = Mock(spec=AlertStrategy)
    thresholds = {"TEMP-01": 30.0}
    service = AnomalyDetectorService(
        alert_strategy=mock_strategy, thresholds=thresholds
    )

    service.process_reading("HUM-01", 80.0)

    mock_strategy.notify.assert_not_called()


def test_console_alert_strategy_prints_alert(capsys: pytest.CaptureFixture[str]) -> None:
    strategy = ConsoleAlertStrategy()
    strategy.notify("TEMP-01", 45.0, 40.0)

    captured = capsys.readouterr()
    assert "[ALERTA CONSOLA]" in captured.out
    assert "TEMP-01" in captured.out
    assert "45.0" in captured.out


def test_database_alert_strategy_instantiation() -> None:
    mock_session = Mock(spec=Session)
    strategy = DatabaseAlertStrategy(db_session=mock_session)
    strategy.notify("TEMP-01", 45.0, 40.0)
