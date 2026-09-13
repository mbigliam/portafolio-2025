# 🚀 CONFIGURACIÓN MASTER - Portafolio en GitHub & Render

## 📋 PASOS EXACTOS PARA CREAR TU REPOSITORIO

### PASO 1: Crear Repositorio en GitHub
```bash
# 1. Ve a https://github.com/new
# 2. Nombre: portafolio-2025
# 3. Descripción: Portafolio profesional con 8 proyectos (Java, Python, HTML/CSS/JS)
# 4. Selecciona: Public
# 5. Añade .gitignore: None (lo crearemos)
# 6. Haz click en "Create repository"

# Luego ejecuta en tu terminal:
git clone https://github.com/mbigliam/portafolio-2025.git
cd portafolio-2025
```

---

## 📁 ESTRUCTURA FINAL DEL REPOSITORIO

```
portafolio-2025/
├── README.md                    ← Índice maestro
├── .gitignore                   ← Archivos a ignorar
├── index_ACTUALIZADO.html       ← Portfolio con 8 proyectos
├── assets/                      ← Assets del portfolio
│   ├── css/
│   ├── js/
│   └── img/
│
├── java/
│   ├── smarttask-web/           → Ya configurado ✅
│   │   ├── pom.xml
│   │   ├── Procfile
│   │   ├── .gitignore
│   │   ├── README.md
│   │   ├── src/
│   │   └── target/
│   │
│   └── biblioteca-untec/        → Necesita configuración
│       ├── pom.xml
│       ├── Procfile
│       ├── .gitignore
│       ├── README.md
│       ├── src/
│       └── target/
│
├── python/
│   ├── jarvis/                  → Necesita requirements.txt + Procfile
│   │   ├── requirements.txt
│   │   ├── Procfile
│   │   ├── .gitignore
│   │   ├── run.py
│   │   ├── README.md
│   │   └── (todo contenido)
│   │
│   ├── sismo-predict/           → Necesita requirements.txt + Procfile
│   │   ├── requirements.txt
│   │   ├── Procfile
│   │   ├── .gitignore
│   │   ├── api.py
│   │   ├── index.html
│   │   ├── README.md
│   │   └── (todo contenido)
│   │
│   └── unir-pdf/                → Desktop app (solo incluir)
│       ├── .gitignore
│       ├── Unir_pdfs_1.2.py
│       ├── README.md
│       └── (todo contenido)
│
└── web/
    ├── wallet2/                 → Sitio estático
    │   ├── .gitignore
    │   ├── index.html
    │   ├── login.html
    │   ├── menu.html
    │   ├── deposit.html
    │   ├── sendmoney.html
    │   ├── transactions.html
    │   ├── assets/
    │   └── README.md
    │
    ├── meet-coffe/              → Sitio estático
    │   ├── .gitignore
    │   ├── index.html
    │   ├── assets/
    │   ├── README.md
    │   └── (todo contenido)
    │
    └── viajes-chile/            → Sitio estático
        ├── .gitignore
        ├── index.html
        ├── assets/
        ├── README.md
        └── (todo contenido)
```

---

## 🔧 PASO 2: Crear Archivos de Configuración Globales

### `.gitignore` (raíz del repositorio)
```
# Build directories
build/
dist/
target/
*.o
*.class

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
.Python
venv/
.env

# Sistema
.DS_Store
Thumbs.db
*.log

# Render
.render-api-token

# NodeJS (si aplica)
node_modules/
npm-debug.log
```

