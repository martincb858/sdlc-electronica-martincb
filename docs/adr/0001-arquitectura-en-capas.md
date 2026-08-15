# ADR 0001: Arquitectura en capas para SensorHub

## Estado

Aceptado

## Contexto

SensorHub empezó como un único archivo con validaciones hardcodeadas (`if/elif`
por unidad, umbrales fijos en el service) y lógica de negocio mezclada con el
código de FastAPI. Esto generaba dos problemas concretos:

1. **Portabilidad de infraestructura**: el proyecto necesita correr con
   SQLite en desarrollo local y PostgreSQL en producción (Docker Compose y
   Render), y potencialmente agregar más sensores y unidades de medida sin
   reescribir las validaciones existentes cada vez.
2. **Testeabilidad**: las reglas de negocio (validación física de lecturas,
   compatibilidad unidad-tipo de sensor, umbrales operacionales) necesitan
   probarse sin levantar un servidor HTTP ni depender de una base de datos
   real en cada corrida de CI.

Necesitábamos una estructura donde cambiar la base de datos, o agregar un
tipo de sensor nuevo, no obligara a tocar código ya probado y en producción.

## Decisión

Organizar el código en 4 capas, cada una dependiendo solo de la
inmediatamente inferior:

```
Presentación (app/routers/)     -> HTTP: status codes, mapea excepciones a respuestas
Aplicación   (app/services/)    -> Orquesta reglas de negocio (ReadingService, SensorService)
Dominio      (app/domain/)      -> Python puro, sin FastAPI ni SQLAlchemy (validators.py, sensor_types.py)
Infraestructura (app/repositories/, app/db.py) -> Unico lugar que conoce SQL/SQLAlchemy
```

Dos decisiones de diseño dentro de esta arquitectura:

- **Validación como Strategy + Registry (OCP)**: en vez de `if/elif` por
  unidad o tipo de sensor, cada unidad/tipo tiene su propia clase
  (`CelsiusPhysicsValidator`, `SensorTypeSpec`, etc.) registrada en un
  `ValidatorRegistry` / `SensorTypeRegistry`. Agregar una unidad nueva
  (ej. presión) es registrar una estrategia, no modificar código existente.
- **`DATABASE_URL` como único punto de cambio de infraestructura**:
  `db.py` lee la URL del entorno con normalización
  (`postgres://` → `postgresql+psycopg://`), por lo que SQLite local y
  PostgreSQL en producción usan exactamente el mismo código de la app.

## Consecuencias

+ Los tests de servicio (`ReadingService`, `SensorService`) corren contra
  SQLite en memoria sin necesitar Postgres ni Docker levantado — toda la
  suite de CI corre en menos de 2 segundos.
+ Pasar de SQLite a PostgreSQL en producción no tocó una sola línea de
  `services/`, `routers/` ni `domain/`: solo cambió la variable de entorno
  `DATABASE_URL` (verificado en el deploy de Docker Compose y Render).
+ Agregar una unidad o tipo de sensor nuevo es registrar una estrategia,
  no editar un `if/elif` existente — se verificó explícitamente con un
  test que registra una unidad `HPA` en tiempo de ejecución sin tocar
  `validators.py`.
+ Los validadores de dominio (`app/domain/`) no importan FastAPI ni
  SQLAlchemy, así que se pueden probar con `pytest` puro, sin fixtures de
  base de datos.
- **DIP aplicado de forma informal, no reforzada por tipos**: los
  services reciben clases concretas de repositorio
  (`SqlAlchemyReadingRepository`) como parámetro con default, no una
  interfaz (`Protocol`/ABC). Funciona porque nunca necesitamos otra
  implementación de repositorio, pero `mypy` no impediría pasar un objeto
  incompatible, y si en algún momento necesitamos un repositorio in-memory
  puro para tests unitarios más rápidos, habría que introducir el
  `Protocol` recién en ese momento.
- Los services retornan directamente `ReadingModel`/`SensorModel` (entidades
  de SQLAlchemy) en vez de DTOs propios de la capa de aplicación. FastAPI lo
  serializa correctamente vía `response_model` en el límite HTTP, pero el
  *type hint* interno filtra un detalle de la capa de infraestructura hacia
  la capa de aplicación.
- Más archivos y ceremonia para cambios pequeños: agregar un campo simple a
  `Sensor` toca modelo, repositorio, service, schema, router y tests en al
  menos 5 archivos distintos, en vez de uno solo.