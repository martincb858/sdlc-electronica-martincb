from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.domain.alerts import DatabaseAlertStrategy


def _create_sensor(
    client: TestClient, code: str = "TEMP-01", sensor_type: str = "TEMPERATURE"
) -> None:
    client.post(
        "/sensors",
        json={"code": code, "name": "Sensor de prueba", "sensor_type": sensor_type},
    )


def test_get_sensor_alerts_returns_empty_list_when_no_alerts(
    client: TestClient,
) -> None:
    _create_sensor(client, code="TEMP-01")

    response = client.get("/sensors/TEMP-01/alerts")
    assert response.status_code == 200
    assert response.json() == []


def test_get_sensor_alerts_returns_serialized_alerts(
    client: TestClient, db_session: Session
) -> None:
    _create_sensor(client, code="TEMP-01")

    # Persistimos alertas usando DatabaseAlertStrategy
    db_strategy = DatabaseAlertStrategy(db_session=db_session)
    db_strategy.notify(sensor_id="TEMP-01", value=35.5, threshold=30.0)
    db_strategy.notify(sensor_id="TEMP-01", value=38.0, threshold=30.0)

    response = client.get("/sensors/TEMP-01/alerts")
    assert response.status_code == 200

    alerts = response.json()
    assert len(alerts) == 2

    first_alert = alerts[0]
    assert first_alert["sensor_id"] == "TEMP-01"
    assert first_alert["value"] == 35.5
    assert first_alert["threshold"] == 30.0
    assert "id" in first_alert
    assert "created_at" in first_alert


def test_get_sensor_alerts_returns_404_for_nonexistent_sensor(
    client: TestClient,
) -> None:
    response = client.get("/sensors/NOPE/alerts")
    assert response.status_code == 404


def test_new_alerts_are_created_open(client: TestClient, db_session: Session) -> None:
    _create_sensor(client, code="TEMP-01")
    db_strategy = DatabaseAlertStrategy(db_session=db_session)
    db_strategy.notify(sensor_id="TEMP-01", value=35.5, threshold=30.0)

    alerts = client.get("/sensors/TEMP-01/alerts").json()
    assert alerts[0]["status"] == "open"


def test_filter_alerts_by_status(client: TestClient, db_session: Session) -> None:
    _create_sensor(client, code="TEMP-01")
    db_strategy = DatabaseAlertStrategy(db_session=db_session)
    db_strategy.notify(sensor_id="TEMP-01", value=35.5, threshold=30.0)
    alert_id = client.get("/sensors/TEMP-01/alerts").json()[0]["id"]

    client.patch(f"/alerts/{alert_id}", json={"status": "resolved"})

    open_alerts = client.get("/sensors/TEMP-01/alerts?status=open").json()
    assert open_alerts == []

    resolved_alerts = client.get("/sensors/TEMP-01/alerts?status=resolved").json()
    assert len(resolved_alerts) == 1


def test_patch_alert_status_open_to_acknowledged(
    client: TestClient, db_session: Session
) -> None:
    _create_sensor(client, code="TEMP-01")
    db_strategy = DatabaseAlertStrategy(db_session=db_session)
    db_strategy.notify(sensor_id="TEMP-01", value=35.5, threshold=30.0)
    alert_id = client.get("/sensors/TEMP-01/alerts").json()[0]["id"]

    response = client.patch(f"/alerts/{alert_id}", json={"status": "acknowledged"})
    assert response.status_code == 200
    assert response.json()["status"] == "acknowledged"


def test_patch_alert_status_rejects_backwards_transition(
    client: TestClient, db_session: Session
) -> None:
    _create_sensor(client, code="TEMP-01")
    db_strategy = DatabaseAlertStrategy(db_session=db_session)
    db_strategy.notify(sensor_id="TEMP-01", value=35.5, threshold=30.0)
    alert_id = client.get("/sensors/TEMP-01/alerts").json()[0]["id"]

    client.patch(f"/alerts/{alert_id}", json={"status": "resolved"})
    response = client.patch(f"/alerts/{alert_id}", json={"status": "open"})
    assert response.status_code == 400


def test_patch_alert_status_returns_404_for_unknown_alert(client: TestClient) -> None:
    response = client.patch("/alerts/999", json={"status": "acknowledged"})
    assert response.status_code == 404


def test_patch_alert_status_rejects_unknown_status(
    client: TestClient, db_session: Session
) -> None:
    _create_sensor(client, code="TEMP-01")
    db_strategy = DatabaseAlertStrategy(db_session=db_session)
    db_strategy.notify(sensor_id="TEMP-01", value=35.5, threshold=30.0)
    alert_id = client.get("/sensors/TEMP-01/alerts").json()[0]["id"]

    response = client.patch(f"/alerts/{alert_id}", json={"status": "closed"})
    assert response.status_code == 400
