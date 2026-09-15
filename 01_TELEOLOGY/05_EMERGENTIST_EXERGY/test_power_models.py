"""Conditional toy calculations only: not empirical MPP or worldview validation."""

import math
import unittest


def atwood_stroke(falling_mass, ratio, height, gravity):
    """Ideal rest-start, fixed-height stroke; reset and recovery excluded."""
    acceleration = gravity * (1 - ratio) / (1 + ratio)
    duration = math.sqrt(2 * height / acceleration)
    load_work = ratio * falling_mass * gravity * height
    return duration, load_work, load_work / duration


class PowerModelExamples(unittest.TestCase):
    def test_falling_efficiency_need_not_have_interior_maximum(self):
        # G in J/kg; v and v0 in kg/s. Derivative is positive at every v>=0.
        g_ex, v0 = 7.0, 3.0
        eta = lambda v: 1 / (1 + v / v0)
        power = lambda v: g_ex * v * eta(v)
        for v in (0, 0.5, 1, 3, 10, 100):
            with self.subTest(v=v):
                self.assertLess(eta(v + 1), eta(v))
                self.assertGreater(power(v + 1), power(v))
                self.assertLess(power(v), g_ex * v0)
                self.assertGreater(g_ex / (1 + v / v0) ** 2, 0)

    def test_bounded_rational_converter_peaks_at_upper_boundary(self):
        power = lambda v: 7 * v / (1 + v / 3)
        grid = [i / 10 for i in range(101)]
        self.assertEqual(max(grid, key=power), 10)

    def test_exponential_converter_peak_tracks_scale_not_unit_one(self):
        for v0 in (0.25, 1, 7):
            power = lambda v: 3 * v * math.exp(-v / v0)
            with self.subTest(v0=v0):
                self.assertGreater(power(v0), power(v0 * 0.9))
                self.assertGreater(power(v0), power(v0 * 1.1))
                self.assertAlmostEqual(power(v0), 3 * v0 / math.e)

    def test_atwood_closed_form_agrees_with_work_over_duration(self):
        for mass, height, gravity in ((2, 3, 9.81), (7, 0.5, 1.62)):
            for ratio in (0.1, 0.5, 0.618, 0.9):
                with self.subTest(mass=mass, ratio=ratio):
                    _, _, measured = atwood_stroke(mass, ratio, height, gravity)
                    closed = (mass * gravity * math.sqrt(gravity * height / 2)
                              * ratio * math.sqrt((1 - ratio) / (1 + ratio)))
                    self.assertAlmostEqual(measured, closed)

    def test_atwood_fixed_height_peak_and_derivative(self):
        optimum = (math.sqrt(5) - 1) / 2
        derivative_sign = lambda r: 1 - r - r * r
        power = lambda r: atwood_stroke(2, r, 3, 9.81)[2]
        self.assertAlmostEqual(derivative_sign(optimum), 0)
        self.assertGreater(derivative_sign(optimum - 0.01), 0)
        self.assertLess(derivative_sign(optimum + 0.01), 0)
        self.assertGreater(power(optimum), power(0.5))
        self.assertGreater(power(optimum), power(optimum - 0.01))
        self.assertGreater(power(optimum), power(optimum + 0.01))

    def test_atwood_remaining_energy_is_kinetic_not_disappeared(self):
        mass, height, gravity = 2, 3, 9.81
        for ratio in (0.1, 0.5, 0.9):
            acceleration = gravity * (1 - ratio) / (1 + ratio)
            speed_squared = 2 * acceleration * height
            kinetic = 0.5 * mass * (1 + ratio) * speed_squared
            released = mass * gravity * height
            _, lifted, _ = atwood_stroke(mass, ratio, height, gravity)
            with self.subTest(ratio=ratio):
                self.assertAlmostEqual(released, lifted + kinetic)
                self.assertAlmostEqual(lifted / released, ratio)

    def test_distinct_linear_loading_model_has_half_peak(self):
        power = lambda r: r * (1 - r)
        for r in (0, 0.1, 0.4, 0.618, 0.9, 1):
            with self.subTest(r=r):
                self.assertGreater(power(0.5), power(r))

    def test_present_task_rate_does_not_order_cumulative_delivery(self):
        aggressive = (100, 0, 0, 0)  # accepted tasks per one-hour interval
        reserve = (60, 60, 60, 60)
        self.assertGreater(aggressive[0], reserve[0])
        self.assertEqual(sum(aggressive), 100)
        self.assertEqual(sum(reserve), 240)
        self.assertLess(sum(aggressive), sum(reserve))
        # No energy or post-horizon capability conclusion follows from these arrays.

    def test_duplicate_policy_does_not_supply_missing_physical_dependency(self):
        required = {"controller", "power", "pump-bearing"}
        supplied = {"controller", "power"}
        for _ in range(1000):
            supplied.add("controller")
        self.assertEqual(required - supplied, {"pump-bearing"})
        self.assertFalse(required <= supplied)
        supplied.add("pump-bearing")
        self.assertTrue(required <= supplied)
        # Set inclusion in this stipulated toy is not an availability assessment.


if __name__ == "__main__":
    unittest.main()
