/**
 * Halāhala wing — interactive layer
 * Built by L4 Kṣatriya halahala_wing per cross-caste audit 2026-07-14
 * [S] Structural — JS is presentation behavior, not claim
 */

(function () {
  'use strict';

  // ── Smooth scroll for anchor links ──
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Update URL without jump
        history.pushState(null, '', targetId);
      }
    });
  });

  // ── Poison card hover: subtle glow on severity color ──
  const poisonCards = document.querySelectorAll('.poison-card');
  poisonCards.forEach(card => {
    const severity = card.dataset.severity;
    if (!severity) return;

    card.addEventListener('mouseenter', () => {
      const color = severity === 'critical'
        ? 'rgba(244, 67, 54, 0.08)'
        : severity === 'high'
          ? 'rgba(255, 122, 23, 0.08)'
          : 'rgba(85, 85, 85, 0.06)';
      card.style.boxShadow = `0 0 0 1px var(--border), 0 4px 24px ${color}`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.boxShadow = '';
    });
  });

  // ── Surface card hover ──
  const surfaceCards = document.querySelectorAll('.surface-card');
  surfaceCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.boxShadow = '0 0 0 1px var(--border), 0 4px 24px rgba(255, 122, 23, 0.06)';
    });
    card.addEventListener('mouseleave', () => {
      card.style.boxShadow = '';
    });
  });

  // ── Amrita poison hover ──
  const amritaPoisons = document.querySelectorAll('.amrita-poison');
  amritaPoisons.forEach(p => {
    p.addEventListener('mouseenter', () => {
      p.style.boxShadow = '0 0 0 1px var(--border), 0 4px 24px rgba(255, 122, 23, 0.06)';
    });
    p.addEventListener('mouseleave', () => {
      p.style.boxShadow = '';
    });
  });

  // ── Seam table row: highlight on hover (CSS handles most; JS adds subtle row glow) ──
  const seamRows = document.querySelectorAll('.seam-table tbody tr');
  seamRows.forEach(row => {
    row.addEventListener('mouseenter', () => {
      row.style.borderLeft = '2px solid var(--kintsugi-gold)';
    });
    row.addEventListener('mouseleave', () => {
      row.style.borderLeft = '';
    });
  });

  // ── Intersection Observer for fade-in on scroll ──
  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -60px 0px',
    threshold: 0.05
  };

  const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        fadeObserver.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Observe all major content blocks
  const observeTargets = document.querySelectorAll(
    '.poison-card, .surface-card, .amrita-poison, .fact, .one-line-box'
  );
  observeTargets.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(12px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    fadeObserver.observe(el);
  });

  // Add the visible class styles dynamically
  const style = document.createElement('style');
  style.textContent = `
    .poison-card.is-visible,
    .surface-card.is-visible,
    .amrita-poison.is-visible,
    .fact.is-visible,
    .one-line-box.is-visible {
      opacity: 1 !important;
      transform: translateY(0) !important;
    }
  `;
  document.head.appendChild(style);

  // ── Keyboard navigation: Escape to close any open modals (future-proof) ──
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      // No modals in this wing yet, but the hook is here
      document.activeElement?.blur();
    }
  });

  // ── Console greeting (development-only, not visible to users) ──
  if (typeof console !== 'undefined' && console.log) {
    console.log('%c Halāhala wing loaded ', 'background:#FF7A17;color:#050505;font-weight:700;padding:4px 8px;border-radius:4px;');
    console.log('Evidence tiers on every claim. No receipt = no reality.');
  }

})();
