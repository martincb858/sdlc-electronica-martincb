import pytest

from app.domain.alert_states import (
    ACKNOWLEDGED,
    OPEN,
    RESOLVED,
    InvalidAlertTransitionError,
    validate_transition,
)


def test_open_to_acknowledged_is_allowed() -> None:
    validate_transition(OPEN, ACKNOWLEDGED)


def test_open_to_resolved_is_allowed_directly() -> None:
    validate_transition(OPEN, RESOLVED)


def test_acknowledged_to_resolved_is_allowed() -> None:
    validate_transition(ACKNOWLEDGED, RESOLVED)


def test_resolved_never_moves_backwards() -> None:
    with pytest.raises(InvalidAlertTransitionError):
        validate_transition(RESOLVED, OPEN)
    with pytest.raises(InvalidAlertTransitionError):
        validate_transition(RESOLVED, ACKNOWLEDGED)


def test_acknowledged_never_moves_back_to_open() -> None:
    with pytest.raises(InvalidAlertTransitionError):
        validate_transition(ACKNOWLEDGED, OPEN)


def test_unknown_target_state_is_rejected() -> None:
    with pytest.raises(ValueError, match="invalido"):
        validate_transition(OPEN, "closed")
