import pytest
from datetime import datetime, timezone
from app.db import ReadingModel
from app.services.reading import ReadingService

class FakeReadingRepository:
    def __init__(self):
        self._readings: list[ReadingModel] = []
        self._current_id = 1

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(
            id=self._current_id,
            sensor_id=sensor_id,
            value=value,
            unit=unit,
            created_at=datetime.now(timezone.utc)
        )
        self._readings.append(reading)
        self._current_id += 1
        return reading

    def list_for_sensor(self, sensor_id: str) -> list[ReadingModel]:
        return [r for r in self._readings if r.sensor_id == sensor_id]

def test_service_records_valid_reading() -> None:
    fake_repo = FakeReadingRepository()
    service = ReadingService(fake_repo)
    
    result = service.record("TEMP-01", 25.5, "C")
    
    assert result.sensor_id == "TEMP-01"
    assert result.value == 25.5
    assert len(fake_repo._readings) == 1

def test_service_raises_error_below_absolute_zero() -> None:
    """Prueba que la regla de negocio bloquea lecturas físicamente imposibles."""
    fake_repo = FakeReadingRepository()
    service = ReadingService(fake_repo)
    
    # Comprobamos que lanzar una excepción ValueError es el comportamiento esperado
    with pytest.raises(ValueError, match="Temperatura invalida"):
        service.record("TEMP-01", -300.0, "C")

def test_service_can_list_sensor_history() -> None:
    """Prueba que el historial de un sensor específico se filtra correctamente."""
    fake_repo = FakeReadingRepository()
    service = ReadingService(fake_repo)
    
    # Agregamos ruido (datos de otro sensor) y datos del sensor objetivo
    service.record("SENSOR-A", 10.0, "C")
    service.record("SENSOR-A", 12.5, "C")
    service.record("SENSOR-B", 99.0, "C")
    
    # Verificamos
    history = service.get_history("SENSOR-A")
    assert len(history) == 2
    assert history[0].value == 10.0
    assert history[1].value == 12.5