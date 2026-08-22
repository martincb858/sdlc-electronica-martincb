from fastapi.testclient import TestClient


def test_health_check_returns_ok(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_metrics_returns_zero_counts_when_empty(client: TestClient) -> None:
    response = client.get("/metrics")
    assert response.status_code == 200
    body = response.json()
    assert body == {
        "sensors_total": 0,
        "sensors_active": 0,
        "readings_total": 0,
        "alerts_open": 0,
        "alerts_acknowledged": 0,
        "alerts_resolved": 0,
    }


def test_metrics_reflects_created_sensors_and_readings(client: TestClient) -> None:
    client.post(
        "/sensors",
        json={"code": "TEMP-01", "name": "X", "sensor_type": "TEMPERATURE"},
    )
    client.post("/sensors/TEMP-01/readings", json={"value": 20.0, "unit": "C"})
    client.delete("/sensors/TEMP-01")

    response = client.get("/metrics")
    body = response.json()
    assert body["sensors_total"] == 1
    assert body["sensors_active"] == 0
    assert body["readings_total"] == 1
