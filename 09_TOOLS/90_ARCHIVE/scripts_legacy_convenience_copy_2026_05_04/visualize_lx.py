#!/usr/bin/env python3
"""
visualize_lx.py — Plot L(x) = x/(1-x) and save to PNG.

The L(x) function governs all rates in the organism:
interest rates, leverage ratios, risk multipliers, position sizing.

The equator (x=0.5, L=1.0) is the operating point.
Below 0.5: stagnation. Above 0.8: explosion. Above 0.95: catastrophe.

Run: python3 EMERGENTISM_ORG/09_TOOLS/visualize_lx.py
Output: EMERGENTISM_ORG/09_TOOLS/lx_curve.png
"""

import sys
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_PNG = OUTPUT_DIR / "lx_curve.png"


def generate_text_art() -> str:
    """Generate a text-art version of L(x) for embedding in docs."""
    lines = [
        "L(x) = x / (1-x)  —  The Rate Curve That Governs Everything",
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
        "   1+- - - - - - - * - - - - - - -   <-- EQUATOR (x=0.5, L=1.0)",
        "   |            /",
        " 0.5+        /",
        "   |      /",
        " 0.2+  /",
        "   | /",
        "   0+---+---+---+---+---+---+---+---+---+---+-> x",
        "   0  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0",
        "",
        "  STAGNATION    |  SAFE ZONE  |  DANGER  | CATASTROPHE",
        "    (0-0.2)     | (0.3-0.7)   | (0.8-0.9)| (>0.95)",
        "   L < 0.25     | L = 0.4-2.3 | L = 4-9  | L -> infinity",
        "",
        "Key points:",
        "  x=0.50  L=1.00  The equator. phi=nu. Maximum balance. Operating point.",
        "  x=0.618 L=1.62  The golden ratio. phi-split threshold.",
        "  x=0.80  L=4.00  Danger zone. 4x leverage. One shock kills you.",
        "  x=0.90  L=9.00  Critical. 9x leverage. Liquidation imminent.",
        "  x=0.95  L=19.0  Catastrophe. System cannot survive any perturbation.",
        "",
        "This is why the equator is the operating point.",
        "This is why idle ZAI decays (demurrage pushes x away from 0).",
        "This is why the Faucet closes at low transparency (truth prevents x -> 1).",
        "This is why Grace Exit exists (escape before x reaches catastrophe).",
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

    # Zone fills
    ax.axvspan(0, 0.2, alpha=0.15, color="#FF4444", label="Stagnation")
    ax.axvspan(0.3, 0.7, alpha=0.10, color="#44FF44", label="Safe Zone")
    ax.axvspan(0.8, 0.98, alpha=0.15, color="#FF4444", label="Danger Zone")

    # Equator marker
    ax.plot(0.5, 1.0, "o", color="#FFD600", markersize=12, zorder=5)
    ax.annotate(
        "EQUATOR\nx=0.5, L=1.0\nphi = nu",
        xy=(0.5, 1.0), xytext=(0.25, 5),
        fontsize=11, color="#FFD600", fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#FFD600", lw=1.5),
    )

    # Golden ratio marker
    ax.plot(0.618, 1.618, "D", color="#FF8C00", markersize=8, zorder=5)
    ax.annotate(
        "Golden Ratio\nx=0.618, L=1.618",
        xy=(0.618, 1.618), xytext=(0.72, 3),
        fontsize=9, color="#FF8C00",
        arrowprops=dict(arrowstyle="->", color="#FF8C00", lw=1),
    )

    # Danger markers
    ax.axhline(y=4, color="#FF4444", linestyle="--", alpha=0.5, linewidth=1)
    ax.text(0.02, 4.2, "DANGER (L=4, x=0.80)", color="#FF4444", fontsize=9, alpha=0.7)
    ax.axhline(y=9, color="#FF0000", linestyle="--", alpha=0.5, linewidth=1)
    ax.text(0.02, 9.3, "CRITICAL (L=9, x=0.90)", color="#FF0000", fontsize=9, alpha=0.7)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 15)
    ax.set_xlabel("x (utilization / exposure / leverage ratio)", color="white", fontsize=12)
    ax.set_ylabel("L(x) = x/(1-x)", color="white", fontsize=12)
    ax.set_title(
        "L(x) — The Rate Curve That Governs Everything",
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
