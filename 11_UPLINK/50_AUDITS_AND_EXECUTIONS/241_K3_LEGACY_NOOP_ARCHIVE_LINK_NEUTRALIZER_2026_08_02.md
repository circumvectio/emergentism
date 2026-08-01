---
title: "K3 legacy no-op archive-link neutralizer custody"
status: "ARCHIVED — local source custody only; no successor or authority transition"
date: 2026-08-02
evidence_tier: "[B] local byte identities and path checks; [S] scope and non-claim boundary."
owner: "01_EMERGENTISM"
parents:
  - ../../09_TOOLS/01_SCRIPTS/README.md
  - ../../09_TOOLS/90_ARCHIVE/README.md
  - ../../09_TOOLS/90_ARCHIVE/neuter_broken_archive_links_2026_08_02/README.md
  - ../../09_TOOLS/01_SCRIPTS/check_active_receipt_citations.py
  - ../../09_TOOLS/01_SCRIPTS/check_contact_limited.py
  - ../../00_META/ACTIVE_RECEIPT_CITATION_REGISTRY.json
  - ../../00_META/CONTACT_LIMITED_STATE.json
  - ../../00_WORK_IN_PROGRESS/README.md
  - ../../09_TOOLS/01_SCRIPTS/check_work_in_progress.py
---

# K3 legacy no-op archive-link neutralizer custody

## Outcome

The former active script 09_TOOLS/01_SCRIPTS/neuter_broken_archive_links.py is
retired from the active script surface and preserved byte-identically at
09_TOOLS/90_ARCHIVE/neuter_broken_archive_links_2026_08_02/neuter_broken_archive_links.py.

The source and archive copy both identify as:

    sha256:9bca72d649e9a8460099c73aedee7bdedd0fc587938fb7517e3fadfc1c46ffb5

The one new live-lane filename changes the receipt namespace from 310 to 311
citable targets, 316 to 317 prefixed Markdown files, and 188 to 189 unique
prefixes. The 97 reused-prefix groups, unsafe-bare rule, zero dangling
citations, public lifecycle, claim disposition, owner-held debts, and open
world-contact state are otherwise unchanged. The same new dated path binds the
completion-counter snapshot; it does not close any of its outstanding gates.
The owner-held ids OWNER_GATE_HELD_PUBLIC_DOCS and
OWNER_GATE_OPEN_TOPOLOGY remain open with their existing questions, evidence,
and close conditions; this receipt makes no owner selection or topology ruling.
The WIP manifest and its source-bound checker reflect the same 317/311 receipt
counts and the unchanged two debt rows, so the mirror cannot silently retain
the prior snapshot.

## Evidence

- [B] The retired file was one unchanged tracked blob since commit f101602a.
- [B] No pre-retirement active caller, import, gate, CI entry, test, or README
  reference treating the script as a current tool was found. Historical audit
  material remains unchanged.
- [B] Its only hard-coded roots, 08_ARCHIVE and
  EMERGENTISM_ORG/11_UPLINK/90_ARCHIVE, are absent here. The code would skip
  both roots, inspect zero files, print a completion banner, and return zero.
- [B] The utility can write Markdown in place without a dry run, scope guard,
  manifest, or receipt. It was not executed for this change.

## Boundary

This is local K3 repository custody. It does not repair archive links, create a
replacement tool, re-adjudicate a corpus finding, change doctrine, choose an
owner, obtain independent review, establish world contact, publish, deploy,
sign a contract, move money, or establish external authority.

## Active citation custody marker

active_receipt_citation_registry_canonical_sha256: eadca5c6d739c4fb84f9f5459aeeaa9ea9d9d67a01c3fc769d788e10fdd2b3fe
contact_limited_state_canonical_sha256: 84b826b998c7222200f893c7550fbb4f89ad1608d825818f638acd6635a29ea4

The marker is filled only from the generated registry after all exact active
receipt targets have been reconciled.

---

*A preserved legacy mutator is not an active validator.*
