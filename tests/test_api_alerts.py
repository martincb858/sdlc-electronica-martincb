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
