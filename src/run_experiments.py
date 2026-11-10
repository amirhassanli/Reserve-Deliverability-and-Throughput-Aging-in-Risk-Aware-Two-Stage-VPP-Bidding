#!/usr/bin/env python3
"""Full ablation, week roll, sensitivity, AC check, residual FDIA. HiGHS only."""
from __future__ import annotations
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ieee33 import peak_load_mw, pu_branch, SBASE_MVA
from vpp_two_stage import Plant, solve_da, solve_rt
from ac_bfs import bfs_voltage, injections_from_rt

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "paper" / "figures"
STAT = ROOT / "results/study_b" if (ROOT / "results/study_b").exists() else ROOT / "results"
FIG.mkdir(parents=True, exist_ok=True)
STAT.mkdir(parents=True, exist_ok=True)

MODELS = [
    # name, xu, thr, lam, voltage, aging_obj
    ("B0",  False, False, 0.00, False, False),
    ("B1a", True,  True,  0.00, False, True),
    ("B1b", False, False, 0.05, False, False),
    ("B2",  True,  True,  0.05, False, True),
    ("P0",  False, False, 0.00, True,  False),
    ("P1",  True,  True,  0.05, True,  True),
]
COLORS = {"B0": "#0072B2", "B1a": "#56B4E9", "B1b": "#CC79A7",
          "B2": "#E69F00", "P0": "#999999", "P1": "#009E73"}


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


def list_days(df):
    days = sorted(set(df.index.strftime("%Y-%m-%d")))
    out = []
    for d in days:
        if len(df[df.index.strftime("%Y-%m-%d") == d]) >= 24:
            out.append(d)
    return out


def build_day(df, day, pl: Plant, K=12, seed=None):
    sub = df[df.index.strftime("%Y-%m-%d") == day].iloc[:24]
    if len(sub) < 24:
        raise ValueError(day)
    sd = pl.seed if seed is None else seed
    rng = np.random.default_rng(sd + int(day.replace("-", "")))
    price_act = sub["da"].values.astype(float)
    sol_n = float(np.nanmax(df["solar"]))
    load_n = float(np.nanquantile(df["load"], 0.95))
    pv_shape = np.clip(sub["solar"].values / max(sol_n, 1.0), 0, 1)
    load_shape = np.clip(sub["load"].values / max(load_n, 1.0), 0.35, 1.15)
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


def row_from(name, da, rt, day, seed):
    return dict(
        model=name, day=day, seed=seed,
        da_ok=da["success"], rt_ok=rt["success"],
        da_status=da["status"], rt_status=rt["status"],
        da_gap=da["gap"], rt_gap=rt["gap"],
        da_time_s=da["time_s"], rt_time_s=rt["time_s"],
        time_s=da["time_s"] + rt["time_s"],
        pda_mwh=float(da["pda"].sum()),
        da_rev=rt["da_rev"], imb=rt["imb"], aging=rt["aging"],
        profit=rt["profit"], vmin=rt["vmin"], vmax=rt["vmax"],
        n_viol=rt["n_viol"], n_viol_095=rt["n_viol_095"],
        v_rms_und=rt["v_rms_und"], v_max_und=rt["v_max_und"],
        n_hour_viol=rt["n_hour_viol"], n_episode=rt["n_episode"],
        max_episode_h=rt["max_episode_h"], mean_episode_h=rt["mean_episode_h"],
        s_max_mva=rt["s_max_mva"], n_line_viol=rt["n_line_viol"],
        q_abs_mvarh=rt["q_abs_mvarh"], throughput=rt["throughput_mwh"],
    )


def run_one(pack, pl, name, xu, thr, lam, volt, aging_obj):
    da = solve_da(pack["price"], pack["pv"], pack["lf"], pl, K=12, use_xu=xu, use_thr=thr, lam=lam)
    rt = solve_rt(da["pda"], pack["price_act"], pack["pv_bus_act"], pack["lf_act"], pl,
                  with_voltage=volt, aging_obj=aging_obj)
    return da, rt


