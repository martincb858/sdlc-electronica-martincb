from dataclasses import dataclass
import datetime

@dataclass
class SensorReading:
    device_id: str
    temperatura: float
    humedad: float
    timestamp: datetime
