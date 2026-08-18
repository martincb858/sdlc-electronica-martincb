from fastapi.testclient import TestClient


def _create_sensor(client: TestClient, code="TEMP-01", sensor_type="TEMPERATURE"):
    return client.post(
        "/sensors",
        json={
            "code": code,
            "name": "Sensor de prueba",
            "sensor_type": sensor_type,
            "location": "Sala A",
        },
    )


def test_create_sensor_returns_201(client: TestClient) -> None:
    response = _create_sensor(client)

    assert response.status_code == 201
    body = response.json()
    assert body["code"] == "TEMP-01"
    assert body["sensor_type"] == "TEMPERATURE"
    assert "id" in body
    assert "created_at" in body


def test_create_sensor_normalizes_code_and_type_to_uppercase(
    client: TestClient,
) -> None:
    response = client.post(
        "/sensors",
        json={"code": "temp-02", "name": "X", "sensor_type": "temperature"},
    )
    assert response.status_code == 201
    assert response.json()["code"] == "TEMP-02"
    assert response.json()["sensor_type"] == "TEMPERATURE"


def test_create_sensor_rejects_unknown_sensor_type(client: TestClient) -> None:
    response = client.post(
        "/sensors",
        json={"code": "X-01", "name": "X", "sensor_type": "PRESSURE"},
    )
    assert response.status_code == 422  # error de validación Pydantic


def test_create_sensor_rejects_duplicate_code(client: TestClient) -> None:
    _create_sensor(client)
    response = _create_sensor(client)

    assert response.status_code == 409


def test_list_sensors_returns_created_sensors(client: TestClient) -> None:
    _create_sensor(client, code="TEMP-01")
    _create_sensor(client, code="HUM-01", sensor_type="HUMIDITY")

    response = client.get("/sensors")
    assert response.status_code == 200
    codes = {s["code"] for s in response.json()}
    assert codes == {"TEMP-01", "HUM-01"}


def test_get_sensor_by_code(client: TestClient) -> None:
    _create_sensor(client)

    response = client.get("/sensors/TEMP-01")
    assert response.status_code == 200
    assert response.json()["code"] == "TEMP-01"


def test_get_sensor_returns_404_if_missing(client: TestClient) -> None:
    response = client.get("/sensors/NOPE")
    assert response.status_code == 404


def test_update_sensor_changes_name(client: TestClient) -> None:
    _create_sensor(client)

    response = client.patch("/sensors/TEMP-01", json={"name": "Nuevo nombre"})
    assert response.status_code == 200
    assert response.json()["name"] == "Nuevo nombre"


def test_update_sensor_returns_404_if_missing(client: TestClient) -> None:
    response = client.patch("/sensors/NOPE", json={"name": "X"})
    assert response.status_code == 404


def test_delete_sensor_returns_204(client: TestClient) -> None:
    _create_sensor(client)

    response = client.delete("/sensors/TEMP-01")
    assert response.status_code == 204
    assert client.get("/sensors/TEMP-01").status_code == 404


def test_delete_sensor_returns_404_if_missing(client: TestClient) -> None:
    response = client.delete("/sensors/NOPE")
    assert response.status_code == 404


def test_swagger_docs_are_served(client: TestClient) -> None:
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema_includes_sensor_and_reading_paths(client: TestClient) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/sensors" in paths
    assert "/sensors/{sensor_code}" in paths
    assert "/sensors/{sensor_code}/readings" in paths
    assert "/sensors/{sensor_code}/alerts" in paths
    assert "/readings/{reading_id}" in paths
