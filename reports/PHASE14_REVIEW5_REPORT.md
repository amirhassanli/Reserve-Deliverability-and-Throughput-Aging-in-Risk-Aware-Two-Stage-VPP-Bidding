# PHASE14 — Review-5 remaining items — 2026-11-07

Output: `article 6\Hassanli_Abbasi_VPP_Bidding_IEEE_PHASE14_REVIEW5_FINAL.docx` (+ `_SINGLECOLUMN`).
Copies in `VPP_Article6_Project\manuscript\`.

## Integrity
166 paras (−2: Table XIII caption rows), **32 tables** (−1: Table XIII *removed* per N2 — its
content duplicates Table II; one oMath belonged to that table, so oMath 68 vs 69 is expected),
12 images, 50 oMathPara. Sept anchors intact (148.65 ×4, 2,784 ×4, 2249.80, 102.15, 13.01).

## Newly executed experiments (all real HiGHS / real data)

### P0-6 — LD floor 0.937 pu + NR all 7 days  (`scripts/studyb_v937_rerun.py`)
| Week (7 days, seed 20260827) | LD viol | NR Vmin | result |
|---|---|---|---|
| P1 @0.937 | 0 (by construction) | **0.9338–0.9344 every day (≥0.930)**, max LD–NR err 0.0032 pu | NR shortfall removed |
| P1 cost | | | weekly mean −5109.00 → −5114.40 = **5.4 EUR/day** |
- Manuscript §News (Table X para) updated with both base-case (0.93) and 0.937 runs.

### P0-4b — Study-B charge/discharge overlap (`results/study_b/v937/studyb_overlap_archived_days.csv`)
- No-aging models (B0/B1b/P0): overlap **8.53 and 2.46 MWh/day** on 6/8 Apr.
- Aging-priced models (B1a/B2/P1): overlap **exactly 0** on both archived days.

### B3 — real gap reBAP vs proxy λ− (`results/study_b/v937/b3_rebap_gap_daily.csv`)
- OOS window (6–19 Aug): reBAP 142.53, DA 131.01, proxy λ− 110.50 → **gap +32.03 EUR/MWh**,
  reBAP above λ− in **67.9 %** of intervals; daily mean gap **−2.8 … +99.3** → sign of the
  ≈398 EUR/day imbalance channel is NOT stable ⇒ 151 (−73 %) is the robust reading.

### N1 — 23.5 vs 3.5 reconciled (`ws_run/results_ext/e5_f11_diag.csv` + npz)
- "23.5 MWh/day" = **total (charge+discharge) throughput reduction on 6 Apr** (27.3 → 3.9);
  discharge-only half = 11.1 MWh that day; on 8 Apr discharge-only B0−P1 = **3.3 MWh ≈ EFC
  arithmetic (2.98−1.54)×2.4**. Different quantities/days — contradiction dissolved.

## Manuscript text fixes
| ID | Fix |
|----|-----|
| F1 | Deliverability block printed per scenario: r↑ ≤ P_B−p_dis, r↓ ≤ P_B−p_ch, r↑+r↓ ≤ Ṝ (1.5 MW sold), E ≥ E_min+τ↑r↑/η_d, E+η_cτ↓r↓ ≤ E_max; τ values declared unrecoverable pending artifacts |
| F2 | (PHASE13) honest statement about omitted λᴿr term |
| F3 | (PHASE13) CVaR identity corrected; 77-EUR β-sweep cited |
| F4 | First-stage variables fixed (pDA + r↑/r↓ first stage; no ω index on pDA) |
| F5 | Nomenclature: v = squared voltage magnitude (v = |V|², floor v ≥ 0.93²) |
| F7 | Nomenclature S_nn → S_b (XML-level fix) |
| F8 | θ_d/x_d* rows moved out of "Decision Variables"; reserve row clarified as two separate variables |
| N2 | Table XIII deleted (duplicate of Table II); no text references to renumber |
| B1 | Identification statement: flat prices ⇒ objective sees only r↑+r↓ (capacity rent); POS/NEG split in re-execution program |
| B6 | Study-B overlap now reported (8.53/2.46 vs 0) |
| B3 | Real-measurement sentence added to Limitations (+32.03, 67.9 %) |
| P0-6/C3 | Table XII P–Q row now cites the 0.937/NR-verified run |
| P2-2 (partial) | Abstract rewritten to 235 words (no "ahead on every day" claim, decomposition numbers added, NR qualifier added) |

## Still open (documented in-text as such)
- P0-1/P0-2 re-settlement of the 14 OOS days on real aFRR/reBAP — **blocked: Study-A LP artifacts unrecovered**
  (verified: no solver package anywhere on disk; RUN_STRICT_ROLLING_OOS.py is a stop-guard stub).
- Study-A overlap report (needs A-solver).
- τ↑/τ↓ numerical values (will come with re-derived LP).
- Fig. 3 physical removal + figure renumbering (high-risk; currently "descriptive only" in Limitations).
- Title change (reviewer suggestion) — awaiting author decision.
- DM/HAC full blocker following (needs the daily Study-A diffs, blocked as above).