### `README.md` (raíz - Índice Maestro)
```markdown
# 🚀 Portafolio Profesional - Mauricio Biglia

Portafolio completo con 8 proyectos desplegados en **Render.com** y código fuente en **GitHub**.

## 📂 Proyectos

### ☕ JAVA (2 Proyectos)
1. **SmartTask-Web** - Gestor de tareas con Spring Boot 3
   - [GitHub](./java/smarttask-web)
   - [Demo en Render](https://smarttask-web.onrender.com/smarttask/)

2. **BibliotecaUNTEC** - Sistema de biblioteca
   - [GitHub](./java/biblioteca-untec)
   - [Demo en Render](https://biblioteca-untec.onrender.com/)

### 🐍 PYTHON (3 Proyectos)
3. **JARVIS** - Asistente IA con Ollama/Gemini
   - [GitHub](./python/jarvis)
   - [Demo en Render](https://jarvis-app.onrender.com/)

4. **SISMO-PREDICT B-AUTO** - Predicción de sismos
   - [GitHub](./python/sismo-predict)
   - [Demo en Render](https://sismo-predict.onrender.com/)

5. **UNIR PDF** - Utilidad de escritorio
   - [GitHub](./python/unir-pdf)
   - Nota: Aplicación de escritorio (no tiene demo)

### 🌐 WEB (3 Proyectos)
6. **Wallet2** - Billetera Digital
   - [GitHub](./web/wallet2)
   - [Demo en Render](https://wallet2.onrender.com/)

7. **Meet Coffe** - Sitio Web
   - [GitHub](./web/meet-coffe)
   - [Demo en Render](https://meet-coffe.onrender.com/)

8. **Viajes Chile** - Portal Turístico
   - [GitHub](./web/viajes-chile)
   - [Demo en Render](https://viajes-chile.onrender.com/)

## 📊 Resumen

| Proyecto | Tecnología | Estado |
|----------|-----------|--------|
| SmartTask-Web | Java 17, Spring Boot 3, JSP | ✅ Activo |
| BibliotecaUNTEC | Java, Spring Boot | ✅ Activo |
| JARVIS | Python, FastAPI, Ollama | ✅ Activo |
| SISMO-PREDICT | Python, Flask | ✅ Activo |
| UNIR PDF | Python, PyInstaller | ✅ Desktop |
| Wallet2 | HTML5, CSS3, JS | ✅ Activo |
| Meet Coffe | HTML5, CSS3, JS | ✅ Activo |
| Viajes Chile | HTML5, CSS3, JS | ✅ Activo |

## 👤 Autor
**Mauricio Biglia** - mauriciobigliam@gmail.com

## 📧 Contacto
- LinkedIn: [Tu perfil]
- Email: mauriciobigliam@gmail.com
```

---

## 📋 PASO 3: Archivos por Proyecto

### PROYECTOS PYTHON - Archivos Necesarios

#### `python/jarvis/Procfile`
```
web: python run.py
```

#### `python/jarvis/requirements.txt`
```
# IMPORTANTE: Extraer del proyecto existente o usar:
Flask==2.3.2
requests==2.31.0
python-dotenv==1.0.0
# Añadir más según sea necesario
```

#### `python/jarvis/.gitignore`
```
__pycache__/
*.py[cod]
*.env
.venv/
build/
dist/
*.egg-info/
.DS_Store
```

#### `python/jarvis/README.md`
```markdown
# JARVIS - Asistente IA

Asistente de voz e inteligencia artificial con integración de Ollama y Gemini.

## Características
- Procesamiento de lenguaje natural
- Integración con Ollama local
- API Gemini
- Interfaz web moderna

## Tecnologías
- Python
- Flask/FastAPI
- Ollama
- Gemini API

## Despliegue
Visitá https://jarvis-app.onrender.com/
```

---

#### `python/sismo-predict/Procfile`
```
web: python api.py
```

#### `python/sismo-predict/requirements.txt`
```
Flask==2.3.2
pandas==2.0.3
numpy==1.24.3
requests==2.31.0
python-dotenv==1.0.0
# Añadir más según sea necesario
```

#### `python/sismo-predict/.gitignore`
```
__pycache__/
*.py[cod]
*.env
.venv/
*.csv
.DS_Store
```

