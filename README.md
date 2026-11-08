# Reserve Rent, Error Dependence, and Feeder Voltage: A Controlled Ablation of VPP Bidding Components

**IEEE manuscript project** — two linear-programming studies on SMARD DE-LU data,
with rolling out-of-sample evaluation and feeder-constrained (IEEE 33-bus) evidence.

- **Author:** Amir Hassanli (single author, no affiliation)
- **Status:** submission-ready (PHASE16 — Review-5 package closed: title per reviewer, Fig. 3 removed, 11 figures / 31 tables / 194-word abstract, no dangling cross-references)
- **Manuscript:** `manuscript/Hassanli_Abbasi_VPP_Bidding_IEEE_PHASE16_FINAL.docx` (2-column IEEE)
  and `..._SINGLECOLUMN.docx`

## Repository layout

```
VPP_Article6_Project/
├── manuscript/        # final docx (2-col + single-col) + data dictionary supplement
├── code/
│   ├── study_b/       # degradation-aware feeder study (HiGHS LP, IEEE 33-bus)
│   └── gate10/        # Gate-10 / AlocaBid engine + OOS runner (separate study)
├── data/
│   ├── study_b/       # SMARD week raw (6-12 Apr 2026)
│   ├── gate10/        # processed + calibration + reduced scenarios
│   └── market/        # summer 2026 + OOS Aug + Sept manifests (real data)
├── figures/           # standalone figure files (PNG) used in the manuscript
├── results/
│   ├── study_b/       # week ablation, AC, FDIA, claim_audit + ext/ (E1-E6) + v937/ (0.937 pu rerun, overlap, reBAP-gap)
│   │   └── solutions/ # archived LP solutions (.npz, per model per day: dispatch, SoC, voltage, overlap inputs)
│   └── gate10/        # reserve-price sweep, risk-neutral P1, reBAP summary
├── reports/           # PHASE11-15 reports, RESPONSE_TO_REVIEWERS, changelog
└── scripts/           # reproducibility scripts for every number in the paper
```

## Key numbers (all from real files / real HiGHS solves)

### Study A (market bidding, 5 MW-class, SMARD DE-LU)
- Reserve-capable P1 vs expected-value B0: EUR 549/day (isolation day, 19 Aug 2026);
  EUR 563.44/day (4.84 %) over 14 unseen days (6-19 Aug 2026).
- Reserve-capacity revenue line: EUR 589; energy/imbalance/fuel net -40 EUR.
- Paired Wilcoxon p ≈ 1.2e-4 (2/2^14), 5000 bootstrap resamples.

### Study B (feeder, IEEE 33-bus, 6-12 Apr 2026, K=12, seed 20260827)
- Week ablation: B0 -5195.03 / 241.3 viol / 170.1 aging; B2 +90.3 EUR/day; P1 0 viol (LinDistFlow).
- Wilcoxon P1 vs B2: W=0, p=0.015625 (n=7).
- AC (NR): F-P1 mean |ΔV| 0.0017, max 0.0038 pu; NR min 0.9262 (below 0.930 floor).
- FDIA: V_stealth recall 0.90 (same-twin); 0.68 (independent NR) at δ=0.008 pu.
- re-executed extensions: NR on all 7 days, c^deg sweep 3-20, (α,K) grid, circular envelope, FDIA radius/mismatch.

### Real-data anchors (reserve-price realism)
- Summer 2026 market panel (1 Jun - 21 Aug, 7,872 quarter-hours): reBAP is a single price
  (undercovered = overcovered = reBAP), mean 121.20 EUR/MWh vs DA 113.66, CV 1.03 vs 0.61,
  47.5 % of hours reBAP > DA. OOS window (6-19 Aug): reBAP 142.53 vs DA 131.01 (+8.8 %).
- Real aFRR capacity clearing (6-19 Aug 2026): mean 14.55 EUR/MW/h (median 4.85, range 0.34-92.50)
  vs 16.36 implied by the 589 EUR/day proxy (+12 %, level plausible, flat shape not).
- September 2026 anchor (immutable): reBAP mean 148.65 over 2,784 intervals (1-29 Sep),
  range -7208.55..+4993.15, |reBAP| >= 100 in 66.3 %; aFRR 2249.80, FCR 102.15, mFRR 13.01.

## Reproducibility

Study B (from `code/study_b/` + `data/study_b/`):
```bash
cd code/study_b
# adjust ROOT paths or use the patched copies in _draft/ws_run
python run_experiments.py        # week ablation, seeds, sensitivity, Wilcoxon, FDIA
python extra_experiments.py      # P/Q, AC triple, FDIA suite
```

Gate-10 (from `code/gate10/` + `data/gate10/`):
```bash
cd code/gate10
python RUN_GATE10_REAL_OOS_ARTICLE_READY_FIXED.py   # rc=0, regenerates Gate10_REAL_RESULTS
```
Reserve-price sweep and reBAP anchors: see `scripts/`.

## Important notes

- **Two studies are deliberately kept separate** (different plants; documented in response letter).
- **Study A numbers (549/563/589) are simulation results on proxy prices**, not re-solved;
  reserve-price realism is tested only against real clearing data (see anchors above).
- **Gate-10 (AlocaBid) is a separate project** whose numbers (198828/200283/191668) are NOT cited
  in this manuscript; its engine-variant inconsistency is documented in
  `reports/PHASE12_GATE10_REEXEC_REPORT.md`.
- No synthetic data, no fabricated numbers; every value traces to a file in `data/` or a HiGHS solve.

## License

Data: SMARD/Netztransparenz/Energy-Charts (public, CC BY 4.0 where applicable).
Code: to be released with DOI upon acceptance (see manuscript availability note).
