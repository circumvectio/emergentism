"""Bounded mathematical checks for a tombstone-scope audit, not canon validation.

Run with python3 -B <this file>. Read-only: no network, file writes or adoption.
The source pins detect changes since this review, not falsehood in changed text.
"""
from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib.util
import math
from pathlib import Path
import re
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
# Public corpus digests, verified with shasum -a 256 on 2026-09-05.
SOURCES = {
    '00_META/00_THE_CLAIM_STATUS_REGISTER.md': '7d176b2bf0d0d34abaf732d56986cafbafc83d95dd2b21163a23b36c22bd7a12',  # pragma: allow-secret
    '14_THE_DISTILLATION/04_WHAT_DIED.md': '2753cfc380135cc842bff68ca865ee70a38cdd772486dc7b1e9484802c458d84',  # pragma: allow-secret
    '11_UPLINK/50_AUDITS_AND_EXECUTIONS/126_WELTANSCHAUUNG_FORMAL_AUDIT_2026_07_13.md': '19c3593746bacb6719b1d174fa3ec26dc67cac781bd6b21cb8a5abd304d39044',  # pragma: allow-secret
    '11_UPLINK/50_AUDITS_AND_EXECUTIONS/117_FORCE_LADDER_FORMALIZED_07B.md': '8495d8141d2e41f33744b69b6f274c8fabd085bd3feffe8852efa70f85c51a33',  # pragma: allow-secret
    '11_UPLINK/50_AUDITS_AND_EXECUTIONS/117_PATH_D_NEGATIVE_RESULT.md': 'a8448087fd08fc7ff6fa6cabf50109fc4d6a4b7878e50bb160276c49d68ebbad',  # pragma: allow-secret
    '11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_THE_RECORD_LEDGER.md': '538fbdc4031dc452348a65a07356733d6ccaa1a9890a26ee8a3c3b9e6c0db028',  # pragma: allow-secret
    '03_METHODOLOGY/02_THE_PAPERS/PAPER_P_SU3_OBSTRUCTION_BARE_S2.md': '9a379c0196a5100c7cf66e133286df3e9bb4b174f04e3c86fab739650bbeca47',  # pragma: allow-secret
    '05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md': 'ba48ac8689d31032d3569b62c195bf992ba4b43bfe963e6162d5b77dac32d252',  # pragma: allow-secret
    '05_COSMOLOGY/00_D5_THE_SEVEN_GENERATIVE_ACTIONS.md': 'a39a3e01255d208b852c158635507083127d46719e446ef88d2904b8a742a25c',  # pragma: allow-secret
    '05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md': '21bfad3bb6089fa2d304c1745738eeb9ce035bf201b73b0b7ad79019b29490ef',  # pragma: allow-secret
    '12_PUBLIC_SITE/_PLANS/rosetta_row_probe.py': '65c74e17ec2b22faefc5b4c9f2cd837548f172bff525ed8f927a0d504077ec78',  # pragma: allow-secret
}


def inversion(z):
    """Selected projective toy carrier; None denotes numeric infinity, no Titan."""
    return 0 if z is None else None if z == 0 else 1 / z


def negation(z):
    return None if z is None else -z


def closure(seed, operations):
    result = set(seed)
    while True:
        expanded = result | {f(z) for f in operations for z in result}
        if expanded == result:
            return result
        result = expanded


def potential(s):
    return 4 * math.sinh(s) ** 2


def derivative(s):
    return 4 * math.sinh(2 * s)


class SourceChecks(unittest.TestCase):
    def test_reviewed_sources_are_unchanged(self):
        for path, digest in SOURCES.items():
            with self.subTest(path=path):
                self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), digest,
                                 'Source changed: re-review; do not silently repin.')

    def test_register_denominator_and_status_partition(self):
        text = (ROOT / '00_META/00_THE_CLAIM_STATUS_REGISTER.md').read_text()
        block = text.split('## 5 · The graves, adjudicated', 1)[1].split('### What the adjudication shows', 1)[0]
        rows = re.findall(r'^\| `(DF-\d{2})` \| .*? \| `([^`]+)`', block, re.M)
        self.assertEqual(len(rows), 22)
        self.assertEqual({row[0] for row in rows}, {f'DF-{n:02}' for n in range(1, 23)})
        self.assertEqual(Counter(status for _, status in rows), {
            'FORMALLY-REFUTED': 10, 'EMPIRICALLY-REFUTED': 3, 'CATEGORY-ERROR': 4,
            'NOT-WELL-POSED': 3, 'NARROWED': 1, 'PROCESS-DEFECT': 1,
        })


