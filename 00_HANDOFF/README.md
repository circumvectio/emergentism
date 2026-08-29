---
type: lane-readme
title: "00_HANDOFF"
status: "ACTIVE — lane route card; receipts create no doctrine"
canonical_phrase: "00_HANDOFF lane — session handoffs and release receipts (one dated directory each); `main` is authoritative and `menexus` is the WIP backup; receipts create no doctrine, no formal result, and no validation"
---

# 00_HANDOFF

Session handoffs and release receipts, one dated directory each. The `YYYY_MM_DD` prefix is
zero-padded, so lexical order is date order — `ls` lists them oldest first
(`2026_07_19_broken_66_second_look`) to newest dated directory (`2026_08_21_worktree_consolidation` as of 2026-08-29). Older text named `2026_07_31_tidy_and_handoff`; that directory remains. Loose dated receipts also live at this folder root (`00_INDEX.md`: named working packets, not one-directory-only). Directories
sharing a date carry no order within that day. The newest packet is the last *dated
directory* `ls` prints, not the last line — `AGENTS.md`, `CLAUDE.md` and `README.md` sort
after it.

## Which branch is authoritative

**`main`.** It was 90 commits stale until 2026-07-31, when it was fast-forwarded to the
working branch; nothing in this repository said so, and a newcomer cloning the default
branch got a tree three weeks behind the deployed site. If you are reading this and `main`
again looks stale, check `codex/*` branches before assuming the work is lost — and see
`git for-each-ref refs/rescue/` for recovered stashes that live on no branch at all.

- `origin` (`github.com/circumvectio/emergentism`) is **PUBLIC**. Pushing a branch there
  publishes it.
- `menexus` (`github.com/Menexus-GmbH/emergentism`) is **PRIVATE** and is where WIP
  branches are backed up. All 38 local branches were mirrored there on 2026-07-31.

Session handoffs and release receipts.

**These are receipts.** They record what was observed at a moment — a commit, a gate
result, a deployed byte, a decision taken. They create **no doctrine, no formal result, no
empirical support and no validation**, and none of them may be cited as authority for a
claim. Where a handoff and a source owner disagree, the source owner governs.

Each entry states what it verified and what it did not. A handoff whose counts cannot be
reproduced by the commands it names is wrong and should be repaired rather than trusted.

## Reading order for a new session

1. The newest `00_THE_HANDOFF.md` — current state, the traps, and what is next. (There is no `00_HANDOFF.md` at this path.)
2. [`../00_WORK_IN_PROGRESS/README.md`](../00_WORK_IN_PROGRESS/README.md) — what is open
   and what each item is waiting on.
3. [`../00_ESTABLISHED/README.md`](../00_ESTABLISHED/README.md) — the short list of what
   survives an outside check.

Then run the two gates before changing anything:

```bash
EMERGENTISM_SKIP_LEAN=1 bash 09_TOOLS/01_SCRIPTS/gate.sh
cd 12_PUBLIC_SITE && python3 predeploy_check.py
```

•   ⊙   ○ — *a receipt is not a result.*
