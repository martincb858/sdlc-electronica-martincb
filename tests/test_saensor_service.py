import pytest

from app.services.sensor_service import SensorAlreadyExistsError, SensorService


def test_register_creates_sensor(sensor_service: SensorService) -> None:
    sensor = sensor_service.register(
        "TEMP-01", "Sensor sala A", "TEMPERATURE", "Sala A"
    )

    assert sensor.code == "TEMP-01"
    assert sensor.name == "Sensor sala A"
    assert sensor.sensor_type == "TEMPERATURE"
    assert sensor.location == "Sala A"


def test_register_rejects_duplicate_code(sensor_service: SensorService) -> None:
    sensor_service.register("TEMP-01", "Sensor A", "TEMPERATURE", None)

    with pytest.raises(SensorAlreadyExistsError, match="TEMP-01"):
        sensor_service.register("TEMP-01", "Otro sensor", "TEMPERATURE", None)


def test_list_sensors_returns_all_registered(sensor_service: SensorService) -> None:
    sensor_service.register("TEMP-01", "A", "TEMPERATURE", None)
    sensor_service.register("HUM-01", "B", "HUMIDITY", None)

    sensors = sensor_service.list_sensors()
    assert {s.code for s in sensors} == {"TEMP-01", "HUM-01"}


def test_get_sensor_returns_none_if_missing(sensor_service: SensorService) -> None:
    assert sensor_service.get_sensor("NOPE") is None


def test_get_sensor_returns_existing_sensor(sensor_service: SensorService) -> None:
    sensor_service.register("TEMP-01", "A", "TEMPERATURE", None)
    found = sensor_service.get_sensor("temp-01")  # case-insensitive
    assert found is not None
    assert found.code == "TEMP-01"


def test_update_sensor_changes_name_and_location(sensor_service: SensorService) -> None:
    sensor_service.register("TEMP-01", "A", "TEMPERATURE", "Sala A")
    updated = sensor_service.update_sensor("TEMP-01", "Nuevo nombre", "Sala B")

    assert updated is not None
    assert updated.name == "Nuevo nombre"
    assert updated.location == "Sala B"


def test_update_sensor_returns_none_if_missing(sensor_service: SensorService) -> None:
    assert sensor_service.update_sensor("NOPE", "X", None) is None


def test_delete_sensor_removes_it(sensor_service: SensorService) -> None:
    sensor_service.register("TEMP-01", "A", "TEMPERATURE", None)
    assert sensor_service.delete_sensor("TEMP-01") is True
    assert sensor_service.get_sensor("TEMP-01") is None


def test_delete_sensor_returns_false_if_missing(sensor_service: SensorService) -> None:
    assert sensor_service.delete_sensor("NOPE") is False
