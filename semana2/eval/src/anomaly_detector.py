from src.sensor_reading import SensorReading

class AnomalyDetector:
    def __init__(self, temp_threshold: float, hum_threshold: float):
        self.temp_threshold = temp_threshold
        self.hum_threshold = hum_threshold

    def evaluate(self, reading: SensorReading) -> str:
        if reading.temperatura > self.temp_threshold:
            return "ANOMALIA_TEMPERATURA"
        else:
            return "OPERACION_NORMAL"

