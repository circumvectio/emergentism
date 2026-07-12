/**
 * map.js — Rosetta Map wing interactivity
 * Staging: 01_EMERGENTISM/12_PUBLIC_SITE/_STAGING_COMPASS_RESTRUCTURE/map_rosetta_wing/
 * Role: L4 Kṣatriya execution — functional role toggle, table interactions, evidence tier visibility
 */

(function() {
  'use strict';

  // --- Role toggle: functional / Sanskrit / both ---
  const buttons = document.querySelectorAll('.role-toggle button');
  const roles = document.querySelectorAll('.role');
  const operators = document.querySelectorAll('.operator');

  function setMode(mode) {
    buttons.forEach(b => b.classList.toggle('active', b.dataset.mode === mode));
    roles.forEach(el => {
      if (mode === 'functional') el.textContent = el.dataset.functional;
      else if (mode === 'sanskrit') el.textContent = el.dataset.sanskrit;
      else el.textContent = el.dataset.functional + ' · ' + el.dataset.sanskrit;
    });
    operators.forEach(el => {
      if (mode === 'functional') el.textContent = el.dataset.functional;
      else if (mode === 'sanskrit') el.textContent = el.dataset.sanskrit;
      else el.textContent = el.dataset.functional + ' · ' + el.dataset.sanskrit;
    });
    try {
      localStorage.setItem('rosetta-map-mode', mode);
    } catch (e) {
      // Storage unavailable — silent fail
    }
  }

  buttons.forEach(btn => {
    btn.addEventListener('click', () => setMode(btn.dataset.mode));
  });

  // Restore preference
  try {
    const stored = localStorage.getItem('rosetta-map-mode');
    if (stored) setMode(stored);
  } catch (e) {
    // Storage unavailable — default to functional
  }

  // --- Table row hover: highlight mirror-pair ---
  const tableRows = document.querySelectorAll('.map-table tbody tr');
  tableRows.forEach(row => {
    row.addEventListener('mouseenter', () => {
      const lvl = row.querySelector('.lvl')?.textContent;
      if (!lvl) return;
      // Highlight the same level across cross-domain cards
      document.querySelectorAll('.cd-cell').forEach(cell => {
        const cellText = cell.textContent;
        // Simple heuristic: check if cell contains the level indicator
        // L4 equator gets special handling
        if (lvl === 'L4' && cellText.includes('Fourth')) {
          cell.style.borderColor = 'var(--gold)';
        } else if (lvl === 'L1' && cellText.includes('First')) {
          cell.style.borderColor = 'var(--gold)';
        } else if (lvl === 'L2' && cellText.includes('Second')) {
          cell.style.borderColor = 'var(--gold)';
        } else if (lvl === 'L3' && cellText.includes('Third')) {
          cell.style.borderColor = 'var(--gold)';
        } else if (lvl === 'L5' && cellText.includes('Fifth')) {
          cell.style.borderColor = 'var(--gold)';
        } else if (lvl === 'L6' && cellText.includes('Sixth')) {
          cell.style.borderColor = 'var(--gold)';
        } else if (lvl === 'L7' && cellText.includes('Seventh')) {
          cell.style.borderColor = 'var(--gold)';
        }
      });
    });
    row.addEventListener('mouseleave', () => {
      document.querySelectorAll('.cd-cell').forEach(cell => {
        cell.style.borderColor = '';
      });
    });
  });

  // --- Evidence tier visibility: click to expand/collapse detail ---
  // (No-op for now — tiers are always visible per audit requirement)
  // Future: could add a filter to show/hide [C] claims

  console.log('[map.js] Rosetta Map wing loaded — L4 Kṣatriya execution');
})();
