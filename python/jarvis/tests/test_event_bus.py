import pytest
from core.event_bus import EventBus, EventType


def test_event_subscription_and_emission():
    bus = EventBus()
    received_events = []

    def handler(event):
        received_events.append(event)

    bus.subscribe(EventType.USER_INPUT, handler)
    bus.emit(EventType.USER_INPUT, data={"text": "JARVIS abre Spotify"})

    assert len(received_events) == 1
    assert received_events[0].event_type == EventType.USER_INPUT
    assert received_events[0].data["text"] == "JARVIS abre Spotify"