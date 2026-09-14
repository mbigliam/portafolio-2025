"""
Ollama Local LLM Service
Handles communication with local Ollama instance
"""
import httpx
import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class OllamaService:
    """Service for interacting with Ollama"""

    def __init__(self):
        self.base_url = settings.OLLAMA_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT

    async def health_check(self) -> bool:
        """Check if Ollama is running"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/tags",
                    timeout=5
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False

    async def generate_local(self, prompt: str) -> Optional[str]:
        """
        Generate response using local Ollama model
        All data stays local - NO external API calls
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=self.timeout
                )

                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"✅ Local generation successful (model: {self.model})")
                    return result.get("response", "")
                else:
                    logger.error(f"❌ Ollama error: {response.status_code}")
                    return None

        except Exception as e:
            logger.error(f"❌ Local generation failed: {e}")
            return None

    async def list_models(self) -> list:
        """List available models in local Ollama"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/tags",
                    timeout=10
                )

                if response.status_code == 200:
                    return response.json().get("models", [])
                return []

        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []

# Global instance
ollama_service = OllamaService()
