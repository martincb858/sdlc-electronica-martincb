import pytest

from app.domain.sensor_types import (
    SensorTypeRegistry,
    SensorTypeSpec,
    sensor_type_registry,
)
from app.domain.validators import (
    CelsiusOperationalValidator,
    CelsiusPhysicsValidator,
    FahrenheitPhysicsValidator,
    RelativeHumidityValidator,
    SensorValueValidator,
    ValidatorRegistry,
    physics_registry,
)


def test_celsius_physics_validator_accepts_valid_value() -> None:
    CelsiusPhysicsValidator().validate(20.0)  # no debe lanzar


def test_celsius_physics_validator_rejects_below_absolute_zero() -> None:
    with pytest.raises(ValueError, match="cero absoluto"):
        CelsiusPhysicsValidator().validate(-300.0)


def test_fahrenheit_physics_validator_accepts_valid_value() -> None:
    FahrenheitPhysicsValidator().validate(70.0)


def test_fahrenheit_physics_validator_rejects_below_absolute_zero() -> None:
    with pytest.raises(ValueError, match="cero absoluto"):
        FahrenheitPhysicsValidator().validate(-500.0)


@pytest.mark.parametrize("value", [0.0, 50.0, 100.0])
def test_humidity_validator_accepts_in_range_values(value: float) -> None:
    RelativeHumidityValidator().validate(value)


@pytest.mark.parametrize("value", [-1.0, 101.0])
def test_humidity_validator_rejects_out_of_range_values(value: float) -> None:
    with pytest.raises(ValueError, match="humedad relativa"):
        RelativeHumidityValidator().validate(value)


def test_operational_validator_uses_custom_threshold() -> None:
    validator = CelsiusOperationalValidator(min_value=0.0)
    with pytest.raises(ValueError, match="Temperatura invalida"):
        validator.validate(-5.0)
    validator.validate(10.0)  # no debe lanzar


def test_registry_get_raises_for_unknown_unit() -> None:
    registry = ValidatorRegistry()
    registry.register("C", CelsiusPhysicsValidator())
    with pytest.raises(ValueError, match="Unidad no soportada"):
        registry.get("XYZ")


def test_registry_get_optional_returns_none_for_unknown_unit() -> None:
    registry = ValidatorRegistry()
    assert registry.get_optional("C") is None


def test_registry_can_register_new_unit_without_modifying_existing_code() -> None:
    class PressureValidator(SensorValueValidator):
        def validate(self, value: float) -> None:
            if value < 0:
                raise ValueError("La presion no puede ser negativa.")

    registry = ValidatorRegistry()
    registry.register("HPA", PressureValidator())

    assert "HPA" in registry.supported_units()
    with pytest.raises(ValueError, match="presion"):
        registry.get("HPA").validate(-1.0)


def test_default_physics_registry_has_expected_units() -> None:
    assert physics_registry.supported_units() == ["%", "C", "F", "RH"]


def test_default_sensor_type_registry_has_expected_types() -> None:
    assert sensor_type_registry.supported_types() == ["HUMIDITY", "TEMPERATURE"]


def test_sensor_type_registry_get_raises_for_unknown_type() -> None:
    with pytest.raises(ValueError, match="Tipo de sensor no soportado"):
        sensor_type_registry.get("PRESSURE")


def test_sensor_type_registry_get_optional_returns_none_for_unknown_type() -> None:
    assert sensor_type_registry.get_optional("PRESSURE") is None


def test_sensor_type_registry_can_register_new_type() -> None:
    registry = SensorTypeRegistry()
    registry.register(SensorTypeSpec("PRESSURE", frozenset({"HPA"})))
    spec = registry.get("pressure")
    assert spec.code == "PRESSURE"
    assert "HPA" in spec.accepted_units


def test_temperature_type_accepts_only_c_and_f() -> None:
    spec = sensor_type_registry.get("TEMPERATURE")
    assert spec.accepted_units == frozenset({"C", "F"})


def test_humidity_type_accepts_only_rh_and_percent() -> None:
    spec = sensor_type_registry.get("HUMIDITY")
    assert spec.accepted_units == frozenset({"RH", "%"})
