/**
 * test-falsifiers.js — Test Falsifiers Wing
 * Staging: _STAGING_COMPASS_RESTRUCTURE/test_falsifiers_wing/
 * Role: L4 Kṣatriya (test_falsifiers_wing)
 * Purpose: Interactive gauges, table filtering, scroll-triggered animations
 * Evidence tiers: [S] for structural behavior; [D] for derived animation logic
 */

(function () {
  'use strict';

  // ================================================================
  // 1. GAUGE ANIMATION — fill bars on scroll into view
  // ================================================================
  const gaugeCards = document.querySelectorAll('.gauge-card');

  const gaugeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const fill = entry.target.querySelector('.gauge-fill');
        if (fill) {
          // Read target width from inline style, animate to it
          const targetWidth = fill.style.width || '0%';
          fill.style.width = '0%';
          // Force reflow
          void fill.offsetWidth;
          fill.style.width = targetWidth;
        }
        gaugeObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3, rootMargin: '0px 0px -40px 0px' });

  gaugeCards.forEach(card => gaugeObserver.observe(card));

  // ================================================================
  // 2. TABLE ROW HIGHLIGHT — pulse on hover (CSS handles base,
  //    JS adds subtle row-focus for keyboard nav)
  // ================================================================
  const tables = document.querySelectorAll('.falsifier-table');

  tables.forEach(table => {
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
      row.setAttribute('tabindex', '0');
      row.addEventListener('focus', () => {
        row.style.outline = '1px solid rgba(255, 235, 59, 0.3)';
        row.style.outlineOffset = '-1px';
      });
      row.addEventListener('blur', () => {
        row.style.outline = '';
        row.style.outlineOffset = '';
      });
    });
  });

  // ================================================================
  // 3. SMOOTH SCROLL for CTA anchor links
  // ================================================================
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const topbarHeight = 64;
        const targetTop = target.getBoundingClientRect().top + window.pageYOffset - topbarHeight - 16;
        window.scrollTo({ top: targetTop, behavior: 'smooth' });
      }
    });
  });

  // ================================================================
  // 4. LADDER RUNG ENTRANCE — staggered fade-in on scroll
  // [D] Derived animation pattern, not load-bearing
  // ================================================================
  const ladderRungs = document.querySelectorAll('.ladder-rung');

  const ladderObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        // Stagger by DOM order
        const delay = Array.from(ladderRungs).indexOf(entry.target) * 100;
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, delay);
        ladderObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  ladderRungs.forEach(rung => {
    rung.style.opacity = '0';
    rung.style.transform = 'translateY(12px)';
    rung.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    ladderObserver.observe(rung);
  });

  // ================================================================
  // 5. SECTION ENTRANCE — subtle fade for major sections
  // [D] Derived animation pattern
  // ================================================================
  const sections = document.querySelectorAll('.index-section');

  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        sectionObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -60px 0px' });

  sections.forEach(section => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(16px)';
    section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    sectionObserver.observe(section);
  });

  // ================================================================
  // 6. CONSOLE — simple log for audit trail
  // [S] Structural: visible in browser devtools, not user-facing
  // ================================================================
  console.log(
    '%c[Test Falsifiers Wing] %cL4 Kṣatriya — test_falsifiers_wing\n' +
    '%cCanonical path: %c01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/31_FALSIFIERS_INDEX.md\n' +
    '%cEvidence tiers: %c[A/B/S/I/D/C] visible on every claim',
    'color:#FFEB3B; font-weight:700;',
    'color:#9CA3AF;',
    'color:#555;',
    'color:#9CA3AF;',
    'color:#555;',
    'color:#9CA3AF;'
  );

})();
