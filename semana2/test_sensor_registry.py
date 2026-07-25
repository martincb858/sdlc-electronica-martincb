from sensor_registry import SensorRegistry, SensorNotFoundError

# 1) RED - el test primero; pytest DEBE fallar (ImportError)
def test_get_unknown_sensor_raises():
    registry = SensorRegistry()
    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")