class ScopeCounterexamples(unittest.TestCase):
    def test_inversion_does_not_generate_fixed_points_from_endpoints(self):
        self.assertEqual(closure({Q(0), None}, [inversion]), {Q(0), None})

    def test_selected_triple_is_closed_but_negation_changes_the_problem(self):
        triple = {Q(0), Q(1), None}
        self.assertEqual(closure(triple, [inversion]), triple)
        self.assertEqual(closure(triple, [inversion, negation]), triple | {Q(-1)})
        self.assertEqual(closure({Q(0), None}, [inversion, negation]), {Q(0), None})

    def test_fixed_point_equation_has_two_numeric_solutions(self):
        for z in [Q(-1), Q(1)]:
            self.assertEqual(inversion(z), z)
        # Completeness is the polynomial factorization, not this finite sample:
        # z = 1/z iff z^2 - 1 = (z-1)(z+1) = 0 over C, z != 0.
        self.assertNotEqual(inversion(Q(2)), Q(2))

    def test_reciprocal_product_is_constant_while_balance_changes(self):
        for phi in [Q(1, 4), Q(1, 2), Q(1), Q(2), Q(4)]:
            nu = 1 / phi
            self.assertEqual(phi * nu, 1)
            balance = 2 / (phi + nu)
            self.assertLessEqual(balance, 1)
            self.assertEqual(balance == 1, phi == 1)
        self.assertEqual(2 / (Q(2) + Q(1, 2)), Q(4, 5))

    def test_boundary_conditions_do_not_select_unique_aggregator(self):
        candidates = [lambda x, y: x * y, min]
        grid = [Q(n, 4) for n in range(5)]
        for f in candidates:
            self.assertEqual(f(Q(1), Q(1)), 1)
            for x in grid:
                self.assertEqual(f(x, Q(0)), 0)
                self.assertEqual(f(Q(0), x), 0)
                for a, b in zip(grid, grid[1:]):
                    self.assertLessEqual(f(a, x), f(b, x))
                    self.assertLessEqual(f(x, a), f(x, b))
        self.assertNotEqual(candidates[0](Q(1, 2), Q(1, 2)), candidates[1](Q(1, 2), Q(1, 2)))

    def test_static_potential_permits_opposed_selected_dynamics(self):
        for s in [-2, -0.5, 0.5, 2]:
            d = derivative(s)
            metric = 2 * math.cosh(2 * s)
            self.assertNotEqual(d, 0)
            self.assertLess(d * (-d / metric), 0)  # chosen gradient descent
            self.assertEqual(d * 0, 0)            # chosen stationary dynamics
            self.assertGreater(d * (d / metric), 0)  # chosen gradient ascent

    def test_declared_gradient_solution_obeys_ode(self):
        for s0 in [-2, -0.5, 0.5, 2]:
            for t in [0, 0.25, 1]:
                y = math.sinh(2 * s0) * math.exp(-4 * t)
                s = math.asinh(y) / 2
                ds_dt = -2 * y / math.sqrt(1 + y * y)
                self.assertAlmostEqual(ds_dt, -2 * math.tanh(2 * s))
                self.assertLessEqual(potential(s), potential(s0) + 1e-12)

    def test_nine_symmetric_nodes_have_eightfold_relative_eigenspace(self):
        n, kappa = 9, Q(1)
        def h(v):
            return [(2 + n * kappa) * x - kappa * sum(v) for x in v]
        ones = [Q(1)] * n
        self.assertEqual(h(ones), [2 * x for x in ones])
        # e_j-e_8, j=0..7: independent (first eight coordinates are identity).
        for j in range(n - 1):
            v = [Q(int(i == j) - int(i == n - 1)) for i in range(n)]
            self.assertEqual(h(v), [(2 + n * kappa) * x for x in v])
        # Dimension counting exhausts all nine directions. No SU(3) action supplied.

    def test_positive_coupling_does_not_preclude_profitable_extraction(self):
        lam, phi = Q(1, 2), Q(1)
        def score(own, other):
            return phi * ((1 - lam) * own + lam * (own + other) / 2)
        before, after = score(Q(2, 5), Q(3, 5)), score(Q(3, 5), Q(2, 5))
        self.assertEqual(before, Q(9, 20))
        self.assertEqual(after, Q(11, 20))
        self.assertGreater(lam * phi / 2, 0)  # positive cross-agent derivative
        self.assertGreater(after - before, 0)

    def test_complementary_capability_is_not_individual_sufficiency(self):
        requirements = {'design', 'fabricate', 'test'}
        agents = [{'design'}, {'fabricate'}, {'test'}]
        self.assertTrue(all(not requirements <= own for own in agents))
        self.assertTrue(requirements <= set().union(*agents))
        # Pooling feasibility is assumed, not supplied by the union operation.
        # The sets cannot distinguish consensual cooperation from coercion.

    def test_seven_partial_signatures_do_not_yet_partition_comparisons(self):
        path = ROOT / '12_PUBLIC_SITE/_PLANS/rosetta_row_probe.py'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                         SOURCES['12_PUBLIC_SITE/_PLANS/rosetta_row_probe.py'],
                         'Do not execute a changed probe before source review.')
        spec = importlib.util.spec_from_file_location('row_probe', path)
        probe = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(probe)
        census = probe.census()
        self.assertEqual(census['comparison_records'], 81)
        self.assertEqual([census[k] for k in ['unmatched', 'single_match', 'multiple_matches']], [32, 37, 12])
        self.assertEqual(census['label_orders_preserving_same_predicates'], 5040)
        self.assertEqual(probe.matches(dict(zip(probe.FIELDS, ['up', 'same', 'same', 'same']))), [])


if __name__ == '__main__':
    unittest.main()
