from fastapi import FastAPI

from app.db import Base, engine
from app.routers import reading_router, sensor_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SensorHub API",
    version="0.3.0",
    description=(
        "API para gestionar sensores IoT y sus lecturas, con validacion "
        "fisica real por tipo de sensor."
    ),
)

app.include_router(sensor_router.router)
app.include_router(reading_router.router)
