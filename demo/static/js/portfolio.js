/* SenDev — Lightweight interaction engine. Vanilla JavaScript, no build step. */
(() => {
  'use strict';
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const pointerFine = window.matchMedia('(hover:hover) and (pointer:fine)').matches;

  // Sticky navigation + slim scroll progress.
  const header = $('#siteHeader');
  const progress = $('#scrollProgress');
  let tickingScroll = false;
  const updateScroll = () => {
    const y = window.scrollY;
    header?.classList.toggle('scrolled', y > 28);
    const maxScroll = document.documentElement.scrollHeight - innerHeight;
    if (progress) progress.style.width = (maxScroll > 0 ? (y / maxScroll) * 100 : 0) + '%';
    tickingScroll = false;
  };
  addEventListener('scroll', () => {
    if (!tickingScroll) { requestAnimationFrame(updateScroll); tickingScroll = true; }
  }, { passive: true });
  updateScroll();
  if ($('#footerYear')) $('#footerYear').textContent = String(new Date().getFullYear());
  if ($('#heroYear')) $('#heroYear').textContent = String(new Date().getFullYear());

  // Mobile menu with real keyboard semantics.
  const menuToggle = $('#menuToggle');
  const navPanel = $('#navPanel');
  function closeMenu() {
    navPanel?.classList.remove('open');
    menuToggle?.setAttribute('aria-expanded', 'false');
    menuToggle?.setAttribute('aria-label', 'Buka menu');
  }
  menuToggle?.addEventListener('click', () => {
    const open = navPanel.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Tutup menu' : 'Buka menu');
  });
  $$('.nav-link').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('click', e => {
    if (navPanel?.classList.contains('open') && !header.contains(e.target)) closeMenu();
  });
  addEventListener('resize', () => { if (innerWidth > 900) closeMenu(); });

  // Active section nav and intersection-based entrance animations.
  const reveals = $$('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion) {
    const revealObserver = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      }
    }, { threshold: .1, rootMargin: '0px 0px -32px 0px' });
    reveals.forEach((el, i) => { el.style.transitionDelay = (i % 4) * 75 + 'ms'; revealObserver.observe(el); });
  } else reveals.forEach(el => el.classList.add('is-visible'));
  const sections = $$('section[id]');
  if ('IntersectionObserver' in window) {
    const activeObserver = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          $$('.nav-link').forEach(link => link.classList.toggle('active', link.dataset.nav === entry.target.id || (entry.target.id === 'journey' && link.dataset.nav === 'gallery')));
        }
      }
    }, { rootMargin: '-25% 0px -60% 0px' });
    sections.forEach(section => activeObserver.observe(section));
  }

  // Pointer response: soft spotlight, interactive card tilt, subtle magnetic CTA.
  const glow = $('#cursorGlow');
  if (pointerFine && !reduceMotion) {
    window.addEventListener('pointermove', e => {
      if (glow) { glow.style.left = e.clientX + 'px'; glow.style.top = e.clientY + 'px'; }
    }, { passive: true });
    $$('[data-tilt]').forEach(card => {
      const maxTilt = card.classList.contains('hero-portrait-wrap') ? 6 : 3;
      const initialRotation = card.classList.contains('hero-portrait-wrap') ? -6 : 0;
      card.addEventListener('pointermove', e => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - .5;
        const y = (e.clientY - rect.top) / rect.height - .5;
        card.style.transform = `rotateX(${-y * maxTilt}deg) rotateY(${x * maxTilt}deg) rotate(${initialRotation}deg) translateY(-3px)`;
      });
      card.addEventListener('pointerleave', () => { card.style.transform = ''; });
    });
    $$('.spotlight-card').forEach(card => card.addEventListener('pointermove', e => {
      const bounds = card.getBoundingClientRect();
      card.style.setProperty('--mx', e.clientX - bounds.left + 'px');
      card.style.setProperty('--my', e.clientY - bounds.top + 'px');
    }));
    $$('.magnetic').forEach(button => {
      button.addEventListener('pointermove', e => {
        const rect = button.getBoundingClientRect();
        const x = (e.clientX - rect.left - rect.width / 2) * .09;
        const y = (e.clientY - rect.top - rect.height / 2) * .12;
        button.style.transform = `translate(${x}px,${y}px)`;
      });
      button.addEventListener('pointerleave', () => { button.style.transform = ''; });
    });
  }

  // Functional filter controls; no items are fetched or fabricated.
  const projectCards = $$('.project-card');
  const projectEmpty = $('#projectEmpty');
  $$('.filter-btn').forEach(button => button.addEventListener('click', () => {
    $$('.filter-btn').forEach(b => { b.classList.toggle('active', b === button); b.setAttribute('aria-pressed', String(b === button)); });
    const filter = button.dataset.filter;
    let visible = 0;
    for (const card of projectCards) {
      const match = filter === 'all' || card.dataset.category === filter;
      card.hidden = !match;
      if (match) visible++;
    }
    if (projectEmpty) projectEmpty.hidden = visible > 0;
  }));

  // Click-to-copy email with a truthful success/failure toast.
  let toastTimer;
  const toast = $('#toast');
  function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('visible'), 2600);
  }
  $$('[data-copy]').forEach(button => button.addEventListener('click', async () => {
    try {
      if (!navigator.clipboard || !window.isSecureContext) throw new Error('Clipboard API unavailable');
      await navigator.clipboard.writeText(button.dataset.copy || '');
      showToast('✓ Email berhasil disalin');
    } catch (_) {
      showToast('Salin alamat email secara manual dari tautan di sebelah kiri');
    }
  }));

  // Full-screen native dialog lightbox: only active when a real image exists.
  const lightbox = $('#lightboxDialog');
  $$('[data-lightbox]').forEach(trigger => trigger.addEventListener('click', () => {
    if (!lightbox || !trigger.dataset.lightbox) return;
    $('#lightboxImage').src = trigger.dataset.lightbox;
    $('#lightboxImage').alt = trigger.dataset.caption || 'Pratinjau galeri';
    $('#lightboxCaption').textContent = trigger.dataset.caption || '';
    lightbox.showModal();
  }));
  $('#closeLightbox')?.addEventListener('click', () => lightbox?.close());
  lightbox?.addEventListener('click', e => { if (e.target === lightbox) lightbox.close(); });
  lightbox?.addEventListener('close', () => { $('#lightboxImage').removeAttribute('src'); });

  // Keyboard command palette — Ctrl+K or Cmd+K and nav search.
  const dialog = $('#commandDialog');
  const input = $('#commandSearch');
  const commandButtons = $$('#commandList button');
  const openCommand = () => { if (!dialog?.open) { dialog?.showModal(); input.value = ''; filterCommands(); input.focus(); } };
  const closeCommand = () => { if (dialog?.open) dialog.close(); };
  function filterCommands() {
    const term = (input?.value || '').toLocaleLowerCase('id');
    commandButtons.forEach(button => { button.hidden = !button.textContent.toLocaleLowerCase('id').includes(term); });
  }
  function goToSection(id) {
    closeCommand();
    closeMenu();
    const section = $('#' + id);
    if (section) { section.scrollIntoView({ behavior: reduceMotion ? 'instant' : 'smooth' }); history.replaceState(null, '', '#' + id); }
  }
  $('#openCommand')?.addEventListener('click', openCommand);
  $('#closeCommand')?.addEventListener('click', closeCommand);
  input?.addEventListener('input', filterCommands);
  commandButtons.forEach(button => button.addEventListener('click', () => goToSection(button.dataset.command)));
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); dialog?.open ? closeCommand() : openCommand(); }
    if (e.key === 'Enter' && dialog?.open && document.activeElement === input) { const first = commandButtons.find(button => !button.hidden); if (first) goToSection(first.dataset.command); }
  });
  dialog?.addEventListener('click', e => { if (e.target === dialog) closeCommand(); });

  // Particle backdrop: very lightweight canvas; automatically disabled for reduced-motion.
  const canvas = $('#starfield');
  if (canvas && !reduceMotion) {
    const context = canvas.getContext('2d', { alpha: true });
    if (context) {
      let width = 0, height = 0, particles = [], frame = 0, animationId;
      const resize = () => {
        const dpr = Math.min(devicePixelRatio || 1, 2);
        width = innerWidth; height = innerHeight;
        canvas.width = Math.round(width * dpr); canvas.height = Math.round(height * dpr);
        context.setTransform(dpr, 0, 0, dpr, 0, 0);
        const count = Math.min(75, Math.max(25, Math.round((width * height) / 18000)));
        particles = Array.from({ length: count }, () => ({ x: Math.random()*width, y: Math.random()*height, r: .4+Math.random()*1.1, speed: .08+Math.random()*.25, alpha: .15+Math.random()*.43 }));
      };
      const animate = () => {
        frame++;
        context.clearRect(0,0,width,height);
        for (const p of particles) {
          p.y -= p.speed;
          if (p.y < -3) { p.y = height + 3; p.x = Math.random() * width; }
          context.fillStyle = `rgba(171,166,255,${p.alpha * (.8 + Math.sin(frame*.012 + p.x)*.2)})`;
          context.beginPath(); context.arc(p.x,p.y,p.r,0,Math.PI*2); context.fill();
        }
        animationId = requestAnimationFrame(animate);
      };
      resize(); animate();
      let resizeTimer;
      window.addEventListener('resize', () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(resize, 180); });
      document.addEventListener('visibilitychange', () => {
        if (document.hidden) cancelAnimationFrame(animationId);
        else { cancelAnimationFrame(animationId); animate(); }
      });
    }
  }
})();
