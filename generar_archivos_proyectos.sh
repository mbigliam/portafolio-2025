#!/bin/bash

# 🚀 SCRIPT DE GENERACIÓN AUTOMÁTICA DE ARCHIVOS PARA PROYECTOS
# Este script crea todos los archivos necesarios (requirements.txt, Procfile, .gitignore, README.md)
# para tus 8 proyectos

set -e

echo "════════════════════════════════════════════════════"
echo "🚀 GENERADOR DE ARCHIVOS PARA PORTAFOLIO-2025"
echo "════════════════════════════════════════════════════"

# Variables
REPO_ROOT="${1:-.}"
DATE=$(date +"%Y-%m-%d")

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para crear archivo de configuración
create_file() {
    local path=$1
    local content=$2
    local dir=$(dirname "$path")

    mkdir -p "$dir"
    echo -e "$content" > "$path"
    echo -e "${GREEN}✅ Creado:${NC} $path"
}

echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}1️⃣  CONFIGURANDO PROYECTOS PYTHON${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# === JARVIS ===
echo "📦 JARVIS..."
create_file "$REPO_ROOT/python/jarvis/requirements.txt" "Flask==2.3.2
Werkzeug==2.3.6
Jinja2==3.1.2
click==8.1.3
itsdangerous==2.1.2
requests==2.31.0
certifi==2023.5.7
charset-normalizer==3.1.0
idna==3.4
urllib3==2.0.3
python-dotenv==1.0.0
ollama==0.0.11
google-generativeai==0.3.0
# Añade más dependencias según sea necesario"

create_file "$REPO_ROOT/python/jarvis/Procfile" "web: python run.py"

create_file "$REPO_ROOT/python/jarvis/.gitignore" "__pycache__/
*.py[cod]
*\$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.env
.vscode/
.idea/
*.log
.DS_Store
Thumbs.db"

create_file "$REPO_ROOT/python/jarvis/README.md" "# 🤖 JARVIS - Asistente IA

Asistente de voz e inteligencia artificial con integración con **Ollama** y **Gemini API**.

## 🎯 Características

- 🗣️ Procesamiento de voz con reconocimiento de lenguaje natural
- 🧠 Integración con Ollama para modelos locales
- ✨ API Gemini de Google para respuestas inteligentes
- 🎨 Interfaz web moderna y responsiva
- ⚙️ Sistema modular y extensible

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|-----------|-----------|
| **Backend** | Python |
| **Web Framework** | Flask |
| **IA Local** | Ollama |
| **IA Cloud** | Google Gemini API |
| **Frontend** | HTML5/CSS3/JavaScript |

## 📋 Requisitos

- Python 3.8+
- pip
- Ollama instalado (opcional para modo local)
- API Key de Gemini (opcional)

## 🚀 Instalación Local

\`\`\`bash
# Clonar el repositorio
git clone https://github.com/mbigliam/portafolio-2025.git
cd portafolio-2025/python/jarvis

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\\Scripts\\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar aplicación
python run.py
\`\`\`

## 🌐 Acceso

Abre tu navegador y ve a:
\`\`\`
http://localhost:5000
\`\`\`

## 🌍 Despliegue en Render

Visitá la demo en vivo:
**https://jarvis-app.onrender.com/**

## 📂 Estructura del Proyecto

\`\`\`
jarvis/
├── run.py                 # Punto de entrada
├── requirements.txt       # Dependencias
├── Procfile              # Config Render
├── .gitignore
├── ai/                   # Módulo IA
├── app/                  # Aplicación Flask
├── config/               # Configuración
├── core/                 # Lógica principal
├── voice/                # Procesamiento de voz
├── ui/                   # Interfaz web
└── README.md
\`\`\`

## 🔌 Endpoints

| Método | URL | Descripción |
|--------|-----|------------|
| GET | `/` | Página principal |
| POST | `/api/ask` | Enviar pregunta |
| POST | `/api/voice` | Procesar audio |

## 👤 Autor

**Mauricio Biglia** - mauriciobigliam@gmail.com

## 📄 Licencia

MIT License - Siéntete libre de usar este proyecto"

# === SISMO-PREDICT ===
echo "📦 SISMO-PREDICT B-AUTO..."
create_file "$REPO_ROOT/python/sismo-predict/requirements.txt" "Flask==2.3.2
Werkzeug==2.3.6
Jinja2==3.1.2
click==8.1.3
itsdangerous==2.1.2
requests==2.31.0
certifi==2023.5.7
charset-normalizer==3.1.0
idna==3.4
urllib3==2.0.3
pandas==2.0.3
numpy==1.24.3
matplotlib==3.7.1
python-dateutil==2.8.2
pytz==2023.3
six==1.16.0
python-dotenv==1.0.0
# Añade más dependencias según sea necesario"

create_file "$REPO_ROOT/python/sismo-predict/Procfile" "web: python api.py"

create_file "$REPO_ROOT/python/sismo-predict/.gitignore" "__pycache__/
*.py[cod]
*\$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.env
.vscode/
.idea/
*.log
.DS_Store
Thumbs.db
*.csv
cache/
*.json"

create_file "$REPO_ROOT/python/sismo-predict/README.md" "# 🌍 SISMO-PREDICT B-AUTO

Sistema de predicción y monitoreo de sismos con análisis de datos en **tiempo real**.

## 🎯 Características

- 📊 Análisis de datos sísmicos históricos
- 🔮 Predicción de eventos sísmicos
- 📈 Visualización interactiva de datos
- 🌐 API REST para consultas
- 📱 Frontend moderno y responsivo

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|-----------|-----------|
| **Backend** | Python |
| **Web Framework** | Flask |
| **Análisis de Datos** | Pandas, NumPy |
| **Visualización** | Matplotlib |
| **Frontend** | HTML5/CSS3/JavaScript |

## 📋 Requisitos

- Python 3.8+
- pip
- Datos sísmicos (CSV/JSON)

## 🚀 Instalación Local

\`\`\`bash
# Clonar el repositorio
git clone https://github.com/mbigliam/portafolio-2025.git
cd portafolio-2025/python/sismo-predict

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\\Scripts\\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python api.py
\`\`\`

## 🌐 Acceso

Abre tu navegador y ve a:
\`\`\`
http://localhost:5000
\`\`\`

## 🌍 Despliegue en Render

Visitá la demo en vivo:
**https://sismo-predict.onrender.com/**

## 📂 Estructura del Proyecto

\`\`\`
sismo-predict/
├── api.py                    # Aplicación Flask
├── sismo_predict_b_auto.py   # Lógica de predicción
├── requirements.txt          # Dependencias
├── Procfile                  # Config Render
├── .gitignore
├── index.html               # Frontend
├── assets/                  # CSS, JS, imágenes
├── data/                    # Datos sísmicos
└── README.md
\`\`\`

## 🔌 Endpoints

| Método | URL | Descripción |
|--------|-----|------------|
| GET | `/` | Dashboard principal |
| GET | `/api/sismos` | Obtener eventos |
| GET | `/api/prediccion` | Obtener predicciones |
| POST | `/api/analizar` | Analizar datos |

## 👤 Autor

**Mauricio Biglia** - mauriciobigliam@gmail.com

## 📄 Licencia

MIT License - Siéntete libre de usar este proyecto"

# === UNIR PDF ===
echo "📦 UNIR PDF..."
create_file "$REPO_ROOT/python/unir-pdf/.gitignore" "__pycache__/
*.py[cod]
*\$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.env
.vscode/
.idea/
*.log
.DS_Store
Thumbs.db
*.spec
build/"

create_file "$REPO_ROOT/python/unir-pdf/README.md" "# 📄 UNIR PDF - Utilidad de Fusión

Herramienta de escritorio para fusionar múltiples archivos **PDF** en uno solo.

## 🎯 Características

- 🖱️ Interfaz gráfica amigable (No requiere terminal)
- 📂 Selecciona múltiples PDFs fácilmente
- 🔄 Reordena archivos drag-and-drop
- 💾 Guarda el PDF combinado donde desees
- ⚡ Rápido y eficiente

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|-----------|-----------|
| **Lenguaje** | Python |
| **GUI** | tkinter (incluido en Python) |
| **Compilación** | PyInstaller |
| **PDF** | PyPDF2 |
| **Distribución** | Ejecutable .exe |

## 📥 Descarga

Descarga el ejecutable compilado desde las **Releases** de este repositorio.

### Windows
\`\`\`
unir-pdf.exe
\`\`\`

## 🚀 Instalación Desde Código

Si prefieres ejecutar desde código:

\`\`\`bash
# Clonar el repositorio
git clone https://github.com/mbigliam/portafolio-2025.git
cd portafolio-2025/python/unir-pdf

# Crear entorno virtual
python -m venv venv
venv\\Scripts\\activate  # En Linux/Mac: source venv/bin/activate

# Instalar dependencias
pip install PyPDF2

# Ejecutar
python Unir_pdfs_1.2.py
\`\`\`

## 📖 Cómo Usar

1. **Abre la aplicación** (ejecuta el .exe o python Unir_pdfs_1.2.py)
2. **Añade archivos** haciendo click en \"Agregar PDFs\"
3. **Reordena** si lo necesitas (drag-and-drop)
4. **Elimina** archivos innecesarios
5. **Fusiona** haciendo click en \"Combinar PDFs\"
6. **Guarda** el archivo resultante

## 📂 Estructura del Proyecto

\`\`\`
unir-pdf/
├── Unir_pdfs_1.2.py      # Script principal
├── requirements.txt       # Dependencias (si ejecutas desde código)
├── .gitignore
├── README.md
└── (compilado como .exe si lo has generado)
\`\`\`

## 📋 Requisitos

**Para ejecutar el .exe:**
- Windows 10/11

**Para ejecutar desde código:**
- Python 3.8+
- pip
- PyPDF2

## 👤 Autor

**Mauricio Biglia** - mauriciobigliam@gmail.com

## 📄 Licencia

MIT License - Siéntete libre de usar este proyecto"

echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}2️⃣  CONFIGURANDO PROYECTOS WEB (ESTÁTICOS)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# === WALLET2 ===
echo "📦 WALLET2..."
create_file "$REPO_ROOT/web/wallet2/.gitignore" ".DS_Store
.vscode/
.idea/
node_modules/
*.log
Thumbs.db"

create_file "$REPO_ROOT/web/wallet2/README.md" "# 💳 Wallet2 - Billetera Digital

Aplicación interactiva de **gestión de transacciones** y control monetario.

## 🎯 Características

- 🔐 Sistema de login seguro
- 💰 Gestión de saldos
- 💸 Depósitos y transferencias
- 📋 Historial de transacciones
- 📱 Interfaz moderna y responsiva
- 🎨 Diseño elegante con animaciones

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|-----------|-----------|
| **Frontend** | HTML5 |
| **Estilos** | CSS3 |
| **Interactividad** | JavaScript Vanilla |
| **Framework CSS** | Bootstrap 5 |
| **Iconos** | Font Awesome |

## 📂 Estructura

\`\`\`
wallet2/
├── index.html              # Página principal
├── login.html              # Login
├── menu.html               # Menú principal
├── deposit.html            # Depósitos
├── sendmoney.html          # Enviar dinero
├── transactions.html       # Historial
├── assets/
│   ├── css/                # Estilos
│   ├── js/                 # Scripts
│   └── img/                # Imágenes
└── README.md
\`\`\`

## 🌐 Demo en Vivo

Visitá: **https://wallet2.onrender.com/**

## 💻 Ejecución Local

1. Clona el repositorio
2. Abre \`index.html\` en tu navegador
3. ¡Listo! No requiere backend

## 👤 Autor

**Mauricio Biglia** - mauriciobigliam@gmail.com

## 📄 Licencia

MIT License"

# === MEET COFFE ===
echo "📦 MEET COFFE..."
create_file "$REPO_ROOT/web/meet-coffe/.gitignore" ".DS_Store
.vscode/
.idea/
node_modules/
*.log
Thumbs.db"

create_file "$REPO_ROOT/web/meet-coffe/README.md" "# ☕ Meet Coffe - Sitio Web Corporativo

Sitio web corporativo de **cafetería** con diseño responsivo y elegante.

## 🎯 Características

- 🏪 Información de la empresa
- ☕ Catálogo de productos
- 🖼️ Galería de fotos
- 📍 Ubicación y contacto
- 📱 Diseño responsive
- ✨ Animaciones atractivas

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|-----------|-----------|
| **Frontend** | HTML5 |
| **Estilos** | CSS3 |
| **Interactividad** | JavaScript Vanilla |
| **Iconos** | Font Awesome |
| **Animaciones** | CSS Animations |

## 📂 Estructura

\`\`\`
meet-coffe/
├── index.html          # Página principal
├── assets/
│   ├── css/            # Estilos
│   ├── js/             # Scripts
│   └── img/            # Imágenes
└── README.md
\`\`\`

## 🌐 Demo en Vivo

Visitá: **https://meet-coffe.onrender.com/**

## 💻 Ejecución Local

1. Clona el repositorio
2. Abre \`index.html\` en tu navegador
3. ¡Listo! No requiere backend

## 👤 Autor

**Mauricio Biglia** - mauriciobigliam@gmail.com

## 📄 Licencia

MIT License"

# === VIAJES CHILE ===
echo "📦 VIAJES CHILE..."
create_file "$REPO_ROOT/web/viajes-chile/.gitignore" ".DS_Store
.vscode/
.idea/
node_modules/
*.log
Thumbs.db"

create_file "$REPO_ROOT/web/viajes-chile/README.md" "# 🏔️ Viajes Chile - Portal Turístico

Portal turístico de **destinos en Chile** con galería de atractivos y paquetes de viajes.

## 🎯 Características

- 🗺️ Destinos turísticos de Chile
- 🏖️ Galería de atractivos
- 🎫 Paquetes de viajes
- 📸 Fotos de paisajes
- 📱 Diseño responsive
- 🎨 Interfaz elegante

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|-----------|-----------|
| **Frontend** | HTML5 |
| **Estilos** | CSS3 |
| **Interactividad** | JavaScript Vanilla |
| **Framework CSS** | Bootstrap 5 |
| **Animaciones** | CSS Animations |

## 📂 Estructura

\`\`\`
viajes-chile/
├── index.html          # Página principal
├── assets/
│   ├── css/            # Estilos
│   ├── js/             # Scripts
│   └── img/            # Imágenes
└── README.md
\`\`\`

## 🌐 Demo en Vivo

Visitá: **https://viajes-chile.onrender.com/**

## 💻 Ejecución Local

1. Clona el repositorio
2. Abre \`index.html\` en tu navegador
3. ¡Listo! No requiere backend

## 👤 Autor

**Mauricio Biglia** - mauriciobigliam@gmail.com

## 📄 Licencia

MIT License"

echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}3️⃣  CONFIGURANDO PROYECTOS JAVA${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# === SMARTTASK-WEB (ya está configurado, solo verificamos) ===
echo "📦 SMARTTASK-WEB (verificación)..."
if [ -f "$REPO_ROOT/java/smarttask-web/Procfile" ]; then
    echo -e "${GREEN}✅ Procfile encontrado${NC}"
else
    create_file "$REPO_ROOT/java/smarttask-web/Procfile" "web: java -jar target/smarttask-web-1.0.0.war"
fi

# === BIBLIOTECA-UNTEC ===
echo "📦 BIBLIOTECA-UNTEC..."
create_file "$REPO_ROOT/java/biblioteca-untec/Procfile" "web: java -jar target/biblioteca-untec.war"

create_file "$REPO_ROOT/java/biblioteca-untec/.gitignore" "# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.backup
release.properties
dependency-reduced-pom.xml

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.classpath
.project
.settings/
*.iml

# Build
build/
dist/
*.class
*.jar
*.war
*.ear
*.zip

# System
.DS_Store
Thumbs.db
*.log

# Render
.render-api-token"

create_file "$REPO_ROOT/java/biblioteca-untec/README.md" "# 📚 BibliotecaUNTEC - Sistema de Biblioteca

Sistema completo de **gestión bibliotecaria** con módulos de catalogación, préstamos y reportes.

## 🎯 Características

- 📖 Catálogo de libros
- 👥 Gestión de usuarios/miembros
- 📋 Sistema de préstamos
- 📊 Reportes y estadísticas
- 🔍 Búsqueda avanzada
- 🎨 Interfaz web moderna

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|-----------|-----------|
| **Lenguaje** | Java |
| **Framework** | Spring Boot |
| **Web** | Spring MVC, JSP |
| **Persistence** | JPA/Hibernate |
| **Database** | MySQL |
| **Build Tool** | Maven |
| **Frontend** | HTML5/CSS3/Bootstrap |

## 📋 Requisitos Previos

- Java 11 o superior
- Maven 3.8.1 o superior
- MySQL Server

## 🚀 Instalación Local

\`\`\`bash
# Clonar el repositorio
git clone https://github.com/mbigliam/portafolio-2025.git
cd portafolio-2025/java/biblioteca-untec

# Compilar
mvn clean package

# Ejecutar
mvn spring-boot:run
\`\`\`

## 🌐 Acceso

Abre tu navegador y ve a:
\`\`\`
http://localhost:8080/biblioteca/
\`\`\`

## 🌍 Despliegue en Render

Visitá la demo en vivo:
**https://biblioteca-untec.onrender.com/**

## 📂 Estructura del Proyecto

\`\`\`
biblioteca-untec/
├── pom.xml                         # Configuración Maven
├── Procfile                        # Config Render
├── .gitignore
├── src/main/java/com/biblioteca/
│   ├── model/                      # Modelos (Libro, Usuario, etc)
│   ├── repository/                 # Acceso a datos
│   ├── service/                    # Lógica de negocio
│   ├── controller/                 # Controladores
│   └── BibliotecaApplication.java
├── src/main/webapp/WEB-INF/jsp/
│   ├── index.jsp
│   └── (otras vistas)
├── src/main/resources/
│   └── application.properties
└── README.md
\`\`\`

## 🔌 Endpoints Principales

| Método | URL | Descripción |
|--------|-----|------------|
| GET | `/biblioteca/` | Inicio |
| GET | `/biblioteca/libros` | Listar libros |
| GET | `/biblioteca/usuarios` | Listar usuarios |
| POST | `/biblioteca/prestamos` | Crear préstamo |
| GET | `/biblioteca/reportes` | Ver reportes |

## 👤 Autor

**Mauricio Biglia** - mauriciobigliam@gmail.com

## 📄 Licencia

MIT License"

echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}✅ GENERACIÓN COMPLETADA${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${YELLOW}📋 PRÓXIMOS PASOS:${NC}"
echo -e "1. Ve a GitHub y crea el repositorio: ${GREEN}portafolio-2025${NC}"
echo -e "2. Clona el repositorio en tu computadora"
echo -e "3. Copia los archivos generados en la estructura del repositorio"
echo -e "4. Ejecuta: ${GREEN}git add -A && git commit -m 'Initial commit: Portfolio structure'${NC}"
echo -e "5. Ejecuta: ${GREEN}git push${NC}"
echo -e "6. ¡Avísame cuando esté en GitHub!\n"

echo -e "${GREEN}✨ ¡Todos los archivos han sido generados! ✨${NC}\n"
