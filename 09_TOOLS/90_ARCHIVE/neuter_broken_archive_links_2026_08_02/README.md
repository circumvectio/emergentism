---
title: "Legacy archive-link neutralizer — K3 custody"
status: "ARCHIVED — provenance only; no active repair authority"
evidence_tier: "[B] local byte identity and path checks; [S] retirement boundary."
date: 2026-08-02
---

# Legacy archive-link neutralizer — 2026-08-02

This directory preserves the former active script
09_TOOLS/01_SCRIPTS/neuter_broken_archive_links.py after its K3 retirement.
It is not a current validator, link checker, or repair mechanism.

| Archived path | Former active path | SHA-256 |
|---|---|---|
| neuter_broken_archive_links.py | 09_TOOLS/01_SCRIPTS/neuter_broken_archive_links.py | sha256:9bca72d649e9a8460099c73aedee7bdedd0fc587938fb7517e3fadfc1c46ffb5 |

The retired script could rewrite Markdown archive links in place, without a
dry run or scoped manifest. Its only hard-coded roots were 08_ARCHIVE and
EMERGENTISM_ORG/11_UPLINK/90_ARCHIVE; both are absent in this corpus. It would
therefore check zero files, print a completion banner, and return zero.

The script was not executed for this custody change. No corpus content, runtime,
network, publication, deployment, owner decision, or world-contact state
changed. If an archive-link repair is needed later, it must be a separately
reviewed successor with explicit scope and a safe dry-run boundary.
