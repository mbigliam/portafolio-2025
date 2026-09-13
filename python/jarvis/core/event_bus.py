"""
Bus de Eventos Asíncrono y Desacoplado (Pub/Sub).
Permite la comunicación entre la UI, el Core y los futuros motores de Voz e IA.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Dict, List
import logging

logger = logging.getLogger("jarvis.event_bus")


class EventType(Enum):
    STATE_CHANGED = auto()
    SYSTEM_TELEMETRY = auto()
    LOG_MESSAGE = auto()
    USER_INPUT = auto()
    ACTION_STARTED = auto()
    ACTION_FINISHED = auto()
    ERROR_OCCURRED = auto()


@dataclass
class Event:
    event_type: EventType
    data: Any = None
    timestamp: datetime = field(default_factory=datetime.now)


class EventBus:
    """Bus central para emitir y suscribirse a eventos del sistema."""

    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable[[Event], None]]] = {
            event_type: [] for event_type in EventType
        }

    def subscribe(self, event_type: EventType, handler: Callable[[Event], None]) -> None:
        """Suscribe un handler a un tipo de evento específico."""
        self._subscribers[event_type].append(handler)

    def emit(self, event_type: EventType, data: Any = None) -> None:
        """Emite un evento a todos los suscriptores registrados."""
        event = Event(event_type=event_type, data=data)
        for handler in self._subscribers.get(event_type, []):
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error en handler de evento {event_type.name}: {e}", exc_info=True)


# Instancia global del bus de eventos
global_event_bus = EventBus()