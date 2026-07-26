# Product Backlog — Sistema de Monitoreo IoT

**Contexto del Proyecto:**
Desarrollo de un sistema de monitoreo IoT para una bodega industrial operado por un único desarrollador. El ecosistema consta de 10 nodos sensores que transmiten datos de temperatura y humedad cada 30 segundos hacia un servidor central. El sistema incluye detección en tiempo real de anomalías (Temperatura > 35 °C o Humedad > 80%), alertas automatizadas, monitoreo de salud de los dispositivos y visualización continua.

---

## US-01: Autenticación y registro del nodo sensor
Como administrador del sistema de monitoreo,  
quiero dar de alta un nodo sensor asignándole una dirección MAC y credenciales de acceso,  
para garantizar que únicamente los dispositivos autorizados puedan transmitir mediciones a la base de datos central.

**Story Points:** 3  
**Prioridad (MoSCoW):** Must Have  

### Scenario: Registro exitoso de un nuevo nodo sensor
  Given una dirección MAC "00:1B:44:11:3A:B7" que no ha sido registrada previamente
  When envío la solicitud de alta utilizando la dirección MAC "00:1B:44:11:3A:B7"
  Then el sistema almacena el dispositivo con estado "ACTIVO"
  And devuelve un mensaje "El dispositivo se registró correctamente"

### Scenario: Rechazar el registro de una dirección MAC duplicada
  Given una dirección MAC "00:1B:44:11:3A:B7" que ya se encuentra en el sistema
  When envío una solicitud de alta utilizando la misma dirección MAC
  Then el sistema rechaza la operación con código HTTP 409
  And devuelve el mensaje "El dispositivo ya se encuentra registrado"

---

## US-02: Ingesta periódica de telemetría cada 30 segundos
Como nodo sensor desplegado en la bodega,  
quiero enviar mediciones de temperatura y humedad cada 30 segundos mediante un payload ligero,  
para registrar las condiciones ambientales en tiempo real sin saturar el ancho de banda ni el servidor central.

**Story Points:** 5  
**Prioridad (MoSCoW):** Must Have  

### Scenario: Recepción y almacenamiento de telemetría válida
  Given un nodo sensor con dirección MAC "00:1B:44:11:3A:B7" autenticado y en estado "ACTIVO"
  When el nodo envía el payload `{"temp": 24.5, "hum": 60.2, "timestamp": "2026-07-25T21:00:00Z"}`
  Then el sistema valida las credenciales y la estructura de datos
  And almacena la medición exitosamente en la base de datos de series temporales
  And responde al dispositivo con un código HTTP 201

### Scenario: Rechazo de telemetría proveniente de un nodo no autorizado
  Given un dispositivo con dirección MAC "FF:FF:FF:00:00:00" no registrado en el sistema
  When el dispositivo intenta transmitir una lectura de temperatura y humedad
  Then el sistema rechaza la conexión con código HTTP 401
  And descarta el payload sin escribir registros en la base de datos de telemetría

---

## US-03: Validación de integridad y rangos físicos de las mediciones
Como responsable de la calidad del dato,  
quiero que el servidor valide que las lecturas recibidas se encuentren dentro de rangos físicos posibles (temperatura entre -10 °C y 60 °C, humedad entre 0% y 100%),  
para evitar que fallas de hardware en los sensores corrompan el historial o generen falsas alarmas.

**Story Points:** 3  
**Prioridad (MoSCoW):** Must Have  

### Scenario: Procesamiento de una medición dentro del rango aceptable
  Given una lectura recibida desde el sensor "BODEGA-ZONA-4" con temperatura de 28.0 °C y humedad de 65.0%
  When el motor de ingesta evalúa la validez del paquete
  Then marca la medición como "VÁLIDA"
  And permite que el dato pase al motor de evaluación de reglas de negocio

### Scenario: Descarte de lecturas fuera del rango físico posible por falla de hardware
  Given una lectura recibida con temperatura de 150.0 °C o humedad de -5.0% debido a un cortocircuito en el sensor
  When el motor de ingesta evalúa los valores de la medición
  Then el sistema descarta el registro para el cálculo de promedios o anomalías
  And registra un evento en la bitácora del sistema indicando "ERROR_LECTURA_HARDWARE"

---

