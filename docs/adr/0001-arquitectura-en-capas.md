# ADR 0001: Arquitectura en capas para SensorHub

## Estado
Aceptado

## Contexto
Necesitamos cambiar de base de datos y testear la logica sin infraestructura.

## Decision
routers -> services -> repositories -> models, con el repositorio detras
de una abstraccion (Protocol) para aplicar DIP.

## Consecuencias
+ Tests de servicio sin base de datos (fake repository).
+ Cambiar SQLite por PostgreSQL no toca la logica de negocio.
- Mas archivos y algo mas de ceremonia para features pequenas.
