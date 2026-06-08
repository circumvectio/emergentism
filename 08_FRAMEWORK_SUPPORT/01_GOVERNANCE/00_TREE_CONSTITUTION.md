---

title: "Tree Constitution — the law of the seven canonical roots"
type: governance
status: active
date: 2026-05-07
owner: L7 Ṛṣi (doctrine) + L5 Brāhmaṇa (codification) + L4 Kṣatriya (enforcement)
evidence_tier: "[S] Structural — codifies pre-existing K2 directives + L5 architect packet"
ratifies:
  - 2026-04-25 reorganization (commit 73b288c5)
  - 2026-04-29 root tidy (Tiers 1–7 complete)
  - 2026-05-02 Agentz reclassification (RECLASSIFICATION_NOTICE.md)
rosetta:
  primary_level: L4
  primary_column: Philosophy
  secondary:
    - level: L7
      column: Philosophy
      role: "witness the canonical root law as constitutional source"
    - level: L5
      column: Philosophy
      role: "codify seven-root tree architecture"
    - level: L3
      column: Philosophy
      role: "audit filesystem claims against tracked evidence"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[S/B/I]"
  canonical_phrase: "Tree Constitution — Seven Canonical Roots"
---


# Tree Constitution

> The current 7-root holobiont is not a layout. It is a **law**.
> What follows codifies that law so future placement decisions become self-evident.

The five-caste tree audit (L1 firewall, L2 explorer, L3 auditor, L5 architect, L6 compressor) converged on this finding: the current tree strictly dominates every alternative on hard criteria (routing stability, SSoT discipline, convergence index, evidence-tier honesty, reorganisation cost). What was missing was not better topology but the **constitutional codification** that prevents drift.

---

## The Four Laws

### 1. Boundary Law

Every folder must answer one question:

> **"What does this content *become* in the holobiont life-cycle?"**

Not what it *is*, not who *made* it, not what *technology* it uses. The seven valid answers are:

| Becoming | Root |
|---|---|
| **Doctrine** | `01_EMERGENTISM/` |
| **Organism-runtime** | `02_SKYZAI/01_NOOSPHERE/` |
| **Product-surface (scaffold)** | `02_SKYZAI/02_PUBLIC_SCAFFOLD/` |
| **Legal-membrane** | `03_VENTURES/` |
| **Outside-portfolio (sidecar)** | `03_VENTURES/_PORTFOLIO/` |
| **Physical-substrate** | `02_SKYZAI/06_SPECTRE/` |
| **Cold-history** | `90_ARCHIVE/` |

Nouns drift. Life-cycle roles do not.

### 2. Ownership Law

Every root has **exactly one** constitutional owner at **exactly one** authority tier. No root has two.

| Root | Owner | Tier |
|---|---|---|
| `01_EMERGENTISM/` | L7 Ṛṣi | doctrine; only L7 amends invariants |
| `02_SKYZAI/01_NOOSPHERE/` | K2 signatory + L4 Kṣatriya | K2 signs, L4 commits |
| `02_SKYZAI/02_PUBLIC_SCAFFOLD/` | L4 Kṣatriya under K2 ratification | scaffold; not yet K2-bound at deployment |
| `03_VENTURES/` | K2 signatory only | legal personhood is non-delegable |
| `03_VENTURES/_PORTFOLIO/` | K2 signatory + bilateral counterparty contract | sidecars are bilateral, not organism-internal |
| `02_SKYZAI/06_SPECTRE/` | substrate-only | no K2; peer to Skyzai; physical mesh has no caste agents |
| `90_ARCHIVE/` | L6 Sādhu (write-once, append-only) | axiomatic; only what is removed |

### 3. Routing Law

When content fits two roots, **precedence (highest wins)**:

```
03_VENTURES > 01_EMERGENTISM > 02_SKYZAI/06_SPECTRE > 02_SKYZAI/01_NOOSPHERE > 02_SKYZAI/02_PUBLIC_SCAFFOLD > 03_VENTURES/_PORTFOLIO > 90_ARCHIVE
```

**Worked example — the Agentz / Tokencen case (post 2026-05-02):**

