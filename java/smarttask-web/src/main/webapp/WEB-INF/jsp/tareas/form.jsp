<%@ page contentType="text/html; charset=UTF-8" %>
<%@ page import="com.smarttask.model.Tarea" %>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulario de Tareas - SmartTask</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .navbar-custom { background: rgba(102, 126, 234, 0.95); box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }
        .form-container { background: white; border-radius: 10px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2); padding: 40px; margin: 30px auto; max-width: 600px; animation: slideUp 0.5s ease; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        .form-title { color: #333; font-weight: 700; margin-bottom: 30px; text-align: center; font-size: 1.8rem; }
        .form-group label { font-weight: 600; color: #555; margin-bottom: 10px; }
        .form-control, .form-select { border: 2px solid #e0e0e0; border-radius: 8px; padding: 10px 15px; font-size: 1rem; transition: all 0.3s ease; }
        .form-control:focus, .form-select:focus { border-color: #667eea; box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25); }
        .btn-submit { width: 100%; padding: 12px; font-size: 1.1rem; font-weight: 600; border: none; border-radius: 8px; margin-top: 20px; transition: all 0.3s ease; }
        .btn-submit-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .btn-submit-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4); color: white; }
        .btn-cancel { background: #e0e0e0; color: #333; }
        .btn-cancel:hover { background: #d0d0d0; color: #333; }
        .button-group { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 20px; }
        .form-icon { color: #667eea; margin-right: 8px; }
        .help-text { font-size: 0.85rem; color: #888; margin-top: 5px; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom">
        <div class="container-fluid">
            <a class="navbar-brand" href="/smarttask"><i class="fas fa-tasks"></i> SmartTask</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/smarttask/tareas"><i class="fas fa-list"></i> Mis Tareas</a></li>
                    <li class="nav-item"><a class="nav-link active" href="/smarttask/tareas/nuevo"><i class="fas fa-plus"></i> Crear Tarea</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="form-container">
        <%
            String modo = (String) request.getAttribute("modo");
            Tarea tarea = (Tarea) request.getAttribute("tarea");
            boolean esEdicion = "editar".equals(modo);
        %>

        <h1 class="form-title">
            <i class="form-icon fas fa-plus-circle"></i>
            <%= esEdicion ? "Editar Tarea" : "Crear Nueva Tarea" %>
        </h1>

        <% if (esEdicion && tarea != null) { %>
            <form action="/smarttask/tareas/actualizar/<%= tarea.getId() %>" method="post" id="tareaForm">
        <% } else { %>
            <form action="/smarttask/tareas/guardar" method="post" id="tareaForm">
        <% } %>

            <div class="form-group">
                <label for="nombre"><i class="form-icon fas fa-heading"></i> Nombre de la Tarea</label>
                <input type="text" class="form-control" id="nombre" name="nombre"
                       value="<%= tarea != null ? tarea.getNombre() : "" %>"
                       placeholder="Ingrese el nombre de la tarea" required maxlength="255">
                <div class="help-text">Máximo 255 caracteres</div>
            </div>

            <div class="form-group mt-4">
                <label for="prioridad"><i class="form-icon fas fa-star"></i> Prioridad</label>
                <select class="form-select" id="prioridad" name="prioridad" required>
                    <option value="" disabled>Seleccione una prioridad</option>
                    <option value="Baja" <%= tarea != null && "Baja".equals(tarea.getPrioridad()) ? "selected" : "" %>>Baja</option>
                    <option value="Media" <%= tarea != null && "Media".equals(tarea.getPrioridad()) ? "selected" : "" %>>Media</option>
                    <option value="Alta" <%= tarea != null && "Alta".equals(tarea.getPrioridad()) ? "selected" : "" %>>Alta</option>
                </select>
                <div class="help-text">Define la urgencia de la tarea</div>
            </div>

            <% if (!esEdicion) { %>
                <div class="form-group mt-4">
                    <label for="tipo"><i class="form-icon fas fa-tag"></i> Tipo de Tarea</label>
                    <select class="form-select" id="tipo" name="tipo" required>
                        <option value="" disabled selected>Seleccione un tipo</option>
                        <option value="normal">Tarea Normal</option>
                        <option value="urgente">Tarea Urgente</option>
                    </select>
                    <div class="help-text">Las tareas urgentes reciben un aviso especial</div>
                </div>
            <% } %>

            <div class="button-group">
                <button type="submit" class="btn btn-submit btn-submit-primary">
                    <i class="fas fa-save"></i>
                    <%= esEdicion ? "Guardar Cambios" : "Crear Tarea" %>
                </button>
                <a href="/smarttask/tareas" class="btn btn-submit btn-cancel">
                    <i class="fas fa-times"></i> Cancelar
                </a>
            </div>

        </form>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('tareaForm').addEventListener('submit', function(e) {
            const nombre = document.getElementById('nombre').value.trim();
            if (nombre.length === 0) {
                e.preventDefault();
                alert('Por favor, ingrese el nombre de la tarea.');
                document.getElementById('nombre').focus();
            }
        });
    </script>
</body>
</html>