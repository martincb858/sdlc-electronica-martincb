# 🛠️ SDLC Electrónica - Martín

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.x-59666C?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Render">
  <a href="https://github.com/martincb858/sdlc-electronica-martincb/actions/workflows/ci.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/martincb858/sdlc-electronica-martincb/ci.yml?branch=main&style=for-the-badge&logo=github" alt="CI">
  </a>
</div>

---

## 📝 Descripción del proyecto
Este repositorio reúne una serie de ejercicios y una API real para el desarrollo de software con enfoque en calidad, pruebas y buenas prácticas. El proyecto principal es una API REST con FastAPI para gestionar sensores IoT y sus lecturas, con validaciones de dominio y soporte para despliegue en Render.

---

## ✨ Funcionalidades principales
- Gestión de sensores: crear, listar, consultar, actualizar y desactivar
  (soft-delete: un sensor desactivado deja de aceptar lecturas nuevas, pero
  su histórico sigue consultable), con umbral de alerta configurable.
- Gestión de lecturas: ingesta con validación física por tipo de sensor,
  consulta paginada con filtro por rango de fechas.
- Detección de anomalías: una lectura que supera el umbral del sensor
  genera automáticamente una alerta.
- Gestión de alertas: consulta filtrable por estado y cambio de estado
  (`open -> acknowledged -> resolved`, validado como máquina de estados).
- Estadísticas por sensor y periodo: mínimo, máximo y promedio.
- Endpoint de salud (`/health`) y métricas básicas (`/metrics`).
- Logging estructurado en JSON y manejo global de errores.
- Configuración exclusivamente por variables de entorno.

---

## 🚀 Stack utilizado
- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- Pytest
- Ruff
- Mypy

---

## 🏗️ Arquitectura

Cuatro capas, cada una conoce solo la inmediata inferior. Ver
[ADR-0001](docs/adr/0001-arquitectura-en-capas.md) y
[ADR-0002](docs/adr/0002-ciclo-de-vida-de-alertas.md) para el porqué.

```mermaid
flowchart TB
    subgraph client["Cliente"]
        HTTP["HTTP / Swagger UI"]
    end

    subgraph presentacion["Presentación — app/routers/"]
        SR["sensor_router"]
        RR["reading_router"]
        AR["alert_router"]
        HR["health_router"]
    end

    subgraph aplicacion["Aplicación — app/services/"]
        SS["SensorService"]
        RS["ReadingService"]
        AS["AlertService"]
        AD["AnomalyDetectorService"]
        MS["MetricsService"]
    end

    subgraph dominio["Dominio — app/domain/ (Python puro)"]
        VAL["validators.py<br/>(física por unidad)"]
        TYP["sensor_types.py<br/>(unidades por tipo)"]
        ALS["alert_states.py<br/>(máquina de estados)"]
        STA["stats.py<br/>(min/max/avg)"]
        ALT["alerts.py<br/>(estrategias de notificación)"]
    end

    subgraph infra["Infraestructura — app/repositories/, db.py"]
        SREPO["SqlAlchemySensorRepository"]
        RREPO["SqlAlchemyReadingRepository"]
        AREPO["SqlAlchemyAlertRepository"]
        DB[("SQLite local /<br/>PostgreSQL producción")]
    end

    HTTP --> SR & RR & AR & HR
    SR --> SS
    RR --> RS
    AR --> AS
    HR --> MS

    RS --> VAL & TYP
    RS --> AD
    AD --> ALT
    AS --> ALS
    RS --> STA

    SS --> SREPO
    RS --> RREPO
    AS --> AREPO
    MS --> SREPO & RREPO & AREPO

    SREPO --> DB
    RREPO --> DB
    AREPO --> DB
```

**Flujo de una lectura con anomalía:**

```mermaid
sequenceDiagram
    participant C as Cliente
    participant R as reading_router
    participant S as ReadingService
    participant Rep as SensorRepository
    participant Det as AnomalyDetectorService
    participant DB as Base de datos

    C->>R: POST /sensors/TEMP-01/readings {value: 42.0, unit: "C"}
    R->>S: record("TEMP-01", 42.0, "C")
    S->>Rep: get_by_code("TEMP-01")
    Rep-->>S: Sensor(active=true, alert_threshold=35.0)
    S->>S: valida unidad + rango físico
    S->>DB: guarda Reading
    S->>Det: process_reading("TEMP-01", 42.0, threshold=35.0)
    Det->>DB: crea Alert(status="open")
    S-->>R: Reading
    R-->>C: 201 Created
```

---

## 🧱 Estructura del proyecto
- app/: aplicación FastAPI, routers, servicios, esquemas y modelo de base de datos.
- migrations/: migraciones de Alembic.
- tests/: pruebas de la API y de la lógica de negocio.
- semana1/, semana2/: ejercicios y prácticas de SDLC, diseño y testing.

---

## 🛠️ Instalación local

### 1. Clonar el repositorio
```bash
git clone https://github.com/martincb858/sdlc-electronica-martincb.git
cd sdlc-electronica-martincb
```

### 2. Crear y activar un entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecutar la API localmente
```bash
uvicorn app.main:app --reload
```

La API quedará disponible en:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

---

## 🧪 Ejecutar pruebas
```bash
pytest
```

---

## 🌐 API desplegada en Render
La versión publicada actualmente está disponible en:

https://sensorhub-api-7bkq.onrender.com/

Endpoints útiles:
- /health
- /metrics
- /docs
- /sensors
- /sensors/{sensor_code}/readings
- /sensors/{sensor_code}/stats
- /sensors/{sensor_code}/alerts
- /alerts/{alert_id} (PATCH para cambiar estado)

---

## ⚙️ Variables de entorno

Toda la configuración es exclusivamente por variables de entorno, sin
archivos de config adicionales:

| Variable | Default local | Descripción |
|---|---|---|
| `DATABASE_URL` | `sqlite:///sensorhub.db` | Cadena de conexión. Acepta `postgres://`/`postgresql://` y los normaliza a `postgresql+psycopg://`. |
| `LOG_LEVEL` | `INFO` | Nivel de logging (`DEBUG`, `INFO`, `WARNING`, `ERROR`). Logs emitidos como JSON estructurado a stdout. |

---

## 🐳 Ejecutar con Docker
```bash
docker compose up --build
```

---

## 📌 Notas
El despliegue en Render está configurado con Alembic para aplicar migraciones automáticamente antes de iniciar la aplicación.
