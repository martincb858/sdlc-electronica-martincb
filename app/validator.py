"""Estrategias de validación de lecturas de sensores.

Este módulo reemplaza las cadenas de `if/elif` hardcodeadas que existían
en el schema (validate_physics) y en el service (record). En su lugar,
cada unidad de medida tiene su propia estrategia de validación, y esas
estrategias se agrupan en un `ValidatorRegistry`.

Por qué esto respeta OCP (Open/Closed Principle):
- Para soportar una nueva unidad (ej. "hPa" para presión, "PPM" para CO2)
  solo hay que crear una nueva clase que implemente `SensorValueValidator`
  y registrarla. No es necesario tocar el schema, el service, ni ninguna
  de las validaciones existentes.
- El código que *usa* el registro (schema, service) nunca cambia cuando
  se agregan nuevas unidades: solo depende de la interfaz abstracta.

Se separan dos niveles de validación porque responden a preguntas
distintas:
- "Physics" (`physics_registry`): ¿el valor es físicamente posible?
  Se usa en el schema Pydantic, en el borde de la API.
- "Operational" (`operational_registry`): ¿el valor está dentro del
  rango operativo aceptado por el negocio para este despliegue?
  Se usa en el service, como regla de negocio independiente de la API.
"""

from abc import ABC, abstractmethod


class SensorValueValidator(ABC):
    """Contrato para validar el valor de una lectura de una unidad dada."""

    @abstractmethod
    def validate(self, value: float) -> None:
        """Lanza ValueError si `value` es inválido. No retorna nada si es válido."""
        raise NotImplementedError


class CelsiusPhysicsValidator(SensorValueValidator):
    """El cero absoluto en Celsius es -273.15."""

    def validate(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("Temperatura en Celsius por debajo del cero absoluto.")


class FahrenheitPhysicsValidator(SensorValueValidator):
    """El cero absoluto en Fahrenheit es -459.67."""

    def validate(self, value: float) -> None:
        if value < -459.67:
            raise ValueError("Temperatura en Fahrenheit por debajo del cero absoluto.")


class RelativeHumidityValidator(SensorValueValidator):
    """La humedad relativa solo tiene sentido entre 0% y 100%."""

    def validate(self, value: float) -> None:
        if value < 0 or value > 100:
            raise ValueError("La humedad relativa debe estar entre 0% y 100%.")


class CelsiusOperationalValidator(SensorValueValidator):
    """Regla de negocio: por debajo de este umbral se considera una lectura
    inválida para operación (no es una ley física, es una decisión del
    negocio, por eso vive separada de CelsiusPhysicsValidator).
    """

    def __init__(self, min_value: float = -25.0) -> None:
        self._min_value = min_value

    def validate(self, value: float) -> None:
        if value < self._min_value:
            raise ValueError("Temperatura invalida")


class ValidatorRegistry:
    """Registro de validadores por unidad, abierto a extensión.

    Uso:
        registry = ValidatorRegistry()
        registry.register("C", CelsiusPhysicsValidator())
        registry.get("C").validate(-300.0)  # -> ValueError
    """

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
        """Como `get`, pero retorna None si no hay validador registrado
        para esa unidad, en vez de lanzar. Útil para registros donde no
        todas las unidades tienen una regla (ej. operational_registry).
        """
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


# Instancias por defecto, listas para usar vía inyección de dependencias.
# Nada impide crear otra instancia con validadores distintos (ej. en tests
# o para un despliegue con otros umbrales) e inyectarla en su lugar.
physics_registry = build_default_physics_registry()
operational_registry = build_default_operational_registry()