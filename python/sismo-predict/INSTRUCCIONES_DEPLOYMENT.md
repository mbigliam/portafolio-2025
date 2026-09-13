# 🚀 Instrucciones de Deployment - Sismo Predict

## ✅ Lo que ya está hecho

He creado exitosamente:

1. **Procfile** - Configuración para Railway con uvicorn
2. **requirements.txt actualizado** - Con todas las dependencias necesarias (FastAPI, uvicorn, etc.)
3. **Commit en Git** - Los cambios están listos para push

## 📝 Cambios realizados

### Procfile (NUEVO)
```
web: python -m uvicorn api:app --host 0.0.0.0 --port $PORT
```

### requirements.txt (ACTUALIZADO)
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
requests>=2.25.0
numpy>=1.20.0
pandas>=1.2.0
sgp4>=2.20
python-multipart>=0.0.5
```

## 🔧 Pasos para completar el deployment

### Opción 1: Desde tu máquina local (RECOMENDADO)

1. **Abre una terminal/PowerShell en tu máquina**

2. **Navega al repositorio:**
```powershell
cd C:\Users\Mbiglia\REPOSITORIO
# o donde tengas clonado el repositorio
```

3. **Clona o actualiza el repositorio:**
```powershell
# Si aún no está clonado:
git clone https://github.com/mbigliam/portafolio-2025.git
cd portafolio-2025

# Si ya está clonado:
cd portafolio-2025
git pull origin main
```

4. **Copia los archivos en `python/sismo-predict/`:**
   - Copia el archivo `Procfile` a `python/sismo-predict/Procfile`
   - Copia el contenido del `requirements.txt` a `python/sismo-predict/requirements.txt`

5. **Verifica los cambios:**
```powershell
git status
```
Deberías ver dos archivos modificados/nuevos.

6. **Haz el commit (si aún no está):**
```powershell
git add python/sismo-predict/Procfile python/sismo-predict/requirements.txt
git commit -m "Add Procfile and update requirements.txt with FastAPI and Uvicorn

- Create Procfile for Railway deployment with uvicorn server configuration
- Update requirements.txt with FastAPI, uvicorn, and python-multipart dependencies
- Ensure all API dependencies are properly declared for production deployment"
```

7. **Push a GitHub:**
```powershell
git push origin main
```

### Opción 2: A través de GitHub Web

1. Ve a https://github.com/mbigliam/portafolio-2025
2. Crea los archivos directamente desde la web interface
3. O abre un Pull Request con los cambios

---

## ⚡ Después del push

Una vez que hagas push:

1. **Railway detectará automáticamente los cambios**
2. **Se iniciará un nuevo deployment** con:
   - FastAPI y uvicorn configurados correctamente
   - Todas las dependencias necesarias instaladas
   - El Procfile indicando cómo iniciar la aplicación

3. **Verifica el deployment** en tu panel de Railway:
   - Proyecto: `lucid-freedom`
   - Servicio: `portafolio-2025`
   - Dirección raíz: `python/sismo-predict/`

---

## 📋 Resumen del cambio

| Archivo | Cambio | Razón |
|---------|--------|-------|
| **Procfile** | ✨ NUEVO | Define cómo Railway inicia la aplicación con uvicorn |
| **requirements.txt** | 🔄 ACTUALIZADO | Agregadas FastAPI y uvicorn que faltaban |

---

## ✅ Verificación

Después del deployment, accede a tu aplicación en:
- `https://portafolio-2025-production-22d2.up.railway.app`

¡Y listo! Tu sismo-predict API estará desplegada en Railway. 🎉
