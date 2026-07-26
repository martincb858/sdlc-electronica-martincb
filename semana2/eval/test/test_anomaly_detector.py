from datetime import datetime
from src.sensor_reading import SensorReading
from src.anomaly_detector import AnomalyDetector, TipoAnomalia
import pytest


@pytest.mark.parametrize("temperatura, humedad", [
    (36.8, 55.0),
    (37.0, 60.0)
])
def test_operacion(temperatura, humedad) -> None:
    detector = AnomalyDetector(temp_threshold=35.0, hum_threshold=80.0)
    reading = SensorReading("BODEGA-1", temperatura=temperatura, humedad=humedad, timestamp=datetime.now())
    
    if temperatura > detector.temp_threshold:
        assert detector.evaluate(reading) == "ANOMALIA_TEMPERATURA"
    else:
        assert detector.evaluate(reading) == "OPERACION_NORMAL"
