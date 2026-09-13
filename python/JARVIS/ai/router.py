"""
Enrutador de Inteligencia Artificial (AIRouter).
Selecciona el proveedor configurado e implementa respuestas de contingencia.
"""
import logging
from typing import List, Optional

from ai.gemini_provider import GeminiProvider
from ai.ollama_provider import OllamaProvider
from ai.openai_provider import OpenAIProvider
from ai.provider import AIProvider, ChatMessage
from app.config import AppConfig

logger = logging.getLogger("jarvis.ai.router")


class AIRouter:
    """Fábrica y administrador central de proveedores de IA."""

    def __init__(self, config: AppConfig):
        self.config = config
        self.provider: Optional[AIProvider] = None
        self._init_provider()

    def _init_provider(self) -> None:
        ai_cfg = self.config.raw_data.get("ai", {})
        provider_name = ai_cfg.get("provider", "gemini").lower()
        model_name = ai_cfg.get("model", "gemini-1.5-flash")
        api_key = ai_cfg.get("api_key", "").strip()

        logger.info(f"Inicializando proveedor de IA: {provider_name.upper()} (Modelo: {model_name})")

        try:
            if provider_name == "gemini":
                if api_key:
                    self.provider = GeminiProvider(api_key=api_key, model=model_name)
                else:
                    logger.warning("API Key de Gemini vacía. Configure su clave en config/default_config.yaml")

            elif provider_name == "openai":
                if api_key:
                    self.provider = OpenAIProvider(api_key=api_key, model=model_name)
                else:
                    logger.warning("API Key de OpenAI vacía en config.")

            elif provider_name == "ollama":
                host = ai_cfg.get("host", "http://localhost:11434")
                self.provider = OllamaProvider(host=host, model=model_name)

        except Exception as e:
            logger.error(f"Error al instanciar proveedor {provider_name}: {e}")
            self.provider = None

    def query(self, messages: List[ChatMessage]) -> str:
        """Consulta al modelo configurado o usa el motor cognitivo local de respaldo."""
        if self.provider:
            try:
                return self.provider.generate_response(messages)
            except Exception as e:
                logger.error(f"Fallo en llamada al modelo: {e}")

        # Motor de respaldo inteligente si no hay API Key configurada
        last_user_msg = messages[-1].content if messages else ""
        return self._local_fallback(last_user_msg)

    def _local_fallback(self, user_text: str) -> str:
        t = user_text.lower()
        if "gato" in t or "elagu" in t or "mila" in t:
            return "El Elagu y La Mila están registrados bajo supervisión constante, señor. Le avisaré si detecto anomalías felinas cerca de su estación de trabajo."
        elif "quién eres" in t or "quien eres" in t:
            return "Soy JARVIS, su sistema de inteligencia artificial personal. Mis redes neuronales están enlazadas a su equipo."
        elif "cómo estás" in t or "como estas" in t:
            return "Operando a plena capacidad, señor. Listo para asistirle en lo que requiera."
        else:
            return f"He procesado su solicitud: '{user_text}'. Para desbloquear razonamiento generativo ilimitado, configure su API Key de Gemini o OpenAI en default_config.yaml, señor."