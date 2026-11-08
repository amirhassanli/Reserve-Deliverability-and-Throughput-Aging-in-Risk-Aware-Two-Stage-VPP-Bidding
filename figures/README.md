# Figures

Two sets, both from this project.

## `manuscript/` — exact figures embedded in the PHASE15 manuscript

Extracted byte-for-byte from
`manuscript/Hassanli_Abbasi_VPP_Bidding_IEEE_PHASE15_FINAL_SUBMISSION.docx`.
Figure numbers match the manuscript after the Review-5 renumbering (old Fig. 3, the
58-day KDE panel, was removed).

| File | Manuscript caption |
|---|---|
| `fig01.png` | Forecast versus realized SMARD price series, 19 August 2026. |
| `fig02.png` | Joint daily-block scenario fans, K = 50. |
| `fig03.png` | Expected profit versus realized settlement, and the gap relative to B0 (IS: in-sample scenario distribution). |
| `fig04.png` | Expected-profit-to-CVaR slope and tail gap across configurations. |
| `fig05.png` | Empirical CDF of the K = 50 joint-scenario profits. |
| `fig06.png` | First-stage day-ahead energy position and realized DE-LU price. |
| `fig07.png` | Battery SoC; P1 retains overnight energy to support reserve deliverability. |
| `fig08.png` | P1 two-sided reserve position (upward positive, downward negative); B0 and B2 sell no reserve. |
| `fig09.png` | Daily realized profit of B0, B2, and P1 over the 14-day strict rolling OOS window (6–19 August 2026). |
| `fig10.png` | Daily realized-profit advantage of P1 relative to B0. |
| `fig11.png` | Real September 2026 settlement data used as adjacent-month anchors (reBAP, aFRR/FCR/mFRR). |

## `source/` — figure sources rendered by `code/study_b/make_figures.py`

Lower-resolution working renders (17 PNGs) produced during PHASE7. The manuscript embeds
higher-DPI re-renders of the same content, so these files are **not** byte-identical to the
embedded ones; `manuscript/` is authoritative for what is in the paper.
