# PHASE12 — Gate-10 (AlocaBid) bundle: validation, reserve-price sweep, and single-price reBAP anchors (Nov 2026)

## 0. Scope and honesty statement

The user pointed to `C:\Users\Mahboobian\Desktop\Aericle 4\arena\VPP_IEEE_Gate10` (`data\processed`, `data\calibration`) and asked to use it. This report records exactly what was executed and what was NOT found. **No number is fabricated; every value below is read from a real file or produced by a real HiGHS solve.**

Critical scope clarification (must be carried into any manuscript edit):

- The article-6 manuscript (`Hassanli_Abbasi_VPP_Bidding_IEEE_PHASE7_REVISED.docx`) has **two** studies: Study A = mean–CVaR energy+reserve bidding on SMARD DE-LU, 5 MW-class, 14-day OOS 6–19 Aug 2026 (numbers **549 / 563.44 / 589**); Study B = degradation-aware feeder (numbers in `PHASE11_REEXEC_REPORT.md`).
- The Gate-10 bundle is a **third, separate project (AlocaBid)**: a 7-stage rolling MILP on SMARD Germany 2024 (single 24-h base day 2024-01-07/08), 100 MW DG / 20 MWh battery. Its locked numbers (198828.98, 200283.79, 191668.92 …) **do not appear anywhere in the article-6 manuscript** (grep of all article-6 docx phases: 0 hits). So Gate-10 results are a **methodology/anchor layer**, not a drop-in replacement for Study A numbers.
- The article-6 Study A LP code (the 14-day OOS orchestration, reserve-price sweep, λ^R=0, Wilcoxon/CI) is **not present in any recovered artifact**. The Gate-10 engine (`gate10f1_repaired_final.py`) is the same family and is now available, but the 14-day orchestration is not. Therefore the three demanded re-solves for Study A remain **blocked at the orchestration layer**; only a single-base-day demonstration is produced here (clearly labelled).

## 1. Bundle validation (copy + re-run)

- Bundle copied to `_draft\gate10_run` (originals untouched). Inputs present: `master_physical_15min.csv` (61,340 rows), `load_forecast_derived_from_smard.csv` (61,340), `da_price_calibrated_forecast.csv` (15,335); reduced scenarios K=30/50/100. `oos_calendar.csv` MISSING (not required by runner).
- `RUN_GATE10_REAL_OOS_ARTICLE_READY_FIXED.py` re-run in the copy: rc=0, 38.1 s. Base 24-h forecast byte-identical to the original (md5 `cc7f6298…`).

### Integrity finding (important)
The re-run produced **different optimization numbers** than the bundle's locked `Gate10_REAL_RESULTS` / Master State table:

| Quantity | Locked (Master State) | Re-run (runner as-shipped) |
|---|---|---|
| B2 K=100 expected profit | 198828.98 | 200283.79 |
| B2 K=100 CVaR95 | 88088.51 | −112287.54 |
| P1 K=100 risk-adj | 198564.09 | 202529.54 |
| Realized settlement B0 | 191668.92 | 191668.92 (same) |

Root cause: the runner imports `gate10f1_repaired_final.py` (find_any prefers that name), which yields 200283.79. The locked Master State table (198828.98) is reproduced by the **other** engine in the bundle, `gate10f1_repaired_final_CVaRfixed_FIXED.py` (expected profit 198828.98, matching locked). The two engines differ in CVaR definition (repaired_final: standard CVaR of −profit; CVaRfixed_FIXED: CVaR of `max(0, loss_reference − profit)` with `loss_reference` default 0, which collapses to 0 when all scenario profits are positive). The realized-settlement layer is identical in both (191668.92), so settlement numbers are stable.

**Recommendation for the bundle's own manuscript (`AlocaBid_IEEE_Final_Draft.tex`):** decide and document which engine is canonical; the runner as-shipped does not reproduce the locked table. For the article-6 manuscript this does not affect any number (Gate-10 numbers are not cited there).

