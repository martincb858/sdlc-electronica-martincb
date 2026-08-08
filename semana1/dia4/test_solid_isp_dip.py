import pytest
from solid_isp_dip import (
    AdvancedSmartSensor_B,
    Calibratable,
    DataProcessor_B,
    DataProcessor_M,
    InMemoryRepository,
    Readable,
    SensorReading,
    SimpleThermometer_B,
    SimpleThermometer_M,
)

# =====================================================================
# TESTS ISP
# =====================================================================

def test_ISP_M() -> None: 

    sensor_basico = SimpleThermometer_M(sensor_id="TEMP-01")
    

    assert sensor_basico.read().value == 25.0
    
    with pytest.raises(NotImplementedError) as exc_info:
        sensor_basico.calibrate()
    
    assert "Este sensor básico no se puede calibrar" in str(exc_info.value)


def test_ISP_B() -> None:

    sensor_basico = SimpleThermometer_B(sensor_id="TEMP-01")
    sensor_avanzado = AdvancedSmartSensor_B(sensor_id="SMART-01")


    assert isinstance(sensor_basico, Readable) is True
    assert isinstance(sensor_basico, Calibratable) is False  

    assert isinstance(sensor_avanzado, Calibratable) is True


    with pytest.raises(AttributeError):
        sensor_basico.calibrate()


def test_DIP_M(capsys: pytest.CaptureFixture) -> None:

    processor = DataProcessor_M()
    reading = SensorReading(sensor_id="TEMP-01", value=25.555)
    
    processor.process_and_save(reading)
    

    captured = capsys.readouterr()
    assert "Guardando en PostgreSQL" in captured.out


def test_DIP_B() -> None:

    test_repo = InMemoryRepository()
    

    processor = DataProcessor_B(repository=test_repo)
    

    reading = SensorReading(sensor_id="TEMP-01", value=25.55)
    processor.process_and_save(reading)
    

    saved_reading = test_repo.get_latest("TEMP-01")
    
    assert saved_reading is not None
    assert saved_reading.sensor_id == "TEMP-01"
    assert saved_reading.value == 25.55  