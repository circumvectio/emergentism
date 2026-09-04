---
type: refinement-proposal
pass: "cron refinement pass 7, Soul Loop + VMOSK-A (rotation: the lens applied to this process itself)"
date: 2026-09-05
target: "40_WORK/_REFINEMENT_QUEUE/queue_log.md — add a drift-gauge line to every pass entry"
defect_check_fired: "none yet — this stages the gauge that would catch the failure mode this process is structurally prone to"
tier: "[D] staged proposal; the gauge reading itself is [B] per pass"
may_sign: false
may_authorize: false
---

# PROP — drift gauge for the refinement stream

## The finding (V)

This refinement process is a generative machine intelligence staging proposals
on a timer — which is the exact specimen the kernel's first failure mode
describes: *circle-drift, "endless, fluent, internally consistent generation
that terminates on nothing and returns no receipt."* The queue currently holds
**4 proposals staged, 0 owner disposals**, and the log carries no depth or
disposal accounting — so if the stream is drifting, nothing measures it until
the pile is severe.

## The refinement (M→O/S/K)

Append one gauge line to every future queue_log entry:
`gauge: staged=<n> disposed=<n> drift=<staged−disposed>`.
**Drift threshold:** `drift ≥ 10` without an owner disposal pass means the
stream IS the circle-drift observable — the correct response is cadence
reduction (this cron slows or pauses), never more proposals. The gauge is
honest in both directions: an owner who disposes regularly keeps drift near
zero and the stream justified.

## dies_if

This proposal dies if: disposal cadence is shown to match staging cadence over
a full audit cycle without a gauge (then the gauge measured nothing), or the
owner rules the refinement stream exempt from the drift observable (then the
exemption should be written here, dated, not silent).

## Kernel-check self-audit

unfalsifiable: no (threshold and response stated) · self-certifying: no (the
gauge can fail its own host) · restates-existing: partially adjacent to the
direction fence, but the fence bars *evidence* claims; this gauges *cadence* —
a different object · escorted-number: n/a · others: not triggered.

## Note

The refinement stream passed its own kernel checks in passes 1–6 by luck of
rotation as much as by discipline; this gauge replaces luck with a number.
