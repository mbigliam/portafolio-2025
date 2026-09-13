"""
Motor de Síntesis de Voz (TTS) para JARVIS.
Utiliza Edge-TTS y el reproductor nativo multimedia de Windows (sin pygame).
"""
import asyncio
import ctypes
import logging
import os
import tempfile
import threading
from typing import Callable, Optional
import edge_tts

logger = logging.getLogger("jarvis.tts")


class TextToSpeech:
    """Sintetizador de voz con reproducción asíncrona nativa de Windows."""

    def __init__(self, voice_name: str = "es-ES-AlvaroNeural"):
        self.voice_name = voice_name
        self._is_speaking = False
        self._lock = threading.Lock()

    @property
    def is_speaking(self) -> bool:
        return self._is_speaking

    def speak(self, text: str, on_start: Optional[Callable[[], None]] = None, on_finish: Optional[Callable[[], None]] = None) -> None:
        """Sintetiza y reproduce el audio en un hilo secundario."""
        if not text.strip():
            return

        thread = threading.Thread(
            target=self._speak_worker,
            args=(text, on_start, on_finish),
            daemon=True,
        )
        thread.start()

    def _speak_worker(self, text: str, on_start: Optional[Callable[[], None]], on_finish: Optional[Callable[[], None]]):
        with self._lock:
            self._is_speaking = True
            if on_start:
                try:
                    on_start()
                except Exception as e:
                    logger.error(f"Error en callback on_start: {e}")

            self._speak_edge_tts_native(text)

            self._is_speaking = False
            if on_finish:
                try:
                    on_finish()
                except Exception as e:
                    logger.error(f"Error en callback on_finish: {e}")

    def _speak_edge_tts_native(self, text: str) -> bool:
        """Genera MP3 con Edge-TTS y lo reproduce usando la API nativa MCI de Windows."""
        temp_file = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                temp_file = f.name

            async def _generate():
                communicate = edge_tts.Communicate(text, self.voice_name)
                await communicate.save(temp_file)

            asyncio.run(_generate())

            # Reproducción nativa en Windows con winmm.dll
            winmm = ctypes.windll.winmm
            alias = "jarvis_tts_sound"
            winmm.mciSendStringW(f'open "{temp_file}" type mpegvideo alias {alias}', None, 0, None)
            winmm.mciSendStringW(f"play {alias} wait", None, 0, None)
            winmm.mciSendStringW(f"close {alias}", None, 0, None)
            return True

        except Exception as e:
            logger.error(f"Error al sintetizar audio con Edge-TTS: {e}")
            return False

        finally:
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass