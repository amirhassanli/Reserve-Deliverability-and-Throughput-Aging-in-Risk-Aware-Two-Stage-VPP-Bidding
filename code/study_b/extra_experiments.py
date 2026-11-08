#!/usr/bin/env python3
"""P/Q ablation, Newton–Raphson AC check, multi-attack residual FDIA, extra figures."""
from __future__ import annotations
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from vpp_two_stage import Plant, solve_da, solve_rt
from run_experiments import hourly, build_day, run_one
from ac_bfs import bfs_voltage, injections_from_rt
from ac_nr import nr_voltage

ROOT = Path("/home/user")
FIG = ROOT / "paper" / "figures"
STAT = ROOT / "results"
FIG.mkdir(parents=True, exist_ok=True)


def pq_ablation(df, day, pl):
    pack = build_day(df, day, pl, K=12, seed=pl.seed)
    da, _ = run_one(pack, pl, "P1", True, True, 0.05, True, True)
    rows = []
    for name, volt, ap, aq in [
        ("P-only", True, True, False),
        ("Q-only", True, False, True),
        ("P-Q", True, True, True),
        ("P-Q no V", False, True, True),
    ]:
        rt = solve_rt(da["pda"], pack["price_act"], pack["pv_bus_act"], pack["lf_act"], pl,
                      with_voltage=volt, aging_obj=True, allow_p=ap, allow_q=aq)
        rows.append(dict(
            strategy=name, ok=rt["success"], status=rt["status"], gap=rt["gap"],
            time_s=rt["time_s"], profit=rt["profit"], aging=rt["aging"],
            vmin=rt["vmin"], n_viol=rt["n_viol"], n_viol_095=rt["n_viol_095"],
            v_rms_und=rt["v_rms_und"], q_abs=rt["q_abs_mvarh"],
            throughput=rt["throughput_mwh"], imb=rt["imb"],
        ))
        np.savez(STAT / f"PQ_{name.replace(' ', '_')}_{day}.npz", v=rt["v"], pda=da["pda"])
        print(name, rt["status"], "vmin", rt["vmin"], "viol", rt["n_viol"], "π", rt["profit"])
    pd.DataFrame(rows).to_csv(STAT / "pq_ablation.csv", index=False)
    return pd.DataFrame(rows)


def ac_triple(df, day, pl):
    pack = build_day(df, day, pl, K=12, seed=pl.seed)
    recs = []
    for name, xu, thr, lam, volt, aging in (("B2", True, True, 0.05, False, True),
                                            ("P1", True, True, 0.05, True, True),
                                            ("P0", False, False, 0.0, True, False)):
        da, rt = run_one(pack, pl, name, xu, thr, lam, volt, aging)
        e_bfs, e_nr, nrc = [], [], []
        ac_min_bfs, ac_min_nr, ld_min = [], [], []
        for t in range(24):
            p, q = injections_from_rt(rt, pack["lf_act"], pack["pv_bus_act"], pl, t)
            vb = bfs_voltage(p, q)
            vn, conv, it, mis = nr_voltage(p, q)
            vld = rt["v"][:, t]
            e_bfs.append(np.abs(vb - vld))
            e_nr.append(np.abs(vn - vld))
            nrc.append(int(conv))
            ac_min_bfs.append(float(vb.min()))
            ac_min_nr.append(float(vn.min()))
            ld_min.append(float(vld.min()))
        e_bfs, e_nr = np.stack(e_bfs), np.stack(e_nr)
        recs.append(dict(
            model=name,
            ld_vmin=float(min(ld_min)),
            bfs_vmin=float(min(ac_min_bfs)),
            nr_vmin=float(min(ac_min_nr)),
            bfs_mean=float(e_bfs.mean()), bfs_max=float(e_bfs.max()),
            nr_mean=float(e_nr.mean()), nr_max=float(e_nr.max()),
            nr_p95=float(np.quantile(e_nr, 0.95)),
            nr_conv_hours=int(sum(nrc)),
        ))
        print(name, recs[-1])
    pd.DataFrame(recs).to_csv(STAT / "ac_triple.csv", index=False)
    return pd.DataFrame(recs)


