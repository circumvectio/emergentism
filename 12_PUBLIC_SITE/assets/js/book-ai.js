/* The AI-leveraged book — retrieval-augmented reading.
   Static-first: BM25 retrieval over book/rag_index.json runs entirely in the
   browser (no keys, no external calls). If the reader configures an LLM
   endpoint (settings ⚙ — stored in localStorage, sent only to the endpoint
   they choose), the chat and per-section expansion upgrade from quoted
   passages to generated prose grounded in those passages (RAG).
   All rendering is DOM-built; corpus text and model output are never
   injected as HTML. */
(function () {
  "use strict";
  if (window.__bookAI) return;
  window.__bookAI = true;

  var GOLD = "#FFEB3B", INK = "#050505", CREAM = "#FFFDE7";
  var LS_KEY = "emergentism-llm-endpoint";
  var onBookPage = /^\/book\//.test(location.pathname);

  /* ---------- styles ---------- */
  var css = [
    "#ask-fab{position:fixed;left:18px;bottom:18px;z-index:9000;background:" + INK + ";color:" + CREAM + ";",
    "border:1px solid rgba(255,235,59,.55);border-radius:999px;padding:10px 16px;font:600 13px/1 'Roboto','Noto Sans',sans-serif;",
    "letter-spacing:.08em;cursor:pointer;opacity:.92}",
    "#ask-fab:hover{background:" + GOLD + ";color:" + INK + "}",
    "#ask-panel{position:fixed;top:0;left:0;bottom:0;width:min(440px,94vw);z-index:9001;background:rgba(5,5,5,.97);",
    "border-right:1px solid rgba(255,235,59,.35);clip-path:inset(0 100% 0 0);opacity:0;visibility:hidden;pointer-events:none;",
    "transition:clip-path .22s ease,opacity .22s ease,visibility 0s linear .22s;",
    "display:flex;flex-direction:column;font-family:'Roboto','Noto Sans',sans-serif;color:" + CREAM + ";backdrop-filter:blur(6px)}",
    "#ask-panel.open{clip-path:inset(0);opacity:1;visibility:visible;pointer-events:auto;transition:clip-path .22s ease,opacity .22s ease}",
    "#ask-head{display:flex;gap:8px;align-items:center;padding:14px 14px 8px}",
    "#ask-head b{color:" + GOLD + ";font-size:13px;letter-spacing:.14em}",
    "#ask-head button{background:none;border:0;color:" + CREAM + ";font-size:16px;cursor:pointer;opacity:.7}",
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
    "font:400 14px/1.3 'Roboto','Noto Sans',sans-serif;outline:none}",
    "#ask-in:focus{border-color:" + GOLD + "}",
    "#ask-go{background:" + GOLD + ";color:" + INK + ";border:0;border-radius:8px;padding:0 16px;font-weight:700;cursor:pointer}",
    "#ask-settings{display:none;padding:10px 16px;border-top:1px solid #222;font-size:12.5px}",
    "#ask-settings.open{display:block}",
    "#ask-settings label{display:block;margin:8px 0 3px;color:#cfcab0;letter-spacing:.04em}",
    "#ask-settings input,#ask-settings select{width:100%;padding:7px 10px;background:#111;border:1px solid #333;",
    "border-radius:6px;color:" + CREAM + ";font:400 12.5px/1.2 'Roboto Mono',monospace;outline:none}",
    "#ask-settings .note{margin-top:8px;color:#8a8568;font-size:11px;line-height:1.5}",
    ".expand-btn{display:inline-block;margin:6px 0 0 8px;padding:3px 10px;border:1px solid rgba(255,235,59,.4);",
    "border-radius:999px;background:none;color:" + GOLD + ";font:600 11px/1.4 'Roboto','Noto Sans',sans-serif;",
    "letter-spacing:.06em;cursor:pointer;vertical-align:middle;opacity:.75}",
    ".expand-btn:hover{opacity:1;background:rgba(255,235,59,.12)}",
    ".expand-out{margin:10px 0 4px;padding:12px 16px;border-left:2px solid " + GOLD + ";background:rgba(255,235,59,.04);font-size:14.5px}",
    ".expand-out h4{margin:0 0 6px;color:" + GOLD + ";font-size:12px;letter-spacing:.12em}"
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

  /* ---------- LLM endpoint (owner-configured, optional) ---------- */
  function getCfg() {
    try { return JSON.parse(localStorage.getItem(LS_KEY) || "null"); } catch (e) { return null; }
  }
  function setCfg(cfg) { localStorage.setItem(LS_KEY, JSON.stringify(cfg)); }

  function llmAvailable() {
    var c = getCfg();
    return !!(c && c.url && c.key);
  }

  function askLLM(system, user) {
    var c = getCfg();
    var isAnthropic = (c.style || "anthropic") === "anthropic";
    var body, headers = { "content-type": "application/json" };
    if (isAnthropic) {
      headers["x-api-key"] = c.key;
      headers["anthropic-version"] = "2023-06-01";
      headers["anthropic-dangerous-direct-browser-access"] = "true";
      body = { model: c.model || "claude-sonnet-4-6", max_tokens: 1024, system: system,
               messages: [{ role: "user", content: user }] };
    } else {
      headers.authorization = "Bearer " + c.key;
      body = { model: c.model || "gpt-4o-mini", max_tokens: 1024,
               messages: [{ role: "system", content: system }, { role: "user", content: user }] };
    }
    return fetch(c.url, { method: "POST", headers: headers, body: JSON.stringify(body) })
      .then(function (r) {
        if (!r.ok) throw new Error("endpoint returned " + r.status);
        return r.json();
      })
      .then(function (j) {
        if (isAnthropic) return (j.content && j.content[0] && j.content[0].text) || "";
        return (j.choices && j.choices[0] && j.choices[0].message.content) || "";
      });
  }

  function ragPrompt(passages) {
    var ctx = passages.map(function (p, i) {
      return "[" + (i + 1) + "] " + p.title + " (" + p.href + ")\n" + p.text;
    }).join("\n\n");
    return "You answer questions about Emergentism, a metaphysical framework, using ONLY the " +
      "passages provided. Tier-honest: established maths is [A], structural claims [S], " +
      "interpretive readings [I], conjectures [C] — keep those distinctions when the passages " +
      "make them. Cite passages as [1], [2]. If the passages do not answer it, say so plainly.\n\n" +
      "PASSAGES:\n" + ctx;
  }

  /* ---------- chat panel ---------- */
  var fab = document.createElement("button");
  fab.id = "ask-fab";
  fab.type = "button";
  fab.setAttribute("aria-label", "Ask the book");
  fab.textContent = "✦ ASK THE BOOK";
  document.body.appendChild(fab);

  var panel = document.createElement("aside");
  panel.id = "ask-panel";
  panel.setAttribute("aria-label", "Ask the book — corpus chat");
  document.body.appendChild(panel);

  var head = document.createElement("div"); head.id = "ask-head";
  var ttl = document.createElement("b"); ttl.textContent = "ASK THE BOOK";
  var gear = document.createElement("button"); gear.type = "button"; gear.textContent = "⚙"; gear.setAttribute("aria-label", "LLM endpoint settings");
  var x = document.createElement("button"); x.type = "button"; x.textContent = "×"; x.setAttribute("aria-label", "Close"); x.style.marginLeft = "auto";
  head.appendChild(ttl); head.appendChild(x); head.insertBefore(gear, x);
  panel.appendChild(head);

  var modeEl = document.createElement("div"); modeEl.id = "ask-mode"; panel.appendChild(modeEl);
  var log = document.createElement("div"); log.id = "ask-log"; panel.appendChild(log);

  var settings = document.createElement("div"); settings.id = "ask-settings";
  function field(labelText, inputEl) {
    var l = document.createElement("label"); l.textContent = labelText;
    settings.appendChild(l); settings.appendChild(inputEl);
    return inputEl;
  }
  var styleSel = document.createElement("select");
  ["anthropic", "openai-compatible"].forEach(function (v) {
    var o = document.createElement("option"); o.value = v; o.textContent = v; styleSel.appendChild(o);
  });
  field("API style", styleSel);
  var urlIn = field("Endpoint URL", Object.assign(document.createElement("input"), { type: "url", placeholder: "https://api.anthropic.com/v1/messages" }));
  var modelIn = field("Model", Object.assign(document.createElement("input"), { type: "text", placeholder: "claude-sonnet-4-6" }));
  var keyIn = field("API key", Object.assign(document.createElement("input"), { type: "password", placeholder: "sk-…" }));
  var note = document.createElement("div"); note.className = "note";
  note.textContent = "Stored only in this browser (localStorage) and sent only to the endpoint you set. " +
    "Leave empty to stay key-free: answers then quote the corpus directly.";
  settings.appendChild(note);
  panel.appendChild(settings);

  var form = document.createElement("form"); form.id = "ask-form";
  var input = document.createElement("input"); input.id = "ask-in"; input.type = "text";
  input.placeholder = "ask the weltanschauung…"; input.autocomplete = "off";
  var go = document.createElement("button"); go.id = "ask-go"; go.type = "submit"; go.textContent = "ASK";
  form.appendChild(input); form.appendChild(go);
  panel.appendChild(form);

  function refreshMode() {
    modeEl.textContent = llmAvailable()
      ? "RAG mode: retrieval + your configured model"
      : "key-free mode: the corpus answers in its own words · ⚙ to connect a model";
    var c = getCfg();
    if (c) { styleSel.value = c.style || "anthropic"; urlIn.value = c.url || ""; modelIn.value = c.model || ""; keyIn.value = c.key || ""; }
  }
  refreshMode();

  [styleSel, urlIn, modelIn, keyIn].forEach(function (el) {
    el.addEventListener("change", function () {
      setCfg({ style: styleSel.value, url: urlIn.value.trim(), model: modelIn.value.trim(), key: keyIn.value });
      refreshMode();
    });
  });

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
      if (llmAvailable()) {
        askLLM(ragPrompt(hits), q).then(function (answer) {
          thinking.textContent = "";
          answer.split(/\n{2,}/).forEach(function (para) {
            if (!para.trim()) return;
            var p = document.createElement("p"); p.textContent = para; thinking.appendChild(p);
          });
          addSources(thinking, hits);
        }).catch(function (err) {
          thinking.textContent = "Endpoint error (" + err.message + ") — falling back to the corpus's own words.";
          addSources(thinking, hits);
        });
      } else {
        thinking.textContent = "The corpus answers in its own words:";
        addSources(thinking, hits);
      }
    });
  });

  fab.addEventListener("click", function () { panel.classList.add("open"); loadIndex(); input.focus(); });
  x.addEventListener("click", function () { panel.classList.remove("open"); });
  gear.addEventListener("click", function () { settings.classList.toggle("open"); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") panel.classList.remove("open"); });

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
      if (llmAvailable()) {
        h4.textContent = "EXPANDED · grounded in the corpus";
        askLLM(ragPrompt(hits),
          "Expand this section of the book with one level more depth, staying strictly within " +
          "the cited passages and the section itself. Section “" + heading.textContent + "”: " +
          sectionText.slice(0, 700)
        ).then(function (answer) {
          answer.split(/\n{2,}/).forEach(function (para) {
            if (!para.trim()) return;
            var p = document.createElement("p"); p.textContent = para; out.appendChild(p);
          });
          addSources(out, hits);
          done();
        }).catch(function () {
          h4.textContent = "DEEPER IN THE CORPUS (endpoint error — key-free fallback)";
          addSources(out, hits);
          done();
        });
      } else {
        h4.textContent = "DEEPER IN THE CORPUS";
        addSources(out, hits);
        done();
      }
    });
  }

  Array.prototype.slice.call(document.querySelectorAll("h2[id]")).forEach(function (h) {
    var btn = document.createElement("button");
    btn.className = "expand-btn";
    btn.type = "button";
    btn.textContent = "✦ expand";
    btn.setAttribute("aria-label", "Expand this section");
    btn.addEventListener("click", function () { expandSection(h, btn); }, { once: true });
    h.appendChild(btn);
  });
})();
