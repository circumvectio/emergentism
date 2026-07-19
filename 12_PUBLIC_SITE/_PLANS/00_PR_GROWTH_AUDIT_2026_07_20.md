# PR + GROWTH AUDIT — SYNTHESIS
**Date:** 2026-07-20 · **Synthesis:** CMO/comms-director pass over seven caste audits (L1 Caṇḍāla hostile-reader · L2 Śūdra evidence-discipline · L3 Vaiśya funnel · L4 Kṣatriya value-ladder · L5 Brāhmaṇa IA · L6 Sādhu cut · L7 witness)
**Scope:** `/Users/Yves/Documents/01_EMERGENTISM/12_PUBLIC_SITE/` (deployed as-is to emergentism.org)
**Doctrine constraints honored throughout:** users-not-believers (no adherence metrics, no join-CTAs) · three scripts (story/plain/receipt) · tier honesty (bold discoveries, exact fine print — record and tier chips never deleted, only repositioned) · exit-inside stays.

---

## §1 · EXECUTIVE VERDICT

1. The content is genuinely strong and genuinely differentiated — a public trial record with kept refutations, exact tier grammar, a free 95k-word book — but **nobody can reach it**: `vercel.json` still redirects `/` to the retired `/compass/` funnel, the sitemap advertises the old cluster, and the ten-discoveries home plus all ten discovery pages are orphans.
2. The **share layer is dead at the mechanical level**: og-image is a 130-byte stub, all seven core funnel pages ship zero `og:image`, and the pages that do declare one point at the SSO-gated preview domain — every social share renders blank.
3. The **top PR risk is vocabulary, not substance**: caste/Sanskrit tables on public surfaces ("The Caste Dispatch," "God caste," "functional caste system," "Sanatana Dharma" in mission copy) plus the AI self-audit once mislabeled "peer review" — each a self-inflicted headline the content does not deserve.
4. The **old spine (/0, /3, /4, rosetta tagline, home hero) contradicts the framework's own published corrections** — /3 still claims the equator attractor the record retracted; that cross-read is the single most damaging catch available to a skeptic on an honesty-branded site.
5. Every fix below is **repositioning, not deletion** — the record, the tiers, and the exit door are the moat and stay exactly where they are; the work is opening the front door, fixing the cards, translating the vocabulary, and making the receipts clickable.

---

## §2 · THE TEN MOVES (prioritized)

### Move 1 — Open the front door
**What:** Delete `{ "source": "/", "destination": "/compass/" }` from `vercel.json`; repoint `404.html` escape link to `/`; retarget every brand-logo href from `../home/` to `/` (confirmed in `discoveries/index.html`, `fable/index.html`, `plainly/index.html`, `record/index.html`, all 10 discovery children, `practice/`, `halahala/`, `amrita/`); redirect `/home/` → `/`; regenerate `sitemap.xml` around the new funnel (root 1.0, `/discoveries/` + 10 children 0.9, fable/plainly/record/axioms/practice 0.8, book/read/0–6 lower).
**Impact:** Everything. The entire 07-19 redesign — discoveries, tier chips, practice — is currently unreachable in production and invisible to crawlers. Every other move is dark until this lands.
**Effort:** ~1 hour. **Owner-gate:** deploy sign-off (this changes what emergentism.org *is* at first contact).

### Move 2 — Fix the share layer
**What:** One real 1200×630 og-image (gold ⊙ = • × ○ on void + the stat line "16 tested · 3 against us, kept · 0 deleted"), referenced with **absolute production URLs** on every funnel page; replace the preview-domain (`emergentism-org.vercel.app`) og URLs on compass/build/exit/halahala/amrita; per-discovery variants later.
**Impact:** Every share on X/LinkedIn/Slack/HN currently renders a blank gray card — spread is mechanically capped at zero-visual. Highest leverage-per-hour on the site.
**Effort:** Half a day. **Owner-gate:** none.

