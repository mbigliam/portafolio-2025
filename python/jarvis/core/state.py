"""
Máquina de Estados Central para JARVIS.
Gestiona las fases operativas del asistente y notifica al bus de eventos.
"""
from enum import Enum, auto
from typing import Callable, List
import logging

logger = logging.getLogger("jarvis.state")


class SystemState(Enum):
    OFFLINE = auto()
    STARTING = auto()
    IDLE = auto()
    LISTENING = auto()
    THINKING = auto()
    SPEAKING = auto()
    EXECUTING = auto()
    ERROR = auto()

    @property
    def label(self) -> str:
        names = {
            SystemState.OFFLINE: "SISTEMA FUERA DE LÍNEA",
            SystemState.STARTING: "INICIALIZANDO SUBSISTEMAS",
            SystemState.IDLE: "SISTEMA EN ESPERA // OPERATIVO",
            SystemState.LISTENING: "ESCUDRIÑANDO AUDIO // ESCUCHANDO...",
            SystemState.THINKING: "PROCESANDO MODELO NEURONAL...",
            SystemState.SPEAKING: "TRANSMITIENDO RESPUESTA DE VOZ",
            SystemState.EXECUTING: "EJECUTANDO COMANDO EN WINDOWS",
            SystemState.ERROR: "ADVERTENCIA // CONDICIÓN ANÓMALA",
        }
        return names.get(self, self.name)


class StateMachine:
    """Controlador de transiciones de estado del asistente."""

    def __init__(self, initial_state: SystemState = SystemState.STARTING):
        self._current_state = initial_state
        self._previous_state = SystemState.OFFLINE
        self._listeners: List[Callable[[SystemState, SystemState], None]] = []
        logger.info(f"StateMachine instanciada en estado: {self._current_state.name}")

    @property
    def current_state(self) -> SystemState:
        return self._current_state

    @property
    def previous_state(self) -> SystemState:
        return self._previous_state

    def add_listener(self, callback: Callable[[SystemState, SystemState], None]) -> None:
        """Registra un observador que recibe (nuevo_estado, estado_anterior)."""
        self._listeners.append(callback)

    def transition_to(self, new_state: SystemState, reason: str = "") -> bool:
        """Efectúa la transición si es válida y notifica a los oyentes."""
        if self._current_state == new_state:
            return False

        self._previous_state = self._current_state
        self._current_state = new_state
        logger.info(f"Transición de Estado: {self._previous_state.name} -> {new_state.name} | Motivo: {reason}")

        for listener in self._listeners:
            try:
                listener(self._current_state, self._previous_state)
            except Exception as e:
                logger.error(f"Error al notificar listener de estado: {e}", exc_info=True)

        return True