from __future__ import annotations

import json
import unittest
from pathlib import Path


# --- TitanFrame: the smallest type system that satisfies CM-04 ---------------
#
# CM-04 (49_FINITY_RECOVERY_AND_COUNTERMODEL_SUITE.md §CM-04; spec §1):
#   `zero_T × unbounded_T` must fail type checking; no Titan arithmetic.
#
# TitanFrame is a closed inductive type. Its only inhabitants are the three
# named tags; it has no numeric instances and no arithmetic operations other
# than `__mul__`, which exists solely to refuse Titan × Titan multiplication.
# Spec §1 declares `render_T : TitanFrame → Glyph` as the only legitimate
# operation on TitanFrame; this module enforces the negative: there is no
# `__add__`, no `__truediv__`, no coercion path that would let a TitanFrame
# become a Number, Field[F], or ProjectivePoint[P1(F)] (spec §1: "TitanFrame
# ↛ Number / ↛ Field[F] / ↛ ProjectivePoint[P1(F)]").

class TitanFrame:
    __slots__ = ("tag",)
    _VALID = frozenset({"zero_T", "one_T", "unbounded_T"})

    def __init__(self, tag: str) -> None:
        if tag not in TitanFrame._VALID:
            raise ValueError(f"unknown TitanFrame tag: {tag!r}")
        self.tag = tag

    def __repr__(self) -> str:
        return self.tag

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TitanFrame) and self.tag == other.tag

    def __hash__(self) -> int:
        return hash(("TitanFrame", self.tag))

    def __mul__(self, other: object):
        # CM-04: Titan × Titan multiplication is not a well-formed term.
        if isinstance(other, TitanFrame):
            if {self.tag, other.tag} == {"zero_T", "unbounded_T"}:
                raise TypeError(
                    f"CM-04: TitanFrame multiplication {self.tag} × {other.tag} "
                    f"is not a well-formed term (no Titan arithmetic)."
                )
        return NotImplemented


zero_T = TitanFrame("zero_T")
one_T = TitanFrame("one_T")
unbounded_T = TitanFrame("unbounded_T")
# --- end TitanFrame ---------------------------------------------------------


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM"


class FinityBoundarySpecificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = (FORMAL / "47_FINITY_BOUNDARY_CALCULUS_SPEC.md").read_text(encoding="utf-8")
        cls.ledger = json.loads((FORMAL / "48_FINITY_PARADOX_LEDGER.yaml").read_text(encoding="utf-8"))
        cls.countermodels = (FORMAL / "49_FINITY_RECOVERY_AND_COUNTERMODEL_SUITE.md").read_text(encoding="utf-8")

    def test_cm04_zero_T_times_unbounded_T_raises(self) -> None:
        """CM-04: zero_T × unbounded_T must fail type checking; no Titan arithmetic."""
        with self.assertRaises(TypeError) as ctx:
            _ = zero_T * unbounded_T
        self.assertIn("CM-04", str(ctx.exception))

    def test_cm04_holds_in_both_argument_orders(self) -> None:
        """CM-04 is symmetric; Titan arithmetic has no implicit order. The
        raised error must come from the TitanFrame type system, not from
        Python's generic `*` fallback — checked by CM-04 tag in the message."""
        with self.assertRaises(TypeError) as ctx:
            _ = unbounded_T * zero_T
        self.assertIn("CM-04", str(ctx.exception))

    def test_titanframe_has_no_numeric_or_field_coercion(self) -> None:
        """Spec §1: TitanFrame ↛ Number / ↛ Field[F] / ↛ ProjectivePoint. There
        is no __int__, __float__, __add__, or __truediv__ that could create one."""
        for t in (zero_T, one_T, unbounded_T):
            self.assertFalse(isinstance(t, (int, float, complex)),
                             f"{t!r} must not be a numeric instance")
        for forbidden in ("__int__", "__float__", "__complex__", "__add__", "__truediv__"):
            self.assertFalse(hasattr(TitanFrame, forbidden),
                             f"TitanFrame must not define {forbidden} (no silent coercion)")

    def test_titanframe_tag_set_is_closed(self) -> None:
        """TitanFrame is a closed inductive type with exactly three members."""
        members = {t.tag for t in (zero_T, one_T, unbounded_T)}
        self.assertEqual(members, {"zero_T", "one_T", "unbounded_T"})
        with self.assertRaises(ValueError):
            TitanFrame("not_a_tag")
        # __mul__ with a non-Titan returns NotImplemented (no silent coercion
        # to or from Number / Field[F] / ProjectivePoint[P1(F)]).
        self.assertIs(zero_T.__mul__(0), NotImplemented)
        self.assertIs(zero_T.__mul__(0.0), NotImplemented)
        self.assertIs(zero_T.__mul__(1 + 2j), NotImplemented)

    def test_standard_recovery_and_smallest_extension_are_mandatory(self) -> None:
        for marker in ("conservativity", "Smallest-extension test", "Native recovery", "Independent review"):
            self.assertIn(marker, self.spec)

    def test_paradox_rows_are_scoped_and_typed(self) -> None:
        rows = self.ledger["rows"]
        self.assertGreaterEqual(len(rows), 9)
        allowed = set(self.ledger["classifications"])
        self.assertTrue(all(row["classification"] in allowed for row in rows))
        self.assertEqual(len({row["id"] for row in rows}), len(rows))
        for row in rows:
            for field in ("formal_domain", "native_account", "recovered_result", "residual", "rivals", "kill"):
                self.assertTrue(row[field], f"{row['id']} missing {field}")

    def test_open_physics_is_not_promoted(self) -> None:
        measurement = next(row for row in self.ledger["rows"] if row["id"] == "MEAS-01")
        self.assertEqual(measurement["classification"], "unresolved_question")
        self.assertEqual(measurement["evidence_tier"], "C")


if __name__ == "__main__":
    unittest.main()
