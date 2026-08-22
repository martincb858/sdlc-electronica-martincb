from fastapi.testclient import TestClient

from app.dependencies import get_sensor_service
from app.main import app


class _BrokenSensorService:
    def list_sensors(self, limit: int = 50, offset: int = 0):  # noqa: ANN201
        raise RuntimeError("boom: fallo interno inesperado")


def test_unhandled_exception_returns_generic_500_without_leaking_details(
    client: TestClient,
) -> None:
    app.dependency_overrides[get_sensor_service] = lambda: _BrokenSensorService()
    try:
        with TestClient(app, raise_server_exceptions=False) as no_raise_client:
            response = no_raise_client.get("/sensors")
    finally:
        del app.dependency_overrides[get_sensor_service]

    assert response.status_code == 500
    body = response.json()
    assert body == {"detail": "Error interno del servidor."}
    assert "RuntimeError" not in response.text
    assert "boom" not in response.text
