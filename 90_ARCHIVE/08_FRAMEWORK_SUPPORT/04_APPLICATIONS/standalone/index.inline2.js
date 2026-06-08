document.querySelectorAll('[data-href]').forEach(el => {
  el.setAttribute('role','button');
  el.setAttribute('tabindex','0');
  el.addEventListener('click', () => { window.location.href = el.getAttribute('data-href'); });
  el.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); window.location.href = el.getAttribute('data-href'); }});
});