| Concept | Life-cycle role | Root |
|---|---|---|
| Agentz as Rosetta-mapped skill taxonomy | organism-runtime | `02_SKYZAI/01_NOOSPHERE/04_CHILD_DAVS/AGENTZ_CLOUD/` |
| Tokencen-the-KSA-legal-entity | legal-membrane | `03_VENTURES/` (when entity is formed) |
| Tokencen as portfolio-bridge venture | outside-portfolio | `03_VENTURES/_PORTFOLIO/TOKENIZATION_CENTRES/` |

Same name, three life-cycle roles, three roots. The Routing Law makes this unambiguous, not contradictory.

### 4. Failure-Mode Law

Architectural decisions drift wherever a root could absorb work that legitimately belongs to another. The guard is **explicit exclusion clauses**, not inclusion lists.

> Every root README must end with:
> **"This root does NOT contain X, Y, Z — those belong to root N."**
>
> Inclusion drifts. Exclusion holds.

---

## The Anti-Recommendation

**Do NOT collapse `02_SKYZAI/02_PUBLIC_SCAFFOLD/` into `02_SKYZAI/01_NOOSPHERE/`** "for cleanliness."

It looks elegant: Skyzai.com is "just" the public surface of Skyzai the organism, so why two roots? The Routing Law itself seems to push this way.

The failure mode this creates: **product-scaffold work would inherit organism evidence-tier discipline before it has the receipts to earn it.** Today `3_*` is honestly [I]/[D] scaffold per `ORGANISM_RUNTIME_TRUTH.md`; once moved into `2_*` it would either (i) be silently upgraded in readers' minds to "organism runtime" (overclaim drift), or (ii) force `2_*` to host [D]-tier scaffolding, polluting the runtime-truth register. The two-root separation is the **evidence quarantine**.

**The principle generalises: roots that look redundant by core state are often separated by evidence-tier or by life-cycle phase.** Test before merging. Same anti-pattern applies to merging `03_VENTURES/` into organs (legal-personhood quarantine) and `02_SKYZAI/06_SPECTRE/` into organs (substrate quarantine). Both have been tried; both broke.

---

## Mechanical Tests (`make tree-audit`)

The CI script at [`01_EMERGENTISM/09_TOOLS/01_SCRIPTS/tree_audit.py`](../../09_TOOLS/01_SCRIPTS/tree_audit.py) enforces a subset of the laws automatically:

1. **Exclusion-clause test** — every root README must contain a "Does NOT contain" section.
2. **Single-archive-root test** — no `99_ARCHIVE/` or `90_ARCHIVE/` siblings of canonical roots; cold history consolidates in `90_ARCHIVE/`.
3. **Compatibility-stub decay test** — flags `*/91_COMPATIBILITY/` folders > 180 days old without a redirect tombstone.

Three more tests are *normative-only* (require human judgment per case, not enforced by CI):

4. **Doctrine-leak test** — runtime files that redefine Rosetta terms, η/K2/K4 invariants, or caste mappings should fail review (those belong to `1_*`).
5. **Substrate-isolation test** — `02_SKYZAI/06_SPECTRE/` should not import from `2_*/10_AGENTS/`. Substrate ↔ organism communication only via the five primitives.
6. **Portfolio-quarantine test** — `5_*/` should not write to or read from `2_*/00_BACKBONE/` directly. Bridge-folder pattern only.

A seventh test is recommended for commit messages but not enforced:

7. **Routing-precedence citation test** — any cross-root path-move commit message should cite the Routing Law (e.g., `routing: 5_*→2_*/04_CHILD_DAVS per Agentz K2-2026-05-02`).

---

## Source

- **L1 Caṇḍāla** (firewall) detected the drift surfaces
- **L2 Śūdra** (explorer) generated the candidate set (6 alternatives)
- **L3 Vaiśya** (auditor) ranked C0 (current) at 57/60 vs next-best 36/60 — strict dominance
- **L5 Brāhmaṇa** (architect) authored the four laws and exclusion-clause discipline
- **L6 Sādhu** (compressor) identified the archive-first compression queue

The audit ran 2026-05-07 against HEAD `da70d2ef3` (post-restoration, post-routing-repair).

Zero-Sum Resolution Equation

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/01_GOVERNANCE/00_TREE_CONSTITUTION.md
