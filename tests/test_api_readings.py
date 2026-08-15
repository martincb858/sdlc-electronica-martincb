from fastapi.testclient import TestClient


def _create_sensor(
    client: TestClient, code="TEMP-01", sensor_type="TEMPERATURE"
) -> None:
    client.post(
        "/sensors",
        json={"code": code, "name": "Sensor de prueba", "sensor_type": sensor_type},
    )


def test_create_reading_returns_201(client: TestClient) -> None:
    _create_sensor(client)

    response = client.post(
        "/sensors/TEMP-01/readings", json={"value": 24.5, "unit": "C"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["sensor_id"] == "TEMP-01"
    assert body["value"] == 24.5
    assert body["unit"] == "C"


def test_create_reading_returns_404_for_unknown_sensor(client: TestClient) -> None:
    response = client.post("/sensors/NOPE/readings", json={"value": 20.0, "unit": "C"})
    assert response.status_code == 404


def test_create_reading_rejects_physically_impossible_value(
    client: TestClient,
) -> None:
    _create_sensor(client)

    response = client.post(
        "/sensors/TEMP-01/readings", json={"value": -300.0, "unit": "C"}
    )
    assert response.status_code == 422


def test_create_reading_rejects_unknown_unit(client: TestClient) -> None:
    _create_sensor(client)

    response = client.post(
        "/sensors/TEMP-01/readings", json={"value": 10.0, "unit": "XX"}
    )
    assert response.status_code == 422


def test_create_reading_rejects_unit_incompatible_with_sensor_type(
    client: TestClient,
) -> None:
    _create_sensor(client, code="TEMP-01", sensor_type="TEMPERATURE")

    response = client.post(
        "/sensors/TEMP-01/readings", json={"value": 50.0, "unit": "RH"}
    )
    assert response.status_code == 400


def test_create_reading_rejects_below_operational_threshold(
    client: TestClient,
) -> None:
    _create_sensor(client)

    response = client.post(
        "/sensors/TEMP-01/readings", json={"value": -30.0, "unit": "C"}
    )
    assert response.status_code == 400
    assert "Temperatura invalida" in response.json()["detail"]


def test_list_readings_for_sensor(client: TestClient) -> None:
    _create_sensor(client)
    client.post("/sensors/TEMP-01/readings", json={"value": 10.0, "unit": "C"})
    client.post("/sensors/TEMP-01/readings", json={"value": 12.5, "unit": "C"})

    response = client.get("/sensors/TEMP-01/readings")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_reading_by_id(client: TestClient) -> None:
    _create_sensor(client)
    created = client.post(
        "/sensors/TEMP-01/readings", json={"value": 20.0, "unit": "C"}
    ).json()

    response = client.get(f"/readings/{created['id']}")
    assert response.status_code == 200
    assert response.json()["value"] == 20.0


def test_get_reading_returns_404_if_missing(client: TestClient) -> None:
    response = client.get("/readings/999")
    assert response.status_code == 404


def test_update_reading(client: TestClient) -> None:
    _create_sensor(client)
    created = client.post(
        "/sensors/TEMP-01/readings", json={"value": 20.0, "unit": "C"}
    ).json()

    response = client.patch(f"/readings/{created['id']}", json={"value": 22.0})
    assert response.status_code == 200
    assert response.json()["value"] == 22.0


def test_update_reading_returns_404_if_missing(client: TestClient) -> None:
    response = client.patch("/readings/999", json={"value": 22.0})
    assert response.status_code == 404


def test_delete_reading(client: TestClient) -> None:
    _create_sensor(client)
    created = client.post(
        "/sensors/TEMP-01/readings", json={"value": 20.0, "unit": "C"}
    ).json()

    response = client.delete(f"/readings/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/readings/{created['id']}").status_code == 404


def test_delete_reading_returns_404_if_missing(client: TestClient) -> None:
    response = client.delete("/readings/999")
    assert response.status_code == 404


def test_list_readings_returns_404_for_unknown_sensor(client: TestClient) -> None:
    # Antes, get_history() nunca verificaba que el sensor existiera, asi
    # que esto devolvia 200 con una lista vacia en vez de 404.
    response = client.get("/sensors/NOPE/readings")
    assert response.status_code == 404


def test_create_reading_rejects_empty_sensor_code(client: TestClient) -> None:
    response = client.post("/sensors//readings", json={"value": 20.0, "unit": "C"})
    # FastAPI trata "//readings" como una ruta que no matchea con un
    # segmento vacio -> 404 de enrutamiento, no 422. Se deja explicito
    # para documentar el comportamiento real observado.
    assert response.status_code == 404


def test_list_readings_rejects_sensor_code_too_long(client: TestClient) -> None:
    long_code = "X" * 51
    response = client.get(f"/sensors/{long_code}/readings")
    assert response.status_code == 422


def test_openapi_documents_error_responses_for_reading_endpoints(
    client: TestClient,
) -> None:
    paths = client.get("/openapi.json").json()["paths"]

    create_responses = paths["/sensors/{sensor_code}/readings"]["post"]["responses"]
    assert "404" in create_responses
    assert "400" in create_responses

    update_responses = paths["/readings/{reading_id}"]["patch"]["responses"]
    assert "404" in update_responses
    assert "400" in update_responses

    delete_responses = paths["/readings/{reading_id}"]["delete"]["responses"]
    assert "404" in delete_responses