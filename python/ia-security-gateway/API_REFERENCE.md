# 📚 API REFERENCE - Complete Endpoints

## Base URL
```
http://localhost:8000/api
```

---

## 🤖 AI Gateway Endpoints

### 1. Get System Status
```
GET /api/ai/status
```
**Respuesta:**
```json
{
  "status": "online",
  "version": "1.0.0",
  "models_available": ["gpt-4", "gpt-3.5"],
  "uptime_seconds": 3600
}
```
**Dashboard:** Status card en Dashboard

---

### 2. Get Traffic Statistics
```
GET /api/ai/traffic-stats
```
**Respuesta:**
```json
{
  "total_requests": 1250,
  "allowed_requests": 1200,
  "blocked_requests": 50,
  "block_rate": 4.0
}
```
**Dashboard:** Traffic stats card

---

### 3. Get Compliance Report
```
GET /api/ai/compliance
```
**Respuesta:**
```json
{
  "status": "COMPLIANT",
  "violations": 5,
  "last_check": "2026-09-13T10:30:00",
  "policies": ["GDPR", "CCPA"],
  "score": 92.5
}
```
**Dashboard:** Compliance card

---

### 4. Generate Text
```
POST /api/ai/generate
Content-Type: application/json

{
  "prompt": "Write a security report"
}
```
**Respuesta:**
```json
{
  "generated_text": "Security Report...",
  "tokens_used": 150,
  "model": "gpt-4"
}
```
**Dashboard:** AI Gateway → Generate Text

---

### 5. Chat with AI
```
POST /api/ai/chat
Content-Type: application/json

{
  "message": "What is DLP?"
}
```
**Respuesta:**
```json
{
  "response": "DLP stands for Data Loss Prevention...",
  "model": "gpt-4",
  "timestamp": "2026-09-13T10:31:00"
}
```
**Dashboard:** AI Gateway → Chat

---

## 🔐 Security - IP Control

### 6. Verify IP Access
```
GET /api/security/ip/verify?ip=192.168.1.100
```
**Parámetros:**
- `ip` (string): IP a verificar

**Respuesta:**
```json
{
  "ip": "192.168.1.100",
  "allowed": true,
  "rule_type": "whitelist",
  "description": "Office Desktop",
  "risk_level": "LOW",
  "timestamp": "2026-09-13T10:32:00"
}
```
**Dashboard:** IPs → Verificar IP

---

### 7. Get IP Rules
```
GET /api/security/ip/rules
```
**Respuesta:**
```json
{
  "whitelist": {
    "192.168.1.100": "Office Desktop",
    "192.168.1.101": "Office Laptop"
  },
  "blacklist": {
    "10.0.0.50": "Suspicious Activity",
    "10.0.0.51": "Malware Detected"
  }
}
```
**Dashboard:** IPs → Ver Reglas

---

### 8. Add IP to Whitelist
```
POST /api/security/ip/whitelist
Content-Type: application/json

{
  "ip": "192.168.1.102",
  "description": "New Office Machine"
}
```
**Respuesta:**
```json
{
  "success": true,
  "message": "IP added to whitelist",
  "ip": "192.168.1.102"
}
```
**Dashboard:** IPs → Gestionar IPs → Whitelist

---

### 9. Add IP to Blacklist
```
POST /api/security/ip/blacklist
Content-Type: application/json

{
  "ip": "10.0.0.100",
  "reason": "Unauthorized Access Attempt"
}
```
**Respuesta:**
```json
{
  "success": true,
  "message": "IP added to blacklist",
  "ip": "10.0.0.100"
}
```
**Dashboard:** IPs → Gestionar IPs → Blacklist

---

## 📄 File Analysis

### 10. Analyze File
```
POST /api/security/file/analyze
Content-Type: multipart/form-data

file: (binary file)
client_ip: 192.168.1.100
```

**Respuesta:**
```json
{
  "filename": "document.pdf",
  "risk_level": "MEDIUM",
  "patterns_found": ["email_patterns", "credit_card_patterns"],
  "sensitive_content": {
    "emails": ["user@example.com"],
    "credit_cards": 2
  },
  "timestamp": "2026-09-13T10:33:00"
}
```
**Dashboard:** Archivos → Analizar Archivo

---

### 11. Get Analysis Summary
```
GET /api/security/file/analysis-summary
```
**Respuesta:**
```json
{
  "total_analyzed": 150,
  "safe": 130,
  "at_risk": 20,
  "top_patterns": {
    "credit_card_patterns": 45,
    "email_patterns": 38,
    "ssn_patterns": 12
  }
}
```
**Dashboard:** Archivos → Resumen de Análisis

---

## 🌐 Network Tracking

### 12. Get All Devices
```
GET /api/network/devices
```
**Respuesta:**
```json
{
  "devices": [
    {
      "ip": "192.168.1.100",
      "hostname": "DESKTOP-USER",
      "risk_level": "LOW",
      "last_activity": "2026-09-13T10:30:00"
    },
    {
      "ip": "192.168.1.101",
      "hostname": "LAPTOP-USER",
      "risk_level": "MEDIUM",
      "last_activity": "2026-09-13T10:25:00"
    }
  ]
}
```
**Dashboard:** Red → Todos los Dispositivos