def experiment_week(df, days, pl, seed=20260827):
    rows = []
    packs = {}
    for day in days:
        pack = build_day(df, day, pl, K=12, seed=seed)
        packs[day] = pack
        for name, xu, thr, lam, volt, aging_obj in MODELS:
            da, rt = run_one(pack, pl, name, xu, thr, lam, volt, aging_obj)
            print(f"{day} {name} DA={da['status']} RT={rt['status']} "
                  f"π={rt['profit']:.1f} vmin={rt['vmin']:.3f} viol={rt['n_viol']} "
                  f"t={da['time_s']+rt['time_s']:.2f}s")
            rows.append(row_from(name, da, rt, day, seed))
            if day == days[0] or day.endswith("08"):
                np.savez(STAT / f"{name}_{day}.npz", pda=da["pda"], v=rt["v"],
                         export=rt["export"], price=pack["price_act"],
                         Pf=rt["Pf"], Qf=rt["Qf"], pch=rt["pch"], pdis=rt["pdis"],
                         qbp=rt["qbp"], qbn=rt["qbn"])
    pd.DataFrame(rows).to_csv(STAT / "week_results.csv", index=False)
    return pd.DataFrame(rows), packs


def experiment_seeds(df, day, pl, seeds):
    rows = []
    for sd in seeds:
        pack = build_day(df, day, pl, K=12, seed=sd)
        for name, xu, thr, lam, volt, aging_obj in MODELS:
            da, rt = run_one(pack, pl, name, xu, thr, lam, volt, aging_obj)
            rows.append(row_from(name, da, rt, day, sd))
            print(f"seed {sd} {name} π={rt['profit']:.1f} viol={rt['n_viol']}")
    pd.DataFrame(rows).to_csv(STAT / "seed_results.csv", index=False)
    return pd.DataFrame(rows)


def experiment_sensitivity(df, day, pl0):
    rows = []
    pack0 = build_day(df, day, pl0, K=12, seed=pl0.seed)
    # c_deg
    for c in (6.0, 12.0, 18.0):
        pl = Plant(c_deg=c)
        pack = pack0
        for name in ("B2", "P1"):
            xu, thr, lam, volt, aging_obj = [m[1:] for m in MODELS if m[0] == name][0]
            da, rt = run_one(pack, pl, name, xu, thr, lam, volt, aging_obj)
            r = row_from(name, da, rt, day, pl0.seed)
            r.update(sweep="c_deg", param=c)
            rows.append(r)
    # lam (CVaR weight), aging on, no extra voltage except P1-style off
    for lam in (0.0, 0.05, 0.15):
        pl = Plant()
        da, rt = run_one(pack0, pl, "B2", True, True, lam, False, True)
        r = row_from("B2", da, rt, day, pl0.seed)
        r.update(sweep="lam", param=lam)
        rows.append(r)
        da, rt = run_one(pack0, pl, "P1", True, True, lam, True, True)
        r = row_from("P1", da, rt, day, pl0.seed)
        r.update(sweep="lam", param=lam)
        rows.append(r)
    # PV size
    for ppv in (0.30, 0.60, 0.90):
        pl = Plant(p_pv=ppv)
        pack = build_day(df, day, pl, K=12, seed=pl0.seed)
        for name in ("B2", "P1"):
            xu, thr, lam, volt, aging_obj = [m[1:] for m in MODELS if m[0] == name][0]
            da, rt = run_one(pack, pl, name, xu, thr, lam, volt, aging_obj)
            r = row_from(name, da, rt, day, pl0.seed)
            r.update(sweep="p_pv", param=ppv)
            rows.append(r)
    pd.DataFrame(rows).to_csv(STAT / "sensitivity.csv", index=False)
    return pd.DataFrame(rows)


