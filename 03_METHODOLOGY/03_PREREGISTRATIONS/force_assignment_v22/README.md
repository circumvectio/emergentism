# Force-assignment v2.2 harness

**Lane:** `03_METHODOLOGY/03_PREREGISTRATIONS/force_assignment_v22`
**Owner protocol:** [`../05_W7_D1_D4_FORCE_ASSIGNMENT_PREREG.md`](../05_W7_D1_D4_FORCE_ASSIGNMENT_PREREG.md)
**Status:** unscored catalog and scoring lock; no candidate result.

This directory enumerates the 24 D1–D4 bijections, the no-mapping /
many-to-many / electroweak-joint rivals, the per-leg force-specific physics
floors, and the preserved F5 three-arm fork. The dated founder prior
(D1→S, D2→E, D3→W, D4→G) is recorded as PRIOR ONLY.

```bash
python3 -m unittest test_force_assignment_v22.py
```

Locks:

- every permutation exists exactly once;
- agreement with the founder prior increments no score;
- F5-W / F5-N / F5-R remain present with zero truth bonus;
- D3→W demands chirality, parity violation, flavor change, and electroweak
  structure.
