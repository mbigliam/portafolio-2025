// ==========================================
// CONFIGURACIÓN INICIAL
// ==========================================
$(document).ready(function() {
    
    // ==========================================
    // CARRUSEL CONFIGURATION
    // ==========================================
    $("#carouselExampleSlidesOnly").carousel({
        interval: 5000, // Cambia cada 5 segundos
        ride: "carousel",
        wrap: true,
        pause: "hover"
    });
    
    // ==========================================
    // NAVBAR SCROLL EFFECT
    // ==========================================
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('#navhijo').addClass('scrolled');
        } else {
            $('#navhijo').removeClass('scrolled');
        }
    });
    
    // ==========================================
    // SMOOTH SCROLL PARA ENLACES
    // ==========================================
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        
        if (target.length) {
            event.preventDefault();
            
            var targetPosition = target.offset().top - 80;
            
            $('html, body').stop().animate({
                scrollTop: targetPosition
            }, 1000, 'swing');
        }
    });
    
    // ==========================================
    // BACK TO TOP BUTTON
    // ==========================================
    $(window).scroll(function() {
        if ($(this).scrollTop() > 500) {
            $('#backToTop').addClass('show');
        } else {
            $('#backToTop').removeClass('show');
        }
    });
    
    $('#backToTop').on('click', function() {
        $('html, body').stop().animate({
            scrollTop: 0
        }, 1000, 'swing');
    });
    
    // ==========================================
    // FORMULARIO CON SWEETALERT2
    // ==========================================
    $('#contactForm').on('submit', function(e) {
        e.preventDefault();
        
        var nombre = $('#nombre').val().trim();
        var email = $('#email').val().trim();
        var asunto = $('#asunto').val().trim();
        var mensaje = $('#mensaje').val().trim();
        
        // Validación
        if (!nombre || !email || !asunto || !mensaje) {
            Swal.fire({
                title: "Campos incompletos",
                text: "Por favor completa todos los campos",
                icon: "warning",
                confirmButtonColor: "#3fb7fd",
                confirmButtonText: "Aceptar"
            });
            return;
        }
        
        // Mostrar alerta de éxito
        Swal.fire({
            title: "¡Mensaje Enviado!",
            html: `
                <img src="assets/img/viajes.svg" alt="Viajes Chile" width="60px" class="mb-3"><br>
                <div class="text-start mt-3">
                    <b>Nombre:</b> ${nombre}<br>
                    <b>Email:</b> ${email}<br>
                    <b>Asunto:</b> ${asunto}<br>
                    <b>Mensaje:</b> ${mensaje.substring(0, 100)}${mensaje.length > 100 ? '...' : ''}
                </div>
            `,
            icon: "success",
            confirmButtonColor: "#3fb7fd",
            confirmButtonText: "¡Genial!",
            backdrop: `
                rgba(0,0,0,0.7)
                left top
                no-repeat
            `
        });
        
        // Limpiar formulario
        this.reset();
    });
    
    // ==========================================
    // ANIMACIONES AL SCROLL
    // ==========================================
    $(window).on('scroll', function() {
        var windowHeight = $(window).height();
        var scrollTop = $(this).scrollTop();
        
        $('.card, .section-title').each(function() {
            var elementTop = $(this).offset().top;
            var elementBottom = elementTop + $(this).outerHeight();
            
            if (elementBottom > scrollTop && elementTop < scrollTop + windowHeight) {
                $(this).css({
                    'opacity': '1',
                    'transform': 'translateY(0)'
                });
            }
        });
    });
    
    // Inicializar cards con opacidad 0
    $('.card, .section-title').css({
        'opacity': '0',
        'transform': 'translateY(30px)',
        'transition': 'all 0.6s ease'
    });
});