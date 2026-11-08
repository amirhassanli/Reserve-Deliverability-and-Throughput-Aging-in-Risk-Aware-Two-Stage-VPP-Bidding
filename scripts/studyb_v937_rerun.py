# -*- coding: utf-8 -*-
"""PHASE14 computations:
(a) P0-6: re-run 7-day B2/P1 week at LD floor v_min=0.937 + NR verification per day
(b) P0-4b: charge/discharge overlap from existing npz (Study B)
(c) N1: PV absorption reconciliation (23.5 MWh vs 3.5 MWh) from e5 diag + npz
Outputs -> _draft/results_v937/ and _draft/results_check/
"""
import sys, os, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np, pandas as pd

WS = r"C:\Users\Mahboobian\Documents\Default Project\_draft\ws_run"
sys.path.insert(0, os.path.join(WS, "src"))
from ieee33 import peak_load_mw, pu_branch, SBASE_MVA
from vpp_two_stage import Plant, solve_da, solve_rt
from ac_nr import nr_voltage
import ac_bfs
import ieee33
import inspect

OUT = r"C:\Users\Mahboobian\Documents\Default Project\_draft\results_v937"
CHK = r"C:\Users\Mahboobian\Documents\Default Project\_draft\results_check"
os.makedirs(OUT, exist_ok=True); os.makedirs(CHK, exist_ok=True)

# ---------- (a) week at 0.937 ----------
from run_experiments import hourly, list_days, build_day, MODELS, run_one, row_from

df = hourly()
days = list_days(df)
print("days:", days)

pl937 = Plant(v_min=0.937)
rows = []
for day in days:
    pack = build_day(df, day, pl937, K=12, seed=20260827)
    for name, xu, thr, lam, volt, aging_obj in MODELS:
        da, rt = run_one(pack, pl937, name, xu, thr, lam, volt, aging_obj)
        rows.append(row_from(name, da, rt, day, 20260827))
        print(f"937 {day} {name} ok={rt['success']} pi={rt['profit']:.2f} vmin={rt['vmin']:.4f} viol={rt['n_viol']}")
    # NR check for P1 and B2 on this day
    for name, xu, thr, lam, volt, aging_obj in (("B2", True, True, 0.05, False, True),
                                                ("P1", True, True, 0.05, True, True)):
        da, rt = run_one(pack, pl937, name, xu, thr, lam, volt, aging_obj)
        errs, amins, lmins = [], [], []
        for t in range(24):
            p, q = ac_bfs.injections_from_rt(rt, pack["lf_act"], pack["pv_bus_act"], pl937, t)
            vac, conv, it, mis = nr_voltage(p, q)
            amins.append(float(np.min(vac)))
            lmins.append(float(np.min(rt["v"][:, t])))
            errs.append(np.abs(vac - rt["v"][:, t]).max())
        print(f"   NR937 {day} {name} LDmin={min(lmins):.4f} NRmin={min(amins):.4f} maxerr={max(errs):.4f} conv={conv}")

w = pd.DataFrame(rows)
w.to_csv(os.path.join(OUT, "week_v937.csv"), index=False)

g = w.groupby("model")[["profit", "n_viol", "vmin", "aging"]].agg(["mean", "std"])
print("\nv937 weekly means:")
print(g)

# compare vs existing 0.93 baseline
base = pd.read_csv(os.path.join(WS, "results", "week_results.csv"))
gb = base.groupby("model")[["profit", "n_viol", "vmin", "aging"]].mean()
print("\nbaseline 0.93 means:")
print(gb)

# ---------- (b) charge/discharge overlap from npz ----------
recs = []
for fn in sorted(os.listdir(os.path.join(WS, "results"))):
    if fn.endswith(".npz"):
        z = np.load(os.path.join(WS, "results", fn))
        if "pch" in z and "pdis" in z:
            pch, pdis = z["pch"], z["pdis"]  # (units, T)
            ov = np.minimum(pch, pdis)
            recs.append(dict(
                file=fn, shape=str(pch.shape),
                total_overlap_mwh=float(ov.sum()),
                max_hour_overlap_mw=float(ov.sum(axis=0).max()) if ov.ndim == 2 else None,
                overlap_hours=int((ov.sum(axis=0) if ov.ndim == 2 else ov > 0).sum()) if ov.ndim==2 else int((ov>0).sum()),
                total_ch=float(pch.sum()), total_dis=float(pdis.sum())))
pd.DataFrame(recs).to_csv(os.path.join(CHK, "studyb_overlap.csv"), index=False)
for r in recs: print("OVERLAP", r)

# ---------- (c) N1 PV absorption ----------
e5 = os.path.join(WS, "results_ext", "e5_f11_diag.csv")
if os.path.exists(e5):
    d5 = pd.read_csv(e5)
    print("\ne5_f11_diag cols:", list(d5.columns))
    print(d5.head(20).to_string())
