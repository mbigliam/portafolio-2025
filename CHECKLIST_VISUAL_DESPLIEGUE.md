# ✅ CHECKLIST VISUAL - Despliegue del Portafolio

## 🎯 OBJETIVO FINAL
```
✨ Portfolio en GitHub Pages
   ↓
   Muestra 8 proyectos
   ↓
   Cada proyecto tiene:
   - Link a GitHub (código fuente)
   - Link a Render (demo en vivo)
```

---

## 📋 FASE 1: PREPARACIÓN (Hoy)

### A. Archivo HTML del Portfolio ✅
- [ ] Descarga `index_ACTUALIZADO.html`
- [ ] Renómbralo a `index.html`
- [ ] Verifica los 8 proyectos estén completos
- [ ] Comprueba que todos los links sean correctos

**Ubicación:** `/mnt/user-data/outputs/index_ACTUALIZADO.html`

---

### B. Archivos de Configuración ✅
- [ ] Descarga `generar_archivos_proyectos.sh`
- [ ] Descarga `CONFIGURACION_GITHUB_MAESTRO.md`
- [ ] Lee la guía maestro

**Ubicación:** `/mnt/user-data/outputs/`

---

## 🚀 FASE 2: CREAR REPOSITORIO EN GITHUB (1 hora)

### PASO 1: Crear Repositorio
```
1. Ve a https://github.com/mbigliam
2. Haz click en "New Repository"
3. Nombre: portafolio-2025
4. Descripción: Portafolio profesional con 8 proyectos
5. Selecciona: Public
6. .gitignore: None (lo crearemos)
7. Haz click en "Create repository"
```

**Resultado esperado:**
```
https://github.com/mbigliam/portafolio-2025
```

- [ ] Repositorio creado en GitHub

### PASO 2: Clonar Repositorio
```bash
cd C:\Users\Mbiglia\Documents  # o donde guardes proyectos
git clone https://github.com/mbigliam/portafolio-2025.git
cd portafolio-2025
```

- [ ] Repositorio clonado localmente

### PASO 3: Crear Estructura de Carpetas
```bash
# En PowerShell (Windows)
mkdir java, python, web
mkdir java\smarttask-web
mkdir java\biblioteca-untec
mkdir python\jarvis
mkdir python\sismo-predict
mkdir python\unir-pdf
mkdir web\wallet2
mkdir web\meet-coffe
mkdir web\viajes-chile
```

- [ ] Carpetas creadas

---

## 📁 FASE 3: AGREGAR ARCHIVOS DE CONFIGURACIÓN (2 horas)

### PASO 4: Usar el Script Generador

**Opción A: En Linux/Mac**
```bash
chmod +x generar_archivos_proyectos.sh
./generar_archivos_proyectos.sh /ruta/a/portafolio-2025
```

**Opción B: Manual (Windows)**

Copia manualmente cada archivo desde `CONFIGURACION_GITHUB_MAESTRO.md` según el proyecto.

- [ ] Todos los `requirements.txt` creados (Python)
- [ ] Todos los `Procfile` creados
- [ ] Todos los `.gitignore` creados
- [ ] Todos los `README.md` creados

### Checklist por Proyecto:

#### Python/JARVIS
- [ ] `requirements.txt`
- [ ] `Procfile`
- [ ] `.gitignore`
- [ ] `README.md`

#### Python/SISMO-PREDICT
- [ ] `requirements.txt`
- [ ] `Procfile`
- [ ] `.gitignore`
- [ ] `README.md`

#### Python/UNIR-PDF
- [ ] `.gitignore`
- [ ] `README.md`

#### Java/SmartTask-Web
- [ ] `Procfile` (ya debe existir)
- [ ] `.gitignore` (ya debe existir)
- [ ] `README.md`
- [ ] `pom.xml` (ya debe existir)

#### Java/BibliotecaUNTEC
- [ ] Descomprimir `BibliotecaUNTEC.zip`
- [ ] `Procfile`
- [ ] `.gitignore`
- [ ] `README.md`
- [ ] `pom.xml`

#### Web/Wallet2
- [ ] `.gitignore`
- [ ] `README.md`

#### Web/Meet-Coffe
- [ ] `.gitignore`
- [ ] `README.md`

#### Web/Viajes-Chile
- [ ] `.gitignore`
- [ ] `README.md`

