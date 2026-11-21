/* SenDev animated mobile navigation.
   Safe to load after existing portfolio.js; overrides its click on #menuToggle
   without changing desktop navigation or other portfolio scripts. */
(() => {
  'use strict';

  const toggle = document.getElementById('menuToggle');
  const panel = document.getElementById('navPanel');
  const backdrop = document.getElementById('mobileNavBackdrop');
  const header = document.getElementById('siteHeader');
  if (!toggle || !panel || !backdrop || !header) return;

  const mobile = window.matchMedia('(max-width: 991px)');
  let isOpen = false;

  // CSS positions the panel underneath the actual header, even if its size changes.
  function syncHeaderPosition() {
    const bottom = Math.max(0, Math.round(header.getBoundingClientRect().bottom));
    document.documentElement.style.setProperty('--sendev-header-bottom', `${bottom}px`);
  }

  function setOpen(open, restoreFocus = false) {
    isOpen = Boolean(open && mobile.matches);
    toggle.classList.toggle('is-open', isOpen);
    panel.classList.toggle('is-open', isOpen);
    backdrop.classList.toggle('is-open', isOpen);
    document.body.classList.toggle('sendev-menu-open', isOpen);
    toggle.setAttribute('aria-expanded', String(isOpen));
    toggle.setAttribute('aria-label', isOpen ? 'Tutup menu navigasi' : 'Buka menu navigasi');

    if (mobile.matches) {
      panel.inert = !isOpen;
      panel.setAttribute('aria-hidden', String(!isOpen));
    } else {
      panel.inert = false;
      panel.removeAttribute('aria-hidden');
    }
    if (isOpen) syncHeaderPosition();
    if (!isOpen && restoreFocus && mobile.matches) toggle.focus();
  }

  // Capture first so older portfolio.js hamburger listeners won't toggle twice.
  toggle.addEventListener('click', (event) => {
    if (!mobile.matches) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    setOpen(!isOpen);
  }, { capture: true });

  backdrop.addEventListener('click', () => setOpen(false, true));
  panel.querySelectorAll('a[href]').forEach(link => {
    link.addEventListener('click', () => setOpen(false));
  });
  document.querySelectorAll('.site-header .brand, .site-header .nav-cta').forEach(link => {
    link.addEventListener('click', () => setOpen(false));
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && isOpen) {
      event.preventDefault();
      setOpen(false, true);
    }
  });

  // On changing to desktop, unlock scrolling and restore regular nav accessibility.
  function onViewportChange() {
    syncHeaderPosition();
    setOpen(false);
  }
  if (mobile.addEventListener) mobile.addEventListener('change', onViewportChange);
  else mobile.addListener(onViewportChange);
  window.addEventListener('resize', syncHeaderPosition, { passive: true });
  window.addEventListener('scroll', () => {
    if (isOpen) syncHeaderPosition();
  }, { passive: true });

  syncHeaderPosition();
  setOpen(false);
})();
