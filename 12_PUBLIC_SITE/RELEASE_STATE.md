---
title: "O9 release-state ledger — emergentism.org"
date: 2026-08-22
status: "ACTIVE LEDGER — v2 publicly served; publication is not validation"
evidence_tier: "[D] owner-directed deployment; [S] Vercel and HTTP receipts; [B] local and live gates; no independent outcome evidence"
contract: _PLANS/2026_07_28_VMOSK_A_WORLDVIEW_FRONT_DOOR.md · O9
may_sign: false
may_authorize: false
---

# O9 — verified release states

A local green is not a deploy. A deploy is not empirical contact, scientific
validation, priority, or evidence that any Emergentist conjecture is true.

| State | Value 2026-08-22 | How measured |
|---|---|---|
| **committed** | `e25070f07b3fc142db82270b9631c07277eddc47` — v2 release source | `git rev-parse HEAD` before deployment |
| **pushed** | **yes** — release source matched its upstream `0/0` | `git rev-list --left-right --count HEAD...@{upstream}` |
| **immutable artifact** | `dpl_7zuts6H4Jvr1XL4aniLhiehoRofL` · `emergentism-k3qgps9sz-yves-projects-c163dce1.vercel.app` · `READY` | Vercel deployment API and immutable-URL probes |
| **promoted** | **yes** — the exact artifact above | `vercel promote dpl_7zuts6H4Jvr1XL4aniLhiehoRofL`; branded-domain probes |
| **DNS** | **existing Vercel configuration; unchanged in this sitting** | no DNS mutation command was issued |
| **served hash** | homepage `e6b695cf…` matches the committed v2 artifact | SHA-256 over `https://emergentism.org/` and local `index.html` |

## Deployment custody

The primary wrapper matched the independently supplied project and team pins,
then passed all 16 predeploy sections and the generated-artifact gate. Its first
upload, `dpl_9u7nXXWDYXY1RdhGi4Z2qLqk6rkL`, was blocked before build or
promotion because Vercel could not bind the Git author email to the destination
team. That blocked artifact is not the release.

The successful recovery was staged from `git archive
e25070f07b3fc142db82270b9631c07277eddc47:12_PUBLIC_SITE` outside Git metadata.
The staged homepage hash matched the source before upload. The existing reviewed
`.vercel/project.json` was copied into that isolated stage and checked against:

- project `prj_RyoMG78ylqIWRSnz7URjkeniOKLH`;
- team `team_wtr2VOkP7ZQTWjCJXgaFpQq6`.

The artifact was created with custom-domain assignment held back, audited at its
immutable URL, and only then promoted. No credential file was copied, read, or
logged.

## Live verification

| Check | Result |
|---|---|
| Production state | `READY` |
| Immutable strict manifest audit | **PASS** — 717/717 probes returned 200; 74/74 manifest documents returned 200 |
| Branded strict manifest audit | **PASS** — 717/717 probes returned 200; 74/74 manifest documents returned 200 |
| Core v2 routes | `/`, `/f5/`, `/dasein/`, `/plainly/`, `/practice/`, and `/spark/` returned 200 |
| Historical withholding | boundary routes retained `noindex, noarchive, nosnippet, nofollow` and `no-store` |
| Source parity | all six sampled served hashes matched the frozen local artifacts |

### Served-hash sample

| URL | SHA-256 |
|---|---|
| `https://emergentism.org/` | `e6b695cf0df89fa06faf123e69cf70391ccc2073bab39016267a0c49b603d895` | <!-- pragma: allow-secret -- served digest -->
| `https://emergentism.org/practice/` | `6b8185ef3c84c7fc7aeea248b8ed1eaba2567a6cd3792d0fd5544d98e158d27b` | <!-- pragma: allow-secret -- served digest -->
| `https://emergentism.org/public_semantic_parity.json` | `01b59701bccd6fff4da91988b2db60266b693b095713fc4be729fdabd5601258` | <!-- pragma: allow-secret -- served digest -->
| `https://emergentism.org/living-map.json` | `89361e816e74ae838e00013d70ebeddfa4bf9741a7db5e4ce986aa64b4ba9e16` | <!-- pragma: allow-secret -- served digest -->
| `https://emergentism.org/atlas/site_index.json` | `e84b90f5df54c1e3807de086ac190952845b264e91d55d72dff4c276e9240601` | <!-- pragma: allow-secret -- served digest -->
| `https://emergentism.org/manifest.webmanifest` | `cfec0d9a4816de13bd35bfba313c5e9f98658bc75d0958a76957612e41ebfbfb` | <!-- pragma: allow-secret -- served digest -->

## Boundary

The v2 Gestalt of Dasein is publicly served. This receipt does not establish
F5, the serial-force assignment, retrocausality, Emergentism, the Dasein Test,
novelty, priority, or any other scientific or philosophical claim. Those remain
typed by their source cards and require their own evidence.

---

*Six states. None collapsed.*
