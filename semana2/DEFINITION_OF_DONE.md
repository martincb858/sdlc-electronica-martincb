# Definition of Done (DoD)

Para que una historia de usuario o tarea técnica sea considerada **Terminada**, debe cumplir con:

## 1. Pruebas (pytest)
1. **Desarrollo guiado por pruebas (TDD):** El historial de Git demuestra que las pruebas se escribieron y fallaron primero (*RED*), luego se hizo pasar el código (*GREEN*) y finalmente se limpió (*REFACTOR*).
2. **Criterios Gherkin en código:** Los escenarios de la historia (Given-When-Then) están implementados como funciones de prueba en `pytest`.
3. **Cobertura mínima obligatoria:** Al correr `pytest`, la suite ejecuta el análisis de cobertura (`pytest-cov`) y supera el umbral del 80% sin fallos en ninguna prueba.

## 2. Análisis de Código (ruff y mypy)
1. **Estilo y buenas prácticas limpios (ruff):** El comando `ruff check .` se ejecuta en la terminal y devuelve `0` errores o advertencias para las reglas configuradas (E, F, I, UP, B).
2. **Tipado estático estricto (mypy):** El comando `mypy .` se ejecuta sin reportar errores. Todas las funciones y métodos creados tienen anotaciones de tipo explícitas en sus parámetros y en su valor de retorno (`disallow_untyped_defs = true`).
3. **Mypy en modo estricto:** Además de `disallow_untyped_defs`, incluir `strict_optional = true.


## 3. Proceso y Control de Versiones (Git & PRs)
1. **Desarrollo en rama aislada:** Todo el código de la historia se trabajó en una rama independiente descriptiva (ej. `feature/us-XX-nombre-historia`), nunca directamente en `main`.
2. **Auto-revisión de Pull Request (Diff):** El autor leyó su propio *diff* línea por línea antes de unir la rama, asegurando que no queden rastros de depuración (`print()`, `pdb`, comentarios de código muerto).
3. **Sin conflictos:** La rama está actualizada con `main` y resuelve los conflictos antes del merge.