"""
Detector de Wake Word con Pausa Estricta y Prevención de Bucles.
"""
import logging
import threading
import time
from typing import Callable, List
from voice.speech_to_text import SpeechToText

logger = logging.getLogger("jarvis.wake_word")


class WakeWordDetector:
    """Escucha en segundo plano con control de concurrencia."""

    def __init__(self, stt_engine: SpeechToText, keywords: List[str] | None = None):
        self.stt = stt_engine
        self.keywords = [k.lower() for k in (keywords or ["jarvis", "oye jarvis", "hola jarvis", "hey jarvis"])]
        self._running = False
        self._paused = False
        self._thread: threading.Thread | None = None
        self._on_detected_callback: Callable[[], None] | None = None

    def start(self, on_detected: Callable[[], None]) -> None:
        if self._running:
            return
        self._on_detected_callback = on_detected
        self._running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()
        logger.info("Detector Wake Word iniciado.")

    def pause(self) -> None:
        self._paused = True

    def resume(self) -> None:
        self._paused = False

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)

    def _listen_loop(self) -> None:
        time.sleep(1.0)  # Espera inicial para estabilizar dispositivos de audio
        while self._running:
            if self._paused:
                time.sleep(0.3)
                continue

            try:
                # Escucha bloques cortos de 2.2 segundos
                text = self.stt.listen_phrase(record_seconds=2.2)
                if text and not self._paused:
                    cleaned = text.lower()
                    for kw in self.keywords:
                        if kw in cleaned:
                            logger.info(f"Palabra clave detectada: '{kw}'")
                            self.pause()
                            if self._on_detected_callback:
                                self._on_detected_callback()
                            break
            except Exception:
                time.sleep(0.4)
            time.sleep(0.1)