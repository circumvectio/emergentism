---
type: local-experiment-receipt
title: "APU P1 — passages and source-cited proposals"
date: 2026-09-06
status: "IMPLEMENTED AND TESTED LOCALLY — GENERAL-READER ACCEPTANCE FAILED"
evidence_tier: "[B] local observations; [I/D] next-step and editorial proposals"
---

# Passages improved; broader autonomy not earned

P1 adds a read-only, corpus-side passage selector around the pinned copied-source
APU pilot. It now presents exact text with document titles, heading breadcrumbs,
line ranges, source and excerpt hashes, document declarations and full copied
source access. It emits no answers and changes no source, policy or permissions.
**The shared APU product/core and the website have not been changed.**

The [machine receipt](receipt.json) records inputs, hashes, both fresh-process
runs and measurements. Its private run paths contain static review HTML,
complete copied-source views, full passage results and cited proposals.
Temporary output is not durable custody; reconstruction requires the pinned
sources/P0 engine and the recorded implementation. No output was pushed or deployed.

## What was built

- [passages.mjs](passages.mjs): deterministic token retrieval; no external
  dependencies, model provider, semantic answer generation or source mutation.
  Negations remain searchable. Frontmatter is excluded from body matches and
  shown as untrusted document declarations, never per-passage warrant.
- [run_passages.mjs](run_passages.mjs): validates a completed P0 manifest, exact
  frozen source set, original-byte checkpoints and input/code consistency.
  Writes exclusively into a fresh private temporary directory; completion is last.
- [passages.test.mjs](passages.test.mjs): 16 tests for exact UTF-8/CRLF/EOF
  slices, metadata separation, qualifications, long blocks, code fences,
  tampering, safe paths, inert hostile markup/instructions, budgets, aliases,
  non-mutation, ordering and incomplete manifests.
- [proposals.json](proposals.json): two experimental glossary aids and four
  website-outline suggestions, all source-cited in the generated package.
  These are **assistant-authored drafts**, not discoveries made by an autonomous
  APU agent. No synonym, website change or policy was adopted.

Results have explicit `NO_QUERY_TERMS`, `SOURCE_ONLY`, `NO_PASSAGE_MATCH`,
`MATCH_OMITTED_BY_LIMIT` or `PASSAGE_MATCH` status. A passage match means literal
token overlap, not relevant support. Default caps: five results, two per source,
36 lines and 6,000 characters per window. Whole-source access preserves the
route to omitted context. Incomplete blocks/context remain flagged; no claim
is made that all material qualifications have been found.

## Freeze and evidence

Implementation, ranking, caps and the two-alias map were frozen at
`9bb1310a2d48952ef89e6c7f8cd78dfe1b12f63f`, **before** L2 revealed the six
[challenge questions](challenges.json). Those questions were source-informed
and withheld from this implementation lane, not externally blinded or validated.
No code/config changes followed reveal.

The original eight P0 tasks are explicitly a development set. An early P1
development run let one repetitive source crowd out the formula source; the
two-results-per-source cap was added before freeze. Early private runs remain
`emergentism-apu-passages-Kdo4V4` and `emergentism-apu-passages-KiNTY6`; they are
development observations, not the frozen challenge result. P0's predecessor
receipt and test questions remain untouched.

| Measurement | Result | What it does not establish |
|---|---|---|
| Focused P1 tests | 16/16 pass | General semantic retrieval quality or OS sandboxing |
| Fresh P0 rehearsal | Seven boundary checks pass | Broader authority or current APU product acceptance |
| Repeated P1 processes | Identical results and HTML | Independent replication |
| Source slices | 115/115 returned passage instances reconstruct exactly | That every passage answers its question |
| Proposal citations | 6/6 exact source references | Approval of the proposals |
| Development owner/range retrieval | 5/7 literal; 7/7 with explicit aliases | Held-out improvement; those aliases target known misses |
| Challenge owner/range retrieval | 2/5 supported questions, both arms | Two fully qualified answers |
| Challenge cooking control | Failed: irrelevant lexical matches returned | No cooking answer was fabricated |

