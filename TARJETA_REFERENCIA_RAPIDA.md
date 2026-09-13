# 📋 TARJETA DE REFERENCIA RÁPIDA - Portafolio 2025

## 🔗 LINKS ESENCIALES

```
Repositorio GitHub:        https://github.com/mbigliam/portafolio-2025
Portfolio en GitHub Pages: https://mbigliam.github.io/portafolio-2025/
Render Dashboard:          https://dashboard.render.com/
Tu Perfil GitHub:          https://github.com/mbigliam
```

---

## 📁 ESTRUCTURA DE CARPETAS

```
portafolio-2025/
├── index.html                          ← Portfolio principal
├── README.md                           ← Índice maestro
├── assets/                             ← CSS, JS, imágenes
├── CV_2026_2_MauricioFernando_BigliaMaldonado.pdf
├── .gitignore                          ← Global
│
├── java/
│   ├── smarttask-web/     (✅ Con Procfile)
│   └── biblioteca-untec/  (✅ Con Procfile)
│
├── python/
│   ├── jarvis/            (✅ Con requirements.txt + Procfile)
│   ├── sismo-predict/     (✅ Con requirements.txt + Procfile)
│   └── unir-pdf/          (✅ Sin Procfile - Desktop app)
│
└── web/
    ├── wallet2/           (✅ Static site)
    ├── meet-coffe/        (✅ Static site)
    └── viajes-chile/      (✅ Static site)
```

---

## 🎯 LOS 8 PROYECTOS

| # | Nombre | Tipo | Render | GitHub |
|---|--------|------|--------|--------|
| 1 | SmartTask-Web | Java | ✅ | ✅ |
| 2 | BibliotecaUNTEC | Java | ✅ | ✅ |
| 3 | JARVIS | Python | ✅ | ✅ |
| 4 | SISMO-PREDICT | Python | ✅ | ✅ |
| 5 | UNIR PDF | Python | ❌ | ✅ |
| 6 | Wallet2 | Web | ✅ | ✅ |
| 7 | Meet-Coffe | Web | ✅ | ✅ |
| 8 | Viajes-Chile | Web | ✅ | ✅ |

---

## 💻 COMANDOS GIT ESENCIALES

### Clonar
```bash
git clone https://github.com/mbigliam/portafolio-2025.git
cd portafolio-2025
```

### Verificar estado
```bash
git status
```

### Agregar cambios
```bash
git add .
git add archivo.txt           # Un archivo específico
```

### Hacer commit
```bash
git commit -m "Mensaje del cambio"
```

### Push
```bash
git push origin main          # Primer push
git push                       # Push posterior
```

### Ver historial
```bash
git log --oneline
```

---

## 🚀 PASOS PRINCIPALES (CHECKLIST)

### Fase 1: GitHub
- [ ] Crear repo: portafolio-2025
- [ ] Clonar repositorio
- [ ] Crear estructura de carpetas
- [ ] Copiar archivos de configuración
- [ ] Primer commit y push

### Fase 2: GitHub Pages
- [ ] Ir a Settings → Pages
- [ ] Branch: main | Folder: / (root)
- [ ] Save
- [ ] Esperar 2-3 min y abrir: https://mbigliam.github.io/portafolio-2025/

### Fase 3: Render (8 servicios)
Para cada proyecto:
- [ ] Dashboard Render → New + → Web Service (o Static Site)
- [ ] Conectar GitHub
- [ ] Configurar según tipo (Python/Java/Static)
- [ ] Create
- [ ] Obtener URL de Render
- [ ] Actualizar index.html si es necesario

---

## 📄 ARCHIVOS DE CONFIGURACIÓN POR PROYECTO

### Python (JARVIS, SISMO-PREDICT)

**Procfile:**
```
web: python run.py    # O: python api.py
```

**requirements.txt:**
```
Flask==2.3.2
requests==2.31.0
python-dotenv==1.0.0
# ... más dependencias
```

**. gitignore:**
```
__pycache__/
*.py[cod]
*.env
.venv/
.DS_Store
```

### Java (SmartTask-Web, BibliotecaUNTEC)

**Procfile:**
```
web: java -jar target/smarttask-web-1.0.0.war
```

**.gitignore:**
```
target/
.idea/
*.class
.DS_Store
```

### Web (Wallet2, Meet-Coffe, Viajes-Chile)

**.gitignore:**
```
.DS_Store
node_modules/
*.log
Thumbs.db
```

---

## 🌐 CONFIGURACIÓN EN RENDER

### Para Python Web Service
- Root Directory: `python/jarvis` (ejemplo)
- Runtime: Python 3
- Build Command: `pip install -r requirements.txt`
- Start Command: (lee de Procfile)

### Para Java Web Service
- Root Directory: `java/smarttask-web`
- Runtime: Java
- Build Command: `mvn clean package`
- Start Command: (lee de Procfile)

### Para Static Site
- Root Directory: `web/wallet2`
- Build Command: (dejar vacío)
- Publish Directory: `.` (punto)

---

## 🔍 VERIFICACIÓN FINAL

### Portfolio
- [ ] Se carga en GitHub Pages
- [ ] Todos los 8 proyectos visibles
- [ ] Links a GitHub funcionan
- [ ] Links a Render funcionan

### GitHub
- [ ] Repositorio público
- [ ] Todos los archivos visibles
- [ ] README.md se ve bien

### Render
- [ ] 7 servicios desplegados (sin unir-pdf)
- [ ] Ningún error 500
- [ ] Aplicaciones funcionan

---

## ⚠️ PROBLEMAS COMUNES

| Problema | Solución |
|----------|----------|
| GitHub Pages no carga | Esperar 2-3 min, verificar Settings |
| Procfile no funciona | Verificar formato y ubicación |
| Python: ModuleNotFoundError | Agregar dependencia a requirements.txt |
| Java: Build fail | Verificar pom.xml, ejecutar `mvn clean package` |
| Links portfolio muertos | Actualizar index.html, hacer push |
| Render: 500 error | Ver logs en Render Dashboard |

---

## 📞 ARCHIVOS DE AYUDA

| Archivo | Propósito |
|---------|-----------|
| CONFIGURACION_GITHUB_MAESTRO.md | Guía completa |
| generar_archivos_proyectos.sh | Script automático |
| CHECKLIST_VISUAL_DESPLIEGUE.md | Lista paso a paso |
| PLAN_MAESTRO_DESPLIEGUE_PORTAFOLIO.md | Plan detallado |
| RESUMEN_EJECUTIVO_Y_PROXIMOS_PASOS.txt | Este documento |
| TARJETA_REFERENCIA_RAPIDA.md | Esta tarjeta |

---

## 🎯 RESULTADO FINAL (≈4 horas)

```
✅ Portfolio profesional en GitHub Pages
✅ 8 proyectos en GitHub
✅ 7 demos en vivo en Render
✅ Todos los links funcionan
✅ Listo para compartir con empleadores
```

**Compartir:**
```
https://mbigliam.github.io/portafolio-2025/
```

---

## 🚀 ¡COMIENZA AHORA!

1. Descarga los archivos de `/mnt/user-data/outputs/`
2. Crea el repo en GitHub
3. Copia esta tarjeta y ten a mano
4. Sigue el CHECKLIST_VISUAL_DESPLIEGUE.md
5. ¡Éxito! 🎉
