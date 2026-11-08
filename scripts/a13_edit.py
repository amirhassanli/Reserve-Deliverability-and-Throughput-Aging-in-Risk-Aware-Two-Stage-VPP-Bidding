# -*- coding: utf-8 -*-
"""PHASE11 re-exec integration edits on PHASE7_REVISED -> new docx."""
import sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import docx
SRC = r"C:\Users\Mahboobian\Desktop\article 6\Hassanli_Abbasi_VPP_Bidding_IEEE_PHASE7_REVISED.docx"
DST = r"C:\Users\Mahboobian\Desktop\article 6\Hassanli_Abbasi_VPP_Bidding_IEEE_PHASE11_REEXEC.docx"
d = docx.Document(SRC)

def rep_para(p, old, new):
    # run-level first
    for r in p.runs:
        if old in r.text:
            r.text = r.text.replace(old, new)
            return "run"
    if old in p.text:
        p.text = p.text.replace(old, new)
        return "para"
    return None

def rep_cell(cell, old, new):
    for p in cell.paragraphs:
        res = rep_para(p, old, new)
        if res:
            return res
    return None

edits = []

# E1: NR honesty (para 113)
old = "Table X compares LinDistFlow with a Newton-Raphson (NR) solution on the same 8 April injections; all 24 hourly NR solves converged. The mean absolute discrepancy is 0.17% for F-P1 and the largest observed discrepancy is 0.0068 pu (F-B2). A margin of 0.007 pu is"
new = ("Table X compares LinDistFlow with a Newton-Raphson (NR) solution on the same 8 April injections; all 24 hourly NR solves converged. "
       "The mean absolute discrepancy is 0.17% for F-P1 and the largest observed discrepancy is 0.0068 pu (F-B2). Re-executed on all seven Study-B days, "
       "the F-P1 LinDistFlow minimum of 0.930 pu corresponds to an NR minimum of 0.9261-0.9277 pu (maximum LD-NR deviation 0.0082 pu on 10 April), so the "
       "'zero voltage violations' statement is a LinDistFlow result and the empirical AC margin is about 0.004 pu. A margin of 0.007 pu is")
edits.append(("E1_NR", rep_para(d.paragraphs[113], old, new), old[:60]))

# E2: FDIA honesty (para 119)
old = "A physics-residual/z-score screen was tested offline against six attack tapes (Table XI). It detects every voltage-channel tape, including a stealth tape (recall 0.90), but cannot detect bid or price manipulation because those variables are not observable through"
new = ("A physics-residual/z-score screen was tested offline against six attack tapes (Table XI). It detects every voltage-channel tape, including a stealth tape, "
       "but only against the same LinDistFlow twin: recall rises from 0.01 at delta = 0.002 pu to 0.93 at delta = 0.008 pu and 1.00 at delta >= 0.010 pu, with threshold "
       "theta = 0.0132 pu (99th percentile of 200 clean residual draws). Against an independent Newton-Raphson measurement the same threshold gives recall 0.09/0.68/1.00 "
       "and precision 0.56/0.86/0.89 at delta = 0.004/0.008/0.012 pu (FPR up to 0.12), so the 0.90 figure is a same-twin result, not an independent-detector result. "
       "The screen cannot detect bid or price manipulation because those variables are not observable through")
edits.append(("E2_FDIA", rep_para(d.paragraphs[119], old, new), old[:60]))

# E4: aging mechanism + cdeg function (para 101)
old = "Adding throughput aging improves mean profit by EUR 90/day (1.7% of |profit|) and cuts the aging bill from 170 to 69 EUR/day."
new = ("Adding throughput aging improves mean profit by EUR 90/day (1.7% of |profit|) and cuts the aging bill from 170 to 69 EUR/day. "
       "Re-executed across c^deg in {3,...,20} EUR/MWh, the benefit scales approximately as 7.5*c^deg - 10.7 EUR/day (+15 at c=3, +90 at c=12, +165 at c=20), "
       "and the 242-to-276 violation increase occurs on all seven days because aging raises the midday charge cost, reduces PV absorption by up to 23.5 MWh/day, "
       "and deepens far-end voltage sags.")
edits.append(("E4_AGING", rep_para(d.paragraphs[101], old, new), old[:60]))

# E5: (alpha,K) robustness (para 123)
old = "Sweeping beta in {0, 0.05, 0.15, 0.30, 0.50} on 8 April moves F-P1 profit from about -6105 to -6182 EUR and the day-ahead position from -63.4 to -67.8 MWh: CVaR can affect the solution at higher weights but is economically inert at the operating beta = 0.05. The Xu d"
new = ("Sweeping beta in {0, 0.05, 0.15, 0.30, 0.50} on 8 April moves F-P1 profit from about -6105 to -6182 EUR and the day-ahead position from -63.4 to -67.8 MWh: CVaR can affect the solution at higher weights but is economically inert at the operating beta = 0.05. "
       "Re-executed over alpha in {0.8,0.9,0.95} x K in {12,100}, mean profit varies by at most 6.1 EUR (0.2%), so the operating choice (alpha=0.95, K=12) is not load-bearing. "
       "The Xu d")