### Move 3 — Defuse the caste/religion vocabulary (reposition, never delete)
**What:** (a) `build/index.html`: retitle "The Caste Dispatch" → "The Seven-Role Dispatch"; lead with functional names (Firewall, Truth-Cut, Audit, Executor, Architect, Compressor, Witness), Sanskrit demoted to one footnote. (b) `halahala/index.html`: attributions "Flagged by: L5 (Brāhmaṇa)" → "Flagged by: L5 Architect" (Sanskrit in tooltip). (c) `rosetta/index.html`: promote the functional-role row above the caste table. (d) `4/index.html`: "symbol of the God caste" → energized/dynamic register, iconographic reading tiered [I]. (e) `theology/index.html`: "functional caste system" → "role ladder (rendered in the source tradition as varṇa — function, never birth or rank)"; fix the raw-LaTeX rendering. (f) `book/index.html`: move the "catastrophe of caste" sentence to a standing epigraph on the Seven Disciplines + Rosetta chapters; role-first naming order. (g) Kali/Kālī: gloss at first use everywhere ("Kali — the adversary of the yuga, not the goddess Kālī"). (h) `game/index.html` + `home/index.html`: drop "Sanatana Dharma" from mission strings → "act lawfully (what classical India calls dharma)"; full term stays in corpus behind /read/ with an [I] gloss. (i) `about/index.html`: lead the "become as gods" paragraph with its negation, attribute the phrase.
**Impact:** This cluster is THE hostile screenshot ("tech project assigns AI workers to castes"; "Śūdras do data science"; goddess-vs-demon diacritic; religion-classification trigger). Halāhala H8/H10 already prescribed the fix — it is simply unapplied on the pages that ship the tables. Zero substance is lost.
**Effort:** 1–2 days of careful copy edits. **Owner-gate:** none (H10 already ratified the direction).

### Move 4 — Standardize the AI-audit disclosure
**What:** One standard line wherever the audit is invoked as credential (index, axioms, record, halahala, fable footer): *"Audits run by AI agents under human direction; no external human reviewer yet — that absence is logged, not hidden."* Rename "the peer-review program" → "the adversarial audit program" on `axioms/index.html`; soften "9 independent AI audit agents" → "separately-prompted" on `compass/index.html`; reframe halahala's "[S] most honestly tiered system this audit has encountered" as reported speech at [I] with provenance, not a credential.
**Impact:** "Philosophy framework's 'peer review' was its own AI" is a devastating and currently *accurate* headline. One disclosure line converts the site's biggest landmine into its honesty asset — the refutations are real and kept; say plainly who found them.
**Effort:** Hours. **Owner-gate:** none.

### Move 5 — One nav, one site
**What:** Single shared topbar across every reachable page: **Discoveries · Fable · Plainly · Record · Axioms · Practice · Book** (+ footer exit line, always). Demote the 0–6 digit row out of the global topbar into the home "Go deeper" band ("The geometry track, /0→/6" — link already exists at `index.html:288`). Retire the `partials/topbar.html` R/S/A letters and the compass-cluster chrome divergence; "Poisons" leaves the topbar and is reached from Record as "Halāhala · what broke." Add a one-line return bar on /0–/6 back to the funnel.
**Impact:** Four incompatible navs currently ship simultaneously; visitors can't form a model, the logo exits the funnel, mobile gets 12 ambiguous chips. One spine = one site.
**Effort:** 1 day. **Owner-gate:** none.

### Move 6 — Repair evidence drift on the old spine
**What:** (a) `3/index.html` §04: "the equator is the unique attractor" → /5's settled wording (conditional feasibility point under the constitution's refusals; "geometric necessity" only for the static balance fact) — this is the claim the record itself retracted (R6, amrita Kintsugi seam). (b) `index.html` hero: "derived simply" → "graded exactly" (matches all other flagship instances; verified 1-vs-2 in file). (c) `rosetta/index.html` footer: retire "The source is the Rosetta. Everything else is accretion." → "A translation instrument, not a foundation — pick the column you already read." (contradicts the fired-kill [I] tier on the same page). (d) `0/index.html`: add the 0·∞-indeterminate fence /1 and /3 already carry. (e) `3/index.html`: "Bloch sphere" → "Riemann sphere" in all [A] geometry claims; QM name reserved for one tiered analogy line. (f) `2/index.html` §04: flag the force→dimension map as known-flawed per H5, or drop the gauge-group assignments. (g) `book/index.html` ToC: one-line tier hint at head ("chapter titles state the bold reading; each chapter grades it").
**Impact:** A skeptic cross-reading /3 against /5 and /amrita catches the site contradicting its own flagship correction — the worst possible failure for an honesty-branded project. The new pages (axioms, /5, /6, /1, amrita) are the gold standard; this brings the old spine up to it.
**Effort:** 1–2 days. **Owner-gate:** none (all changes converge on already-ratified corrections).