## 2. Reserve-price sweep (0–150 % of the proxy) — Gate-10 single base day

Engine: `gate10f1_repaired_final.py`, K=100, base day 2024-01-07/08, proxy reserve price 5 EUR/MW. Sweep `market.reserve_price_eur_per_mw` ∈ {0, 1.25, 2.5, 3.75, 5.0, 6.25, 7.5} (= 0/25/50/75/100/125/150 %). Output: `_draft\sweep_reserve_price_K100.csv`.

| reserve_price (EUR/MW) | % of proxy | B2 exp. profit | P1 risk-adj | mean RES (MW) | reserve revenue (EUR/day) |
|---|---:|---:|---:|---:|---:|
| 0.00 | 0 | 200163.79 | 202407.14 | 1.000 | 0.00 |
| 1.25 | 25 | 200193.79 | 202437.74 | 1.000 | 30.00 |
| 2.50 | 50 | 200223.79 | 202468.34 | 1.000 | 60.00 |
| 3.75 | 75 | 200253.79 | 202498.94 | 1.000 | 90.00 |
| 5.00 | 100 | 200283.79 | 202529.54 | 1.000 | 120.00 |
| 6.25 | 125 | 200313.79 | 202560.14 | 1.000 | 150.00 |
| 7.50 | 150 | 200343.79 | 202590.74 | 1.000 | 180.00 |

Findings (Gate-10, single base day):
1. **RES is pinned at the N-1 surviving-flexibility cap (1.0 MW) at every price level** → reserve revenue is exactly linear in price (slope = 1.0 MW × 24 h = 24 EUR per 1 EUR/MW). The marginal value of reserve price is therefore trivially 24 EUR/day per EUR/MW; there is no quantity response.
2. **B2 and P1 have identical expected profit at every price level** (200163.79 … 200343.79). P1's advantage is confined to the risk-adjusted objective (202407 … 202590) via CVaR protection. In this model, reserve revenue does not distinguish P1 from B2.
3. **Risk-neutral P1 (λ_risk = 0) at the proxy price is byte-identical to B2** (`P1 − B2 = 0.00` EUR; `_draft\p1_riskneutral_K100.csv`). So P1's entire differentiation from B2 is the CVaR term (λ = 0.02); reserve price and reserve quantity are shared.

**Implication for the article-6 manuscript:** the reviewer's demand "P1 with λ^R = 0 + paired test on reserve-stripped differences" is answered structurally by (2)–(3): in the only available engine, stripping risk aversion (λ = 0) eliminates the P1–B2 gap entirely, and stripping reserve price (0 %) reduces both models identically. The *magnitude* of the reserve contribution in article-6's Study A (589 EUR/day) is a property of the Study A plant/data and cannot be re-derived from Gate-10; but the qualitative structure (reserve revenue common to both, gain driven by risk adjustment) is consistent with the manuscript's Table III decomposition (reserve-capacity line 589, energy/imbalance/fuel netting −40).

## 3. Single-price reBAP anchors (real data, no LP)

Source: `article 6\data\processed\market_data_2026-summer\market_panel_15min.csv` (7,872 quarter-hours, 1 Jun – 21 Aug 2026, 82 days). Output: `_draft\rebap_summary.csv`.

Structural finding (decisive for the "two-price proxy vs single-price reBAP" critique): **reBAP is a single price in this panel** — `rebap_undercovered == rebap_overcovered == rebap` for all 7,872 rows. The manuscript's two-price imbalance proxy (`da ± spread`) is therefore structurally unlike the German single-price reBAP, and any "single-price reBAP settlement" re-run must use one price, not two.

