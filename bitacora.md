# Bitácora de IA
---

## [2026-07-16] — Entrada 1: Python idiomático para ingenieros de C


###  Lo que aprendí / Implementaciones
1. **Inmutabilidad con Dataclasses:** Reemplazar los structs mutables tradicionales por instancias `frozen=True`. Si un dato cambia (ej. conversión a Fahrenheit o Kelvin), se genera un nuevo objeto en lugar de sobreescribir el registro en memoria, evitando efectos secundarios.
2. **Protocolos (`typing.Protocol`):** Definición de interfaces estructurales sin herencia forzada (Duck Typing estático), ideal para desacoplar drivers de hardware de la lógica de procesamiento.
3. **Serialización Cruda:** Uso de `struct.pack('!d', ...)` para empaquetar flotantes de 64 bits en Big-Endian, permitiendo una comunicación directa con microcontroladores receptores.

###  Notas de Verificación de Calidad
El código fue verificado localmente utilizando las herramientas del entorno de QA:
* **Mypy (`--strict`):** Validación de firmas exitosa. Cero tipos dinámicos implícitos (`Any`).
* **Ruff:** Ninguna correccion realizada por ```ruff check ejercicios.py``` y formateo mediante ```ruff format ejercicios.py```

### Prompts utilizados
Para el desarrollo de esta actividad se utilizo un LLM para profundizar en algunos aspectos del codigo:
1. **Ejemplos de codigo:** Se solicitaron ejemplos de codigo en el cual se utilizan las funciones especificadas en el codigo de ejemplo, posteriormente se analiza cada ejemplo linea por linea para una mayor comprension.
2. **Ejemplificacion de uso de mypy y ruff:** Se solicita un ejemplo practico del uso de mypy y ruff para hacer test y aprender el uso practico de estas dos herramientas.
3. **Formato de archivos .md:** Por ultimo se solicita ayuda para formatear la bitacora y aprender a darle formatos en archivos del tipo `bitacoras.md`