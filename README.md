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
- Gestión de sensores: crear, listar, consultar, actualizar y eliminar.
- Gestión de lecturas: registrar historiales por sensor y consultar lecturas individuales.
- Validaciones de negocio por tipo de sensor.
- Endpoints de salud para monitoreo.
- Configuración preparada para base de datos y despliegue en producción.

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
- /docs
- /sensors
- /sensors/{sensor_code}/readings

---

## 🐳 Ejecutar con Docker
```bash
docker compose up --build
```

---

## 📌 Notas
El despliegue en Render está configurado con Alembic para aplicar migraciones automáticamente antes de iniciar la aplicación.
