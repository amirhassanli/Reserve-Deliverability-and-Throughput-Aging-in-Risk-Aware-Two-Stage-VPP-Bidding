#!/usr/bin/env python3
"""IEEE-style figures. No titles inside the axes."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "paper" / "figures"
STAT = ROOT / "results/study_b" if (ROOT / "results/study_b").exists() else ROOT / "results"
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 8.0,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def fig_architecture():
    fig, ax = plt.subplots(figsize=(7.2, 3.15))
    ax.set_xlim(0, 12.2)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    def box(x, y, w, h, text, fc, ec="#222"):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                           facecolor=fc, edgecolor=ec, lw=1.05)
        ax.add_patch(p)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=7.2)

    def arrow(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color="#222", lw=1.05))

    box(0.15, 3.55, 2.55, 1.25, "SMARD DE-LU\nDA price, solar,\nnational load shape", "#E8F1F8")
    box(0.15, 1.85, 2.55, 1.25, "IEEE 33-bus plant\n3 BESS + 3 PV\nBaran–Wu 1989", "#F4E8D8")
    box(3.15, 2.55, 3.55, 1.85,
        "Stage 1  (hourly, 24 h)\nmean–CVaR energy bid\nXu PWL cycle-depth\nthroughput aging", "#D9EAD3")
    box(7.15, 2.55, 3.55, 1.85,
        "Stage 2  (hourly, realised)\nLinDistFlow P/Q/V\ninverter Q support\nsame aging row", "#D0E2F3")
    box(3.15, 0.25, 3.55, 1.35, "B0  EV, no aging, no V\nB2  CVaR+aging, no V\nP1  CVaR+aging + V slack", "#FCE5CD")
    box(7.15, 0.25, 3.55, 1.35, "Settlement\nDA revenue + two-price\nimbalance − aging", "#EAD1DC")

    arrow(2.70, 4.15, 3.15, 3.85)
    arrow(2.70, 2.45, 3.15, 3.05)
    arrow(6.70, 3.45, 7.15, 3.45)
    ax.text(6.90, 3.62, r"$p^{\mathrm{DA}}$", fontsize=8, ha="center")
    arrow(4.90, 2.55, 4.90, 1.60)
    arrow(8.90, 2.55, 8.90, 1.60)
    fig.tight_layout()
    fig.savefig(FIG / "Fig_architecture.png", dpi=300, bbox_inches="tight")
    plt.close()


def fig_feeder():
    """Schematic of IEEE 33-bus with BESS and PV siting."""
    pos = {}
    # main feeder 1..18
    for i in range(1, 19):
        pos[i] = (i - 1, 2.0)
    # lateral 19-22 from 2
    for k, b in enumerate(range(19, 23)):
        pos[b] = (1.0, 2.0 - 0.48 * (k + 1))
    # lateral 23-25 from 3
    for k, b in enumerate(range(23, 26)):
        pos[b] = (2 + 0.15 + 0.95 * k, 2.85)
    # lateral 26-33 from 6
    for k, b in enumerate(range(26, 34)):
        pos[b] = (5 + 0.95 * k, 0.85)

    edges = [
        (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9),
        (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16),
        (16, 17), (17, 18), (2, 19), (19, 20), (20, 21), (21, 22),
        (3, 23), (23, 24), (24, 25), (6, 26), (26, 27), (27, 28), (28, 29),
        (29, 30), (30, 31), (31, 32), (32, 33),
    ]
    bess = {6, 18, 33}
    pv = {7, 24, 31}

    fig, ax = plt.subplots(figsize=(7.2, 2.85))
    for i, j in edges:
        x1, y1 = pos[i]; x2, y2 = pos[j]
        ax.plot([x1, x2], [y1, y2], color="#555", lw=1.05, zorder=1)
    for b, (x, y) in pos.items():
        if b == 1:
            c, m = "#222", "s"
        elif b in bess and b in pv:
            c, m = "#009E73", "D"
        elif b in bess:
            c, m = "#0072B2", "o"
        elif b in pv:
            c, m = "#E69F00", "^"
        else:
            c, m = "#888", "o"
        ax.scatter([x], [y], s=38 if b != 1 else 46, c=c, marker=m, zorder=3, edgecolors="none")
        ax.text(x, y + 0.18, str(b), ha="center", va="bottom", fontsize=6.2, color="#222")
    handles = [
        Line2D([0], [0], marker="s", color="w", markerfacecolor="#222", markersize=7, label="Substation"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#0072B2", markersize=7, label="BESS 0.30/0.40/0.50 MW"),
        Line2D([0], [0], marker="^", color="w", markerfacecolor="#E69F00", markersize=7, label="PV 0.60 MW"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#888", markersize=6, label="Load bus"),
    ]
    ax.legend(handles=handles, loc="upper right", frameon=False, fontsize=7, ncol=2)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(-0.6, 17.6); ax.set_ylim(-0.15, 3.55)
    for sp in ax.spines.values():
        sp.set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "Fig_feeder.png", dpi=300, bbox_inches="tight")
    plt.close()


def fig_results(day="2026-04-08"):
    res = pd.read_csv(STAT / "case_results.csv")
    colors = ["#0072B2", "#E69F00", "#009E73"]
    x = np.arange(len(res))

    fig, ax = plt.subplots(figsize=(3.45, 2.45))
    ax.bar(x, res["profit"], color=colors, width=0.62)
    ax.set_xticks(x); ax.set_xticklabels(res["model"])
    ax.set_ylabel("Realised wholesale profit (EUR)")
    fig.tight_layout(); fig.savefig(FIG / "Fig_profit.png", dpi=300); plt.close()

    fig, ax = plt.subplots(figsize=(3.45, 2.45))
    ax.bar(x - 0.18, res["aging"], 0.36, label="Aging (EUR)", color="#D55E00")
    ax.bar(x + 0.18, res["n_viol"], 0.36, label="Bus-hours $V<0.93$", color="#0072B2")
    ax.set_xticks(x); ax.set_xticklabels(res["model"])
    ax.legend(frameon=False, fontsize=7)
    ax.set_ylabel("EUR  /  count")
    fig.tight_layout(); fig.savefig(FIG / "Fig_aging_volt.png", dpi=300); plt.close()

    p1 = np.load(STAT / f"P1_{day}.npz" if (STAT / f"P1_{day}.npz").exists() else ROOT / f"P1_{day}.npz")
    b2 = np.load(STAT / f"B2_{day}.npz" if (STAT / f"B2_{day}.npz").exists() else ROOT / f"B2_{day}.npz")
    b0 = np.load(STAT / f"B0_{day}.npz" if (STAT / f"B0_{day}.npz").exists() else ROOT / f"B0_{day}.npz")
    fig, ax = plt.subplots(figsize=(3.45, 2.45))
    h = np.arange(24)
    ax.step(h, b0["pda"], where="mid", label="B0", color="#0072B2", lw=1.15)
    ax.step(h, b2["pda"], where="mid", label="B2 / P1", color="#009E73", lw=1.25)
    ax.axhline(0, color="#333", lw=0.6)
    ax.set_xlabel("Hour"); ax.set_ylabel("DA export (MW)")
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout(); fig.savefig(FIG / "Fig_bids.png", dpi=300); plt.close()

    fig, ax = plt.subplots(figsize=(3.45, 2.45))
    ax.plot(h, b2["v"].min(axis=0), label="B2 (no V penalty)", color="#E69F00", ls="--", lw=1.2)
    ax.plot(h, p1["v"].min(axis=0), label="P1 (V slack)", color="#009E73", lw=1.25)
    ax.axhline(0.93, color="#D55E00", lw=0.9, label="0.93 pu floor")
    ax.set_xlabel("Hour"); ax.set_ylabel("Minimum bus voltage (pu)")
    ax.set_ylim(0.86, 1.02)
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout(); fig.savefig(FIG / "Fig_voltage.png", dpi=300); plt.close()


if __name__ == "__main__":
    fig_architecture()
    fig_feeder()
    fig_results()
    print("figures written", list(FIG.iterdir()))
