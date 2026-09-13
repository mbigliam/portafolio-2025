"""
Orquestador Central de Voz con Cerebro de Inteligencia Artificial Conectado.
"""
import logging
import threading
import time
from typing import Optional
from PySide6.QtCore import QCoreApplication

from ai.router import AIRouter
from core.conversation import ConversationManager
from core.event_bus import EventType, global_event_bus
from core.state import StateMachine, SystemState
from voice.speech_to_text import SpeechToText
from voice.text_to_speech import TextToSpeech
from voice.wake_word import WakeWordDetector

logger = logging.getLogger("jarvis.voice_engine")


class VoiceEngine:
    """Coordina micrófono, cerebro de IA, síntesis de voz y estados."""

    def __init__(self, state_machine: StateMachine, ai_router: AIRouter, language: str = "es-ES"):
        self.state_machine = state_machine
        self.ai_router = ai_router
        self.conversation = ConversationManager(user_name="Mauricio")
        self.tts = TextToSpeech(voice_name="es-ES-AlvaroNeural")
        self.stt = SpeechToText(language=language)
        self.wake_detector = WakeWordDetector(self.stt, keywords=["jarvis", "oye jarvis", "hola jarvis", "hey jarvis"])
        self._lock = threading.Lock()

    def start(self) -> None:
        threading.Thread(target=self._initialize_background, daemon=True).start()

    def _initialize_background(self) -> None:
        self.stt.calibrate(duration=0.5)
        self.wake_detector.start(on_detected=self.on_wake_word_triggered)
        global_event_bus.emit(EventType.LOG_MESSAGE, "VoiceEngine: Cerebro de IA y escucha activa enlazados.")

    def on_wake_word_triggered(self) -> None:
        threading.Thread(target=self._interaction_flow, daemon=True).start()

    def trigger_push_to_talk(self) -> None:
        threading.Thread(target=self._interaction_flow, daemon=True).start()

    def _interaction_flow(self) -> None:
        if not self._lock.acquire(blocking=False):
            return

        self.wake_detector.pause()

        try:
            # 1. Estado LISTENING
            self.state_machine.transition_to(SystemState.LISTENING, reason="Capturando orden")
            global_event_bus.emit(EventType.LOG_MESSAGE, "JARVIS: Escuchando su orden...")

            # 2. Captura de audio del usuario
            user_text = self.stt.listen_phrase(record_seconds=3.5)

            # 3. Estado THINKING
            self.state_machine.transition_to(SystemState.THINKING, reason="Consultando Cerebro de IA")

            if user_text:
                global_event_bus.emit(EventType.LOG_MESSAGE, f"Usuario: '{user_text}'")
                t = user_text.lower()

                # Comando de salida por voz
                if any(k in t for k in ["salir", "apágate", "apagate", "cerrar", "apagar", "adiós", "adios"]):
                    farewell = "Apagando sistemas centrales, señor. Hasta pronto."
                    global_event_bus.emit(EventType.LOG_MESSAGE, f"JARVIS: '{farewell}'")
                    self.tts.speak(
                        text=farewell,
                        on_start=lambda: self.state_machine.transition_to(SystemState.SPEAKING),
                        on_finish=lambda: self._exit_app(),
                    )
                    return

                # CONSULTA AL CEREBRO DE IA
                messages = self.conversation.get_messages(user_text)
                response_text = self.ai_router.query(messages)

                # Guardar en memoria de conversación
                self.conversation.add_interaction(user_text, response_text)
            else:
                response_text = "Sí, señor. ¿En qué puedo ayudarle?"

            # 4. Estado SPEAKING y Reproducción de Voz
            global_event_bus.emit(EventType.LOG_MESSAGE, f"JARVIS: '{response_text}'")

            self.tts.speak(
                text=response_text,
                on_start=lambda: self.state_machine.transition_to(SystemState.SPEAKING),
                on_finish=lambda: self.state_machine.transition_to(SystemState.IDLE),
            )

            while self.tts.is_speaking:
                time.sleep(0.1)

        except Exception as e:
            logger.error(f"Error en interacción con IA: {e}")
            self.state_machine.transition_to(SystemState.IDLE)

        finally:
            time.sleep(0.4)
            self.wake_detector.resume()
            self._lock.release()

    def _exit_app(self):
        time.sleep(0.5)
        QCoreApplication.quit()