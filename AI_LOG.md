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


# Bitácora de Inteligencia Artificial - Semana 4

---

## [2026-08-04] — Entrada 1: Dockerización y Arquitectura de Contenedores

### Lo que aprendí e Implementaciones
Este día me enfoqué en el despliegue mediante contenedores. Comprendí que el orden de las instrucciones en el `Dockerfile` es crítico para optimizar los tiempos de construcción mediante la caché de capas. Implementé una imagen ligera (`python:3.12-slim`) y configuré el entorno para separar la instalación de dependencias del código fuente. Logré construir y ejecutar mi servicio **SensorHub** localmente utilizando `docker build` y `docker run`.

### Prompts y Uso de IA
Utilicé la IA para optimizar mi flujo de trabajo con Docker:
*  **Optimización:** Le pedí que revisara mi `Dockerfile` para asegurar que el orden de `COPY` y `RUN` fuera el más eficiente para aprovechar la caché de capas.
*  **Depuración de Entorno:** Consulté sobre cómo manejar correctamente la variable `DATABASE_URL` para que el contenedor funcionara tanto en desarrollo (SQLite) como en producción (PostgreSQL).
*  **Buenas Prácticas:** Pedí explicaciones sobre por qué se prefiere `python:slim` sobre la imagen completa para entornos de microservicios.

### Reflexión
> Entender que el `Dockerfile` funciona por capas cambió mi perspectiva sobre el desarrollo. Al principio, reconstruía todo ante cualquier cambio; ahora, al separar las dependencias en una capa, el desarrollo es mucho más ágil. Es un primer paso fundamental para garantizar que el software funcione igual en mi computadora que en el servidor.

---

## [2026-08-06] — Entrada 2: Docker Compose, PostgreSQL y Migraciones con Alembic

### Lo que aprendí e Implementaciones
Día de integración compleja. Implementé `docker-compose.yml` para orquestar la API con una base de datos PostgreSQL, gestionando volúmenes para la persistencia de datos (`pgdata`). Aprendí la importancia del driver `psycopg` para conectar SQLAlchemy con Postgres y normalicé la cadena de conexión en `db.py` para asegurar compatibilidad entre entornos. Finalmente, inicialicé **Alembic** para gestionar el versionado de mi esquema de base de datos.

### Prompts y Uso de IA
La IA fue clave para navegar los errores de conectividad:
*  **Solución de Errores:** Cuando obtuve un `ModuleNotFoundError` con psycopg, la IA me explicó la diferencia entre `psycopg2` y el nuevo `psycopg` (driver binario).
*  **Refactorización:** Pedí ayuda para escribir una función en `db.py` que detectara y normalizara automáticamente la URL de la base de datos, manejando los prefijos `postgres://` vs `postgresql+psycopg://`.
*  **Alembic:** Solicité una guía paso a paso para configurar el versionado inicial sin borrar mis datos de prueba locales.

### Reflexión
> La gestión de bases de datos siempre me había parecido una tarea manual y arriesgada. Con Alembic, siento que he pasado de "intentar no romper la base de datos" a tener un control real y auditable sobre ella. La orquestación con Docker Compose facilita enormemente el testing, permitiéndome levantar todo el ecosistema con un solo comando.

---

## [2026-08-06] — Entrada 3: CI/CD y Calidad de Código con GitHub Actions

### Lo que aprendí e Implementaciones
Aprendí a automatizar la validación de mi código. Implementé un pipeline de **GitHub Actions** que se dispara con cada `push` a `main`. El pipeline incluye: *Linting* (Ruff), validación de tipos (Mypy) y pruebas unitarias con cobertura (Pytest + Cov). Aprendí que un CI bien configurado no solo detecta errores, sino que actúa como una red de seguridad antes de cualquier despliegue.

