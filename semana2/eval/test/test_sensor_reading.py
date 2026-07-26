import pytest
from datetime import datetime
from src.sensor_reading import SensorReading


# US-3
def test_creacion_lectura_valida():
    now = datetime.now()
    #Valores de temp y hum fijos pero serian variables
    reading = SensorReading(device_id="BODEGA-1", temperatura=25.0, humedad=50.0, timestamp=now) 
    assert reading.device_id == "BODEGA-1"
    assert reading.temperatura == 25.0
    assert reading.humedad == 50.0

def test_rechazo_temperatura_alta():
    with pytest.raises(ValueError, match="fuera de rango físico"):
        SensorReading("BODEGA-1", temperatura=150.0, humedad=50.0, timestamp=datetime.now())

def test_rechazo_temperatura_baja():
    with pytest.raises(ValueError, match="fuera de rango físico"):
        SensorReading("BODEGA-1", temperatura=-15.0, humedad=50.0, timestamp=datetime.now())

def test_rechazo_humedad_negativa():
    with pytest.raises(ValueError, match="fuera de rango físico"):
        SensorReading("BODEGA-1", temperatura=20.0, humedad=-5.0, timestamp=datetime.now())

def test_rechazo_humedad_excesiva():
    with pytest.raises(ValueError, match="fuera de rango físico"):
        SensorReading("BODEGA-1", temperatura=20.0, humedad=105.0, timestamp=datetime.now())