## US-04: Detección en tiempo real de anomalías ambientales
Como supervisor de operaciones de la bodega industrial,  
quiero que el sistema identifique automáticamente cuando cualquier medición supere los umbrales críticos (temperatura > 35 °C o humedad > 80%),  
para detectar de manera inmediata condiciones que puedan deteriorar las mercancías almacenadas.

**Story Points:** 5  
**Prioridad (MoSCoW):** Must Have  

### Scenario: Detección de anomalía por superación del umbral de temperatura (> 35 °C)
  Given que los umbrales máximos configurados son 35.0 °C para temperatura y 80.0% para humedad
  When el sensor "BODEGA-ZONA-3" transmite una temperatura de 36.8 °C y humedad de 55.0%
  Then el motor de reglas clasifica el evento como "ANOMALÍA_TEMPERATURA"
  And actualiza el estado del nodo "BODEGA-ZONA-3" a "ALERTA_CRÍTICA"

### Scenario: Operación normal sin disparo de anomalía
  Given que los umbrales máximos configurados son 35.0 °C para temperatura y 80.0% para humedad
  When el sensor transmite una temperatura de 34.5 °C y humedad de 79.5%
  Then el sistema clasifica el evento como "OPERACIÓN_NORMAL"
  And mantiene el estado del nodo como "ACTIVO" sin generar banderas de anomalía

---

## US-05: Notificación automática ante alertas de anomalía
Como gerente de mantenimiento,  
quiero recibir una notificación inmediata por correo electrónico y SMS cuando se detecte una anomalía,  
para acudir a la zona afectada de la bodega y corregir la falla de ventilación o climatización en el menor tiempo posible.

**Story Points:** 5  
**Prioridad (MoSCoW):** Must Have  

### Scenario: Envío exitoso de notificación por humedad crítica
  Given que se ha generado un evento de "ANOMALÍA_HUMEDAD" del sensor "BODEGA-ZONA-1" con lectura del 85.0%
  When el servicio de notificaciones procesa el evento desde la cola de mensajería
  Then envía un correo electrónico y un SMS al personal de turno indicando el identificador de zona, valor actual y marca de tiempo
  And registra el envío de la alerta en la tabla de incidencias

### Scenario: Supresión de alertas repetitivas (Alert Throttling)
  Given que el sensor "BODEGA-ZONA-1" envió una notificación por humedad crítica hace 5 minutos
  When el mismo sensor reporta nuevamente humedad del 86.0% en el ciclo actual (30 segundos después)
  Then el sistema registra la medición y mantiene el estado de incidente
  And suprime el envío de un nuevo correo electrónico para evitar saturar al personal operativo

---

## US-06: Panel de control (Dashboard) en vivo de la bodega
Como supervisor de la bodega,  
quiero visualizar en un tablero central el estado actual, última lectura y tiempo transcurrido desde la última transmisión de los 10 nodos,  
para obtener una vista rápida y panorámica de las condiciones ambientales en toda la instalación industrial.

**Story Points:** 8  
**Prioridad (MoSCoW):** Should Have  

### Scenario: Actualización en vivo de la tarjeta de un sensor
  Given que el supervisor tiene el dashboard web abierto en su navegador
  When cualquiera de los 10 nodos envía una medición válida y es procesada por el servidor
  Then la interfaz web actualiza automáticamente los valores de temperatura y humedad en menos de 2 segundos sin recargar la página
  And actualiza el contador de tiempo a "Hace unos segundos"

### Scenario: Destello visual en el tablero al activarse una alerta
  Given que la vista general de los 10 sensores está renderizada en pantalla
  When el nodo "BODEGA-ZONA-8" cambia su estado en el backend a "ALERTA_CRÍTICA"
  Then el fondo de la tarjeta del sensor en la pantalla cambia a color rojo visible
  And emite una señal visual en el mapa del plano de la bodega para guiar al operador

---

## US-07: Monitoreo de salud del nodo y detección de desconexiones (Heartbeat)
Como ingeniero de soporte técnico,  
quiero que el sistema detecte cuando un sensor deje de transmitir datos por más de 90 segundos (3 ciclos perdidos),  
para identificar fallas de alimentación eléctrica o pérdida de conectividad inalámbrica de los dispositivos.

**Story Points:** 5  
**Prioridad (MoSCoW):** Should Have  

### Scenario: Marcaje automático de un nodo caído (Offline)
  Given un nodo sensor cuyo último registro de telemetría ocurrió a las 14:00:00 y su estado era "ACTIVO"
  When el reloj del servidor alcanza las 14:01:31 sin haber recibido nuevas mediciones de ese dispositivo
  Then el planificador de monitoreo de salud cambia el estado del dispositivo a "OFFLINE"
  And genera una alerta técnica indicando "PÉRDIDA_DE_CONECTIVIDAD"

