# Bitácora de Inteligencia Artificial - Semana 3
---

Esta bitácora documenta el proceso de aprendizaje, los desafíos técnicos y la integración de herramientas de Inteligencia Artificial durante la tercera semana de desarrollo, enfocada en la persistencia de datos, arquitectura de software y desarrollo de APIs.

---

##  [2026-07-28] — Entrada 1: Persistencia con SQLAlchemy 2.x

###  Lo que aprendí e Implementaciones
Durante esta jornada me adentré en el uso de **SQLAlchemy 2.x**. Aunque previamente había tenido interacciones básicas con bases de datos como SQLite, esta sesión funcionó como mucho más que un simple repaso, ya que me permitió comprender conceptos profundos del ORM que antes pasaba por alto. 

Aprendí sobre la nueva sintaxis y el paradigma de la versión 2.0, enfocándome en la declaración de modelos. Realicé varias implementaciones de prueba prácticas, ya que personalmente encuentro mucho más efectivo el aprendizaje empírico ("aprender haciendo") que la simple lectura de documentación. Esto me permitió asimilar cómo el código en Python se traduce en transacciones SQL reales.

###  Prompts y Uso de IA
Utilicé la IA como un tutor personalizado para desglosar conceptos complejos. Mis interacciones se centraron en:
1. **Funcionamiento de Core vs ORM:** Pedí explicaciones claras sobre la diferencia entre la capa de abstracción de base de datos (Core) y el mapeo objeto-relacional (ORM).
2. **Clases Base:** Solicité ejemplos sobre cómo estructurar y heredar de la clase `Base` declarativa.
3. **Mapeo de datos (`Mapped`):** Indagué sobre el uso de tipado estricto con `Mapped` y `mapped_column` introducidos en las versiones recientes.
4. **Operaciones CRUD:** Pedí ejemplos específicos de funciones de edición en la base de datos (operaciones `SELECT`, `JOIN`, `DELETE`, y actualizaciones de estado).

###  Reflexión
> El uso de SQLAlchemy facilita enormemente la interacción con la base de datos, pero tiene una curva de aprendizaje inicial pronunciada. Utilizar la IA para generar fragmentos de código de prueba fue clave para desbloquear mi comprensión. Me di cuenta de que tener una base teórica es importante, pero ver los datos persistir en tiempo real gracias a los scripts de prueba es lo que realmente consolida el conocimiento.

---

##  [2026-07-30] — Entrada 2: Patrón Repositorio y Capa de Servicio

###  Lo que aprendí e Implementaciones
Este fue un día de gran crecimiento técnico. Al iniciar la jornada, me sentía desorientado sobre cómo estructurar el proyecto, ya que el concepto de "Capa de Servicio" y "Patrón Repositorio" era completamente nuevo para mí. 

Aprendí que el **Patrón Repositorio** se encarga exclusivamente de la comunicación con la base de datos (abstraer las consultas), mientras que la **Capa de Servicio** encapsula toda la lógica de negocio (las reglas de la aplicación). Empecé a visualizar cómo esta separación de responsabilidades hace que el código sea más limpio, escalable y, sobre todo, testeable.

###  Prompts y Uso de IA
Mi flujo de trabajo con la IA cambió hacia un enfoque más arquitectónico y orientado a pruebas (TDD):
*   **Exploración conceptual:** Comencé pidiendo definiciones sencillas, casos de uso y ejemplos de código aplicados a Python sobre las capas de servicio y repositorios.
*   **Pseudocódigo para Tests:** En lugar de pedir código funcional de inmediato, escribí textualmente (en lenguaje natural y pseudocódigo) qué debían hacer mis pruebas. Envié este borrador a la IA para que me ayudara a estructurar los tests reales.
*   **Contraste de modelos:** Tomé la respuesta generada y la comparé utilizando otra IA para obtener una segunda opinión. A partir de las observaciones cruzadas, procedí a escribir el código de los repositorios y servicios de manera abstracta, apoyándome iterativamente en las sugerencias generadas.

###  Reflexión
> Delegar la fase de investigación a una IA ahorra incontables horas de lectura en foros y documentación fragmentada. Aunque eran temas de arquitectura de software que desconocía por completo, la IA me proporcionó el contexto mínimo viable para empezar a codificar. Sin embargo, aprendí una lección valiosa: los LLMs pueden desviarse del tema o proponer arquitecturas sobredimensionadas, por lo que es crucial mantener el pensamiento crítico y revisar línea por línea cada sugerencia antes de integrarla.

