# -*- coding: utf-8 -*-
"""PHASE11 extension experiments (Study B re-execution): multi-day NR, cdeg sweep, alpha/K, polygon envelope, viol diagnosis."""
import sys, os, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
WS = r"C:\Users\Mahboobian\Documents\Default Project\_draft\ws_run"
sys.path.insert(0, os.path.join(WS, "src"))
import numpy as np, pandas as pd
from run_experiments import hourly, list_days, build_day, run_one, MODELS, row_from, STAT
from vpp_two_stage import Plant, solve_da, solve_rt
from ac_bfs import bfs_voltage, injections_from_rt
from ac_nr import nr_voltage
import dataclasses, time

OUT = os.path.join(WS, "results_ext")
os.makedirs(OUT, exist_ok=True)
df = hourly()
days = list_days(df)
print("days:", days)
pl0 = Plant()

SKIP = set(sys.argv[1:])
# ---------------- E1: NR validation on all 7 days ----------------
t0 = time.time()
rows = []
for day in days:
    pack = build_day(df, day, pl0, K=12, seed=pl0.seed)
    for name, xu, thr, lam, volt, ag in (("B2", True, True, 0.05, False, True),
                                          ("P1", True, True, 0.05, True, True)):
        da, rt = run_one(pack, pl0, name, xu, thr, lam, volt, ag)
        nrmins = []
        ld_v = rt["v"]
        e_nr_all = []
        for t in range(24):
            p, q = injections_from_rt(rt, pack["lf_act"], pack["pv_bus_act"], pl0, t)
            vn, conv, it, mis = nr_voltage(p, q)
            e_nr_all.append(np.abs(vn - ld_v[:, t]))
            nrmins.append(float(vn.min()))
        e = np.stack(e_nr_all)
        rows.append(dict(day=day, model=name, ld_vmin=float(ld_v.min()),
                         nr_vmin=float(min(nrmins)),
                         nr_nviol=int(np.sum(np.array(nrmins) < 0.93 - 1e-4)),
                         nr_hours=int(np.sum(np.array(nrmins) < 0.93 - 1e-4)),
                         nr_mean_err=float(e.mean()), nr_max_err=float(e.max()),
                         nr_p95_err=float(np.quantile(e, 0.95)),
                         ld_noV=not volt))
tab = pd.DataFrame(rows)
tab.to_csv(os.path.join(OUT, "e1_nr_multiday.csv"), index=False)
print("E1 NR multiday:\n", tab.to_string(index=False), f"[{time.time()-t0:.1f}s]")

# ---------------- E2: cdeg sweep (feeder week) ----------------
rows = []
for cd in (3.0, 6.0, 9.0, 12.0, 15.0, 20.0):
    pl = dataclasses.replace(pl0, c_deg=cd)
    pack_by_day = {}
    agg = {}
    for day in days:
        pack = build_day(df, day, pl, K=12, seed=pl0.seed)
        for name, xu, thr, lam, volt, ag in (("B0", False, False, 0.0, False, False),
                                              ("B2", True, True, 0.05, False, True),
                                              ("P1", True, True, 0.05, True, True)):
            da, rt = run_one(pack, pl, name, xu, thr, lam, volt, ag)
            d = agg.setdefault(name, dict(profit=[], viol=[], thr=[], aging=[]))
            d["profit"].append(rt["profit"]); d["viol"].append(rt["n_viol"])
            d["thr"].append(rt["throughput_mwh"]); d["aging"].append(rt["aging"])
    for name, d in agg.items():
        rows.append(dict(cdeg=cd, model=name,
                         profit_mean=float(np.mean(d["profit"])),
                         viol_mean=float(np.mean(d["viol"])),
                         thr_mean=float(np.mean(d["thr"])),
                         aging_mean=float(np.mean(d["aging"]))))
    b0 = [r for r in rows if r["cdeg"] == cd and r["model"] == "B0"][0]
    b2 = [r for r in rows if r["cdeg"] == cd and r["model"] == "B2"][0]
    p1 = [r for r in rows if r["cdeg"] == cd and r["model"] == "P1"][0]
    rows.append(dict(cdeg=cd, model="B2-B0",
                     profit_mean=b2["profit_mean"] - b0["profit_mean"],
                     viol_mean=b2["viol_mean"] - b0["viol_mean"], thr_mean=np.nan, aging_mean=np.nan))
    rows.append(dict(cdeg=cd, model="P1-B0",
                     profit_mean=p1["profit_mean"] - b0["profit_mean"],
                     viol_mean=p1["viol_mean"] - b0["viol_mean"], thr_mean=np.nan, aging_mean=np.nan))
    print(f"cdeg {cd}: B2-B0 {b2['profit_mean']-b0['profit_mean']:.1f} | P1-B0 {p1['profit_mean']-b0['profit_mean']:.1f} | P1 thr {p1['thr_mean']:.2f} | mu viol {p1['viol_mean']:.1f}")
