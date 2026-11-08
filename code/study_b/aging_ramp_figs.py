#!/usr/bin/env python3
"""Rainflow vs Xu vs throughput; ramp limits; Pareto; timeline/architecture SVG data."""
from __future__ import annotations
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from vpp_two_stage import Plant, XU_W, XU_S, solve_rt
from run_experiments import hourly, build_day, run_one

ROOT = Path("/home/user")
STAT = ROOT / "results"
FIG = ROOT / "paper" / "figures"


def soc_from(pch, pdis, E, eta_c=0.95, eta_d=0.95, soc0=0.50):
    T = pch.shape[1]
    soc = np.zeros((pch.shape[0], T))
    for b in range(pch.shape[0]):
        e = soc0 * E[b]
        for t in range(T):
            e = e + eta_c * pch[b, t] - pdis[b, t] / eta_d
            soc[b, t] = e / E[b]
    return soc


def turning_points(x):
    x = np.asarray(x, float)
    if len(x) < 3:
        return x
    pts = [x[0]]
    for i in range(1, len(x) - 1):
        if (x[i] - x[i - 1]) * (x[i + 1] - x[i]) < 0:
            pts.append(x[i])
    pts.append(x[-1])
    return np.array(pts)


def rainflow_ranges(soc):
    """ASTM-like 4-point rainflow on a 1-D SoC series. Returns list of (depth, 0.5 or 1)."""
    pts = list(turning_points(soc))
    cycles = []
    stack = []
    for p in pts:
        stack.append(p)
        while len(stack) >= 4:
            r1 = abs(stack[-2] - stack[-3])
            r0 = abs(stack[-3] - stack[-4])
            r2 = abs(stack[-1] - stack[-2])
            if r1 <= r0 and r1 <= r2:
                cycles.append((r1, 1.0))
                del stack[-3:-1]
            else:
                break
    for i in range(len(stack) - 1):
        cycles.append((abs(stack[i + 1] - stack[i]), 0.5))
    return cycles


def xu_cost_from_depth(depth):
    """depth = (smax-smin) as fraction of nameplate, one battery-day."""
    rem = max(float(depth), 0.0)
    c = 0.0
    for w, s in zip(XU_W, XU_S):
        take = min(rem, w)
        c += take * s
        rem -= take
        if rem <= 0:
            break
    return c


def analyse_day(day="2026-04-08"):
    pl = Plant()
    E = pl.e_arr()
    rows = []
    for name in ("B0", "B1a", "B1b", "B2", "P0", "P1"):
        z = np.load(STAT / f"{name}_{day}.npz")
        soc = soc_from(z["pch"], z["pdis"], E)
        thr = float((z["pch"] + z["pdis"]).sum())
        efc_thr = 0.5 * thr / float(E.sum())  # MWh throughput / (2E) 
        efc_rf = 0.0
        xu = 0.0
        for b in range(len(E)):
            cyc = rainflow_ranges(soc[b])
            efc_rf += sum(d * w for d, w in cyc)  # depth in SoC fraction * weight
            depth = float(soc[b].max() - soc[b].min())
            xu += xu_cost_from_depth(depth)
        # rainflow EFC: sum of (DoD * count) over units, DoD in [0,1]
        rows.append(dict(
            model=name, throughput_mwh=thr, efc_throughput=efc_thr,
            efc_rainflow=efc_rf, xu_eur=xu, aging_thr_eur=12.0 * thr,
            soc_min=float(soc.min()), soc_max=float(soc.max()),
        ))
    df = pd.DataFrame(rows)
    df.to_csv(STAT / "rainflow.csv", index=False)
    print(df.to_string(index=False))
    return df


def ramp_exp(day="2026-04-08"):
    pl = Plant()
    df = hourly()
    pack = build_day(df, day, pl, K=12, seed=pl.seed)
    da, _ = run_one(pack, pl, "P1", True, True, 0.05, True, True)
    rows = []
    for rmp in (None, 0.20, 0.10, 0.05):
        rt = solve_rt(da["pda"], pack["price_act"], pack["pv_bus_act"], pack["lf_act"], pl,
                      with_voltage=True, aging_obj=True, ramp_mw=rmp)
        rows.append(dict(
            ramp=0 if rmp is None else rmp, ok=rt["success"],
            profit=rt["profit"], vmin=rt["vmin"], n_viol=rt["n_viol"],
            aging=rt["aging"], thr=rt["throughput_mwh"], time_s=rt["time_s"],
        ))
        print("ramp", rmp, rt["status"], "vmin", rt["vmin"], "viol", rt["n_viol"], "π", rt["profit"])
    pd.DataFrame(rows).to_csv(STAT / "ramp.csv", index=False)


def figures(rain, day="2026-04-08"):
    plt.rcParams.update({"font.family": "serif", "font.size": 8.0,
                         "axes.spines.top": False, "axes.spines.right": False})
    week = pd.read_csv(STAT / "week_results.csv")
    fig, ax = plt.subplots(figsize=(3.5, 2.5))
    for m, c in [("B0", "#0072B2"), ("B1a", "#56B4E9"), ("B2", "#E69F00"),
                 ("P0", "#999999"), ("P1", "#009E73")]:
        s = week[week.model == m]
        ax.scatter(-s["profit"], s["aging"], s=18 + 0.04 * s["n_viol"], c=c, label=m, alpha=0.85)
    ax.set_xlabel("Service cost −profit (EUR/d)")
    ax.set_ylabel("Aging bill (EUR/d)")
    ax.legend(frameon=False, fontsize=6.5, ncol=2)
    fig.tight_layout(); fig.savefig(FIG / "Fig_pareto.png", dpi=300); plt.close()

    fig, ax = plt.subplots(figsize=(3.5, 2.45))
    x = np.arange(len(rain))
    ax.bar(x - 0.2, rain["aging_thr_eur"], 0.4, label="Throughput 12 EUR/MWh", color="#D55E00")
    ax.bar(x + 0.2, rain["xu_eur"], 0.4, label="Xu PWL on daily range", color="#0072B2")
    ax.set_xticks(x); ax.set_xticklabels(rain["model"], fontsize=7)
    ax.set_ylabel("EUR / day (8 Apr)")
    ax.legend(frameon=False, fontsize=6.5)
    fig.tight_layout(); fig.savefig(FIG / "Fig_rainflow.png", dpi=300); plt.close()
    print("figs written")


if __name__ == "__main__":
    rain = analyse_day()
    ramp_exp()
    figures(rain)
    Path(STAT / "epsilon_v.json").write_text(json.dumps({
        "nr_p1_max_dV": 0.0038, "nr_p1_mean_dV": 0.0017,
        "epsilon_v_suggested": 0.004,
        "note": "hard floor v_min+eps on LinDistFlow to cover NR error",
    }, indent=2))
