# Archived Study-B LP solutions

One `.npz` per model per archived day (models B0, B1a, B1b, B2, P0, P1; days 2026-04-06 and
2026-04-08), plus the four P/Q ablation runs on 8 April. These are the solver outputs behind
`results/study_b/week_results.csv`, the AC/NR checks, the charge–discharge overlap numbers in
`results/study_b/v937/studyb_overlap_archived_days.csv`, and the PV-absorption reconciliation.

Arrays (hourly, 24 columns):

| Key | Shape | Meaning |
|---|---|---|
| `pda` | (24,) | first-stage day-ahead energy position, MW |
| `v` | (33, 24) | LinDistFlow squared voltage magnitude, pu² |
| `export` | (24,) | export/import at the substation, MW |
| `price` | (24,) | day-ahead price used in that solve, EUR/MWh |
| `Pf`, `Qf` | (32, 24) | branch active/reactive flows, MW/MVAr |
| `pch`, `pdis` | (3, 24) | battery charge/discharge per unit (units at buses 6, 18, 33), MW |
| `qbp`, `qbn` | (3, 24) | reactive support split (positive/negative), MVAr |

Overlap convention used in the paper: `min(pch, pdis)` summed over units and hours (MWh),
i.e. simultaneous charging and discharging. Aging-priced models (B1a, B2, P1) show exactly zero
overlap on both archived days; no-aging models (B0, B1b, P0) show 8.53 and 2.46 MWh/day.
