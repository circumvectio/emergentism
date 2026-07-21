---
title: "07_AGENT_OPS"
status: "ACTIVE — pure Emergentism route-card maintenance"
evidence_tier: "[B] current generator behavior; [S] routing boundary"
---

# Agent operations

This lane contains the deterministic route-card generator for the Emergentism
repository. It maintains navigation and epistemic boundaries; it does not
create doctrine or import instructions from any product, venture, company, or
external governance system.

## Active utility

`generate_agents_md.py` renders every active `AGENTS.md` and `CLAUDE.md` route
card from one pure-worldview template. Historical archives, compatibility
material, session packets, and the public projection are excluded.

Check without changing files:

```bash
python3 -B 09_TOOLS/07_AGENT_OPS/generate_agents_md.py --repo . --check
```

Regenerate after an intentional instruction change:

```bash
python3 -B 09_TOOLS/07_AGENT_OPS/generate_agents_md.py --repo . --write
```

The generator ignores tracked paths that have been relocated from the working
tree so an archive move cannot accidentally recreate an obsolete instruction
surface.

## Authority boundary

- Ordinary repository and AI work follows the user's scoped request, tool and
  repository permissions, provenance, reversibility, and tests.
- A private person's financial or contractual signature convention is not a
  work gate and is not part of Emergentist doctrine.
- Consequential actions are described through a complete, scoped, contestable
  `AuthorizationEnvelope`.
- Generated cards remain downstream from the Kernel Index, Settled Canon
  Registry, and source-owning documents.

## Read upstream

- [Emergentism route](../../AGENTS.md)
- [Kernel Index](../../00_THE_KERNEL_INDEX.md)
- [Settled Canon Registry](../../00_META/00_SETTLED_CANON_REGISTRY.md)
