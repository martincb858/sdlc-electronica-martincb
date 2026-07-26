from src.sensor_reading import SensorReading
from enum import Enum

class AnomalyType(str, Enum):
    NORMAL = "OPERACION_NORMAL"
    TEMPERATURA = "ANOMALIA_TEMPERATURA"
    HUMEDAD = "ANOMALIA_HUMEDAD"
    TEMPERATURA_Y_HUMEDAD = "ANOMALIA_TEMPERATURA_Y_HUMEDAD"

class AnomalyDetector:
    def __init__(self, temp_threshold: float, hum_threshold: float):
        self.temp_threshold = temp_threshold
        self.hum_threshold = hum_threshold

    def evaluate(self, reading: SensorReading) -> str:
        temp_alta = reading.temperatura > self.temp_threshold
        hum_alta = reading.humedad > self.hum_threshold

        match (temp_alta, hum_alta):
            case (True, True):
                return AnomalyType.TEMPERATURA_Y_HUMEDAD
            case (True, False):
                return AnomalyType.TEMPERATURA
            case (False, True):
                return AnomalyType.HUMEDAD
            case (False, False):
                return AnomalyType.NORMAL