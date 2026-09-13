"""
Proveedor de Inteligencia Artificial: Google Gemini con Diagnóstico Detallado y Cabeceras Universales.
"""
import json
import logging
import urllib.error
import urllib.request
from typing import List

from ai.provider import AIProvider, ChatMessage

logger = logging.getLogger("jarvis.ai.gemini")


class GeminiProvider(AIProvider):
    """Conector avanzado con la API de Google Gemini."""

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        # Limpieza de espacios y comillas accidentales
        cleaned_key = api_key.strip().strip("'").strip('"')
        cleaned_model = model.strip()

        # Si se especificó gemini-2.5 (que aún no existe en el endpoint público v1beta), mapear a gemini-1.5-flash o gemini-2.0-flash
        if "2.5" in cleaned_model:
            logger.info(f"Modelo '{cleaned_model}' normalizado a 'gemini-1.5-flash' para compatibilidad con el endpoint oficial.")
            cleaned_model = "gemini-1.5-flash"

        super().__init__(api_key=cleaned_key, model=cleaned_model)

    def generate_response(self, messages: List[ChatMessage], temperature: float = 0.7) -> str:
        if not self.api_key:
            raise ValueError("API Key de Gemini vacía.")

        # Construir contenido
        system_instruction = None
        contents = []

        for msg in messages:
            if msg.role == "system":
                system_instruction = {"parts": [{"text": msg.content}]}
            elif msg.role == "user":
                contents.append({"role": "user", "parts": [{"text": msg.content}]})
            elif msg.role == "assistant":
                contents.append({"role": "model", "parts": [{"text": msg.content}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 300,
            },
        }

        if system_instruction:
            payload["systemInstruction"] = system_instruction

        data_bytes = json.dumps(payload).encode("utf-8")

        # Intentar conectar con la API oficial v1beta
        # URL limpia (sin la clave en la query string para evitar duplicidades)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

        # ÚNICO método de autenticación necesario (funciona tanto para AIza como para AQ.)
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key,
        }

        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")

  

        try:
            with urllib.request.urlopen(req, timeout=12.0) as response:
                result = json.loads(response.read().decode("utf-8"))
                candidates = result.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()

            return "Respuesta vacía del núcleo de Gemini, señor."

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="ignore")
            logger.error(f"Error HTTP {e.code} de Google Gemini: {error_body}")
            try:
                err_json = json.loads(error_body)
                err_msg = err_json.get("error", {}).get("message", error_body)
                return f"Aviso de Gemini ({e.code}): {err_msg}"
            except Exception:
                return f"Aviso de Gemini: Error {e.code}. Verifique que el modelo sea 'gemini-1.5-flash'."

        except Exception as e:
            logger.error(f"Fallo de conexión con Gemini: {e}")
            return f"Error de conexión con el servicio neuronal: {e}"