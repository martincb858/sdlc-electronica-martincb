from abc import ABC, abstractmethod


class SensorValueValidator(ABC):
    @abstractmethod
    def validate(self, value: float) -> None:
        raise NotImplementedError


class CelsiusPhysicsValidator(SensorValueValidator):
    def validate(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("Temperatura en Celsius por debajo del cero absoluto.")


class FahrenheitPhysicsValidator(SensorValueValidator):
    def validate(self, value: float) -> None:
        if value < -459.67:
            raise ValueError("Temperatura en Fahrenheit por debajo del cero absoluto.")


class RelativeHumidityValidator(SensorValueValidator):
    def validate(self, value: float) -> None:
        if value < 0 or value > 100:
            raise ValueError("La humedad relativa debe estar entre 0% y 100%.")


class CelsiusOperationalValidator(SensorValueValidator):
    def __init__(self, min_value: float = -25.0) -> None:
        self._min_value = min_value

    def validate(self, value: float) -> None:
        if value < self._min_value:
            raise ValueError("Temperatura invalida")


class ValidatorRegistry:
    def __init__(self) -> None:
        self._validators: dict[str, SensorValueValidator] = {}

    def register(self, unit: str, validator: SensorValueValidator) -> None:
        self._validators[unit.upper()] = validator

    def get(self, unit: str) -> SensorValueValidator:
        """Retorna el validador para `unit` o lanza ValueError si no existe."""
        try:
            return self._validators[unit.upper()]
        except KeyError as exc:
            supported = ", ".join(sorted(self._validators))
            raise ValueError(
                f"Unidad no soportada: {unit.upper()}. Use {supported}."
            ) from exc

    def get_optional(self, unit: str) -> SensorValueValidator | None:
        return self._validators.get(unit.upper())

    def supported_units(self) -> list[str]:
        return sorted(self._validators)


def build_default_physics_registry() -> ValidatorRegistry:
    registry = ValidatorRegistry()
    registry.register("C", CelsiusPhysicsValidator())
    registry.register("F", FahrenheitPhysicsValidator())
    registry.register("RH", RelativeHumidityValidator())
    registry.register("%", RelativeHumidityValidator())
    return registry


def build_default_operational_registry() -> ValidatorRegistry:
    registry = ValidatorRegistry()
    registry.register("C", CelsiusOperationalValidator(min_value=-25.0))
    return registry


physics_registry = build_default_physics_registry()
operational_registry = build_default_operational_registry()
