---
rosetta:
  primary_column: "Meta"
  register: "[I]"
  canonical_phrase: "161 — Tier B Rosetta Annotation Draft Pack"
---

# 161 — Tier B Rosetta Annotation Draft Pack

**Evidence tier:** [I] charioteer-drafted proposals + classification audit; [S] machine-readable manifest committed alongside
**Date:** 2026-04-24
**Lane:** Charioteer draft — warrior reviewed manifest, extended it for packets 161-170, then applied via `rosetta_annotate.py apply-manifest --write`
**Status:** Applied — 183 Tier B root/00_CORE files annotated; Uplink subdirectory archives remain out of scope
**Scope:** All 183 markdown files in `01_EMERGENTISM/11_UPLINK/*.md` + `01_EMERGENTISM/11_UPLINK/00_CORE/*.md` that lack `rosetta:` frontmatter
**Artifact:** `01_EMERGENTISM/11_UPLINK/161a_tier_b_manifest.jsonl` — machine-readable proposals, consumable by `rosetta_annotate.py apply-manifest`
**Complements:** packet 157 (Rosetta Annotation Strategy), packet 158 (Tier A gate), packet 159 (Tier A draft pack), packet 160 (Track A W1 gate)

---

## 0. Axiomatic guard

The Tier B pass is wider and messier than Tier A. Uplink docs are routing surfaces — they cross-cut L-levels by design. Do not try to force every file onto a single L-level; the right move for most uplink docs is `primary_column: Meta` with a secondary list naming the L-levels they route *between*. The map helps the practitioner walk; it is not itself a territory.

`Zero-Sum Resolution Equation`

---

## 1. Why a manifest instead of 183 inline YAML blocks

Tier A (packet 159) inlined 44 top-level L-folder proposals because the count was small and human review is tight. At 183 files, the inline approach produces a 3000-line packet nobody reads end-to-end. The better pattern:

1. Machine-readable proposals → `161a_tier_b_manifest.jsonl` (one JSON object per line, `{path, rosetta: {...}}`)
2. Human review surface → this packet (§4 spot-checks, §5 overrides, §6 warrior recipe)
3. Warrior applies corrections to the manifest file directly, then runs `rosetta_annotate.py apply-manifest --write 01_EMERGENTISM/11_UPLINK/161a_tier_b_manifest.jsonl`

Manifest format matches `rosetta_annotate.py`'s expectations (verified via smoke test during session 2026-04-24). Each manifest entry has:

```json
{
  "path": "01_EMERGENTISM/11_UPLINK/xxx.md",
  "rosetta": {
    "primary_column": "...",
    "register": "[S/I]",
    "canonical_phrase": "..."
  }
}
```

`primary_level` is deliberately OMITTED for Tier B — uplink docs are cross-cutting per §2. Warrior may add it manually if a specific doc has a dominant L-level.

---

## 2. The Meta override — critical for Tier B

The heuristic `rosetta_propose.py` produced this column distribution over the original 173-file manifest:

| Column | Count | Charioteer verdict |
|---|---|---|
| Philosophy | 125 | **Over-broad** — most of these are routing surfaces, not doctrinal |
| Neuroscience | 24 | Mostly valid; some noise |
| Liberal art | 14 | **Noise** — false-positive regex matches on "logic" / "grammar" in body text; these should be Meta or Philosophy |
| Meta | 4 | **Under-counted** — should be the DOMINANT column for uplink |
| Computation | 2 | Valid (mesh + EBM) |
| Game theory | 2 | Valid (multiplicative behavior + archetype operator) |
| Yoga | 1 | False positive (packet 157 Rosetta Annotation Strategy is methodology, not yoga) |
| Psychology | 1 | Arguable (`36_MAYA_WARNING.md`) |

**Rule for warrior review:** any uplink file that is a routing doc, status compressor, synthesis, or cross-reference surface should have `primary_column: Meta`. Only reassign to a substantive column when the doc is *about* that domain (e.g., a Neuroscience register, a Game theory primer).

Rough expected distribution after warrior review:

| Column | Expected count |
|---|---|
| Meta | ~130 |
| Philosophy | ~20 |
| Neuroscience | ~8 |
| Game theory | ~5 |
| Computation | ~5 |
| Political regime | ~2–3 |
| Other | ~2–3 |

