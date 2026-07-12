/**
 * build.js — Build wing interactivity for Emergentism Compass
 * Minimal, functional, no external dependencies.
 */

(function () {
  'use strict';

  /* ── Theme toggle ──────────────────────────────────────────────────────── */
  const themeToggle = document.getElementById('themeToggle');
  const root = document.documentElement;

  // Initialize from localStorage or system preference
  const storedTheme = localStorage.getItem('emergentism-theme');
  if (storedTheme) {
    root.setAttribute('data-theme', storedTheme);
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
    root.setAttribute('data-theme', 'light');
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = root.getAttribute('data-theme');
      const next = current === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', next === 'dark' ? '' : next);
      // data-theme="" is dark (default), "light" is light
      if (next === 'dark') {
        root.removeAttribute('data-theme');
        localStorage.removeItem('emergentism-theme');
      } else {
        root.setAttribute('data-theme', next);
        localStorage.setItem('emergentism-theme', next);
      }
    });
  }

  /* ── Active nav highlighting on scroll ───────────────────────────────── */
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.topbar .routes a[href^="#"], .topbar .routes a[href^="./"]');

  function updateActiveNav() {
    let current = '';
    const scrollPos = window.scrollY + 120; // offset for topbar

    sections.forEach((sec) => {
      const top = sec.offsetTop;
      if (scrollPos >= top) {
        current = sec.getAttribute('id');
      }
    });

    navLinks.forEach((link) => {
      link.classList.remove('active');
      const href = link.getAttribute('href');
      if (href === '#' + current || (current === '' && href === './')) {
        link.classList.add('active');
      }
    });
  }

  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        updateActiveNav();
        ticking = false;
      });
      ticking = true;
    }
  });

  // Run once on load
  updateActiveNav();

  /* ── Copy-to-clipboard for code blocks ───────────────────────────────── */
  document.querySelectorAll('.step-body pre, .console-body').forEach((block) => {
    const btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.textContent = 'Copy';
    btn.setAttribute('aria-label', 'Copy code to clipboard');
    btn.style.cssText = `
      position: absolute;
      top: 8px;
      right: 8px;
      padding: 4px 10px;
      border: 1px solid var(--border);
      border-radius: 4px;
      background: var(--elevated);
      color: var(--text-muted);
      font-family: var(--font-mono);
      font-size: 0.68rem;
      font-weight: 700;
      text-transform: uppercase;
      cursor: pointer;
      opacity: 0;
      transition: opacity 0.2s ease;
    `;

    block.style.position = 'relative';
    block.appendChild(btn);

    block.addEventListener('mouseenter', () => { btn.style.opacity = '1'; });
    block.addEventListener('mouseleave', () => { btn.style.opacity = '0'; });

    btn.addEventListener('click', () => {
      const code = block.querySelector('code');
      if (!code) return;
      const text = code.textContent;
      navigator.clipboard.writeText(text).then(() => {
        btn.textContent = 'Copied';
        btn.style.color = 'var(--gate-pass)';
        setTimeout(() => {
          btn.textContent = 'Copy';
          btn.style.color = 'var(--text-muted)';
        }, 1500);
      }).catch(() => {
        // Fallback: select and execCommand
        const range = document.createRange();
        range.selectNode(code);
        const sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        try {
          document.execCommand('copy');
          btn.textContent = 'Copied';
          setTimeout(() => { btn.textContent = 'Copy'; }, 1500);
        } catch (e) {
          btn.textContent = 'Failed';
          setTimeout(() => { btn.textContent = 'Copy'; }, 1500);
        }
        sel.removeAllRanges();
      });
    });
  });

  /* ── Console typing effect for gate section (subtle, once) ─────────────── */
  const consoleBody = document.querySelector('.console-body');
  if (consoleBody && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const originalText = consoleBody.textContent;
    const lines = originalText.trim().split('\n');
    consoleBody.textContent = '';

    let lineIndex = 0;
    let charIndex = 0;
    let currentSpan = null;

    function typeNext() {
      if (lineIndex >= lines.length) return;

      if (!currentSpan) {
        currentSpan = document.createElement('span');
        currentSpan.style.display = 'block';
        consoleBody.appendChild(currentSpan);
      }

      const line = lines[lineIndex];
      if (charIndex < line.length) {
        currentSpan.textContent += line[charIndex];
        charIndex++;
        setTimeout(typeNext, 12);
      } else {
        lineIndex++;
        charIndex = 0;
        currentSpan = null;
        if (lineIndex < lines.length) {
          setTimeout(typeNext, 40);
        }
      }
    }

    // Intersection Observer: start typing when console enters viewport
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          typeNext();
          observer.disconnect();
        }
      });
    }, { threshold: 0.5 });

    observer.observe(consoleBody);
  }

  /* ── Receipt hash verification hint ────────────────────────────────────── */
  const receiptHash = document.getElementById('receipt-hash');
  if (receiptHash) {
    receiptHash.addEventListener('click', () => {
      // Show a transient tooltip
      const tooltip = document.createElement('span');
      tooltip.textContent = 'Run: git show 7a3f9e2';
      tooltip.style.cssText = `
        position: absolute;
        background: var(--elevated);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 4px 8px;
        font-family: var(--font-mono);
        font-size: 0.72rem;
        color: var(--text-muted);
        margin-left: 8px;
        white-space: nowrap;
      `;
      receiptHash.style.position = 'relative';
      receiptHash.appendChild(tooltip);
      setTimeout(() => tooltip.remove(), 2500);
    });
    receiptHash.style.cursor = 'pointer';
  }

})();