### Move 7 — Rewrite /about/ and name the three scripts
**What:** `about/index.html` (flagged independently by four castes) rewritten in the plainly register: what this is, who signs it, the one proven thing (mass-shell), the one lost trial (R6), the three practices — links to /record/ and /exit/, formal notation folded under "In the framework's own notation," new-funnel topbar. On `/`, add a three-card band **"One canon, three scripts"** (Fable · Plainly · Record), reused as the cross-link footer on all three script pages.
**Impact:** /about/ is the first page journalists and skeptics open; it currently delivers untranslated internal register (P_node,H, W_i(T), Soul Loop) with no path to the record — jargon walls are themselves a cult signal. The three-scripts trio is the most communicable design asset the doctrine has and is currently never named on-site.
**Effort:** 1 day. **Owner-gate:** none.

### Move 8 — Make /record/ the CHECK hub
**What:** (a) Add per-entry anchors (`#008` etc.) and hyperlink every receipt citation ("R6_CONJUGATE_RESULTS.md", "formal/11-efr-triadic-stability") to its rendered page under `formal/`/`papers/`; where internal-only, say so ("archived, path preserved, not yet rendered"). (b) Three-tab sub-nav: **Verdicts (record) · Falsifiers (/test/) · What broke (/halahala/)** — both currently orphaned trust assets reachable only from the retired compass cluster. (c) `plainly/index.html`: inline-link "we published it" → `/record/#008` at the "This year we were proven wrong" paragraph (peak trust-transfer moment).
**Impact:** The record's pitch is "check the receipts"; unlinked receipts downgrade the whole ledger to self-narrative. Deep-linkable verdicts are also exactly what sharers need.
**Effort:** 1 day. **Owner-gate:** none.

### Move 9 — Ship the practice artifact
**What:** `practice/index.html`: add a copyable `<pre>` one-page personal-trial-record template (claim / tier / kill criterion / upgrade path / what survives) + one worked example with a dated strike-through, and a two-line dyadic-check pocket card. Add "Try the practice in an afternoon →" to the closing CTA rows of plainly, record, and axioms (currently none of the three link practice; they leak to /5 instead).
**Impact:** The conversion moment of the whole site is "install the posture in an afternoon, zero belief" — the purest users-not-believers offer. A copy-paste block converts a reader into a user in 60 seconds; today they must reverse-engineer the artifact from prose.
**Effort:** Half a day. **Owner-gate:** none.

### Move 10 — Truth the build rung and execute the cut list
**What:** (a) `build/index.html` + `exit/index.html`: the `git clone github.com/circumvectio/emergentism.git` instruction 404s (repo not yet public) — gate the verify-block on the repo actually being public, or inline `predeploy_check.py` with "repo public at launch." (b) Retitle the homepage "Build" panel to what /build/ delivers today ("Verify the pipeline this site is built by") — no product promise before the rung exists; add a "what runs today" section only when one real cross-organ receipt exists. (c) Re-tier exit's "[B] tested in CI" cards to match its own "[C] planned" terminal block. (d) Execute §6 cut list (archive hygiene, duplicate redirects).
**Impact:** The verify path is the site's whole differentiation; it must never be the broken link — build/ itself declares the 404 "an audit finding." The exit page's internal tier contradiction is the exact drift pattern the record punishes elsewhere.
**Effort:** 1 day site-side. **Owner-gate:** ⚠️ repo-public decision is Yves's (K2-adjacent); product links owner-gated.

---