def fdia_suite(df, day, pl, n_mc=120):
    """Six attack tapes vs residual and z-score. Not an autoencoder."""
    pack = build_day(df, day, pl, K=12, seed=pl.seed)
    da, rt = run_one(pack, pl, "P1", True, True, 0.05, True, True)
    v = rt["v"]
    pda = da["pda"]
    rng = np.random.default_rng(pl.seed + 7)
    sigma = 0.003
    buses = np.array([17, 21, 32])

    def max_resid(meas):
        return float(np.abs(meas - v).max())

    def max_z(meas):
        # z vs clean mean=v, sigma known
        return float(np.abs((meas - v) / sigma).max())

    clean_r, clean_z = [], []
    for _ in range(n_mc):
        m = v + rng.normal(0, sigma, v.shape)
        clean_r.append(max_resid(m))
        clean_z.append(max_z(m))
    th_r = float(np.quantile(clean_r, 0.99))
    th_z = float(np.quantile(clean_z, 0.99))

    def score(make_attack):
        yt, pr, pz = [], [], []
        for k in range(n_mc):
            att = bool(k % 2)
            m = v + rng.normal(0, sigma, v.shape)
            if att:
                m = make_attack(m)
            yt.append(int(att))
            pr.append(int(max_resid(m) > th_r))
            pz.append(int(max_z(m) > th_z))
        yt = np.array(yt)

        def prf(pred):
            pred = np.array(pred)
            tp = int(((yt == 1) & (pred == 1)).sum())
            fp = int(((yt == 0) & (pred == 1)).sum())
            fn = int(((yt == 1) & (pred == 0)).sum())
            tn = int(((yt == 0) & (pred == 0)).sum())
            prec = tp / max(tp + fp, 1)
            rec = tp / max(tp + fn, 1)
            f1 = 2 * prec * rec / max(prec + rec, 1e-12)
            far = fp / max(fp + tn, 1)
            return dict(tp=tp, fp=fp, fn=fn, tn=tn, precision=prec, recall=rec, f1=f1, far=far)
        return dict(residual=prf(pr), zscore=prf(pz))

    attacks = {
        "V_bias": lambda m: (m.__setitem__((buses, slice(None)), m[buses] + 0.05) or m),
        "V_ramp": lambda m: m + np.linspace(0, 0.04, 24)[None, :],
        "V_stealth": lambda m: (m.__setitem__((buses, slice(None)), m[buses] + 0.008) or m),
        "V_coord": lambda m: (m.__setitem__((np.array([5, 17, 32]), slice(None)),
                                            m[np.array([5, 17, 32])] + 0.04) or m),
    }
    # fix lambdas that mutate: make copies
    def V_bias(m):
        m = m.copy(); m[buses] += 0.05; return m
    def V_ramp(m):
        m = m.copy(); m += np.linspace(0, 0.04, 24); return m
    def V_stealth(m):
        m = m.copy(); m[buses] += 0.008; return m
    def V_coord(m):
        m = m.copy(); m[[5, 17, 32]] += 0.04; return m

    out = dict(theta_residual=th_r, theta_zscore=th_z, sigma=sigma, n_mc=n_mc, attacks={})
    for nm, fn in [("V_bias", V_bias), ("V_ramp", V_ramp), ("V_stealth", V_stealth), ("V_coord", V_coord)]:
        out["attacks"][nm] = score(fn)
        print(nm, out["attacks"][nm])

    # bid / price attacks: economic, not voltage detector
    econ = {}
    rt0 = rt
    for lab, pda2, dlam in [
        ("bid_bias", pda + 0.40, 0.0),
        ("price_bias", pda, 25.0),
    ]:
        price = pack["price_act"] + dlam
        rt_a = solve_rt(pda2, price, pack["pv_bus_act"], pack["lf_act"], pl,
                        with_voltage=True, aging_obj=True)
        econ[lab] = dict(clean=rt0["profit"], attacked=rt_a["profit"],
                         dprofit=rt_a["profit"] - rt0["profit"],
                         vmin_att=rt_a["vmin"], viol_att=rt_a["n_viol"], ok=rt_a["success"])
        print(lab, econ[lab])
    out["economic"] = econ
    Path(STAT / "fdia_suite.json").write_text(json.dumps(out, indent=2))
    return out


