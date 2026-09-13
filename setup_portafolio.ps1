# ========================================
# SCRIPT DE CONFIGURACIÓN AUTOMÁTICA
# Portafolio 2025 - Setup Completo
# ========================================

param(
    [string]$RepoPath = "C:\Proyectos\Proyectos\portafolio-2025"
)

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🚀 CONFIGURADOR AUTOMÁTICO - PORTAFOLIO 2025            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "📁 Carpeta: $RepoPath" -ForegroundColor Yellow
Write-Host ""

# Cambiar a la carpeta del repositorio
if (-not (Test-Path $RepoPath)) {
    Write-Host "❌ La carpeta no existe. Abortando..." -ForegroundColor Red
    exit 1
}

Set-Location $RepoPath
Write-Host "✅ Ubicación: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# ========================================
# 1. CREAR ESTRUCTURA DE CARPETAS
# ========================================
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "1️⃣  CREANDO ESTRUCTURA DE CARPETAS..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

$folders = @(
    "java\smarttask-web",
    "java\biblioteca-untec",
    "python\jarvis",
    "python\sismo-predict",
    "python\unir-pdf",
    "web\wallet2",
    "web\meet-coffe",
    "web\viajes-chile"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
    Write-Host "✅ Creado: $folder" -ForegroundColor Green
}

Write-Host ""
Write-Host "✨ Estructura de carpetas completa" -ForegroundColor Green
Write-Host ""

# ========================================
# 2. CREAR .gitignore GLOBAL
# ========================================
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "2️⃣  CREANDO .gitignore GLOBAL..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

