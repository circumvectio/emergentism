---
type: benchmark-custody-contract
status: "[D] local interface · no held-out run · no independent custodian appointed"
date: 2026-08-21
owner: Yves R. Burri
---

# EUB-1 v1.0 held-out custodian interface

`custodian.py` keeps the public and private halves of a held-out fixture
separate. The published fixture must be `HELD_OUT`, use
`INDEPENDENT_HIDDEN` custody, set `seed` and `hidden_truth` to `null`, and retain
only commitments. A private `EUBCustodyPayload.v1` opens the seed, hidden truth,
five reveal packets, and every intervention outcome against those commitments.
An additional payload commitment binds the exact private custody envelope.
Held-out seed, truth, packet, outcome, and private-receipt commitments are
domain-separated with a custodian-retained nonce, so low-entropy outcomes are
not exposed as unsalted public dictionary oracles. The nonce remains private
through scoring.

Scoring is available only inside the one-shot `CustodianContext`. Its first
score attempt consumes the context even if validation raises. The ordinary
scorer receives a private in-memory reconstruction; it still refuses the public
fixture by itself with `CUSTODY_UNAVAILABLE`. On exit, the context drops its
reference to the private reconstruction.

The interface accepts only a complete successful five-sitting run: a valid
`RunEnvelope.v1`, five prompt/output commitments, five snapshots, and the exact
usage-call ledger must form one valid run bundle. Failure-bearing or partial
runs are not scored here. Consequently `failure_hash` binds the canonical empty
failure object, while `usage_hash` binds the actual successful-run ledger.

The returned `EUBCustodianPublicReceipt.v1` publishes the fifteen-dimensional
score vector, uncertainty bounds, hard-gate labels, run/output commitments, the
public fixture commitments, and a nonce-separated commitment to the complete
private scorer receipt.
It deliberately excludes the seed, truth, reveal packets, intervention outcomes,
grader disagreements, validation detail, and score components that contain
oracle values. It has no scalar aggregate.

This is a protocol membrane, not secure hardware or proof of independent
custody. Python cannot guarantee memory erasure. A real custodian must generate
and retain a high-entropy nonce and the private payload outside public Git. The
software verifies openings and run-bundle consistency, not the time of
commitment, custodian independence, authorization, or publication.
