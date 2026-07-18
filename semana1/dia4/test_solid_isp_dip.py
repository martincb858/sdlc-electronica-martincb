import pytest
from solid_isp_dip import (
    SimpleThermometer_M,
    SimpleThermometer_B,
    AdvancedSmartSensor_B,
    Readable,
    Calibratable,   
    DataProcessor_M,
    DataProcessor_B,
    InMemoryRepository,
    SensorReading,
)


# =====================================================================
# TESTS ISP
# =====================================================================

def test_ISP_M() -> None: 
    """Test de la versión mala: Demuestra cómo una interfaz gorda
    causa que los clientes del código sufran excepciones inesperadas.
    """
    sensor_basico = SimpleThermometer_M(sensor_id="TEMP-01")
    
    # El método read funciona
    assert sensor_basico.read().value == 25.0
    
    # Pero si el sistema intenta calibrarlo (porque la interfaz dice que se puede), ¡explota!
    with pytest.raises(NotImplementedError) as exc_info:
        sensor_basico.calibrate()
    
    assert "Este sensor básico no se puede calibrar" in str(exc_info.value)


def test_ISP_B() -> None:
    """Test de la versión buena: Demuestra que al segregar interfaces,
    cada objeto tiene estrictamente los métodos que puede cumplir.
    """
    sensor_basico = SimpleThermometer_B(sensor_id="TEMP-01")
    sensor_avanzado = AdvancedSmartSensor_B(sensor_id="SMART-01")

    # 1. Podemos validar sus capacidades de forma segura con isinstance()
    assert isinstance(sensor_basico, Readable) is True
    assert isinstance(sensor_basico, Calibratable) is False  

    assert isinstance(sensor_avanzado, Calibratable) is True

    # 2. Intentar llamar a un método que no le corresponde a un sensor básico
    # lanza un AttributeError estándar de Python, lo cual es correcto porque el método NO existe,
    # en lugar de engañar al sistema con un NotImplementedError de un método vacío.
    with pytest.raises(AttributeError):
        sensor_basico.calibrate()


def test_DIP_M(capsys: pytest.CaptureFixture) -> None:
    """Test de la versión mala: Como DataProcessor_M crea la base de datos
    por dentro, no podemos evitar que ejecute el código de producción.
    """
    processor = DataProcessor_M()
    reading = SensorReading(sensor_id="TEMP-01", value=25.555)
    
    processor.process_and_save(reading)
    
    # Para saber si funcionó, tenemos que atrapar prints o hacer mocks complejos,
    # porque no tenemos acceso a la base de datos interna.
    captured = capsys.readouterr()
    assert "Guardando en PostgreSQL" in captured.out


def test_DIP_B() -> None:
    """Test de la versión buena: Gracias a DIP y la inyección de dependencias,
    podemos probar la lógica usando un repositorio en memoria súper rápido.
    """
    # 1. Instanciamos nuestra base de datos simulada (sin librerías externas)
    test_repo = InMemoryRepository()
    
    # 2. Inyectamos la dependencia al procesador
    processor = DataProcessor_B(repository=test_repo)
    
    # 3. Ejecutamos la acción
    reading = SensorReading(sensor_id="TEMP-01", value=25.55)
    processor.process_and_save(reading)
    
    # 4. Verificación directa y segura: Leemos la RAM simulada
    saved_reading = test_repo.get_latest("TEMP-01")
    
    assert saved_reading is not None
    assert saved_reading.sensor_id == "TEMP-01"
    assert saved_reading.value == 25.55  # Verificamos que sí pasó por el round()