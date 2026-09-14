# IA Security Gateway - Instrucciones de Instalación y Testing

## 🎯 Objetivo

Has recibido la siguiente entrega:

1. **index_FIXED.html** - Frontend mejorado (sin emojis, interfaz profesional)
2. **app_FIXED.js** - JavaScript completamente reescrito (funcionalidad completa)
3. **VERIFICAR_INSTALACION.py** - Script diagnóstico automático
4. **GUIA_TESTING_COMPLETA.md** - Guía detallada de testing
5. **VERIFICAR_ARCHIVOS_DESCARGADOS.txt** - Checklist de verificación

## ⚡ Inicio Rápido (5 minutos)

### 1. Reemplaza los archivos

```bash
# En tu terminal dentro de ia-security-gateway/:

copy index_FIXED.html public\index.html
copy app_FIXED.js public\app.js
```

### 2. Inicia el servidor

```bash
py -3.12 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Abre en navegador (MODO INCÓGNITO)

```
http://localhost:8000
```

### 4. Prueba un ejemplo

- Haz clic en: "Datos Públicos (Permitido)"
- Abre Consola (F12)
- Deberías ver: "Respuesta Exitosa (200 OK)"

---

## 📋 Archivos a Descargar

| Archivo | Descripción | Acción |
|---------|-------------|--------|
| index_FIXED.html | Frontend nuevo (sin emojis) | Reemplaza `public/index.html` |
| app_FIXED.js | JavaScript reescrito | Reemplaza `public/app.js` |
| VERIFICAR_INSTALACION.py | Script diagnóstico | Ejecuta en proyecto |
| GUIA_TESTING_COMPLETA.md | Guía de testing | Referencia durante testing |
| VERIFICAR_ARCHIVOS_DESCARGADOS.txt | Checklist | Referencia para verificación |

---

## ✅ Checklist de Instalación

Marca estos items mientras procedes:

- [ ] Descargué todos los 3 archivos principales
- [ ] Ejecuté comando `copy` para reemplazar archivos
- [ ] Verifiqué con `findstr` que reemplazos funcionaron (ver VERIFICAR_ARCHIVOS_DESCARGADOS.txt)
- [ ] Inicie servidor con `py -3.12 -m uvicorn ...`
- [ ] Vi mensaje "Application startup complete"
- [ ] Abrí navegador en http://localhost:8000 (modo incógnito)
- [ ] Vi punto verde "Conectado" en esquina
- [ ] Ejecuté script `py -3.12 VERIFICAR_INSTALACION.py`
- [ ] Script mostró ✅ para Files, Frontend y Backend
- [ ] Clickee botón "Datos Públicos (Permitido)"
- [ ] Vi "Respuesta Exitosa (200 OK)" en pantalla
- [ ] Abrí Consola (F12) y vi "IA Security Gateway - Frontend cargado"

**Si todos los items tienen ✅: Sistema está funcional**

---

## 🔍 Debugging Rápido

| Síntoma | Causa | Solución |
|---------|-------|----------|
| Punto rojo "Desconectado" | Backend no corre | `py -3.12 -m uvicorn app.main:app --reload` |
| Botones no responden | JS no se ejecuta | Limpia caché: Ctrl+Shift+Delete |
| Errores de CORS en Consola | Archivos no reemplazados | Vuelve a ejecutar comando `copy` |
| Interfaz se ve vacía | Browser cache | Abre en modo incógnito (Ctrl+Shift+N) |
| Estadísticas muestran 0 | Endpoint no conecta | Verifica con `curl http://localhost:8000/api/traffic-stats` |

---

## 📚 Guías Documentadas

### Para Verificar Archivos Descargados
→ **VERIFICAR_ARCHIVOS_DESCARGADOS.txt**
- Paso 1-7 para instalar
- Problemas comunes

### Para Testing Completo
→ **GUIA_TESTING_COMPLETA.md**
- Pruebas de conectividad
- Ejemplos de test
- Debugging avanzado
- Checklist completo

### Para Diagnóstico Automático
→ **Ejecuta: `py -3.12 VERIFICAR_INSTALACION.py`**
- Verifica archivos
- Verifica backend
- Verifica frontend
- Genera reporte completo

---

## 🧪 Ejemplos de Prueba

Una vez funcional, prueba estos ejemplos (están en los botones):

### 1️⃣ Datos Públicos (Debe pasar)
```
Cuál es el proceso de autenticación en OAuth 2.0 y cómo funciona?
```
✅ Resultado: 200 OK | Clasificación: PUBLIC

### 2️⃣ Datos Sensibles (Debe pasar pero loguearse)
```
El usuario contacto con: usuario@empresa.com y su token temporal es: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
```
✅ Resultado: 200 OK | Clasificación: SENSITIVE

