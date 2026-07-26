from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar


@dataclass(slots=True, frozen=True)
class SensorReading:

    MIN_TEMP: ClassVar[float] = -10.0
    MAX_TEMP: ClassVar[float] = 60.0
    MIN_HUMEDAD: ClassVar[float] = 0.0
    MAX_HUMEDAD: ClassVar[float] = 100.0

    device_id: str
    temperatura: float
    humedad: float
    timestamp: datetime
    def __post_init__(self) -> None:
        if not (self.MIN_TEMP <= self.temperatura <= self.MAX_TEMP):
            raise ValueError(
                f"Temperatura {self.temperatura} °C fuera de rango "
                f"[{self.MIN_TEMP}, {self.MAX_TEMP}]"
            )
        if not (self.MIN_HUMEDAD <= self.humedad <= self.MAX_HUMEDAD):
            raise ValueError(
                f"Humedad {self.humedad} % fuera de rango "
                f"[{self.MIN_HUMEDAD}, {self.MAX_HUMEDAD}]"
            )