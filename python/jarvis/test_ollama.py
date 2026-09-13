"""
Script de Diagnóstico Rápido de la conexión con Ollama.
"""
from app.config import AppConfig
from ai.provider import ChatMessage
from ai.ollama_provider import OllamaProvider

config = AppConfig.load()
ai_cfg = config.raw_data.get("ai", {})

# Tomamos los valores del YAML, con valores por defecto seguros
model = ai_cfg.get("model", "qwen2.5:7b")
base_url = ai_cfg.get("base_url", "http://localhost:11434")

print("=" * 60)
print("PROBANDO CONEXIÓN CON OLLAMA (LOCAL)...")
print(f"Modelo configurado: {model}")
print(f"URL del servicio:   {base_url}")
print("=" * 60)

# Ahora SÍ acepta api_key y base_url sin lanzar TypeError
provider = OllamaProvider(api_key="", model=model, base_url=base_url)

messages = [
    ChatMessage(role="system", content="Eres JARVIS, un asistente de IA local eficiente y conciso."),
    ChatMessage(role="user", content="Hola JARVIS, responde en una frase confirmando que estás en línea y funcionando en local."),
]

respuesta = provider.generate_response(messages, temperature=0.7, max_tokens=350)
print("\nRESPUESTA RECIBIDA DE OLLAMA:")
print(f"> {respuesta}")
print("=" * 60)