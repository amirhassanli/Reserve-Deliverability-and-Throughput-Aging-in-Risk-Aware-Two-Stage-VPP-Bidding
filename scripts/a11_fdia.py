# -*- coding: utf-8 -*-
"""FDIA extension: (a) recall vs stealth radius; (b) NR-based independent measurement test."""
import sys, os, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
WS = r"C:\Users\Mahboobian\Documents\Default Project\_draft\ws_run"
sys.path.insert(0, os.path.join(WS, "src"))
import numpy as np, pandas as pd
from run_experiments import hourly, list_days, build_day, run_one, STAT
from ac_bfs import bfs_voltage, injections_from_rt
from ac_nr import nr_voltage

OUT = os.path.join(WS, "results_ext")
df = hourly(); days = list_days(df); day = "2026-04-08"
pl_current = None
import dataclasses
from vpp_two_stage import Plant
pl = Plant()
pack = build_day(df, day, pl, K=12, seed=pl.seed)
da, rt = run_one(pack, pl, "P1", True, True, 0.05, True, True)
v = rt["v"]
pda = da["pda"]
rng = np.random.default_rng(pl.seed + 7)
sigma = 0.003
buses = np.array([17, 21, 32])

def stealth(m, delta):
    cols = np.any(np.isin(np.arange(m.shape[0]), buses), axis=0)
    for b in buses:
        m[b, :] = m[b, :] + delta
    return m

# clean threshold from LD twin (same as legacy protocol with n_mc=200)
clean_r = [float(np.abs((v + rng.normal(0, sigma, v.shape)) - v).max()) for _ in range(200)]
th_r = float(np.quantile(clean_r, 0.99))
print("theta from LD residual, n_mc=200:", th_r)

rows = []
for delta in (0.002, 0.004, 0.006, 0.008, 0.010, 0.012):
    yt, pr = [], []
    for k in range(200):
        att = bool(k % 2)
        m = v + rng.normal(0, sigma, v.shape)
        if att:
            m = stealth(m, delta)
        yt.append(int(att)); pr.append(int(np.abs(m - v).max() > th_r))
    yt, pr = np.array(yt), np.array(pr)
    tp = int(((yt == 1) & (pr == 1)).sum()); fp = int(((yt == 0) & (pr == 1)).sum())
    fn = int(((yt == 1) & (pr == 0)).sum()); tn = int(((yt == 0) & (pr == 0)).sum())
    rec = tp / max(tp + fn, 1); prec = tp / max(tp + fp, 1)
    fpr = fp / max(fp + tn, 1)
    rows.append(dict(delta_pu=delta, tp=tp, fp=fp, fn=fn, tn=tn, recall=rec, precision=prec, fpr=fpr))
    print(f"delta {delta:.3f}: recall {rec:.2f} prec {prec:.2f} (tp{tp} fp{fp} fn{fn})")
tab = pd.DataFrame(rows)
tab.to_csv(os.path.join(OUT, "e6a_radius_sweep.csv"), index=False)

# ---- (b) NR-based independent test ----
# Build NR voltage trajectory from clean RT (hours), then evaluate detector:
#   threshold still from LD clean draws; test: clean NR measurement draws vs attacked NR measurement draws.
nr_v = np.zeros_like(v)
for t in range(24):
    p, q = injections_from_rt(rt, pack["lf_act"], pack["pv_bus_act"], pl, t)
    vn, conv, it, mis = nr_voltage(p, q)
    nr_v[:, t] = vn
print("LD min v", v.min(), "NR min v", nr_v.min())

rng2 = np.random.default_rng(pl.seed + 77)
rows2 = []
for delta in (0.004, 0.008, 0.012):
    yt, pr = [], []
    for k in range(200):
        att = bool(k % 2)
        m = nr_v + rng2.normal(0, sigma, nr_v.shape)   # measurement on NR model
        if att:
            m = stealth(m, delta)
        # detector compares against LD twin oracle v (as legacy: residual vs v), th from LD clean
        yt.append(int(att)); pr.append(int(np.abs(m - v).max() > th_r))
    yt, pr = np.array(yt), np.array(pr)
    tp = int(((yt == 1) & (pr == 1)).sum()); fp = int(((yt == 0) & (pr == 1)).sum())
    fn = int(((yt == 1) & (pr == 0)).sum()); tn = int(((yt == 0) & (pr == 0)).sum())
    rec = tp / max(tp + fn, 1); fpr = fp / max(fp + tn, 1); prec = tp / max(tp + fp, 1)
    rows2.append(dict(delta_pu=delta, tp=tp, fp=fp, fn=fn, tn=tn, recall=rec, precision=prec, fpr=fpr))
    print(f"NR-test delta {delta:.3f}: recall {rec:.2f} prec {prec:.2f} (tp{tp} fp{fp} fn{fn} tn{tn})")
tab2 = pd.DataFrame(rows2)
tab2.to_csv(os.path.join(OUT, "e6b_nr_mismatch.csv"), index=False)
print("DONE ->", OUT)