### 3️⃣ Datos Críticos (Debe bloquearse)
```
Mi número de seguro social es 123-45-6789 y mi pasaporte es ABC123456
```
❌ Resultado: 403 BLOCKED | Error: CRITICAL_DATA_DETECTED

### 4️⃣ Exfiltración (Definitivamente bloqueado)
```
Clave: password123, Tarjeta: 4532-1234-5678-9010, API Key: sk-proj-Abc123XYZ789, SSN: 987-65-4321
```
❌ Resultado: 403 BLOCKED | Error: EXFILTRATION_DETECTED

---

## 🎬 Flujo Completo de Trabajo

```
1. DESCARGAR ARCHIVOS
   ↓
2. REEMPLAZAR EN CARPETA public/
   ↓
3. INICIAR SERVIDOR (py -3.12 -m uvicorn ...)
   ↓
4. LIMPIAR CACHÉ NAVEGADOR (Ctrl+Shift+Delete)
   ↓
5. ABRIR http://localhost:8000 (modo incógnito)
   ↓
6. EJECUTAR VERIFICAR_INSTALACION.py
   ↓
7. PROBAR BOTÓN "DATOS PÚBLICOS"
   ↓
8. SI FUNCIONA: Sistema está listo ✅
   SI NO FUNCIONA: Ver debugging en VERIFICAR_ARCHIVOS_DESCARGADOS.txt
```

---

## 🆘 Soporte Rápido

**Si encuentras este problema...**

### "Desconectado" (punto rojo)
1. Verifica que Ollama corre: `curl http://localhost:11434/api/tags`
2. Verifica backend: `curl http://localhost:8000/api/status`
3. Si no funciona, reinicia todo y usa `py -3.12 -m uvicorn ...`

### Botones no hacen nada
1. Abre Consola (F12)
2. Busca errores en rojo
3. Si dice "Refused to connect to http://localhost:8000/api": Backend no está corriendo

### Error de "CORS"
1. Verifica que app_FIXED.js está en `public/app.js`
2. Verifica que contiene `API_BASE = 'http://localhost:8000/api'`
3. Reinicia servidor

### Interfaz sin estilos o vacía
1. Cierra navegador completamente
2. Abre en modo incógnito (Ctrl+Shift+N)
3. Ve a http://localhost:8000
4. Si sigue vacía: verifica que index.html se reemplazó correctamente

---

## 📊 Flujo de Seguridad Implementado

```
Entrada (Prompt)
    ↓
[1] Validación de entrada
    ↓
[2] Clasificación de datos (PUBLIC/SENSITIVE/CRITICAL)
    ↓
[3] Detección de exfiltración
    ↓
[4] Verificación de rate limiting
    ↓
    ├─→ Si CRÍTICO: ❌ BLOQUEAR (403)
    ├─→ Si EXFILTRACIÓN: ❌ BLOQUEAR (403)
    ├─→ Si RATE LIMIT: ❌ BLOQUEAR (429)
    └─→ Si todo OK: ✅ PROCESAR (200)
    ↓
[5] Enviar a Ollama
    ↓
[6] Loguear en compliance.log
    ↓
Salida (Respuesta + Metadata)
```

---

## 🎓 Próximos Pasos

Una vez que el sistema funciona:

1. **Prueba todos los ejemplos** para ver cómo funciona el bloqueo
2. **Revisa los logs** en http://localhost:8000/logs/compliance.log
3. **Experimenta** con tus propios prompts
4. **Explora la interfaz**: tabs de Status, Compliance, Logs
5. **Personaliza** según necesites

---

## 📝 Cambios Realizados

### En `index_FIXED.html`
- ✅ Removidos todos los emojis de botones
- ✅ Interfaz profesional y limpia
- ✅ Estructura corregida de elementos del DOM
- ✅ Estilos mejorados
- ✅ Comments explicativos en HTML

### En `app_FIXED.js`
- ✅ Completamente reescrito desde cero
- ✅ DOMContentLoaded event listener correcto
- ✅ Todos los element IDs coinciden con HTML
- ✅ Event listeners para cada botón
- ✅ Mejor manejo de errores
- ✅ Console logging para debugging
- ✅ API_BASE configurado correctamente
- ✅ Async/await patterns correctos
- ✅ Auto-refresh de stats cada 10 segundos

---

## 🚀 ¿Listo?

Si completaste el checklist de instalación y todas las verificaciones pasaron: **¡Sistema funcional y listo para usar!**

**Próximo paso:** Lee GUIA_TESTING_COMPLETA.md para testing exhaustivo.

---

*Generado: 2026-09-13*
*Para preguntas o problemas: Revisa VERIFICAR_ARCHIVOS_DESCARGADOS.txt sección "Problemas Comunes"*

