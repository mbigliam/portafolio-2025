# ⚡ QUICK START - IA Security Gateway Dashboard

## 3 PASOS PARA EMPEZAR

### 1️⃣ ASEGURAR QUE BACKEND ESTÁ ACTIVO
```bash
# Terminal - Backend debe estar corriendo
python main.py
# Debe escuchar en: http://localhost:8000/api
# Verificar: curl http://localhost:8000/api/ai/status
```

### 2️⃣ SERVIR ARCHIVOS FRONTEND
```bash
# Terminal - En la carpeta del proyecto
python -m http.server 8001
# O usa cualquier servidor web
```

### 3️⃣ ABRIR DASHBOARD
```
Navega a: http://localhost:8001/dashboard_completo.html
```

---

## 📁 ESTRUCTURA REQUERIDA
```
ia-security-gateway/
├── dashboard_completo.html        ← Abrir este archivo
├── public/
│   └── dashboard.js               ← Lógica del dashboard
└── (backend FastAPI)
```

---

## 🎯 PRUEBAS RÁPIDAS

Cuando abras el dashboard, prueba estos elementos:

### ✅ Test 1: Dashboard (debe cargar stats)
1. Sidebar → Click en "📊 Dashboard"
2. Click en "🔄 Actualizar Dashboard"
3. Debe mostrar estado, tráfico y compliance

### ✅ Test 2: Análisis de IPs
1. Sidebar → "🔍 Análisis de IPs"
2. Tab "Verificar IP"
3. Ingresa: `192.168.1.100`
4. Click "Verificar"
5. Debe mostrar si es permitida/bloqueada

### ✅ Test 3: Archivo
1. Sidebar → "📄 Análisis Archivos"
2. Selecciona cualquier archivo (.txt, .pdf, .doc, etc)
3. Click "📄 Analizar"
4. Debe mostrar nivel de riesgo

### ✅ Test 4: Dispositivos
1. Sidebar → "🌐 Rastreo de Red"
2. Tab "Todos los Dispositivos"
3. Click "Cargar Dispositivos"
4. Debe listar dispositivos conectados

### ✅ Test 5: Chat AI
1. Sidebar → "🤖 AI Gateway"
2. Tab "Chat"
3. Escribe mensaje: "Hola"
4. Click "💬 Enviar"
5. Debe recibir respuesta

---

## 🔴 SI NO FUNCIONA

### Error: "Failed to fetch" o "No connection"
```
❌ Backend no está corriendo
✅ Solución: Ejecutar: python main.py
```

### Error: "No se pudo cargar..."
```
❌ Endpoint falla en backend
✅ Solución: Verificar que endpoint existe en Swagger
            Revisar consola del navegador (F12 → Network)
```

### Error: CORS issue
```
❌ Backend no permite requests desde frontend
✅ Solución: En main.py agregar CORS middleware
```

---

## 🚀 FUNCIONES PRINCIPALES

| Función | Acceso | Qué hace |
|---------|--------|----------|
| Verificar IP | IPs → Tab 1 | Chequea si IP es permitida |
| Ver Reglas | IPs → Tab 2 | Lista whitelist/blacklist |
| Agregar Whitelist | IPs → Tab 3 | Permitir nueva IP |
| Analizar Archivo | Archivos | Detecta datos sensibles en archivo |
| Ver Dispositivos | Red → Tab 1 | Lista todos los dispositivos |
| Rastrear Dispositivo | Red → Tab 4 | Registra nuevo dispositivo |
| Ver Violaciones | Violaciones → Tab 1 | Muestra violaciones de seguridad |
| Reportar Violación | Violaciones → Tab 2 | Crea nuevo reporte |
| Chat AI | AI → Tab 2 | Conversa con IA del gateway |

---

## 📊 ENTENDER LOS COLORES

- 🟢 **Verde**: Seguro / Permitido / Bajo riesgo
- 🟠 **Naranja**: Advertencia / Riesgo medio
- 🔴 **Rojo**: Peligro / Bloqueado / Alto riesgo
- 🔵 **Azul**: Información / Acción principal

---

## 🎨 MODO NOCTURNO (Ya incluido)

El dashboard viene en dark theme profesional. Para cambiar a light theme, editar en dashboard_completo.html:

```css
/* Cambiar colores de fondo */
body { background: #ffffff; } /* de #0f0f0f */
.card { background: #f5f5f5; } /* de #1a1a2e */
```

---

## 📱 ACCESO MÓVIL

El dashboard es completamente responsive:
- Desktop (>768px): Sidebar ancho
- Móvil (<768px): Sidebar colapsado

Simplemente abre en tu teléfono:
```
http://localhost:8001/dashboard_completo.html
```

---

## 🔒 SEGURIDAD

El dashboard **NO almacena** credenciales o datos sensibles:
- Todo se comunica directamente con backend
- Usa HTTP (en localhost) - para producción usar HTTPS
- Las sesiones se manejan por headers de request

---

## 📝 NOTA IMPORTANTE

Este dashboard está **100% conectado al backend real**:
- ✅ Sin mock data
- ✅ Sin simulaciones
- ✅ Todos los análisis son REALES
- ✅ Todo lo que veas viene del servidor

Si no ves datos, es porque:
1. Backend no está corriendo
2. Endpoint falla
3. No hay datos en la BD

---

## 🎯 PRÓXIMOS PASOS

1. ✅ Backend + Frontend corriendo
2. ✅ Dashboard accesible
3. ✅ Realizar pruebas de cada sección
4. ✅ Integrar en tu portafolio
5. ✅ Mostrar a clientes/empleadores

---

**¿Listo?** Abre http://localhost:8001/dashboard_completo.html y prueba! 🚀
