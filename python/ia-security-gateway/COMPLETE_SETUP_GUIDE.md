# 🚀 IA Security Gateway - Guía Completa de Setup y Comandos

**Versión:** 2.0 Production Ready  
**Fecha:** Septiembre 2026  
**Estado:** ✅ Operativo 100%

---

## 📖 Tabla de Contenidos

1. [Setup Inicial](#setup-inicial)
2. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
3. [Comandos para Correr](#comandos-para-correr)
4. [Comandos de Testing](#comandos-de-testing)
5. [API Endpoints](#api-endpoints)
6. [Debugging](#debugging)
7. [Troubleshooting](#troubleshooting)
8. [Desarrollo](#desarrollo)

---

## 🔧 Setup Inicial

### Paso 1: Clonar el Repositorio

```bash
git clone <repo-url>
cd ia-security-gateway
```

### Paso 2: Crear Virtual Environment

**Windows (CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Si falta `requests`:**
```bash
pip install requests
```

### Paso 4: Verificar Instalación

```bash
python VERIFICAR_INSTALACION.py
```

Debe mostrar: `✅ All dependencies installed correctly`

---

## 🏗️ Arquitectura del Proyecto

```
ia-security-gateway/
├── app/
│   ├── api/
│   │   ├── routes.py              # AI Gateway endpoints (/api/ai/*)
│   │   └── security_routes.py     # Security endpoints (/api/security/*, /api/network/*)
│   ├── core/
│   │   └── config.py              # Configuración (OLLAMA_URL, OLLAMA_MODEL, etc)
│   ├── models/
│   │   └── schemas.py             # Modelos de datos
│   ├── services/
│   │   ├── ollama_service.py      # Conexión a Ollama LLM
│   │   ├── traffic_control.py     # Rate limiting
│   │   ├── compliance.py          # Logging de compliance
│   │   └── dlp_engine.py          # Motor de análisis DLP
│   ├── security/
│   │   ├── ip_control.py          # Whitelist/Blacklist de IPs
│   │   ├── file_analyzer.py       # Análisis de archivos
│   │   └── network_tracking.py    # Rastreo de dispositivos
│   └── main.py                    # Aplicación principal FastAPI
├── public/
│   ├── dashboard_completo.html    # Dashboard (interfaz)
│   └── dashboard.js               # Lógica del dashboard
├── data/
│   ├── whitelist.json             # IPs permitidas
│   ├── blacklist.json             # IPs bloqueadas
│   ├── devices.json               # Dispositivos rastreados
│   ├── violations.json            # Violaciones reportadas
│   └── analysis_log.json          # Histórico de análisis
├── logs/
│   └── gateway.log                # Logs de la aplicación
├── TEST_ALL_ENDPOINTS.py          # Script de testing automático
├── VERIFICAR_INSTALACION.py       # Verificador de dependencias
└── requirements.txt               # Dependencias Python
```

---

## ▶️ Comandos para Correr

### Terminal 1: Ollama Server (Local LLM)

**Prerequisito:** Descargar modelo Mistral (primera vez)
```bash
ollama pull mistral
```

**Iniciar Ollama:**
```bash
ollama serve
```

Debe mostrar:
```
INFO pulling manifest ...
INFO [cli] loaded images ...
```

**Verificar que Ollama está disponible:**
```bash
curl http://localhost:11434/api/tags
```

Debe retornar los modelos disponibles en JSON.

---

### Terminal 2: Backend FastAPI

**Prerequisito:** Activar venv en la Terminal 2

**Iniciar Backend:**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Debe mostrar:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Ver documentación API (Swagger):**
Abre en navegador:
```
http://localhost:8000/docs
```

---

### Terminal 3: Dashboard (opcional si no usas http.server)

Si necesitas servir el dashboard en puerto diferente:

```bash
cd public
python -m http.server 8001
```

Abre en navegador:
```
http://localhost:8001/dashboard_completo.html
```

---

### Resumen de Puertos

| Servicio | Puerto | URL |
|----------|--------|-----|
| Backend FastAPI | 8000 | http://localhost:8000 |
| Ollama | 11434 | http://localhost:11434 |
| Dashboard | 8001 | http://localhost:8001 |
| API Docs | 8000/docs | http://localhost:8000/docs |

---

## 🧪 Comandos de Testing

### Test Automático Completo

Verifica todos los 17+ endpoints:

```bash
python TEST_ALL_ENDPOINTS.py
```

**Salida esperada:**
```
✅ PASS System Status Check
✅ PASS Traffic Statistics
✅ PASS Compliance Report
✅ PASS IP Verification
... (más tests)

📊 Success Rate: 100%
✅ SUCCESS: All endpoints working!
```

---

### Test Manual con curl

#### 1. **Health Check**
```bash
curl http://localhost:8000/api/ai/status
```

#### 2. **Verificar IP**
```bash
curl "http://localhost:8000/api/security/ip/verify?ip=192.168.1.100"
```

#### 3. **Agregar IP a Whitelist**
```bash
curl -X POST "http://localhost:8000/api/security/ip/whitelist?ip=10.0.0.1&description=Mi%20PC"
```

#### 4. **Listar Dispositivos**
```bash
curl http://localhost:8000/api/network/devices
```

#### 5. **Generar Texto con Ollama**
```bash
curl -X POST "http://localhost:8000/api/ai/generate?prompt=Hola%20mundo"
```

#### 6. **Chat**
```bash
curl -X POST "http://localhost:8000/api/ai/chat?message=Como%20estas"
```

#### 7. **Obtener Violaciones**
```bash
curl http://localhost:8000/api/security/violations
```

---

### Test Ollama Directo

Verifica que Ollama está disponible:

```bash
curl http://127.0.0.1:11434/api/generate -X POST \
  -H "Content-Type: application/json" \
  -d '{"model":"mistral","prompt":"test","stream":false}'
```

---

## 📡 API Endpoints

### AI Gateway Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/ai/status` | Estado del sistema |
| GET | `/api/ai/traffic-stats` | Estadísticas de tráfico |
| GET | `/api/ai/compliance` | Reporte de compliance |
| POST | `/api/ai/generate` | Generar texto (Ollama) |
| POST | `/api/ai/chat` | Chat interactivo |

---

### Security IP Control Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/security/ip/rules` | Obtener whitelist/blacklist |
| GET | `/api/security/ip/verify` | Verificar si IP está permitida |
| POST | `/api/security/ip/whitelist` | Agregar a whitelist |
| POST | `/api/security/ip/blacklist` | Agregar a blacklist |
| DELETE | `/api/security/ip/rules/{ip}` | Eliminar regla de IP |

**Ejemplo - Verificar IP:**
```bash
curl "http://localhost:8000/api/security/ip/verify?ip=192.168.1.50"
```

**Ejemplo - Whitelist:**
```bash
curl -X POST "http://localhost:8000/api/security/ip/whitelist?ip=192.168.1.100&description=Office%20PC"
```

---

### File Analysis Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/security/file/analyze` | Analizar archivo |
| GET | `/api/security/file/analysis-summary` | Resumen de análisis |

**Ejemplo - Analizar archivo:**
```bash
curl -X POST "http://localhost:8000/api/security/file/analyze" \
  -F "file=@documento.txt" \
  -F "client_ip=192.168.1.1"
```

---

### Network Tracking Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/network/devices` | Listar dispositivos |
| GET | `/api/network/device-profile` | Perfil de dispositivo |
| POST | `/api/network/track-device` | Rastrear dispositivo |
| GET | `/api/network/summary` | Resumen de red |

**Ejemplo - Rastrear dispositivo:**
```bash
curl -X POST "http://localhost:8000/api/network/track-device?ip=192.168.1.50&hostname=OFFICE-PC"
```

---

### Violations Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/security/violations` | Obtener violaciones |
| POST | `/api/security/violations` | Reportar violación |

**Ejemplo - Reportar violación:**
```bash
curl -X POST "http://localhost:8000/api/security/violations?ip=203.0.113.50&type=UNAUTHORIZED_ACCESS&description=Acceso%20no%20autorizado"
```

---

## 🐛 Debugging

### Ver Logs en Tiempo Real

**En Linux/Mac:**
```bash
tail -f logs/gateway.log
```

**En Windows (PowerShell):**
```powershell
Get-Content logs/gateway.log -Tail 50 -Wait
```

**En Windows (CMD):**
```bash
type logs/gateway.log
```

---

### Verificar Puertos en Uso

**Windows (CMD):**
```bash
netstat -ano | findstr ":8000"
netstat -ano | findstr ":11434"
```

**Linux/Mac:**
```bash
lsof -i :8000
lsof -i :11434
```

---

### Inspeccionar Datos Almacenados

**Ver IPs en Whitelist:**
```bash
python -c "import json; print(json.dumps(json.load(open('data/whitelist.json')), indent=2))"
```

**Ver Dispositivos Rastreados:**
```bash
python -c "import json; print(json.dumps(json.load(open('data/devices.json')), indent=2))"
```

**Ver Violaciones:**
```bash
python -c "import json; print(json.dumps(json.load(open('data/violations.json')), indent=2))"
```

---

### Limpiar Datos (para Testing)

```bash
# Limpiar todo
python -c "
import json
for file in ['data/whitelist.json', 'data/blacklist.json', 'data/devices.json', 'data/violations.json', 'data/analysis_log.json']:
    with open(file, 'w') as f:
        json.dump({}, f)
print('✅ Datos limpiados')
"
```

---

### Debug Mode (más verbose)

En `app/core/config.py`, cambia:
```python
DEBUG: bool = False
```

A:
```python
DEBUG: bool = True
```

Luego reinicia el backend.

---

## ⚠️ Troubleshooting

### Error: "Cannot connect to backend"

**Solución:**
```bash
# Verifica que el backend esté corriendo
netstat -ano | findstr ":8000"

# Si no, inicia en Terminal 2:
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### Error: "Local LLM service temporarily unavailable"

**Solución:**
```bash
# 1. Verifica que Ollama esté corriendo
netstat -ano | findstr ":11434"

# 2. Si no, inicia Ollama en Terminal 1:
ollama serve

# 3. Verifica que el modelo mistral esté descargado:
ollama list

# Si no aparece, descárgalo:
ollama pull mistral
```

---

### Error: "Request timeout (>10s)"

**Causa:** Ollama tarda en procesar  
**Solución:**

En `app/core/config.py`:
```python
OLLAMA_TIMEOUT: int = 60  # Aumenta a 60 segundos
```

---

### Error: "ModuleNotFoundError"

**Solución:**
```bash
# Asegúrate que venv está activado
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Reinstala dependencias
pip install -r requirements.txt
```

---

### Dashboard muestra errores 404

**Causa:** Endpoints de backend no coinciden con esperado  
**Solución:**

1. Verifica que los archivos corregidos están en lugar:
   ```bash
   # Debe existir:
   # - app/api/routes.py (reemplazado)
   # - app/api/security_routes.py (reemplazado)
   ```

2. Reinicia el backend:
   ```bash
   # Ctrl+C en Terminal 2
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. Limpia cache del navegador:
   ```
   Ctrl+Shift+Delete (Windows)
   Cmd+Shift+Delete (Mac)
   ```

---

## 💻 Desarrollo

### Estructura de Desarrollo

**Para agregar nuevo endpoint:**

1. Abre `app/api/routes.py` o `app/api/security_routes.py`
2. Agrega tu función:
   ```python
   @router.get("/api/nuevo/endpoint")
   async def nuevo_endpoint():
       return {"mensaje": "Hola"}
   ```
3. El backend recarga automáticamente (--reload)
4. Prueba con:
   ```bash
   curl http://localhost:8000/api/nuevo/endpoint
   ```

---

### Agregar Nuevos Modelos Ollama

Si quieres usar un modelo diferente:

1. Descargalo:
   ```bash
   ollama pull neural-chat
   ```

2. Cambia en `app/core/config.py`:
   ```python
   OLLAMA_MODEL: str = "neural-chat"
   ```

3. Reinicia el backend

---

### Testing Local

Crea un script de testing personalizado:

```python
# test_custom.py
import requests

API_URL = "http://localhost:8000/api"

def test_custom():
    # Tu test aquí
    response = requests.get(f"{API_URL}/ai/status")
    assert response.status_code == 200
    print("✅ Test pasado")

if __name__ == "__main__":
    test_custom()
```

Ejecuta:
```bash
python test_custom.py
```

---

### Logs de Desarrollo

Ver logs en tiempo real mientras desarrollas:

**Terminal 4 (nueva):**
```bash
tail -f logs/gateway.log
```

Así ves errores mientras desarrollas.

---

## 📚 Referencias Rápidas

### Comandos Más Usados

```bash
# Iniciar todo
# Terminal 1:
ollama serve

# Terminal 2:
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3:
python TEST_ALL_ENDPOINTS.py
```

### URLs Útiles

- API Swagger: http://localhost:8000/docs
- Dashboard: http://localhost:8001/dashboard_completo.html
- Health Check: curl http://localhost:8000/api/ai/status

### Archivos Importantes

- Configuración: `app/core/config.py`
- API Routes: `app/api/routes.py` y `app/api/security_routes.py`
- Dashboard: `public/dashboard_completo.html`
- Testing: `TEST_ALL_ENDPOINTS.py`

---

## ✅ Checklist de Setup Completo

- [ ] Cloné el repositorio
- [ ] Creé venv
- [ ] Instalé dependencias
- [ ] Descargué modelo mistral (`ollama pull mistral`)
- [ ] Inicia Ollama en Terminal 1 (`ollama serve`)
- [ ] Inicia Backend en Terminal 2 (`python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`)
- [ ] Backend muestra "Application startup complete"
- [ ] Dashboard abre sin errores (http://localhost:8001/dashboard_completo.html)
- [ ] Ejecuté TEST_ALL_ENDPOINTS.py y pasó 100%

**Si todo está ✅: Sistema 100% operativo** 🎉

---

## 🆘 Soporte

Si algo no funciona:

1. Verifica que los 3 servidores estén corriendo (Ollama, Backend, Dashboard)
2. Revisa los logs: `logs/gateway.log`
3. Ejecuta: `python TEST_ALL_ENDPOINTS.py` para diagnóstico
4. Verifica puertos: `netstat -ano | findstr ":8000"` y `netstat -ano | findstr ":11434"`

---

**Versión:** 2.0 Production Ready  
**Última actualización:** Septiembre 2026  
**Estado:** ✅ Completamente operativo
