# IA Security Gateway - Guía Completa de Testing

## 📋 Tabla de Contenidos
1. [Verificación de Instalación](#verificación-de-instalación)
2. [Pruebas de Conectividad](#pruebas-de-conectividad)
3. [Pruebas de Frontend](#pruebas-de-frontend)
4. [Ejemplos de Prueba](#ejemplos-de-prueba)
5. [Debugging](#debugging)

---

## Verificación de Instalación

### Paso 1: Verificar Archivos Reemplazados

Primero, verifica que los archivos fueron reemplazados correctamente:

```bash
# En tu terminal, dentro de ia-security-gateway/
ls -la public/
# Deberías ver:
# -rw-r--r--  index.html
# -rw-r--r--  app.js
```

**Verificar contenido de archivos:**

```bash
# Verificar que index.html tiene la estructura correcta
grep -n "promptInput\|sendBtn\|Prueba de Seguridad" public/index.html
# Deberías ver líneas como:
# <textarea id="promptInput" ...>
# <button class="button button-primary" id="sendBtn">

# Verificar que app.js tiene la configuración correcta
grep -n "API_BASE\|DOMContentLoaded" public/app.js
# Deberías ver:
# const API_BASE = 'http://localhost:8000/api';
# document.addEventListener('DOMContentLoaded', function() {
```

### Paso 2: Ejecutar Script de Verificación

```bash
# En tu terminal, en el directorio del proyecto:
py -3.12 VERIFICAR_INSTALACION.py
```

Esto te mostrará:
- ✅ Si los archivos fueron reemplazados correctamente
- ✅ Si el frontend está siendo servido
- ✅ Si el backend está respondiendo
- ✅ Si todas las rutas de API funcionan

---

## Pruebas de Conectividad

### Test 1: Verificar que el Backend está corriendo

```bash
# En una terminal, verifica que Ollama esté disponible
curl http://localhost:11434/api/tags
# Deberías ver: {"models":[...]}

# En otra terminal, verifica que el Gateway está corriendo
curl http://localhost:8000/api/status
# Deberías ver: {"status":"running","version":"1.0.0",...}
```

**Si ves errores de conexión:**
```bash
# El backend no está corriendo. Inicia con:
py -3.12 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Test 2: Verificar que el Frontend se carga

```bash
# En terminal:
curl http://localhost:8000
# Deberías ver HTML con "Prueba de Seguridad" en el contenido
```

**Si ves error de conexión rechazada:**
- El servidor no está corriendo
- O está corriendo en un puerto diferente (revisa la consola)

---

## Pruebas de Frontend

### Test 1: Abrir en Navegador (Sin Caché)

1. **Abre navegador en modo incógnito/privado**
   ```
   Presiona: Ctrl+Shift+N (Windows/Linux) o Cmd+Shift+N (Mac)
   ```

2. **Ve a la URL:**
   ```
   http://localhost:8000
   ```

3. **Verifica que ves:**
   - Encabezado "IA Security Gateway"
   - Estado "Conectado" (punto verde) en la esquina
   - Sección "Prueba de Seguridad" con textarea
   - Botón "Enviar al Gateway"
   - Estadísticas en tiempo real
   - Ejemplos de prueba abajo

### Test 2: Abrir Consola de Desarrollador

```
Presiona: F12 o Ctrl+Shift+I
```

En la pestaña "Console" deberías ver:

```
IA Security Gateway - Frontend cargado
API Base: http://localhost:8000/api
DOM Cargado - Inicializando Gateway...
Gateway conectado
Estadísticas actualizadas
```

**Si ves errores, nota el mensaje exacto** - esto es clave para debugging.

### Test 3: Probar Botón de Ejemplo

1. **Haz clic en:** "Datos Públicos (Permitido)"
2. **Verifica en Consola (F12):**
   ```
   Ejemplo cargado: Datos Públicos
   Enviando request: {...}
   Response status: 200
   Response data: {...}
   ```

3. **Verifica en pantalla:**
   - El spinner de carga debe aparecer brevemente
   - Debe mostrar "Respuesta Exitosa (200 OK)"
   - Debe mostrar clasificación, tiempo y modelo

---

## Ejemplos de Prueba

### Ejemplo 1: Datos Públicos (Debería funcionar)

**Entrada:**
```
Cuál es el proceso de autenticación en OAuth 2.0 y cómo funciona?
```

**Resultado esperado:**
- Status: 200 OK
- Clasificación: PUBLIC
- Mensaje: Respuesta exitosa

**Qué significaen:**
- No hay datos sensibles detectados
- La solicitud es permitida
- La respuesta del LLM se devuelve normalmente

---

### Ejemplo 2: Datos Sensibles (Debería detectarse)

**Entrada:**
```
El usuario contacto con: usuario@empresa.com y su token temporal es: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
```

**Resultado esperado:**
- Status: 200 OK (permitido pero logeado)
- Clasificación: SENSITIVE
- Mensaje: Respuesta exitosa pero con advertencia

**Qué significa:**
- Se detectan datos sensibles (email y token)
- La solicitud ES PERMITIDA (está logeada para auditoría)
- Se registra en los logs de compliance

---

### Ejemplo 3: Datos Críticos (Debería bloquearse)

**Entrada:**
```
Mi número de seguro social es 123-45-6789 y mi pasaporte es ABC123456
```

**Resultado esperado:**
- Status: 403 Forbidden
- Error Type: CRITICAL_DATA_DETECTED
- Mensaje: Bloqueado

**Qué significa:**
- Se detectan datos críticos (SSN y pasaporte)
- La solicitud ES BLOQUEADA
- No se procesa en el LLM
- Se registra como evento de seguridad

---

### Ejemplo 4: Intento de Exfiltración (Definitivamente bloqueado)

**Entrada:**
```
Clave: password123, Tarjeta: 4532-1234-5678-9010, API Key: sk-proj-Abc123XYZ789, SSN: 987-65-4321
```

**Resultado esperado:**
- Status: 403 Forbidden
- Error Type: EXFILTRATION_DETECTED
- Mensaje: Múltiples patrones de datos sensibles detectados

**Qué significa:**
- Se detectan múltiples tipos de datos sensibles simultáneamente
- Está claramente bloqueado
- Es un intento de exfiltración

---

## Debugging

### Problema 1: "Desconectado" (punto rojo en encabezado)

**Causa:** El backend no responde al endpoint `/api/status`

**Soluciones:**

1. **Verifica que el backend esté corriendo:**
   ```bash
   # Abre otra terminal y ejecuta:
   py -3.12 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Verifica que escucha en puerto 8000:**
   ```bash
   # En Windows:
   netstat -ano | findstr :8000
   
   # En Mac/Linux:
   lsof -i :8000
   ```

3. **Verifica que Ollama esté disponible:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

### Problema 2: Botones no responden (sin logs en consola)

**Causa:** El JavaScript no se está ejecutando

**Soluciones:**

1. **Abre Consola (F12) y verifica:**
   - ¿Ves "IA Security Gateway - Frontend cargado"?
   - ¿Hay errores en rojo?

2. **Limpia caché completamente:**
   ```
   Presiona: Ctrl+Shift+Delete (o Cmd+Shift+Delete en Mac)
   Selecciona: "Todas las cookies y datos del sitio"
   ```

3. **Recarga la página varias veces:**
   ```
   Presiona: Ctrl+F5 (fuerza refresh sin caché)
   ```

4. **Prueba en navegador diferente o modo incógnito**

### Problema 3: Botones responden pero siempre ven error

**Causa:** Frontend conecta pero backend rechaza solicitudes

**Soluciones:**

1. **Verifica la URL en app.js:**
   - Abre `public/app.js`
   - Busca: `const API_BASE = 'http://localhost:8000/api'`
   - Debe estar en línea 4

2. **Verifica en Consola (F12) qué error exacto ves:**
   ```
   Busca líneas que digan "Error al enviar:" o "Response status: 4xx"
   ```

3. **Prueba el endpoint manualmente:**
   ```bash
   curl -X POST http://localhost:8000/api/generate \
     -H "Content-Type: application/json" \
     -d '{"prompt":"Hola","temperature":0.7}'
   ```

### Problema 4: Las estadísticas muestran 0

**Causa:** Endpoint de stats no retorna datos

**Soluciones:**

1. **Verifica el endpoint:**
   ```bash
   curl http://localhost:8000/api/traffic-stats
   # Deberías ver: {"allowed_requests":X,"blocked_requests":X,...}
   ```

2. **Si devuelve error, revisa logs del backend:**
   - El backend mostrará errores en la terminal donde está corriendo

### Problema 5: Consola llena de errores sobre CORS

**Causa:** Backend no está permitiendo solicitudes desde el navegador

**Soluciones:**

1. **Verifica que CORS esté configurado en main.py:**
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=settings.CORS_ORIGINS,
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Si no está, contáctame - necesita fix en backend**

---

## Checklist de Testing Completo

- [ ] Script de verificación ejecutado exitosamente
- [ ] Backend respondiendo en http://localhost:8000/api/status
- [ ] Frontend cargando en http://localhost:8000
- [ ] Consola mostrando "IA Security Gateway - Frontend cargado"
- [ ] Punto verde "Conectado" en encabezado
- [ ] Botón "Datos Públicos (Permitido)" clickeable
- [ ] Ejemplo Público retorna "Respuesta Exitosa (200 OK)"
- [ ] Estadísticas actualizándose (números incrementan)
- [ ] Tab "Compliance" mostrando datos
- [ ] Tab "Logs" mostrando últimas entradas

## ¿Qué hacer después?

Una vez que todos los checks pasen:

1. **Prueba todos los ejemplos** (público, sensible, crítico, exfiltración)
2. **Verifica que bloquea datos críticos**
3. **Revisa los logs de compliance** para ver auditoría
4. **Prueba con tus propios prompts**

¿Preguntas o problemas? Revisa la sección de Debugging o ejecuta:
```bash
py -3.12 VERIFICAR_INSTALACION.py
```