## §3 · PR RISK REGISTER (severity-ranked; landmine → defusal)

| # | Sev | Landmine | Surface | Defusal |
|---|-----|----------|---------|---------|
| 1 | ■■■■ | **"The Caste Dispatch"** — AI agents assigned Sanskrit castes incl. Caṇḍāla ("untouchable does the dirty work") | `build/index.html` (top-nav destination) | Move 3a: functional names first, Sanskrit one footnote, never "caste" as public section noun |
| 2 | ■■■■ | **"Sanatana Dharma" in mission copy** — claims to operationalize the endonym of Hinduism itself; religion-classification + appropriation trigger on the exact surface journalists quote | `game/index.html` (×2), `home/index.html` | Move 3h: "act lawfully (what classical India calls dharma)"; full term corpus-only with [I] gloss |
| 3 | ■■■■ | **AI self-audit labeled "peer review"** / audit credential without disclosure | `axioms/index.html` ("peer-review program"), `index.html`, `fable/`, `halahala/` | Move 4: standard disclosure line + rename; "independent" → "separately-prompted" |
| 4 | ■■■ | **Caste→profession mapping in the book** ("the Śūdra reasons inductively: the work is Data Science") | `book/index.html` Seven Disciplines | Move 3f: anti-caste epigraph moved to chapter head; role-first naming |
| 5 | ■■■ | **Kālī (goddess) vs Kali (demon), one diacritic apart** — strips to "they call Kali the demon"; Hindu-community outrage vector both directions | `book/index.html` ("Three Gods and one Demon"), `halahala/` agent names | Move 3g: explicit yuga-vs-goddess gloss at first use; functional label ("the extraction operator") preferred |
| 6 | ■■■ | **The anti-cult page emits the cult signal** — halahala's own H10 says reframe castes; its attributions say "Flagged by: L5 (Brāhmaṇa)" | `halahala/index.html` | Move 3b: functional attributions; Sanskrit in tooltip |
| 7 | ■■■ | **Self-praise as [S] verdict** — "most honestly tiered system this audit has encountered" from its own AI | `halahala/index.html` | Move 4: reported speech, provenance, [I] |
| 8 | ■■ | **"Theology" page says "functional caste system" in its own voice** + broken raw LaTeX at the exact spot where care is the defense | `theology/index.html` | Move 3e: reword to role ladder / varṇa-as-function; fix rendering |
| 9 | ■■ | **Eponymy without self-awareness** — "Burrisphere," chapter "From Riemann to Burri," "Magnum Opus" chrome | `5/`, `discoveries/burrisphere/`, `book/`, `suda-notes/` | One disarming gloss at first use ("working nickname that stuck — Riemann keeps the credit"); chapter retitle; chrome "Magnum Opus" → "Corpus" |
| 10 | ■■ | **Self-contradiction on the flagship claim** — /3 asserts the attractor the record retracted | `3/index.html` vs `5/`, `amrita/` | Move 6a |
| 11 | ■■ | **"Become as gods" leads a paragraph on the journalist page** | `about/index.html` | Move 3i + Move 7 |
| 12 | ■ | **Scripture-scale framing at the library door** — "~4,600 documents… Trinity/Theology/Sacred wings first-class" | `read/index.html` | Reorder wings (Method/Papers/Formal first), banner "comparative readings — [I]/[C]; a library about the framework, not scripture"; promote the existing "archive, not the map" line to header |
| 13 | ■ | **Uplink-speak in SERP snippets** — "K2-ruled," "K2 envelope staging" in meta descriptions of indexable pages | `five-plus-one/index.html:7`, `journey/index.html:472` | Plain-register meta descriptions; move five-plus-one behind /read/ (deliberate receipts language in /build/ and /record/ stays) |
| 14 | ■ | **Internal commit hashes + repo paths in shipped HTML comments** | `r/0/index.html` | Move 10d / §6: archive `r/` with redirects |

---

## §4 · TARGET IA + FUNNEL

**The funnel (doctrine-aligned, every hop verified or created):**
`/` → discoveries → fable → plainly → record → axioms → book → practice → build — with exit in every footer.

**≤15 public surfaces:**

