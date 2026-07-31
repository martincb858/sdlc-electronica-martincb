from app.repositories.reading import SqlAlchemyReadingRepository

from app.db import Base, SessionLocal, engine
from app.services.reading_service import ReadingService

# Esto crea el archivo sensorhub.db y las tablas si no existen
Base.metadata.create_all(bind=engine)


def run_local_test():

    db_session = SessionLocal()

    try:
        repo = SqlAlchemyReadingRepository(db_session)
        service = ReadingService(repo)

        print("PRUEBA INICIADA")

        print("\n1. Registrando datos de temperatura normales...")
        r1 = service.record("TEMP-01", 24.5, "C")
        print(f"Guardado con ID de Base de Datos: {r1.id}")

        r2 = service.record("TEMP-01", 25.1, "C")
        print(f"Guardado con ID de Base de Datos: {r2.id}")

        print("\n2. Recuperando el historial del sensor TEMP-01...")
        history = service.get_history(
            "TEMP-01", limit=10, offset=0, from_date=None, to_date=None
        )

        for reading in history:
            print(
                f"ID={reading.id}: {reading.value} °{reading.unit}"
                f" (Fecha: {reading.created_at})"
            )

        print("\n3. Intentando registrar una temperatura imposible (-300 °C)...")
        try:
            service.record("TEMP-01", -300.0, "C")
        except ValueError as error_msg:
            print(f"Bloqueo: '{error_msg}'")

    finally:
        db_session.close()
        print("\nFIN DE PRUEBA")


if __name__ == "__main__":
    run_local_test()
