"""
Motor de Reconocimiento de Voz (STT) Robusto con Calibración Dinámica de Ruido.
"""
import io
import logging
import time
import wave
from typing import Optional
import numpy as np
import speech_recognition as sr

try:
    import sounddevice as sd
    SD_AVAILABLE = True
except ImportError:
    sd = None
    SD_AVAILABLE = False

logger = logging.getLogger("jarvis.stt")


class SpeechToText:
    """Captura de micrófono calibrada y transcripción de voz."""

    def __init__(self, language: str = "es-ES", sample_rate: int = 16000):
        self.language = language
        self.sample_rate = sample_rate
        self.recognizer = sr.Recognizer()
        self.noise_floor = 200.0

    def calibrate(self, duration: float = 1.0) -> None:
        """Mide el nivel de ruido ambiental de la habitación para calibrar el umbral."""
        if not SD_AVAILABLE:
            return

        try:
            frames = int(duration * self.sample_rate)
            sample = sd.rec(frames, samplerate=self.sample_rate, channels=1, dtype="int16")
            sd.wait()
            self.noise_floor = float(np.mean(np.abs(sample)))
            logger.info(f"Micrófono calibrado. Nivel de ruido base: {self.noise_floor:.1f}")
        except Exception as e:
            logger.warning(f"Aviso en calibración de micrófono: {e}")

    def listen_phrase(self, record_seconds: float = 3.5) -> Optional[str]:
        """Graba audio durante un intervalo optimizado y lo transcribe."""
        if not SD_AVAILABLE:
            logger.warning("sounddevice no está disponible.")
            return None

        try:
            num_frames = int(record_seconds * self.sample_rate)
            recording = sd.rec(num_frames, samplerate=self.sample_rate, channels=1, dtype="int16")
            sd.wait()

            # Verificar si realmente hubo voz por encima del ruido base
            mean_energy = float(np.mean(np.abs(recording)))
            if mean_energy < (self.noise_floor * 1.1 + 30):
                # Solo silencio/ruido de fondo
                return None

            # Convertir el buffer a WAV en memoria
            wav_io = io.BytesIO()
            with wave.open(wav_io, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.sample_rate)
                wf.writeframes(recording.tobytes())

            wav_io.seek(0)

            with sr.AudioFile(wav_io) as source:
                audio_data = self.recognizer.record(source)

            text = self.recognizer.recognize_google(audio_data, language=self.language)
            logger.info(f"Transcripción detectada: '{text}'")
            return text.strip()

        except sr.UnknownValueError:
            return None
        except Exception as e:
            logger.debug(f"Aviso de captura: {e}")
            return None