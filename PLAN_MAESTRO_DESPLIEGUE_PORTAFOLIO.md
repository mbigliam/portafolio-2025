# 🚀 PLAN MAESTRO - Despliegue Portafolio Completo
**Usuario:** @mbigliam  
**Repositorio:** https://github.com/mbigliam  
**Objetivo:** Desplegar 8 proyectos en Render.com + Demo en GitHub

---

## 📊 DIAGNÓSTICO POR PROYECTO

### 🐍 PROYECTOS PYTHON (3)

#### 1️⃣ **JARVIS** - Asistente IA con Ollama/Gemini
**Estado:** ✅ LISTO (parcialmente)
```
- ✅ Tiene requirements.txt
- ✅ Tiene run.py (punto de entrada)
- 📁 Estructura: ai/, app/, config/, core/, voice/, ui/
- ⚠️ FALTA: Procfile, .gitignore, requirements.txt en formato completo
```
**Tipo de Despliegue:** Python app (Flask/FastAPI)
**Prioridad:** ALTA - Requiere pocas modificaciones

**Cambios necesarios:**
- [ ] Verificar si es Flask/FastAPI
- [ ] Crear requirements.txt completo
- [ ] Crear Procfile
- [ ] Crear .gitignore
- [ ] Inicializar git

---

#### 2️⃣ **SISMO-PREDICT B-AUTO** - Predicción de Sismos
**Estado:** ⚠️ PARCIALMENTE LISTO
```
- ✅ Tiene api.py (aplicación principal)
- ✅ Tiene index.html (frontend)
- ✅ Tiene sismo_predict_b_auto.py
- 📊 Datos: CSV, JSON de cache
- ⚠️ FALTA: requirements.txt, Procfile, .gitignore
```
**Tipo de Despliegue:** Python Flask/FastAPI + HTML frontend
**Prioridad:** ALTA - Similar a JARVIS

**Cambios necesarios:**
- [ ] Extraer requirements.txt
- [ ] Crear Procfile
- [ ] Crear .gitignore
- [ ] Verificar rutas de archivos estáticos
- [ ] Inicializar git

---

#### 3️⃣ **UNIR_PDF** - Utilidad de PDFs
**Estado:** ❌ NO DESPLEGABLE EN RENDER
```
- 📄 Unir_pdfs_1.2.py (utilidad de escritorio)
- 📁 build/, dist/ (indica compilación como .exe)
- ⚠️ NO es aplicación web
- ⚠️ Posiblemente usa GUI (tkinter, PyQt, etc)
```
**Tipo:** Aplicación de escritorio
**Prioridad:** BAJA - Incluir en repo pero no desplegar en Render
**Alternativa:** Crear wrapper web si es necesario

---

### ☕ PROYECTOS JAVA (2)

#### 4️⃣ **SmartTask-Web** (Ya hecho)
**Estado:** ✅ COMPLETAMENTE LISTO
```
- ✅ pom.xml configurado
- ✅ Spring Boot 3.2.5
- ✅ Procfile creado
- ✅ .gitignore creado
- ✅ README.md
- ✅ RENDER_DEPLOYMENT.md
```
**Despliegue:** https://smarttask-web.onrender.com/smarttask/
**Prioridad:** ✅ COMPLETADO

---

#### 5️⃣ **BibliotecaUNTEC** - Sistema de Biblioteca
**Estado:** ⚠️ CÓDIGO COMPILADO DISPONIBLE
```
- ✅ BibliotecaUNTEC.war (WAR compilado)
- ✅ BibliotecaUNTEC.zip (código fuente)
- ✅ README.MD
- 🎬 Video de demostración (20MB)
- ⚠️ FALTA: pom.xml, .gitignore, Procfile
```
**Tipo de Despliegue:** Java Spring Boot (WAR)
**Prioridad:** ALTA - Similar a SmartTask

**Cambios necesarios:**
- [ ] Extraer fuentes del ZIP
- [ ] Verificar pom.xml
- [ ] Crear Procfile
- [ ] Crear .gitignore
- [ ] Crear README.md
- [ ] Inicializar git

---

### 🌐 PROYECTOS HTML-CSS-JS (3)

#### 6️⃣ **wallet2** - Aplicación de Billetera
**Estado:** ✅ LISTO
```
- 📄 login.html, menu.html, deposit.html, sendmoney.html, transactions.html
- 📁 Assets/ (CSS, JS, imágenes)
- ✅ Sitio estático
- ⚠️ FALTA: .gitignore, README.md, index.html
```
**Tipo de Despliegue:** HTML estático (Render Static Site)
**Prioridad:** MEDIA