---

### 13. Get Network Summary
```
GET /api/network/summary
```
**Respuesta:**
```json
{
  "connected_devices": 10,
  "whitelist_ips": 8,
  "blacklist_ips": 3,
  "average_risk": "LOW",
  "total_traffic": 50000
}
```
**Dashboard:** Red → Resumen de Red

---

### 14. Get Device Profile
```
GET /api/network/device-profile?ip=192.168.1.100
```
**Parámetros:**
- `ip` (string): IP del dispositivo

**Respuesta:**
```json
{
  "ip": "192.168.1.100",
  "hostname": "DESKTOP-USER",
  "user_agent": "Mozilla/5.0...",
  "ai_model": "gpt-4",
  "risk_level": "LOW",
  "total_requests": 500,
  "blocked_requests": 5,
  "first_seen": "2026-09-01T08:00:00",
  "last_activity": "2026-09-13T10:30:00"
}
```
**Dashboard:** Red → Perfil de Dispositivo

---

### 15. Track New Device
```
POST /api/network/track-device
Content-Type: application/json

{
  "ip": "192.168.1.110",
  "hostname": "NEW-DEVICE",
  "user_agent": "Mozilla/5.0...",
  "ai_model": "gpt-4"
}
```
**Respuesta:**
```json
{
  "success": true,
  "message": "Device tracked successfully",
  "ip": "192.168.1.110",
  "device_id": "dev_123abc"
}
```
**Dashboard:** Red → Rastrear

---

## ⚠️ Violations

### 16. Get Violations
```
GET /api/security/violations
```
**Respuesta:**
```json
{
  "violations": [
    {
      "id": "viol_001",
      "ip": "10.0.0.50",
      "type": "SUSPICIOUS_ACTIVITY",
      "description": "Multiple failed login attempts",
      "timestamp": "2026-09-13T10:00:00",
      "severity": "HIGH"
    },
    {
      "id": "viol_002",
      "ip": "192.168.1.50",
      "type": "DATA_TRANSFER",
      "description": "Large data transfer detected",
      "timestamp": "2026-09-13T09:00:00",
      "severity": "MEDIUM"
    }
  ]
}
```
**Dashboard:** Violaciones → Ver Violaciones

---

### 17. Report Violation
```
POST /api/security/violations
Content-Type: application/json

{
  "ip": "192.168.1.50",
  "type": "SUSPICIOUS_ACTIVITY",
  "description": "Unusual access pattern detected"
}
```
**Respuesta:**
```json
{
  "success": true,
  "message": "Violation reported successfully",
  "violation_id": "viol_003"
}
```
**Dashboard:** Violaciones → Reportar

---

## 🔄 Request/Response Patterns

### Success Response (2xx)
```json
{
  "success": true,
  "data": {...},
  "timestamp": "2026-09-13T10:30:00"
}
```

### Error Response (4xx/5xx)
```json
{
  "success": false,
  "error": "Invalid IP format",
  "code": "INVALID_INPUT",
  "timestamp": "2026-09-13T10:30:00"
}
```

---

## 🧪 CURL Examples

### Test System Status
```bash
curl -X GET "http://localhost:8000/api/ai/status"
```

### Verify IP
```bash
curl -X GET "http://localhost:8000/api/security/ip/verify?ip=192.168.1.100"
```

### Add to Whitelist
```bash
curl -X POST "http://localhost:8000/api/security/ip/whitelist" \
  -H "Content-Type: application/json" \
  -d '{"ip":"192.168.1.102","description":"New Device"}'
```

### Analyze File
```bash
curl -X POST "http://localhost:8000/api/security/file/analyze" \
  -F "file=@/path/to/file.pdf" \
  -F "client_ip=192.168.1.100"
```

### Chat with AI
```bash
curl -X POST "http://localhost:8000/api/ai/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"What is DLP?"}'
```

---

## 📊 HTTP Status Codes

| Code | Significado | Acción |
|------|-------------|--------|
| 200 | OK | Éxito |
| 201 | Created | Recurso creado |
| 400 | Bad Request | Dato inválido |
| 401 | Unauthorized | Autenticación requerida |
| 403 | Forbidden | Acceso denegado |
| 404 | Not Found | Recurso no existe |
| 500 | Server Error | Error interno |

---

## 🔑 Headers Requeridos

Todos los requests POST/PUT deben incluir:
```
Content-Type: application/json
```

Para file uploads:
```
Content-Type: multipart/form-data
```

---

## ⏱️ Timeouts

- Read timeout: 30 segundos
- Connection timeout: 10 segundos
- Total request timeout: 60 segundos

---

## 🚀 Rate Limiting

- Default: 100 requests/minuto por IP
- Premium: 1000 requests/minuto
- Batch: 10000 requests/hora

---

## 📝 Notas Importantes

1. **Autenticación**: Por ahora no requiere token (localhost)
2. **CORS**: Habilitado para localhost:*
3. **Datos**: Se persisten en JSON local
4. **Caché**: Respuestas se cachean 30 segundos
5. **Logs**: Todos los requests se logean en backend

---

**Última actualización**: Septiembre 2026
**API Version**: 1.0.0
**Dashboard Version**: 2.0
