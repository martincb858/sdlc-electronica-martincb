# Prompting Efectivo - SensorHub API

---

## Tarea 1: Conversión de unidades de temperatura

### Prompt Pobre

> haz una funcion para pasar celsius a fahrenheit

### Prompt Efectivo

> **CONTEXTO:** API FastAPI (Python 3.12) para gestion de sensores. SQLAlchemy 2.x tipado, arquitectura en capas.
> **TAREA:** escribe una funcion pura `celsius_to_fahrenheit(c: float) -> float` en `semana5/conversions.py`.
> **RESTRICCIONES:** type hints completos, docstring, sin dependencias externas, redondeo a 2 decimales.
> **ENTREGA:** solo la funcion, sin explicacion.

---

## Tarea 2: Cálculo de promedios para reportes de sensores

### Prompt Pobre

> haz una funcion que saque el promedio de las lecturas. si no hay lecturas devuelve 0.

### Prompt Efectivo

> **CONTEXTO:** API FastAPI (Python 3.12) para gestion de sensores. SQLAlchemy 2.x tipado, arquitectura en capas.
> **TAREA:** escribe una funcion pura `calculate_average_reading(readings: list[float]) -> float` en `app/services/analytics.py`.
> **RESTRICCIONES:** type hints completos, docstring, sin dependencias externas. Si la lista esta vacia, debe devolver 0.0. Redondear el resultado a 2 decimales.
> **ENTREGA:** solo la funcion, sin explicacion.

---

## Tarea 3: Validación de datos de entrada con Pydantic

### Prompt Pobre

> en pydantic valida que la lectura no sea menor a 0 si es un sensor de luz

### Prompt Efectivo

> **CONTEXTO:** API FastAPI (Python 3.12) para gestion de sensores. SQLAlchemy 2.x tipado, arquitectura en capas, Pydantic v2.
> **TAREA:** Escribe un `model_validator` (modo after) para el esquema `ReadingCreate` en `app/schemas/reading_schema.py`.
> **RESTRICCIONES:** Validar que si `unit` es "lux" (sensor de luz), el `value` no sea negativo. Si es negativo, levantar `ValueError`. Type hints completos.
> **ENTREGA:** Solo el metodo del validador y sus imports necesarios, sin la clase completa ni explicacion.