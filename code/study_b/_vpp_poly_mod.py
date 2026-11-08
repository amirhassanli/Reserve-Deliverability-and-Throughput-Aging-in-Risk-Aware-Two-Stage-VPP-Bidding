#!/usr/bin/env python3
"""Two-stage VPP: CVaR DA bidding + LinDistFlow RT correction on IEEE 33-bus.

Ablation (Stage-1 aging vs CVaR; Stage-2 voltage):
  B0   EV, no aging, RT no voltage
  B1a  EV, Xu+throughput, RT no voltage
  B1b  CVaR, no aging, RT no voltage
  B2   CVaR, Xu+throughput, RT no voltage
  P0   EV, no aging, RT voltage slack
  P1   CVaR, Xu+throughput, RT voltage slack
"""
from __future__ import annotations
from dataclasses import dataclass, field
import time
import numpy as np
from scipy.optimize import linprog
from scipy import sparse
from ieee33 import pu_branch, peak_load_mw, SBASE_MVA

XU_W = np.array([0.20, 0.30, 0.30, 0.20])
XU_S = np.array([8.0, 30.0, 60.0, 90.0])  # EUR per unit daily depth


def _as_arr(x, n):
    a = np.asarray(x, dtype=float)
    if a.ndim == 0:
        return np.full(n, float(a))
    return a


@dataclass
class Plant:
    n_bess: int = 3
    bess_bus: tuple = (6, 18, 33)  # 1-based
    p_bess: tuple = (0.30, 0.40, 0.50)  # MW, heterogeneous
    e_bess: tuple = (0.60, 0.80, 1.00)  # MWh
    eta_c: float = 0.95
    eta_d: float = 0.95
    soc_min: float = 0.10
    soc_max: float = 0.90
    soc_init: float = 0.50
    pv_bus: tuple = (7, 24, 31)
    p_pv: float = 0.60  # MW each
    c_deg: float = 12.0  # EUR/MWh throughput (true settlement cost)
    v_min: float = 0.93
    v_max: float = 1.05
    inv_head: float = 1.25
    s_line_max: float = 5.0  # MVA reporting rating
    v_pen: float = 2500.0
    imb_short_add: float = 18.0
    imb_short_c: float = 0.12
    imb_long_add: float = 10.0
    imb_long_c: float = 0.08
    p_da_max: float = 4.0
    lam: float = 0.05
    alpha: float = 0.95
    T: int = 24
    seed: int = 20260827

    def p_arr(self):
        return _as_arr(self.p_bess, self.n_bess)

    def e_arr(self):
        return _as_arr(self.e_bess, self.n_bess)


class LP:
    def __init__(self, n):
        self.n = n
        self.c = np.zeros(n)
        self.er, self.ec, self.ev, self.eb = [], [], [], []
        self.ur, self.uc, self.uv, self.ub = [], [], [], []
        self.lo = np.full(n, -np.inf)
        self.hi = np.full(n, np.inf)

    def obj(self, j, v):
        self.c[j] += v

    def bnd(self, j, lo, hi):
        self.lo[j], self.hi[j] = lo, hi

    def eq(self, terms, b):
        i = len(self.eb)
        for j, v in terms:
            if v:
                self.er.append(i); self.ec.append(j); self.ev.append(v)
        self.eb.append(b)

    def le(self, terms, b):
        i = len(self.ub)
        for j, v in terms:
            if v:
                self.ur.append(i); self.uc.append(j); self.uv.append(v)
        self.ub.append(b)

    def solve(self):
        t0 = time.perf_counter()
        Aeq = sparse.coo_matrix((self.ev, (self.er, self.ec)), shape=(len(self.eb), self.n)).tocsr() if self.eb else None
        Aub = sparse.coo_matrix((self.uv, (self.ur, self.uc)), shape=(len(self.ub), self.n)).tocsr() if self.ub else None
        res = linprog(
            self.c, A_ub=Aub, b_ub=np.array(self.ub) if self.ub else None,
            A_eq=Aeq, b_eq=np.array(self.eb) if self.eb else None,
            bounds=list(zip(self.lo.tolist(), self.hi.tolist())),
            method="highs", options={"disp": False, "presolve": True, "time_limit": 60.0},
        )
        res._time_s = time.perf_counter() - t0
        return res