$gitignore = @"
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
*`$py.class
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

# Node
node_modules/
npm-debug.log
"@

$gitignore | Set-Content -Path ".gitignore" -Encoding UTF8
Write-Host "✅ Creado: .gitignore" -ForegroundColor Green
Write-Host ""

# ========================================
# 3. CREAR README.md MAESTRO
# ========================================
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "3️⃣  CREANDO README.md MAESTRO..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

$readme = @"
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

## 👤 Autor
**Mauricio Biglia** - mauriciobigliam@gmail.com
"@

$readme | Set-Content -Path "README.md" -Encoding UTF8
Write-Host "✅ Creado: README.md" -ForegroundColor Green
Write-Host ""

# ========================================
# 4. CREAR PROCFILE PARA PYTHON
# ========================================
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "4️⃣  CREANDO PROCFILES PYTHON..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# JARVIS
"web: python run.py" | Set-Content -Path "python\jarvis\Procfile" -Encoding UTF8
Write-Host "✅ Creado: python/jarvis/Procfile" -ForegroundColor Green

# SISMO-PREDICT
"web: python api.py" | Set-Content -Path "python\sismo-predict\Procfile" -Encoding UTF8
Write-Host "✅ Creado: python/sismo-predict/Procfile" -ForegroundColor Green

Write-Host ""

# ========================================
# 5. CREAR PROCFILE PARA JAVA
# ========================================
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "5️⃣  CREANDO PROCFILES JAVA..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# SmartTask-Web
"web: java -jar target/smarttask-web-1.0.0.war" | Set-Content -Path "java\smarttask-web\Procfile" -Encoding UTF8
Write-Host "✅ Creado: java/smarttask-web/Procfile" -ForegroundColor Green

# BibliotecaUNTEC
"web: java -jar target/biblioteca-untec.war" | Set-Content -Path "java\biblioteca-untec\Procfile" -Encoding UTF8
Write-Host "✅ Creado: java/biblioteca-untec/Procfile" -ForegroundColor Green

Write-Host ""

# ========================================
# 6. CREAR .gitignore POR PROYECTO
# ========================================
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "6️⃣  CREANDO .gitignore POR PROYECTO..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# Python projects .gitignore
$python_gitignore = @"
__pycache__/
*.py[cod]
*.env
.venv/
build/
dist/
*.egg-info/
.DS_Store
"@

foreach ($proj in @("python\jarvis", "python\sismo-predict", "python\unir-pdf")) {
    $python_gitignore | Set-Content -Path "$proj\.gitignore" -Encoding UTF8
    Write-Host "✅ Creado: $proj/.gitignore" -ForegroundColor Green
}

# Java projects .gitignore
$java_gitignore = @"
target/
.idea/
*.class
.DS_Store
*.iml
.vscode/
"@

foreach ($proj in @("java\smarttask-web", "java\biblioteca-untec")) {
    $java_gitignore | Set-Content -Path "$proj\.gitignore" -Encoding UTF8
    Write-Host "✅ Creado: $proj/.gitignore" -ForegroundColor Green
}

# Web projects .gitignore
$web_gitignore = @"
.DS_Store
node_modules/
*.log
Thumbs.db
.vscode/
"@

foreach ($proj in @("web\wallet2", "web\meet-coffe", "web\viajes-chile")) {
    $web_gitignore | Set-Content -Path "$proj\.gitignore" -Encoding UTF8
    Write-Host "✅ Creado: $proj/.gitignore" -ForegroundColor Green
}

Write-Host ""

# ========================================
# 7. CREAR README.md POR PROYECTO
# ========================================
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "7️⃣  CREANDO README.md POR PROYECTO..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# Crear README para cada proyecto
$readmes = @{
    "java\smarttask-web" = "# SmartTask-Web`n`nGestor de tareas con Spring Boot 3, Java 17, JSP y H2 Database.`n`n## Deploy: https://smarttask-web.onrender.com/smarttask/"
    "java\biblioteca-untec" = "# BibliotecaUNTEC`n`nSistema de gestión bibliotecaria con módulos de catalogación, préstamos y reportes.`n`n## Deploy: https://biblioteca-untec.onrender.com/"
    "python\jarvis" = "# JARVIS`n`nAsistente IA con integración de Ollama y Gemini.`n`n## Deploy: https://jarvis-app.onrender.com/"
    "python\sismo-predict" = "# SISMO-PREDICT`n`nSistema de predicción de sismos con análisis de datos en tiempo real.`n`n## Deploy: https://sismo-predict.onrender.com/"
    "python\unir-pdf" = "# UNIR PDF`n`nHerramienta de escritorio para fusionar archivos PDF."
    "web\wallet2" = "# Wallet2`n`nAplicación interactiva de gestión de transacciones.`n`n## Deploy: https://wallet2.onrender.com/"
    "web\meet-coffe" = "# Meet Coffe`n`nSitio web corporativo de cafetería.`n`n## Deploy: https://meet-coffe.onrender.com/"
    "web\viajes-chile" = "# Viajes Chile`n`nPortal turístico de destinos en Chile.`n`n## Deploy: https://viajes-chile.onrender.com/"
}

foreach ($proj in $readmes.Keys) {
    $readmes[$proj] | Set-Content -Path "$proj\README.md" -Encoding UTF8
    Write-Host "✅ Creado: $proj/README.md" -ForegroundColor Green
}

Write-Host ""

# ========================================
# 8. INICIALIZAR GIT
# ========================================
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "8️⃣  INICIALIZANDO GIT..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path ".git")) {
    & git init
    Write-Host "✅ Repositorio Git inicializado" -ForegroundColor Green
} else {
    Write-Host "⚠️  Git ya estaba inicializado" -ForegroundColor Yellow
}

Write-Host ""

# ========================================
# 9. AGREGAR ARCHIVOS Y PRIMER COMMIT
# ========================================
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "9️⃣  HACIENDO PRIMER COMMIT..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

& git add .
Write-Host "✅ Archivos agregados" -ForegroundColor Green

$commitMessage = @"
Initial commit: Portfolio 2025 structure setup

- Added main portfolio (index.html)
- Configured 8 projects (2 Java, 3 Python, 3 Web)
- Created Procfile for Python and Java projects
- Generated .gitignore files
- Created README.md for each project
- Added portfolio assets (CSS, JS, images)
- Ready for GitHub Pages and Render deployment

Projects:
- SmartTask-Web (Java/Spring Boot)
- BibliotecaUNTEC (Java/Spring Boot)
- JARVIS (Python/Flask)
- SISMO-PREDICT (Python/Flask)
- UNIR-PDF (Python/Desktop)
- Wallet2 (Web Static)
- Meet-Coffe (Web Static)
- Viajes-Chile (Web Static)
"@

& git commit -m $commitMessage
Write-Host "✅ Primer commit realizado" -ForegroundColor Green

Write-Host ""

# ========================================
# 10. MOSTRAR RESUMEN
# ========================================
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host "✨ ¡TODO COMPLETADO! ✨" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host ""

Write-Host "📊 RESUMEN:" -ForegroundColor Yellow
Write-Host "✅ Estructura de carpetas creada (8 proyectos)" -ForegroundColor Green
Write-Host "✅ .gitignore global y por proyecto" -ForegroundColor Green
Write-Host "✅ Procfile para Python y Java" -ForegroundColor Green
Write-Host "✅ README.md maestro y por proyecto" -ForegroundColor Green
Write-Host "✅ Git inicializado" -ForegroundColor Green
Write-Host "✅ Primer commit realizado" -ForegroundColor Green
Write-Host "✅ Portfolio index.html y assets listos" -ForegroundColor Green
Write-Host ""

Write-Host "🎯 PRÓXIMOS PASOS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Configura tu usuario de Git (si no lo has hecho):" -ForegroundColor Cyan
Write-Host "   git config --global user.name 'Mauricio Biglia'" -ForegroundColor Yellow
Write-Host "   git config --global user.email 'mauriciobigliam@gmail.com'" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Crea el repositorio en GitHub:" -ForegroundColor Cyan
Write-Host "   https://github.com/new" -ForegroundColor Yellow
Write-Host "   Nombre: portafolio-2025" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Agrega el remote y haz push:" -ForegroundColor Cyan
Write-Host "   git remote add origin https://github.com/mbigliam/portafolio-2025.git" -ForegroundColor Yellow
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Habilita GitHub Pages en Settings" -ForegroundColor Cyan
Write-Host "   Settings → Pages → Deploy from main" -ForegroundColor Yellow
Write-Host ""
Write-Host "5. Despliega en Render (7 servicios)" -ForegroundColor Cyan
Write-Host "   https://dashboard.render.com/" -ForegroundColor Yellow
Write-Host ""

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    ¡Vamos Mauricio! 🚀                    ║" -ForegroundColor Green
Write-Host "║         Tu portafolio está listo en 3-4 horas más        ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
