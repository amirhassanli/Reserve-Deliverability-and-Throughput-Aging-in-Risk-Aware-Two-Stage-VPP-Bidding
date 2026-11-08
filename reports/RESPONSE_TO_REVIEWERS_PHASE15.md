# Response to Reviewers — Fifth Review (Major Revision, 7 Nov 2026)

Status after PHASE13/14/15. All numbers below are reproduced from real files or real HiGHS solves.

## 1. Internal contradictions (P0-7) — RESOLVED

| # | Contradiction | Resolution in the manuscript |
|---|---|---|
| C1 | "aFRR file not present" vs "14.55 EUR/MW/h" | §V-A now states the September download lacks the file, and that the cleared German aFRR capacity series for the OOS window was retrieved separately (regelleistung.net, 168 hourly POS/NEG rows; mean 14.55, median 4.85, range 0.34–92.50 (EUR/MW)/h — verified from `afrr_capacity.csv`), within 12 % of the 16.36 implied by EUR 589 (= 1.5 × 16.36 × 24). It is presented as a level anchor, not a re-executed settlement. |
| C2 | "no June–Aug reBAP record" vs "142.53 EUR/MWh" | Both occurrences now state the record has since been retrieved (7,872 quarter-hours; OOS mean 142.53 vs DA 131.01) and that re-settlement is blocked by missing Study-A LP artifacts, not by data. |
| C3 | "enforces voltage feasibility" vs NR 0.926 | Conclusion and abstract now state "enforces LinDistFlow feasibility", with the NR residual shortfall (≈0.004 pu). A 0.937 pu LD setpoint was re-executed on all seven days: LD violations zero, NR V_min 0.9338–0.9344 every day, max LD–NR deviation 0.0032 pu, cost EUR 5.4/day (P1 mean −5109.00 → −5114.40 EUR/day). |
| C4 | "code upon acceptance" vs "not reproducible" | Limitations and Acknowledgment rewritten: Study-B artifacts recovered and every Study-B figure re-executed; Study-A numbers trace to archived result files and are labelled simulations on proxy prices pending artifact recovery; recovered code/data/results accompany the submission. |

## 2. P0 package — status

| Item | Status |
|---|---|
| P0-1, P0-2 (re-settle 14 OOS days on real aFRR + reBAP) | **Blocked** — Study-A LP artifacts were not recovered anywhere on disk (verified; `RUN_STRICT_ROLLING_OOS.py` is a stop-guard stub). Documented in §V-A, the Table III paragraph and §VIII. |
| P0-3 (text corrections: LD-form claims, +90 reframing) | Done (PHASE11 + PHASE13). |
| P0-4a (Study-A charge/discharge overlap) | Blocked (needs A-solver). |
| P0-4b (Study-B overlap) | Done: from archived LP solutions, no-aging models (B0/B1b/P0) overlap 8.53 and 2.46 MWh on 6/8 April; aging-priced models (B1a/B2/P1) exactly 0. |
| P0-5 (decompose 549) | Done: ΔDA = −448, ΔReserve = +589, ΔImbalance = +398, ΔDG = −10 (sum +549); with the imbalance spread removed the gap falls to EUR 151 (−73 %). |
| P0-6 (LD floor 0.937 + NR all days) | Done (see C3). |
| P0-8 (artifacts now) | Done — supplementary/repository with code, data panels, re-execution results, scripts. |

## 3. Other substantive items

- **B1** identification: flat proxy prices mean the objective sees only r↑ + r↓, so EUR 589 is effectively a capacity rent; POS/NEG-separated re-execution is stated as the identifying experiment.
- **B3** real measurement: on the OOS panel, reBAP averages 142.53 while proxy λ− averages 110.50 → gap +32.03 EUR/MWh (reBAP above λ− in 67.9 % of intervals; daily mean spans −2.8 … +99.3), so the sign of the ≈398 EUR/day imbalance channel is not stable and 151 is presented as the robust reading.
- **B5** "+90 EUR/day" reframed as the magnitude of the modeling error, not a market property; the 242→276 violation side-effect is highlighted.
- **N1** 23.5 vs 3.5 MWh reconciled: 23.5 is the total (charge + discharge) throughput reduction on 6 April (27.3 → 3.9 MWh/day); the discharge-only half that day is 11.1 MWh, and on 8 April the discharge-only B0−P1 reduction is 3.3 MWh, consistent with the EFC arithmetic (2.98 − 1.54) × 2.4 ≈ 3.5.
- **N2** Table XIII deleted (duplicate of Table II); no text references required renumbering.
- **N3** voltage-correction cost now given per removed bus-hour (≈ EUR 0.016).
- **F1** deliverability block printed per scenario (r↑ ≤ P_B − p_dis, r↓ ≤ P_B − p_ch, r↑ + r↓ ≤ Ṝ = 1.5 MW, E ≥ E_min + τ↑r↑/η_d, E + η_cτ↓r↓ ≤ E_max); τ↑, τ↓ declared unrecoverable with the solver file.
- **F2** the omission of the reserve-revenue term is now stated plainly, with the EUR 589 = 1.5 × 16.36 × 24 identity and the re-derivation requirement.
- **F3** CVaR statement corrected to the Rockafellar–Uryasev dual of E[Π] − β(E[Π] − CVaRα(Π)); the 77 EUR β-sweep is cited.
- **F4/F5/F7/F8** first-stage variables, squared-voltage nomenclature, S_b symbol and nomenclature row placement corrected.
- **P2** title changed to the reviewer's suggestion; Fig. 3 removed and all figures renumbered (11 figures); abstract rewritten to 235 words without the "ahead on every day" and "removes 276 bus-hours" claims.

## 4. Remaining open (honestly stated in the manuscript)

Re-settlement of the 14 OOS days on cleared aFRR/reBAP prices, the Study-A overlap report, numerical τ↑/τ↓ values, and a DM/HAC correction of the daily gain all require the unrecovered Study-A LP package. The manuscript says so explicitly rather than implying reproducibility.
