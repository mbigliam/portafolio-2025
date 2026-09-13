<%@ page contentType="text/html; charset=UTF-8" %>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartTask - Gestor de Tareas</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .hero-container { text-align: center; color: white; max-width: 600px; animation: fadeIn 0.8s ease-in; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .hero-container h1 { font-size: 3.5rem; font-weight: 700; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
        .hero-container p { font-size: 1.3rem; margin-bottom: 40px; opacity: 0.95; }
        .btn-custom { padding: 12px 30px; font-size: 1.1rem; font-weight: 600; border: none; border-radius: 50px; transition: all 0.3s ease; margin: 10px; text-decoration: none; display: inline-block; cursor: pointer; }
        .btn-primary-custom { background-color: rgba(255, 255, 255, 0.9); color: #667eea; }
        .btn-primary-custom:hover { background-color: white; transform: translateY(-2px); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2); color: #667eea; }
        .btn-secondary-custom { background-color: rgba(255, 255, 255, 0.2); color: white; border: 2px solid white; }
        .btn-secondary-custom:hover { background-color: rgba(255, 255, 255, 0.3); transform: translateY(-2px); color: white; }
        .icon-large { font-size: 4rem; margin-bottom: 20px; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.8; } }
    </style>
</head>
<body>
    <div class="hero-container">
        <i class="fas fa-tasks icon-large"></i>
        <h1>SmartTask</h1>
        <p>Gestor inteligente de tareas con Spring Boot 3</p>
        <div class="mt-4">
            <a href="/smarttask/tareas" class="btn btn-custom btn-primary-custom"><i class="fas fa-list"></i> Ver Tareas</a>
            <a href="/smarttask/tareas/nuevo" class="btn btn-custom btn-secondary-custom"><i class="fas fa-plus"></i> Crear Tarea</a>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>