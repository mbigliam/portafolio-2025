/* ============================================
   PORTAFOLIO MAURICIO BIGLIA - SCRIPT PRINCIPAL
   Efectos: Canvas Partículas, Typing, Scroll, jQuery
   ============================================ */

$(document).ready(function () {

    /* ==========================================
       1. PRELOADER
       ========================================== */
    $(window).on('load', function () {
        setTimeout(function () {
            $('#preloader').addClass('hidden');
        }, 2000);
    });

    /* ==========================================
       2. CANVAS DE PARTÍCULAS (Efecto profesional)
       ========================================== */
    const canvas = document.getElementById('particleCanvas');
    const ctx = canvas.getContext('2d');
    let particles = [];
    let mouseX = 0;
    let mouseY = 0;

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resizeCanvas();
    $(window).on('resize', resizeCanvas);

    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2 + 0.5;
            this.speedX = (Math.random() - 0.5) * 0.5;
            this.speedY = (Math.random() - 0.5) * 0.5;
            this.opacity = Math.random() * 0.5 + 0.2;
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;

            // Interacción con el mouse
            const dx = mouseX - this.x;
            const dy = mouseY - this.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            if (distance < 100) {
                this.x -= dx * 0.01;
                this.y -= dy * 0.01;
            }

            // Bordes
            if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
            if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
        }
        draw() {
            ctx.fillStyle = `rgba(0, 217, 255, ${this.opacity})`;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    function initParticles() {
        particles = [];
        const count = Math.min(100, Math.floor((canvas.width * canvas.height) / 15000));
        for (let i = 0; i < count; i++) {
            particles.push(new Particle());
        }
    }
    initParticles();

    function connectParticles() {
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < 120) {
                    ctx.strokeStyle = `rgba(0, 217, 255, ${0.15 * (1 - distance / 120)})`;
                    ctx.lineWidth = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
    }

    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        connectParticles();
        requestAnimationFrame(animateParticles);
    }
    animateParticles();

    $(document).on('mousemove', function (e) {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    /* ==========================================
       3. NAVBAR SCROLL EFFECT
       ========================================== */
    $(window).on('scroll', function () {
        const scrollY = $(this).scrollTop();
        if (scrollY > 50) {
            $('#navbar').addClass('scrolled');
        } else {
            $('#navbar').removeClass('scrolled');
        }

        // Botón volver arriba
        if (scrollY > 400) {
            $('#scrollToTopBtn').addClass('show');
        } else {
            $('#scrollToTopBtn').removeClass('show');
        }

        // Active link tracking
        $('section[id]').each(function () {
            const sectionTop = $(this).offset().top - 100;
            const sectionBottom = sectionTop + $(this).outerHeight();
            const sectionId = $(this).attr('id');
            if (scrollY >= sectionTop && scrollY < sectionBottom) {
                $('.nav-link').removeClass('active');
                $(`.nav-link[href="#${sectionId}"]`).addClass('active');
            }
        });
    });

    /* ==========================================
       4. SMOOTH SCROLL CON JQUERY (2 segundos)
       ========================================== */
    $('a[href^="#"]').on('click', function (e) {
        const target = $(this.getAttribute('href'));
        if (target.length) {
            e.preventDefault();
            const targetPosition = target.offset().top - 80;
            $('html, body').stop().animate({
                scrollTop: targetPosition
            }, 2000, 'swing');

            // Cerrar menú móvil
            if ($('.navbar-collapse').hasClass('show')) {
                bootstrap.Collapse.getInstance($('.navbar-collapse')[0]).hide();
            }
        }
    });

    /* ==========================================
       5. BOTÓN VOLVER ARRIBA
       ========================================== */
    $('#scrollToTopBtn').on('click', function () {
        $('html, body').stop().animate({ scrollTop: 0 }, 2000, 'swing');
    });

    /* ==========================================
       6. TYPING EFFECT
       ========================================== */
    const typingTexts = [
        'Systems Analyst',
        'Full Stack Java Developer',
        'Python Developer',
        'Infrastructure Specialist',
        'Problem Solver'
    ];
    let textIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const typingElement = document.getElementById('typing-text');

    function typeEffect() {
        const currentText = typingTexts[textIndex];
        if (isDeleting) {
            typingElement.textContent = currentText.substring(0, charIndex - 1);
            charIndex--;
        } else {
            typingElement.textContent = currentText.substring(0, charIndex + 1);
            charIndex++;
        }

        let speed = isDeleting ? 50 : 100;

        if (!isDeleting && charIndex === currentText.length) {
            speed = 2000;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            textIndex = (textIndex + 1) % typingTexts.length;
            speed = 500;
        }

        setTimeout(typeEffect, speed);
    }
    typeEffect();

    /* ==========================================
       7. REVEAL ON SCROLL (Intersection Observer)
       ========================================== */
    const revealItems = document.querySelectorAll('.reveal-item');
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    revealItems.forEach(item => revealObserver.observe(item));

    /* ==========================================
       8. COUNTER ANIMATION (Stats)
       ========================================== */
    const statNumbers = document.querySelectorAll('.stat-number');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute('data-target'));
                animateCounter(entry.target, target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    statNumbers.forEach(num => counterObserver.observe(num));

    function animateCounter(element, target) {
        let current = 0;
        const increment = target / 60;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target + (target === 100 ? '%' : '+');
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 30);
    }

    /* ==========================================
       9. SKILL BARS ANIMATION
       ========================================== */
    const skillBars = document.querySelectorAll('.skill-progress');
    const skillObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const width = entry.target.getAttribute('data-width');
                entry.target.style.width = width;
                skillObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    skillBars.forEach(bar => skillObserver.observe(bar));

    /* ==========================================
       10. FORMULARIO DE CONTACTO
       ========================================== */
    $('#contactForm').on('submit', function (e) {
        e.preventDefault();
        const form = this;
        const submitBtn = $(form).find('button[type="submit"]');
        const originalText = submitBtn.html();

        if (!form.checkValidity()) {
            $(form).addClass('was-validated');
            return;
        }

        submitBtn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin me-2"></i>Enviando...');

        setTimeout(() => {
            const nombre = $('#nombre').val();
            const email = $('#email').val();
            const asunto = $('#asunto').val();
            const mensaje = $('#mensaje').val();

            // Modal de éxito
            const modal = `
                <div class="modal fade" id="successModal" tabindex="-1">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content" style="background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 20px;">
                            <div class="modal-body text-center p-5">
                                <div style="width: 80px; height: 80px; background: rgba(0,217,255,0.1); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem;">
                                    <i class="fas fa-check" style="font-size: 2.5rem; color: var(--primary);"></i>
                                </div>
                                <h3 style="color: var(--text-light); margin-bottom: 1rem;">¡Mensaje Enviado!</h3>
                                <p style="color: var(--text-muted); margin-bottom: 1.5rem;">Gracias <strong style="color: var(--primary);">${nombre}</strong>, te contactaré a la brevedad.</p>
                                <div style="text-align: left; background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 10px; font-size: 0.9rem;">
                                    <p style="color: var(--text-muted); margin: 0.25rem 0;"><strong style="color: var(--primary);">Email:</strong> ${email}</p>
                                    <p style="color: var(--text-muted); margin: 0.25rem 0;"><strong style="color: var(--primary);">Asunto:</strong> ${asunto}</p>
                                </div>
                                <button type="button" class="btn btn-primary-custom mt-4" data-bs-dismiss="modal">Aceptar</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            $('body').append(modal);
            const modalInstance = new bootstrap.Modal(document.getElementById('successModal'));
            modalInstance.show();
            $('#successModal').on('hidden.bs.modal', function () { $(this).remove(); });

            form.reset();
            $(form).removeClass('was-validated');
            submitBtn.prop('disabled', false).html(originalText);
        }, 1500);
    });

    /* ==========================================
       11. PARALLAX EFFECT EN HERO
       ========================================== */
    $(window).on('scroll', function () {
        const scrolled = $(this).scrollTop();
        if (scrolled < 800) {
            $('.hero-image-wrapper').css('transform', `translateY(${scrolled * 0.15}px)`);
            $('.hero-content').css('transform', `translateY(${scrolled * 0.05}px)`);
        }
    });

    /* ==========================================
       12. TILT EFFECT EN PROJECT CARDS
       ========================================== */
    $('.project-card').on('mousemove', function (e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;
        $(this).css('transform', `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`);
    });

    $('.project-card').on('mouseleave', function () {
        $(this).css('transform', 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)');
    });

});