The alias arm is disclosed and compared to the unexpanded arm. `cheating →
extraction` and `tested → validated` are search aids, **not semantic equivalences**.
The latter explicitly does not imply that testing validates a claim.

## What the challenge failures teach

H1 (correction history), H2 (adding ordinal rankings) and H3 (almost-best
admissible action) missed their designated owner passages. An owner-key miss
is not by itself a finding that every returned passage was irrelevant; no
complete semantic score is assigned to those questions.

The separate L3 review found:

- **H4:** the Compact's lines 44–47 retain the full deletion-duty boundary,
  including narrowing, superseding or retracting a policy that preserves harmful
  data against valid deletion duties.
- **H5: partial.** The retrieved Power-Max lines 133–155 include the short-horizon
  defection rival and comparison requirement, but omit the corollary's selected
  `[I/C]` status at 123–124 and domain kill criteria at 157–160. The visible
  `[I/C]` at 145 belongs to a different practice claim and cannot supply that
  missing warrant. Range overlap is not full qualification coverage.
- **H6: failed no-support control.** “How many minutes should I roast carrots
  at 200°C?” matched only `many` and/or `c`. Celsius was tokenized into the
  same `c` that appears in `[C]` tier labels. Both arms returned irrelevant
  passages; neither fabricated a cooking instruction.

These observations justify preserving the prototype as experimental. They do
not justify autonomous source writes. A later version should separate domain
terms and status notation, improve meaningful query coverage and abstention,
and retrieve linked qualifications. It needs new withheld wording; these six
questions are now revealed and must not be relabelled as a fresh held-out test.

## Source-cited website suggestions [I/D]

The four proposals are: keep adoption distinct from evidence; show ordinal
comparison assumptions beside model widgets; keep the cooperation counterexample
reachable; and present provisional public wisdom together with its kill criteria.
Each suggestion is paired with an exact copied-source citation and remains
outside the live website. The proposal packet does not alter the approved
Read/Explore journey, brand guide or public claims.

## Reproduce

From the Emergentism checkout, first run the unchanged predecessor harness:

```sh
node 00_HANDOFF/2026_09_06_apu_readonly_pilot/run_pilot.mjs
```

Then use the new private output directory that command prints:

```sh
node --test 00_HANDOFF/2026_09_06_apu_passage_pilot/passages.test.mjs
node 00_HANDOFF/2026_09_06_apu_passage_pilot/run_passages.mjs P0_OUTPUT_DIRECTORY 00_HANDOFF/2026_09_06_apu_passage_pilot/challenges.json
```

The selector uses standard-library modules only. The predecessor uses its
recorded local dependency environment; its full dependency closure is not pinned.
All views escape source HTML and instructions; they include no JavaScript or
external resources. Static content and link checks are not browser acceptance.

## Checks and preserved boundaries

L4 separately verified both completion manifests, 115 exact source slices,
six proposal citations and repeat equality. L3 also checked all passage and
proposal citations and manually reviewed H4/H5 qualifications and the H6 failure.
These are two review roles in the same local environment, not external validation.

L3's pre-freeze corrections covered missing manifest entries, before/after
input hashes, oversized-match status and false code-fence closers. L4 applied
them and retained the narrow explicit commit group. Parent L1 read the existing
runner directly; the prior usage-limited worker was not retried around its limit.

Browser QA is **UNVERIFIED**: the offline CLI was unavailable, the shared browser
connection was busy, and the fresh file preview was denied by browser policy.
No alternate browser or serving route was attempted after that denial. No claim
of desktop/mobile, keyboard, contrast or no-JavaScript browser acceptance follows.

The Rosetta skill's A3 freeze still expects blob
`54658d7797198cfc45677716aa743e728e7012d2`; a read-only current-HEAD probe found
`21ebb5c97709a52ac54bcc287662e523167dfac0`. Logging remains HOLD, with no reset,
retry, event mutation or claim of a fully recorded Soul Loop.

No model-provider calls, credentials, publishing, deployment, source promotion,
daemon, permission expansion or autonomous editing were enabled. Existing
foreign dirty/untracked work is preserved. Public-site gates are not claimed
for this receipt-only change; the website and canonical sources are unchanged.