#### `python/sismo-predict/README.md`
```markdown
# SISMO-PREDICT B-AUTO

Sistema de predicción y monitoreo de sismos con análisis de datos en tiempo real.

## Características
- API REST con Flask
- Análisis de datos sísmicos
- Frontend interactivo
- Base de datos de eventos

## Tecnologías
- Python
- Flask
- HTML5/CSS3/JavaScript

## Despliegue
Visitá https://sismo-predict.onrender.com/
```

---

#### `python/unir-pdf/README.md`
```markdown
# UNIR PDF - Utilidad de Fusión

Herramienta de escritorio para fusionar múltiples archivos PDF en uno solo.

## Características
- Interfaz gráfica amigable
- Soporte para múltiples PDFs
- Salida configurada

## Tecnologías
- Python
- PyInstaller (compilado como .exe)
- Desktop GUI

## Nota
Esta es una aplicación de escritorio compilada. No tiene versión web en Render.
```

---

### PROYECTOS JAVA - Procfile

#### `java/smarttask-web/Procfile`
```
web: java -jar target/smarttask-web-1.0.0.war
```

#### `java/biblioteca-untec/Procfile`
```
web: java -jar target/biblioteca-untec.war
```

---

### PROYECTOS WEB - .gitignore

#### `web/wallet2/.gitignore`
```
.DS_Store
.vscode/
node_modules/
*.log
```

#### `web/meet-coffe/.gitignore`
```
.DS_Store
.vscode/
node_modules/
*.log
```

#### `web/viajes-chile/.gitignore`
```
.DS_Store
.vscode/
node_modules/
*.log
```

---

## ✅ CHECKLIST DE ARCHIVOS

### Por Tipo de Proyecto:

**Python (JARVIS, SISMO-PREDICT):**
- [ ] requirements.txt
- [ ] Procfile
- [ ] .gitignore
- [ ] README.md
- [ ] Código fuente completo

**Python (UNIR-PDF):**
- [ ] .gitignore
- [ ] README.md
- [ ] Código fuente

**Java (SmartTask-Web, BibliotecaUNTEC):**
- [ ] pom.xml
- [ ] Procfile
- [ ] .gitignore
- [ ] README.md
- [ ] src/ compilado
- [ ] target/ (ignorado en .gitignore)

**Web (Wallet2, Meet-Coffe, Viajes-Chile):**
- [ ] index.html
- [ ] assets/
- [ ] .gitignore
- [ ] README.md

---

## 🎯 ORDEN DE TAREAS

### Día 1: Configuración GitHub
1. Crear repositorio `portafolio-2025`
2. Crear estructura de carpetas
3. Agregar `.gitignore` global
4. Agregar `README.md` maestro
5. Primer commit

### Día 2: Python Projects
1. Configurar `python/jarvis/`
2. Configurar `python/sismo-predict/`
3. Incluir `python/unir-pdf/`
4. Commits y pushes

### Día 3: Java Projects
1. Configurar `java/smarttask-web/`
2. Configurar `java/biblioteca-untec/`
3. Verificar builds
4. Commits y pushes

### Día 4: Web Projects
1. Configurar `web/wallet2/`
2. Configurar `web/meet-coffe/`
3. Configurar `web/viajes-chile/`
4. Commits y pushes

### Día 5: Render Deployments
1. Crear servicios en Render (8 total)
2. Conectar repositorios GitHub
3. Configurar variables de entorno
4. Ejecutar deployments
5. Probar todos los links

### Día 6: Portfolio Final
1. Actualizar `index_ACTUALIZADO.html` como `index.html`
2. Verificar todos los links
3. Commit final
4. ¡LANZAR! 🚀

---

## 📞 Próximos Pasos

1. **Crea el repositorio en GitHub** con el nombre `portafolio-2025`
2. **Clona el repositorio** en tu computadora
3. **Avísame cuando esté listo**, y vamos a:
   - Crear la estructura de carpetas
   - Generar automáticamente los archivos faltantes
   - Hacer el primer push

¿Empezamos? 🚀