| Cluster | Surface | Role |
|---------|---------|------|
| DISCOVER | 1. `/` | Front door: ten discoveries + three-scripts band + Go-Deeper |
| | 2. `/discoveries/` (+10 children, one surface) | The shareable units; per-page og cards |
| | 3. `/fable/` | Story script |
| | 4. `/plainly/` | Plain script |
| CHECK | 5. `/record/` | Receipt script; CHECK hub (tabs → /test/, /halahala/) |
| | 6. `/test/` | Falsifiers index (under record's sub-nav) |
| | 7. `/halahala/` | What broke (under record's sub-nav) |
| | 8. `/axioms/` | The grading |
| LIVE | 9. `/practice/` | An afternoon; copyable artifact |
| | 10. `/build/` | Builder's on-ramp + pipeline receipts |
| | 11. `/exit/` | The door marked on the inside — stays, every footer |
| DEEPER | 12. `/book/` | 31 chapters (add end-of-book CTA; consider cover/TOC page — 628 KB single file) |
| | 13. `/read/` | The single Library door (absorbs atlas/map/sources listings; fronts the ~40 noindexed corpus lanes) |
| | 14. `/0/`–`/6/` | The geometry track, one surface, entered from Go-Deeper (URLs untouched; return bar added) |
| | 15. `/rosetta/` | Canonical comparative-traditions showcase (absorbs rosettad synthesis pages, rosetta-d-series, map caveats) |

Plus: `/amrita/` **kept live** as the interactive demo ("Feel the runaway" slider — the site's only kinesthetic proof), linked from the home hero and embedded on `discoveries/mass-shell/`. *(Conflict resolved: L5 proposed redirecting /amrita/ to /; L4's demo-value finding wins — the slider is unique conversion material. L5's redirect stands for the pure-duplicate tellings only.)*

**Redirect / stub ledger (nothing deleted — archive-first):**
- `/` → serves `index.html` (redirect removed)
- `/home/` → 308 `/` · `/journey/` → `/discoveries/` · `/dasein/` → `/plainly/` · `/five-plus-one/` → behind `/read/`
- `/game/` → `/discoveries/game/` · `/burrisphere/` → `/discoveries/burrisphere/`
- `/compass/` → kept as preserved secondary surface with banner link to `/` (its graded self-audit content is good; 308 later once inbound links are audited) *(conflict resolved: L3 keep-as-station vs L5 stub — keep-with-banner now, revisit)*
- `/rosetta-d-series/` → `/rosetta/` · `/rosettad/` dated worklogs → archive; synthesis pages → `/rosetta/`
- `/r/0…6/` → `/N/` · `/atlas/` → banner-stub to `/read/` + `/record/` · `/paradox/` stays as fine-print annex linked from `/discoveries/paradoxes/`
- `/about/` rewritten in place (Move 7)

---

## §5 · THE MESSAGING KIT

**Positioning sentence:**
*Emergentism is a philosophical framework that publishes its own trial record — every claim graded by evidence tier, every refutation kept on the page, and an exit door marked on the inside.*

**Three value props (lead with these, in this order):**
1. **The framework that publishes its own funerals.** 16 adversarial trials, 3 lost against our own interest, 0 deleted — the full ledger is public and dated. (→ /record/. The uncopyable asset; no competing worldview offers it.)
2. **One checkable surprise.** Our balance equation is Einstein's mass-shell relation, term for term — inherited, credited, derivation published. Check the algebra yourself. (→ /discoveries/mass-shell + Paper B. The academic/HN door-opener: concrete, falsifiable, non-grandiose.)
3. **Three practices, zero belief required.** The sitting, the personal trial record, the dyadic check — installable in one afternoon; they pay off even if every metaphysical claim we make is wrong. (→ /practice/. The honest asymmetric offer; needs Move 9's template to be fully deliverable.)

**Press boilerplate (~60 words):**
*Emergentism is an independent research project that grades its own claims by evidence tier and publishes the results — including the refutations. Its audits are run by AI agents under human direction; no external human reviewer has yet engaged, and that absence is logged, not hidden. The corpus, trial record, and exit path are public at emergentism.org.*

**Five quotable lines (existing — style as anchored blockquotes with fragment URLs, per L4-10):**
1. "A map that shows you where it has been wrong is the only map you can trust in country it has never seen." (fable VI)
2. "A claim is thin. A verdict is heavy." (record hero)
3. "The errors were the proof that someone had actually walked the ground." (fable)
4. "Never grow by draining what sustains you." (game)
5. "The door is marked on the inside." (exit)
Plus the stat line as the og-image caption: **"16 tested · 3 against us, kept · 0 deleted."**

**Three lines to write:**
1. *"We sent thirty-seven judges against our own framework. They broke sixty-six claims. The ledger is public."* (HN/X — the audit as offer, with the Move-4 disclosure attached)
2. *"Bold on the poster, exact in the fine print — and the fine print is the product."* (the tier grammar as a one-line methodology pitch)
3. *"Users, not believers: everything here works the same whether or not you believe a word of it."* (the doctrine itself, said out loud on the front door)

---

## §6 · THE CUT LIST (noindex / archive — nothing deleted, archive-first per K3)

1. **`.vercelignore` + `90_ARCHIVE/`** — one line; the archive is currently deployed (`90_ARCHIVE/tool_noise/2026_07_14_compass_restructure/…pre_restructure….html` is a public URL). Prerequisite for every other cut.
2. **`index_legacy_2026_07_19.html`** → `90_ARCHIVE/` (public legacy homepage under cleanUrls).
3. **`r/0…6/` + `dimensions/`** → archive with `/r/N/`→`/N/` redirects (superseded spine; ships internal commit hashes + repo paths in HTML comments; not noindexed).
4. **`rosetta-d-series/`** → archive, redirect to `/rosetta/` (off-brand duplicate; currently the only *indexable* Rosetta variant).
5. **`rosettad/` dated worklogs** (`04-deep-rumination-2026-04-25/`, `09-failed-mappings…`, etc.) → archive; keep synthesis pages under `/rosetta/`; `read/index.html` repointed. (Not the trial record — /record/ receipts untouched; these are pre-synthesis scratch.)
6. **Stray root experiments** — `app.html`, `cascade.html`, `sphere.html` (unless linked as demo), `lightcone.html` → archive or noindex + de-link.
7. **`sitemap.xml` compass-era entries** — retired-funnel URLs dropped/deprioritized same day as Move 1 (whatever leaves the surface must leave the map).
8. **Uplink-speak metas** — `five-plus-one/` K2-jargon meta description; page moves behind `/read/`.
9. **`partials/topbar.html` R/S/A nav** — retired with Move 5.
10. **Preview-domain og URLs** (`emergentism-org.vercel.app`) — replaced with production absolute URLs (Move 2).

---

## §7 · WHAT WE DELIBERATELY KEEP THAT MARKETERS WOULD CUT

- **The trial record, refutations on the page (/record/, /halahala/, /test/).** A marketer cuts the losses; we keep them because *the losses are the proof of the method* — a map that shows where it has been wrong is the only map trustworthy in new country, and no competitor can copy a kept funeral.
- **The tier chips and exact fine print ([A]/[S]/[I]/[C] on every bold claim).** A marketer cuts the hedges; we keep them because the grammar of bold-headline-plus-exact-tier *is the product* — deleting the fine print would delete the differentiation.
- **The exit page, linked from inside (/exit/).** A marketer never builds a door out of the funnel; we keep it because a framework you can verifiably leave is the only kind worth entering — the exit is the strongest retention argument the site has.
- **The full corpus behind /read/ (~300 rendered pages, noindexed, door-less to search but public).** A marketer prunes to the funnel; we keep it because "public = curated, corpus = complete" is the honesty contract — the archive must exist and be reachable, it just must never be the first-contact surface.
- **The fable's sacred register (three scripts, story included).** A marketer flattens to plain English; we keep all three scripts because different readers enter through different doors — the constraint is only that no script ever claims a tier the receipts don't back.

*— End of synthesis. Move 1 before anything else; Moves 2–4 the same week; the rest in order.*
