# semana1/test_fsm.py
from fsm_demo import TrafficLightFSM, TrafficLightState

def test_initial_state():
    """1. Test de estado inicial: la FSM debe arrancar en RED."""
    fsm = TrafficLightFSM()
    assert fsm.state == TrafficLightState.RED
    assert fsm._cycle_count == 0

def test_transition_red_to_green():
    """2. Test de transición RED -> GREEN."""
    fsm = TrafficLightFSM()
    next_state = fsm.transition()
    assert next_state == TrafficLightState.GREEN
    assert fsm.state == TrafficLightState.GREEN

def test_full_cycle_returns_to_red():
    """3. Test de ciclo completo: RED -> GREEN -> YELLOW -> RED."""
    fsm = TrafficLightFSM()
    
    fsm.transition()  # RED -> GREEN
    fsm.transition()  # GREEN -> YELLOW
    final_state = fsm.transition()  # YELLOW -> RED
    
    assert final_state == TrafficLightState.RED
    assert fsm.state == TrafficLightState.RED

def test_cycle_counting():
    """4. Test de conteo de ciclos: incrementa al completar la vuelta a RED."""
    fsm = TrafficLightFSM()
    
    # Ciclo 1
    fsm.transition()  # GREEN
    fsm.transition()  # YELLOW
    fsm.transition()  # RED (Ciclo 1 completo)
    assert fsm._cycle_count == 3
    
    # Ciclo 2
    fsm.transition()  # GREEN
    fsm.transition()  # YELLOW
    fsm.transition()  # RED (Ciclo 2 completo)
    assert fsm._cycle_count == 6