def experiment_v95(df, day, pl0):
    """Try ANSI 0.95 with more inverter headroom / extra Q."""
    rows = []
    pack = build_day(df, day, pl0, K=12, seed=pl0.seed)
    for head, vmin in [(1.25, 0.95), (2.0, 0.95), (3.0, 0.95), (1.25, 0.93)]:
        pl = Plant(inv_head=head, v_min=vmin)
        da, rt = run_one(pack, pl, "P1", True, True, 0.05, True, True)
        r = row_from("P1", da, rt, day, pl0.seed)
        r.update(inv_head=head, v_min_set=vmin)
        rows.append(r)
        print(f"v95 head={head} vmin_set={vmin} ok={rt['success']} vmin={rt['vmin']:.4f} "
              f"viol={rt['n_viol']} slack_pen_active n_viol_095={rt['n_viol_095']}")
    pd.DataFrame(rows).to_csv(STAT / "v95_try.csv", index=False)
    return pd.DataFrame(rows)


def experiment_ac(df, day, pl):
    pack = build_day(df, day, pl, K=12, seed=pl.seed)
    recs = []
    for name, xu, thr, lam, volt, aging_obj in (("B2", True, True, 0.05, False, True),
                                                 ("P1", True, True, 0.05, True, True)):
        da, rt = run_one(pack, pl, name, xu, thr, lam, volt, aging_obj)
        err = []
        ac_min = []
        ld_min = []
        for t in range(24):
            p, q = injections_from_rt(rt, pack["lf_act"], pack["pv_bus_act"], pl, t)
            vac = bfs_voltage(p, q)
            vld = rt["v"][:, t]
            ac_min.append(float(vac.min()))
            ld_min.append(float(vld.min()))
            err.append(np.abs(vac - vld))
        err = np.stack(err, 0)  # T x 33
        recs.append(dict(
            model=name,
            mean_abs_err_pu=float(err.mean()),
            max_abs_err_pu=float(err.max()),
            p95_abs_err_pu=float(np.quantile(err, 0.95)),
            ld_vmin=float(min(ld_min)),
            ac_vmin=float(min(ac_min)),
        ))
        print(name, "LinDist vs AC |ΔV| mean", recs[-1]["mean_abs_err_pu"],
              "max", recs[-1]["max_abs_err_pu"], "ac_vmin", recs[-1]["ac_vmin"])
    pd.DataFrame(recs).to_csv(STAT / "ac_check.csv", index=False)
    return pd.DataFrame(recs)


def experiment_fdia(df, day, pl, n_mc=200):
    """Residual LinDistFlow detector on voltage measurements.
    Clean: Gaussian noise. Attack: bias on a subset of buses.
    Not an autoencoder — residual vs the model that produced v.
    """
    pack = build_day(df, day, pl, K=12, seed=pl.seed)
    da, rt = run_one(pack, pl, "P1", True, True, 0.05, True, True)
    v = rt["v"]  # 33 x 24
    rng = np.random.default_rng(pl.seed + 99)
    sigma = 0.003  # pu measurement noise
    bias = 0.05
    attack_buses = np.array([17, 21, 32])  # 0-based: 18, 22, 33
    # threshold from clean residuals (should be ~noise)
    clean_max = []
    for _ in range(n_mc):
        noise = rng.normal(0, sigma, v.shape)
        meas = v + noise
        resid = np.abs(meas - v)
        clean_max.append(resid.max())
    theta = float(np.quantile(clean_max, 0.99))
    # evaluate hour-level detection: flag if any bus residual > theta
    y_true, y_pred = [], []
    for k in range(n_mc):
        noise = rng.normal(0, sigma, v.shape)
        attacked = bool(k % 2)  # 50% attack samples
        meas = v + noise
        if attacked:
            meas[attack_buses, :] += bias
        resid = np.abs(meas - v)
        flag = bool(resid.max() > theta)
        y_true.append(int(attacked))
        y_pred.append(int(flag))
    y_true = np.array(y_true); y_pred = np.array(y_pred)
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    prec = tp / max(tp + fp, 1)
    rec = tp / max(tp + fn, 1)
    # bid-attack economic impact: corrupt pda by +0.4 MW, re-solve RT
    pda = da["pda"]
    pda_att = pda + 0.40
    rt_att = solve_rt(pda_att, pack["price_act"], pack["pv_bus_act"], pack["lf_act"], pl,
                      with_voltage=True, aging_obj=True)
    out = dict(
        detector="LinDistFlow residual (not AE)",
        sigma_pu=sigma, bias_pu=bias, theta_99=theta,
        n_mc=n_mc, tp=tp, fp=fp, fn=fn, tn=tn,
        precision=prec, recall=rec,
        clean_profit=rt["profit"], attack_bid_profit=rt_att["profit"],
        attack_bid_dprofit=rt_att["profit"] - rt["profit"],
        attack_bid_ok=rt_att["success"],
    )
    Path(STAT / "fdia_residual.json").write_text(json.dumps(out, indent=2))
    print("FDIA residual", out)
    return out


