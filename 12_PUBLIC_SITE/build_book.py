#!/usr/bin/env python3
"""Render the pure Emergentism reader stack into book/index.html.

A Network-State-style free online book: sticky chapter table-of-contents, scroll
progress, deep-linkable sections, inline evidence-tier chips, light/dark reading
themes. Output is fully self-contained (no external resource references) so it
passes the 12_PUBLIC_SITE predeploy supply-chain gate. This .py is
.vercelignored (build tooling, not shipped). Source authority stays with the
three Emergentism documents named below; the result is only a public snapshot.

Run:  python3 -B build_book.py
"""
import os, re, sys
import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SOURCES = [
    os.path.join(ROOT, "00_THE_WELTANSCHAUUNG_ONE_SITTING.md"),
    os.path.join(ROOT, "06_ONTOLOGY", "08_THE_HUMAN_CONDITION.md"),
    os.path.join(ROOT, "01_TELEOLOGY", "04_THE_LIVED_COMPASS.md"),
]
OUT_DIR = os.path.join(HERE, "book")
OUT = os.path.join(OUT_DIR, "index.html")

TIER_RE = re.compile(r'\[(A|B|S|I|D|C)((?:/[A-Z]+)*)\]')

def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s).strip()

def wrap_tiers(htmltext):
    def repl(m):
        first = m.group(1).lower()
        return f'<span class="tier t-{first}">[{m.group(1)}{m.group(2)}]</span>'
    return TIER_RE.sub(repl, htmltext)

