# 00_HANDOFF

Session handoffs and release receipts, newest last.

**These are receipts.** They record what was observed at a moment — a commit, a gate
result, a deployed byte, a decision taken. They create **no doctrine, no formal result, no
empirical support and no validation**, and none of them may be cited as authority for a
claim. Where a handoff and a source owner disagree, the source owner governs.

Each entry states what it verified and what it did not. A handoff whose counts cannot be
reproduced by the commands it names is wrong and should be repaired rather than trusted.

## Reading order for a new session

1. The newest `00_HANDOFF.md` — current state, the traps, and what is next.
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
