from datetime import datetime

import pytest
from src.sensor_reading import SensorReading


# US-3
def test_creacion_lectura_valida() -> None:
    now = datetime.now()
    #Valores de temp y hum fijos pero serian variables
    reading = SensorReading(
        device_id="BODEGA-1", 
        temperatura=25.0, 
        humedad=50.0, 
        timestamp=now
    ) 
    assert reading.device_id == "BODEGA-1"
    assert reading.temperatura == 25.0
    assert reading.humedad == 50.0

@pytest.mark.parametrize("temperatura, humedad", [
    (25.0, 50.0),
    (0.0, 100.0),
    (100.0, 0.0)
])
def test_limites_validos(temperatura, humedad) -> None:
    reading = SensorReading(
        device_id="BODEGA-1", 
        temperatura=temperatura, 
        humedad=humedad, 
        timestamp=datetime.now()
    )
    if temperatura < -10.0 or temperatura > 100.0 or humedad < 0.0 or humedad > 100.0:
        with pytest.raises(ValueError, match="fuera de rango físico"):
            SensorReading(
                device_id="BODEGA-1",
                temperatura=temperatura,
                humedad=humedad,
                timestamp=datetime.now()
            )
    else:
        assert reading.temperatura == temperatura
        assert reading.humedad == humedad