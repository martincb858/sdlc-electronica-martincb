# Plan de Ejecución — Sprint 1

## 1. Sprint Goal
> **"Establecer una arquitectura backend funcional y local que permita el registro y autenticación de los 10 nodos sensores, la recepción continua y validada de telemetría cada 30 segundos, y la detección y notificación automatizada de anomalías ambientales en tiempo real."**

---

## 2. Sprint Backlog — Selección y Justificación (26 Story Points)

Al trabajar como un único desarrollador, este bloque de 6 historias cubre el flujo de datos completo de extremo a extremo (desde la simulación del hardware hasta la alerta operativa):

* **US-01: Autenticación y registro del nodo sensor (3 SP | Must Have)**
  * *Justificación:* Es la puerta de entrada del sistema. Controlar el registro por dirección MAC evita que dispositivos no autorizados inyecten datos basura en la base de datos central.
* **US-02: Ingesta periódica de telemetría cada 30 segundos (5 SP | Must Have)**
  * *Justificación:* Representa el canal principal de comunicación. El endpoint debe soportar el tráfico concurrente de los 10 nodos sin fugas de memoria ni alta latencia.
* **US-03: Validación de integridad y rangos físicos de las mediciones (3 SP | Must Have)**
  * *Justificación:* Los sensores físicos sufren fallos eléctricos. Validar que la temperatura esté entre -10 °C y 60 °C, y la humedad entre 0% y 100%, es indispensable para no corromper el historial ni disparar falsas alarmas.
* **US-04: Detección en tiempo real de anomalías ambientales (5 SP | Must Have)**
  * *Justificación:* Es el core del negocio. El backend debe evaluar cada paquete recibido contra los umbrales críticos (T > 35 °C o H > 80%) de forma instantánea.
* **US-05: Notificación automática ante alertas de anomalía (5 SP | Must Have)**
  * *Justificación:* Detectar el error no sirve sin una acción correctiva. Se implementa el canal de alerta implementando un algoritmo de supresión (*throttling*) para evitar la fatiga de alertas.
* **US-07: Monitoreo de salud del nodo y detección de desconexiones / Heartbeat (5 SP | Should Have)**
  * *Justificación:* Se incorpora al Sprint 1 porque aprovecha el mismo pipeline de ingesta. Si un nodo pierde alimentación eléctrica y deja de transmitir por 90 segundos, es operacionalmente tan grave como una anomalía ambiental.

---

## 3. Desglose de Tareas Técnicas (≤ 4 horas por tarea)

### US-01: Autenticación y registro del nodo sensor
* **T1.1 (2 h):** Diseñar la tabla `dispositivos` (campos: `id`, `mac_address`, `estado`, `token_auth`, `ultima_conexion`).
* **T1.2 (3 h):** Implementar endpoint HTTP POST `/api/v1/devices/register` con validación de sintaxis MAC y generación de tokens de seguridad únicos.
* **T1.3 (2 h):** Manejar la excepción de duplicidad para devolver el código HTTP 409 (Conflict) y escribir las pruebas unitarias.

### US-02: Ingesta periódica de telemetría cada 30 segundos
* **T2.1 (2 h):** Diseñar la tabla de series temporales `telemetria` con índices optimizados por `device_id` y `timestamp`.
* **T2.2 (4 h):** Implementar endpoint POST `/api/v1/telemetry` que valide el token en el header HTTP y almacene el payload.
* **T2.3 (3 h):** Crear el script base en Python que emule peticiones HTTP concurrentes.

### US-03: Validación de integridad y rangos físicos
* **T3.1 (2 h):** Crear un middleware o función de validación física antes de la inserción a base de datos (-10 a 60 °C y 0 a 100% HR).
* **T3.2 (3 h):** Crear la tabla `system_logs` e implementar la lógica para descartar paquetes corruptos devolviendo HTTP 400 y registrando el evento `ERROR_LECTURA_HARDWARE`.
* **T3.3 (2 h):** Escribir pruebas unitarias inyectando strings, valores nulos y temperaturas extremas (ej. 150 °C).

### US-04: Detección en tiempo real de anomalías
* **T4.1 (3 h):** Construir un servicio evaluador de reglas que se ejecute en el pipeline inmediatamente después de validar la lectura física.
* **T4.2 (2 h):** Implementar la actualización de base de datos para cambiar el campo `estado` de la tabla `dispositivos` a `ALERTA_CRÍTICA` o `ACTIVO`.
* **T4.3 (2 h):** Escribir pruebas de integración verificando que una lectura de 36 °C o 81% HR active el cambio de estado.

### US-05: Notificación automática con Throttling
* **T5.1 (4 h):** Configurar el servicio de envío de alertas (ej. SMTP para correos o un log local de notificaciones para el MVP) usando variables de entorno (`.env`).
* **T5.2 (4 h):** Implementar el algoritmo de *Alert Throttling*: consultar la marca de tiempo de la última notificación enviada para ese nodo antes de disparar un nuevo mensaje (ventana de silencio de 5 minutos).
* **T5.3 (2 h):** Diseñar las plantillas en texto plano con los parámetros clave (ID de zona, valor registrado, marca de tiempo).

### US-07: Monitoreo de salud (Heartbeat)
* **T6.1 (3 h):** Configurar una tarea programada en segundo plano (*background task*) en el servidor que se ejecute en un bucle cada 30 segundos.
* **T6.2 (3 h):** Escribir una consulta SQL que identifique dispositivos con estado `ACTIVO` cuya `ultima_conexion` sea anterior al tiempo actual menos 90 segundos.
* **T6.3 (3 h):** Implementar la transición de esos nodos a estado `OFFLINE` generándose un registro de alerta técnica, y permitir que el endpoint de telemetría los regrese automáticamente a `ACTIVO` cuando vuelvan a transmitir.

---

## 4. Definition of Done (DoD)

Para marcar una historia como terminada, debe cumplir estrictamente con:
* **Código Limpio:** Control de versiones en Git, sin credenciales ni variables fijadas en el código (*hardcoding*), gestionando configuración vía archivos `.env`.
* **Pruebas Unitarias/Integración:** Todos los escenarios Gherkin del backlog están cubiertos por pruebas automatizadas (ej. con PyTest) y pasan al 100%.
* **Base de Datos:** Las migraciones o scripts de creación de tablas se ejecutan desde cero sin errores e incluyen restricciones y llaves foráneas correctas.
* **Semántica HTTP:** Endpoints devolviendo códigos de estado correctos (200, 201, 400, 401, 409, 500) y estructuras de error en JSON comprensibles.
* **Documentación:** Contratos de API documentados (OpenAPI / Swagger automático de FastAPI o colección exportada de Postman).