def imb_prices(da, pl: Plant):
    short = da + pl.imb_short_add + pl.imb_short_c * np.abs(da)
    longp = da - pl.imb_long_add - pl.imb_long_c * np.abs(da)
    short = np.maximum(short, da + 5.0)
    longp = np.minimum(longp, da - 3.0)
    return short, longp


def _opt_record(res):
    ok = bool(res.success)
    gap = 0.0 if ok else np.nan
    # scipy HiGHS LP: success ⇒ proven optimal (no MIP). Dual residual not always exposed.
    return {
        "success": ok,
        "status": "kOptimal" if ok else str(getattr(res, "message", "fail")),
        "time_s": float(getattr(res, "_time_s", np.nan)),
        "nit": int(getattr(res, "nit", 0) or 0),
        "gap": gap,
        "fun": float(res.fun) if res.fun is not None else np.nan,
    }


def solve_da(price, pv, load_fac, pl: Plant, K: int, use_xu=True, use_thr=True, lam=None):
    """Aggregate DA CVaR. pv (K,T) MW total plant PV; load_fac (K,T)."""
    T, Nb = pl.T, pl.n_bess
    lam = pl.lam if lam is None else lam
    p_peak, _ = peak_load_mw()
    p_load_peak = float(p_peak.sum())
    n = 0
    pda = n; n += T
    pch = [0]*K; pdis = [0]*K; soc = [0]*K
    ish = [0]*K; ilo = [0]*K
    smax = [0]*K; smin = [0]*K
    vseg = [[0]*K for _ in range(4)]
    for s in range(K):
        pch[s] = n; n += T
        pdis[s] = n; n += T
        soc[s] = n; n += T
        ish[s] = n; n += T
        ilo[s] = n; n += T
        if use_xu:
            smax[s] = n; n += 1
            smin[s] = n; n += 1
            for m in range(4):
                vseg[m][s] = n; n += 1
    use_cvar = lam > 1e-12
    if use_cvar:
        eta = n; n += 1
        z = n; n += K
    lp = LP(n)
    E = float(pl.e_arr().sum())
    pmax = float(pl.p_arr().sum())
    soc0 = pl.soc_init * E
    smin0, smax0 = pl.soc_min * E, pl.soc_max * E
    cdeg = pl.c_deg if use_thr else 0.0
    for t in range(T):
        lp.bnd(pda + t, -pl.p_da_max, pl.p_da_max)
    for s in range(K):
        if use_xu:
            lp.bnd(smax[s], smin0, smax0)
            lp.bnd(smin[s], smin0, smax0)
            for m in range(4):
                lp.bnd(vseg[m][s], 0.0, float(XU_W[m]))
        for t in range(T):
            lp.bnd(pch[s] + t, 0.0, pmax)
            lp.bnd(pdis[s] + t, 0.0, pmax)
            lp.bnd(soc[s] + t, smin0, smax0)
            lp.bnd(ish[s] + t, 0.0, 8.0)
            lp.bnd(ilo[s] + t, 0.0, 8.0)
    if use_cvar:
        lp.bnd(eta, -1e6, 1e6)
        for s in range(K):
            lp.bnd(z + s, 0.0, 1e6)
    sh, lo = imb_prices(price, pl)
    pi = np.full(K, 1.0 / K)
    w = (1.0 - lam) * pi

    def profit_terms(s, t):
        terms = [(pda + t, float(price[s, t])),
                 (ilo[s] + t, float(lo[s, t])),
                 (ish[s] + t, -float(sh[s, t]))]
        if cdeg:
            terms += [(pch[s] + t, -cdeg), (pdis[s] + t, -cdeg)]
        return terms

    for s in range(K):
        for t in range(T):
            net = float(pv[s, t] - p_load_peak * load_fac[s, t])
            lp.eq([(pda + t, 1.0), (pch[s] + t, 1.0), (ilo[s] + t, 1.0),
                   (pdis[s] + t, -1.0), (ish[s] + t, -1.0)], net)
            if t == 0:
                lp.eq([(soc[s] + t, 1.0), (pch[s] + t, -pl.eta_c),
                       (pdis[s] + t, 1.0 / pl.eta_d)], soc0)
            else:
                lp.eq([(soc[s] + t, 1.0), (soc[s] + t - 1, -1.0),
                       (pch[s] + t, -pl.eta_c), (pdis[s] + t, 1.0 / pl.eta_d)], 0.0)
            if use_xu:
                lp.le([(soc[s] + t, 1.0), (smax[s], -1.0)], 0.0)
                lp.le([(smin[s], 1.0), (soc[s] + t, -1.0)], 0.0)
        lp.eq([(soc[s] + T - 1, 1.0)], soc0)
        extra = []
        if use_xu:
            lp.eq([(smax[s], 1.0 / E), (smin[s], -1.0 / E)] +
                  [(vseg[m][s], -1.0) for m in range(4)], 0.0)
            extra = [(vseg[m][s], -float(XU_S[m])) for m in range(4)]
        for t in range(T):
            for j, v in profit_terms(s, t) + extra:
                lp.obj(j, -w[s] * v)
            extra = []
        if use_cvar:
            terms = [(eta, 1.0), (z + s, -1.0)]
            xu_terms = [(vseg[m][s], -float(XU_S[m])) for m in range(4)] if use_xu else []
            for t in range(T):
                for j, v in profit_terms(s, t):
                    terms.append((j, -v))
            terms += [(j, -v) for j, v in xu_terms]
            lp.le(terms, 0.0)
    if use_cvar:
        lp.obj(eta, -lam)
        inv = lam / max(1.0 - pl.alpha, 1e-9)
        for s in range(K):
            lp.obj(z + s, inv * pi[s])
    res = lp.solve()
    x = res.x if res.x is not None else np.zeros(n)
    out = _opt_record(res)
    out.update({"pda": x[pda:pda + T].copy(), "use_xu": use_xu, "use_thr": use_thr, "K": K, "lam": lam})
    return out


