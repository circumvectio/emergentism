#!/usr/bin/env python3
"""
Flat 1D control for the cosh potential used in the log-form comparison.

This solves

    -psi''(u) + (2 cosh(u) - 2) psi(u) = E psi(u)

on a large symmetric interval with Dirichlet boundary conditions.
"""

from __future__ import annotations

import argparse
import numpy as np
from scipy.linalg import eigh_tridiagonal


def compute_spectrum(num_points: int = 2000, half_width: float = 8.0, num_states: int = 5) -> np.ndarray:
    h = 2.0 * half_width / (num_points + 1)
    u = np.linspace(-half_width + h, half_width - h, num_points)
    potential = 2.0 * np.cosh(u) - 2.0

    diagonal = 2.0 / h**2 + potential
    off_diagonal = -np.ones(num_points - 1) / h**2
    values = eigh_tridiagonal(
        diagonal,
        off_diagonal,
        select="i",
        select_range=(0, min(num_states - 1, num_points - 1)),
    )[0]
    return values


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--points", type=int, default=2000, help="Number of interior grid points")
    parser.add_argument("--half-width", type=float, default=8.0, help="Half-width of the symmetric box")
    parser.add_argument("--states", type=int, default=5, help="Number of low states to print")
    args = parser.parse_args()

    values = compute_spectrum(args.points, args.half_width, args.states)
    print("# flat 1D cosh control")
    print(f"points={args.points} half_width={args.half_width} states={len(values)}")
    for i, value in enumerate(values):
        print(f"E_{i} = {value:.6f}")


if __name__ == "__main__":
    main()