edits.append(("E5_ALPHAK", rep_para(d.paragraphs[123], old, new), old[:60]))

# E10: P/Q circular envelope (para 109)
old = "Table IX isolates active and reactive control on the F-P1 bid. P-only control cannot hold either floor. Q-only control holds 0.93 pu but freezes battery arbitrage (aging 0): in this mode the inverter reactive headroom consumes the |P|+|Q| <= 1.25 P_rated budge"
new = ("Table IX isolates active and reactive control on the F-P1 bid. P-only control cannot hold either floor. Q-only control holds 0.93 pu but freezes battery arbitrage (aging 0): in this mode the inverter reactive headroom consumes the |P|+|Q| <= 1.25 P_rated budget. "
       "Re-executed with an inscribed octagonal (circular) inverter envelope, the P-Q gain moves by only +1.8 to +11.1 EUR/day and reactive use stays 13.7-20.1 MVArh/day, "
       "so the 'P-Q is the only practical option' conclusion does not depend on the diamond envelope.")
# para 109 text may be truncated; check
edits.append(("E10_PQ", rep_para(d.paragraphs[109], old, new), old[:60]))

# E11: Study B re-execution statement (para 127)
old = "Table XII summarizes which mechanisms the evidence supports. In Study A the reserve product, not the error-dependence model, explains the gain: removing dependence changes P1 by EUR 6 on the isolation day, the fitted Student-t copula has a near-Gaussian tail p"
new = ("Table XII summarizes which mechanisms the evidence supports. All Study-B figures (Tables VII-XI) were re-executed from the recovered code and data (HiGHS, 7 days, K=12, seed 20260827): "
       "the week ablation, Wilcoxon (W=0, p=0.015625), P/Q ablation, AC triple (LD 0.9300 to NR 0.9262), and FDIA suite reproduce exactly; the new experiments above (NR on all 7 days, c^deg sweep, (alpha,K) grid, circular envelope, FDIA radius/mismatch) are reported with their CSVs. "
       "In Study A the reserve product, not the error-dependence model, explains the gain: removing dependence changes P1 by EUR 6 on the isolation day, the fitted Student-t copula has a near-Gaussian tail p")
edits.append(("E11_REEXEC", rep_para(d.paragraphs[127], old, new), old[:60]))

# E9: reBAP anchors in limitations (para 133 - Future work)
old = "Future work should extend the evaluation across seasons and, where possible, to metered data; test the reserve finding against cleared aFRR/FCR capacity prices; integrate the feeder-aware first stage with the reserve product on one consistent plant; perform a "
new = ("Real-data anchors for reserve-price realism (added on re-execution): in the 1 Jun-21 Aug 2026 market panel (7,872 quarter-hours), reBAP is a single price (undercovered = overcovered = reBAP) with mean 121.20 EUR/MWh against 113.66 DA, CV 1.03 against 0.61, "
       "and 47.5% of hours reBAP > DA; in the 6-19 Aug 2026 OOS window reBAP averages 142.53 EUR/MWh against 131.01 DA (+8.8%). The September 2026 reBAP dispersion (mean 148.65 over 2,784 intervals, range -7208.55 to +4993.15, |reBAP| >= 100 in 66.3%) remains the immutable anchor. "
       "Future work should extend the evaluation across seasons and, where possible, to metered data; test the reserve finding against cleared aFRR/FCR capacity prices; integrate the feeder-aware first stage with the reserve product on one consistent plant; perform a ")
edits.append(("E9_REBAP", rep_para(d.paragraphs[133], old, new), old[:60]))

# E8: Table XII reserve row (table 31)
t = d.tables[31]
for row in t.rows:
    if row.cells[0].text.strip().startswith("Reserve deliverability"):
        oldc = row.cells[2].text
        row.cells[2].text = oldc + "; real aFRR capacity clearing in the 6-19 Aug 2026 OOS window averages 14.55 EUR/MW/h (median 4.85, range 0.34-92.50) against the 16.36 EUR/MW/h implied by the 589 EUR/day proxy, so the level is plausible (+12%) but the flat shape is not."
        edits.append(("E8_RESERVE", "cell", row.cells[0].text.strip()[:40]))
    if row.cells[0].text.strip().startswith("Voltage-residual FDIA screen"):
        oldc = row.cells[1].text
        row.cells[1].text = "Recall 0.93 at delta=0.008 pu (same-twin); 0.68 (NR)"
        edits.append(("E7_FDIA", "cell", row.cells[0].text.strip()[:40]))

# E3/E7: Table 29 stealth row (table 29) - recall cell
t29 = d.tables[29]
for row in t29.rows:
    if "stealth" in row.cells[0].text.lower():
        # recall column index 2
        row.cells[2].text = "0.93 (same-twin) / 0.68 (NR)"
        edits.append(("E3_STEALTH", "cell", row.cells[0].text.strip()[:40]))

# Save
d.save(DST)
print("SAVED", DST)
print("\nEdit results:")
for e in edits:
    print(" ", e)
# verify counts
print("\nparagraphs:", len(d.paragraphs), "tables:", len(d.tables))
