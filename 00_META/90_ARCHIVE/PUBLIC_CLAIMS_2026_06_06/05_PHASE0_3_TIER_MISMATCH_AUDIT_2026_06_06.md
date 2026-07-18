# Phase 0.3 — Tier-Mismatch Audit Report

**Date:** 2026-06-06
**Status:** Phase 0.2 (504 claims) → 0.3 (audit verdict) COMPLETE
**Inputs:** [`05_PUBLIC_CLAIMS_ALL_2026_06_06.csv`](05_PUBLIC_CLAIMS_ALL_2026_06_06.csv) (504 rows × 32 pages)
**Method:** Constitutional audit against the A7 evidence-tier rule + the public-site claim discipline (no claim above `[I]` without a dated receipt).

---

## 1. Headline finding

**93.7% of public-site claims are UNSOURCED.**

Of 504 substantive claims extracted from 32 live HTML pages:

| Tier stated | Count | % of total | Verdict |
|---|---:|---:|---|
| `[A]` axiom | 10 | 2.0% | 9 downgraded to `[S]` (no source anchor) |
| `[B]` dated receipt | 2 | 0.4% | 1 downgraded to `[I]` (no source anchor) |
| `[C]` conjecture | 6 | 1.2% | retained (self-attesting) |
| `[D]` draft | 0 | 0.0% | n/a |
| `[I]` interpretive | 2 | 0.4% | retained + 2 up-tag (see §3) |
| `[S]` structural (Rosetta) | 12 | 2.4% | retained + 9 up-tag from `[A]` demotions |
| `UNSOURCED` | 472 | **93.7%** | **CONSTITUTIONAL DEFICIT** |

After audit, 11 downgrades move the stated/audit-distribution from stated → audit. The audit distribution lands at:

| Tier audit | Count | % of total |
|---|---:|---:|
| `[A]` | 1 | 0.2% |
| `[B]` | 0 | 0.0% |
| `[C]` | 6 | 1.2% |
| `[D]` | 0 | 0.0% |
| `[I]` | 4 | 0.8% |
| `[S]` | 21 | 4.2% |
| `UNSOURCED` | 472 | **93.7%** |

The 472 UNSOURCED claims are the **primary constitutional gap** between the framework's stated discipline (A7) and its public surface.

---

## 2. What the constitutional rule says

From the A7 evidence ladder (canonical in `02_EPISTEMOLOGY/01_EVIDENCE_TIERS/`):

> Every claim in the framework is labeled with one of six evidence tiers — `[A]` axiom, `[B]` receipt, `[S]` structural, `[I]` intake, `[C]` conjecture, `[D]` draft. A claim that mixes `[A]` and `[C]` evidence should be split into two rows. Report the actual tier, not the strongest tier the claim could justify; tier upgrades follow the append-only Falsifier Register.

The public-site README reinforces this:

> No claim above `[I]` without a dated receipt. `[S]` claims must point back to canonical Rosetta geometry.

**The 472 UNSOURCED claims do not violate the letter of A7 (because A7 applies to the *framework*, not the *promotional site*) — but they violate the spirit of the discipline the framework claims to embody. The site reads as if every paragraph is a free-floating interpretation, when in fact most of its substantive sentences rest on either framework axioms (`[A]/[S]`) or dated receipts (`[B]`) that are simply not labeled.**

---

## 3. The 11 downgrades in detail

All 11 are A7 self-corrections in service of the public-facing claim discipline.

| Page | Stated | Audit | Reason | Sample claim |
|---|---|---|---|---|
| `r/1/index.html` | A | S | no anchor | "Every claim in the framework is labeled with one of six evidence tiers —" |
| `r/1/index.html` | A | S | no anchor | "[A] axiom / [B] receipt / [S] structural / [I] intake" |
| `r/1/index.html` | A | S | no anchor | "The evidence ladder is a receipt ladder, not a quality ladder." |
| `r/1/index.html` | A | S | no anchor | "The Honest Position rule from the GFS Wave 1 results" |
| `r/5/index.html` | A | S | no anchor | (A-tier claims about Honest Position, Falsifier Register) |
| `r/5/index.html` | A | S | no anchor | (A-tier about constitutional 5+1 enumeration) |
| `r/5/index.html` | A | S | no anchor | (A-tier about the seven agent castes) |
| `r/5/index.html` | A | S | no anchor | (A-tier about K2 envelope) |
| `r/5/index.html` | A | S | no anchor | (A-tier about η = 0 fence) |
| `r/5/index.html` | B | I | no anchor | "[B] Honest verdict: signal in 7/23 cells, AK1 partially triggered, m" |
| (one additional) | B | I | no anchor | (B-tier claim missing date stamp) |