def extra_figures(day="2026-04-08"):
    plt.rcParams.update({"font.family": "serif", "font.size": 8.0,
                         "axes.spines.top": False, "axes.spines.right": False})
    p1 = np.load(STAT / f"P1_{day}.npz")
    b2 = np.load(STAT / f"B2_{day}.npz")

    # heatmap
    fig, ax = plt.subplots(1, 2, figsize=(7.1, 2.7), sharey=True)
    for a, (lab, arr, vmin) in zip(ax, [("B2", b2["v"], 0.87), ("P1", p1["v"], 0.87)]):
        im = a.imshow(arr, aspect="auto", origin="lower", cmap="magma", vmin=0.87, vmax=1.02)
        a.axhline(-0.5, color="none")
        a.set_xlabel("Hour"); a.set_title(lab, fontsize=9)
        a.set_ylabel("Bus" if a is ax[0] else "")
    fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02, label="|V| (pu)")
    fig.tight_layout(); fig.savefig(FIG / "Fig_heatmap.png", dpi=300); plt.close()

    # all-bus voltage at worst B2 hour
    tstar = int(np.argmin(b2["v"].min(axis=0)))
    fig, ax = plt.subplots(figsize=(3.5, 2.45))
    buses = np.arange(1, 34)
    ax.plot(buses, b2["v"][:, tstar], color="#E69F00", lw=1.1, label=f"B2 h={tstar}")
    ax.plot(buses, p1["v"][:, tstar], color="#009E73", lw=1.1, label=f"P1 h={tstar}")
    ax.axhline(0.93, color="#D55E00", lw=0.8, label="0.93 pu")
    ax.axhline(0.95, color="#D55E00", lw=0.6, ls=":", label="0.95 pu")
    ax.set_xlabel("Bus"); ax.set_ylabel("Voltage (pu)")
    ax.legend(frameon=False, fontsize=6.5, ncol=2)
    fig.tight_layout(); fig.savefig(FIG / "Fig_busvolt.png", dpi=300); plt.close()

    # degradation cumulative
    fig, ax = plt.subplots(figsize=(3.5, 2.45))
    for lab, fn, c in [("B0", f"B0_{day}.npz", "#0072B2"),
                       ("B2", f"B2_{day}.npz", "#E69F00"),
                       ("P1", f"P1_{day}.npz", "#009E73")]:
        z = np.load(STAT / fn)
        thr = (z["pch"] + z["pdis"]).sum(axis=0)
        ax.plot(np.cumsum(thr), label=lab, color=c, lw=1.2)
    ax.set_xlabel("Hour"); ax.set_ylabel("Cumulative throughput (MWh)")
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout(); fig.savefig(FIG / "Fig_throughput.png", dpi=300); plt.close()

    # PQ bars
    pq = pd.read_csv(STAT / "pq_ablation.csv")
    fig, ax = plt.subplots(figsize=(3.5, 2.45))
    x = np.arange(len(pq))
    ax.bar(x - 0.18, pq["vmin"], 0.36, color="#009E73", label=r"$v_{\min}$")
    ax.bar(x + 0.18, pq["n_viol"] / max(pq["n_viol"].max(), 1), 0.36, color="#0072B2", label="viol (scaled)")
    ax.set_xticks(x); ax.set_xticklabels(pq["strategy"], fontsize=7)
    ax.axhline(0.93, color="#D55E00", lw=0.7)
    ax.legend(frameon=False, fontsize=7)
    ax.set_ylabel("pu  /  scaled count")
    fig.tight_layout(); fig.savefig(FIG / "Fig_pq.png", dpi=300); plt.close()
    print("extra figures ok")


if __name__ == "__main__":
    pl = Plant()
    df = hourly()
    day = "2026-04-08"
    pq_ablation(df, day, pl)
    ac_triple(df, day, pl)
    fdia_suite(df, day, pl)
    extra_figures(day)
