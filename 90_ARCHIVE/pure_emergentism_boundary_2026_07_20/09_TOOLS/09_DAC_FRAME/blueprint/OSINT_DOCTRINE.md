---
rosetta:
  primary_level: L3
  primary_column: OSINT Evidence Collection
  secondary:
    - level: L4
      column: Collection Operations
      role: "route passive and active collection through scope, mission-order, and stop-condition gates"
    - level: L5
      column: Collection Architecture
      role: "map passive recon, active recon, ROE, and public-domain exhaust sources"
    - level: L6
      column: Legality/Ethics Boundary
      role: "prevent OSINT doctrine from authorizing hacking, social engineering, unlawful collection, or out-of-scope pivots"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  register: "[I/B]"
  canonical_phrase: "OSINT Doctrine (Digital Collection)"
title: "OSINT Doctrine (Digital Collection)"
status: "BLUEPRINT — public-source collection reference"
evidence_tier: "[I] for OSINT doctrine; [B] only for scoped, lawful, approved collection receipts and source records."
---

# OSINT Doctrine (Digital Collection)

> **Holographic Briefing**
> **Position: 80_DAC_FRAME > 02__BLUEPRINT > OSINT_DOCTRINE
> **Status**: Canonical ✅
> **Intent**: Define and operationalize OSINT Doctrine (Digital Collection).

---


**Purpose**: To gather information from the public domain without violating laws or ethics.

**Rosetta boundary:** [I] This paper defines public-source collection doctrine.
It does not authorize hacking, social engineering, evasion, unlawful collection,
or out-of-scope pivots. [B] Collection claims require scope, source, approval,
and mission-order receipts where active collection is involved.

## 1. Passive vs Active Reconnaissance

### Passive Recon (Green Light)
*Touching the target only as a normal user would.*
- **Definition**: Gathering info without directly interacting with the target's systems in a suspicious way.
- **Examples**: Browsing their website, searching Whois records, reading LinkedIn profiles, checking Shodan (which scans for you).
- [I] **Approval**: Pre-approved for all Intel Agents inside lawful passive scope.

### Active Recon (Amber Light)
*Touching the target in ways that trigger logs/alerts.*
- **Definition**: Directly scanning, probing, or interacting with the target's infrastructure.
- **Examples**: Port scanning (Nmap), Spidering a site (Burp Suite), Social Engineering.
- [I] **Approval**: **REQUIRES MISSION ORDER**. Do not do this without explicit authorization.

## 2. Rules of Engagement (ROE)
1.  [I] **Do Not Hack**: OSINT is about *finding* info, not exploiting it. If you find a vulnerability, document it and STOP.
2.  [I] **Respect Scope**: Only collecting on the specified Target. Do not pivot to their family/partners without cause.
3.  [I] **Attribution Management**: operational security. Use VPNs/Tor/Sock Puppets only when lawful, approved, and necessary to protect *our* identity.

## 3. The Digital Exhaust
Everyone leaves a trace. We collect:
- **Technical Exhaust**: DNS records, SSL certs, Server headers.
- **Social Exhaust**: Employee posts, Job listings, PR releases.
- **Business Exhaust**: Filings, Patents, Partnerships.

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/09_DAC_FRAME/blueprint/OSINT_DOCTRINE.md`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
