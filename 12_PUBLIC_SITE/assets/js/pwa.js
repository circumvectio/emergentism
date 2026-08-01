// PWA registration — 124_PRIME_TIME_PWA_STAKEHOLDER_AUDIT_SHIP.md
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function () {
    navigator.serviceWorker.register('/sw.js').catch(function () {});
  });
}
