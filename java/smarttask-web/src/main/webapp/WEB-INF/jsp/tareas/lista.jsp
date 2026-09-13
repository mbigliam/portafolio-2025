<%@ page contentType="text/html; charset=UTF-8" %>
<%@ page import="java.util.List" %>
<%@ page import="com.smarttask.model.Tarea" %>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de Tareas - SmartTask</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .navbar-custom { background: rgba(102, 126, 234, 0.95); box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }
        .container-custom { background: white; border-radius: 10px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2); padding: 30px; margin: 30px auto; max-width: 1000px; }
        .badge-urgente { background-color: #dc3545; font-size: 0.85rem; }
        .badge-normal { background-color: #6c757d; font-size: 0.85rem; }
        .badge-completada { background-color: #28a745; font-size: 0.85rem; }
        .badge-pendiente { background-color: #ffc107; color: black; font-size: 0.85rem; }
        .btn-action { font-size: 0.9rem; padding: 5px 10px; margin: 2px; }
        .empty-state { text-align: center; padding: 60px 20px; color: #999; }
        .empty-state i { font-size: 4rem; margin-bottom: 20px; color: #ddd; }
        h1 { color: #333; font-weight: 700; margin-bottom: 30px; }
        .prioridad { font-weight: 600; }
        .prioridad.alta { color: #dc3545; }
        .prioridad.media { color: #ffc107; }
        .prioridad.baja { color: #28a745; }
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
                    <li class="nav-item"><a class="nav-link active" href="/smarttask/tareas"><i class="fas fa-list"></i> Mis Tareas</a></li>
                    <li class="nav-item"><a class="nav-link" href="/smarttask/tareas/nuevo"><i class="fas fa-plus"></i> Crear Tarea</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container-custom">
        <% if (request.getAttribute("success") != null) { %>
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                <i class="fas fa-check-circle"></i> <%= request.getAttribute("success") %>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        <% } %>

        <% if (request.getAttribute("error") != null) { %>
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="fas fa-exclamation-circle"></i> <%= request.getAttribute("error") %>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        <% } %>

        <h1><i class="fas fa-list-check"></i> Mis Tareas</h1>

        <%
            List<Tarea> tareas = (List<Tarea>) request.getAttribute("tareas");
            if (tareas == null || tareas.isEmpty()) {
        %>
            <div class="empty-state">
                <i class="fas fa-inbox"></i>
                <h3>No hay tareas registradas</h3>
                <p>¡Crea tu primera tarea para comenzar!</p>
                <a href="/smarttask/tareas/nuevo" class="btn btn-primary mt-3"><i class="fas fa-plus"></i> Crear Tarea</a>
            </div>
        <% } else { %>
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-light">
                        <tr>
                            <th><i class="fas fa-hashtag"></i> ID</th>
                            <th><i class="fas fa-tasks"></i> Tarea</th>
                            <th><i class="fas fa-tag"></i> Tipo</th>
                            <th><i class="fas fa-star"></i> Prioridad</th>
                            <th><i class="fas fa-check"></i> Estado</th>
                            <th><i class="fas fa-cog"></i> Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <% for (Tarea tarea : tareas) { %>
                            <tr>
                                <td><strong><%= tarea.getId() %></strong></td>
                                <td><%= tarea.getNombre() %></td>
                                <td>
                                    <% if ("URGENTE".equals(tarea.getTipo())) { %>
                                        <span class="badge badge-urgente">⚠️ URGENTE</span>
                                    <% } else { %>
                                        <span class="badge badge-normal">✓ NORMAL</span>
                                    <% } %>
                                </td>
                                <td>
                                    <span class="prioridad <%= tarea.getPrioridad().toLowerCase() %>">
                                        <%= tarea.getPrioridad() %>
                                    </span>
                                </td>
                                <td>
                                    <% if (tarea.isCompletada()) { %>
                                        <span class="badge badge-completada">✓ Completada</span>
                                    <% } else { %>
                                        <span class="badge badge-pendiente">⏳ Pendiente</span>
                                    <% } %>
                                </td>
                                <td>
                                    <% if (!tarea.isCompletada()) { %>
                                        <a href="/smarttask/tareas/completar/<%= tarea.getId() %>" class="btn btn-sm btn-success btn-action" title="Marcar como completada">
                                            <i class="fas fa-check"></i>
                                        </a>
                                    <% } %>
                                    <a href="/smarttask/tareas/editar/<%= tarea.getId() %>" class="btn btn-sm btn-warning btn-action" title="Editar tarea">
                                        <i class="fas fa-edit"></i>
                                    </a>
                                    <a href="/smarttask/tareas/eliminar/<%= tarea.getId() %>" class="btn btn-sm btn-danger btn-action" onclick="return confirm('¿Está seguro?')" title="Eliminar tarea">
                                        <i class="fas fa-trash"></i>
                                    </a>
                                </td>
                            </tr>
                        <% } %>
                    </tbody>
                </table>
            </div>
        <% } %>

        <div class="mt-4 pt-4 border-top text-center">
            <a href="/smarttask" class="btn btn-outline-secondary"><i class="fas fa-home"></i> Volver al Inicio</a>
            <a href="/smarttask/tareas/nuevo" class="btn btn-primary"><i class="fas fa-plus"></i> Nueva Tarea</a>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>