---
rosetta:
  primary_level: L5
  primary_column: Infinite Book PWA Source Scaffold
  secondary:
    - level: L3
      column: Build and Runtime Evidence Audit
      role: "separate local commands, provider integrations, and deployment claims from current receipts"
    - level: L4
      column: Local Operations
      role: "route source install, Prisma, seed, dev, lint, and build operations"
    - level: L6
      column: Source-Only Boundary
      role: "prevent scaffold docs from overriding manuscript canon or production truth"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I/C/B]"
  canonical_phrase: "Infinite Book PWA Source Scaffold"
title: "Infinite Book PWA Source Scaffold"
status: "SOURCE SCAFFOLD — not deployment proof"
evidence_tier: "[I] for scaffold organization; [C] for provider/payment/pricing plans; [B] only for current build, runtime, deployment, auth, payment, database, or live-model receipts."
---

# Infinite Book PWA Source Scaffold

Date: 2026-05-30.

## Purpose

This folder is the source-only Next.js scaffold for the public Infinite Book PWA. It translates the
static proof-of-shape in `../infinite.html` into a routed app with:

- manuscript-backed node ingestion through Prisma;
- a Workflowy-style recursive reader;
- local-first branch state for AI expansions;
- gated expansion and payment routes for future Clerk, Anthropic, and Stripe integration.

[I] It is not a deployed production app and does not override the static public-site front door or the
Definitive One Book source corpus.

**Rosetta boundary:** [I] This README describes source scaffold scope. It does not [B] prove production deployment, build success, auth/payment/live-model readiness, database state, pricing approval, or canonical text promotion without current receipts.

## Workflowy UX Reference

[B/I] The controlling public-interface pattern is Workflowy's one-document outliner model: nested
nodes, zoom focus, breadcrumbs/home, collapse/expand, inline editing, live search, node-type
semantics, mirrors/templates, slash commands, and optional sidebar access for starred/home routes.
The implementation should preserve that feeling before adding app chrome.

## Current Status

| Surface | Status |
|---|---|
| Next.js source | Source scaffold |
| Prisma schema and seed | Source scaffold; local DB not committed |
| Clerk auth route use | [C] environment-gated |
| Anthropic expansion route | [C] environment-gated |
| Stripe checkout/webhook routes | [C] environment-gated |
| Pricing and plan copy | [C] planning until product receipt |
| `.env`, `.next/`, `node_modules/`, SQLite DBs | Local artifacts; not canon |

## Controlling Sources

| Control | Path |
|---|---|
| Public-site lane | [`../README.md`](../README.md) |
| Public narrative contract | [`../WEBSITE_NARRATIVE.md`](../WEBSITE_NARRATIVE.md) |
| Static Infinite Book proof | [`../infinite.html`](../infinite.html) |
| Product controlling spec | [`../../../02_SKYZAI/02_AIA/EMERGENTISM_AIA/07_DEFINITIVE_ONE_BOOK/10_ADAPTIVE_PWA_RAG_BLUEPRINT/00_THE_INFINITE_BOOK.md`](../../../02_SKYZAI/02_AIA/EMERGENTISM_AIA/07_DEFINITIVE_ONE_BOOK/10_ADAPTIVE_PWA_RAG_BLUEPRINT/00_THE_INFINITE_BOOK.md) |
| Product intake lane | [`../../../02_SKYZAI/02_AIA/EMERGENTISM_AIA/07_DEFINITIVE_ONE_BOOK/10_ADAPTIVE_PWA_RAG_BLUEPRINT/29_D23A13_INFINITE_BOOK_PRODUCT_SPEC_INTAKE`](../../../02_SKYZAI/02_AIA/EMERGENTISM_AIA/07_DEFINITIVE_ONE_BOOK/10_ADAPTIVE_PWA_RAG_BLUEPRINT/29_D23A13_INFINITE_BOOK_PRODUCT_SPEC_INTAKE) |
| Manuscript source | [`../../../02_SKYZAI/02_AIA/EMERGENTISM_AIA/07_DEFINITIVE_ONE_BOOK/MANUSCRIPT`](../../../02_SKYZAI/02_AIA/EMERGENTISM_AIA/07_DEFINITIVE_ONE_BOOK/MANUSCRIPT) |

## Local Operation

```bash
npm install
npx prisma generate
npx prisma db push
npx prisma db seed
npm run dev
```

Use a local `.env` with `DATABASE_URL` and provider credentials. Do not commit that file or any
local SQLite database.

## Verification Targets

```bash
npm run lint
npm run build
```

These commands are receipts for source readiness only. Runtime claims still need deployment,
auth/payment sandbox, live-model, and database receipts.

## Claim Boundary

[I] The PWA may render and extend the Infinite Book. It cannot promote AI-generated branches into canon,
ratify pricing, or replace manuscript source truth without the controlling D25-D28 gates and product
receipts.

## Source-Only Discipline

- [I] Keep source files and the dependency lockfile.
- [I] Keep generated output and local state out of Git.
- [I] Keep static public prototypes available until this PWA has a deployment receipt.
- [I] Keep public claims tier-marked when they depend on payment, auth, AI provider, or external factual
  behavior.
