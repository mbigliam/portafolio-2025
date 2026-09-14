# app/services/dlp_engine.py
import re
import httpx
import json
from typing import Tuple, List, Dict
from app.core.config import settings

# --- CAPA 1: REGEX (Bloqueo inmediato y determinista) ---
PATRONES_CRITICOS = {
    "TARJETA_CREDITO": r"\b(?:\d[ -]*?){13,16}\b",
    "API_KEY_OPENAI": r"sk-[a-zA-Z0-9]{20,}",
    "API_KEY_AWS": r"AKIA[0-9A-Z]{16}",
    "SSN_USA": r"\b\d{3}-\d{2}-\d{4}\b",
    "PASSWORD_FIELD": r"(?i)(password|contraseña|passwd)[\s:=]+['\"]?([^\s'\"]+)['\"]?",
    "PRIVATE_KEY": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
    "EMAIL_MASIVO": r"[\w\.-]+@[\w\.-]+\.\w+" # Si hay más de 5 emails, es sospechoso
}

# --- CAPA 2: IA LOCAL (Auditor semántico) ---
async def auditar_con_ia_local(texto: str) -> Tuple[bool, str]:
    """
    Usa Ollama para leer el texto y decidir si es peligroso.
    """
    prompt_auditor = f"""
    Eres un auditor de seguridad DLP (Data Loss Prevention) para una empresa.
    Tu trabajo es leer el siguiente texto y determinar si contiene información CONFIDENCIAL que NO debería ser compartida con una IA externa.
    
    Busca específicamente:
    - Secretos comerciales o propiedad intelectual.
    - Datos de clientes (nombres, direcciones, teléfonos).
    - Información financiera interna (balances, proyecciones).
    - Código fuente propietario.
    - Credenciales o tokens de acceso.
    
    Responde ÚNICAMENTE con un JSON válido:
    {{"peligroso": true/false, "razon": "explicación breve", "categoria": "PII|FINANCIERO|CODIGO|SECRETO|NINGUNO"}}
    
    Texto a analizar:
    ---
    {texto[:1500]} 
    ---
    """
    
    payload = {
        "model": settings.OLLAMA_MODEL, # Asegúrate de tener esto en config
        "prompt": prompt_auditor,
        "stream": False,
        "format": "json"
    }
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Usamos el endpoint de Ollama directamente
            response = await client.post(f"{settings.OLLAMA_BASE_URL}/api/generate", json=payload)
            response.raise_for_status()
            resultado = response.json()
            
            analisis = json.loads(resultado.get("response", "{}"))
            
            if analisis.get("peligroso", False):
                return True, f"IA Local detectó: {analisis.get('razon')} (Cat: {analisis.get('categoria')})"
            return False, "Análisis IA Local: Limpio"
            
    except Exception as e:
        # Si el auditor falla, bloqueamos por precaución (Fail-Safe)
        return True, f"Error en auditoría IA: {str(e)}. Bloqueado por seguridad."

# --- FUNCIÓN PRINCIPAL ---
async def analizar_payload(texto: str) -> Dict:
    """
    Orquesta el análisis en dos capas y devuelve un veredicto.
    """
    alertas = []
    
    # 1. Análisis Regex (Rápido y letal)
    for nombre, patron in PATRONES_CRITICOS.items():
        coincidencias = re.findall(patron, texto)
        if coincidencias:
            # Si encontramos algo crítico, bloqueamos de inmediato
            alertas.append(f"Patrón crítico detectado: {nombre}")
            return {
                "bloqueado": True,
                "razon": f"Coincidencia exacta con patrón {nombre}",
                "alertas": alertas,
                "capa": "REGEX"
            }
    
    # 2. Análisis IA Local (Solo si la Capa 1 está limpia)
    es_peligroso_ia, razon_ia = await auditar_con_ia_local(texto)
    
    if es_peligroso_ia:
        return {
            "bloqueado": True,
            "razon": razon_ia,
            "alertas": ["Análisis semántico de IA Local"],
            "capa": "IA_LOCAL"
        }
    
    return {
        "bloqueado": False,
        "razon": "Payload seguro",
        "alertas": [],
        "capa": "NINGUNA"
    }