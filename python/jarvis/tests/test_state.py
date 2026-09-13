import pytest
from core.state import StateMachine, SystemState


def test_initial_state():
    sm = StateMachine(initial_state=SystemState.STARTING)
    assert sm.current_state == SystemState.STARTING
    assert sm.previous_state == SystemState.OFFLINE


def test_valid_transition():
    sm = StateMachine(initial_state=SystemState.IDLE)
    result = sm.transition_to(SystemState.LISTENING, reason="Wake word detectada")

    assert result is True
    assert sm.current_state == SystemState.LISTENING
    assert sm.previous_state == SystemState.IDLE


def test_redundant_transition_ignored():
    sm = StateMachine(initial_state=SystemState.IDLE)
    result = sm.transition_to(SystemState.IDLE)

    assert result is False
    assert sm.current_state == SystemState.IDLE


def test_state_listener_callback():
    sm = StateMachine(initial_state=SystemState.IDLE)
    notifications = []

    def on_change(new_state, prev_state):
        notifications.append((new_state, prev_state))

    sm.add_listener(on_change)
    sm.transition_to(SystemState.THINKING)

    assert len(notifications) == 1
    assert notifications[0] == (SystemState.THINKING, SystemState.IDLE)