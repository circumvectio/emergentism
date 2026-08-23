"""Fail-closed tests for FAL-01 Fiber-Asymmetry Lemma.

Earned report tag: PROJECTION_ASYMMETRY_PROVEN
Forbidden report tag: ONTOLOGICAL_STRONG_EMERGENCE_PROVEN

These tests exercise declared reconstruction models only. They do not
claim physical strong emergence.
"""

from __future__ import annotations

import math
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, FrozenSet, Generic, Hashable, TypeVar

L = TypeVar("L", bound=Hashable)
H = TypeVar("H", bound=Hashable)

ONTOLOGY = Path(__file__).resolve().parents[1]
LEMMA = ONTOLOGY / "SLWP_FIBER_ASYMMETRY_2026_08_23.md"
OWNER = ONTOLOGY / "12_STRONG_LIFT_WEAK_PROJECTION_CONJECTURE_SLWP_01.md"

EARNED_TAG = "PROJECTION_ASYMMETRY_PROVEN"
FORBIDDEN_TAG = "ONTOLOGICAL_STRONG_EMERGENCE_PROVEN"

SLOTS = (
    "projection_loss",
    "computational_opacity",
    "ontological_irreducibility",
    "downward_intervention",
)


@dataclass(frozen=True)
class ReconstructionModel(Generic[L, H]):
    name: str
    lowers: FrozenSet[L]
    highers: FrozenSet[H]
    U: Callable[[H], L]
    s: Callable[[L], H]

    def check_types(self) -> None:
        for h in self.highers:
            ell = self.U(h)
            if ell not in self.lowers:
                raise AssertionError(f"{self.name}: U({h!r})={ell!r} not in L")
        for ell in self.lowers:
            h = self.s(ell)
            if h not in self.highers:
                raise AssertionError(f"{self.name}: s({ell!r})={h!r} not in H")

    def section_identity(self) -> bool:
        return all(self.U(self.s(ell)) == ell for ell in self.lowers)

    def retraction_is_identity(self) -> bool:
        return all(self.s(self.U(h)) == h for h in self.highers)

    def fiber(self, ell: L) -> FrozenSet[H]:
        return frozenset(h for h in self.highers if self.U(h) == ell)

    def has_nontrivial_fiber(self) -> bool:
        return any(len(self.fiber(ell)) >= 2 for ell in self.lowers)

    def report_tag(self) -> str:
        if self.section_identity() and self.has_nontrivial_fiber():
            if self.retraction_is_identity():
                raise AssertionError(
                    f"{self.name}: nontrivial fiber cannot satisfy s\u2218U = id"
                )
            return EARNED_TAG
        return "NO_PROJECTION_ASYMMETRY"

    def forbidden_promotion(self) -> str:
        return "REFUSED"


def bit_forget_model() -> ReconstructionModel[int, tuple[int, int]]:
    """CM-grain / positive instance: forget the selector bit."""
    lowers = frozenset({0, 1, 2})
    highers = frozenset((n, sigma) for n in lowers for sigma in (0, 1))
    return ReconstructionModel(
        name="bit_forget",
        lowers=lowers,
        highers=highers,
        U=lambda h: h[0],
        s=lambda n: (n, 0),
    )


def identity_model() -> ReconstructionModel[int, int]:
    """CM-id: trivial fibers, both composites are identities."""
    xs = frozenset({0, 1, 2})
    return ReconstructionModel(
        name="identity",
        lowers=xs,
        highers=xs,
        U=lambda x: x,
        s=lambda x: x,
    )


def iso_model() -> ReconstructionModel[int, str]:
    """CM-iso: unique inverse, selector idle."""
    lowers = frozenset({0, 1, 2})
    table = {0: "a", 1: "b", 2: "c"}
    inverse = {v: k for k, v in table.items()}
    return ReconstructionModel(
        name="iso",
        lowers=lowers,
        highers=frozenset(table.values()),
        U=lambda h: inverse[h],
        s=lambda n: table[n],
    )


def slot_status(slot: str, model_tag: str) -> str:
    if slot not in SLOTS:
        raise KeyError(slot)
    if slot == "projection_loss" and model_tag == EARNED_TAG:
        return "EARNED_IN_DECLARED_MODEL"
    return "UNEARNED"