These are not errors. They are **cautious readings of claims that state a tier inside the text but do not anchor the claim to a dated source file**. The framework's own discipline says: a tier that cannot be tied to a receipt collapses one rung. We collapse.

Two `[I]` claims were retained (and a further 2 are up-tagged from implicit `[A]`-less statements that read as interpretation). The audit is intentionally **conservative**: when in doubt, demote.

---

## 4. Per-page claim discipline

Distribution of UNSOURCED claims (worst offenders first). Pages with <5 UNSOURCED claims are canvas-heavy and have little text to audit.

| Page | Total | UNSOURCED | % UNSOURCED | Tier-bearing |
|---|---:|---:|---:|---:|
| `r/5/index.html` (L5 Cosmology ladder) | 37 | 26 | 70% | 11 |
| `r/2/index.html` (L2 Epistemology ladder) | 22 | 21 | 95% | 1 |
| `r/3/index.html` (L3 Methodology ladder) | 24 | 24 | 100% | 0 |
| `r/4/index.html` (L4 Axiology ladder) | 16 | 14 | 88% | 2 |
| `r/6/index.html` (L6 Ontology ladder) | 18 | 17 | 94% | 1 |
| `0/index.html` (D0 Ground) | 19 | 18 | 95% | 1 |
| `3/index.html` (D3) | 42 | 39 | 93% | 3 |
| `4/index.html` (D4) | 30 | 28 | 93% | 2 |
| `5/index.html` (D5) | 41 | 35 | 85% | 6 |
| `6/index.html` (D6) | 34 | 31 | 91% | 3 |
| `soul-loop/index.html` | 22 | 20 | 91% | 2 |
| `index.html` (home) | 34 | 33 | 97% | 1 |
| `rosetta/index.html` | 17 | 12 | 71% | 5 |
| `atlas/index.html` | 12 | 11 | 92% | 1 |

**Key observation:** the 5 ladder routes (`r/0` through `r/6`) and the 7 dimension pages (`0/` through `6/`) are the **largest and most claim-dense**, and they have the **highest UNSOURCED ratios**. These are the pages that will be expanded under Phase 1–3. The constitutional deficit is concentrated where the substantive content is.

---

## 5. Rosetta-geometry coverage (the `[S]` backbone)

70 of 504 claims (13.9%) contain Rosetta geometry — canonical glyphs (φ, ν, η, ⊙, ○, •, ◇, ⚔, ☠, 💀, ✦) or canonical forms (Φ·ν=1, (φ−ν)² ≥ 0, sin θ, S², η=0, 5+1).

These are the **structurally self-attesting** claims. They do not need dated receipts because they **are** the geometry. A claim like *"the equator is the unique locus of self-symmetry"* is not asserting a historical fact; it is restating the S² model. It belongs at `[S]`.

The 70 Rosetta-geometry claims are distributed across 18 of 32 pages. They form the load-bearing backbone of the public site and the safest place to start Phase 1 (publish Master Rosetta + Canonical Formula Block + The Honest Position).

---

## 6. Source-anchor coverage

110 of 504 claims (21.8%) have a source anchor — an internal href, an `#anchor` link, a `/N/` route reference, or a `.md` file reference. 450 of 504 claims are on pages that have at least one internal link (i.e., the page-level structural property holds for 89% of pages).

The gap is **per-claim**, not **per-page**. The pages are linked; the claims are not labeled. This is the **first concrete remediation target** for Phase 5 (site engineering) and Phase 6 (continuous tier discipline).

---

## 7. Public-site discipline targets (the 472-claim remediation surface)

The 472 UNSOURCED claims can be partitioned into four remediation classes:

| Class | Disposition | Estimated count |
|---|---|---:|
| **Rosetta-geometry statements** — already self-attesting | add `[S]` label | ~50 (overlap with the 70 above) |
| **Framework axioms restated in narrative** — already canon | add `[A]` + link to source | ~30 (L1-L7 role statements, 5+1, η=0, K2) |
| **Cross-domain mappings** — comparative claims | add `[I]` + external reference | ~100 (Piaget/Kohlberg/Maslow rows, Vedic Varṇa rows) |
| **Pure narrative exposition** — pedagogical | leave UNSOURCED, mark with `<aside class="narrative">` | ~290 (introductory text, scene descriptions) |

The fourth class — pure narrative — is **not** a discipline failure. The first three classes are the remediation target.

A targeted Phase 5.3 sprint could resolve 180 of 472 claims with a `[A]/[S]/[I]` label + a source link. That would lift the tier-bearing ratio from 6.3% to **42%** without re-writing any claim, just labeling existing claims correctly.

---

## 8. Pre-launch gates derived from this audit

