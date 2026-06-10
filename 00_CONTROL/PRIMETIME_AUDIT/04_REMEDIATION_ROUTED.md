# PRIMETIME AUDIT — Routed Remediation (the items "fix all" cannot safely auto-execute)

**2026-06-10.** Two findings are real, P0, and **must not be auto-executed** by an agent on a "fix all" — they touch the public surface and the runtime, and they carry a launch / signature decision that is the owner's (K2). Per A7/K3, the audit's duty for these is to **find → route to owner → let K2 decide**. That is done here. Neither is "incomplete"; each is *correctly handed off*.

---

## R-PUBLIC-ANCHOR (P0) — the public site is tier-badged but not source-anchored
**Finding (R-RECON, confirmed):** on the live public site, ~55% of sampled claims carry an evidence-tier badge `[A]/[S]/[I]/[C]`, but only ~9% **link to the doctrine that grounds them**. The 2026-06-06 audit's "93.7% unsourced" figure **holds** (it measured *source-anchoring*, not badging). A site that badges `[I]` on every paragraph without saying *why* is honest-looking but hollow — and this is the single biggest gap between the corpus and a *defensible* public launch.

**Why not auto-fixed:** (1) it's the **public surface**; (2) the right fix is in the **generator** (`09_TOOLS/.../generate_public_library.py` / the handoff-bundle pipeline), not fragile hand-edits to generated HTML that regeneration would wipe; (3) the **book-pwa** lane is K2-frozen for migration; (4) "ship the public site" is a **launch decision** that is yours.

**Routed to:** `12_PUBLIC_SITE/` governance + K2. **Spec:** add a claim→source anchor pass in the generator (target the ~180 highest-value claims to lift source-anchoring from ~9% toward the audit's ~42% interim target); each anchored claim links to its doctrine file/heading. **K2 decision (one of):**
- **(a) Anchor then launch** — commission the generator pass (R-RECON est. a few hours). *Recommended — it's the difference between "looks disciplined" and "is verifiable," which is the framework's whole thesis.*
- **(b) Launch with a disclaimer band** — interim: a per-claim "evidence tier [X]; see source `…`" band (clickable file path) until full anchoring ships.
- **(c) Hold public launch** until anchored.

---

## R-TOOLS-MIGRATE (P0/P1) — ~49 scripts on dead pre-consolidation paths
**Finding (Sprint 2, 09_TOOLS):** ~49 scripts hardcode retired paths (`02_ORGANISM/`, `SKYZAI_ORG/`); `05_DEPLOY` is correctly self-blocked pending the refresh. Tier discipline in the lane is otherwise sound.

**Why not auto-fixed:** it **touches runtime code** — a blind bulk path-rewrite can silently break execution; it needs a **dormant-vs-active triage, per-file rewrite, and a test pass**, not a sweep. The current verification scout is producing the dormant/active split.

**Routed to:** `09_TOOLS/` + runtime owner + K2. **Spec:** (1) take the verification scout's DORMANT/ACTIVE split; (2) archive or leave DORMANT files (K3); (3) rewrite ACTIVE files to canonical paths (`02_SKYZAI/01_NOOSPHERE/…`), run the affected tests, and publish a dated K2 migration receipt listing what was fixed vs archived; (4) unblock `05_DEPLOY` only after the test pass.

---

## Everything else IS being completed
Audit coverage: the whole *live* tree (front door + 7 -ologies + 6 support/stream lanes) is audited; Wave 3 (archives/compat) verified clean mechanically (90_ARCHIVE 97% tombstoned, 91_COMPATIBILITY 99% stub-conformant). Remediation executed: the P0 public-edge fences + 8 P1/P2 tier-hardening guards + the K2-signed archival cut (R-META-1 + the unambiguous R-UPLINK-1 subset). The remaining safe archival moves (verified stale planning packets, compat-stub redirects) execute once the verification scout returns precise lists. These two routed items are what's left, and they're the owner's call by design.
