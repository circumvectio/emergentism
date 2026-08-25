/* The key-free book — bounded local retrieval over book/rag_index.json.
   BM25 search runs entirely in the browser. This public asset accepts no API
   key, stores no credential, and contacts no model endpoint. A future live
   compute service requires a separate server-side authorization and security
   boundary. All rendering is DOM-built; corpus text is never injected as HTML. */
(function () {
  "use strict";
  if (window.__bookAI) return;
  window.__bookAI = true;

  var GOLD = "#FFEB3B", INK = "#050505", CREAM = "#FFFDE7";
  var onBookPage = /^\/book\//.test(location.pathname);

  /* ---------- styles ---------- */
  var css = [
    "#ask-fab{position:fixed;left:18px;bottom:18px;z-index:9000;background:" + INK + ";color:" + CREAM + ";",
    "min-width:48px;min-height:48px;border:1px solid rgba(255,235,59,.55);border-radius:999px;padding:10px 16px;font:600 13px/1 'Roboto','Noto Sans',sans-serif;",
    "letter-spacing:0;cursor:pointer;opacity:.92}",
    "#ask-fab:hover{background:" + GOLD + ";color:" + INK + "}",
    "#ask-panel{position:fixed;top:0;left:0;bottom:0;width:min(440px,94vw);z-index:9001;background:rgba(5,5,5,.97);",
    "border-right:1px solid rgba(255,235,59,.35);clip-path:inset(0 100% 0 0);opacity:0;visibility:hidden;pointer-events:none;",
    "transition:clip-path .22s ease,opacity .22s ease,visibility 0s linear .22s;",
    "display:flex;flex-direction:column;font-family:'Roboto','Noto Sans',sans-serif;color:" + CREAM + ";backdrop-filter:blur(6px)}",
    "#ask-panel.open{clip-path:inset(0);opacity:1;visibility:visible;pointer-events:auto;transition:clip-path .22s ease,opacity .22s ease}",
    "#ask-head{display:flex;gap:8px;align-items:center;padding:14px 14px 8px}",
    "#ask-head b{color:" + GOLD + ";font-size:13px;letter-spacing:0}",
    "#ask-head button{margin-left:auto;min-width:48px;min-height:48px;background:none;border:0;color:" + CREAM + ";font-size:16px;cursor:pointer;opacity:.7}",
    "#ask-head button:hover{opacity:1;color:" + GOLD + "}",
    "#ask-mode{padding:0 16px 8px;font:400 11px/1.4 'Roboto Mono',monospace;color:#8a8568}",
    "#ask-log{flex:1;overflow-y:auto;padding:6px 16px}",
    ".ask-msg{margin:10px 0;font-size:14px;line-height:1.55}",
    ".ask-q{color:" + GOLD + ";font-weight:600}",
    ".ask-a{color:" + CREAM + "}",
    ".ask-a p{margin:6px 0}",
    ".ask-src{display:block;margin:4px 0 0 10px;padding:6px 10px;border-left:2px solid rgba(255,235,59,.5);",
    "font-size:13px;color:#cfcab0;text-decoration:none}",
    ".ask-src:hover{color:" + GOLD + "}",
    ".ask-src small{display:block;color:#8a8568;font-size:11.5px;margin-top:2px}",
    "#ask-form{display:flex;gap:8px;padding:12px 14px;border-top:1px solid #222}",
    "#ask-in{flex:1;padding:10px 12px;background:#111;border:1px solid #333;border-radius:8px;color:" + CREAM + ";",
    "min-height:48px;font:400 14px/1.3 'Roboto','Noto Sans',sans-serif;outline:none}",
    "#ask-in:focus{border-color:" + GOLD + "}",
    "#ask-go{min-width:48px;min-height:48px;background:" + GOLD + ";color:" + INK + ";border:0;border-radius:8px;padding:0 16px;font-weight:700;cursor:pointer}",
    ".expand-btn{display:inline-grid;place-items:center;min-width:48px;min-height:48px;margin:6px 0 0 8px;padding:7px 12px;border:1px solid rgba(255,235,59,.4);",
    "border-radius:999px;background:none;color:" + GOLD + ";font:600 11px/1.4 'Roboto','Noto Sans',sans-serif;",
    "letter-spacing:0;cursor:pointer;vertical-align:middle;opacity:.75}",
    ".expand-btn:hover{opacity:1;background:rgba(255,235,59,.12)}",
    ".expand-out{margin:10px 0 4px;padding:12px 16px;border-left:2px solid " + GOLD + ";background:rgba(255,235,59,.04);font-size:14.5px}",
    ".expand-out h4{margin:0 0 6px;color:" + GOLD + ";font-size:12px;letter-spacing:0}",
    ".bookbar #ask-fab{position:static;left:auto;bottom:auto;z-index:auto;flex:0 0 auto;width:48px;height:48px;",
    "padding:0;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;font-size:0;line-height:1;opacity:1}",
    ".bookbar #ask-fab::before{content:'✦';font-size:17px;line-height:1;color:inherit}",
    "@media(max-width:680px){#ask-fab{left:12px;bottom:calc(env(safe-area-inset-bottom,0px) + 12px);",
    "width:48px;height:48px;padding:0;border-radius:50%;display:flex;align-items:center;justify-content:center;",
    "font-size:0;line-height:1}#ask-fab::before{content:'✦';font-size:19px;line-height:1;color:inherit}}"
  ].join("");
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  /* ---------- retrieval (BM25) ---------- */
  var index = null, loading = null;

  function tokenize(s) {
    return (s.toLowerCase().normalize("NFKD").match(/[a-z0-9φνηθωγβμ]+/g) || []);
  }

  function loadIndex() {
    if (index) return Promise.resolve(index);
    if (loading) return loading;
    loading = fetch("/book/rag_index.json").then(function (r) { return r.json(); }).then(function (j) {
      var docs = j.passages.map(function (p) {
        var terms = tokenize(p.title + " " + p.text);
        var tf = {};
        terms.forEach(function (t) { tf[t] = (tf[t] || 0) + 1; });
        return { p: p, tf: tf, len: terms.length };
      });
      var df = {}, N = docs.length, avg = 0;
      docs.forEach(function (d) {
        avg += d.len;
        Object.keys(d.tf).forEach(function (t) { df[t] = (df[t] || 0) + 1; });
      });
      avg /= (N || 1);
      index = { docs: docs, df: df, N: N, avg: avg };
      return index;
    });
    return loading;
  }

  function search(query, k, excludeHrefPrefix) {
    var q = tokenize(query);
    var K1 = 1.4, B = 0.75;
    var scored = index.docs.map(function (d) {
      var s = 0;
      q.forEach(function (t) {
        var f = d.tf[t];
        if (!f) return;
        var idf = Math.log(1 + (index.N - index.df[t] + 0.5) / (index.df[t] + 0.5));
        s += idf * (f * (K1 + 1)) / (f + K1 * (1 - B + B * d.len / index.avg));
      });
      return { s: s, p: d.p };
    }).filter(function (r) {
      if (r.s <= 0) return false;
      if (excludeHrefPrefix && r.p.href.indexOf(excludeHrefPrefix) === 0) return false;
      return true;
    });
    scored.sort(function (a, b) { return b.s - a.s; });
    return scored.slice(0, k || 5).map(function (r) { return r.p; });
  }

  /* ---------- chat panel ---------- */
  var fab = document.createElement("button");
  fab.id = "ask-fab";
  fab.type = "button";
  fab.setAttribute("aria-label", "Ask the book");
  fab.setAttribute("title", "Ask the book");
  fab.setAttribute("aria-controls", "ask-panel");
  fab.setAttribute("aria-expanded", "false");
  fab.textContent = "✦ ASK THE BOOK";
  var bookbarNav = document.querySelector(".bookbar nav");
  var atlasFab = document.getElementById("atlas-fab");
  if (bookbarNav && atlasFab && atlasFab.parentNode === bookbarNav) {
    bookbarNav.insertBefore(fab, atlasFab);
  } else {
    (bookbarNav || document.body).appendChild(fab);
  }

  var panel = document.createElement("aside");
  panel.id = "ask-panel";
  panel.setAttribute("aria-label", "Ask the book — corpus chat");
  panel.setAttribute("aria-hidden", "true");
  document.body.appendChild(panel);

  var head = document.createElement("div"); head.id = "ask-head";
  var ttl = document.createElement("b"); ttl.textContent = "ASK THE BOOK";
  var x = document.createElement("button"); x.type = "button"; x.textContent = "×"; x.setAttribute("aria-label", "Close"); x.style.marginLeft = "auto";
  head.appendChild(ttl); head.appendChild(x);
  panel.appendChild(head);

  var modeEl = document.createElement("div"); modeEl.id = "ask-mode"; panel.appendChild(modeEl);
  var log = document.createElement("div"); log.id = "ask-log"; log.setAttribute("role", "log"); log.setAttribute("aria-live", "polite"); panel.appendChild(log);

  var form = document.createElement("form"); form.id = "ask-form";
  var input = document.createElement("input"); input.id = "ask-in"; input.type = "text";
  input.placeholder = "ask the weltanschauung…"; input.autocomplete = "off";
  input.setAttribute("aria-label", "Ask the book");
  var go = document.createElement("button"); go.id = "ask-go"; go.type = "submit"; go.textContent = "ASK";
  form.appendChild(input); form.appendChild(go);
  panel.appendChild(form);

  modeEl.textContent = "key-free local retrieval · corpus passages only · no external endpoint";

  function addMsg(cls, text) {
    var d = document.createElement("div");
    d.className = "ask-msg " + cls;
    text.split(/\n{2,}|\n/).forEach(function (para) {
      if (!para.trim()) return;
      var p = document.createElement("p");
      p.textContent = para;
      d.appendChild(p);
    });
    log.appendChild(d);
    log.scrollTop = log.scrollHeight;
    return d;
  }

  function addSources(container, passages) {
    passages.forEach(function (p, i) {
      var a = document.createElement("a");
      a.className = "ask-src";
      a.href = p.href;
      a.textContent = "[" + (i + 1) + "] " + p.title;
      var sm = document.createElement("small");
      sm.textContent = p.text.slice(0, 180) + "…";
      a.appendChild(sm);
      container.appendChild(a);
    });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var q = input.value.trim();
    if (!q) return;
    input.value = "";
    addMsg("ask-q", q);
    var thinking = addMsg("ask-a", "…");
    loadIndex().then(function () {
      var hits = search(q, 5);
      if (!hits.length) { thinking.textContent = "Nothing in the corpus matches that — try other words."; return; }
      thinking.textContent = "The corpus answers in its own words:";
      addSources(thinking, hits);
    });
  });

  function setPanelOpen(open, restoreFocus) {
    panel.classList.toggle("open", open);
    panel.setAttribute("aria-hidden", String(!open));
    fab.setAttribute("aria-expanded", String(open));
    if (open) {
      loadIndex();
      input.focus();
    } else if (restoreFocus) {
      fab.focus();
    }
  }
  fab.addEventListener("click", function () { setPanelOpen(true, false); });
  x.addEventListener("click", function () { setPanelOpen(false, true); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && panel.classList.contains("open")) setPanelOpen(false, true);
  });

  /* ---------- per-section expansion (book page only) ---------- */
  if (!onBookPage) return;

  function expandSection(heading, btn) {
    btn.disabled = true;
    btn.textContent = "✦ expanding…";
    var sectionText = "";
    var node = heading.nextElementSibling;
    while (node && !/^H[12]$/.test(node.tagName) && sectionText.length < 900) {
      sectionText += " " + node.textContent;
      node = node.nextElementSibling;
    }
    var query = heading.textContent + " " + sectionText.slice(0, 300);
    loadIndex().then(function () {
      var anchor = heading.id ? "#" + heading.id : "";
      var hits = search(query, 4, "/book/" + anchor);
      var out = document.createElement("div");
      out.className = "expand-out";
      var h4 = document.createElement("h4");
      out.appendChild(h4);
      function done() {
        heading.parentNode.insertBefore(out, heading.nextSibling);
        btn.textContent = "✦ expanded";
      }
      h4.textContent = "DEEPER IN THE CORPUS";
      addSources(out, hits);
      done();
    });
  }

  Array.prototype.slice.call(document.querySelectorAll(".ch-body h2[id]")).forEach(function (h) {
    var btn = document.createElement("button");
    btn.className = "expand-btn";
    btn.type = "button";
    btn.textContent = "✦ expand";
    btn.setAttribute("aria-label", "Expand this section");
    btn.addEventListener("click", function () { expandSection(h, btn); }, { once: true });
    h.appendChild(btn);
  });
})();
