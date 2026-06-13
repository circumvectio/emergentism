/* WorkFlowy-style outline rail — the heading hierarchy as live navigation.
   Reads every h1/h2/h3[id] on the page and renders a right-docked, collapsible
   tree: nested bullets, expand/collapse, click-to-scroll, scroll-spy highlight,
   and WorkFlowy's signature zoom-into-node (click a bullet dot to make it the
   root, breadcrumb to climb back).

   Type follows the Material type SYSTEM (m2): each outline level is rendered in
   the named role's weight/tracking/case grammar — H1→Overline (chapter), H2→
   Subtitle2 (section), H3→Body2 (subsection) — adapted to navigation scale (not
   the literal display px). Typeface is Roboto, Material's own face, already
   self-hosted. Self-contained, same-origin only — gate-safe. DOM-built; heading
   text is set via textContent, never innerHTML. */
(function () {
  "use strict";
  if (window.__wfOutline) return;
  window.__wfOutline = true;

  var heads = Array.prototype.slice.call(
    document.querySelectorAll("main h1[id], main h2[id], main h3[id], .reading h1[id], .reading h2[id], .reading h3[id]")
  );
  if (heads.length < 4) {
    heads = Array.prototype.slice.call(document.querySelectorAll("h1[id], h2[id], h3[id]"));
  }
  if (heads.length < 4) return;   // not enough hierarchy to be worth a rail

  var LS_OPEN = "emergentism-outline-open";
  var LS_COLLAPSED = "emergentism-outline-collapsed";

  /* ---------- styles (Material type grammar, Skyzai palette) ---------- */
  var css = [
    "#wf-tab{position:fixed;right:0;top:42%;z-index:8800;writing-mode:vertical-rl;",
    "background:var(--bg2,#111);color:var(--gold,#FFEB3B);border:1px solid rgba(255,235,59,.4);",
    "border-right:0;border-radius:8px 0 0 8px;padding:14px 7px;font:600 11px/1 'Roboto','Noto Sans',sans-serif;",
    "letter-spacing:.22em;text-transform:uppercase;cursor:pointer}",
    "#wf-tab:hover{background:var(--gold,#FFEB3B);color:var(--bg,#050505)}",
    "#wf-rail{position:fixed;right:0;top:0;bottom:0;width:min(330px,90vw);z-index:8801;",
    "background:color-mix(in srgb,var(--bg,#050505) 96%,transparent);backdrop-filter:blur(9px);",
    "border-left:1px solid rgba(255,235,59,.28);clip-path:inset(0 0 0 100%);opacity:0;visibility:hidden;",
    "pointer-events:none;transition:clip-path .2s ease,opacity .2s ease;",
    "display:flex;flex-direction:column;font-family:'Roboto','Noto Sans',sans-serif;color:var(--ink,#FFFDE7);overflow:hidden}",
    "#wf-rail.open{clip-path:inset(0);opacity:1;visibility:visible;pointer-events:auto}",
    "#wf-head{display:flex;align-items:center;gap:8px;padding:14px 14px 8px}",
    "#wf-head b{color:var(--gold,#FFEB3B);font-size:11px;letter-spacing:.2em;text-transform:uppercase}",   /* Overline */
    "#wf-head .wf-x{margin-left:auto;background:none;border:0;color:var(--ink,#FFFDE7);font-size:17px;cursor:pointer;opacity:.6;line-height:1}",
    "#wf-head .wf-x:hover{opacity:1;color:var(--gold,#FFEB3B)}",
    "#wf-crumb{padding:0 14px 6px;font:400 11px/1.4 'Roboto Mono',monospace;color:var(--ink-faint,#8a8568);display:none}",
    "#wf-crumb.show{display:block}",
    "#wf-crumb a{color:var(--ink-faint,#8a8568);text-decoration:none;cursor:pointer}",
    "#wf-crumb a:hover{color:var(--gold,#FFEB3B)}",
    "#wf-tree{flex:1;overflow-y:auto;overflow-x:hidden;padding:2px 8px 28px;scrollbar-width:thin}",
    ".wf-row{display:flex;align-items:flex-start;gap:5px;border-radius:5px;padding:2px 4px}",
    ".wf-row:hover{background:var(--bg2,rgba(255,235,59,.06))}",
    ".wf-caret{flex:none;width:14px;text-align:center;cursor:pointer;color:var(--ink-faint,#8a8568);font-size:10px;",
    "line-height:1.7;user-select:none}",
    ".wf-caret:hover{color:var(--gold,#FFEB3B)}",
    ".wf-caret.leaf{visibility:hidden}",
    ".wf-dot{flex:none;width:14px;text-align:center;cursor:pointer;color:var(--ink-faint,#8a8568);line-height:1.5;font-size:13px}",
    ".wf-dot:hover{color:var(--gold,#FFEB3B)}",
    ".wf-dot.has-kids{color:var(--ink-soft,#cfcab0)}",
    ".wf-label{flex:1;cursor:pointer;text-decoration:none;color:var(--ink-soft,#cfcab0);padding:1px 2px;min-width:0;overflow-wrap:anywhere;word-break:break-word}",
    ".wf-label:hover{color:var(--ink,#FFFDE7)}",
    ".wf-node.active>.wf-row>.wf-label{color:var(--gold,#FFEB3B)}",
    ".wf-node.active>.wf-row{background:var(--bg2,rgba(255,235,59,.08))}",
    ".wf-kids{margin-left:11px;border-left:1px solid rgba(255,235,59,.12);padding-left:3px}",
    ".wf-kids.collapsed{display:none}",
    /* Material type roles per level */
    ".wf-l1>.wf-row .wf-label{font:600 11px/1.5 'Roboto','Noto Sans',sans-serif;letter-spacing:.13em;text-transform:uppercase}", /* Overline */
    ".wf-l2>.wf-row .wf-label{font:500 13px/1.45 'Roboto','Noto Sans',sans-serif;letter-spacing:.01em}",                          /* Subtitle2 */
    ".wf-l3>.wf-row .wf-label{font:400 12.5px/1.45 'Roboto','Noto Sans',sans-serif;letter-spacing:.015em;font-style:italic}",     /* Body2 */
    "body.wf-rail-open #atlas-fab{right:348px}",   /* clear the open rail */
    "@media(max-width:760px){#wf-rail{width:86vw}body.wf-rail-open #atlas-fab{right:18px}}"
  ].join("");
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  /* ---------- build the tree from the flat heading list ---------- */
  function levelOf(el) { return parseInt(el.tagName.charAt(1), 10); }
  var root = { level: 0, children: [], el: null, id: "__root__" };
  var stack = [root];
  heads.forEach(function (el, i) {
    if (!el.id) el.id = "wf-h-" + i;
    var lv = levelOf(el);
    var node = { level: lv, el: el, id: el.id,
                 text: (el.textContent || "").replace(/\s*✦\s*expand.*$/i, "").trim(),
                 children: [] };
    while (stack.length > 1 && stack[stack.length - 1].level >= lv) stack.pop();
    stack[stack.length - 1].children.push(node);
    node.parent = stack[stack.length - 1];
    stack.push(node);
  });

  var collapsed = {};
  try { collapsed = JSON.parse(localStorage.getItem(LS_COLLAPSED) || "{}"); } catch (e) { collapsed = {}; }
  function saveCollapsed() { try { localStorage.setItem(LS_COLLAPSED, JSON.stringify(collapsed)); } catch (e) {} }

  var byId = {};
  var zoomNode = root;

  /* ---------- render ---------- */
  var tree = document.createElement("div"); tree.id = "wf-tree";

  function renderNode(node) {
    var wrap = document.createElement("div");
    wrap.className = "wf-node wf-l" + node.level;
    wrap.dataset.id = node.id;
    byId[node.id] = wrap;

    var row = document.createElement("div"); row.className = "wf-row";
    var hasKids = node.children.length > 0;

    var caret = document.createElement("span");
    caret.className = "wf-caret" + (hasKids ? "" : " leaf");
    caret.textContent = collapsed[node.id] ? "▸" : "▾";
    row.appendChild(caret);

    var dot = document.createElement("span");
    dot.className = "wf-dot" + (hasKids ? " has-kids" : "");
    dot.textContent = "•";
    dot.title = "zoom in";
    row.appendChild(dot);

    var label = document.createElement("a");
    label.className = "wf-label";
    label.href = "#" + node.id;
    label.textContent = node.text || "(untitled)";
    row.appendChild(label);
    wrap.appendChild(row);

    var kids = null;
    if (hasKids) {
      kids = document.createElement("div");
      kids.className = "wf-kids" + (collapsed[node.id] ? " collapsed" : "");
      node.children.forEach(function (c) { kids.appendChild(renderNode(c)); });
      wrap.appendChild(kids);
      caret.addEventListener("click", function (e) {
        e.stopPropagation();
        var now = !kids.classList.contains("collapsed");
        kids.classList.toggle("collapsed", now);
        caret.textContent = now ? "▸" : "▾";
        collapsed[node.id] = now; saveCollapsed();
      });
    }

    dot.addEventListener("click", function (e) {
      e.stopPropagation();
      if (hasKids) zoomTo(node);
      else scrollToNode(node);
    });
    label.addEventListener("click", function (e) {
      e.preventDefault();
      scrollToNode(node);
    });
    return wrap;
  }

  function paint() {
    byId = {};
    tree.textContent = "";
    var base = (zoomNode === root) ? root.children : [zoomNode];
    base.forEach(function (n) { tree.appendChild(renderNode(n)); });
    renderCrumb();
  }

  function renderCrumb() {
    crumb.textContent = "";
    if (zoomNode === root) { crumb.classList.remove("show"); return; }
    crumb.classList.add("show");
    var chain = [];
    var n = zoomNode;
    while (n && n !== root) { chain.unshift(n); n = n.parent; }
    var home = document.createElement("a"); home.textContent = "⌂"; home.title = "all chapters";
    home.addEventListener("click", function () { zoomTo(root); });
    crumb.appendChild(home);
    chain.forEach(function (node, i) {
      crumb.appendChild(document.createTextNode("  ›  "));
      if (i === chain.length - 1) {
        var span = document.createElement("span"); span.textContent = node.text; crumb.appendChild(span);
      } else {
        var a = document.createElement("a"); a.textContent = node.text;
        a.addEventListener("click", function () { zoomTo(node); });
        crumb.appendChild(a);
      }
    });
  }

  function zoomTo(node) { zoomNode = node; paint(); if (node !== root) scrollToNode(node); }

  function scrollToNode(node) {
    if (node.el) node.el.scrollIntoView({ behavior: "smooth", block: "start" });
    if (history.replaceState) history.replaceState(null, "", "#" + node.id);
  }

  /* ---------- panel chrome ---------- */
  var tab = document.createElement("button");
  tab.id = "wf-tab"; tab.type = "button"; tab.textContent = "❯ Outline";
  tab.setAttribute("aria-label", "Open the outline");
  document.body.appendChild(tab);

  var rail = document.createElement("aside");
  rail.id = "wf-rail"; rail.setAttribute("aria-label", "Document outline");
  var head = document.createElement("div"); head.id = "wf-head";
  var ttl = document.createElement("b"); ttl.textContent = "Outline";
  var x = document.createElement("button"); x.className = "wf-x"; x.type = "button"; x.textContent = "×"; x.setAttribute("aria-label", "Close outline");
  head.appendChild(ttl); head.appendChild(x);
  var crumb = document.createElement("div"); crumb.id = "wf-crumb";
  rail.appendChild(head); rail.appendChild(crumb); rail.appendChild(tree);
  document.body.appendChild(rail);

  function setOpen(open) {
    rail.classList.toggle("open", open);
    document.body.classList.toggle("wf-rail-open", open);
    tab.style.display = open ? "none" : "block";
    try { localStorage.setItem(LS_OPEN, open ? "1" : "0"); } catch (e) {}
  }
  tab.addEventListener("click", function () { setOpen(true); });
  x.addEventListener("click", function () { setOpen(false); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && rail.classList.contains("open")) setOpen(false);
    if (e.key === "\\" && (e.metaKey || e.ctrlKey)) { e.preventDefault(); setOpen(!rail.classList.contains("open")); }
  });

  paint();
  var savedOpen = null;
  try { savedOpen = localStorage.getItem(LS_OPEN); } catch (e) {}
  setOpen(savedOpen === "1");

  /* ---------- scroll-spy: highlight + reveal the current heading ---------- */
  var visible = {};
  var spy = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) visible[en.target.id] = en.boundingClientRect.top;
      else delete visible[en.target.id];
    });
    var bestId = null, bestTop = Infinity;
    Object.keys(visible).forEach(function (id) {
      if (visible[id] < bestTop) { bestTop = visible[id]; bestId = id; }
    });
    if (!bestId) return;
    Object.keys(byId).forEach(function (id) { byId[id].classList.remove("active"); });
    var el = byId[bestId];
    if (!el) return;             // outside the current zoom view
    el.classList.add("active");
    // reveal ancestors (uncollapse) and bring into rail view
    var p = el.parentNode;
    while (p && p !== tree) {
      if (p.classList && p.classList.contains("wf-kids")) p.classList.remove("collapsed");
      p = p.parentNode;
    }
    var r = el.getBoundingClientRect(), tr = tree.getBoundingClientRect();
    if (r.top < tr.top || r.bottom > tr.bottom) el.scrollIntoView({ block: "center" });
  }, { rootMargin: "-10% 0px -75% 0px" });
  heads.forEach(function (h) { spy.observe(h); });
})();
