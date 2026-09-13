# SmartTask - Aplicación Web de Gestión de Tareas

Una aplicación web moderna para gestión de tareas construida con **Spring Boot 3**, **Java 17**, **Maven**, **JSP** y **H2 Database**.

![Status](https://img.shields.io/badge/Status-Active-success)
![Java](https://img.shields.io/badge/Java-17-orange)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2.5-green)

## 🎯 Características

- ✨ **Crear Tareas**: Crea tareas normales o urgentes
- 📝 **Editar Tareas**: Modifica nombre y prioridad
- ✅ **Marcar Completas**: Marca tareas como completadas
- 🗑️ **Eliminar Tareas**: Borra tareas del sistema
- 📊 **Listar Tareas**: Visualiza todas tus tareas con estado
- 🏷️ **Tipos de Tareas**: Tareas normales y urgentes (herencia JPA)
- 🎨 **Interfaz Moderna**: Bootstrap 5 + Font Awesome + gradientes personalizados

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|------------|-----------|
| **Lenguaje** | Java 17 |
| **Framework** | Spring Boot 3.2.5 |
| **Build Tool** | Maven |
| **Web** | Spring MVC |
| **Persistence** | Spring Data JPA |
| **Database** | H2 (en memoria) |
| **View** | Jakarta EE 10 JSP |
| **Styling** | Bootstrap 5 + Font Awesome 6 |
| **Empaquetado** | WAR (Web Application Archive) |

## 📦 Requisitos Previos

Para ejecutar localmente:
- **Java 17** o superior
- **Maven 3.8.1** o superior
- **Eclipse IDE** (opcional, pero recomendado)

## 🚀 Ejecución Local

### 1. Clonar el Repositorio

```bash
git clone https://github.com/TU_USUARIO/smarttask-web.git
cd smarttask-web
```

### 2. Compilar con Maven

```bash
mvn clean package
```

### 3. Ejecutar la Aplicación

**Opción A: Con Maven**
```bash
mvn spring-boot:run
```

**Opción B: Con el JAR generado**
```bash
java -jar target/smarttask-web-1.0.0.war
```

**Opción C: En Eclipse (Recomendado)**
1. Click derecho en el proyecto
2. Selecciona **Run As** → **Spring Boot App**

### 4. Acceder a la Aplicación

Abre tu navegador y ve a:
```
http://localhost:8080/smarttask/
```

## 📂 Estructura del Proyecto

```
smarttask-web/
├── src/main/java/com/smarttask/
│   ├── model/
│   │   ├── Tarea.java              # Clase base abstracta
│   │   ├── TareaNormal.java        # Subtipo: Tarea Normal
│   │   └── TareaUrgente.java       # Subtipo: Tarea Urgente
│   ├── repository/
│   │   └── TareaRepository.java    # Acceso a datos JPA
│   ├── service/
│   │   └── TareaService.java       # Lógica de negocio
│   ├── controller/
│   │   ├── HomeController.java     # Controlador de inicio
│   │   └── TareaController.java    # Controlador de tareas
│   └── SmartTaskWebApplication.java
├── src/main/webapp/WEB-INF/jsp/
│   ├── index.jsp                   # Página de inicio
│   └── tareas/
│       ├── form.jsp                # Formulario crear/editar
│       └── lista.jsp               # Listado de tareas
├── src/main/resources/
│   └── application.properties      # Configuración Spring
├── pom.xml                         # Configuración Maven
├── Procfile                        # Configuración para Render
└── .gitignore                      # Archivos a ignorar en Git
```

## 🗄️ Modelo de Datos

### Clase Base: `Tarea`
```
- id: Long (Primary Key)
- nombre: String (255 caracteres)
- prioridad: String (Baja, Media, Alta)
- completada: boolean
- tipo_tarea: String (discriminador - NORMAL, URGENTE)
```

### Herencia JPA (Single Table)
```
Tarea (abstracta)
├── TareaNormal    (@DiscriminatorValue = "NORMAL")
└── TareaUrgente   (@DiscriminatorValue = "URGENTE")
```

## 🔌 Endpoints API

| Método | URL | Descripción |
|--------|-----|------------|
| GET | `/smarttask/` | Página de inicio |
| GET | `/smarttask/tareas` | Listar todas las tareas |
| GET | `/smarttask/tareas/nuevo` | Formulario crear tarea |
| POST | `/smarttask/tareas/guardar` | Guardar nueva tarea |
| GET | `/smarttask/tareas/editar/{id}` | Formulario editar tarea |
| POST | `/smarttask/tareas/actualizar/{id}` | Actualizar tarea |
| GET | `/smarttask/tareas/completar/{id}` | Marcar como completada |
| GET | `/smarttask/tareas/eliminar/{id}` | Eliminar tarea |

## 🌐 Despliegue en Render.com

Para desplegar en producción usando Render.com, consulta la guía detallada:

📖 **[RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md)**

**Quick Start:**
1. Push el código a GitHub
2. Ve a [Render Dashboard](https://dashboard.render.com/)
3. Crea un nuevo "Web Service"
4. Conecta tu repositorio GitHub
5. Render detectará automáticamente el `Procfile`
6. ¡Listo! Tu aplicación estará en vivo

**URL de demo:** `https://smarttask-web.onrender.com/smarttask/`

## ⚙️ Configuración

### `application.properties`

```properties
# Servidor
server.port=${PORT:8080}                    # Puerto (Render lo asigna)
server.servlet.context-path=/smarttask      # Ruta base de la app

# Vistas JSP
spring.mvc.view.prefix=/WEB-INF/jsp/
spring.mvc.view.suffix=.jsp

# Base de Datos H2
spring.datasource.url=jdbc:h2:mem:testdb
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.jpa.hibernate.ddl-auto=create-drop  # Crea tablas automáticamente

# Consola H2 (para desarrollo)
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console
```

## 🐛 Solución de Problemas

### Error: "Port already in use"
```bash
# Cambiar puerto en local
mvn spring-boot:run -Dspring-boot.run.arguments="--server.port=9090"
```

### Error: "No se ve la página"
- Verifica que accedas a `http://localhost:8080/smarttask/`
- No olvides el context path `/smarttask`

### Logs de H2 Console
```
http://localhost:8080/smarttask/h2-console
```
Usuario: `sa`
Contraseña: (vacía)

## 📚 Documentación Adicional

- [Spring Boot Docs](https://spring.io/projects/spring-boot)
- [Spring Data JPA](https://spring.io/projects/spring-data-jpa)
- [Jakarta EE 10](https://jakarta.ee/)
- [H2 Database](http://www.h2database.com)

## 👤 Autor

- **Mauricio** - mauriciobigliam@gmail.com

## 📄 Licencia

Este proyecto está bajo licencia MIT. Siéntete libre de usar, modificar y distribuir.

## 🤝 Contribuciones

¿Tienes ideas para mejorar SmartTask? ¡Abre un issue o un pull request!

---

**¿Preguntas? Consulta la guía de despliegue en [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md)** 🚀
