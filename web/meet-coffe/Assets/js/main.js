/* =============================================================
   MEET & COFFEE — Interacciones
   ============================================================= */

document.addEventListener('DOMContentLoaded', () => {

  /* ---------- 1. AOS: animaciones al scroll ---------- */
  if (window.AOS) {
    AOS.init({
      duration: 900,
      easing: 'ease-out-cubic',
      once: true,
      offset: 80,
    });
  }

  /* ---------- 2. Preloader ---------- */
  const preloader = document.getElementById('preloader');
  window.addEventListener('load', () => {
    setTimeout(() => {
      preloader.classList.add('hidden');
      document.body.classList.remove('preload');
    }, 700);
  });

  /* ---------- 3. Navbar: fondo al hacer scroll ---------- */
  const nav = document.getElementById('mainNav');
  const onScroll = () => {
    nav.classList.toggle('scrolled', window.scrollY > 60);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- 4. Barra de progreso de scroll ---------- */
  const progress = document.getElementById('scrollProgress');
  const updateProgress = () => {
    const h = document.documentElement;
    const scrolled = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
    progress.style.width = scrolled + '%';
  };
  window.addEventListener('scroll', updateProgress, { passive: true });

  /* ---------- 5. Cursor personalizado ---------- */
  const cursor = document.getElementById('cursor');
  const cursorDot = document.getElementById('cursorDot');
  const isFine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  if (isFine && cursor && cursorDot) {
    let mouseX = 0, mouseY = 0;
    let curX = 0, curY = 0;

    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      cursorDot.style.transform = `translate(${mouseX}px, ${mouseY}px) translate(-50%, -50%)`;
    });

    const animate = () => {
      curX += (mouseX - curX) * 0.15;
      curY += (mouseY - curY) * 0.15;
      cursor.style.transform = `translate(${curX}px, ${curY}px) translate(-50%, -50%)`;
      requestAnimationFrame(animate);
    };
    animate();

    // Efecto al pasar por enlaces / botones
    document.querySelectorAll('a, button, .evento-card, .info-list li').forEach(el => {
      el.addEventListener('mouseenter', () => cursor.classList.add('active'));
      el.addEventListener('mouseleave', () => cursor.classList.remove('active'));
    });
  }

  /* ---------- 6. Contadores animados ---------- */
  const counters = document.querySelectorAll('[data-count]');
  const animateCounter = (el) => {
    const target = +el.dataset.count;
    const duration = 1600;
    const start = performance.now();

    const tick = (now) => {
      const t = Math.min((now - start) / duration, 1);
      // easeOutExpo
      const eased = t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
      el.textContent = Math.floor(eased * target).toLocaleString('es-CL');
      if (t < 1) requestAnimationFrame(tick);
      else el.textContent = target.toLocaleString('es-CL') + (el.dataset.suffix || '');
    };
    requestAnimationFrame(tick);
  };

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.4 });

  counters.forEach(c => counterObserver.observe(c));

  /* ---------- 7. Smooth scroll para anchors ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
      const id = link.getAttribute('href');
      if (id === '#' || id.length < 2) return;
      const target = document.querySelector(id);
      if (!target) return;

      e.preventDefault();
      const navHeight = nav.offsetHeight;
      const top = target.getBoundingClientRect().top + window.scrollY - navHeight + 10;

      window.scrollTo({ top, behavior: 'smooth' });

      // Cierra el menú móvil si está abierto
      const collapse = document.getElementById('menuPrincipal');
      if (collapse && collapse.classList.contains('show')) {
        new bootstrap.Collapse(collapse).hide();
      }
    });
  });

  /* ---------- 8. Parallax suave en el hero ---------- */
  const hero = document.querySelector('.hero');
  if (hero && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    window.addEventListener('scroll', () => {
      const y = window.scrollY;
      if (y < window.innerHeight) {
        hero.style.backgroundPositionY = `calc(50% + ${y * 0.35}px)`;
      }
    }, { passive: true });
  }

  /* ---------- 9. Año dinámico en el footer ---------- */
  const copy = document.querySelector('.footer__copy');
  if (copy) {
    copy.textContent = `© ${new Date().getFullYear()} Meet & Coffee · Desafío Latam`;
  }

});