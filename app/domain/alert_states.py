OPEN = "open"
ACKNOWLEDGED = "acknowledged"
RESOLVED = "resolved"

VALID_STATES = {OPEN, ACKNOWLEDGED, RESOLVED}

_ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    OPEN: {ACKNOWLEDGED, RESOLVED},
    ACKNOWLEDGED: {RESOLVED},
    RESOLVED: set(),
}


class InvalidAlertTransitionError(Exception):
    """Se lanza al intentar una transicion de estado no permitida."""


def validate_transition(current: str, new: str) -> None:
    """Valida la maquina de estados de una alerta: open -> acknowledged ->
    resolved, o open -> resolved directo. Nunca se retrocede."""
    if new not in VALID_STATES:
        raise ValueError(f"Estado de alerta invalido: '{new}'.")

    if new not in _ALLOWED_TRANSITIONS.get(current, set()):
        raise InvalidAlertTransitionError(
            f"Transicion invalida de '{current}' a '{new}'."
        )
