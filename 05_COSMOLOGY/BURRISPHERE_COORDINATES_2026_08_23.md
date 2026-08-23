---
title: "Burrisphere coordinates — 2026-08-23"
date: 2026-08-23
status: "WORKTREE DRAFT — display and chart contract. may_sign=false."
evidence_tier: "[A] reciprocal-chart identities; [I] named projections and horizon labels; [C] Dharma / opportunity-cost transfer"
owner: "Yves R. Burri"
machine: "./burrisphere_coordinates.json"
depends_on:
  - "./00_CANONICAL_FORMULA_BLOCK.md"
  - "./00_THE_BURRISPHERE.md"
  - "../00_HANDOFF/EMERGENTISM_HORIZON_BALANCE_OWNER_DIRECTION_2026_08_23.md"
  - "../00_HANDOFF/EMERGENTISM_ORG_V2.2_QUESTION_ATLAS_CHARTER_2026_08_23.md"
---

# Burrisphere coordinates (2026-08-23)

Display geometry and chart numbers for one selected Burrisphere. This file
does not override owners. The sphere remains a reader projection.

Lowercase chart coordinates `φ, ν` are not uppercase powers `Φ₅, Φ̂₄, V₄`.

## Four strategic quadrants

M4 cells occupy four azimuthal sectors on the selected 360° itinerary.
Direction (self ↔ other) crosses channel (possible `Φ` ↔ actual `V`).

| Sector | Azimuth (deg, half-open) | Cell | Direction | Channel |
| --- | --- | --- | --- | --- |
| Q1 | `[0, 90)` | Taking-Φ | self / ego-facing | possible / model (`Φ`) |
| Q2 | `[90, 180)` | Taking-V | self / ego-facing | actual / embodied (`V`) |
| Q3 | `[180, 270)` | Giving-Φ | other / collective-facing | possible / model (`Φ`) |
| Q4 | `[270, 360)` | Giving-V | other / collective-facing | actual / embodied (`V`) |

Bare ego/collective signs are insufficient: they would merge Taking-Φ with
Taking-V and Giving-Φ with Giving-V. The path encounters all four sectors
in displayed reading order. The path is not a continuous G7 state and does
not turn a Titan frame into a move.

## 360° ascending projection

A selected display itinerary `[I]` rises from the Śiva bottom station to the
Brahmā top station while completing **one 360° turn** around the Titan axis.
Viṣṇu `1_T` marks the centre latitude. Phase and handedness are visualization
choices, not time, recurrence, moral ranking, developmental necessity,
physical dynamics, causal mechanism, or a geometric derivation of seven.

Parametric form (selected, not forced):

```text
s ∈ [0, 1]
θ(s) = π · s                          south-origin polar parameter
λ(s) = 2π · s                         one full azimuth
```

At `s=0`: Śiva. At `s=1/2`: Viṣṇu latitude with λ=π. At `s=1`: Brahmā
after one full turn.

## V / Φ poles

On the positive reciprocal chart:

```text
φ := cot(θ/2),   ν := tan(θ/2),   φ · ν = 1
```

Selected orientation (south-origin `θ`):

| Pole | Geographic word | Raw chart | Raw power reading `[I]` |
| --- | --- | --- | --- |
| Φ-pole | south `•` | `θ→0`, `φ→∞`, `ν→0` | long-horizon future potential → `Φ` |
| V-pole | north `○` | `θ→π`, `ν→∞`, `φ→0` | short-horizon present power → `V` |

**Raw poles** diverge: `V→∞` at the V-pole, `Φ→∞` at the Φ-pole. Those
infinities are chart limits, not scores.

**Normalized scores** stay in `[0, 1]`:

```text
v := ν / (φ + ν)          short-horizon / Vward weight   (= w_S)
φ̂ := φ / (φ + ν)         long-horizon / Φward weight    (= w_L)
v + φ̂ = 1
product  P̂ := v · φ̂ = νφ / (φ+ν)² ≤ 1/4
```

The **product of normalized scores is maximized uniquely at `v = φ̂ = 1/2`**,
which is the chart centre **`φ = ν = 1`** (`θ = π/2`). Equivalently,
`B = 2/(φ+ν) = sin θ ≤ 1` equals 1 only there `[A]`. The constraint product
`φν = 1` is constant on the whole chart and **cannot** select the centre.

Do not rank nodes by a raw uppercase product `Φ × V`. Historical `ΦV`
ranking is retired.

## Three Titan stations (numeric)

South-origin polar `θ` in radians; geographic latitude
`lat_deg = 90 − (180/π)θ` only as a display alias.

| Station | Titan | Glyph | θ (rad) | θ (deg) | lat_deg | φ | ν | v | φ̂ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Śiva / dissolution | `0_T` Ground | `•` | `0` | `0` | `−90` | `+∞` | `0` | `0` | `1` |
| Viṣṇu / preservation | `1_T` Unit | `⊙` | `π/2` | `90` | `0` | `1` | `1` | `0.5` | `0.5` |
| Brahmā / creation | `∞_T` Horizon | `○` | `π` | `180` | `+90` | `0` | `+∞` | `1` | `0` |

Azimuth of a station on the axis is undefined (the axis is the pole of `λ`).
The itinerary assigns `λ(0)=0`, `λ(1/2)=π`, `λ(1)=2π ≡ 0`.

Machine copy: [`burrisphere_coordinates.json`](burrisphere_coordinates.json).

## Horizon overlay (named `[I]`)

- Short-horizon **present power** is read **Vward** (ν-dominant).
- Long-horizon **future potential** is read **Φward** (φ-dominant).
- The **centre** is the unique equal-weight chart point and is a **candidate**
  for **minimum opportunity-cost** and for **Dharma / flow** only in domains
  where present enactment and future-option retention are complementary under
  declared premises `[C]`. The transfer is untested.

The overlay does **not** claim that the centre removes every real tradeoff,
equalizes clocks, or derives Dharma, Justice, or the Good from geometry.
Specialized domains may lawfully optimize off-centre. Represented futures
still act only through present D4 carriers. The Burrisphere path is not a
clock.

## G7 operational 4+3 vs Burrisphere geometric 3+1+3

| Object | Composition | Source of seven |
| --- | --- | --- |
| G7 operational | **4+3** = M4 transfers ⊎ F3 Titan frames | selected vocabulary `[S]` |
| Burrisphere geometric | **3+1+3** = three southern GEN7 stations + equator + three northern | selected equal-station meridian `[I]` after seven are chosen |

`G7@1 ≠ GEN7@1`. Shared count transfers no proof.

**Join rule:** the two sevens may be drawn together **only** through a
**named `[I]` projection**. This file names that projection

`BurrisphereDisplayItinerary.v1`

and nothing else. No silent identification of a transfer with a frame, of
M4 with a latitude band, or of G7 with GEN7.

M4 compression protocol: [`M4Compression.v1/README.md`](M4Compression.v1/README.md).
