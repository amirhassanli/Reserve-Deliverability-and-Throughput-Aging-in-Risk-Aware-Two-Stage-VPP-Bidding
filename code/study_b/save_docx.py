#!/usr/bin/env python3
"""Persist the current IEEE manuscript as DOCX with real tables and figures."""
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(r"C:\Users\Mahboobian\Documents\Default Project\_draft\ws_run")
FIG = ROOT / "paper" / "figures"
OUT = ROOT / "paper" / "Hassanli_Abbasi_VPP_TwoStage_IEEE.docx"


def font(run, size=10, bold=False, italic=False):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


def p(doc, text, size=10, bold=False, italic=False, align="justify", before=0, after=6):
    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(before)
    para.paragraph_format.space_after = Pt(after)
    para.paragraph_format.line_spacing = 1.15
    para.alignment = {
        "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
        "center": WD_ALIGN_PARAGRAPH.CENTER,
        "right": WD_ALIGN_PARAGRAPH.RIGHT,
        "left": WD_ALIGN_PARAGRAPH.LEFT,
    }[align]
    r = para.add_run(text)
    font(r, size=size, bold=bold, italic=italic)
    return para


def heading(doc, text):
    return p(doc, text, size=11, bold=True, align="center", before=12, after=8)


def sub(doc, text):
    return p(doc, text, size=10.5, bold=True, italic=True, before=8, after=4)


def eq(doc, text, n):
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(4)
    para.paragraph_format.space_after = Pt(4)
    r = para.add_run(text)
    font(r, size=10, italic=True)
    r2 = para.add_run("    (" + str(n) + ")")
    font(r2, size=10)
    return para


def shade(cell):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), "F3F3F3")
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def cell(c, text, bold=False, size=8):
    c.text = ""
    para = c.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_after = Pt(0)
    r = para.add_run(str(text))
    font(r, size=size, bold=bold)


def table(doc, caption, headers, rows):
    p(doc, caption, size=9, bold=True, align="center", before=8, after=3)
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(headers):
        cell(tbl.rows[0].cells[j], h, bold=True, size=8)
        shade(tbl.rows[0].cells[j])
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            cell(tbl.rows[i + 1].cells[j], v, size=8)
    return tbl


def fig(doc, name, cap, width=6.2):
    path = FIG / name
    if not path.exists():
        p(doc, "[missing " + name + "]", size=8, italic=True, align="center")
        return
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(6)
    run = para.add_run()
    run.add_picture(str(path), width=Inches(width))
    p(doc, cap, size=8.5, align="justify", after=8)