tab = pd.DataFrame(rows)
tab.to_csv(os.path.join(OUT, "e2_cdeg_sweep.csv"), index=False)

# ---------------- E3: alpha/K recalibration ----------------
rows = []
for alpha in (0.80, 0.90, 0.95):
    for K in (12, 100):
        pl = dataclasses.replace(pl0, alpha=alpha)
        agg = {}
        for day in days:
            pack = build_day(df, day, pl0, K=K, seed=pl0.seed)
            for name, xu, thr, lam, volt, ag in (("B2", True, True, 0.05, False, True),
                                                  ("P1", True, True, 0.05, True, True)):
                da = solve_da(pack["price"], pack["pv"], pack["lf"], pl, K=K, use_xu=xu, use_thr=thr, lam=lam)
                rt = solve_rt(da["pda"], pack["price_act"], pack["pv_bus_act"], pack["lf_act"], pl,
                              with_voltage=volt, aging_obj=ag)
                d = agg.setdefault(name, {"profit": [], "viol": []})
                d["profit"].append(rt["profit"]); d["viol"].append(rt["n_viol"])
                da_ok = da["success"]
        for name, d in agg.items():
            tail = (1.0 - alpha) * K
            rows.append(dict(alpha=alpha, K=K, expected_tail=tail, model=name,
                             profit_mean=float(np.mean(d["profit"])),
                             viol_mean=float(np.mean(d["viol"]))))
            print(f"E3 alpha={alpha} K={K} tail={tail:.2f} {name}: profit {np.mean(d['profit']):.1f} viol {np.mean(d['viol']):.1f}")
tab = pd.DataFrame(rows)
tab.to_csv(os.path.join(OUT, "e3_alpha_K.csv"), index=False)

# ---------------- E4: circular-envelope (inner octagon) emulation ----------------
# Replace diamond |p|+|q|<=head*pmax with inscribed octagon: cos(th)|p| + sin(th)|q| <= R*cos(pi/16), th in {22.5,67.5,0,90}
def solve_rt_poly(pda, price, pv_bus_mw, load_fac, pl, aging_obj=True):
    src = open(os.path.join(WS, "src", "vpp_two_stage.py"), encoding="utf-8").read()
    # monkey approach: temporary module copy with constraint replaced
    import types, importlib
    code = src.replace(
        "lp.le([(ix(pch, b, t, T), 1.0), (ix(pdis, b, t, T), 1.0),\n"
        "                   (ix(qbp, b, t, T), 1.0), (ix(qbn, b, t, T), 1.0)], pl.inv_head * pmax[b])",
        "Rn = pl.inv_head * pmax[b] * 0.995184726672197\n"
        "            lp.le([(ix(pch, b, t, T), 0.99518472667), (ix(pdis, b, t, T), 0.99518472667),\n"
        "                   (ix(qbp, b, t, T), 0.09801714033), (ix(qbn, b, t, T), 0.09801714033)], Rn)\n"
        "            lp.le([(ix(pch, b, t, T), 0.09801714033), (ix(pdis, b, t, T), 0.09801714033),\n"
        "                   (ix(qbp, b, t, T), 0.99518472667), (ix(qbn, b, t, T), 0.99518472667)], Rn)\n"
        "            lp.le([(ix(pch, b, t, T), 0.70710678118), (ix(pdis, b, t, T), 0.70710678118),\n"
        "                   (ix(qbp, b, t, T), 0.70710678118), (ix(qbn, b, t, T), 0.70710678118)], Rn)")
    p = os.path.join(WS, "src", "_vpp_poly_mod.py")
    open(p, "w", encoding="utf-8").write(code)
    spec = importlib.util.spec_from_file_location("_vpp_poly_mod", p)
    m = importlib.util.module_from_spec(spec)
    sys.modules["_vpp_poly_mod"] = m
    spec.loader.exec_module(m)
    return m.solve_rt(pda, price, pv_bus_mw, load_fac, pl, with_voltage=True, aging_obj=aging_obj)

