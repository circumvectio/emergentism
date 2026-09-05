---
type: session-handoff
title: "Public Wisdom integration — local validation and upload hygiene"
date: 2026-09-06
status: "LOCAL PUBLIC GATES PASS; PUSH AUTHORIZED; NOT DEPLOYED"
evidence_tier: "[B] local execution evidence only"
may_sign: false
may_authorize: false
---

# Validation after integration

Implementation commit: `0041d6eacc011434998b8884efc9d260a9be5334`.
Its [80-path implementation manifest](PATHSET.json) and [takeover receipt](README.md)
were committed with explicit scope. Git reports 81 changed file records because
the exact design-v1 relocation is one rename; the explicit staging set had
82 paths including the two handoff files and both rename endpoints.

## Verified local results

- Full public predeploy: **all 18 sections pass**, first after the implementation
  commit, then again with the upload-hygiene changes below. All 75 declared
  public surfaces match exact HEAD bytes. These checks used strict external
  source replay, not unavailable-source mode.
- All 17 documented generator `--check` operations pass. The nine default
  site-artifact checks pass on repeated runs; no generator changed tracked
  bytes during those checks.
- 72 focused site tests pass after the two upload-hygiene regressions; seven
  node-ranking tests and 13 canonical Wisdom-source tests pass. The complete
  103-test contact-limited suite passed before the upload-only exclusion;
  its exact current census checker passes afterward without rebaselining.
  All 16 selected ignore/publication/census controls also pass after the
  exclusion, including parity of both ignore matchers over the present site.
- The 20 route/viewport/no-JavaScript browser cases and additional
  keyboard/storage-denied/system-theme checks are detailed in the takeover
  receipt. No external requests or page errors occurred in that bounded run.
- The normal staged secret scanner and whitespace checks pass. One earlier
  false positive was a digest without a same-line label; the label was fixed,
  not the scanner bypassed.

The final cache identity is `emergentism-0dd7296e390f`, derived from 99 assets.
The census remains 419 artifacts, partitioned 60 current / 3 provisional /
90 frozen / 264 withheld / 2 infrastructure / 0 unclassified. The exact
withholding registry still holds 199 artifacts. These denominators differ.
The two owner-held debts and world-contact state OPEN / 0 / 2 are unchanged.

## Separate upload-hygiene correction

The successful asset-validity scan counted local browser screenshots as
potential deployment assets. That check proves valid bytes, not that those
bytes belong in a public upload. No upload occurred.

Add the anchored `/output/` rule to `.vercelignore`; require it in predeploy,
with risky-output and safe-lookalike probes. Unit tests reject removal and
negation of the rule while preserving nested output names and actual Wisdom
and OG assets. This is a deployment exclusion, **not** a Git ignore or deletion.

The three separately reviewed changes accompanying this receipt are:

- `12_PUBLIC_SITE/.vercelignore` — SHA-256: `335d58fcc3eeba2a4fdd5a55abe5abfd4a8914adb0025161e52a4b17938f748f`.
- `12_PUBLIC_SITE/predeploy_check.py` — SHA-256: `a6006341cc67f04d5c319462a48870a211f752c760d3decbe3ffa37a5c842b1d`.
- `12_PUBLIC_SITE/test_public_wisdom_release.py` — SHA-256: `51e8b1f15c2cd1f717edeb857695535bf4a4fec4d804dfc09b7090d45bcf11b2`.

Five local plans and 30 browser-output files remain untracked and preserved.
No output path is Git-tracked. Their retention means “tracked tree clean”
must not be shortened to “no untracked files.” No corpus doctrine was changed
by this upload exclusion, and no public artifact or claim tier was promoted.

## Reproduce and respect the boundary

From `12_PUBLIC_SITE`, run:

```sh
EMERGENTISM_PRIMARY_CHECKOUT_ROOT=/Users/Yves/Documents/01_EMERGENTISM python3 -B predeploy_check.py
python3 -B ../09_TOOLS/01_SCRIPTS/check_site_build_artifacts.py
python3 -B -m unittest test_public_wisdom_release test_gestalt_v2 test_living_map test_decision_transaction test_burrisphere_instrument test_burrisphere_operators
```

The authorized push targets the existing `origin` branch
`theory/parasite-load-2026-08-17`, not `main`. Origin is public: pushing publishes
repository history, not proof that emergentism.org serves this revision.
Remote identity must be checked after the push; this receipt does not predict it.

No deployment command, DNS change, model evaluation, product adoption or
independent scientific validation occurred. The broader corpus gate's previously
reported debts are not cleared by the public predeploy pass. A3 frozen-record
logging remains on HOLD; no reset, bypass or retry was used.
