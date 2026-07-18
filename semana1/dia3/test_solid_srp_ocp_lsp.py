import os
import json
import pytest    
from solid_srp_ocp_lsp import (
    SensorReader_M, 
    DataLogger, 
    SensorReading, 
    SensorReader_B, 
    AnomalyDetector_M, 
    AlertStrategy, 
    ConsoleAlert, 
    FileAlert, 
    AnomalyDetector_B,
    TemperatureSensor_M,
    HumiditySensor_M,
    process_sensor_M,
    TemperatureSensor,
    HumiditySensor,
    process_sensor_B,
    BaseSensor,

)

# =====================================================================
# EJEMPLOS SRP
# =====================================================================

def test_SRP_M() -> None:
    """Test de SensorReader_M: Verifica que la funcion que rompe la SRP funciona correctamente."""

    filename = "test_sensor_log.json"
    reader = SensorReader_M(sensor_id="TEMP-01", target_dir=".")

    #Probar lectura
    reading = reader.read()
    assert isinstance(reading, SensorReading)
    assert reading.sensor_id == "TEMP-01"
    assert reading.value == 75.0

    #Probar log
    reader.log(reading, "test_sensor_log.json")
    assert os.path.exists(filename)

    with open(filename, "r") as f:
        saved_data = json.load(f)
        
    assert saved_data["sensor_id"] == "TEMP-01"
    assert saved_data["value"] == 75.0

    #Borrar archivo de prueba
    if os.path.exists(filename):
        os.remove(filename)


def test_SRP_B() -> None:
    """Test de SensorReader_B y DataLogger: Verifica que las funciones que cumplen la SRP funcionan correctamente."""

    filename = "test_sensor_log.json"
    reader = SensorReader_B(sensor_id="TEMP-01")
    logger = DataLogger(target_dir=".")

    #Probar lectura
    reading = reader.read()
    assert isinstance(reading, SensorReading)
    assert reading.sensor_id == "TEMP-01"
    assert reading.value == 75.0

    #Probar log
    logger.log(reading, "test_sensor_log.json")
    assert os.path.exists(filename)

    with open(filename, "r") as f:
        saved_data = json.load(f)
        
    assert saved_data["sensor_id"] == "TEMP-01"
    assert saved_data["value"] == 75.0

    #Borrar archivo de prueba
    if os.path.exists(filename):
        os.remove(filename)


# =====================================================================
# TEST OCP OCP
# =====================================================================

@pytest.mark.parametrize("value", [75.0, 65.0])  # Casos: por encima y por debajo del umbral
@pytest.mark.parametrize("alert_type", ["console", "file", "email"])  # Todos los tipos de alerta
def test_OCP_M(value: float, alert_type: str) -> None:
    """Test de AnomalyDetector_M: Verifica de forma compacta y segura que

    todas las alertas (soportadas o no) manejan correctamente el flujo.
    """
    detector = AnomalyDetector_M(threshold=70.0)
    reading = SensorReading(sensor_id="TEMP-01", value=value)

    # 1. Si el tipo de alerta es 'email', sabemos que va a fallar porque NO está implementado en la versión _M
    if alert_type == "email" and value > 70.0:
        with pytest.raises(ValueError) as exc_info:
            detector.check(reading, alert_type=alert_type)
        assert str(exc_info.value) == "Tipo de alerta no soportado"
        
    # 2. Si es 'console' o 'file', el código debería ejecutar su lógica sin lanzar excepciones
    else:
        detector.check(reading, alert_type=alert_type)


@pytest.mark.parametrize("value", [75.0, 65.0])  # Casos: por encima y por debajo del umbral
@pytest.mark.parametrize("strategy", [
    ConsoleAlert(), 
    FileAlert(filepath="test_alerts.log")
])
def test_OCP_B(strategy: AlertStrategy, value: float, capsys: pytest.CaptureFixture) -> None:
    """Test de AnomalyDetector_B: Verifica que las alertas se envían correctamente."""
    
    # 1. Configuración inicial
    detector = AnomalyDetector_B(alert=strategy, threshold=70.0)
    reading = SensorReading(sensor_id="TEMP-01", value=value)
    expected_message = "Anomalia en TEMP-01"

    # Limpieza preventiva: si quedó un archivo de una prueba anterior, lo borramos
    if isinstance(strategy, FileAlert) and os.path.exists(strategy.filepath):
        os.remove(strategy.filepath)

    # 2. Ejecución
    detector.check(reading)

    # 3. Verificaciones
    if value > 70.0:
        # === CASO A: Supera el umbral (SÍ debe haber alerta) ===
        if isinstance(strategy, ConsoleAlert):
            captured = capsys.readouterr()  # Leemos la consola
            assert expected_message in captured.out
            
        elif isinstance(strategy, FileAlert):
            assert os.path.exists(strategy.filepath) # El archivo debe existir
            with open(strategy.filepath, "r") as f:
                assert expected_message in f.read()  # El archivo debe tener el texto
            
            os.remove(strategy.filepath) # Limpiamos al terminar

    else:
        # === CASO B: No supera el umbral (NO debe haber alerta) ===
        if isinstance(strategy, ConsoleAlert):
            captured = capsys.readouterr()
            assert expected_message not in captured.out # La consola debe estar limpia
            
        elif isinstance(strategy, FileAlert):
            # El archivo no debería haberse creado
            assert not os.path.exists(strategy.filepath)



# =====================================================================
# TEST OCP LSP
# =====================================================================

def test_LSP_M() -> None:
    """Demuestra cómo HumiditySensor_M rompe la sustitución de Liskov."""
    
    sensor_temp = TemperatureSensor_M(sensor_id="TEMP-01")
    sensor_hum = HumiditySensor_M(sensor_id="HUM-01")

    # 1. El sensor de temperatura funciona bien (devuelve un objeto SensorReading)
    # Si ejecutamos esto, el código no lanza ningún error.
    process_sensor_M(sensor_temp) 

    # 2. El sensor de humedad ROMPE la función (devuelve un dict)
    # process_sensor_M intenta hacer reading.value, pero los diccionarios no tienen .value
    with pytest.raises(AttributeError) as exc_info:
        process_sensor_M(sensor_hum)
        
    # Verificamos que el error exacto sea porque intentó leer '.value' de un diccionario
    assert "'dict' object has no attribute 'value'" in str(exc_info.value)


@pytest.mark.parametrize("sensor_instance, expected_value", [
    (TemperatureSensor(sensor_id="TEMP-01"), 22.5),
    (HumiditySensor(sensor_id="HUM-01"), 55.0)
])
def test_LSP_B(sensor_instance: BaseSensor, expected_value: float, capsys: pytest.CaptureFixture) -> None:
    """Demuestra que process_sensor_B funciona de forma idéntica e
    intercambiable con cualquier subclase de BaseSensor.
    """
    
    # 1. Ejecutamos la función.
    process_sensor_B(sensor_instance)
    
    # 2. Capturamos la consola para verificar que se procesó correctamente
    captured = capsys.readouterr()
    expected_message = f"Procesando lectura: {expected_value} del sensor {sensor_instance.sensor_id}"
    
    # 3. Afirmamos que el mensaje salió bien, sin importar de qué clase venía
    assert expected_message in captured.out

