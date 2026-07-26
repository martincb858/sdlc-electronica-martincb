# Sprint Retrospective — Sprint 1: Núcleo de Ingesta y Alertas IoT

## 1. Resumen
El Sprint 1 concluyó con una arquitectura sólida y funcional para el núcleo de monitoreo industrial. La adopción de **TDD (Test-Driven Development)** y **principios SOLID** permitió construir una base mantenible y escalable. Aunque la gran mayoría de los componentes (`SensorReading`, `PhysicalRangeValidator`, `AnomalyDetector`) superaron las expectativas y pruebas con éxito, el módulo de alertas (`AlertManager`) se identificó como el principal foco de deuda técnica y riesgo operativo antes de pasar a un entorno de producción.

---

## 2. ¿Qué salió bien?

* **Adopción exitosa de TDD y Principios SOLID:** La separación estricta de responsabilidades entre la estructura de datos (`SensorReading`), el validador de rangos (`PhysicalRangeValidator`) y el evaluador de reglas (`AnomalyDetector`) evitó el acoplamiento y facilitó un diseño limpio sin valores fijados en el código (*hardcoded*).
* **Eficiencia mediante pruebas parametrizadas:** El uso de `@pytest.mark.parametrize` optimizó el tiempo de desarrollo en solitario al permitir validar múltiples combinaciones de entrada y análisis de valores frontera (*Boundary Value Analysis*) en un solo bloque de código limpio y sin repeticiones (principio DRY).

---

## 3. ¿Qué debemos mejorar? (What to Improve)

* **Cobertura incompleta en el Gestor de Alertas (`AlertManager`):** Aunque las pruebas de integración pasaron exitosamente en verde, el módulo no alcanza el **100% de cobertura** en los reportes de `pytest-cov`. Esto evidencia la existencia de ramas condicionales, caminos de error o excepciones en la lógica de *throttling* y envío que aún no se ejecutan en las pruebas automatizadas.
* **Fragilidad ante fallos en los canales de notificación:** Las pruebas del `AlertManager` demostraron que, en escenarios reales, el envío de correos o SMS puede fallar silenciosamente o lanzar excepciones no controladas si un servicio externo o la red se cae, lo cual compromete la estabilidad del ciclo general de monitoreo.
* **Persistencia temporal del Throttling:** Actualmente, el control para evitar envíos repetidos en ventanas de 5 minutos reside en un diccionario en memoria (`_last_alert_time`). Si el servidor experimenta un reinicio o una caída temporal, este historial se pierde, ocasionando ráfagas de alertas duplicadas al reactivarse el sistema.

---

## 4. Plan de Acción Concreta para el Sprint 2

> **Acción Principal:** Refactorizar y blindar el módulo `AlertManager` para alcanzar el **100% de cobertura de pruebas**.