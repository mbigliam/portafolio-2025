"""
Capa Abstracta de Proveedor de Inteligencia Artificial (AIProvider).
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ChatMessage:
    role: str  # "system" | "user" | "assistant"
    content: str


class AIProvider(ABC):
    """Interfaz base para cualquier motor de IA (Gemini, OpenAI, Ollama, Claude, etc.)."""

    def __init__(self, api_key: Optional[str] = None, model: str = "default"):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    def generate_response(self, messages: List[ChatMessage], temperature: float = 0.7) -> str:
        """Genera una respuesta basada en el historial de mensajes."""
        pass