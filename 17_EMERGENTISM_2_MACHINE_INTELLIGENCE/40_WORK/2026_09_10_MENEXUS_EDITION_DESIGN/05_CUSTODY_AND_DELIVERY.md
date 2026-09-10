---
type: edition-design-custody
date: 2026-09-10
status: "DESIGN TRANSFER BOUNDARY — actual delivery is verified separately"
evidence_tier: "[B] inspected repository state; [I/D] proposed bounded delivery"
---

# Custody: an edition on Menexus GitHub, not an export of private memory

## Owner clarification

The owner clarified: “This versions will live on Menexus GitHub. But first we
need to understand the outline etc. create it locally then push.” This corrects
the prior planning interpretation that the primary destination was the private
Menexus runtime project `emergentism`. That runtime is an optional development
and review environment; the intended edition repository already exists.

## Verified destination and input states [B]

- Repository: private `Menexus-GmbH/emergentism`.
- Existing delivery branch: `theory/parasite-load-2026-08-17`.
- Inspected remote parent: `998d8025d0f36d2c38c1d1c932d212e533f67d45`.
- Local planning source: `4150a25f7d4be810afe2e1cc743f1052a6c5d6d4`.
- Private `main` is not the selected delivery branch; public `origin` is not
  the selected destination.

Local source is ten commits and 27 changed paths ahead of the inspected private
branch. Those changes are not part of this packet transfer. The source map pins
already-delivered sources and also records their local blob identities. One of
the selected twelve sources, the machine entry, differs between these snapshots.
These are deliberate two-version records, not an assertion of source parity.

Source links use the exact delivered revision. They remain inspectable in the
private repository without silently transferring newer source bodies. The map
is a dependency inventory, not certification that all source claims are true or
current. Unpublished later trial work is outside this delivery; sealed payloads
were not inspected or copied. A later source update requires its own reviewed
transfer and edition refresh.

## Exact-path transfer [D]

The seven files in this directory form one independently revertible group.
First commit them locally with an explicit pathspec. Then recheck remote privacy,
branch and parent. Build a delivery tree from that remote parent using only the
seven committed file blobs, with a temporary index rather than the live index.
Create a one-parent delivery commit recording the local source commit and pathset.

Before push, prove that the parent-to-delivery diff contains exactly the packet,
each blob equals its local source commit, source pins and packet links resolve,
and no unexpected files or credential-shaped payloads enter the packet. Push
with an ordinary fast-forward update to the explicit existing branch. If that
branch changes, stop and recheck; never force, reset, merge unrelated history or
quietly broaden the transfer. Verify the remote SHA afterward.

This is a proposed exact-path implementation, not a claim that earlier receipts
used this mechanism. It leaves local-source and remote-delivery commits distinct.
Future synchronization must reconcile them explicitly; a later whole-branch
push is not authorized by this packet.

The Git commit records and the final verified remote ref supply the actual
delivery receipt. This preparation document does not predict success. Reversal
is an explicit packet-only revert, preserving predecessor history; no existing
source, trial or kernel is deleted.

## Review and limits

[I] L1 inspected the existing successor entry; L2 compared reader-job and typed
artifact outlines; L3 audited the source/remote gap and narrow delivery. L5–L7
counsel retained the source owners, optional runtime boundary, adverse evidence
and reversible packet-only change. These are agent design reviews, not empirical
replication, efficacy evidence or authority.

[B/I] Final review selected one explicit synthetic first walkthrough. It also
caught a checker gap: supplied local blob IDs were not verified against the
recorded local revision. The checker now verifies both source snapshots by
default, with a regression that rejects a fabricated local hash even when its
drift flag is internally consistent. Eleven self-tests and the two-snapshot
structural check pass locally. The explicit delivered-only mode reports that
local planning pins are not verified; it is not equivalent to the full check.

[B] The formal A3 recorder probe returned HOLD: frozen-v0 observed blob
`21ebb5c97709a52ac54bcc287662e523167dfac0` differs from expected
`54658d7797198cfc45677716aa743e728e7012d2`. No bypass or alternate identity retry
was used. A connected recorded Soul Loop is not claimed.

No code-product change, corpus ingestion, private-memory acceptance, provider
call, new benchmark run, agent mail, deployment or source-truth promotion is
part of this task. Broader repository gates retain their separate dated status;
the packet checker does not replace them.
