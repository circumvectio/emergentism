#!/usr/bin/env python3
"""
Weighted sphere-spectrum baseline for V(theta) = 2/sin(theta) - 2 on S^2.

This script solves the weighted self-adjoint Sturm-Liouville problem

    -(1/2) d/dtheta (sin(theta) dpsi/dtheta) + V(theta) sin(theta) psi
        = E sin(theta) psi

on theta in (0, pi) using a finite-volume / generalized-eigenvalue discretization.
"""

from __future__ import annotations

import argparse
import numpy as np
from scipy.linalg import eigh


def compute_spectrum(num_points: int = 1200, num_states: int = 10) -> np.ndarray:
    h = np.pi / (num_points + 1)
    theta = np.linspace(h, np.pi - h, num_points)
    s = np.sin(theta)
    s_minus = np.sin(theta - h / 2.0)
    s_plus = np.sin(theta + h / 2.0)
    potential = 2.0 / s - 2.0

    operator = np.zeros((num_points, num_points))
    diag = 0.5 * (s_plus + s_minus) / h**2 + potential * s
    upper = -0.5 * s_plus[:-1] / h**2
    lower = -0.5 * s_minus[1:] / h**2

    operator[np.diag_indices(num_points)] = diag
    operator[np.arange(num_points - 1), np.arange(1, num_points)] = upper
    operator[np.arange(1, num_points), np.arange(num_points - 1)] = lower

    weight = np.diag(s)
    max_index = min(num_states - 1, num_points - 1)
    eigenvalues, _ = eigh(operator, weight, subset_by_index=[0, max_index])
    return eigenvalues


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--points", type=int, default=1200, help="Number of interior grid points")
    parser.add_argument("--states", type=int, default=10, help="Number of low states to print")
    args = parser.parse_args()

    values = compute_spectrum(args.points, args.states)
    print("# weighted sphere spectrum")
    print(f"points={args.points} states={len(values)}")
    for i, value in enumerate(values):
        print(f"E_{i} = {value:.6f}")


if __name__ == "__main__":
    main()