class FiberAsymmetryLemmaTests(unittest.TestCase):
    def test_bit_forget_section_and_nontrivial_fibers(self) -> None:
        m = bit_forget_model()
        m.check_types()
        self.assertTrue(m.section_identity())
        self.assertTrue(m.has_nontrivial_fiber())
        self.assertFalse(m.retraction_is_identity())
        self.assertEqual(m.report_tag(), EARNED_TAG)
        self.assertEqual(m.forbidden_promotion(), "REFUSED")
        self.assertEqual(m.U((1, 0)), m.U((1, 1)))
        self.assertNotEqual(m.s(m.U((1, 1))), (1, 1))

    def test_identity_countermodel_no_asymmetry(self) -> None:
        m = identity_model()
        m.check_types()
        self.assertTrue(m.section_identity())
        self.assertTrue(m.retraction_is_identity())
        self.assertFalse(m.has_nontrivial_fiber())
        self.assertEqual(m.report_tag(), "NO_PROJECTION_ASYMMETRY")

    def test_iso_countermodel_no_asymmetry(self) -> None:
        m = iso_model()
        m.check_types()
        self.assertTrue(m.section_identity())
        self.assertTrue(m.retraction_is_identity())
        self.assertFalse(m.has_nontrivial_fiber())
        self.assertEqual(m.report_tag(), "NO_PROJECTION_ASYMMETRY")

    def test_slots_fail_closed_except_projection_loss(self) -> None:
        earned = bit_forget_model().report_tag()
        none = identity_model().report_tag()
        self.assertEqual(slot_status("projection_loss", earned), "EARNED_IN_DECLARED_MODEL")
        self.assertEqual(slot_status("projection_loss", none), "UNEARNED")
        for slot in (
            "computational_opacity",
            "ontological_irreducibility",
            "downward_intervention",
        ):
            self.assertEqual(slot_status(slot, earned), "UNEARNED")
            self.assertEqual(slot_status(slot, none), "UNEARNED")

    def test_lemma_file_earns_only_projection_tag(self) -> None:
        text = LEMMA.read_text(encoding="utf-8")
        self.assertIn(EARNED_TAG, text)
        self.assertIn("report_tag_forbidden", text)
        self.assertIn(FORBIDDEN_TAG, text)
        self.assertIn('report_tag_earned: "PROJECTION_ASYMMETRY_PROVEN"', text)
        self.assertNotIn(
            'report_tag_earned: "ONTOLOGICAL_STRONG_EMERGENCE_PROVEN"', text
        )
        self.assertIn('computational_opacity: "UNEARNED"', text)
        self.assertIn('ontological_irreducibility: "UNEARNED"', text)
        self.assertIn('downward_intervention: "UNEARNED"', text)
        self.assertIn("does not prove physical strong emergence", text)

    def test_owner_still_open_and_does_not_claim_strong_emergence(self) -> None:
        text = OWNER.read_text(encoding="utf-8")
        self.assertIn("SLWP-01", text)
        self.assertIn("U_n \u2218 s_(n,\u03c3) = id_(L_n)", text)
        self.assertIn("They do not by themselves prove strong emergence", text)
        self.assertIn("PA-SLWP-01 = PARTIAL / BRIDGE NOT ESTABLISHED", text)


class PathSensitiveArithmeticTests(unittest.TestCase):
    """Ordinary arithmetic vs extended labels vs limits must not collapse."""

    def test_ordinary_zero_times_finite_is_zero(self) -> None:
        for m in (0, 1, 7, 10**6):
            self.assertEqual(0 * m, 0)

    def test_ordinary_division_by_zero_undefined(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            _ = 5 / 0

    def test_limit_form_is_path_sensitive(self) -> None:
        ks = range(1, 80)

        def products(xk, yk):
            return [xk(k) * yk(k) for k in ks]

        zero_path = products(lambda k: 1 / k**2, lambda k: float(k))
        finite_n = products(lambda k: 4 / k, lambda k: float(k))
        inf_path = products(lambda k: 1 / k, lambda k: float(k**2))
        osc_path = products(
            lambda k: (2 + (-1) ** k) / (2 * k), lambda k: float(k)
        )

        # (1/k^2)*k = 1/k → 0; same endpoints, four different product behaviors.
        self.assertAlmostEqual(zero_path[-1], 1 / 79, places=12)
        self.assertLess(zero_path[-1], zero_path[0])
        self.assertTrue(all(abs(p - 4.0) < 1e-12 for p in finite_n))
        self.assertTrue(inf_path[-1] > inf_path[0])
        self.assertGreater(inf_path[-1], 70)
        osc_vals = set(round(p, 10) for p in osc_path)
        self.assertGreaterEqual(len(osc_vals), 2)

    def test_limit_n_over_eps_is_not_field_division_by_zero(self) -> None:
        n = 3.0
        seq = [n / (10 ** (-k)) for k in range(1, 8)]
        self.assertTrue(seq[-1] > seq[0])
        with self.assertRaises(ZeroDivisionError):
            _ = n / 0.0

    def test_mixing_ordinary_zero_infinity_is_a_type_error(self) -> None:
        """CM-arith: there is no ordinary product 0\u00b7\u221e."""

        class ExtendedLabel:
            def __init__(self, tag: str) -> None:
                self.tag = tag

            def __mul__(self, other: object) -> object:
                if isinstance(other, ExtendedLabel):
                    raise TypeError(
                        "CM-arith: 0\u00b7\u221e is not an ordinary product; "
                        "use a declared path or refuse the term"
                    )
                return NotImplemented

        zero_hat = ExtendedLabel("0")
        inf_hat = ExtendedLabel("+inf")
        with self.assertRaises(TypeError) as ctx:
            _ = zero_hat * inf_hat
        self.assertIn("CM-arith", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
