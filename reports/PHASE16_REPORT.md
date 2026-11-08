# PHASE16 — consistency closure — 2026-11-08

Output: `article 6\Hassanli_Abbasi_VPP_Bidding_IEEE_PHASE16_FINAL.docx` (+ `_SINGLECOLUMN`).
Copies in `VPP_Article6_Project\manuscript\`.

## What this phase fixed (all defects found by a full cross-reference audit)

| # | Defect found in PHASE15 | Fix |
|---|---|---|
| 1 | **Dangling figure reference**: §V (P68) still began "Fig. 3 presents the kernel density estimates … a 58-day diagnostic window", but Fig. 3 no longer exists as the KDE panel — after the renumbering Fig. 3 is the profit-vs-settlement figure | Paragraph rewritten: the KDE panel is declared omitted (day-retention rule not reconstructable) and the marginals are described in text; the 58-day subsample is defined against the 82-day span, the 2024–2025 copula window and the 14-day OOS window |
| 2 | **Second dangling reference** in Limitations: "the day-retention rule behind the 58-day KDE window of Fig. 3 … Fig. 3 is reported as descriptive only" | Reworded to "that panel is omitted from the figure set rather than reported" |
| 3 | Reviewer's P2-2 objection survived in the body: "is the best configuration on all 14 days", "consistently dominates … across all 14 unseen days", "the uniformly positive bars" | Claims restated as the exact-test statement they are: all 14 paired differences against B0 are positive, which is what p = 2/2¹⁴ encodes; editorial framing removed |
| 4 | Fig. 9 / Fig. 10 captions repeated the same unqualified claims ("P1 is highest on every day", "all 14 values are positive") | Captions now state the fact plus its exact-test identity (p = 2/2¹⁴) |
| 5 | Abstract 235 words (target ≈200) | Rewritten to **194 words**; keeps the decomposition (549/589/398/−448/−10), 563/day (4.8 %), p = 1.2×10⁻⁴, 90/day, 242→276, 4.3/day, 0.937 pu/NR, and the proxy caveat |

## Verification after the edits

- Paragraphs 166 | Tables **31** | Figures **11** | oMath 68 + oMathPara 50 (unchanged, no equation touched)
- Figure captions present exactly 1–11; every "Fig. N" in the text resolves to a caption that exists
  (Fig. 3 now referenced only by the profit-vs-settlement paragraph and its caption)
- Table captions I–XII contiguous; every "Table R" used in the text has a caption
- September anchors intact: 148.65 ×4, 2,784 ×4, 2249.80, 102.15, 13.01, 14.55, 142.53
- Study-A/B numbers intact: 549 (×5), 563.44, 589, 0.9338, +32.03, "8.53 and 2.46", "27.3 MWh"
- Title unchanged (reviewer's suggested title from PHASE15)

## Remaining open (unchanged, documented in the manuscript)

Re-settling the 14 OOS days on cleared aFRR/reBAP, the Study-A charge/discharge overlap report,
numeric τ↑/τ↓ values, and a DM/HAC correction of the daily gain all require the unrecovered
Study-A LP package (`RUN_STRICT_ROLLING_OOS.py` is a stop-guard stub; no solver artifacts exist on
disk). The manuscript states this explicitly in §V-A, the Table III paragraph and §VIII.
