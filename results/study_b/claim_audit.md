# Claim vs evidence audit (HiGHS week 6–12 Apr 2026, IEEE 33-bus)

All euros kOptimal, gap 0. B1 = code B1b.

## Effect sizes (7-day mean profit)

| Contrast | What it tests | Δ profit EUR/d | Δ viol /d | Verdict |
|---|---|---|---|---|
| B1 − B0 | CVaR only | **+0.24** | +1 | **Not supported** |
| B2 − B1 | Aging on top of CVaR | **+90.1** | +34 | **Supported (economic)** |
| B2 − B1a | CVaR on top of aging | **−0.09** | −1 | **Not supported** |
| P1 − B2 | Voltage slack, same bid | **−4.3** | **−276** | **Supported (technical), tiny €** |
| P0 − B0 | Voltage without aging | +6.5 | −241 | Voltage works without CVaR |

Day-to-day std of profit ≈ **2485 EUR**. Voltage premium 4.3 EUR is **0.08%** of |B2 profit|. Aging 90 EUR is **1.7%**.

## Bid coupling

B2 and P1 have **identical p^DA every day** of the week. Voltage is a real-time row only. The slogan “connect bidding to control” is **not** a first-stage effect on this data.

## Xu vs throughput

Xu daily-range cost = **85.8 EUR for all six models** on 8 Apr (SoC hits 10–90% box). Throughput aging is what moves: 172 (B0) vs 89 (P1). Claiming Xu as the discriminating aging model is **not** supported; linear throughput is.

## P / Q

0.93 pu: P-only vmin=0.921, 61 viol. Q-only holds 0.93 but −529 EUR. P–Q holds 0.93 at −6109.
0.95 pu: **only P–Q feasible**. This claim **is** supported.

## AC check

P1 LD 0.930 vs NR 0.926, mean |ΔV|=0.17%. LinDistFlow is an acceptable proxy **with ε_v=0.004**. Not OpenDSS.

## FDIA

Voltage bias/ramp/coord: P=R=1.0 against the **same twin that generated v** (upper bound).
Stealth +0.008 pu: recall 0.90.
Bid +0.40 MW: −226 EUR, **voltage detector blind**.
Price +25: −1565 EUR, **blind**.
“Cyber-resilient VPP” as a headline is **not** supported. Residual screening of voltage **is** a limited, honest result.

## CVaR

B0 vs B1: 0.24 EUR/day. Not an innovation on this week.

## LLM / MARL / GNN / B3 / P2 / Full

No numbers. Must stay empty.

## Notation / reporting (fixed)

- Operational floor v_op=0.93 vs technical box 0.80–1.15 pu on v².
- Reported profit omits ρ_s; P1/P0 have s=0 so it coincides with the complete objective.
- Q-only −6638 is not an operating policy (no P cycling).
- 8 Apr aging 92 vs week 69: high spread day → more throughput.
- ε_v=0.007 from B2 max NR error 0.0068, not P1-only 0.0038.
- β=0.05 is the null; β=0.5 on 8 Apr costs ~77 EUR extra conservatism.

## What *is* the paper

A copper-plate CVaR bid does almost nothing here. Putting **throughput aging** in the optimiser halves cycling. Putting **LinDistFlow + P–Q slack** in Stage 2 zeros 0.93 pu violations at a few euros/day, without changing the bid. That is the supported contribution.
