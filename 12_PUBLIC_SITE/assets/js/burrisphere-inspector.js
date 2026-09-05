/* Native disclosures remain usable even when Three/WebGL cannot load. */
(() => {
  const records = [...document.querySelectorAll('[data-operator]')];
  const openTarget = (hash, focus = false) => {
    const id = hash.slice(1);
    const target = records.find(record => record.id === id);
    if (!target) return;
    records.forEach(record => { record.open = record === target; });
    if (focus) target.querySelector('summary').focus({preventScroll:true});
    target.scrollIntoView({block:'nearest', behavior:'instant'});
  };
  document.querySelectorAll('.bi-action-plane a').forEach(link => {
    link.addEventListener('click', () => openTarget(link.hash, true));
  });
  // Close peers synchronously before the native click toggles its target.
  // Queued toggle events can otherwise let an earlier choice defeat a later one.
  records.forEach(record => record.querySelector('summary').addEventListener('click', () => {
    if (!record.open) records.forEach(other => { if (other !== record) other.open = false; });
  }));
  window.addEventListener('hashchange', () => openTarget(window.location.hash));
  openTarget(window.location.hash);
})();