def build():
    missing = [source for source in SOURCES if not os.path.exists(source)]
    if missing:
        sys.exit(f"book source not found: {missing[0]}")
    bodies = []
    for source in SOURCES:
        text = open(source, encoding="utf-8").read()
        text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, flags=re.S)
        bodies.append(text.strip())
    raw = "\n\n---\n\n".join(bodies)

    md = markdown.Markdown(extensions=["extra", "toc", "sane_lists"])
    body = md.convert(raw)
    # Repository Markdown sources are not deployed. Route their links to the
    # public source boundary instead of emitting dead filesystem-relative URLs.
    body = re.sub(r'href="[^"#]*\.md(?:#[^"]*)?"', 'href="../sources/"', body)
    body = wrap_tiers(body)

    # Split into chapter sections at each <h1 id=...>.
    heads = re.findall(r'<h1 id="([^"]+)">(.*?)</h1>', body, flags=re.S)
    parts = re.split(r'(<h1 id="[^"]+">.*?</h1>)', body, flags=re.S)

    # pass 1: collect chapters
    chapters = []
    pre = parts[0]  # anything before the first h1 (normally empty)
    i = 1
    while i < len(parts):
        h1 = parts[i]
        content = parts[i + 1] if i + 1 < len(parts) else ""
        m = re.match(r'<h1 id="([^"]+)">(.*?)</h1>', h1, flags=re.S)
        chapters.append((m.group(1), strip_tags(m.group(2)), content))
        i += 2

    # pass 2: build sections with prev/next chapter nav
    sections, toc = [], []
    for idx, (hid, htitle, content) in enumerate(chapters):
        first = (idx == 0)
        cls = "chapter overture" if first else "chapter"
        # The chapter number badge (skip the front-matter overture).
        badge = "" if first else f'<span class="ch-num">{idx:02d}</span>'
        nav_bits = []
        if idx > 0:
            phid, ptitle, _ = chapters[idx - 1]
            plabel = "Overture" if idx == 1 else ptitle
            nav_bits.append(f'<a class="ch-prev" href="#{phid}">← {plabel}</a>')
        if idx < len(chapters) - 1:
            nhid, ntitle, _ = chapters[idx + 1]
            nav_bits.append(f'<a class="ch-next" href="#{nhid}">{ntitle} →</a>')
        nav = f'<nav class="ch-nav" aria-label="Chapter navigation">{"".join(nav_bits)}</nav>' if nav_bits else ""
        sections.append(
            f'<section class="{cls}" id="{hid}">'
            f'<header class="ch-head">{badge}<h1 id="{hid}-h">{htitle}</h1></header>'
            f'<div class="ch-body">{content}</div>{nav}</section>')
        label = "Overture" if first else htitle
        toc.append(
            f'<a class="toc-link{" is-overture" if first else ""}" href="#{hid}" data-target="{hid}">'
            f'<span class="toc-n">{"·" if first else f"{idx:02d}"}</span>'
            f'<span class="toc-t">{label}</span></a>')

    body_html = pre + "\n".join(sections)
    toc_html = "\n".join(toc)
    n_ch = len(chapters) - 1
    words = len(re.findall(r"\w+", strip_tags(body)))

    page = TEMPLATE
    page = page.replace("%%TOC%%", toc_html)
    page = page.replace("%%BODY%%", body_html)
    page = page.replace("%%NCH%%", str(n_ch))
    page = page.replace("%%WORDS%%", f"{words:,}")

    os.makedirs(OUT_DIR, exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(page)
    print(f"wrote {OUT}")
    print(f"  chapters: {n_ch} (+overture)   words: {words:,}   bytes: {len(page):,}")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en" data-reading-theme="light">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>The Book — Emergentism</title>
<meta name="description" content="Emergentism, the whole book, free to read online: P∞ = φ · ν = 1 as manifold identity, P_node = Φ × V as finite action rule, read from seven positions. Every claim wears its evidence tier; the book ends by dissolving itself." />
<meta name="color-scheme" content="light dark" />
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='13' fill='none' stroke='%23b8862c' stroke-width='2'/%3E%3Ccircle cx='16' cy='16' r='2.4' fill='%23b8862c'/%3E%3C/svg%3E" />
<style>
/* Self-hosted Roboto (Apache-2.0) — accessible and gate-safe */
@font-face{font-family:'Roboto';font-style:normal;font-weight:100 900;font-display:optional;src:url('../assets/fonts/Roboto-latin.woff2') format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Roboto';font-style:normal;font-weight:100 900;font-display:optional;src:url('../assets/fonts/Roboto-greek.woff2') format('woff2');unicode-range:U+0370-0377,U+037A-037F,U+0384-038A,U+038C,U+038E-03A1,U+03A3-03FF}
@font-face{font-family:'Roboto Mono';font-style:normal;font-weight:100 700;font-display:optional;src:url('../assets/fonts/RobotoMono-latin.woff2') format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Roboto Mono';font-style:normal;font-weight:100 700;font-display:optional;src:url('../assets/fonts/RobotoMono-greek.woff2') format('woff2');unicode-range:U+0370-0377,U+037A-037F,U+0384-038A,U+038C,U+038E-03A1,U+03A3-03FF}
:root{
  --serif:"Hoefler Text","Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --sans:"Roboto",-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
  --mono:"Roboto Mono",ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  --measure:40rem; --shape-lg:16px; --shape-full:999px; --target-min:48px;
}
/* ---- light (parchment) reading theme : default ---- */
html[data-reading-theme="light"]{
  --bg:#FDFAF4; --bg2:#FAF7F0; --panel:#F2EDE3;
  --ink:#18160E; --ink-soft:#4A4438; --ink-faint:#7A7062;
  --rule:rgba(24,22,14,.14); --rule-soft:rgba(24,22,14,.08);
  --gold:#92650A; --gold-bright:#7a5408;
  --t-a:#1565C0; --t-b:#92650A; --t-s:#1d7e70; --t-i:#92650A; --t-d:#6d6d6d; --t-c:#6f4fa0;
  --shadow:0 1px 0 rgba(255,255,255,.5);
}
/* ---- dark (void) reading theme ---- */
html[data-reading-theme="dark"]{
  --bg:#050505; --bg2:#0e0e0e; --panel:#101010;
  --ink:#F3F4F6; --ink-soft:#9CA3AF; --ink-faint:#6b7280;
  --rule:rgba(243,244,246,.13); --rule-soft:rgba(243,244,246,.07);
  --gold:#FFEB3B; --gold-bright:#FFF176;
  --t-a:#7fb2e6; --t-b:#FFEB3B; --t-s:#5fc6b0; --t-i:#e8d24a; --t-d:#a3a3a3; --t-c:#b59ce0;
  --shadow:none;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:var(--serif);font-size:20px;line-height:1.72;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
  font-feature-settings:"liga" 1,"onum" 1,"kern" 1;}
::selection{background:rgba(184,134,44,.26)}
a{color:inherit}

/* progress bar */
.progress{position:fixed;top:0;left:0;height:3px;width:0;z-index:60;
  background:linear-gradient(90deg,var(--gold),var(--gold-bright));transition:width .12s linear}

/* topbar */
.bookbar{position:sticky;top:0;z-index:50;display:flex;align-items:center;justify-content:space-between;
  gap:1rem;min-height:64px;padding:.7rem clamp(1rem,3vw,1.6rem);
  background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:blur(10px);
  border-bottom:1px solid var(--rule-soft)}
.bookbar .brand{font-family:var(--sans);font-weight:600;font-size:1.05rem;letter-spacing:0}
.bookbar .brand b{color:var(--gold)}
.bookbar nav{display:flex;align-items:center;gap:.4rem;font-family:var(--mono);font-size:.76rem}
.bookbar nav a,.bookbar nav button{color:var(--ink-soft);background:none;border:1px solid transparent;
  min-height:var(--target-min);display:inline-flex;align-items:center;border-radius:var(--shape-full);padding:0 .75rem;cursor:pointer;font:inherit;letter-spacing:0}
.bookbar nav a:hover,.bookbar nav button:hover{color:var(--gold);border-color:var(--rule)}
#toc-toggle{display:none}

/* layout */
.book-shell{display:grid;grid-template-columns:clamp(240px,22vw,310px) minmax(0,1fr);
  max-width:1320px;margin:0 auto}
/* TOC */
.toc{position:sticky;top:52px;align-self:start;height:calc(100vh - 52px);overflow-y:auto;
  padding:2rem 1rem 4rem 1.4rem;border-right:1px solid var(--rule-soft);
  scrollbar-width:thin}
.toc-head{font-family:var(--mono);font-size:.68rem;letter-spacing:0;text-transform:uppercase;
  color:var(--ink-faint);margin:0 0 1rem .2rem}
.toc-link{display:flex;gap:.7rem;align-items:baseline;padding:.32rem .4rem;border-radius:5px;
  text-decoration:none;color:var(--ink-soft);line-height:1.3;transition:.16s}
.toc-link .toc-n{font-family:var(--mono);font-size:.66rem;color:var(--ink-faint);min-width:1.4em;text-align:right;flex:none}
.toc-link .toc-t{font-size:.9rem;font-family:var(--sans)}
.toc-link:hover{color:var(--ink);background:var(--bg2)}
.toc-link.is-active{color:var(--gold);background:var(--bg2)}
.toc-link.is-active .toc-n{color:var(--gold)}
.toc-link.is-overture .toc-t{font-style:italic}

/* reading column */
.reading{padding:clamp(1.5rem,4vw,3.5rem) clamp(1.1rem,5vw,2rem) 6rem;min-width:0}
.reading-inner{max-width:var(--measure);margin:0 auto}
.chapter{padding:2.2rem 0 1rem;border-top:1px solid var(--rule-soft)}
.chapter.overture{border-top:0;padding-top:.5rem}
.chapter:first-of-type{border-top:0}
.ch-head{margin:0 0 1.4rem}
.ch-num{display:block;font-family:var(--mono);font-size:.72rem;letter-spacing:0;color:var(--gold);margin-bottom:.7rem}
.ch-body>h1:first-child,.chapter>header h1{margin-top:0}
h1{font-family:var(--serif);font-weight:600;font-size:clamp(1.9rem,4.2vw,2.9rem);line-height:1.08;
  letter-spacing:0;margin:.2rem 0 1rem;text-wrap:balance}
.overture .ch-head h1{font-size:clamp(2.6rem,6vw,4rem)}
h2{font-family:var(--serif);font-weight:600;font-size:clamp(1.25rem,2.4vw,1.6rem);line-height:1.2;
  margin:2.4rem 0 .8rem;letter-spacing:0}
h3{font-family:var(--mono);font-weight:600;font-size:.82rem;letter-spacing:0;text-transform:uppercase;
  color:var(--ink-faint);margin:2rem 0 .6rem}
p{margin:0 0 1.15rem}
.reading-inner>.chapter .ch-body>p:first-of-type{margin-top:.2rem}
/* drop cap on the first paragraph of each non-overture chapter */
.chapter:not(.overture) .ch-body>p:first-of-type::first-letter{
  font-family:var(--serif);font-weight:600;float:left;font-size:3.6em;line-height:.78;
  padding:.04em .12em 0 0;color:var(--gold)}
strong{font-weight:600}
em{font-style:italic}
code{font-family:var(--mono);font-size:.86em;background:var(--bg2);padding:.06em .35em;border-radius:3px;
  overflow-wrap:anywhere;word-break:break-word}
pre{max-width:100%;font-family:var(--mono);font-size:.9em;background:var(--bg2);padding:.75rem;border-radius:6px;overflow-x:auto}
hr{border:0;height:1px;background:var(--rule);margin:2.4rem auto;width:42%}
blockquote{margin:1.6rem 0;padding:.4rem 0 .4rem 1.3rem;border-left:2px solid var(--gold);
  color:var(--ink-soft);font-style:italic}
ul,ol{margin:0 0 1.15rem;padding-left:1.4rem}
li{margin:.3rem 0}
table{border-collapse:collapse;width:100%;margin:1.4rem 0;font-size:.9rem}
th,td{border:1px solid var(--rule);padding:.5rem .7rem;text-align:left}
th{background:var(--bg2);font-family:var(--mono);font-weight:600;font-size:.8rem}

/* tier chips */
.tier{font-family:var(--mono);font-size:.72em;font-weight:600;padding:.04em .34em;border-radius:3px;
  white-space:nowrap;border:1px solid currentColor;line-height:1.4;vertical-align:baseline}
.tier.t-a{color:var(--t-a)} .tier.t-b{color:var(--t-b)} .tier.t-s{color:var(--t-s)}
.tier.t-i{color:var(--t-i)} .tier.t-d{color:var(--t-d)} .tier.t-c{color:var(--t-c)}

/* heading anchor on hover */
h1[id],h2[id]{scroll-margin-top:70px;position:relative}

/* chapter prev/next nav */
.ch-nav{display:flex;justify-content:space-between;gap:1rem;margin:2.4rem 0 .2rem;padding-top:1.1rem;
  border-top:1px solid var(--rule-soft);font-family:var(--sans);font-size:.85rem}
.ch-nav a{color:var(--ink-soft);text-decoration:none;max-width:46%;overflow:hidden;
  text-overflow:ellipsis;white-space:nowrap;transition:color .15s}
.ch-nav a:hover{color:var(--gold)}
.ch-nav .ch-next{margin-left:auto;text-align:right}

/* footer */
.book-foot{border-top:1px solid var(--rule);margin-top:3rem;padding:3rem clamp(1rem,5vw,2rem);text-align:center}
.book-foot .phi{font-family:var(--serif);font-size:1.7rem;color:var(--gold);margin-bottom:.6rem}
.book-foot p{color:var(--ink-faint);font-family:var(--mono);font-size:.76rem;max-width:54ch;margin:0 auto .4rem}
.book-foot a{color:var(--ink-soft);text-decoration:underline;text-underline-offset:3px}

/* mobile */
@media(max-width:900px){
  body{font-size:18px}
  .bookbar{align-items:flex-start;flex-wrap:wrap}
  .bookbar nav{width:100%;justify-content:flex-start;overflow-x:auto;scrollbar-width:none}
  .bookbar nav::-webkit-scrollbar{display:none}
  .bookbar nav a,.bookbar nav button{flex:0 0 auto;white-space:nowrap}
  #toc-toggle{display:inline-block}
  .book-shell{grid-template-columns:1fr}
  .toc{position:fixed;top:0;left:0;height:100vh;width:min(84vw,330px);z-index:55;background:var(--panel);
    border-right:1px solid var(--rule);clip-path:inset(0 100% 0 0);opacity:0;visibility:hidden;pointer-events:none;
    transition:clip-path .28s cubic-bezier(.2,.7,.2,1),opacity .18s ease;padding-top:3.4rem}
  html.toc-open .toc{clip-path:inset(0);opacity:1;visibility:visible;pointer-events:auto;box-shadow:0 0 60px rgba(0,0,0,.4)}
  html.toc-open .toc-scrim{position:fixed;inset:0;z-index:54;background:rgba(0,0,0,.45)}
  pre{overflow-x:hidden;white-space:pre-wrap}
  pre code{white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word}
}
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .progress,.toc{transition:none}
}
@media(prefers-reduced-transparency:reduce){
  .bookbar{background:var(--bg);backdrop-filter:none}
}
</style>
</head>
<body>
<div class="progress" id="progress"></div>

<header class="bookbar">
  <a class="brand" href="../">Emergent<b>ism</b></a>
  <nav>
    <button id="toc-toggle" aria-label="Contents">☰ Contents</button>
    <a href="../">↑ Site</a>
    <a href="../read/">Library</a>
    <button id="theme-toggle" aria-label="Toggle reading theme" title="Toggle reading theme">◐</button>
  </nav>
</header>

<div class="book-shell">
  <aside class="toc" id="toc" aria-label="Table of contents">
    <div class="toc-head">The Book · %%NCH%% chapters · %%WORDS%% words</div>
    %%TOC%%
  </aside>
  <main class="reading">
    <div class="reading-inner">
      %%BODY%%
      <footer class="book-foot">
        <div class="phi">⊙ = • × ○</div>
        <p>This reader distills the current <a href="../dimensions/">dimension-first spine</a>, <a href="../practice/">Lived Compass</a>, and <a href="../record/">correction record</a>.</p>
        <p>Its highest success is that you can put it down.</p>
      </footer>
    </div>
  </main>
</div>

<script>
(function(){
  var root=document.documentElement;
  // theme: default light, honor stored choice
  try{var t=localStorage.getItem("emergentism-reading-theme");if(t)root.setAttribute("data-reading-theme",t);}catch(e){}
  var tt=document.getElementById("theme-toggle");
  if(tt)tt.addEventListener("click",function(){
    var cur=root.getAttribute("data-reading-theme")==="dark"?"light":"dark";
    root.setAttribute("data-reading-theme",cur);
    try{localStorage.setItem("emergentism-reading-theme",cur);}catch(e){}
  });
  // mobile TOC drawer
  var tg=document.getElementById("toc-toggle"), toc=document.getElementById("toc");
  function closeToc(){root.classList.remove("toc-open");var s=document.querySelector(".toc-scrim");if(s)s.remove();}
  if(tg)tg.addEventListener("click",function(){
    if(root.classList.contains("toc-open")){closeToc();return;}
    root.classList.add("toc-open");
    var s=document.createElement("div");s.className="toc-scrim";s.addEventListener("click",closeToc);document.body.appendChild(s);
  });
  toc&&toc.addEventListener("click",function(e){if(e.target.closest(".toc-link"))closeToc();});
  // progress bar
  var bar=document.getElementById("progress");
  function onScroll(){
    var h=document.documentElement;var max=h.scrollHeight-h.clientHeight;
    bar.style.width=(max>0?(h.scrollTop/max*100):0)+"%";
  }
  window.addEventListener("scroll",onScroll,{passive:true});onScroll();
  // scroll-spy: highlight current chapter in TOC
  var links={};document.querySelectorAll(".toc-link").forEach(function(a){links[a.dataset.target]=a;});
  if("IntersectionObserver" in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(en){
        if(en.isIntersecting){
          var a=links[en.target.id];if(!a)return;
          document.querySelectorAll(".toc-link.is-active").forEach(function(x){x.classList.remove("is-active");});
          a.classList.add("is-active");
          a.scrollIntoView({block:"nearest"});
        }
      });
    },{rootMargin:"-15% 0px -75% 0px"});
    document.querySelectorAll("section.chapter").forEach(function(s){io.observe(s);});
  }
})();
</script>
<script defer src="/assets/js/workflowy-outline.js"></script>
<script defer src="/assets/js/atlas-drawer.js"></script>
<script defer src="/assets/js/book-ai.js"></script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
