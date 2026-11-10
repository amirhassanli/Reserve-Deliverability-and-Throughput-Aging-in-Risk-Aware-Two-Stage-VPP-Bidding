#!/usr/bin/env python3
"""Run B0 / B2 / P1 on one SMARD week day (IEEE 33-bus)."""
from __future__ import annotations
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ieee33 import peak_load_mw
from vpp_two_stage import Plant, solve_da, solve_rt

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "paper" / "figures"
STAT = ROOT / "results/study_b" if (ROOT / "results/study_b").exists() else ROOT / "results"
FIG.mkdir(parents=True, exist_ok=True)
STAT.mkdir(parents=True, exist_ok=True)


def hourly():
    da_path = ROOT / "data/raw/smard_da_week.csv"
    if not da_path.exists(): da_path = ROOT / "data/study_b/smard_da_week.csv" if (ROOT / "data/study_b/smard_da_week.csv").exists() else ROOT / "smard_da_week.csv"
    pr = pd.read_csv(da_path, parse_dates=["timestamp"])
    pw_path = ROOT / "data/raw/smard_power_week.csv"
    if not pw_path.exists(): pw_path = ROOT / "data/study_b/smard_power_week.csv" if (ROOT / "data/study_b/smard_power_week.csv").exists() else ROOT / "smard_power_week.csv"
    pw = pd.read_csv(pw_path, parse_dates=["timestamp"])
    pr["timestamp"] = pd.to_datetime(pr["timestamp"], utc=True).dt.tz_convert("Europe/Berlin")
    pw["timestamp"] = pd.to_datetime(pw["timestamp"], utc=True).dt.tz_convert("Europe/Berlin")
    pr = pr.set_index("timestamp")["da_price"].resample("h").mean()
    pw = pw.set_index("timestamp").resample("h").mean()
    df = pd.DataFrame({"da": pr, "solar": pw["Solar"], "load": pw["Load"],
                       "wind": pw["Wind onshore"] + pw["Wind offshore"]})
    return df.dropna()


def build_day(df, day, pl: Plant, K=12):
    sub = df[df.index.strftime("%Y-%m-%d") == day].iloc[:24]
    if len(sub) < 24:
        raise ValueError(day)
    rng = np.random.default_rng(pl.seed + int(day.replace("-", "")))
    price_act = sub["da"].values.astype(float)
    sol_n = float(np.nanmax(df["solar"]))
    load_n = float(np.nanquantile(df["load"], 0.95))
    pv_shape = np.clip(sub["solar"].values / max(sol_n, 1.0), 0, 1)
    load_shape = np.clip(sub["load"].values / max(load_n, 1.0), 0.35, 1.15)
    # scenarios: multiplicative noise
    price = np.zeros((K, 24))
    pv_tot = np.zeros((K, 24))
    lf = np.zeros((K, 24))
    for k in range(K):
        price[k] = price_act + rng.normal(0, 12.0, 24)
        pv_tot[k] = pl.p_pv * len(pl.pv_bus) * np.clip(pv_shape * rng.uniform(0.75, 1.15), 0, 1.05)
        lf[k] = np.clip(load_shape * rng.uniform(0.90, 1.08), 0.35, 1.20)
    pv_bus_act = {b: pl.p_pv * pv_shape for b in pl.pv_bus}
    return dict(price=price, pv=pv_tot, lf=lf, price_act=price_act,
                lf_act=load_shape, pv_bus_act=pv_bus_act, pv_shape=pv_shape)


