import pytest

from app.domain.alert_states import ACKNOWLEDGED, OPEN, RESOLVED
from app.repositories.alert_repository import SqlAlchemyAlertRepository
from app.services.alert_service import AlertNotFoundError, AlertService
from app.services.sensor_service import SensorService


@pytest.fixture
def alert_repo(db_session) -> SqlAlchemyAlertRepository:
    return SqlAlchemyAlertRepository(db_session)


@pytest.fixture
def alert_service(alert_repo: SqlAlchemyAlertRepository) -> AlertService:
    return AlertService(alert_repo)


def _open_alert(db_session, sensor_service: SensorService, alert_repo):
    sensor_service.register("TEMP-01", "A", "TEMPERATURE", None)
    from app.db import AlertModel

    alert = AlertModel(sensor_id="TEMP-01", value=35.0, threshold=30.0, status=OPEN)
    db_session.add(alert)
    db_session.commit()
    db_session.refresh(alert)
    return alert


def test_list_alerts_filters_by_status(
    db_session, sensor_service: SensorService, alert_repo, alert_service: AlertService
) -> None:
    alert = _open_alert(db_session, sensor_service, alert_repo)

    open_alerts = alert_service.list_alerts("TEMP-01", status=OPEN)
    assert len(open_alerts) == 1
    assert open_alerts[0].id == alert.id

    resolved_alerts = alert_service.list_alerts("TEMP-01", status=RESOLVED)
    assert resolved_alerts == []


def test_change_status_open_to_acknowledged(
    db_session, sensor_service: SensorService, alert_repo, alert_service: AlertService
) -> None:
    alert = _open_alert(db_session, sensor_service, alert_repo)

    updated = alert_service.change_status(alert.id, ACKNOWLEDGED)
    assert updated.status == ACKNOWLEDGED


def test_change_status_rejects_backwards_transition(
    db_session, sensor_service: SensorService, alert_repo, alert_service: AlertService
) -> None:
    alert = _open_alert(db_session, sensor_service, alert_repo)
    alert_service.change_status(alert.id, RESOLVED)

    with pytest.raises(Exception, match="[Ii]nv[aá]lid"):
        alert_service.change_status(alert.id, OPEN)


def test_change_status_raises_for_unknown_alert(alert_service: AlertService) -> None:
    with pytest.raises(AlertNotFoundError):
        alert_service.change_status(999, ACKNOWLEDGED)