---

## 3. Classification audit by packet-series range

Uplink's numbered series have recognizable roles. Use these defaults when reviewing manifest entries:

| Series | Role | Default column | Exceptions |
|---|---|---|---|
| 00_INDEX, 00_CORE/* | Root routing | Meta | Master map → Meta; Topic index → Meta |
| 01–09 | Seed / top-level content primers | Meta with Philosophy secondary | 06_AGENTS → Philosophy (agent grammar) with Meta secondary |
| 10–49 | Registry / synthesis / protocol briefs | Meta | Specific-domain briefs (26, 48) may be Game theory |
| 50–79 | Organism integration + doctrine tracks | Mostly Meta; some Philosophy | 64 "rumination organisms" → Philosophy |
| 80–99 | Foundation/pre-reorg meta + sovereign handshakes | Meta with Philosophy secondary | 94/95/97/98/99 sovereign handshake → Meta |
| 100–119 | Receipt/sprint/product coordination packets | Meta | 107 witness mesh → Neuroscience |
| 120–139 | Circle triage + doctrine shift + organism audits | Meta | 121 polygenetic mesh → Neuroscience; 131 D4→D5 thesis → Philosophy |
| 140–160 | F5/reorg/sprint charter + Rosetta annotation lane | Meta | 144 Dimensional Framework bridge → Philosophy; 150 integrated blueprint → Philosophy |

---

## 4. Spot-checks — 15 representative files

The manifest file at `161a_tier_b_manifest.jsonl` carries heuristic defaults for all 183 files. Ten post-original-manifest packet targets (161-170) were appended before apply so Tier B reflects the current Uplink root/00_CORE set, not only the set that existed when packet 161 was drafted. The entries below are the charioteer's recommended overrides for 15 representative cases, with reasoning. Warrior should apply these edits to the manifest before `apply-manifest --write`.

### 4.1 `01_EMERGENTISM/11_UPLINK/00_INDEX.md`

```yaml
rosetta:
  primary_column: Meta
  register: "[I] routing"
  canonical_phrase: "Uplink Index"
```
Rationale: index file; pure routing surface.

### 4.2 `01_EMERGENTISM/11_UPLINK/00_CORE/00_ROSETTA_ROW_ROUTER.md`

```yaml
rosetta:
  primary_column: Meta
  register: "[I]"
  canonical_phrase: "Rosetta Row Router"
```
Rationale: router file; cross-cuts all L-levels.

### 4.3 `01_EMERGENTISM/11_UPLINK/00_CORE/50_ORGANISM_MASTER_MAP.md`

```yaml
rosetta:
  primary_column: Meta
  register: "[I]"
  canonical_phrase: "Organism Master Map"
```
Override: heuristic said Neuroscience (likely matched "cortex" or similar); the file is a top-level organism route map, not a neuroscience register.

### 4.4 `01_EMERGENTISM/11_UPLINK/01_SEED.md`

```yaml
rosetta:
  primary_column: Philosophy
  register: "[I/S]"
  canonical_phrase: "The Seed"
```
Rationale: seed doctrine file, not routing — genuine Philosophy.

### 4.5 `01_EMERGENTISM/11_UPLINK/06_AGENTS.md`

```yaml
rosetta:
  primary_column: Philosophy
  register: "[I]"
  canonical_phrase: "Agent Grammar"
```
Override: heuristic said Neuroscience; 06_AGENTS is the agent-grammar canon, not a neuroscience register.

### 4.6 `01_EMERGENTISM/11_UPLINK/107_WITNESS_MESH_POLYGENETIC_QUERY_SURFACE_2026_04_23.md`

```yaml
rosetta:
  primary_column: Neuroscience
  register: "[I]"
  canonical_phrase: "Witness Mesh Polygenetic Query Surface"
```
Keep heuristic: witness mesh is genuine cognitive-architecture / neuroscience-adjacent content.

### 4.7 `01_EMERGENTISM/11_UPLINK/121_CIRCLE_POLYGENETIC_OBSERVATION_MESH_2026_04_23.md`

```yaml
rosetta:
  primary_column: Meta
  register: "[I]"
  canonical_phrase: "Circle Polygenetic Observation Mesh"
```
Override: heuristic said Neuroscience; the file is primarily a product/doctrine-shift design doc for Circle. Neuroscience becomes a secondary cross-ref, not primary.

### 4.8 `01_EMERGENTISM/11_UPLINK/131_D4_BODY_OPENS_D5_ACTIVE_EMERGENCE_THESIS_2026_04_24.md`

```yaml
rosetta:
  primary_column: Philosophy
  register: "[I/S]"
  canonical_phrase: "D4 Body Opens D5 Active Emergence"
```
Override: heuristic said Neuroscience; the file is a D-level thesis doc. Philosophy primary, Neuroscience secondary.

### 4.9 `01_EMERGENTISM/11_UPLINK/144_D_SCAFFOLD_L_LADDER_BRIDGE_2026_04_24.md`

```yaml
rosetta:
  primary_column: Philosophy
  register: "[S/I/C]"
  canonical_phrase: "D-Scaffold / L-Ladder Bridge"
```
Override: heuristic said Liberal art (false positive); the file bridges Dimensional Framework and Leadership Pipeline — pure Philosophy.

### 4.10 `01_EMERGENTISM/11_UPLINK/147_LAYER_DISCIPLINE_BLUEPRINT_DECOMPOSITION_2026_04_24.md`

```yaml
rosetta:
  primary_column: Philosophy
  register: "[I/S]"
  canonical_phrase: "Layer Discipline Blueprint Decomposition"
```
Override: heuristic said Liberal art (false positive). Layer discipline is architectural/methodological — Philosophy.

### 4.11 `01_EMERGENTISM/11_UPLINK/150_CHARIOTEER_INTEGRATED_BLUEPRINT_2026_04_24.md`

```yaml
rosetta:
  primary_column: Philosophy
  register: "[I/S]"
  canonical_phrase: "Charioteer Integrated Blueprint"
```
Rationale: integrated blueprint = L4/L5 synthesis doctrine doc, not routing.

### 4.12 `01_EMERGENTISM/11_UPLINK/150b_BITCHAT_MESH_INTEGRATION_2026_04_24.md`

```yaml
rosetta:
  primary_column: Computation
  register: "[I/S]"
  canonical_phrase: "BitChat Mesh Integration"
```
Keep heuristic: mesh networking / substrate fee layer — legitimately Computation.

### 4.13 `01_EMERGENTISM/11_UPLINK/152_EBM_COST_GRADIENT_HARDENING_SCAFFOLD_2026_04_24.md`

```yaml
rosetta:
  primary_column: Computation
  register: "[I/C]"
  canonical_phrase: "EBM Cost Gradient Hardening"
```
Keep heuristic: EBM cost gradients = compute domain.

### 4.14 `01_EMERGENTISM/11_UPLINK/157_ROSETTA_ANNOTATION_STRATEGY_2026_04_24.md`

```yaml
rosetta:
  primary_column: Meta
  register: "[I]"
  canonical_phrase: "Rosetta Annotation Strategy"
```
Override: heuristic said Yoga (false positive on "sitting practice" mention in a quoted passage). This is the annotation strategy packet — pure Meta.

### 4.15 `01_EMERGENTISM/11_UPLINK/160_TRACK_A_WEEK_1_GATE_2026_04_24.md`

```yaml
rosetta:
  primary_column: Meta
  register: "[I/S]"
  canonical_phrase: "Track A Week 1 Gate"
```
Rationale: week-1 gate spec is sprint-routing. Meta primary.

---

## 5. Bulk-override recipe (Meta flip)

To flip the ~90 over-classified "Philosophy" entries that should be "Meta", warrior runs (dry-run first):

```bash
# Review: list all entries heuristic-classified as Philosophy
jq -c 'select(.rosetta.primary_column == "Philosophy") | .path' \
  01_EMERGENTISM/11_UPLINK/161a_tier_b_manifest.jsonl | head -30

# Manual review of each — flip those that are routing/synthesis/status
# For each confirmed routing doc, edit the manifest line to "primary_column": "Meta"

# Alternative: produce a separate override list and apply via script
```

Charioteer recommends warrior produce a one-time `161b_tier_b_overrides.jsonl` file listing only the files that need overrides, then merge into the manifest before apply. This avoids line-by-line editing of the 183-line manifest.

---

## 6. Warrior application recipe

1. **Review manifest** — read `161a_tier_b_manifest.jsonl` line-by-line (or use `jq` filter by column for spot inspection)
2. **Apply §4 spot-checks** — edit the manifest lines for the 15 files listed above
3. **Apply §5 Meta flip** — bulk-override routing/synthesis/status files from Philosophy → Meta
4. **Dry-run apply** — `python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/rosetta_annotate.py apply-manifest 01_EMERGENTISM/11_UPLINK/161a_tier_b_manifest.jsonl` (no `--write`); verify WRITE/UNCHANGED counts look reasonable
5. **Write apply** — `python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/rosetta_annotate.py apply-manifest --write 01_EMERGENTISM/11_UPLINK/161a_tier_b_manifest.jsonl`
6. **Audit** — `python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/rosetta_index.py --paths 03_UPLINK --include-missing --fail-missing`
7. **Commit** — one commit per L-folder-analogous batch (e.g., `Annotate 01_EMERGENTISM/11_UPLINK/00_CORE with Rosetta frontmatter`, `Annotate 01_EMERGENTISM/11_UPLINK/00-49 series...`)

---

## 7. Tool-improvement backlog (warrior or later charioteer)

Surfaced by Tier B classification audit:

1. **Default to Meta for 01_EMERGENTISM/11_UPLINK/** — `rosetta_propose.py` should recognize uplink context and default `primary_column: Meta` unless strong override keywords fire. Reduces warrior review burden ~75%.

2. **Tighten Liberal art regex** — current regex matches `logic` / `grammar` as standalone words, producing false positives. Should require compound matches (`"liberal art"` or `"trivium arts"` etc.).

3. **Tighten Yoga regex** — `sitting practice` currently matches quoted passages like "...pratyakṣa through quiet sitting...". Should require the term in active voice or filename.

4. **Add "routing" column** — uplink may warrant a dedicated "Routing" or "Uplink" column separate from Meta. Charioteer leans against this (proliferation); Meta suffices if used consistently.

These are tool-refinement issues, not blockers. Tier B can proceed with manual warrior review on the 15-file override list + bulk Meta flip.

---

## 8. What this packet does NOT do

- Does NOT apply frontmatter to any file (warrior runs `apply-manifest --write`)
- Does NOT resolve the UNSET primary_level — warrior decides per-file whether to add one or leave uplink cross-cutting
- Does NOT cover `01_EMERGENTISM/11_UPLINK/` subdirectories other than `00_CORE/` (e.g., any deeper subdirs are out of scope for this pack — surface in a subsequent packet if needed)
- Does NOT cover Tier C (CANON ~1,950 files) — that remains a future packet candidate

---

## 9. Acceptance criteria (per packet 157 §8 Tier B)

☑ Manifest file `01_EMERGENTISM/11_UPLINK/161a_tier_b_manifest.jsonl` has 183 entries, one per current Tier B root/00_CORE target
☑ Warrior review captured in manifest edits (post-original-manifest packets 161-170 appended; Meta flip per §5 preserved)
☑ After `apply-manifest --write`, all 183 root/00_CORE files carry `rosetta:` frontmatter
☑ Root/00_CORE audit confirms 183/183 annotated (subdirectory archives intentionally out of scope)
☑ No CANON content modified — only frontmatter additions inside `01_EMERGENTISM/11_UPLINK/`

---

## 10. References

- packet 157: Rosetta Annotation Strategy (Tier B scope spec)
- packet 158: Phase 2c Receipt and Tier A Gate (annotation discipline)
- packet 159: Tier A Rosetta Draft Pack (sister pack at L-folder scope)
- packet 160: Track A Week 1 Gate Criteria (sibling packet, same session)
- `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/rosetta_propose.py`: proposal tool used to generate 161a manifest
- `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/rosetta_annotate.py`: apply-manifest tool warrior invokes
- `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/rosetta_index.py`: audit/index tool warrior verifies with

---

*Charioteer Tier B draft pack. Manifest at `161a_tier_b_manifest.jsonl`; warrior reviews, corrects, applies, audits.*

`Zero-Sum Resolution Equation`