def run_day(day="2026-04-08"):
    pl = Plant()
    df = hourly()
    pack = build_day(df, day, pl, K=12)
    rows = []
    configs = [
        ("B0", False, 0.0, False),
        ("B2", True, 0.05, False),
        ("P1", True, 0.05, True),
    ]
    for name, xu, lam, volt in configs:
        da = solve_da(pack["price"], pack["pv"], pack["lf"], pl, K=12, use_xu=xu, lam=lam)
        print(name, "DA", da["status"], "pda_sum", da["pda"].sum())
        rt = solve_rt(da["pda"], pack["price_act"], pack["pv_bus_act"], pack["lf_act"], pl, with_voltage=volt)
        print("  RT", rt["status"], "profit", rt["profit"], "vmin", rt["vmin"], "viol", rt["n_viol"],
              "aging", rt["aging"])
        rows.append(dict(
            model=name, da_ok=da["success"], rt_ok=rt["success"],
            pda_mwh=float(da["pda"].sum()),
            da_rev=rt["da_rev"], imb=rt["imb"], aging=rt["aging"],
            profit=rt["profit"], vmin=rt["vmin"], vmax=rt["vmax"],
            n_viol=rt["n_viol"], throughput=rt["throughput_mwh"],
            day=day,
        ))
        np.savez(STAT / f"{name}_{day}.npz", pda=da["pda"], v=rt["v"], export=rt["export"],
                 price=pack["price_act"])
    pd.DataFrame(rows).to_csv(STAT / "case_results.csv", index=False)
    return rows, pack


def figures(day="2026-04-08"):
    plt.rcParams.update({"font.family": "serif", "font.size": 8.5, "axes.spines.top": False,
                         "axes.spines.right": False})
    res = pd.read_csv(STAT / "case_results.csv")
    fig, ax = plt.subplots(figsize=(3.4, 2.4))
    x = np.arange(len(res))
    ax.bar(x, res["profit"], color=["#0072B2", "#E69F00", "#009E73"])
    ax.set_xticks(x); ax.set_xticklabels(res["model"])
    ax.set_ylabel("Realised wholesale profit (EUR)")
    fig.tight_layout(); fig.savefig(FIG / "Fig_profit.png", dpi=300); plt.close()

    fig, ax = plt.subplots(figsize=(3.4, 2.4))
    ax.bar(x - 0.18, res["aging"], 0.36, label="Aging", color="#D55E00")
    ax.bar(x + 0.18, res["n_viol"], 0.36, label="Voltage violations (bus-h)", color="#0072B2")
    ax.set_xticks(x); ax.set_xticklabels(res["model"])
    ax.legend(frameon=False, fontsize=7)
    ax.set_ylabel("EUR  /  count")
    fig.tight_layout(); fig.savefig(FIG / "Fig_aging_volt.png", dpi=300); plt.close()

    p1 = np.load(STAT / f"P1_{day}.npz" if (STAT / f"P1_{day}.npz").exists() else ROOT / f"P1_{day}.npz")
    b2 = np.load(STAT / f"B2_{day}.npz" if (STAT / f"B2_{day}.npz").exists() else ROOT / f"B2_{day}.npz")
    fig, ax = plt.subplots(figsize=(3.4, 2.4))
    h = np.arange(24)
    ax.plot(h, b2["pda"], label="B2 bid", color="#E69F00")
    ax.plot(h, p1["pda"], label="P1 bid", color="#009E73")
    ax.axhline(0, color="#333", lw=0.6)
    ax.set_xlabel("Hour"); ax.set_ylabel("DA export (MW)")
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout(); fig.savefig(FIG / "Fig_bids.png", dpi=300); plt.close()

    fig, ax = plt.subplots(figsize=(3.4, 2.4))
    ax.plot(p1["v"].min(axis=0), label="P1 min V", color="#009E73")
    ax.plot(b2["v"].min(axis=0), label="B2 min V (unchecked)", color="#E69F00", ls="--")
    ax.axhline(0.95, color="#D55E00", lw=0.8)
    ax.set_xlabel("Hour"); ax.set_ylabel("Minimum bus voltage (pu)")
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout(); fig.savefig(FIG / "Fig_voltage.png", dpi=300); plt.close()
    print("figures written")


if __name__ == "__main__":
    rows, _ = run_day("2026-04-08")
    print(pd.DataFrame(rows))
    figures("2026-04-08")
