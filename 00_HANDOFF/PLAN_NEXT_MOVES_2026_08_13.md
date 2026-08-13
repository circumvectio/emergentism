# Next moves — PWA / Book I / containment

> Supersedes the “in-repo next” section of `PLAN_PWA_BOOK1_CONTINUE_2026_08_13.md`.
> In-repo only. Not a public release. Not Amrita emerged. Not Halāhala contained.

**Goal:** Keep stacking firewood that G10 can actually use, without pretending G10 is paid.

**Architecture:** `/book/` stays One-Sitting until a separate public-edition gate is paid. The Manifesto current-body stays staged under `13_BOOKS/manifesto/`. PWA generators own chrome. Hygiene runner is the daily lock. Missing Skyzai archives are a named block, not a license to invent files.

**Stack:** `check_pwa_book1_hygiene.py`, manifesto unittest, `assemble_manifesto_book.py`, `extract_manifesto_public_current_body.py`, `compile_claim_cards.py`, `check_barred_claims.py`, `predeploy_check.py`.

---

## Standing (do not redo)

| Item | State |
|---|---|
| Next public book named | Manifesto current-body only (Preamble + 1–11 + 17) |
| Extract | `PUBLIC_CURRENT_BODY_STAGED.md` — 28,919 words, `public_route: null` |
| Hostile read (agent) | P1–P11 / Grave 4 LIVE=0; ch.17 seams reseated |
| CURRENT HTML poison scan | LIVE=0 |
| Private full book | 63,608 words / 638 units; `test_manifesto*.py` 36/36 |
| Hygiene runner | `python3 -B 09_TOOLS/01_SCRIPTS/check_pwa_book1_hygiene.py` |
| PWA chrome on CURRENT HTML | present (dimensions via `render_dimension_site.py`) |
| Q4 / semantic parity | PASS |

## Hard bans (every increment)

- Do not write the extract into `/book/` or the sitemap.
- Do not retarget `build_book.py` `CURRENT_WORK_ID`.
- Do not ship Titans / Reciprocal / Serpent.
- Do not invent missing Skyzai archive files.
- Do not commit, deploy, or say the Amrita sentence.
- Do not cite `16_THE_EMISSION` or Second Churning as owners.

---

## Lane A — in-repo, agent can run

### A1 — Keep the lock green after every edit
Run:

```
python3 -B 09_TOOLS/01_SCRIPTS/check_pwa_book1_hygiene.py
python3 -m unittest discover -s 09_TOOLS/02_COMPILERS -p 'test_manifesto*.py'
python3 -B 09_TOOLS/02_COMPILERS/assemble_manifesto_book.py --check
```

Expected: all PASS. If not, heal the owner that drifted; do not skip.

### A2 — G9 remainder that is not claim-card compile
These are named in `FULL_BOOK_1_COMPLETION_GATE.md` G9 and have not been run as a set this loop:

```
python3 -B 09_TOOLS/01_SCRIPTS/check_barred_claims.py --scope cards
python3 -B 09_TOOLS/01_SCRIPTS/check_barred_claims.py --scope public
python3 -B 09_TOOLS/01_SCRIPTS/check_emergentism_purity.py
python3 -B 09_TOOLS/01_SCRIPTS/check_links.py
python3 -B 09_TOOLS/01_SCRIPTS/check_trophic_rosetta_doctrine.py
python3 -B 12_PUBLIC_SITE/predeploy_check.py
```

Record each result as PASS / FAIL / BLOCKED with the first error. Heal only mechanical public-site or script defects. Do not “fix” a doctrine owner to silence a purity fail.

### A3 — Stage a public-reader *preview* that cannot become `/book/`
Write `09_TOOLS/02_COMPILERS/render_manifesto_public_current_body.py`.

- Input: `13_BOOKS/manifesto/PUBLIC_CURRENT_BODY_STAGED.md`
- Output: `13_BOOKS/manifesto/PUBLIC_CURRENT_BODY_READER_STAGED.html` **only**
- Must refuse to write under `12_PUBLIC_SITE/`
- Must inject the same PWA chrome as `build_book.py`
- Must carry a banner: staged preview, not a public edition, G10 unpaid
- Add a unittest that fails if the renderer writes into `12_PUBLIC_SITE/` or emits `RIP01-` / `## 12.`

This is the next legal firewood toward a public edition. It is not the edition.

### A4 — Draft the G10 protocol (paper, not a run)
Add `13_BOOKS/manifesto/G10_PUBLIC_RELEASE_PROTOCOL.md` with preregistered, unpaid boxes:

1. Fresh-reader tier comprehension — who, n, what they must distinguish (`[A]/[I]/[C]/open`), kill if they cannot.
2. Independent *human* hostile review — not this agent; named reviewer; P1–P11 + Grave 4 + Reciprocal leak.
3. Public edition build — current-body only; parity; predeploy; immutable artifact hash.
4. Operator deploy + live host audit.
5. World-contact remainder stays `0` unless a dated receipt says otherwise.

Do not tick any box from AI agreement.

### A5 — Claim-card compile: receipt the block, do not invent the archive
`compile_claim_cards.py --check` is blocked on missing Skyzai historical Reciprocal/Sarpasya paths.

Allowed next acts:

- Search the live machine (and only existing trees) for the pinned SHA-256s.
- If found, retarget `book-manifest.json` `historical_sources` to the real file.
- If not found, write a one-page **missing-archive receipt** under `00_HANDOFF/` naming the paths, hashes, and that compile stays red.

Forbidden: creating a file whose hash “matches” by reconstruction.

---

## Lane B — human / world (agent cannot pay)

| ID | Gate | Who |
|---|---|---|
| E1a | Fresh-reader tier comprehension | human subjects, preregistered |
| E1b | Independent human hostile review | a person who is not this agent |
| E1c | Controlled Finity comparison | human / lab |
| E2a | Public edition authorization | K2 / operator |
| E2b | Deploy + live `audit_live_domain_against_manifest.py --strict` | operator |
| E2c | World contact > 0 | the world |

A green Lane A does not move any Lane B row.

---

## Lane A standing after 2026-08-13 execution

| ID | Result |
|---|---|
| A1 | PASS — hygiene + 39 manifesto tests + assemble `--check` |
| A2 barred cards/public | PASS |
| A2 trophic | PASS |
| A2 purity | FAIL — pre-existing Skyzai/Helios/K2 tokens in v0.1 drafts. Not raced. |
| A2 links | FAIL — 1 missing `CANON_AMENDMENT_BRIEF_SEED_VS_NO_POTENTIAL_2026_08_05.md`. Not invented. |
| A2 predeploy | FAIL — 888 errors (tinycss2 pin, withheld headers, claim compile, ratchet). Not a this-loop heal. |
| A3 | Done — `PUBLIC_CURRENT_BODY_READER_STAGED.html` off-site, 3 tests green |
| A4 | Done — `G10_PUBLIC_RELEASE_PROTOCOL.md`, all boxes unpaid |
| A5 | Reciprocal/Sarpasya/SES retargeted (hash match). Six Lenses pin not found. Compile stays red. Receipt: `MISSING_ARCHIVE_SKYZAI_PATHS_2026_08_13.md` |

## Order

1. A1 (always)
2. A2 (named G9 remainder)
3. A3 (staged reader preview, off-site)
4. A4 (G10 protocol on paper)
5. A5 (archive hunt or missing-archive receipt)
6. Stop and wait for Lane B. Do not drink.

## Stop rule

The loop may continue as hygiene. It may crown only when CURRENT stays poison-free **and** G10 is paid **and** a live host serves the bytes **and** world contact is not treated as internal cleanup.
