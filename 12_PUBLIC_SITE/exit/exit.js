/**
 * exit.js — K4 Grace Exit Wing
 * Minimal interaction: theme toggle, smooth scroll, console animation
 * No tracking. No analytics. No cookies. K4-aligned by default.
 */

(function () {
  'use strict';

  /* ── Theme toggle ── */
  const themeToggle = document.getElementById('themeToggle');
  const storedTheme = localStorage.getItem('theme');

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    themeToggle.textContent = theme === 'light' ? '◑' : '◐';
  }

  if (storedTheme) {
    applyTheme(storedTheme);
  } else {
    applyTheme('dark');
  }

  themeToggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    applyTheme(current === 'dark' ? 'light' : 'dark');
  });

  /* ── Smooth scroll for anchor links ── */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ── Console animation on scroll ── */
  const consoleBody = document.querySelector('.console-body');
  if (consoleBody) {
    const lines = consoleBody.querySelectorAll('.pass, .output, .cmd');
    lines.forEach((line, i) => {
      line.style.opacity = '0';
      line.style.transform = 'translateY(4px)';
      line.style.transition = 'opacity 0.25s ease, transform 0.25s ease';
    });

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          lines.forEach((line, i) => {
            setTimeout(() => {
              line.style.opacity = '1';
              line.style.transform = 'translateY(0)';
            }, i * 60);
          });
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.25 });

    observer.observe(consoleBody);
  }

  /* ── Exit-step reveal on scroll ── */
  const steps = document.querySelectorAll('.exit-step');
  steps.forEach((step, i) => {
    step.style.opacity = '0';
    step.style.transform = 'translateY(16px)';
    step.style.transition = 'opacity 0.5s ease, transform 0.5s ease';

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
          }, i * 120);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });

    observer.observe(step);
  });

  /* ── K4-card reveal on scroll ── */
  const cards = document.querySelectorAll('.k4-card');
  cards.forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(12px)';
    card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
          }, i * 100);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });

    observer.observe(card);
  });

})();