**Cambios necesarios:**
- [ ] Crear/editar index.html como página principal
- [ ] Crear .gitignore
- [ ] Crear README.md
- [ ] Crear build.sh (opcional)

---

#### 7️⃣ **Meet-Coffe-Main** - Sitio Web
**Estado:** ✅ LISTO
```
- 📄 index.html
- 📁 Assets/
- 📖 README.md
- ✅ Sitio estático
```
**Tipo de Despliegue:** HTML estático (Render Static Site)
**Prioridad:** MEDIA

**Cambios necesarios:**
- [ ] Crear .gitignore
- [ ] Verificar paths relativos de assets

---

#### 8️⃣ **Viajes-Chile-Main** - Sitio Web Turismo
**Estado:** ✅ LISTO
```
- 📄 index.html (22KB)
- 📁 assets/
- 📖 README.md
- ✅ Sitio estático
```
**Tipo de Despliegue:** HTML estático (Render Static Site)
**Prioridad:** MEDIA

**Cambios necesarios:**
- [ ] Crear .gitignore
- [ ] Verificar paths relativos de assets

---

## 📋 ESTRATEGIA DE DESPLIEGUE

### **OPCIÓN A: UN REPOSITORIO MAESTRO** ✅ RECOMENDADO
```
portafolio-2025/
├── .gitignore
├── README.md (índice maestro)
├── PROYECTOS.md (descripción de cada proyecto)
│
├── java/
│   ├── smarttask-web/      → Desplegar en Render
│   └── biblioteca-untec/   → Desplegar en Render
│
├── python/
│   ├── jarvis/             → Desplegar en Render
│   ├── sismo-predict/      → Desplegar en Render
│   └── unir-pdf/           → (NO desplegar, solo incluir)
│
└── web/
    ├── wallet2/            → Desplegar en Render (static)
    ├── meet-coffe/         → Desplegar en Render (static)
    └── viajes-chile/       → Desplegar en Render (static)
```

**Ventajas:**
- ✅ Un repositorio único en GitHub
- ✅ Fácil de navegar y compartir
- ✅ Múltiples despliegues desde un repo

**GitHub URL:** `https://github.com/mbigliam/portafolio-2025`

---

## 🎯 ORDEN DE TRABAJO RECOMENDADO

### **FASE 1: PROYECTOS PYTHON** (Día 1)
1. ✅ Revisar JARVIS
   - Extraer requirements.txt completo
   - Crear Procfile
   - Crear .gitignore
   - Inicializar git
   
2. ✅ Revisar SISMO-PREDICT B-AUTO
   - Idem JARVIS
   
3. ✅ Incluir UNIR_PDF
   - Solo agregar al repo (sin despliegue)

### **FASE 2: PROYECTOS JAVA** (Día 2)
4. ✅ SmartTask-Web (YA HECHO ✅)

5. ✅ BibliotecaUNTEC
   - Descomprimir ZIP
   - Extraer pom.xml
   - Crear Procfile
   - Crear .gitignore

### **FASE 3: PROYECTOS WEB** (Día 3)
6. ✅ wallet2
7. ✅ Meet-Coffe-Main
8. ✅ Viajes-Chile-Main

### **FASE 4: INTEGRACIÓN FINAL** (Día 4)
9. Crear repositorio maestro en GitHub
10. Fusionar todos los proyectos
11. Crear README.md maestro
12. Desplegar en Render (múltiples servicios)
13. Crear página de portafolio que links a todos

---

## 🔧 CHECKLIST DE ARCHIVOS NECESARIOS

Para cada proyecto:
- [ ] `.gitignore` (evitar subir build/, dist/, .vscode/, etc)
- [ ] `README.md` (descripción del proyecto)
- [ ] `Procfile` (solo para proyectos que necesiten ejecutable)
- [ ] `requirements.txt` (Python)
- [ ] `pom.xml` (Java - ya debe estar)
- [ ] `.git` inicializado

---

## 📌 PRÓXIMOS PASOS

1. **Confirma:** ¿Quieres UN repositorio maestro o múltiples?
2. **Empezamos por:** ¿Cuál proyecto revisar PRIMERO?

**Mi recomendación:** JARVIS (Python) → más simple que BibliotecaUNTEC

¿Vamos? 🚀
