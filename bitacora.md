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

## [2026-07-16] — Entrada 2:  La FSM que ya conoces, ahora orientada a objetos (3–4 h)


###  Lo que aprendí / Implementaciones
1. **Test con pytest:** Realizar test con `pytest` es algo muy interesante ya que ejecuta las funciones que tengan la forma `def test_function():` lo que hace muy facil generar un codigo el cual pueda poner a prueba la funcionalidad de nuestro codigo en casos que nosotros esperamos.
2. **Assert en test:** La funcion `assert` es una funcion que es nueva para mi pero muy interesante ya que es muy util para testear el codigo, esta funcion nos ayuda a saber si algo es `True` o `False` como un `if` pero mucho mas sencillo y mas util para los test.

###  Notas de Verificación de Calidad
El código fue verificado localmente utilizando una de las herramientas del entorno:
* **Pytest:** Dandonos una validacion exitosa sin ninguna obseervacion

### Prompts utilizados
1. **Ejemplos de codigo:** Gracias a solicitar ejemplos de codigo reales pude observar funciones nuevas como lo fueron los assert que posteriormente implemente.
2. **Explicacion de codigos:** Al momento de observar nuevas funciones solicite una explicacion mas extensa sobre estos metodos y sobre su funcion real.


## [2026-07-18] — Entrada 3:  SOLID en la práctica: S, O y L (3–4 h)


###  Lo que aprendí / Implementaciones
1. **Aprendizaje de SRP:** Comprendi un poco el enfoque que tiene este principio, el cual es separar las tareas para que cada clase se encargue de una sola tarea.
2. **Aprendizaje de OCP:** El principio de Abierto/Cerrado fue algo que fue muy familiar para mi personalmente, ya que muchas veces me gusta hacer codigos que puedan tener esa compatibiidad de solo modificar una variable y hacer el codigo capaz de adfaptarse a ello sin problema, ademas de que fue algo muy divertido de aprender y refrescante.
3. **Profundizacion en pytest:** Algo relacionado a OCP fue el uso de parametros especificos para `pytest` esto me ayudo a aprender algo muy interesante yy nuevo que me ayudo a hacer mas faciles las tareas de test.
4. **Aprendizaje de LSP:** Por ultimo este ultimo principio me dejo en claro que se debe tener en cuenta las clases padres e hijas, esto para hacer que nuestros codigos funcionen ya sea mandando una clase hija o alguna clase padre.

###  Notas de Verificación de Calidad
El código fue verificado localmente utilizando las herramientas del entorno de QA:
* **Mypy (`--strict`):** Validación de firmas exitosa. Cero tipos dinámicos implícitos (`Any`).
* **Ruff:** Ninguna correccion realizada por ```ruff check``` .
* **Pytest:** Dandonos una validacion exitosa sin ninguna obseervacion.

### Prompts utilizados
1. **Aprendizaje de cada principio:** Se solicitaron explicaciones de cada principio para poder comprenderlos de mejor forma, con ejemplos practicos ya en codigo.
2. **Solicitud de codigos de ejemplo:** Al ser temas desconocidos empece por ejemplos que fui desglozando con ayuida de la IA y posteriormente fui trabajando personalmente los codigos despues de comprender mejor las estructuras.


## [2026-07-18] — Entrada 5:  SOLID completo: I y D (3 h)

###  Lo que aprendí / Implementaciones
1. **Aprendizaje de ISP:** El principio ISP fue algo interesante porque es algo que siento que puede suceder mucho, a veces declaramos cosas o definimos acciones que haran algunas clases sin necesidad y hacer un codigo que no tengas que hacer esto necesariamente es muy conveniente.
2. **Aprendizaje de DIP:** El principio DIP al igual que el ISP fue algo muy interesante de aplicar porque hacer que estas partes importantes de nuestro sistema sean por asi decirlo "independientes" en lo personal creo que es algo muy conveniente porque en el caso de que algo suceda en alguno de los dos deje de funcionar no afectaria directamente al otro y ademas de que tambien aplica un poco de otros pincipios como el OCP.

###  Notas de Verificación de Calidad
El código fue verificado localmente utilizando las herramientas del entorno de QA:
* **Pytest:** Al inicio me ayudo a detectar problemas en las direcciones con los imports y algunos errores de sintaxis pero posteriormente nos dio una validacion exitosa sin ninguna obseervacion.

### Prompts utilizados
1. **Aprendizaje de cada principio:** Se solicitaron explicaciones de cada principio para poder comprenderlos de mejor forma, con ejemplos practicos ya en codigo.
2. **Solicitud de codigos de ejemplo:** Al ser temas desconocidos empece por ejemplos que fui desglozando con ayuida de la IA y posteriormente fui trabajando personalmente los codigos despues de comprender mejor las estructuras.
33. **Ayuda con errores de direcciones y test:** Al momento de hacer los test tuve errores con las direcciones de los archivos y mediante esto pude aprender porque sucedia ese error y aprendi una forma nueva de hacer los test para que pueda tener contexto de todas las carpetas del proyecto