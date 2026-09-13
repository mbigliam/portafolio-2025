"""
Proveedor de Inteligencia Artificial: OpenAI (GPT-4o / GPT-4o-mini).
"""
import json
import logging
import urllib.request
from typing import List

from ai.provider import AIProvider, ChatMessage

logger = logging.getLogger("jarvis.ai.openai")


class OpenAIProvider(AIProvider):
    """Conector directo con la API de OpenAI."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        super().__init__(api_key=api_key, model=model)
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def generate_response(self, messages: List[ChatMessage], temperature: float = 0.7) -> str:
        if not self.api_key or self.api_key.strip() == "":
            raise ValueError("API Key de OpenAI no configurada.")

        formatted_msgs = [{"role": m.role, "content": m.content} for m in messages]

        payload = {
            "model": self.model,
            "messages": formatted_msgs,
            "temperature": temperature,
            "max_tokens": 350,
        }

        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.api_url,
            data=data_bytes,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=10.0) as response:
            result = json.loads(response.read().decode("utf-8"))
            choices = result.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "").strip()

        return "Fallo en la comunicación con OpenAI, señor."