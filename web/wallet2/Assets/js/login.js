$(document).ready(function() {

  // ==========================================
  // 1. PANTALLA DE LOGIN
  //
  // ==========================================
  if ($('#loginForm').length > 0) {
    $('#loginForm').submit(function(event) {
      event.preventDefault();
      
      // El .trim() elimina espacios vacíos al inicio o final
      var username = $('#email').val().trim(); 
      var password = $('#password').val().trim();
    
      if (username.includes('admin@ad') && password === 'admin') {
        $('#alert-container').html('<div class="alert alert-success">¡Inicio de sesión exitoso! Ingresando...</div>');
        
        setTimeout(function() {
          window.location.href = 'menu.html';
        }, 1500);
      } else {
        $('#alert-container').html('<div class="alert alert-danger">Usuario o contraseña inválido. Inténtalo de nuevo.</div>');
      }
    });
  }
}); 