### Scenario: Restablecimiento automático de conectividad de un sensor
  Given un nodo sensor que se encuentra actualmente clasificado en estado "OFFLINE"
  When el dispositivo restablece la comunicación y transmite una lectura válida de temperatura y humedad
  Then el sistema retorna automáticamente el estado del sensor a "ACTIVO"
  And cierra la incidencia técnica de conectividad registrada

---

## US-08: Exportación de reportes históricos de telemetría
Como auditor de control de calidad,  
quiero consultar el historial de mediciones por fecha, turno y nodo sensor, y descargarlo en un archivo CSV,  
para certificar ante los clientes que sus productos se almacenaron en un ambiente controlado dentro de los estándares legales.

**Story Points:** 5  
**Prioridad (MoSCoW):** Should Have  

### Scenario: Descarga exitosa del historial en formato CSV
  Given que existen 2,880 registros para el sensor "BODEGA-ZONA-5" en las últimas 24 horas
  When selecciono el rango de fechas de ayer y ejecuto la acción "Descargar CSV"
  Then el sistema genera un archivo conteniendo las columnas de Fecha/Hora, ID del Nodo, Temperatura y Humedad
  And descarga el archivo en el navegador en menos de 3 segundos

### Scenario: Consulta en un intervalo de tiempo sin datos registrados
  Given que un usuario ejecuta una búsqueda para un rango de fechas donde la bodega estuvo fuera de operación
  When el sistema procesa la consulta de base de datos y obtiene cero resultados
  Then muestra un aviso en pantalla con el texto "No se encontraron mediciones para el rango seleccionado"
  And deshabilita el botón de descarga del reporte

---

## US-09: Configuración dinámica de umbrales de alerta por zona
Como administrador del sistema,  
quiero personalizar los umbrales máximos de temperatura y humedad de forma independiente para cada uno de los 10 sensores,  
para adaptar las alertas al tipo específico de inventario almacenado en cada sector (ej. zona de secado vs. zona de congelados).

**Story Points:** 3  
**Prioridad (MoSCoW):** Could Have  

### Scenario: Modificación exitosa del umbral para una zona específica
  Given que el sensor "BODEGA-ZONA-2" tiene un umbral de humedad por defecto de 80.0%
  When el administrador edita la configuración de ese nodo fijando el umbral máximo de humedad en 60.0%
  Then el sistema actualiza los parámetros en la base de datos
  And las lecturas futuras de ese nodo superiores al 60.0% dispararán una anomalía

### Scenario: Prevención de configuración de umbrales inválidos
  Given que el usuario se encuentra en la pantalla de edición de umbrales de un nodo
  When ingresa un umbral mínimo de 40.0 °C y un umbral máximo de 20.0 °C
  Then el sistema bloquea el guardado de la configuración
  And muestra el mensaje de error "El umbral máximo debe ser mayor que el umbral mínimo"

---

## US-10: Modo de mantenimiento y suspensión temporal de alertas
Como técnico de mantenimiento,  
quiero colocar un nodo sensor en "Modo Mantenimiento" por un intervalo determinado (ej. 2 horas),  
para poder recalibrar hardware, limpiar componentes o cambiar baterías sin disparar falsas alertas ni alterar los KPI de la bodega.

**Story Points:** 3  
**Prioridad (MoSCoW):** Won't Have (para el MVP)  

### Scenario: Activación del modo de mantenimiento para evitar falsas alarmas
  Given un sensor operando con estado "ACTIVO" en una zona programada para fumigación y limpieza
  When el técnico activa la opción "Modo Mantenimiento" especificando una duración de 120 minutos
  Then el sistema actualiza el estado del nodo a "MANTENIMIENTO"
  And suprime temporalmente la evaluación de anomalías y el envío de notificaciones para dicho nodo

### Scenario: Reactivación automática al expirar el tiempo de mantenimiento
  Given que un nodo ha permanecido en "Modo Mantenimiento" durante los 120 minutos programados
  When el temporizador de tareas del backend detecta que el tiempo de suspensión expiró
  Then el sistema retorna automáticamente el estado del nodo a "ACTIVO"
  And reanuda la evaluación periódica de umbrales cada 30 segundos