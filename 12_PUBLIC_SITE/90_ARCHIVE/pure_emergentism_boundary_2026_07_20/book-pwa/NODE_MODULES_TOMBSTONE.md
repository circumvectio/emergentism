---
title: "book-pwa node_modules deletion attempt — correction record"
date: 2026-07-20
status: "CORRECTED [B] — DELETION NOT COMPLETED; node_modules remains present in the live main checkout"
supersedes_claims_in_commit: f24e400
evidence_tier: "[B] observed filesystem and command outcomes; no authority or deployment inference"
files_removed: 0
bytes_removed: 0
live_deploy_proof: "NOT ESTABLISHED"
---

# `book-pwa/node_modules` was not deleted

> **[金] Correction.** Commit `f24e400` called this a destructive-act
> tombstone and repeatedly said the dependency tree had been destroyed. The
> same file also recorded that every deletion attempt failed. On 2026-07-20 the
> live main checkout still contained `node_modules/`: 45,062 regular files and
> approximately 876 MB by `du -sh`. The truthful disposition is **attempted,
> not completed**.

## What happened `[B]`

The prior actor recorded four unsuccessful attempts to move the ignored
dependency directory out of the iCloud-backed Documents tree. Those failures
did not remove the directory. No deletion consequence may be inferred from an
intention, an attempted command, or the presence of this record.

```text
requested action -> attempted move -> filesystem refusal/time-out
                                      |
                                      v
                               directory remains
```

The observed live-main state at the correction cut was:

```text
path: 12_PUBLIC_SITE/book-pwa/node_modules/
present: yes
regular files: 45,062
disk usage: approximately 876 MB
```

Other Git worktrees may not show the ignored directory; worktree absence is not
evidence that the live-main copy was deleted.

## Deployment boundary

The cited `02_SKYZAI/03_AIA/app/` migration receipt, local tests, build result,
and HTTP 200 do not establish that this `book-pwa` lane was deployed live or
that its custody gate was satisfied. The controlling Blueprint expressly says
that local build or HTTP-200 evidence is insufficient; release requires a
live-deploy receipt and a reproducible lockfile.

The lockfile is present and is useful regeneration metadata. It does not prove
that a regenerated dependency tree would be byte-identical across package
manager versions, registries, optional dependencies, platform-specific
packages, or install-time scripts.

## Current disposition

- `node_modules/` remains ignored, local dependency material.
- No tracked doctrine was lost.
- No archive-first act occurred because no removal occurred.
- No deployment is evidenced by this file.
- Any future removal is a separate destructive operation. Its receipt must be
  written only after the path is observed absent and must record the exact
  command outcome, scope, and regeneration check.

## Why this filename remains

The filename is retained for link stability and to make the failed act easy to
find. Its current contents are the correction. Git preserves the earlier false
claims in `f24e400`; they are provenance, not present truth.

**Status: NOT DELETED. No further action is authorized by this record.**