---

## 🌐 FASE 4: AGREGAR ARCHIVOS DEL PORTFOLIO (1 hora)

### PASO 5: Copiar Archivos del Portfolio
```
Desde: C:\Users\Mbiglia\Pictures\mauricio_biglia_portfolio
Hacia: portafolio-2025\ (raíz del repositorio)
```

**Archivos a copiar:**
- [ ] `index.html` (renombrado de index_ACTUALIZADO.html)
- [ ] `assets/css/style.css`
- [ ] `assets/js/script.js`
- [ ] `assets/img/yo.png`
- [ ] `CV_2026_2_MauricioFernando_BigliaMaldonado.pdf`
- [ ] `README.md` (maestro)

**Estructura final:**
```
portafolio-2025/
├── index.html                    ← Portfolio principal
├── README.md                     ← Índice maestro
├── assets/
│   ├── css/
│   ├── js/
│   └── img/
├── CV_2026_2_MauricioFernando_BigliaMaldonado.pdf
├── .gitignore                    ← Global
├── java/
├── python/
└── web/
```

---

## 📤 FASE 5: PRIMER PUSH A GITHUB (30 min)

### PASO 6: Verificar Estado
```bash
cd portafolio-2025
git status
```

Deberías ver todos los archivos nuevos en rojo.

- [ ] `git status` muestra todos los archivos

### PASO 7: Agregar y Hacer Commit
```bash
git add .
git commit -m "Initial commit: Portfolio structure with 8 projects

- Added main portfolio (index.html)
- Configured Python projects (JARVIS, SISMO-PREDICT, UNIR-PDF)
- Configured Java projects (SmartTask-Web, BibliotecaUNTEC)
- Added web projects (Wallet2, Meet-Coffe, Viajes-Chile)
- All projects with README.md, requirements.txt, Procfile, .gitignore"
```

- [ ] Commit creado

### PASO 8: Push
```bash
git push -u origin main
```

- [ ] Push exitoso

### PASO 9: Verificar en GitHub
```
Ve a: https://github.com/mbigliam/portafolio-2025
Deberías ver todos los archivos y carpetas
```

- [ ] Repositorio visible en GitHub con toda la estructura

---

## 🎯 FASE 6: CONFIGURAR GITHUB PAGES (30 min)

### PASO 10: Habilitar GitHub Pages
```
1. Ve a: https://github.com/mbigliam/portafolio-2025/settings
2. En el menú izquierdo: "Pages"
3. En "Source", selecciona: "Deploy from a branch"
4. Branch: "main" | Folder: "/ (root)"
5. Haz click en "Save"
```

- [ ] GitHub Pages habilitado

### PASO 11: Verificar Portfolio en GitHub Pages
```
Tu portfolio estará disponible en:
https://mbigliam.github.io/portafolio-2025/

(Espera 2-3 minutos para que se depliegue)
```

- [ ] Portfolio accesible en GitHub Pages

---

## 🚀 FASE 7: DESPLEGAR EN RENDER (1-2 horas)

### PASO 12: Crear Servicio en Render para Cada Proyecto

Repite estos pasos para CADA proyecto deployable:

#### Para Proyectos Python (JARVIS, SISMO-PREDICT):
```
1. Ve a https://dashboard.render.com/
2. Haz click en "New +"
3. Selecciona "Web Service"
4. Conecta tu repositorio GitHub
5. Nombre del Servicio: jarvis-app (o sismo-predict)
6. Root Directory: python/jarvis (o python/sismo-predict)
7. Runtime: Python 3
8. Build Command: pip install -r requirements.txt
9. Start Command: Render lo lee de Procfile
10. Plan: Free
11. Haz click en "Create Web Service"
```

- [ ] JARVIS desplegado en Render
- [ ] SISMO-PREDICT desplegado en Render

#### Para Proyectos Java (SmartTask-Web, BibliotecaUNTEC):
```
1. Ve a https://dashboard.render.com/
2. Haz click en "New +"
3. Selecciona "Web Service"
4. Conecta tu repositorio GitHub
5. Nombre del Servicio: smarttask-web
6. Root Directory: java/smarttask-web
7. Runtime: Java
8. Build Command: mvn clean package
9. Start Command: Render lo lee de Procfile
10. Plan: Free
11. Haz click en "Create Web Service"
```

