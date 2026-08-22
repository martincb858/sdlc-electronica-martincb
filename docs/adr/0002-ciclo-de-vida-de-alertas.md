# ADR 0002: Umbral de anomalías por sensor y ciclo de vida de alertas

## Estado

Aceptado

## Contexto

El diseño original de `AnomalyDetectorService` tomaba un diccionario
`thresholds: dict[str, float]` en el constructor, construido una única vez.
Al conectarlo a `dependencies.py`, ese diccionario nunca se llenaba
(`AnomalyDetectorService(alert_strategy=db_strategy)` sin `thresholds`), así
que `process_reading` siempre encontraba `threshold is None` y ninguna
lectura disparaba una alerta jamás. El bug pasó desapercibido porque los
tests unitarios de `AnomalyDetectorService` instanciaban el diccionario a
mano y nunca ejercitaban el camino de inyección de dependencias real.

Al mismo tiempo, `AlertModel` no tenía columna de estado: cualquier alerta
creada quedaba en un estado implícito único, sin forma de distinguir una
alerta que ya fue revisada de una que sigue activa. La tabla `alerts`
tampoco tenía migración de Alembic — existía en `db.py` pero nunca se había
generado el `alembic revision --autogenerate` correspondiente, por lo que en
Postgres de producción la tabla no existía.

Necesitábamos: (1) que el umbral de alerta sea una propiedad real del
sensor, configurable por el usuario vía la API, y (2) que una alerta tenga
un ciclo de vida explícito y validado (`open -> acknowledged -> resolved`),
en línea con RF-1, RF-4 y RF-5.

## Decisión

- **El umbral vive en `SensorModel.alert_threshold`** (nullable), no en un
  diccionario en memoria. `SensorCreate`/`SensorUpdate` lo exponen como
  campo opcional del CRUD de sensores.
- **`AnomalyDetectorService.process_reading` recibe el umbral como
  parámetro explícito** (`process_reading(sensor_id, value, threshold)`) en
  vez de resolverlo internamente. Sigue siendo Python puro, sin conocer
  `SensorModel` ni SQLAlchemy — `ReadingService.record()` es quien lee
  `sensor.alert_threshold` (ya cargado al validar la lectura) y se lo pasa.
  Esto mantiene el detector testeable sin DB y elimina el estado mutable
  que causó el bug original.
- **Máquina de estados de alertas en `app/domain/alert_states.py`**: una
  función pura `validate_transition(current, new)` con las transiciones
  permitidas (`open -> acknowledged`, `open -> resolved`,
  `acknowledged -> resolved`) como único punto de verdad. `AlertService`
  la usa antes de persistir un cambio de estado; el router nunca decide
  transiciones, solo mapea `InvalidAlertTransitionError` a 400.
- **Sensor inactivo rechaza lecturas nuevas**: `ReadingService._validate_reading`
  levanta `SensorInactiveError` (409) cuando `sensor.active` es `False` y se
  intenta crear una lectura, pero no al consultar histórico ni al actualizar
  una lectura ya existente — el sensor desactivado sigue siendo consultable.

## Consecuencias

+ El bug de detección de anomalías (nunca se disparaba una alerta) quedó
  corregido y cubierto por un test de integración
  (`test_record_triggers_anomaly_detector_with_sensor_threshold`) que
  ejercita el camino real de DI, no solo el servicio en aislamiento.
+ Cambiar el umbral de un sensor es un PATCH sobre `/sensors/{code}`, sin
  reiniciar el proceso ni tocar código — antes hubiera requerido redeploy
  para cambiar un diccionario hardcodeado.
+ La máquina de estados es un módulo de ~25 líneas sin dependencias,
  probado con TDD antes de existir el `AlertService` que la usa.
+ Se generó la migración de Alembic faltante para `alerts` (más
  `alert_threshold` y `active` en `sensors`), con `server_default` en la
  columna `active` para no romper filas ya existentes en Postgres.
- El estado de la alerta se persiste en la misma tabla `alerts` en vez de
  un historial de transiciones separado: no queda auditoría de *cuándo* ni
  *quién* movió una alerta de `open` a `acknowledged`. Aceptable para el
  alcance actual; si se necesita auditoría, es un modelo `AlertStatusLog`
  nuevo sin tocar el resto del diseño.