def wilcoxon_note(week: pd.DataFrame):
    """Paired Wilcoxon P1 vs B2 on profit and n_viol across days."""
    from scipy.stats import wilcoxon
    p1 = week[week.model == "P1"].sort_values("day")
    b2 = week[week.model == "B2"].sort_values("day")
    out = {}
    for col in ("profit", "n_viol", "vmin", "aging"):
        x = p1[col].values
        y = b2[col].values
        try:
            w = wilcoxon(x, y, zero_method="wilcox", alternative="two-sided")
            out[col] = dict(W=float(w.statistic), p=float(w.pvalue),
                            mean_P1=float(x.mean()), mean_B2=float(y.mean()),
                            std_P1=float(x.std(ddof=1) if len(x) > 1 else 0),
                            std_B2=float(y.std(ddof=1) if len(y) > 1 else 0), n=len(x))
        except Exception as e:
            out[col] = dict(error=str(e), mean_P1=float(x.mean()), mean_B2=float(y.mean()), n=len(x))
    Path(STAT / "wilcoxon.json").write_text(json.dumps(out, indent=2))
    print("Wilcoxon", out)
    return out


def figures(week, day="2026-04-08"):
    plt.rcParams.update({"font.family": "serif", "font.size": 8.0,
                         "axes.spines.top": False, "axes.spines.right": False})
    d8 = week[week.day == day]
    order = [m[0] for m in MODELS]
    d8 = d8.set_index("model").loc[order].reset_index()
    cols = [COLORS[m] for m in order]
    x = np.arange(len(order))

    fig, ax = plt.subplots(figsize=(3.6, 2.45))
    ax.bar(x, d8["profit"], color=cols, width=0.7)
    ax.set_xticks(x); ax.set_xticklabels(order, fontsize=7)
    ax.set_ylabel("Realised profit (EUR)")
    fig.tight_layout(); fig.savefig(FIG / "Fig_profit.png", dpi=300); plt.close()

    fig, ax = plt.subplots(figsize=(3.6, 2.45))
    ax.bar(x - 0.18, d8["aging"], 0.36, label="Aging (EUR)", color="#D55E00")
    ax.bar(x + 0.18, d8["n_viol"], 0.36, label="Bus-h V viol.", color="#0072B2")
    ax.set_xticks(x); ax.set_xticklabels(order, fontsize=7)
    ax.legend(frameon=False, fontsize=6.5)
    ax.set_ylabel("EUR  /  count")
    fig.tight_layout(); fig.savefig(FIG / "Fig_aging_volt.png", dpi=300); plt.close()

    # week profit box
    fig, ax = plt.subplots(figsize=(3.6, 2.45))
    data = [week[week.model == m]["profit"].values for m in order]
    bp = ax.boxplot(data, labels=order, patch_artist=True, widths=0.6)
    for patch, c in zip(bp["boxes"], cols):
        patch.set_facecolor(c); patch.set_alpha(0.7)
    ax.set_ylabel("Profit (EUR / day)")
    ax.tick_params(axis="x", labelsize=7)
    fig.tight_layout(); fig.savefig(FIG / "Fig_week_profit.png", dpi=300); plt.close()

    fig, ax = plt.subplots(figsize=(3.6, 2.45))
    data = [week[week.model == m]["n_viol"].values for m in order]
    bp = ax.boxplot(data, labels=order, patch_artist=True, widths=0.6)
    for patch, c in zip(bp["boxes"], cols):
        patch.set_facecolor(c); patch.set_alpha(0.7)
    ax.set_ylabel("Bus-hour violations / day")
    ax.tick_params(axis="x", labelsize=7)
    fig.tight_layout(); fig.savefig(FIG / "Fig_week_viol.png", dpi=300); plt.close()

    # bids / voltage if npz exist
    try:
        p1 = np.load(STAT / f"P1_{day}.npz" if (STAT / f"P1_{day}.npz").exists() else ROOT / f"P1_{day}.npz")
        b2 = np.load(STAT / f"B2_{day}.npz" if (STAT / f"B2_{day}.npz").exists() else ROOT / f"B2_{day}.npz")
        h = np.arange(24)
        fig, ax = plt.subplots(figsize=(3.45, 2.45))
        ax.step(h, b2["pda"], where="mid", label="B2 / P1", color="#009E73", lw=1.2)
        ax.axhline(0, color="#333", lw=0.6)
        ax.set_xlabel("Hour"); ax.set_ylabel("DA export (MW)")
        ax.legend(frameon=False, fontsize=7)
        fig.tight_layout(); fig.savefig(FIG / "Fig_bids.png", dpi=300); plt.close()
        fig, ax = plt.subplots(figsize=(3.45, 2.45))
        ax.plot(h, b2["v"].min(axis=0), label="B2 (no V pen.)", color="#E69F00", ls="--", lw=1.2)
        ax.plot(h, p1["v"].min(axis=0), label="P1 (V slack)", color="#009E73", lw=1.25)
        ax.axhline(0.93, color="#D55E00", lw=0.9, label="0.93 pu floor")
        ax.set_xlabel("Hour"); ax.set_ylabel("Minimum bus voltage (pu)")
        ax.set_ylim(0.86, 1.02)
        ax.legend(frameon=False, fontsize=7)
        fig.tight_layout(); fig.savefig(FIG / "Fig_voltage.png", dpi=300); plt.close()
    except Exception as e:
        print("npz figures skipped", e)

    # time bars
    fig, ax = plt.subplots(figsize=(3.6, 2.45))
    ax.bar(x, d8["time_s"], color=cols, width=0.7)
    ax.set_xticks(x); ax.set_xticklabels(order, fontsize=7)
    ax.set_ylabel("HiGHS wall time (s)")
    fig.tight_layout(); fig.savefig(FIG / "Fig_time.png", dpi=300); plt.close()
    print("figures written")


def main():
    pl = Plant()
    df = hourly()
    days = list_days(df)
    print("days", days)
    week, packs = experiment_week(df, days, pl)
    seeds = [20260827 + i for i in range(5)]
    experiment_seeds(df, days[min(2, len(days)-1)] if "2026-04-08" not in days else "2026-04-08", pl, seeds)
    day8 = "2026-04-08" if "2026-04-08" in days else days[len(days)//2]
    experiment_sensitivity(df, day8, pl)
    experiment_v95(df, day8, pl)
    experiment_ac(df, day8, pl)
    experiment_fdia(df, day8, pl)
    wilcoxon_note(week)
    figures(week, day8)
    # summary
    g = week.groupby("model")[["profit", "n_viol", "vmin", "aging", "time_s", "v_rms_und"]].agg(["mean", "std"])
    print(g)
    print("ok rate", week.da_ok.mean(), week.rt_ok.mean(), "max gap", week[["da_gap","rt_gap"]].max())


if __name__ == "__main__":
    main()
