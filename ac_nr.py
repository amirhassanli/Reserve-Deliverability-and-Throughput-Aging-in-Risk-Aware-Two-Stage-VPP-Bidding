#!/usr/bin/env python3
"""Polar Newton–Raphson AC power flow on the radial IEEE 33-bus (Ybus)."""
from __future__ import annotations
import numpy as np
from ieee33 import pu_branch, SBASE_MVA, VBASE_KV


def ybus():
    fr, to, r, x = pu_branch()
    n = 33
    Y = np.zeros((n, n), dtype=complex)
    for e in range(32):
        y = 1.0 / (r[e] + 1j * x[e])
        i, j = int(fr[e]), int(to[e])
        Y[i, i] += y
        Y[j, j] += y
        Y[i, j] -= y
        Y[j, i] -= y
    return Y


def nr_voltage(p_inj_mw, q_inj_mvar, max_it=25, tol=1e-8):
    """Specified net injections (gen-load) in MW/MVAr. Slack bus 0: V=1∠0.
    Returns |V| pu, converged flag, iterations, max mismatch pu.
    """
    Y = ybus()
    n = 33
    G, B = Y.real, Y.imag
    P = np.asarray(p_inj_mw, float) / SBASE_MVA
    Q = np.asarray(q_inj_mvar, float) / SBASE_MVA
    V = np.ones(n)
    th = np.zeros(n)
    buses = np.arange(1, n)  # PQ
    conv = False
    mis = np.nan
    it = 0
    for it in range(1, max_it + 1):
        Pcal = np.zeros(n)
        Qcal = np.zeros(n)
        for i in range(n):
            for j in range(n):
                a = th[i] - th[j]
                Pcal[i] += V[i] * V[j] * (G[i, j] * np.cos(a) + B[i, j] * np.sin(a))
                Qcal[i] += V[i] * V[j] * (G[i, j] * np.sin(a) - B[i, j] * np.cos(a))
        dP = P[buses] - Pcal[buses]
        dQ = Q[buses] - Qcal[buses]
        mis = float(np.max(np.abs(np.concatenate([dP, dQ]))))
        if mis < tol:
            conv = True
            break
        m = len(buses)
        J = np.zeros((2 * m, 2 * m))
        # H dth, N dV ; M dth, L dV   (standard)
        for a, i in enumerate(buses):
            for b, j in enumerate(buses):
                ang = th[i] - th[j]
                if i == j:
                    Hii = -Qcal[i] - B[i, i] * V[i] ** 2
                    Nii = Pcal[i] / V[i] + G[i, i] * V[i]
                    Mii = Pcal[i] - G[i, i] * V[i] ** 2
                    Lii = Qcal[i] / V[i] - B[i, i] * V[i]
                    J[a, b] = Hii
                    J[a, m + b] = Nii
                    J[m + a, b] = Mii
                    J[m + a, m + b] = Lii
                else:
                    H = V[i] * V[j] * (G[i, j] * np.sin(ang) - B[i, j] * np.cos(ang))
                    N = V[i] * (G[i, j] * np.cos(ang) + B[i, j] * np.sin(ang))
                    M = -V[i] * V[j] * (G[i, j] * np.cos(ang) + B[i, j] * np.sin(ang))
                    L = V[i] * (G[i, j] * np.sin(ang) - B[i, j] * np.cos(ang))
                    J[a, b] = H
                    J[a, m + b] = N
                    J[m + a, b] = M
                    J[m + a, m + b] = L
        try:
            dx = np.linalg.solve(J, np.concatenate([dP, dQ]))
        except np.linalg.LinAlgError:
            break
        th[buses] += dx[:m]
        V[buses] = np.maximum(V[buses] + dx[m:], 0.2)
    return V, conv, it, mis
