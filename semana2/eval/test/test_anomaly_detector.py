from datetime import datetime
import pytest
from src.anomaly_detector import AnomalyDetector, AnomalyType
from src.sensor_reading import SensorReading


@pytest.fixture
def detector() -> AnomalyDetector:
    return AnomalyDetector(temp_threshold=35.0, hum_threshold=80.0)


@pytest.mark.parametrize("temperatura, humedad, esperado", [
    (25.0, 50.0, AnomalyType.NORMAL),
    (36.8, 55.0, AnomalyType.TEMPERATURA),
    (25.0, 85.0, AnomalyType.HUMEDAD),
    (37.0, 85.0, AnomalyType.TEMPERATURA_Y_HUMEDAD), 
])
def test_evaluate_detecta_anomalias_correctamente(
    detector: AnomalyDetector,
    temperatura: float,
    humedad: float,
    esperado: AnomalyType
) -> None:
    reading = SensorReading(
        device_id="BODEGA-1",
        temperatura=temperatura,
        humedad=humedad,
        timestamp=datetime(2026, 1, 1, 12, 0, 0)  # Timestamp fijo y determinístico
    )
    
    assert detector.evaluate(reading) == esperado