---

##  [2026-07-30] — Entrada 3: Inyección de Dependencias y Convenciones REST

###  Lo que aprendí e Implementaciones
Teniendo como base mis experimentos previos con el Swagger de FastAPI, el objetivo de hoy era conectar las piezas del rompecabezas. Sabía que debía unir mi `main.py` con los repositorios y servicios creados el día anterior, pero el mecanismo de "cómo" hacerlo era confuso. 

Aprendí sobre la **Inyección de Dependencias** (usando `Depends` en FastAPI) para proveer instancias de la base de datos y servicios a las rutas. Además, reforcé mi comprensión sobre las convenciones REST y el uso correcto de los verbos HTTP (`GET`, `POST`, `PUT`, `DELETE`) para estructurar los endpoints de la API. Realicé la implementación base conectando la DB, los repositorios, los servicios y los controladores en el `main.py`.

###  Prompts y Uso de IA
*   **Integración de Componentes:** Solicité un ejemplo concreto de cómo inyectar la sesión de la base de datos hacia el repositorio, y a su vez, cómo inyectar el repositorio en el servicio, para finalmente usar el servicio en el endpoint.
*   **Verbos HTTP:** Pedí a la IA que me generara la estructura de los verbos en FastAPI. 

Reconozco que en este punto no cuestioné demasiado la lógica generada; tomé el código, lo revisé superficialmente asegurándome de que no hubiera errores evidentes, y lo adapté a mi proyecto para hacerlo funcionar.

###  Reflexión
> Hoy fue un día donde dependí fuertemente de la IA para avanzar, ya que la teoría detrás de la Inyección de Dependencias y REST se me hizo algo abstracta inicialmente. Aunque logré que la aplicación corriera y los endpoints aparecieran en Swagger, me quedó una sensación de no haber comprendido el mecanismo subyacente al 100%. Esto me deja como tarea pendiente revisar este código con más detenimiento para no ser solo un "copiador de código", sino entender el porqué de cada inyección.

---

##  [2026-08-03] — Entrada 4: Ejercicio Integrador - API completa de SensorHub

###  Lo que aprendí e Implementaciones
Este día representó el cierre y la consolidación de todos los conceptos de la semana. Finalmente tuve el momento "¡Ajá!" respecto a la arquitectura en capas. Al intentar integrar todo en la API de **SensorHub**, me topé con varios errores de ejecución que me obligaron a revisar a fondo cómo interactuaban las diferentes partes.

Comprendí de manera mucho más clara el rol de **Pydantic** (validación de datos de entrada/salida y serialización) frente a los modelos de SQLAlchemy (interacción con la base de datos). También aprendí a modularizar la aplicación utilizando **Routers** (`APIRouter` de FastAPI) para no saturar el `main.py`, y apliqué pruebas de integración reales a la API utilizando `TestClient`.

###  Prompts y Uso de IA
Mi uso de la IA fue exhaustivo, actuando como compañero de depuración (pair-programming):
*   **Debugging:** Pegué trazas de errores (tracebacks) que no lograba comprender, pidiendo a la IA que me explicara la causa raíz en lugar de solo darme la solución.
*   **Reestructuración (Refactoring):** Le pedí que me explicara con mayor detalle la justificación de separar los esquemas (Schemas/Pydantic) de los modelos (Models/SQLAlchemy).
*   **Modularidad:** Solicité ejemplos de cómo implementar `APIRouter` para separar los endpoints de SensorHub y cómo registrar esos routers en el `main`.
*   **Testing:** Generamos en conjunto pruebas con `TestClient` para validar la API, lo que me ayudó a entender si mi división de capas realmente estaba funcionando.

###  Reflexión
> Este ha sido el día de mayor uso de IA, pero también el día de mayor asimilación técnica. Los errores que experimenté al inicio me forzaron a deconstruir lo que había hecho en los días previos. Por fin logré interiorizar *por qué* separamos el código: mantener los routers limpios, delegar la lógica a los servicios y el manejo de datos a los repositorios. 
> 
> La IA fue instrumental no solo para proveer ejemplos, sino para explicarme la filosofía detrás del diseño de software. Superar este desafío con SensorHub me ayudó a corregir la integración "sencilla pero frágil" que tenía antes, dejándome con conocimientos mucho más sólidos, estructurados y listos para ser aplicados en proyectos futuros.