| Gate | Current state | Required for Phase 1 launch | Source |
|---|---|---|---|
| **G-A** | 93.7% UNSOURCED | ≤ 70% UNSOURCED, or full label sweep on the 180 remediation-target claims | this report §7 |
| **G-B** | 0 broken external CDNs (per `predeploy_check.sh`) | re-verify at launch | `12_PUBLIC_SITE/predeploy_check.sh` |
| **G-C** | 1 missing route (`dimensions/index.html` in handoff) | either create the page or update the handoff to `[D]` | this report §9 |
| **G-D** | 0 pages with `(tier=UNSOURCED) AND (claim contains arithmetic or empirical assertion)` left unflagged | implement an `[E]` (empirical) tag for the small set of arithmetic/empirical claims that look `[B]` but have no receipt | this report §10 |
| **G-E** | Master Rosetta not yet live | Phase 1 publish (next) | `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md` |

---

## 9. Anomalies surfaced (separate from the audit)

- **`dimensions/index.html` does not exist.** The handoff listed it as a 32nd page; the folder contains only `dimensions.css` and `dimensions.js`. The dimension routes (`0/` through `6/`) do work standalone. Decision: either create `dimensions/index.html` (a hub page) or update the AGENTS.md to reflect that `dimensions/` is a stylesheet+script asset folder, not a route. **Recommend the former** — the seven `/0/-/6/` routes deserve a hub.
- **`app.html`** has only 10 claims — most of its content is JavaScript-driven app surface, not text. Normal.
- **`r/3/index.html`** (Methodology ladder) has 24 claims, 0 tier-bearing. Methodology's evidence-tier discipline has not been promoted to the public site. **Phase 1.2 target.**

---

## 10. Empirical/arithmetic claims that look like receipts but lack them

A small subset (~12–18 of the 472 UNSOURCED) make empirical or arithmetic assertions that should be `[B]` once a date is attached. Examples (not exhaustive, sampled from CSV):

- "4 stages of formal reasoning (L1–L4)" — should be `[I]` (Kohlberg/Commons) with external anchor
- "5 needs + self-actualization (L4)" — should be `[I]` (Maslow) with external anchor
- "3 levels (L4 anchor at autonomy)" — should be `[I]` (Kohlberg) with external anchor
- "(φ − ν)² ≥ 0" and "ν = tan(θ/2)" / "φ = cot(θ/2)" — these are the formula block, should be `[A]` (axiom) with link to `00_CANONICAL_FORMULA_BLOCK.md`
- "1 = 0 × ∞" / "0 × ∞ = 1" — should be `[S]` (Rosetta geometry) with link to the Burri Sphere equation
- "velocity does not add linearly: two speeds of 0.6c..." — should be `[B]` (relativistic velocity addition) with date

This is the **empirical-discipline gap** (Gate G-D above). It is small but visible to a careful reader.

---

## 11. What this report does NOT cover

- **0.4 Corpus coverage matrix** — what fraction of the ~678 source doctrine documents are reachable from the public site. (Next deliverable.)
- **0.5 Asset inventory** — Three.js scenes, CSS, fonts, images, favicon, manifest, license posture. (Pending.)
- **0.6 Predeploy check verification** — does `12_PUBLIC_SITE/predeploy_check.sh` actually cover the failures the audit surfaced (external CDN, broken internal links, missing alt text, tier-marker presence)? (Pending.)
- **0.7 Manifest orphan check** — if a deployment manifest exists, are there orphan routes or dead links? (Pending.)

---

## 12. Decision recommendations (for K2 review, not yet executed)

1. **Publish Master Rosetta + Canonical Formula Block + The Honest Position** as the Phase 1 first triplet. These are the three documents that the 504-claim audit most depends on for `[A]/[S]/[I]` labels. (Phase 1 work.)
2. **Add a tier-label sweep script** to the `predeploy_check.sh` so that future page additions cannot ship with `> 70%` UNSOURCED claims. (Phase 5 work.)
3. **Create `dimensions/index.html`** as a hub for the `/0/-/6/` routes, or update the AGENTS.md to mark the folder as asset-only. (Phase 5 work.)
4. **Decide on the empirical-discipline gap** (G-D): is `[E]` (empirical-without-receipt) a legitimate tag, or should all empirical claims be downgraded to `[C]` until dated? Recommend the latter — keep the ladder at six tiers. (A7 ruling, requires K2 sign-off.)
5. **Recompile the 3 stale Uplink files** (`02_FRAMEWORK.md`, `03_ORGANISM.md`, `08_PRODUCTS.md`) before any public claim cites them. (Follow-up queue item 1, deferred from earlier session.)

---

**End of Phase 0.3.**
**Next deliverable:** Phase 0.4 — Corpus coverage matrix (source doc × public reachability).
