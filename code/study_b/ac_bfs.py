#!/usr/bin/env python3
"""Backward-forward DistFlow with quadratic losses (radial AC voltage check)."""
from __future__ import annotations
import numpy as np
from ieee33 import pu_branch, peak_load_mw, SBASE_MVA


def _topo(fr, to):
    nB, nE = 33, 32
    ch = [[] for _ in range(nB)]
    for e, (i, j) in enumerate(zip(fr, to)):
        ch[int(i)].append((e, int(j)))
    # edges in parent-before-child order (BFS from slack)
    order = []
    stack = [0]
    seen = {0}
    while stack:
        u = stack.pop()
        for e, v in ch[u]:
            if v not in seen:
                seen.add(v)
                order.append(e)
                stack.append(v)
    return ch, order


def bfs_voltage(p_inj_mw, q_inj_mvar, n_iter=40, tol=1e-10):
    """p_inj_mw, q_inj_mvar: (33,) net injection (gen - load), MW / MVAr.
    Returns |V| pu using DistFlow with losses. Slack |V|=1, angle unused.
    r,x are pu on SBASE; powers converted to pu.
    """
    fr, to, r, x = pu_branch()
    ch, order = _topo(fr, to)
    nB, nE = 33, 32
    P = np.asarray(p_inj_mw, float) / SBASE_MVA
    Q = np.asarray(q_inj_mvar, float) / SBASE_MVA
    V2 = np.ones(nB)
    Pbr = np.zeros(nE)
    Qbr = np.zeros(nE)
    for _ in range(n_iter):
        V2_old = V2.copy()
        # backward: receiving-end outflow then add losses using sending V
        for e in reversed(order):
            j = int(to[e]); i = int(fr[e])
            Pout = -P[j]
            Qout = -Q[j]
            for e2, _k in ch[j]:
                Pout += Pbr[e2]
                Qout += Qbr[e2]
            Vi2 = max(V2[i], 1e-8)
            I2 = (Pout**2 + Qout**2) / Vi2
            Pbr[e] = Pout + r[e] * I2
            Qbr[e] = Qout + x[e] * I2
        V2[0] = 1.0
        for e in order:
            i = int(fr[e]); j = int(to[e])
            Vi2 = V2[i]
            A = Pbr[e] * r[e] + Qbr[e] * x[e]
            B2 = (r[e]**2 + x[e]**2) * (Pbr[e]**2 + Qbr[e]**2) / max(Vi2, 1e-8)
            V2[j] = max(Vi2 - 2 * A + B2, 1e-8)
        if np.max(np.abs(V2 - V2_old)) < tol:
            break
    return np.sqrt(V2)


def injections_from_rt(rt, load_fac, pv_bus_mw, pl, t):
    """Net MW/MVAr injection at each bus at hour t from an RT solve."""
    p_peak, q_peak = peak_load_mw()
    p = -p_peak * float(load_fac[t])
    q = -q_peak * float(load_fac[t])
    for k, bus in enumerate(pl.pv_bus):
        p[bus - 1] += float(pv_bus_mw[bus][t])
    for b, bus in enumerate(pl.bess_bus):
        p[bus - 1] += rt["pdis"][b, t] - rt["pch"][b, t]
        q[bus - 1] += rt["qbp"][b, t] - rt["qbn"][b, t]
    # slack injection is implied; leave bus 0 as whatever residual
    return p, q
