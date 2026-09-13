"""
Proveedor de Inteligencia Artificial: Ollama (Modelos Locales 100% Offline).
Usa la librería oficial de Ollama para una conexión robusta, limpia y con manejo de errores.
"""
import logging
from typing import List

try:
    import ollama
    from ollama import ResponseError
except ImportError:
    raise ImportError("Falta la librería oficial. Ejecuta: pip install ollama")

from ai.provider import AIProvider, ChatMessage

logger = logging.getLogger("jarvis.ai.ollama")


class OllamaProvider(AIProvider):
    """Conector local con Ollama usando la librería oficial."""

    def __init__(self, api_key: str = "", host: str = "http://localhost:11434", model: str = "qwen2.5:7b", base_url: str = None):
        # Aceptamos api_key y base_url por compatibilidad con el loader de configuración de JARVIS,
        # aunque Ollama no los usa realmente.
        actual_host = base_url if base_url else host
        
        # Inicializamos la clase padre sin API key
        super().__init__(api_key="", model=model)
        
        # Configuramos el cliente oficial apuntando al host local
        self.client = ollama.Client(host=actual_host)

    def generate_response(self, messages: List[ChatMessage], temperature: float = 0.7, max_tokens: int = 350) -> str:
        # Formatear mensajes al formato que espera la librería oficial
        formatted_msgs = [{"role": m.role, "content": m.content} for m in messages]

        try:
            # Llamada limpia usando la librería oficial
            response = self.client.chat(
                model=self.model,
                messages=formatted_msgs,
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens  # Respeta el límite de tu config
                }
            )
            return response.message.content.strip()

        except ResponseError as e:
            logger.error(f"Error de respuesta de Ollama: {e}")
            if "not found" in str(e).lower():
                return f"Señor, el modelo '{self.model}' no está descargado. Por favor, ejecuta 'ollama pull {self.model}' en la terminal."
            return f"Error en el núcleo local: {e}"
            
        except ConnectionError:
            logger.error("No se puede conectar con el servicio de Ollama.")
            return "Señor, no puedo conectar con el servicio de Ollama. Verifica que la aplicación esté en ejecución en segundo plano."
            
        except Exception as e:
            logger.error(f"Fallo inesperado con Ollama: {e}")
            return f"Error inesperado en el subsistema de IA local: {e}"