| Quantity | Value |
|---|---:|
| DA price mean (EUR/MWh) | 113.66 (median 125.37; range −45.87 … 665.82; std 69.56) |
| reBAP mean (EUR/MWh) | 121.20 (median 123.29; range −915.96 … 2848.28; std 125.37) |
| reBAP − DA (mean) | +7.55 (median −1.89; range −963.8 … +2663.15) |
| Correlation DA vs reBAP | 0.618 |
| Share of hours reBAP > DA | 47.5 % (reBAP < DA: 52.5 %) |
| Share of days with mean reBAP > mean DA | 54.2 % (83 days; daily diff range −43.4 … +136.7) |
| Coefficient of variation: reBAP | 1.034 (DA: 0.612) |
| Manuscript two-price proxy error vs reBAP | mean |da − 2 − rebap| = 43.01; mean |da + 2 − rebap| = 43.19 EUR/MWh |

OOS window (6–19 Aug 2026, 14 days, 1,344 h): DA mean 131.01, reBAP mean 142.53 (+11.53, +8.8 %), correlation 0.660.

**Implications (honest, data-grounded):**
- The reBAP single price is **higher on average** than DA in the OOS window (+8.8 %), so a single-price reBAP settlement would not simply depress revenue; the direction is mixed (reBAP below DA in 52.5 % of hours).
- reBAP is **~1.7× more volatile** than DA (CV 1.03 vs 0.61) with extreme spikes (−916 … +2848), so a reBAP-settled reserve product faces tail exposure that the flat two-price proxy does not capture.
- The manuscript's existing sensitivity ("gain remains positive as long as reserve revenue exceeds ~40 EUR, ~7 % of the proxy") is a report-time calculation on the Table III decomposition, not a re-solved run. A genuine single-price reBAP re-optimization requires (a) the Study A LP code (unavailable) and (b) running it with reBAP as both the DA and imbalance price. Neither is available; the anchors above are the honest, citable substitute and are now recorded for the Limitations section.

## 4. What remains blocked (unchanged, restated)

- **Study A re-solves (549/563/589):** reserve-price sweep 0–150 %, P1 with λ^R = 0, single-price reBAP re-optimization, and paired Wilcoxon/CI on the 14-day OOS. Blocked because the Study A LP + 14-day orchestration + paired-test scripts are not in any recovered artifact (neither `workspace-….zip` Study B, nor the Gate-10 bundle, which is a different study). The Gate-10 engine is the same family and the sweep methodology is now demonstrated (§2); transferring magnitudes to Study A requires the Study A code.
- **B1 Gaussian-copula benchmark, λ/α sensitivity, paired bootstrap/Wilcoxon** for Gate-10's own manuscript: remain data-dependent per its audit.

## 5. Files produced

- `_draft\gate10_run\` — working copy of the bundle (untouched originals).
- `_draft\gate10_run\Gate10_REAL_RESULTS\` — regenerated by re-run (rc=0).
- `_draft\sweep_reserve_price_K100.csv` — reserve-price sweep (§2).
- `_draft\p1_riskneutral_K100.csv` — risk-neutral P1 (§2).
- `_draft\rebap_summary.csv` — reBAP anchors (§3).
- `_draft\PHASE12_GATE10_REEXEC_REPORT.md` (this file).

## 6. Recommended manuscript actions (article-6)

1. Keep Study A numbers (549/563.44/589) as simulation results on proxy prices; add the §3 reBAP anchors to the Limitations/discussion as "realized OOS-window anchors" (single price, +7.55 EUR/MWh mean, 1.03 CV, 47.5 % of hours reBAP > DA, OOS-window +11.53).
2. Add one sentence noting that a genuine single-price reBAP re-optimization is the required next experiment (already present in §VIII) — now with the structural fact that reBAP is a single price in the OOS window.
3. Do **not** import Gate-10 absolute numbers (198828/200283/191668) into article-6; they belong to a different study and a different (unresolved) engine variant.
4. For the bundle's own manuscript (`AlocaBid_IEEE_Final_Draft.tex`), resolve the engine-variant inconsistency (§1) before submission.
