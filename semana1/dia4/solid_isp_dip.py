from typing import Protocol
from dia3.solid_srp_ocp_lsp import SensorReading

class DataRepository(Protocol):
    def save(self, reading: SensorReading) -> None: ...
    def get_latest(self, sensor_id: str) -> SensorReading | None: ...
 
class DataProcessor:
    """Depende de la abstraccion, no de una implementacion concreta."""
    def __init__(self, repository: DataRepository) -> None:
        self._repo = repository  # inyeccion de dependencias
    def process_and_save(self, reading: SensorReading) -> None:
        # Lógica de procesamiento...
        self._repo.save(reading)
# En produccion: DataProcessor(PostgreSQLRepository())
# En tests:      DataProcessor(InMemoryRepository())  <- sin base de datos


class SensorReading:
    def __init__(self, sensor_id: str, value: float):
        self.sensor_id = sensor_id
        self.value = value

# =======================================================
# 1. ISP: Interface Segregation Principle
# =======================================================
# Dividimos la "interfaz gorda" en interfaces específicas.

class Readable(Protocol):
    def read(self) -> float: ...

class Writable(Protocol):
    def write(self, value: float) -> None: ...

class Calibratable(Protocol):
    def calibrate(self) -> None: ...


# =======================================================
# 2. DIP: Dependency Inversion Principle
# =======================================================

# --- Implementaciones Concretas de Bajo Nivel ---

class InMemoryRepository:
    """Implementación para Tests. Cumple con la firma de DataRepository."""
    def __init__(self) -> None:
        self._db: dict[str, SensorReading] = {}

    def save(self, reading: SensorReading) -> None:
        self._db[reading.sensor_id] = reading
        print(f"[TEST] Guardado en memoria: {reading.sensor_id} = {reading.value}")

    def get_latest(self, sensor_id: str) -> SensorReading | None:
        return self._db.get(sensor_id)

# Si tuvieras una base real, crearías:
# class PostgreSQLRepository:
#     def save(self, reading: SensorReading) -> None:
#         # Lógica SQL real aquí
#         pass


# =======================================================
# Ejemplo de uso (El "pago" del DIP)
# =======================================================
if __name__ == "__main__":
    # En entorno de pruebas (Testing):
    # Inyectamos la base de datos en memoria. DataProcessor no nota la diferencia.
    test_repo = InMemoryRepository()
    processor = DataProcessor(test_repo)
    
    new_reading = SensorReading("SENSOR_01", 45.2)
    processor.process_and_save(new_reading)