def main():
    doc = Document()
    for sec in doc.sections:
        sec.top_margin = Cm(1.8)
        sec.bottom_margin = Cm(1.8)
        sec.left_margin = Cm(1.6)
        sec.right_margin = Cm(1.6)
        sec.page_width = Inches(8.5)
        sec.page_height = Inches(11)
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(10)

    p(doc, "A Degradation-Aware Two-Stage Framework for Secure VPP Bidding and Feeder-Constrained Dispatch",
      size=14, bold=True, align="center", after=8)
    p(doc, "Amir Hassanli and Ali Reza Abbasi", size=11, align="center", after=2)
    p(doc, "IEEE manuscript. Option B: provable two-stage LPs. B3/P2/Full not evaluated. Seed 20260827. SMARD DE-LU 6–12 April 2026. Every euro HiGHS kOptimal, LP gap 0.",
      size=9, italic=True, align="center", after=10)

    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = para.add_run("Abstract—")
    font(r, size=9, bold=True)
    r = para.add_run(
        " This paper is a two-stage, degradation-aware, feeder-constrained bidding study. It is not a trained LLM–MARL–GNN stack. "
        "Stage 1 is a mean–CVaR energy bid with Xu piecewise-linear cycle depth and linear throughput. Stage 2 tracks the cleared bid "
        "on the IEEE 33-bus feeder with LinDistFlow, inverter P and Q, and the same aging cost. Sign convention: p^ch ≥ 0 charge, "
        "p^dis ≥ 0 discharge, p^DA > 0 export. Negative profit is feeder-service cost. Table III filled rows (B0, B1, B2, P1) are "
        "7-day SMARD means, 42/42 HiGHS kOptimal. Aging, not CVaR, moves expected cost by about 90 EUR/day. Voltage safety zeros "
        "276±50 bus-hours/day below 0.93 pu at 4.3 EUR/day (Wilcoxon p=0.016). P-only cannot hold 0.93 pu; only P–Q holds 0.95 pu "
        "(+52 EUR on 8 April). Newton–Raphson gives P1 mean |ΔV|=0.17% and AC vmin=0.926 versus LinDistFlow 0.930 (ε_v=0.004). "
        "A physics residual screen has stealth recall 0.90. Rows B3, P2 and Full are specified and left empty."
    )
    font(r, size=9)
    para = doc.add_paragraph()
    r = para.add_run("Index Terms—")
    font(r, size=9, bold=True)
    r = para.add_run(" Virtual power plant, CVaR, battery degradation, LinDistFlow, two-stage stochastic programming, voltage constraint, residual FDIA.")
    font(r, size=9, italic=True)

    table(doc, "NOMENCLATURE",
          ["Symbol", "Description"],
          [
              ["A. Indices and Sets", ""],
              ["t ∈ T", "Hour, |T|=24, Δt=1 h"],
              ["ω ∈ Ω", "DA scenario, K=12, π_ω=1/K"],
              ["n ∈ N", "Bus, |N|=33, slack n=1"],
              ["ℓ=(i→j) ∈ L", "Branch, |L|=32"],
              ["b ∈ B", "BESS buses {6,18,33}"],
              ["g ∈ G", "PV buses {7,24,31}"],
              ["m ∈ M", "Xu PWL segment, |M|=4"],
              ["B. Parameters", ""],
              ["S_b, V_b", "10 MVA, 12.66 kV"],
              ["P^b_b, E^b_b", "(0.30,0.40,0.50) MW / (0.60,0.80,1.00) MWh"],
              ["η_c, η_d", "0.95 / 0.95"],
              ["c^deg", "12 EUR/MWh throughput"],
              ["β, α", "CVaR weight 0.05, tail 0.95"],
              ["w_m, κ_m", "Xu widths (0.20,0.30,0.30,0.20); slopes (8,30,60,90) EUR"],
              ["v_min, ρ_s", "0.93 pu floor; 2500 EUR/pu² slack penalty"],
              ["ε_v", "NR margin 0.004 pu"],
              ["C. Stage-1 variables", "p^DA_t, p^ch, p^dis, E, δ±, u_m, η, z_ω"],
              ["D. Stage-2 variables", "p^ch_b,t, q±, P_ℓ, Q_ℓ, v²_n,t, s_n,t"],
              ["E. Abbreviations", "B0–P1 evaluated; B3/P2/Full not evaluated"],
          ])

    heading(doc, "I. INTRODUCTION")
    p(doc, "A VPP must bid day-ahead and track that bid on a voltage-constrained feeder while paying cell aging. This manuscript is Option B: a provable two-stage LP. Table III filled rows have HiGHS euros. B3, P2 and Full do not.")
    heading(doc, "II. RELATED WORK")
    p(doc, "Akkas and Cam [8] attach degradation to a risk bid without a feeder row. Li et al. [9] co-optimise VPPs with an ADN. Xu et al. [7] give the PWL depth. Evaluated occupancy: bidding, aging, voltage, residual FDIA.")
    heading(doc, "III. PLANT")
    p(doc, "IEEE 33-bus, 12.66 kV, Sb=10 MVA, peak 3.715 MW+j2.300 MVAr. Heterogeneous BESS at 6/18/33. PV 0.60 MW at 7/24/31. Sign: p^ch≥0 charge, p^dis≥0 discharge, p^DA>0 export. SMARD DE-LU 6–12 April 2026. K=12.")
    eq(doc, "λ+_t = λ^DA_t + 18 + 0.12|λ^DA_t|,    λ−_t = λ^DA_t − 10 − 0.08|λ^DA_t|", 1)
    fig(doc, "Fig_feeder.png", "Fig. 1. IEEE 33-bus feeder. BESS 6, 18, 33; PV 7, 24, 31.")

    heading(doc, "IV. COMPLETE CONSTRAINTS (src/vpp_two_stage.py)")
    p(doc, "E^Σ=2.40 MWh, P^Σ=1.20 MW. Stage 1 aggregate battery.")
    eq(doc, "max  (1−β) Σ_ω π_ω Π_ω + β [η − (1−α)^(−1) Σ_ω π_ω z_ω]", 8)
    eq(doc, "Π_ω = Σ_t [λ^DA p^DA + λ− δ− − λ+ δ+ − c^deg(p^ch+p^dis)] − Σ_m κ_m u_m,ω", 9)
    eq(doc, "z_ω ≥ η − Π_ω,  z_ω ≥ 0,  −4 ≤ p^DA_t ≤ 4", 10)
    eq(doc, "p^DA + p^ch + δ− − p^dis − δ+ = P^PV − 3.715 ℓ", 11)
    eq(doc, "E_t = E_{t−1} + η_c p^ch − p^dis/η_d,  E_0=E_24=0.5 E^Σ", 12)
    eq(doc, "0.10 E^Σ ≤ E ≤ 0.90 E^Σ,  0 ≤ p^ch, p^dis ≤ P^Σ", 13)
    eq(doc, "Σ_m u_m = (E^max − E^min)/E^Σ,  0 ≤ u_m ≤ w_m", 14)
    eq(doc, "min Σ_t [λ+ δ+ − λ− δ− + c^deg Σ_b (p^ch+p^dis) + 2500 Σ_n s_n,t]", 15)
    eq(doc, "E_b,t = E_b,t−1 + η_c p^ch_b − p^dis_b/η_d,  cyclic 50%", 16)
    eq(doc, "p^ch+p^dis+q++q− ≤ 1.25 P^b_b", 18)
    eq(doc, "P_ℓ − Σ_child P = P^L ℓ − P^PV − (p^dis−p^ch)", 19)
    eq(doc, "v²_j = v²_i − 2(r P + x Q)/S_b,  v²_1=1", 21)
    eq(doc, "−P_{1→2} + δ+ − δ− = p^DA", 22)
    eq(doc, "v²_n + s_n ≥ v_min²,  s_n ≥ 0   (P1, P0)", 23)
    p(doc, "Solver: scipy.optimize.linprog(method=\"highs\"). Success ⇒ kOptimal, recorded gap 0.")

    heading(doc, "V. RESULTS (REAL HIGHS NUMBERS)")
    table(doc,
          "TABLE III. ABLATION. FILLED = 7-DAY MEAN, kOptimal. B1=code B1b. EMPTY=not evaluated.",
          ["Model", "LLM", "CVaR", "Aging", "V", "FDIA", "Profit", "Worst", "Viol/d", "Aging"],
          [
              ["B0", "N", "N", "N", "N", "N", "−5195", "−8828", "241", "170"],
              ["B1", "N", "Y", "N", "N", "N", "−5195", "−8829", "242", "169"],
              ["B2", "N", "Y", "Y", "N", "N", "−5105", "−8816", "276", "69"],
              ["B3", "Y", "Y", "Y", "N", "N", "—", "—", "—", "—"],
              ["P1", "N", "Y", "Y", "Y", "N", "−5109", "−8827", "0", "67"],
              ["P2", "Y", "Y", "Y", "Y", "N", "—", "—", "—", "—"],
              ["Full", "Y", "Y", "Y", "Y", "Y", "—", "—", "—", "—"],
          ])
    p(doc, "B0→B1 (CVaR only) does not move mean profit. B1→B2 (aging) +90 EUR/day. B2→P1 (voltage) −4 EUR/day, zeros violations, Wilcoxon p=0.016, n=7. 42/42 kOptimal, gap 0.")
    fig(doc, "Fig_profit.png", "Fig. 4. 8 April profit.", 3.4)
    fig(doc, "Fig_week_viol.png", "Fig. 5. Daily violations below 0.93 pu.", 3.4)
    fig(doc, "Fig_pareto.png", "Fig. 6. Service cost versus aging.", 3.4)
    table(doc, "TABLE IV. 8 APRIL 2026. Π = DA REV. + IMB. − AGING.",
          ["M", "DA rev.", "Imb.", "Aging", "Profit", "|V|min", "Viol"],
          [
              ["B0", "−6067", "+61", "172", "−6178", "0.873", "243"],
              ["B1", "−6080", "+73", "169", "−6176", "0.873", "245"],
              ["B2", "−6083", "+75", "92", "−6101", "0.873", "281"],
              ["P1", "−6083", "+63", "89", "−6109", "0.930", "0"],
          ])
    table(doc, "TABLE V. INVERTER ABLATION ON THE P1 BID, 8 APRIL.",
          ["Floor", "P", "Q", "|V|min", "Viol", "Profit"],
          [
              ["0.93", "Y", "N", "0.921", "61", "−6215"],
              ["0.93", "N", "Y", "0.930", "0", "−6638"],
              ["0.93", "Y", "Y", "0.930", "0", "−6109"],
              ["0.95", "Y", "N", "0.916", "330", "−6258"],
              ["0.95", "N", "Y", "0.942", "63", "−6638"],
              ["0.95", "Y", "Y", "0.950", "0", "−6161"],
          ])
    fig(doc, "Fig_heatmap.png", "Fig. 7. |V| heatmap, B2 vs P1.", 6.2)
    fig(doc, "Fig_busvolt.png", "Fig. 8. All-bus |V| at the B2 worst hour.", 3.4)
    fig(doc, "Fig_pq.png", "Fig. 9. P-only misses the 0.93 pu floor.", 3.4)
    table(doc, "TABLE VI. NEWTON–RAPHSON VS LINDISTFLOW, 8 APRIL. 24/24 NR CONVERGED.",
          ["M", "LD vmin", "NR vmin", "NR mean |ΔV|", "NR max |ΔV|"],
          [
              ["B2", "0.873", "0.867", "0.0029", "0.0068"],
              ["P1", "0.930", "0.926", "0.0017", "0.0038"],
          ])
    table(doc, "TABLE VII. PHYSICS RESIDUAL FDIA, n=120. NOT AN AUTOENCODER.",
          ["Tape", "Prec.", "Rec.", "F1", "ΔΠ if missed"],
          [
              ["V bias +0.05 pu", "1.00", "1.00", "1.00", "—"],
              ["V ramp", "1.00", "1.00", "1.00", "—"],
              ["V stealth +0.008 pu", "1.00", "0.90", "0.95", "—"],
              ["V coordinated", "1.00", "1.00", "1.00", "—"],
              ["Bid +0.40 MW", "—", "—", "—", "−226"],
              ["Price +25 EUR/MWh", "—", "—", "—", "−1565"],
          ])
    fig(doc, "Fig_rainflow.png", "Fig. 10. Throughput aging versus Xu (Xu saturates).", 3.4)
    fig(doc, "Fig_voltage.png", "Fig. Hourly min |V|, B2 vs P1.", 3.4)
    fig(doc, "Fig_sensitivity.png", "Fig. 11. P1 tornado.", 3.4)

    heading(doc, "VI. DISCUSSION")
    p(doc, "Table III is the paper. CVaR without aging is a null. Aging is ~90 EUR/day. Voltage zeros 0.93 pu violations. B3/P2/Full are empty. Seven April days are not two seasons. Residual FDIA is an upper bound against a physics twin. Code: src/vpp_two_stage.py, src/ieee33.py, src/run_experiments.py.")
    heading(doc, "VII. CONCLUSION")
    p(doc, "Aging belongs in both objectives. Voltage safety is a real-time P–Q job. All filled euros are HiGHS kOptimal, gap 0.")
    heading(doc, "ACKNOWLEDGMENT")
    p(doc, "SMARD / Energy-Charts CC BY 4.0. HiGHS. Xu 2018. Rockafellar–Uryasev 2000. Baran–Wu 1989.")
    heading(doc, "REFERENCES")
    refs = [
        "[1] D. Pudjianto, C. Ramsay, and G. Strbac, IET RPG, 2007.",
        "[4] R. T. Rockafellar and S. Uryasev, J. Risk, 2000.",
        "[7] B. Xu et al., IEEE Trans. Power Syst., 2018.",
        "[8] O. P. Akkas and E. Cam, AECE, 2023.",
        "[10] M. E. Baran and F. F. Wu, IEEE Trans. Power Del., 1989.",
        "[11] M. Farivar and S. H. Low, IEEE Trans. Power Syst., 2013.",
        "[18] Bundesnetzagentur, SMARD, https://www.smard.de",
        "[19] B. Burger, Energy-Charts, Fraunhofer ISE.",
        "[20] Q. Huangfu and J. A. J. Hall, Math. Program. Comput., 2018.",
    ]
    for ref in refs:
        p(doc, ref, size=8.5, after=3)
    p(doc, "Full reference list in the HTML manuscript. Archive: results/week_results.csv (B1=B1b).",
      size=8.5, italic=True)
    doc.save(OUT)
    print("wrote", OUT, OUT.stat().st_size)


if __name__ == "__main__":
    main()
