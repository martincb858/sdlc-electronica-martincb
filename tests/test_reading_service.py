from datetime import datetime, timedelta, timezone

import pytest

from app.db import ReadingModel, SensorModel
from app.services.reading_service import ReadingService, SensorNotFoundError
from app.services.sensor_service import SensorService


@pytest.fixture
def temp_sensor(sensor_service: SensorService) -> SensorModel:
    return sensor_service.register("TEMP-01", "Sensor sala A", "TEMPERATURE", None)


def test_service_records_valid_reading(
    reading_service: ReadingService, temp_sensor: ReadingModel
) -> None:
    result = reading_service.record("TEMP-01", 25.5, "C")

    assert result.sensor_id == "TEMP-01"
    assert result.value == 25.5


def test_service_raises_error_below_absolute_zero(
    reading_service: ReadingService, temp_sensor: ReadingModel
) -> None:
    with pytest.raises(ValueError, match="Temperatura invalida"):
        reading_service.record("TEMP-01", -300.0, "C")


def test_service_raises_sensor_not_found_for_unknown_sensor(
    reading_service: ReadingService,
) -> None:
    with pytest.raises(SensorNotFoundError, match="NOPE"):
        reading_service.record("NOPE", 20.0, "C")


def test_service_rejects_unit_incompatible_with_sensor_type(
    reading_service: ReadingService, temp_sensor: ReadingModel
) -> None:
    # TEMP-01 es de tipo TEMPERATURE, no admite RH aunque RH sea una
    # unidad físicamente válida en general.
    with pytest.raises(ValueError, match="no es valida para sensores de tipo"):
        reading_service.record("TEMP-01", 50.0, "RH")


def test_service_can_list_sensor_history(
    reading_service: ReadingService, sensor_service: SensorService
) -> None:
    sensor_service.register("SENSOR-A", "A", "TEMPERATURE", None)
    sensor_service.register("SENSOR-B", "B", "TEMPERATURE", None)

    reading_service.record("SENSOR-A", 10.0, "C")
    reading_service.record("SENSOR-A", 12.5, "C")
    reading_service.record("SENSOR-B", 99.0, "C")

    history = reading_service.get_history("SENSOR-A")
    assert len(history) == 2
    assert history[0].value == 10.0
    assert history[1].value == 12.5


def test_service_can_get_reading_by_id(
    reading_service: ReadingService, temp_sensor: ReadingModel
) -> None:
    reading = reading_service.record("TEMP-01", 20.0, "C")
    retrieved = reading_service.get_reading(reading.id)

    assert retrieved is not None
    assert retrieved.id == reading.id
    assert retrieved.value == 20.0


def test_service_update_reading(
        reading_service: ReadingService, 
        temp_sensor: ReadingModel
    ) -> None:
    reading = reading_service.record("TEMP-01", 20.0, "C")
    updated = reading_service.update_reading(reading.id, value=22.0, unit=None)

    assert updated is not None
    assert updated.value == 22.0
    assert updated.unit == "C"  # Unit remains unchanged


def test_service_delete_reading(
        reading_service: ReadingService, 
        temp_sensor: ReadingModel
    ) -> None:
    reading = reading_service.record("TEMP-01", 20.0, "C")
    deleted = reading_service.delete_reading(reading.id)

    assert deleted is True
    assert reading_service.get_reading(reading.id) is None


def test_service_list_sensor_history_with_date_filters(
    reading_service: ReadingService, temp_sensor: ReadingModel
) -> None:
    reading_service.record("TEMP-01", 10.0, "C")
    reading_service.record("TEMP-01", 12.5, "C")
    reading_service.record("TEMP-01", 15.0, "C")

    now = datetime.now(timezone.utc)
    past = now - timedelta(days=1)

    history = reading_service.get_history("TEMP-01", from_date=past)
    assert len(history) == 3

    history = reading_service.get_history(
        "TEMP-01", to_date=now + timedelta(days=1)
    )
    assert len(history) == 3

    history = reading_service.get_history(
        "TEMP-01",
        from_date=now - timedelta(hours=1),
        to_date=now + timedelta(hours=1),
    )
    assert len(history) >= 1


def test_service_update_nonexistent_reading(reading_service: ReadingService) -> None:
    result = reading_service.update_reading(999, value=22.0, unit=None)
    assert result is None


def test_service_update_reading_no_changes(
    reading_service: ReadingService, temp_sensor: ReadingModel
) -> None:
    reading = reading_service.record("TEMP-01", 20.0, "C")
    updated = reading_service.update_reading(reading.id, value=None, unit=None)

    assert updated is not None
    assert updated.value == 20.0
    assert updated.unit == "C"


def test_service_delete_nonexistent_reading(reading_service: ReadingService) -> None:
    result = reading_service.delete_reading(999)
    assert result is False


def test_reading_model_repr() -> None:
    reading = ReadingModel(
        id=1,
        sensor_id="TEMP-01",
        value=25.5,
        unit="C",
        created_at=datetime.now(timezone.utc),
    )

    repr_str = repr(reading)
    assert "Reading(id=1" in repr_str
    assert "sensor='TEMP-01'" in repr_str
    assert "val=25.5C" in repr_str