- [ ] SmartTask-Web desplegado en Render
- [ ] BibliotecaUNTEC desplegado en Render

#### Para Proyectos Web (Wallet2, Meet-Coffe, Viajes-Chile):
```
1. Ve a https://dashboard.render.com/
2. Haz click en "New +"
3. Selecciona "Static Site"
4. Conecta tu repositorio GitHub
5. Nombre del Sitio: wallet2 (o meet-coffe, viajes-chile)
6. Root Directory: web/wallet2 (o web/meet-coffe, etc)
7. Build Command: (dejar en blanco)
8. Publish Directory: . (punto - para raíz de la carpeta)
9. Plan: Free
10. Haz click en "Create Static Site"
```

- [ ] Wallet2 desplegado en Render
- [ ] Meet-Coffe desplegado en Render
- [ ] Viajes-Chile desplegado en Render

### PASO 13: Obtener URLs de Render
```
Después de cada despliegue, Render te dará una URL:
- JARVIS: https://jarvis-app.onrender.com
- SISMO-PREDICT: https://sismo-predict.onrender.com
- SmartTask-Web: https://smarttask-web.onrender.com
- BibliotecaUNTEC: https://biblioteca-untec.onrender.com
- Wallet2: https://wallet2.onrender.com
- Meet-Coffe: https://meet-coffe.onrender.com
- Viajes-Chile: https://viajes-chile.onrender.com
```

- [ ] Todas las URLs de Render obtenidas

### PASO 14: Actualizar index.html (si es necesario)
Si las URLs en `index.html` no son correctas, actualízalas con las URLs reales de Render.

- [ ] index.html actualizado con URLs reales
- [ ] Haz push: `git add . && git commit -m "Update: Render URLs" && git push`

---

## ✨ FASE 8: PRUEBAS FINALES (1 hora)

### PASO 15: Verificar Todo Funciona

#### Portfolio en GitHub Pages
- [ ] `https://mbigliam.github.io/portafolio-2025/` carga correctamente
- [ ] Todos los 8 proyectos se ven en la sección "Projects"
- [ ] Los botones funcionan

#### GitHub Repository Links
Para cada proyecto, verifica:
- [ ] El link a GitHub apunta al repositorio correcto
- [ ] El código fuente está visible en GitHub

#### Render Demo Links
Para cada proyecto deployable, verifica:
- [ ] El link a Render carga la aplicación
- [ ] La aplicación funciona correctamente
- [ ] No hay errores 500

**Checklist de Links:**
- [ ] SmartTask-Web: GitHub ✅ | Demo ✅
- [ ] BibliotecaUNTEC: GitHub ✅ | Demo ✅
- [ ] JARVIS: GitHub ✅ | Demo ✅
- [ ] SISMO-PREDICT: GitHub ✅ | Demo ✅
- [ ] UNIR-PDF: GitHub ✅ | (Desktop app)
- [ ] Wallet2: GitHub ✅ | Demo ✅
- [ ] Meet-Coffe: GitHub ✅ | Demo ✅
- [ ] Viajes-Chile: GitHub ✅ | Demo ✅

---

## 🎉 ¡LISTO PARA CONTRATAR!

### Checklist Final
- [ ] Repositorio `portafolio-2025` creado en GitHub
- [ ] Portfolio visible en `https://mbigliam.github.io/portafolio-2025/`
- [ ] Todos los 8 proyectos desplegados en Render
- [ ] Todos los links funcionan
- [ ] CV descargable desde el portfolio
- [ ] Información de contacto actualizada

### Compartir Con Empleadores
```
🎯 Tu Portafolio Profesional:
   https://mbigliam.github.io/portafolio-2025/

📂 Código Fuente:
   https://github.com/mbigliam/portafolio-2025

👨‍💼 LinkedIn: [Tu Perfil]

📧 Email: mauriciobigliam@gmail.com
```

---

## 📞 SOPORTE

Si algo no funciona:
1. Verifica el archivo `CONFIGURACION_GITHUB_MAESTRO.md`
2. Revisa los logs en Render Dashboard
3. Asegúrate de que los archivos `Procfile` son correctos
4. Verifica que `requirements.txt` tiene todas las dependencias

¡Éxito! 🚀
