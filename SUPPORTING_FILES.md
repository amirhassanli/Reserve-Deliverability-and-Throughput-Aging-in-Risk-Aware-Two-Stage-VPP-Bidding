# Supporting materials — VPP bidding (Article 6)

This file lists everything that accompanies the manuscript for journal submission
and what is archived in the companion GitHub repository:

https://github.com/amirhassanli/Reserve-Deliverability-and-Throughput-Aging-in-Risk-Aware-Two-Stage-VPP-Bidding

Repository main branch: `e1a37c8`+`PHASE18 push` (see the repository “Commits” page).

## 1. Manuscript (two variants, identical content)

| File | Variant | Size |
|---|---|---|
| `manuscript/Hassanli_Abbasi_VPP_Bidding_IEEE_PHASE18_FINAL.docx` | IEEE two-column | ~2.36 MB |
| `manuscript/Hassanli_Abbasi_VPP_Bidding_IEEE_PHASE18_FINAL_SINGLECOLUMN.docx` | single-column | ~2.36 MB |
| `manuscript/Data_Dictionary_Supplement_PHASE7.docx` | data dictionary supplement | tracked |
| `figures/manuscript/fig01–fig11.png` | figures embedded in the manuscript (byte-exact extraction) | 11 files |

### Manuscript integrity (PHASE18)
- Paragraphs: 166 | Tables: 31 | Figures: 11 | Equation objects: 68 oMath + 50 oMathPara
- Abstract: 194 words (IEEE ceiling 250)
- Figure captions 1–11 contiguous (old Fig. 3 removed per author/decision); no dangling figure or table references
- Table captions I–XII contiguous
- September anchors intact: reBAP mean 148.65 over 2,784 intervals (range −7208.55…+4993.15; \|reBAP\|≥100 in 66.3 %), aFRR 2249.80, FCR 102.15, mFRR 13.01
- Title: “Reserve Rent, Error Dependence, and Feeder Voltage: A Controlled Ablation of VPP Bidding Components” (reviewer’s suggested title, accepted)

## 2. Code (reproducibility)

| Path | Role |
|---|---|
| `code/study_b/*.py` | Study B: two-stage mean–CVaR bid + LinDistFlow RT correction on IEEE 33-bus (HiGHS only): `vpp_two_stage.py`, `run_experiments.py`, `run_case.py`, `ac_nr.py`, `ac_bfs.py`, `ieee33.py`, `save_docx.py`, `_vpp_poly_mod.py`, `make_figures.py`, `aging_ramp_figs.py`, `extra_experiments.py`, `html_to_docx.py` |
| `code/gate10/*.py` | Gate-10 / AlocaBid engine + strict OOS runner (separate project, not cited in the manuscript): `RUN_GATE10_REAL_OOS_ARTICLE_READY_FIXED.py`, `gate10f1_repaired_final.py`, `CHECK_GATE10_REQUIRED_INPUTS.py`, … |
| `scripts/*.py` | Reproducibility / audit scripts: `studyb_v937_rerun.py`, `b3_rebap_gap.py`, `gate10_run_sweep.py`, `sept_2026_anchors.py`, plus earlier audit scripts |
| `setup_github.ps1` | one-shot init + force-push for the existing GitHub target repo |

## 3. Data

| Path | Content |
|---|---|
| `data/study_b/smard_da_week.csv`, `smard_power_week.csv` | SMARD week raw (6–12 April 2026) — Study B input |
| `data/market/market_panel_oos_2026_08_15min.csv` | 14-day OOS window (6–19 Aug 2026): DA + reBAP + national load/solar/wind, 1,344 quarter-hours |
| `data/market/market_panel_summer_2026_15min.csv` | Summer panel (1 Jun–21 Aug 2026): 7,872 quarter-hours |
| `data/market/afrr_capacity_oos_2026_08.csv` | real cleared aFRR capacity, OOS window, 168 hourly POS/NEG rows (GERMANY_AVERAGE mean 14.55 EUR/MW/h) |
| `data/market/manifest_oos_2026_08.json` / `manifest_summer_2026.json` | extraction manifests |
| `data/market/sept_2026/` | September 2026 snapshot: reBAP panel (2,880 rows, 30 Sep kept blank as N.A.), FCR capacity (180 products), mFRR marginal (360 rows), raw XLSX/JSON exports |
| `data/gate10/processed/*.csv` | Gate-10 physical 15-min + derived load forecast + information set + hourly DA price |
| `data/gate10/calibration/*.csv` | joint residual database, copula correlations, baseline/corrected DA forecasts |
| `data/gate10/scenarios/reduced_scenarios/*.csv` | reduced scenario sets (K = 30/50/100) + reduction diagnostics |

## 4. Results (re-executed from recovered code)

| Path | Content |
|---|---|
| `results/study_b/week_results.csv` | week ablation (B0/B1a/B1b/B2/P0/P1): profits, violations, aging |
| `results/study_b/week_v937.csv` | PHASE14 rerun at LD floor 0.937 pu + NR verification (all 7 days) |
| `results/study_b/v937/studyb_overlap_archived_days.csv` | charge/discharge overlap from archived LP solutions |
| `results/study_b/v937/b3_rebap_gap_daily.csv` | real gap reBAP − λ− proxy on OOS panel |
| `results/study_b/ac_*.csv`, `pq_ablation.csv`, `sensitivity.csv`, `seed_results.csv` | AC triple, P/Q ablation, sensitivity, seeds |
| `results/study_b/wilcoxon.json`, `fdia_*.json` | Wilcoxon (W=0, p=0.015625), FDIA suite |
| `results/study_b/ext/*.csv` | extensions: NR multiday, c^deg sweep, (α,K) grid, circular envelope, FDIA radius/mismatch |
| `results/study_b/solutions/*.npz` | archived LP solutions per model per day (dispatch, SoC, v, Pf/Qf, pch/pdis — basis of overlap numbers) |
| `results/gate10/*.csv`, `results/gate10/*.json` | Gate-10 sweep / settlement summary (separate project; not cited) |
| `results/market/sept_2026_anchors.json` | recomputed September anchors from archived files |

## 5. Reports

`reports/PHASE11_REEXEC_REPORT.md`, `PHASE12_GATE10_REEXEC_REPORT.md`, `PHASE13_REVIEW5_REPORT.md`, `PHASE14_REVIEW5_REPORT.md`, `PHASE15_FINAL_PACKAGING.md`, `PHASE16_REPORT.md`, `RESPONSE_TO_REVIEWERS_PHASE15.md`, `PHASE7_CHANGELOG.md`

## 6. What is NOT reproducible (stated in the manuscript, §V-A / §VIII)

- The Study-A LP solver and per-run scenario/settlement artifacts were not recovered anywhere on disk (`RUN_STRICT_ROLLING_OOS.py` is a stop-guard stub only). Study-A numbers (Tables II–VI, Figs. 1–10) are therefore simulations on proxy prices carried forward from earlier revisions; direct re-settlement of the 14 OOS days on real aFRR/reBAP prices, numeric τ↑/τ↓ values, and a DM/HAC correction of the daily gain remain blocked pending artifact recovery. The manuscript states this explicitly rather than implying reproducibility.
