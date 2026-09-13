"""
Script de Diagnóstico Rápido de la API Key de Gemini (Usando SDK Oficial).
"""
from app.config import AppConfig
from google import genai

# 1. Cargar configuración
config = AppConfig.load()
ai_cfg = config.raw_data.get("ai", {})
api_key = ai_cfg.get("api_key", "")
model = ai_cfg.get("model", "gemini-2.0-flash")

print("=" * 60)
print("PROBANDO CONEXIÓN CON GOOGLE GEMINI (SDK OFICIAL)...")
print(f"Modelo configurado: {model}")
print(f"API Key detectada:  {api_key[:10]}... (Total: {len(api_key)} caracteres)")
print("=" * 60)

try:
    # 2. Inicializar el cliente oficial (esto maneja la autenticación AQ. correctamente)
    client = genai.Client(api_key=api_key)
    
    # 3. Enviar la petición
    response = client.models.generate_content(
        model=model,
        contents="Hola JARVIS, responde en una frase confirmando que estás en línea."
    )
    
    print("\n✅ RESPUESTA RECIBIDA DE GEMINI:")
    print(f"> {response.text}")
    print("=" * 60)
    
except Exception as e:
    print("\n❌ ERROR DE CONEXIÓN:")
    print(f"> {e}")
    print("=" * 60)