rows = []
for day in days:
    pack = build_day(df, day, pl0, K=12, seed=pl0.seed)
    for name, xu, thr, lam, volt, ag in (("P1-diamond", True, True, 0.05, True, True),):
        da, rt = run_one(pack, pl0, name, xu, thr, lam, volt, ag)
        rt2 = solve_rt_poly(da["pda"], pack["price_act"], pack["pv_bus_act"], pack["lf_act"], pl0, aging_obj=ag)
        rows.append(dict(day=day, variant="diamond", profit=rt["profit"], vmin=rt["vmin"],
                         viol=rt["n_viol"], thr=rt["throughput_mwh"], q_abs=rt["q_abs_mvarh"]))
        rows.append(dict(day=day, variant="octagon", profit=rt2["profit"], vmin=rt2["vmin"],
                         viol=rt2["n_viol"], thr=rt2["throughput_mwh"], q_abs=rt2["q_abs_mvarh"]))
        print(f"E4 {day}: diamond prof {rt['profit']:.1f}/q {rt['q_abs_mvarh']:.2f} -> octagon prof {rt2['profit']:.1f}/q {rt2['q_abs_mvarh']:.2f}")
tab = pd.DataFrame(rows)
tab.to_csv(os.path.join(OUT, "e4_polygon.csv"), index=False)

# ---------------- E5: violation diagnosis B1b vs B2 per day ----------------
rows = []
for day in days:
    pack = build_day(df, day, pl0, K=12, seed=pl0.seed)
    d = {}
    for name, xu, thr, lam, volt, ag in (("B0", False, False, 0.0, False, False),
                                          ("B1b", False, False, 0.05, False, False),
                                          ("B2", True, True, 0.05, False, True)):
        da, rt = run_one(pack, pl0, name, xu, thr, lam, volt, ag)
        d[name] = dict(profit=rt["profit"], viol=rt["n_viol"], thr=rt["throughput_mwh"],
                       export=rt["export"], imb=rt["imb"], aging=rt["aging"],
                       n_episodes=rt["n_episode"], max_ep=rt["max_episode_h"])
        rows.append(dict(day=day, model=name, profit=rt["profit"], viol=rt["n_viol"],
                         thr=rt["throughput_mwh"], n_episodes=rt["n_episode"],
                         max_ep=rt["max_episode_h"]))
    dv = d["B2"]["viol"] - d["B1b"]["viol"]
    dthr = d["B2"]["thr"] - d["B1b"]["thr"]
    print(f"E5 {day}: B1b viol {d['B1b']['viol']}, B2 viol {d['B2']['viol']} (Δ{dv:+d}), thr Δ{dthr:+.2f}")
tab = pd.DataFrame(rows)
tab.to_csv(os.path.join(OUT, "e5_f11_diag.csv"), index=False)
print("ALL EXT DONE ->", OUT)
