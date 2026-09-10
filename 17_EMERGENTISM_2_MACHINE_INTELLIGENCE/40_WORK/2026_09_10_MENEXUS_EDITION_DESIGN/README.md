---
type: edition-design-packet
title: "Emergentism — the Menexus GitHub edition"
date: 2026-09-10
status: "DESIGN ONLY — outline prepared; instrument release not qualified"
evidence_tier: "[D] proposed edition; [I] editorial design; source claims retain their own tiers"
may_sign: false
may_authorize: false
---

# Emergentism — the Menexus GitHub edition

**Understand the lens. Use the instrument. Inspect what supports it.**

[D] This is the local design packet for an edition intended to live in the
existing private `Menexus-GmbH/emergentism` repository. It builds on the
already-started `17_EMERGENTISM_2_MACHINE_INTELLIGENCE` stack. It is not a new
Menexus database, a third corpus, a website deployment or a finished instrument.

The primary audience is machine intelligence; humans must also be able to read,
teach, question and maintain the same edition. A reader should be able to use a
part without adopting the whole worldview.

## The reader journey [D]

**Start → Lens → Instrument → Worked cases → Research → Sources.**

Start gives the purpose and one small application. The lens explains how the
worldview organizes questions. The instrument provides usable operations. Cases
show those operations succeeding, failing or declining to answer. Research
distinguishes what is being tested from what has been observed. Sources let a
reader recover the exact support, limitations and corrections.

This is a reading route, not six new ontological levels or a required sequence
of applications. The short route may go straight from Start to a worked case.

## Present limits travel with the invitation

[S, source report] The existing trial record reports that MID-01 lost its primary
comparison and MID-02 did not establish transfer superiority. The self-correction
observation does not establish competitive advantage: only the instrument brief
carried that planted flaw. A new presentation cannot change those results.
See the exact `mid01` and `mid02` references in the [source map](04_SOURCE_BINDINGS.json).
No new experiment or user study was run for this packet.

## Read this packet

1. [Outline and chapter contracts](01_OUTLINE.md) — what each section does for its reader.
2. [File architecture](02_FILE_ARCHITECTURE.md) — reuse the existing stack and keep meanings separate.
3. [First release and execution sequence](03_RELEASE_SEQUENCE.md) — build a small usable edition before exhaustive expansion.
4. [Pinned source map](04_SOURCE_BINDINGS.json) — exact delivered and local source versions, not claim acceptance.
5. [Custody and delivery](05_CUSTODY_AND_DELIVERY.md) — local construction, exact-path private push, and remaining limits.

[D] APU and Menexus are development partners and optional connected hosts. The
portable GitHub edition must remain readable and inspectable without a running
Menexus service, an APU account, a provider key or live inference.

Structural check, from this directory:

```sh
python3 -B check_packet.py
python3 -B check_packet.py --self-test
```

These commands check the design packet, not the instrument's efficacy or release
readiness. Whole-corpus coverage remains a separate programme.

The default check requires both recorded source revisions. A checkout containing
only the delivered history may use `python3 -B check_packet.py --delivered-only`;
that narrower result explicitly leaves the local planning pins unverified.
