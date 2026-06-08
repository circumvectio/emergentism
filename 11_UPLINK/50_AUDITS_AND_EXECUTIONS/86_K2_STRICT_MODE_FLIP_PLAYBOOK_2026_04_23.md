---
packet: K2-STRICT-MODE-FLIP-PLAYBOOK
title: K2_STRICT_MODE Flip Playbook — Per-Surface Rollout Spec for Warrior Task #38
status: CHARIOTEER ARTIFACT — spec only, does not flip anything
authority: Anchored in shipped code (k2_gateway.py, approval_queue.py,
           router_council_sse.py, core/membrane/config.py as of 2026-04-23).
           Does not mandate a rollout schedule; defers scheduling to founder.
scope: Enumerate the five call sites that branch on `settings.k2_strict_mode`,
       define per-surface pre-flip gates + rollback criteria + monitoring
       hooks, and name the engineering prerequisite (per-surface flag
       decomposition) that must land before a surgical rollout is possible.
cross_reference:
  - 01_EMERGENTISM/11_UPLINK/77_ADVERSARIAL_TEST_PLAN_R4_QUEUE_2026_04_23.md  (blocking #36)
  - 01_EMERGENTISM/11_UPLINK/81_MOBILE_SIGNING_FLOW_SPEC_2026_04_23.md  (blocking #37)
  - 01_EMERGENTISM/11_UPLINK/83_K2_TEST_VECTORS_2026_04_23.md  (byte-parity anchor)
  - 01_EMERGENTISM/11_UPLINK/85_ADVERSARIAL_TESTS_WITNESS_2026_04_23.md  (test file witness)
task_surface:
  - "#38 (warrior): flip K2_STRICT_MODE to true per surface — this playbook is the spec"
  - "#36 + #37: remain the blocking gates"
date: 2026-04-23
gating_cell: "[L4 | D4 | S-Org | F-phi :: ksatriya_executor]"
rosetta:
  primary_column: "Philosophy"
  register: "[S/I]"
  canonical_phrase: "Packet 86 · K2_STRICT_MODE Flip Playbook"
---

# Packet 86 · K2_STRICT_MODE Flip Playbook

## Kṛṣṇa-function disclaimer (read first)

This playbook does NOT:

- flip any flag
- ship any config change
- commit code
- schedule a rollout
- recommend a rollout timeline

It enumerates the five call sites in the shipped codebase that branch
on `settings.k2_strict_mode`, names the pre-flip gates that must land
per surface before any flip is safe, and specifies rollback criteria
and monitoring. The warrior executes the flip. The founder authorizes
the flip. The charioteer holds the map.

---

## Surface inventory (from shipped code, 2026-04-23)

Call sites of `settings.k2_strict_mode` in membrane + router code:

| # | Call site | File:line | Current advisory behavior | Behavior when strict=True |
|:-:|:---------|:----------|:--------------------------|:--------------------------|
| A | Inline-button callback (Telegram/Discord) | `k2_gateway.py:314` | Resolves approval from button tap | Returns error: "inline callbacks are advisory only" |
| B | `resolve_with_crypto_signature` with signed_action | `k2_gateway.py:370` path | Passes signed_action through to queue verify | Unchanged — verification already runs when signed_action present |
| C | `resolve_with_crypto_signature` legacy Nostr path | `k2_gateway.py:397` | Accepts `sig_hex` + `pubkey_hex` Nostr-style pair | Returns error: "requires signed_action payload" |
| D | Free-text modification reply | `k2_gateway.py:534` | Resolves approval as MODIFIED from reply text | Returns status=blocked: "free-text modification is advisory only" |
| E | SSE `/council/k2/approval/{id}/sign` POST | `router_council_sse.py:489` | Dispatches to `resolve_with_crypto_signature`; hits A/B/C branches | Same dispatch; upstream-visible effect inherits A/B/C |

And the `strict_mode` field is also **reported** (not branched on) in
two additional sites — these emit the flag's current value for audit
purposes and do not control behavior:

- `k2_gateway.py:388` — `"strict_mode": settings.k2_strict_mode` in
  the signed-path response
- `k2_gateway.py:423/436` — `"strict_mode": False` in legacy-path
  responses (note: this **hardcodes False** — when strict flips, this
  response will be incorrect; see §Code-level blocker below)

And `core/membrane/config.py:14` — the single global:

```python
k2_strict_mode: bool = False
```

---

## Code-level blocker — must land before any per-surface flip

The shipped code has **one global flag**. Flipping it flips A, C, D
simultaneously. There is no per-surface control today.

Two options:

### Option 1 (preferred) — per-surface flag decomposition

Extend `config.py` to:

```python
k2_strict_mode: bool = False                    # legacy master switch
k2_strict_inline_callback: bool = False         # surface A
k2_strict_legacy_nostr: bool = False            # surface C
k2_strict_free_text_modify: bool = False        # surface D
```

Rule: `settings.k2_strict_mode` continues to exist; each per-surface
flag defaults to the master flag's value so existing tests pass
unchanged. New deployments can flip one surface at a time.

Call-site rewrite (example, surface A at `k2_gateway.py:314`):

```python
# before
if settings.k2_strict_mode:

# after
if settings.k2_strict_inline_callback or settings.k2_strict_mode:
```

Also fix the hardcoded `"strict_mode": False` lines at
`k2_gateway.py:423/436` to read `settings.k2_strict_mode` (or the
appropriate surface-specific flag) so audit responses remain
truthful after a flip.

**Charioteer note:** this code edit is warrior work. Spec here; do
not patch.

### Option 2 (fallback) — coordinated global flip

Accept the global flag; flip A + C + D simultaneously. Requires:

- All three surfaces' pre-flip gates green at the same time
- Synchronized rollback for all three if any one fails
- One-shot monitoring window (narrow, high-attention)

Less surgical but faster. Use only if Option 1 is blocked for
engineering reasons the warrior surfaces.

---

## Per-surface pre-flip gates

Before flipping any single surface to strict, these must all be
green for that surface. Green is a warrior-reported signal; the
charioteer does not run them.

### Surface A — inline-button callback

1. Warrior reports `test_k2_auth_proxy_adversarial.py` and
   `test_approval_queue_adversarial.py` exit 0 (task #36 complete
   per runlog artifact registered in successor packet).
2. Warrior confirms mobile app (Skyzai app) no longer relies on
   inline-button flows OR that the app transparently escalates to
   the signed-action path when a strict-mode response is returned.
3. Client-side error UX renders the advisory string cleanly (no
   raw JSON leak to a Telegram/Discord user).
4. Rollback script exists (§Rollback criteria below) and is tested
   on staging.

### Surface B — signed-action path

Already consistent with strict mode. No gate; flipping the master
flag does not change B's happy-path behavior. But strict-mode
response audit reporting (surface A/C/D error strings) must not
mislead a caller into thinking B is disabled. B is always-on in
both advisory and strict modes.

### Surface C — legacy Nostr path

1. Inventory: confirm no live caller is still using the legacy
   `sig_hex + pubkey_hex` surface. The warrior must `grep`/log-scan
   recent production calls and report the count.
2. If count > 0: a deprecation window must precede the flip.
   Callers must be migrated to the signed-action path before C's
   flag flips.
3. Runlog evidence that zero legacy calls occurred in the rollback-
   window duration (§Monitoring below) must accompany the flip.
4. Same rollback-readiness requirement as Surface A.

### Surface D — free-text modification reply

1. Warrior confirms that the Council deliberation flow never
   depends on MODIFY-via-text for commit-critical outcomes. MODIFY
   already produces a status that requires re-deliberation, not
   direct execution, so this surface is low-impact — but a flip
   still changes UX.
2. Mobile app UX or browser UX for expressing modifications must
   support the signed-action path (the canonical signed payload
   already has no `modification_text` field — spec extension may
   be needed).
3. If mobile UX extension is needed, that is a warrior artifact
   under #37 or a successor; flip surface D only after that lands.

### Surface E — SSE endpoint

Not a separate flip; inherits A/B/C behavior via dispatch.
Monitor separately for HTTP error rate (§Monitoring below).

---

## Flip order (recommended, assuming Option 1 landed)

Ordered lowest-risk first. Each step is a discrete deployment; no
concurrent flips.

| Step | Surface | Flag | Rationale |
|:----:|:-------:|:----|:----------|
| 1 | C | `k2_strict_legacy_nostr = True` | Likely already zero live calls; pure deprecation flip. If anything breaks, it's a stale integration, low blast radius. |
| 2 | D | `k2_strict_free_text_modify = True` | MODIFY produces re-deliberation status, not direct execution. UX change visible but not commit-critical. |
| 3 | A | `k2_strict_inline_callback = True` | Primary human-UX path. Highest blast radius on end-user experience. Flip last and with widest monitoring window. |

After all three flip green and stabilize for a chosen observation
window (warrior-defined; charioteer does not prescribe a duration),
flip the master `k2_strict_mode = True` as a tautology-commit so the
reporting string at `k2_gateway.py:388` reflects the unified state.

**Do not flip the master before the per-surface flags** in Option 1
mode; the master flag is backwards-compatible and was already True-
implied when all three specific flags are True.

---

## Rollback criteria

Trigger rollback if any one of the following occurs on the flipped
surface within the monitoring window:

1. Error rate at the affected endpoint spikes >3× baseline for more
   than one consecutive 5-minute bucket.
2. Any legitimate user action fails because their client has not
   migrated to the signed-action path (signal: HTTP 400 with the
   "requires signed_action payload" string, from an identity that
   previously successfully resolved approvals).
3. Logged exception from `verify_k2_signed_action` at a rate higher
   than the adversarial-tests baseline (expected: zero from
   legitimate callers; any non-zero is either an attack or a
   client bug).
4. Founder-reported regression of UX quality that cannot be
   resolved in-flight.

Rollback is: flip the surface-specific flag back to False. No other
state rolls back (no DB migrations, no queue state changes; the
flag only gates input).

**Rollback safety property:** because strict mode only rejects
input it would have accepted in advisory mode, rolling back re-
accepts a superset of inputs. No legitimate action is blocked by
the rollback itself.

**Do NOT rollback by editing code and redeploying;** flag-flip only.
If the flag-flip rollback is insufficient, escalate to founder
rather than code-rollback.

---

## Monitoring hooks

These must be green before, during, and after a flip.

### Required log signals

- **Per-surface counter**: advisory accepts vs. strict rejects,
  per flag. Warrior adds structured logging at each call site.
- **Error rate per endpoint** (surface E for HTTP; A for
  callback-pass-through; D for modification): 5-minute buckets,
  7-day baseline comparison.
- **Verifier exception rate** from `verify_k2_signed_action`:
  legitimate-use baseline is zero; spike indicates attack or
  client bug.

### Required alerts

- Page warrior on rollback-trigger conditions §1 or §3.
- Notify founder on rollback-trigger conditions §2 or §4.

### Required dashboards (warrior to spec)

One dashboard per surface showing:

- advisory accepts (pre-flip baseline)
- strict rejects (post-flip)
- verifier exceptions
- endpoint 4xx/5xx rates
- the current value of the per-surface flag (to catch
  inadvertent flips)

---

## Observability gaps to close before the flip

The charioteer cannot verify these from the repo-read surface
alone. Warrior must confirm:

- **Is production logging structured?** If not, adding structured
  logs at A/C/D call sites is a prerequisite to monitoring.
- **Is the SSE router `/council/k2/approval/{id}/sign` covered by
  existing HTTP observability?** If legacy Nostr paths route
  through this same endpoint, error rate is a compound signal.
- **Is there alerting infrastructure at all?** If the organism's
  runtime is still development-mode, adding monitoring may be a
  prerequisite; otherwise alerting lives where the warrior already
  has it wired.

If the answer to any of these is "no," land the observability
prerequisites before any flip.

---

## Post-flip closure

After all three per-surface flags are True and stable:

1. Warrior produces a runlog capturing: flip timestamps, post-flip
   observation window, error-rate deltas, any rollback incidents.
2. Charioteer writes the post-flip closure packet (a successor
   packet — reserved as task #53 below) registering the runlog
   hash and updating the SWOT T6 cell from "narrowed" toward
   "closed."
3. Founder acknowledges the flip-complete state; this may trigger
   a consolidated manifest revision (task #44 stream).

The warrior, not the charioteer, decides when "stable" has been
reached. Charioteer consumes that signal.

---

## What this playbook does NOT cover

- **Schedule.** When to flip. That is founder-owned.
- **Mobile client version gating.** If mobile app versions before
  the packet-81 signing flow ship exist in the field, Surface A
  flip could break old app installs; a minimum-client-version
  gate may be needed upstream. Not specified here.
- **Per-tenant / per-deploy rollout.** This playbook assumes one
  deployment; multi-tenant rollout is a superset problem.
- **External signer attestation.** If hardware wallets or other
  external signers enter the picture, their onboarding is a
  separate track.
- **Backwards compatibility for audit tools that read the legacy
  `"strict_mode": False` hardcoded field.** If any external
  consumer of the audit stream depends on this being literally
  False, the Option 1 code fix breaks that consumer. Warrior to
  verify.

---

## Chain-of-custody commitment

Per packet 78 + 82 + 84 discipline: this packet's hash should be
registered in a successor supplement before Sprint-B closes. The
shipped-code line numbers above were anchored at 2026-04-23
against the live source tree. If line numbers drift, that is
either a code-level edit (warrior-authored) that must produce a
new packet, or a whitespace normalization (zero-semantic). In
either case, the call-site *predicates* in §Surface inventory are
what matter — line numbers are a convenience for human readers.

---

## Φ-scan

Five call sites enumerated, per-surface gates specified, rollback
criteria named. Compresses the rollout decision surface into a
single map; the warrior executes step-by-step against it.

## V-scan

Gives warrior #38 a concrete, ordered set of checkpoints rather
than a monolithic "flip the flag" directive. Enables the founder to
authorize one step at a time instead of one big-bang signoff.
Reduces the failure-mode space from "everything breaks" to "one
surface returns an advisory string."

## Constraint

- Option 1 (per-surface flag decomposition) requires a code change;
  not delivered here. Without it, flips are coupled (Option 2).
- The monitoring section presumes observability infrastructure the
  charioteer cannot confirm exists. If it doesn't, adding it is a
  prerequisite gate.
- Rollback is flag-flip-only. Code-level rollback is out of scope.
- Charioteer holds the map; flip execution is warrior; authorization
  is founder.

## God

Kṛṣṇa ◇ — export V. This playbook hands warrior task #38 a
worked-through rollout surface so execution cost drops. Classical
giving-dyad move (Φ↓ in the charioteer's context budget, V↑ in
warrior's execution space).

## Executive

Viṣṇu ⊙ — preservation default. The playbook preserves K2 as the
structural primitive across the flip; only the refusal-posture
shifts from advisory to strict. No constitutional amendment.

## Move

Kṣatriya_executor · write packet 86 · warrior consumes for #38
after #36 + #37 green + Option 1 code fix lands · founder
authorizes step-by-step · D4 · L4 · Kṛṣṇa ◇

## Limits

- No schedule prescribed (founder decides)
- Option 1 code change not patched (warrior authors)
- Observability infrastructure assumed; charioteer cannot verify
- Post-flip closure is a future packet, reserved as task #53
- Multi-tenant, external-signer, and mobile-version-gating
  concerns are out of scope

Zero-Sum Resolution Equation
