# Product Backlog — Sistema de Monitoreo IoT

## US-01: Autenticación y registro del nodo sensor
Como administrador del sistema de monitoreo,
quiero dar de alta un nodo sensor asignándole una dirección MAC y credenciales de acceso,
para garantizar que únicamente los dispositivos autorizados puedan transmitir mediciones a la base de datos central.

**Story Points:** 3

### Scenario: Registro exitoso de un nuevo nodo sensor
  Given una dirección MAC "00:1B:44:11:3A:B7" que no ha sido registrado previamente
  When envío la solicitud de alta utilizando la direccion MAC "00:1B:44:11:3A:B7"
  Then el sistema almacena el dispositivo con estado "ACTIVO"
  And devuelve un mensaje "El dispositivo se registro correctamente"

### Scenario: Rechazar el registro de una dirección MAC duplicada
  Given una dirección MAC "00:1B:44:11:3A:B7" que ya se encuentra en el sistema
  When envío una solicitud de alta utilizando la misma dirección MAC
  Then el sistema rechaza la operación
  And devuelve el mensaje "El dispositivo ya se encuentra registrado"

---

## US-02: Recepción y validación de datos
Como administrador del sistema,
quiero recibir un paquete de datos con variables de temperatura, humedad y nivel de batería,
para actaulizar las mediciones en tiempo real.

**Story Points:** 5

### Scenario: Recepción de trama de datos en rangos normales
  Given un nodo registrado con el identificador "NODO1"
  When el dispositivo transmite una lectura de temperatura de 22.5 C, humedad de 55% y batería al 88% con el timestamp actual
  Then el servidor valida que las variables estén dentro de las tolerancias físicas del hardware
  And almacena el registro y devuelve el mensaje "NODO1: temperatura: 22.5 C, humedad: 55%, batería: 88%"

### Scenario: Descartar mediciones fuera del umbral físico del sensor
  Given un nodo registrado con el identificador "NODO1"
  When el paquete entrante indica una lectura de temperatura de -150 C, humedad de 55% y batería al 88%
  Then el sistema rechaza el registro de datos
  And almacena el registro y devuelve el mensaje "NODO1: temperatura: ERROR, humedad: 55%, batería: 88%"

---

## US-03: Generación de alertas automáticas por batería muy baja
Como administrador del sistema,
quiero recibir una notificación en la interfaz cuando el nivel de voltaje de la bateria de un nodo caiga por debajo de un umbral seguro,
para solicitar el reemplazo de su bateria antes de que el equipo pierda conectividad.

**Story Points:** 8

### Scenario: Enviar alerta de voltaje crítico
  Given el nodo "NODE1" operando de manera normal en la red
  When el dispositivo envía una actualizacion reportando un nivel de batería de < 15% 
  Then el sistema cambia el estado del nodo a "Bateria_baja"
  And genera una alerta visible en el panel de control del administrador

### Scenario: Restablecer estado de salud tras el reemplazo de batería
  Given un nodo sensor que actualmente se encuentra en estado "Bateria_baja"
  When el dispositivo envía una nueva lectura reportando una capacidad de batería del 99%
  Then el sistema actualiza el estado del dispositivo a "NORMAL"
  And archiva y marca como resuelta la alerta anterior de bateria baja

---

## US-04: Deteccion y alerta de nodo desconectado
Como administrador del sistema,
quiero recibir una notificación cuando un nodo sensor activo deje de transmitir datos durante un intervalo prolongado,
para identificar errores en el sistema y resolverlos lo mas pronto posible.

**Story Points:** 5

### Scenario: Deteccion de inactividad
  Given un nodo con su intervalo maximo configurado en 15 minutos
  When transcurren 15> minutos sin que el servidor reciba actualizacion del nodo
  Then el servidor actualiza el estado del nodo a "Dispositivo apagado"
  And manda una alerta al panel de control.

### Scenario: Reconeccion del nodo
  Given nodo sensor con estado desconectado
  When el servidor recibe un nuevo mensaje de dicho nodo
  Then el sistema actualiza el estado del sensor a "ACTIVO"
  And registra el tiempo estimado que el nodo estuvo desconectado

---

## US-05: Exportación de reportes de calibración en formato CSV
Como administrador del sistema,
quiero descargar un archivo CSV con el historial de lecturas de un nodo por rango de fechas,
para realizar análisis y procesos de calibración.

**Story Points:** 3

### Scenario: Exportación exitosa dentro de un periodo válido
  Given un nodo con lecturas almacenadas durante los últimos 30 días
  When solicito la exportación de datos estableciendo fecha de inicio "2026-07-01" y fecha de fin "2026-07-07"
  Then el sistema genera y descarga un archivo `.csv` con los encabezados "d, temperatura, humedad, nivel de bateria"
  And las filas corresponden a la hora y fecha.

### Scenario: Consulta de un periodo sin registros telemétricos
  Given que un nodo sensor estuvo apagado por mantenimiento durante toda la semana pasada 
  When solicito generar el reporte CSV exactamente para esa semana
  Then el sistema devuelve un archivo CSV que únicamente contiene la fila de los encabezados 
  And muestra un aviso informativo en pantalla indicando "Dispositivo apagado"

