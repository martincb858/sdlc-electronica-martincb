import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.logging_config import configure_logging
from app.routers import alert_router, health_router, reading_router, sensor_router

configure_logging()
logger = logging.getLogger("sensorhub")

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
app.include_router(alert_router.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):  # type: ignore[no-untyped-def]
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info(
        "request completed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        },
    )
    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.exception(
        "unhandled exception",
        extra={"method": request.method, "path": request.url.path},
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor."},
    )