### Prompts y Uso de IA
La IA actuó como guía de arquitectura de pruebas:
*  **CI/CD:** Le pedí que estructurara mi archivo `.github/workflows/ci.yml` para incluir las distintas etapas de validación (linting, types, tests).
*  **Simulación de Fallos:** Le pregunté cómo escribir pruebas que forzaran una falla para verificar que el pipeline de GitHub Actions realmente detuviera un despliegue con código roto.
*  **Métricas:** Consulté cómo interpretar el reporte de cobertura de `pytest-cov` y cómo configurar el `fail-under=80` para mantener la calidad.

### Reflexión
> "Romper algo a propósito" para ver el CI fallar fue revelador. Me di cuenta de que un pipeline de CI no es solo un requisito burocrático, sino una herramienta de confianza. Ahora entiendo qué le responderé al coordinador cuando pregunte qué protege mi código: la automatización es mi primer filtro de calidad.

---

## [2026-08-07] — Entrada 4: Despliegue en la Nube con Render

### Lo que aprendí e Implementaciones
Logré el despliegue real de la API en **Render** usando infraestructura como código (`render.yaml`). Comprendí el concepto de "despertar" el servicio (cold start) y la importancia de configurar migraciones de base de datos en el comando de arranque del servidor. Ahora, cualquier cambio enviado a GitHub se despliega automáticamente, logrando una URL pública para **SensorHub**.

### Prompts y Uso de IA
*  **Infraestructura:** Pedí ayuda para traducir mi configuración de `docker-compose` al formato `render.yaml` de Render.
*  **Despliegue:** Consulté cómo concatenar comandos (`alembic upgrade head && uvicorn...`) para asegurar que la base de datos esté siempre migrada antes de que la aplicación reciba tráfico.
*  **Diagnóstico:** Pregunté sobre por qué la API tardaba en responder después de un tiempo de inactividad, aprendiendo sobre los límites del "free tier".

### Reflexión
> Ver mi API funcionando con una URL pública fue el cierre perfecto. Logré entender que el despliegue no es el final de la cadena, sino una extensión de todo lo hecho anteriormente. La combinación de Docker, Alembic y CI/CD hizo que el despliegue en la nube fuera un proceso fluido y profesional, lejos de las configuraciones manuales de antaño.


## [2026-08-08] — Entrada 5: Evaluación 2 - Pipeline de Producción de SensorHub

### Lo que aprendí e Implementaciones
Este día representó la cúspide de la integración y validación de todo lo construido durante la semana. Enfrenté el reto de consolidar el pipeline de producción completo para **SensorHub**. Perfeccioné el uso de variables de entorno para garantizar cero secretos en el historial del repositorio, integré el badge de estado del pipeline de CI en el README y aseguré que tanto el endpoint `/health` como la documentación interactiva en `/docs` estuvieran accesibles en la URL pública de Render. 

Comprendí a fondo la importancia de verificar que el despliegue continuo respondiera en tiempo real a cada commit enviado a la rama principal, manteniendo una cobertura de pruebas estricta superior al 80%.

### Prompts y Uso de IA
Mi uso de la IA se centró en la validación final de los entregables y la resolución de detalles finos de configuración:
*  **Auditoría de Entregables:** Le pedí que revisara la lista de requisitos de la evaluación para confirmar que no faltara ningún archivo crítico en el repositorio (como la correcta estructura del `render.yaml` y el `docker-compose.yml`).
*  **Inclusión de Badges:** Consulté la sintaxis exacta en Markdown para generar y colocar el badge de GitHub Actions en el README apuntando correctamente al estado del pipeline de CI.
*  **Verificación de Seguridad:** Validé con su ayuda las mejores prácticas para asegurar que ninguna credencial o variable sensible quedara expuesta en el historial de commits antes de realizar la entrega final.

### Reflexión
> Ver la evaluación integrada de esta manera me dio una perspectiva profesional del ciclo de vida del software. No se trata solo de escribir código que funcione en local, sino de asegurar la reproducibilidad con Docker, la integridad con las migraciones y pruebas, y la automatización total con CI/CD y despliegue continuo. Superar esta evaluación con una URL pública funcional y un pipeline en verde consolidó todo lo aprendido en una solución robusta y lista para producción.