def _children(fr, to):
    ch = [[] for _ in range(33)]
    for e, (i, j) in enumerate(zip(fr, to)):
        ch[int(i)].append((e, int(j)))
    return ch


def _episodes(mask_hours):
    """mask_hours: (T,) bool. Return n_episodes, max_run, mean_run."""
    runs = []
    cur = 0
    for f in mask_hours:
        if f:
            cur += 1
        elif cur:
            runs.append(cur); cur = 0
    if cur:
        runs.append(cur)
    if not runs:
        return 0, 0, 0.0
    return len(runs), int(max(runs)), float(np.mean(runs))


def solve_rt(pda, price, pv_bus_mw, load_fac, pl: Plant, with_voltage=True, aging_obj=True,
             allow_p=True, allow_q=True, ramp_mw=None):
    """24-h RT correction. pv_bus_mw: dict bus->(T,) MW. load_fac (T,)."""
    T = pl.T
    fr, to, r, x = pu_branch()
    p_peak, q_peak = peak_load_mw()
    nB, nE = 33, 32
    Nb = pl.n_bess
    pmax = pl.p_arr()
    Earr = pl.e_arr()
    n = 0
    pch = n; n += Nb * T
    pdis = n; n += Nb * T
    qbp = n; n += Nb * T
    qbn = n; n += Nb * T
    soc = n; n += Nb * T
    ish = n; n += T
    ilo = n; n += T
    Pf = n; n += nE * T
    Qf = n; n += nE * T
    vsq = n; n += nB * T
    sun = n; n += nB * T
    lp = LP(n)

    def ix(base, a, t, dim):
        return base + a * T + t

    cdeg_obj = pl.c_deg if aging_obj else 0.0
    for b in range(Nb):
        for t in range(T):
            lp.bnd(ix(pch, b, t, T), 0.0, (pmax[b] if allow_p else 0.0))
            lp.bnd(ix(pdis, b, t, T), 0.0, (pmax[b] if allow_p else 0.0))
            lp.bnd(ix(qbp, b, t, T), 0.0, (pmax[b] if allow_q else 0.0))
            lp.bnd(ix(qbn, b, t, T), 0.0, (pmax[b] if allow_q else 0.0))
            lp.bnd(ix(soc, b, t, T), pl.soc_min * Earr[b], pl.soc_max * Earr[b])
            Rn = pl.inv_head * pmax[b] * 0.995184726672197
            lp.le([(ix(pch, b, t, T), 0.99518472667), (ix(pdis, b, t, T), 0.99518472667),
                   (ix(qbp, b, t, T), 0.09801714033), (ix(qbn, b, t, T), 0.09801714033)], Rn)
            lp.le([(ix(pch, b, t, T), 0.09801714033), (ix(pdis, b, t, T), 0.09801714033),
                   (ix(qbp, b, t, T), 0.99518472667), (ix(qbn, b, t, T), 0.99518472667)], Rn)
            lp.le([(ix(pch, b, t, T), 0.70710678118), (ix(pdis, b, t, T), 0.70710678118),
                   (ix(qbp, b, t, T), 0.70710678118), (ix(qbn, b, t, T), 0.70710678118)], Rn)
    for t in range(T):
        lp.bnd(ish + t, 0.0, 8.0)
        lp.bnd(ilo + t, 0.0, 8.0)
        for e in range(nE):
            lp.bnd(ix(Pf, e, t, T), -8.0, 8.0)
            lp.bnd(ix(Qf, e, t, T), -8.0, 8.0)
        for b in range(nB):
            lp.bnd(ix(vsq, b, t, T), 0.80**2, 1.15**2)
            lp.bnd(ix(sun, b, t, T), 0.0, 1.0)
            if with_voltage:
                lp.le([(ix(vsq, b, t, T), -1.0), (ix(sun, b, t, T), -1.0)], -pl.v_min**2)
                lp.obj(ix(sun, b, t, T), pl.v_pen)
    sh, lo = imb_prices(price.reshape(1, -1), pl)
    sh, lo = sh[0], lo[0]
    chmap = _children(fr, to)
    bess_bus0 = [bb - 1 for bb in pl.bess_bus]
    pv_bus0 = [bb - 1 for bb in pl.pv_bus]

    for t in range(T):
        inj_p = np.zeros(nB)
        for k, b0 in enumerate(pv_bus0):
            inj_p[b0] += float(pv_bus_mw[pl.pv_bus[k]][t])
        pL = p_peak * float(load_fac[t])
        qL = q_peak * float(load_fac[t])
        for e in range(nE):
            i, j = int(fr[e]), int(to[e])
            terms = [(ix(Pf, e, t, T), 1.0)]
            for e2, j2 in chmap[j]:
                terms.append((ix(Pf, e2, t, T), -1.0))
            if j in bess_bus0:
                bb = bess_bus0.index(j)
                terms += [(ix(pdis, bb, t, T), 1.0), (ix(pch, bb, t, T), -1.0)]
            lp.eq(terms, float(pL[j] - inj_p[j]))
            termsQ = [(ix(Qf, e, t, T), 1.0)]
            for e2, j2 in chmap[j]:
                termsQ.append((ix(Qf, e2, t, T), -1.0))
            if j in bess_bus0:
                bb = bess_bus0.index(j)
                termsQ += [(ix(qbp, bb, t, T), 1.0), (ix(qbn, bb, t, T), -1.0)]
            lp.eq(termsQ, float(qL[j]))
        lp.eq([(ix(vsq, 0, t, T), 1.0)], 1.0)
        for e in range(nE):
            i, j = int(fr[e]), int(to[e])
            lp.eq([(ix(vsq, j, t, T), 1.0), (ix(vsq, i, t, T), -1.0),
                   (ix(Pf, e, t, T), 2 * r[e] / SBASE_MVA),
                   (ix(Qf, e, t, T), 2 * x[e] / SBASE_MVA)], 0.0)
        lp.eq([(ix(Pf, 0, t, T), -1.0), (ish + t, 1.0), (ilo + t, -1.0)], float(pda[t]))
        lp.obj(ish + t, float(sh[t]))
        lp.obj(ilo + t, -float(lo[t]))
        for b in range(Nb):
            if cdeg_obj:
                lp.obj(ix(pch, b, t, T), cdeg_obj)
                lp.obj(ix(pdis, b, t, T), cdeg_obj)
            if t == 0:
                lp.eq([(ix(soc, b, t, T), 1.0), (ix(pch, b, t, T), -pl.eta_c),
                       (ix(pdis, b, t, T), 1.0 / pl.eta_d)], pl.soc_init * Earr[b])
            else:
                lp.eq([(ix(soc, b, t, T), 1.0), (ix(soc, b, t - 1, T), -1.0),
                       (ix(pch, b, t, T), -pl.eta_c), (ix(pdis, b, t, T), 1.0 / pl.eta_d)], 0.0)
        for b in range(Nb):
            lp.eq([(ix(soc, b, T - 1, T), 1.0)], pl.soc_init * Earr[b])

    res = lp.solve()
    x = res.x if res.x is not None else np.zeros(n)
    v = np.zeros((nB, T))
    Pf_a = np.zeros((nE, T)); Qf_a = np.zeros((nE, T))
    for t in range(T):
        for b in range(nB):
            v[b, t] = np.sqrt(max(x[ix(vsq, b, t, T)], 0.0))
        for e in range(nE):
            Pf_a[e, t] = x[ix(Pf, e, t, T)]
            Qf_a[e, t] = x[ix(Qf, e, t, T)]
    pch_a = np.array([[x[ix(pch, b, t, T)] for t in range(T)] for b in range(Nb)])
    pdis_a = np.array([[x[ix(pdis, b, t, T)] for t in range(T)] for b in range(Nb)])
    qbp_a = np.array([[x[ix(qbp, b, t, T)] for t in range(T)] for b in range(Nb)])
    qbn_a = np.array([[x[ix(qbn, b, t, T)] for t in range(T)] for b in range(Nb)])
    export = np.array([-x[ix(Pf, 0, t, T)] for t in range(T)])
    ishv = x[ish:ish + T]
    ilov = x[ilo:ilo + T]
    sh, lo = imb_prices(price.reshape(1, -1), pl)
    sh, lo = sh[0], lo[0]
    da_rev = float((price * pda).sum())
    imb = float((lo * ilov - sh * ishv).sum())
    thr = float((pch_a + pdis_a).sum())
    aging = float(pl.c_deg * thr)  # true settlement, always
    und = np.maximum(pl.v_min - v, 0.0)
    over = np.maximum(v - pl.v_max, 0.0)
    nviol = int(np.sum((v < pl.v_min - 1e-4) | (v > pl.v_max + 1e-4)))
    nviol95 = int(np.sum(v < 0.95 - 1e-4))
    hour_viol = np.any(v < pl.v_min - 1e-4, axis=0)
    n_ep, max_ep, mean_ep = _episodes(hour_viol)
    S = np.hypot(Pf_a, Qf_a)
    n_line = int(np.sum(S > pl.s_line_max + 1e-9))
    out = _opt_record(res)
    out.update({
        "da_rev": da_rev, "imb": imb, "aging": aging,
        "profit": da_rev + imb - aging,
        "vmin": float(v.min()), "vmax": float(v.max()),
        "n_viol": nviol, "n_viol_095": nviol95,
        "v_rms_und": float(np.sqrt(np.mean(und**2))),
        "v_max_und": float(und.max()),
        "n_hour_viol": int(hour_viol.sum()),
        "n_episode": n_ep, "max_episode_h": max_ep, "mean_episode_h": mean_ep,
        "s_max_mva": float(S.max()), "n_line_viol": n_line,
        "q_abs_mvarh": float((qbp_a + qbn_a).sum()),
        "throughput_mwh": thr,
        "export": export, "v": v, "pda": pda,
        "pch": pch_a, "pdis": pdis_a, "qbp": qbp_a, "qbn": qbn_a,
        "Pf": Pf_a, "Qf": Qf_a,
    })
    return out
