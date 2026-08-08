from fastapi import FastAPI

from app.routers import health_router, reading_router, sensor_router


app = FastAPI(
    title="SensorHub API",
    version="0.3.0",
    description=(
        "API para gestionar sensores IoT y sus lecturas, con validacion "
        "fisica real por tipo de sensor."
    ),
)

app.include_router(health_router.router)
app.include_router(sensor_router.router)
app.include_router(reading_router.router)