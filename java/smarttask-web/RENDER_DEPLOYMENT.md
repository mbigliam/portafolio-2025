# Guía de Despliegue en Render.com - SmartTask

## 📋 Requisitos Previos

1. ✅ Repositorio GitHub con tu proyecto (pushear todo el código)
2. ✅ Cuenta activa en [Render.com](https://dashboard.render.com/)
3. ✅ La aplicación funciona correctamente en local

## 🚀 Paso a Paso para Desplegar

### 1️⃣ Preparar tu Repositorio GitHub

Asegúrate de que todos los archivos estén en GitHub:

```bash
# En la raíz de tu proyecto, verifica que git está inicializado
git status

# Si no está inicializado:
git init
git add .
git commit -m "Initial commit: SmartTask Spring Boot application"
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git push -u origin main
```

**Archivos críticos que deben estar en el repositorio:**
- ✅ `pom.xml` (Maven configuration)
- ✅ `Procfile` (Render configuration)
- ✅ `.gitignore` (para no subir target/ ni .settings/)
- ✅ `src/` (todo el código fuente)
- ✅ `src/main/resources/application.properties`
- ✅ `src/main/webapp/WEB-INF/jsp/` (vistas JSP)

### 2️⃣ Crear el Servicio en Render

1. **Entra a [Render Dashboard](https://dashboard.render.com/)**
2. **Haz clic en "New +"** en la esquina superior derecha
3. **Selecciona "Web Service"**
4. **Conecta tu repositorio GitHub:**
   - Selecciona "GitHub"
   - Autoriza Render para acceder a tu cuenta de GitHub
   - Selecciona tu repositorio `smarttask-web` (o como lo llamaste)
   - Selecciona la rama `main`

### 3️⃣ Configurar el Servicio

**Nombre del Servicio:**
```
smarttask-web
```

**Región:**
```
Selecciona la más cercana a tus usuarios (ej: Frankfurt para Europa, Ohio para USA)
```

**Rama:**
```
main
```

**Runtime:**
```
Docker (seleccionado automáticamente)
```

**Build Command:**
```bash
mvn clean package -DskipTests
```

**Start Command:**
```bash
Render debería detectar automáticamente el Procfile. Si no, usa:
java -jar -Dserver.port=$PORT target/smarttask-web-1.0.0.war
```

### 4️⃣ Configurar Variables de Entorno (Opcional)

Si deseas agregar variables personalizadas:
1. Desplázate hasta **Environment**
2. Haz clic en **Add Environment Variable**

Ejemplo (esto ya está configurado, pero puedes revisar):
```
PORT = 10000 (Render lo asigna automáticamente)
```

### 5️⃣ Configurar Instancia y Recursos

- **Instance Type:** Selecciona el plan gratuito o el que prefieras
- **Auto-deploy:** Activa esta opción para que se redeploy automáticamente cuando hagas push a GitHub

### 6️⃣ Completar el Despliegue

1. Haz clic en **Create Web Service**
2. Render comenzará a:
   - Clonar tu repositorio
   - Ejecutar `mvn clean package -DskipTests`
   - Construir la aplicación
   - Desplegar el WAR

## 📊 Monitorear el Despliegue

1. Ve a tu servicio en el dashboard
2. En la sección **Logs**, verás el progreso en tiempo real:
   - ✅ "Building..."
   - ✅ "Deploying..."
   - ✅ "Live" (cuando esté listo)

**El URL será algo como:**
```
https://smarttask-web.onrender.com
```

## 🧪 Verificar que Funciona

Una vez que Render diga "Live", accede a:

```
https://smarttask-web.onrender.com/smarttask/
```

Deberías ver:
- ✅ La página de inicio de SmartTask
- ✅ Botones para "Mis Tareas" y "Crear Tarea"
- ✅ Funcionamiento completo CRUD

## 🔧 Solucionar Problemas

### Problema: "Build failed"
**Solución:**
- Verifica que `pom.xml` tenga todas las dependencias correctas
- Revisa los logs: compila localmente con `mvn clean package` para ver errores

### Problema: "Application crashed"
**Solución:**
- Haz clic en **Logs** en el dashboard
- Busca mensajes de error
- Common issues:
  - Puerto no disponible (ya está usando $PORT)
  - Falta de dependencia en `pom.xml`
  - Error en JSP

### Problema: "503 Service Unavailable"
**Solución:**
- El servicio aún está iniciando (espera 2-3 minutos)
- Verifica en **Logs** que Spring Boot haya iniciado correctamente
- Debe mostrar: "Tomcat started on port..."

## 📝 Próximas Mejoras (Opcional)

### 1. Base de datos persistente
Actualmente H2 usa memoria (se borra al reiniciar). Para persistencia:

```properties
# Cambiar en application.properties:
spring.datasource.url=jdbc:h2:file:./data/smarttask
spring.jpa.hibernate.ddl-auto=update
```

### 2. Usar PostgreSQL en lugar de H2
Si quieres una BD real:
- En Render, crea un servicio PostgreSQL
- Agrega a `pom.xml`:
```xml
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
</dependency>
```
- Configura `application.properties` con las credenciales

## ✅ Checklist Final

- [ ] Repositorio GitHub con todos los archivos
- [ ] `.gitignore` presente (no subas `/target`)
- [ ] `Procfile` presente en la raíz
- [ ] `pom.xml` con `<packaging>war</packaging>`
- [ ] `application.properties` con `server.port=${PORT:8080}`
- [ ] Cuenta Render.com activa
- [ ] Conectaste el repositorio GitHub a Render
- [ ] Despliegue completado y servicio marcado como "Live"
- [ ] URL accesible y aplicación funcionando

---

¿Alguna duda en algún paso? 🚀
