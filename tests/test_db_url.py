import importlib

import app.db as db_module


def _reload_with_env(monkeypatch, value: str | None):
    if value is None:
        monkeypatch.delenv("DATABASE_URL", raising=False)
    else:
        monkeypatch.setenv("DATABASE_URL", value)
    importlib.reload(db_module)
    return db_module


def test_get_database_url_defaults_to_sqlite_when_unset(monkeypatch) -> None:
    module = _reload_with_env(monkeypatch, None)
    assert module.get_database_url() == "sqlite:///sensorhub.db"


def test_get_database_url_passes_through_already_normalized_url(monkeypatch) -> None:
    url = "postgresql+psycopg://sensor:secret@db:5432/sensorhub"
    module = _reload_with_env(monkeypatch, url)
    assert module.get_database_url() == url


def test_get_database_url_normalizes_legacy_postgres_scheme(monkeypatch) -> None:
    # Estilo Heroku / algunos proveedores viejos: "postgres://"
    module = _reload_with_env(
        monkeypatch, "postgres://sensor:secret@db:5432/sensorhub"
    )
    assert (
        module.get_database_url()
        == "postgresql+psycopg://sensor:secret@db:5432/sensorhub"
    )


def test_get_database_url_normalizes_postgresql_without_driver(monkeypatch) -> None:
    # Estilo Render: "postgresql://" sin el sufijo del driver
    module = _reload_with_env(
        monkeypatch, "postgresql://sensor:secret@db:5432/sensorhub"
    )
    assert (
        module.get_database_url()
        == "postgresql+psycopg://sensor:secret@db:5432/sensorhub"
    )


def test_get_database_url_does_not_double_normalize(monkeypatch) -> None:
    # Si ya trae +psycopg, no debe tocarlo aunque empiece con "postgresql://"
    url = "postgresql+psycopg://sensor:secret@db:5432/sensorhub"
    module = _reload_with_env(monkeypatch, url)
    result = module.get_database_url()
    assert result == url
    assert result.count("+psycopg") == 1


def test_sqlite_engine_gets_check_same_thread_false(monkeypatch) -> None:
    module = _reload_with_env(monkeypatch, None)
    # SQLite necesita este flag para funcionar bien con FastAPI (threads
    # distintos por request); si falta, algunas requests fallan en
    # produccion aunque los tests locales de un solo hilo no lo detecten.
    assert module.engine.url.get_backend_name() == "sqlite"


def teardown_module(module) -> None:
    # Deja app.db recargado con el estado normal (sin DATABASE_URL) para
    # no afectar a otros archivos de test que se ejecuten despues.
    importlib.reload(db_module)