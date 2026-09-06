---
title: "APU and Emergentism — private handoff and local custody"
date: 2026-09-06
evidence_tier: "[B] local observations; [I] scoped review; [D] outbound handoff pending separate receipt"
status: "PREPARED — PRIVATE BRANCH BACKUP ONLY; NOT RELEASE CERTIFICATION"
---

# Boundary

The owner requested folder/docs tidy, commits, GitHub push and agent mail.
This packet records the Emergentism part. A separate Circle task coordinates
the shared APU repository and one existing developer inbox notification;
this task neither harvests that lane's live website edits nor sends duplicate mail.

The existing branch is `theory/parasite-load-2026-08-17`. The intended backup
is the same named branch on private `Menexus-GmbH/emergentism` (`menexus`).
Live GitHub inspection confirmed private visibility and that this remote branch
did not yet exist. Remote `main` was `6b07a4a3ea758013dce490c64cdaafdbb2433023`.
At initial HEAD `bebc0f95f54628ce3fd0fc15d21d82972c42b7ce`, it was an ancestor
535 commits behind, spanning 1,664 changed paths. The intended transfer includes
that historical branch ancestry, not merely today's research packet.

Do not push public `origin`, change its tracking relation, merge `main`, force
update a ref, deploy, or treat this receipt as authority to do so. Successful
push and mail require separately observed remote receipts; they are not asserted
by this preparation document. Existing dated trial statements saying that no push
occurred describe their own earlier execution and remain intact.

# Tidying without erasing

The [handoff index](../00_INDEX.md) now routes both the
[original trial](../2026_09_06_apu_fresh_questions/README.md) and
[successor reading ledger](../2026_09_06_apu_topic_research/README.md).
One stale future-tense sentence in the successor is corrected. Frozen inputs,
archives, results and canonical doctrine are unchanged.

[Local file inventory](local-files.json) records 35 files, 2,703,974 bytes:

| Preserved group | Files | Bytes |
|---|---:|---:|
| `.hermes/plans/` | 5 | 69,345 |
| `12_PUBLIC_SITE/output/playwright/burrisphere-20260905/` | 12 | 1,732,367 |
| `12_PUBLIC_SITE/output/playwright/public-wisdom-20260906/` | 14 | 612,536 |
| `12_PUBLIC_SITE/output/playwright/public-wisdom-v3/` | 4 | 289,726 |

These files are retained **in place, local-only and outside the commit**.
Exact file entries in this checkout's `.git/info/exclude` suppress only these
already-inventoried paths; future files remain visible. No shared ignore rule,
archive move, deletion, or claim of resolved authorship follows. Remove the
dated local exclusion block to restore ordinary untracked-file visibility.
The inventory is a digest record, not a backup of their contents.

The Burrisphere spec already references its QA output directory. Leaving it in
place preserves that link. `12_PUBLIC_SITE/.vercelignore` already excludes
`/output/` from deployment. The five older plan files are not current inputs of
the Circle release task; their original ownership remains unresolved.

# Verification at the pre-tidy source pin [B]

- Both frozen experiment archives replay byte-identically on Node 22.22.3.
- The ten-question harness passes 11 tests, including qualification loss,
  source/range drift, and pinned source/engine custody.
- Replay reports zero source/engine writes and zero provider calls; this is a
  copied-process test, not an OS sandbox or autonomous readiness result.
- Git LFS object integrity passes locally. Remote receipt verification remains
  a separate push step; local presence is not remote delivery.
- The repository-wide gate **fails** with inherited source, projection, custody,
  WIP and test-expectation drift. Lean is explicitly skipped. The standalone
  predeploy gate reports five errors: unavailable frozen external source custody,
  public-book build-manifest drift and reading-manifest metadata drift.
  These are not waived or relabeled green. No public release is proposed.
- The redacted known-credential-pattern scan below covers historical outgoing
  Git blobs, decoded evidence entries and locally available historical LFS
  payloads. It cannot certify the absence of every possible secret.

## Redacted transfer screen [B]

At initial HEAD, the comparison to private `main` covers 4,915 Git blobs
(231,665,395 bytes). Two gzip archives were expanded; their 46 base64-encoded
entries were then decoded and their SHA-256 fields verified before screening.
All 62 distinct LFS objects named by `git lfs ls-files --all --long` were present
locally and screened (12,780,444 bytes).

Known provider credential patterns from the staged scanner were supplemented
by GitHub credential shapes, AWS access IDs for Git/archive screening and PEM
private-key headers. Generic entropy and bare hexadecimal wallet-key patterns
were not used for this historical screen; no OCR, arbitrary nested-archive
expansion or exhaustive privacy inspection is claimed.

The only three blob findings were versions of `deploy_release_contract.py`:
AST inspection established that the matches were two standalone PEM-header
string constants in the scanner, not key payloads. No PEM end marker was
present. Decoded evidence and LFS payloads had no findings in the screened
pattern set. No credential value was printed or added to this receipt.
This is a bounded transfer check, not certification that all history is secret-free.

## Commands

Run from the Emergentism root:

```sh
node 00_HANDOFF/2026_09_06_apu_topic_research/run.mjs --check
node 00_HANDOFF/2026_09_06_apu_fresh_questions/evidence.mjs replay
node --test 00_HANDOFF/2026_09_06_apu_fresh_questions/score.test.mjs 00_HANDOFF/2026_09_06_apu_fresh_questions/trial.test.mjs
git lfs fsck --objects
git diff --check
EMERGENTISM_SKIP_LEAN=1 bash 09_TOOLS/01_SCRIPTS/gate.sh
python3 -B 12_PUBLIC_SITE/predeploy_check.py
```

# Single mail route and surviving holds

The existing Git-backed route is private `Menexus-GmbH/AIA`, consumed branch
`main`, `coordination-mail/overseer-ramesh/new`, from `apu-menexus` to
`overseer-ramesh`. The coordinating Circle task will include the verified
Emergentism source SHA and link as a metadata-only dependency note. No copied
corpus or raw evidence is placed in the message. Delivery is not acknowledgement.

These APU trials remain limited to read-only copied-source processing.
Topic assistance is source-informed;
strict search did not improve; all evidence requirements remain `NOT_ASSESSED`.
No canonical adoption or additional permission follows. The A3 frozen-record
HOLD remains: no recorder is called, bypassed or retroactively fabricated.

Rosetta review separated direct local inventory (L1), reversible documentation
groups (L2) and private-transfer risks (L3). L6 negative-boundary counsel is
preserve-in-place rather than erase or relocate unresolved material. L4 alone
applies the narrow documentation and local exclusion changes. Connected Soul
Loop completion is not claimed.
