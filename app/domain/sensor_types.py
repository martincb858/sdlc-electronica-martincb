from dataclasses import dataclass


@dataclass(frozen=True)
class SensorTypeSpec:
    code: str
    accepted_units: frozenset[str]


class SensorTypeRegistry:
    def __init__(self) -> None:
        self._types: dict[str, SensorTypeSpec] = {}

    def register(self, spec: SensorTypeSpec) -> None:
        self._types[spec.code.upper()] = spec

    def get(self, sensor_type: str) -> SensorTypeSpec:
        try:
            return self._types[sensor_type.upper()]
        except KeyError as exc:
            supported = ", ".join(sorted(self._types))
            raise ValueError(
                f"Tipo de sensor no soportado: {sensor_type.upper()}. Use {supported}."
            ) from exc

    def get_optional(self, sensor_type: str) -> SensorTypeSpec | None:
        return self._types.get(sensor_type.upper())

    def supported_types(self) -> list[str]:
        return sorted(self._types)


def build_default_sensor_type_registry() -> SensorTypeRegistry:
    registry = SensorTypeRegistry()
    registry.register(SensorTypeSpec("TEMPERATURE", frozenset({"C", "F"})))
    registry.register(SensorTypeSpec("HUMIDITY", frozenset({"RH", "%"})))
    return registry


sensor_type_registry = build_default_sensor_type_registry()