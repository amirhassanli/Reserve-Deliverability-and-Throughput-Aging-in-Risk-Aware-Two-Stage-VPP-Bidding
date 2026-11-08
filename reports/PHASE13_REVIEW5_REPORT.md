# PHASE13 — Review-5 (Major Revision) P0 text package — 2026-11-07

Output: `article 6\Hassanli_Abbasi_VPP_Bidding_IEEE_PHASE13_REVIEW5.docx`
(+ `_SINGLECOLUMN.docx`). Copies placed in `VPP_Article6_Project\manuscript\`.
Integrity: 168 paras / 33 tables / 12 images / 69 oMath + 50 oMathPara — unchanged.
Sept anchors intact: 148.65 ×4, 2,784 ×4, 2249.80, 102.15, 13.01.

## Applied (all numbers verified from real files)

| ID | Review item | Fix |
|----|-------------|-----|
| C1 / P0-7 | §V-A "no aFRR file" vs Table XII "14.55" | §V-A now states Sept download lacks the file, **and** that the cleared German aFRR capacity series for the OOS window was retrieved separately (regelleistung.net, 168 hourly POS/NEG rows; mean 14.55, median 4.85, range 0.34–92.50 (EUR/MW)/h — verified from `afrr_capacity.csv`), within 12% of the 16.36 implied by 589 (=1.5×16.36×24); used as a **level anchor, not a re-executed settlement** |
| C2 / P0-7 | §VIII "no June–Aug reBAP retained" vs "142.53" | Both occurrences now state the record **has been retrieved** (7,872 quarter-hours; OOS mean 142.53 vs DA 131.01) and that re-settlement is blocked by missing **LP artifacts**, not missing data |
| P0-5 / B2 | Table III decomposition hidden | §Table-III paragraph now prints ΔDA=−448, ΔReserve=+589, ΔImbalance=+398, ΔDG-cost=−10 (verified against Table III cells), **sum +549**, plus the sentence: with imbalance spread removed the gap falls to **EUR 151 (−73%)** |
| C4 / P0-8 | "deposit upon acceptance" vs "historical unvalidated" | Limitations and Acknowledgment rewritten: Study-B artifacts recovered + **every Study-B figure re-executed**; Study-A numbers trace to archived files pending artifact recovery; code/data/results **accompany the submission** |
| C3 | "enforces voltage feasibility" | Conclusion: now "enforces **LinDistFlow** feasibility … NR verification shows residual ≈0.004 pu shortfall"; Abstract likewise qualified |
| B4 | "ahead on every day" | Abstract qualified: "under the fixed proxy prices … largely a consequence of the fixed-price proxy (§VI-E)" |
| B5 / P1-2 | "+90 EUR/day" | Reframed: "removing the aging cost **overstates** realizable profit by ≈90 EUR/day — magnitude of the modeling error, not a market property" (101→savings; 242→276 LD violations kept) |
| N3 | "|profit| %" normalization | Voltage cost now "≈ EUR 0.016 per removed bus-hour (276/day)" |
| F3 | CVaR identity mis-stated | Corrected to Rockafellar-Uryasev dual of E[Π]−β(E[Π]−CVaRα(Π)); β=0.05 shifts objective by 5% of the mean–tail spread; full β sweep 0–0.50 = 77 EUR (para VI-K) cited; two-preprint overlap sentence merged |
| F2 (partial) | objective omits λᴿr term | §IV-C now states the truth: solver-reality unverifiable because Study-A artifacts unrecovered; 589 = settlement-reported (1.5×16.36×24); fixing the objective is part of the re-derivation program |

## NOT done (blocked / next pass)

- **P0-1 / P0-2 re-settlement of 14 OOS days** on real hourly aFRR + real reBAP: blocked — Study-A LP artifacts not recovered anywhere (verified across all zips). Documented as such in §V-A, §V-A(Table III para), §VIII.
- **P0-6** LD floor 0.937 + NR all-days re-run: Study-B code IS available (ws_run) — next; requires a full re-solve, separate phase.
- **P0-4** Study-A charge/discharge overlap: blocked (needs A-solver); Study-B overlap reporting possible.
- P1/P2 bands (N1 23.5-vs-3.5 MWh reconciliation, N2 Table XIII removal, B1 POS/NEG split, DM/HAC, abstract 200-word rewrite, title, Fig.3 removal, Chudhury counter verified correct): next pass.
