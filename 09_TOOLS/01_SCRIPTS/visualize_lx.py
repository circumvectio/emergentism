#!/usr/bin/env python3
"""Plot the odds transform L(x) = x/(1-x) as a bounded illustration.

The transform is an analytic map on ``0 < x < 1``. It does not by itself
govern interest, leverage, risk, ethics, or any other empirical domain. The
marked thresholds are visual reference values only; a domain that uses them
must supply its own variables, units, evidence, and kill criterion.

Run: python3 09_TOOLS/01_SCRIPTS/visualize_lx.py
Output: 09_TOOLS/03_SIMULATIONS/lx_curve.png
"""

import sys
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "03_SIMULATIONS"
OUTPUT_PNG = OUTPUT_DIR / "lx_curve.png"


def generate_text_art() -> str:
    """Generate a text-art version of L(x) for embedding in docs."""
    lines = [
        "L(x) = x / (1-x)  —  Illustrative Odds Transform",
        "",
        "  L(x)",
        "   |",
        "  20+                                              /",
        "   |                                             /",
        "  15+                                           /",
        "   |                                          /",
        "  10+                                        /",
        "   |                                       /",
        "   5+                                    /",
        "   |                                  /",
        "   3+                              /",
        "   |                           /",
        "   2+                       /",
        "   |                    /",
        "   1+- - - - - - - * - - - - - - -   <-- MIDPOINT (x=0.5, L=1.0)",
        "   |            /",
        " 0.5+        /",
        "   |      /",
        " 0.2+  /",
        "   | /",
        "   0+---+---+---+---+---+---+---+---+---+---+-> x",
        "   0  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0",
        "",
        "  REFERENCE BANDS ONLY — NO DOMAIN MEANING WITHOUT CALIBRATION",
        "",
        "Key points:",
        "  x=0.50  L=1.00  Analytic midpoint reference.",
        "  x=0.80  L=4.00  Example high-ratio reference.",
        "  x=0.90  L=9.00  Example higher-ratio reference.",
        "  x=0.95  L=19.0  Divergence becomes visually steep as x -> 1.",
        "",
        "Analytic fact: L(0.5)=1 and L(x) diverges as x approaches 1 from below.",
        "Interpretive rule: no visual threshold becomes a policy or ethic by algebra alone.",
    ]
    return "\n".join(lines)


def generate_png():
    """Generate a proper matplotlib chart."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("[visualize_lx] matplotlib not available. Text art only.")
        return False

    x = np.linspace(0.01, 0.98, 500)
    y = x / (1 - x)

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor("#0d1117")
    ax.set_facecolor("#0d1117")

    # Main curve
    ax.plot(x, y, color="#FFD600", linewidth=2.5, label="L(x) = x/(1-x)")

    # Reference bands have no empirical or normative meaning by themselves.
    ax.axvspan(0, 0.2, alpha=0.08, color="#FFFFFF", label="Low-x reference")
    ax.axvspan(0.3, 0.7, alpha=0.08, color="#FFD600", label="Mid-x reference")
    ax.axvspan(0.8, 0.98, alpha=0.08, color="#FFFFFF", label="High-x reference")

    # Equator marker
    ax.plot(0.5, 1.0, "o", color="#FFD600", markersize=12, zorder=5)
    ax.annotate(
        "MIDPOINT\nx=0.5, L=1.0",
        xy=(0.5, 1.0), xytext=(0.25, 5),
        fontsize=11, color="#FFD600", fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#FFD600", lw=1.5),
    )

    # High-ratio reference markers
    ax.axhline(y=4, color="#FF4444", linestyle="--", alpha=0.5, linewidth=1)
    ax.text(0.02, 4.2, "REFERENCE (L=4, x=0.80)", color="#FF4444", fontsize=9, alpha=0.7)
    ax.axhline(y=9, color="#FF0000", linestyle="--", alpha=0.5, linewidth=1)
    ax.text(0.02, 9.3, "REFERENCE (L=9, x=0.90)", color="#FF0000", fontsize=9, alpha=0.7)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 15)
    ax.set_xlabel("x (dimensionless input; domain meaning must be declared)", color="white", fontsize=12)
    ax.set_ylabel("L(x) = x/(1-x)", color="white", fontsize=12)
    ax.set_title(
        "L(x) — Illustrative Odds Transform",
        color="#FFD600", fontsize=14, fontweight="bold", pad=15,
    )

    ax.tick_params(colors="white")
    ax.spines["bottom"].set_color("white")
    ax.spines["left"].set_color("white")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(loc="upper left", fontsize=10, facecolor="#161b22", edgecolor="white", labelcolor="white")

    plt.tight_layout()
    plt.savefig(str(OUTPUT_PNG), dpi=150, facecolor="#0d1117")
    plt.close()
    print(f"[visualize_lx] Saved: {OUTPUT_PNG}")
    return True


def main():
    # Always generate text art
    text = generate_text_art()
    text_path = OUTPUT_DIR / "lx_curve.txt"
    text_path.write_text(text, encoding="utf-8")
    print(f"[visualize_lx] Text art: {text_path}")

    # Try PNG
    generate_png()

    # Print text art to stdout
    print()
    print(text)


if __name__ == "__main__":
    main()
