# Degradation-aware two-stage VPP (IEEE 33-bus, SMARD)

**Title:** A Degradation-Aware Two-Stage Framework for Secure VPP Bidding and Feeder-Constrained Dispatch
**Authors:** Amir Hassanli, Ali Reza Abbasi
**Strategy:** Option B — provable HiGHS LPs. LLM/MARL/GNN not trained.

## Manuscript (saved)

- `paper/Hassanli_Abbasi_VPP_TwoStage_IEEE.html` — primary IEEE HTML
- `paper/Hassanli_Abbasi_VPP_TwoStage_IEEE.docx` — Word
- `paper/figures/` — Fig. 1–15 (feeder, heatmap, P/Q, NR companion plots, Pareto, Xu vs throughput, …)

## Main code (saved)

| File | Role |
|---|---|
| `src/vpp_two_stage.py` | Stage-1 CVaR LP + Stage-2 LinDistFlow LP (`solve_da`, `solve_rt`) |
| `src/ieee33.py` | Baran–Wu 33-bus r, x, peak load |
| `src/run_experiments.py` | Week factorial, seeds, sensitivity, Wilcoxon |
| `src/extra_experiments.py` | P/Q, Newton–Raphson, FDIA suite |
| `src/ac_nr.py` / `src/ac_bfs.py` | Polar NR and lossy DistFlow check |
| `src/aging_ramp_figs.py` | Rainflow/Xu, ramps, Pareto |

Run: `python3 src/run_experiments.py` then `python3 src/extra_experiments.py`.

## Real HiGHS numbers (Table III, 7-day mean, gap 0)

| Model | LLM | CVaR | Aging | V | FDIA | Profit | Viol/d | Aging EUR |
|---|---|---|---|---|---|---|---|---|
| B0 | N | N | N | N | N | −5195 | 241 | 170 |
| B1 (=B1b) | N | Y | N | N | N | −5195 | 242 | 169 |
| B2 | N | Y | Y | N | N | −5105 | 276 | 69 |
| B3 | Y | Y | Y | N | N | — | — | — |
| P1 | N | Y | Y | Y | N | −5109 | 0 | 67 |
| P2 / Full | Y | … | … | … | … | — | — | — |

Wilcoxon P1 vs B2, n=7: profit and n_viol p=0.016. P–Q only holds 0.95 pu. NR P1 mean |ΔV|=0.17%. Residual stealth recall 0.90.

## Results archive

`results/week_results.csv`, `pq_ablation.csv`, `ac_triple.csv`, `fdia_suite.json`, `rainflow.csv`, `ramp.csv`, `wilcoxon.json`.
