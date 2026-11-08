#!/usr/bin/env python3
"""Build IEEE-style DOCX from the manuscript content (not a naive HTML dump)."""
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsmap
from docx.oxml import OxmlElement

ROOT = Path("/home/user")
FIG = ROOT / "paper" / "figures"
OUT = ROOT / "paper" / "Hassanli_Abbasi_VPP_TwoStage_IEEE.docx"


def set_run_font(run, name="Times New Roman", size=10, bold=False, italic=False):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


def add_p(doc, text, size=10, bold=False, italic=False, align="justify", space_after=6, space_before=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = 1.15
    if align == "justify":
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    elif align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "right":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, italic=italic)
    return p


def heading(doc, text):
    p = add_p(doc, text, size=11, bold=True, align="center", space_before=12, space_after=8)
    return p


def subhead(doc, text):
    return add_p(doc, text, size=10.5, bold=True, italic=True, align="justify", space_before=8, space_after=4)


def eq(doc, text, num):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    set_run_font(r, size=10, italic=True)
    r2 = p.add_run("\t(" + num + ")")
    set_run_font(r2, size=10, italic=False)
    return p


def caption_fig(doc, text):
    return add_p(doc, text, size=9, align="justify", space_before=2, space_after=8)


def add_image(doc, path, width=6.3):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    run.add_picture(str(path), width=Inches(width))
    return p


def shade_header(cell):
    tc = cell._tePr if hasattr(cell, "_tePr") else cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), "F3F3F3")
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def set_cell(cell, text, bold=False, size=8):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    r = p.add_run(text)
    set_run_font(r, size=size, bold=bold)


def add_table(doc, headers, rows, caption):
    add_p(doc, caption, size=9, bold=True, align="center", space_before=8, space_after=3)
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(headers):
        set_cell(tbl.rows[0].cells[j], h, bold=True, size=8)
        shade_header(tbl.rows[0].cells[j])
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            set_cell(tbl.rows[i + 1].cells[j], val, bold=False, size=8)
    return tbl


def main():
    doc = Document()
    for sec in doc.sections:
        sec.top_margin = Cm(1.8)
        sec.bottom_margin = Cm(1.8)
        sec.left_margin = Cm(1.6)
        sec.right_margin = Cm(1.6)
        sec.page_width = Inches(8.5)
        sec.page_height = Inches(11)

    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(10)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")

    add_p(doc,
          "Risk-Aware Two-Stage Bidding and Voltage-Constrained Real-Time Correction for Battery-Integrated Virtual Power Plants under Degradation and Network Constraints",
          size=14, bold=True, align="center", space_after=8)
    add_p(doc, "Amir Hassanli and Ali Reza Abbasi", size=11, align="center", space_after=2)
    add_p(doc,
          "IEEE manuscript. IEEE 33-bus feeder (Baran–Wu). Market prices: SMARD DE-LU, 8 April 2026 (CC BY 4.0). Every reported euro is HiGHS kOptimal. Seed 20260827.",
          size=9, italic=True, align="center", space_after=10)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run("Abstract—")
    set_run_font(r, size=9, bold=True)
    r = p.add_run(
        "A day-ahead virtual-power-plant (VPP) bid that treats the distribution feeder as a copper plate can commit an export that real-time storage cannot support without violating voltage. This paper formulates a two-stage linear decision chain that keeps one aging model in both stages and puts LinDistFlow voltage into the real-time correction. Stage 1 is a mean–CVaR energy bid with a convex piecewise-linear cycle-depth cost after Xu and a linear throughput cost. Stage 2 freezes that bid and redispatches three inverters on the IEEE 33-bus radial feeder with reactive support and an undervoltage slack. Three programs are solved to proven optimality on SMARD DE-LU prices of 8 April 2026: an expected-value bid without aging (B0), a CVaR bid with aging but no voltage penalty (B2), and the proposed voltage-aware correction (P1). B2 leaves the minimum bus voltage at 0.873 pu and records 271 bus-hours below 0.93 pu. P1 raises the minimum to 0.93 pu, records zero violations, cuts battery throughput from 7.69 to 7.39 MWh, and pays 7 EUR of wholesale profit relative to B2. The paper writes the full constraint set, places the result against four clusters of prior work (bidding with degradation, safe multi-agent control, language-model dispatch, and false-data injection), and states without numerical claim the LLM, MARL, and FDIA layers that this run does not train."
    )
    set_run_font(r, size=9)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run("Index Terms—")
    set_run_font(r, size=9, bold=True)
    r = p.add_run(" Virtual power plant, CVaR, battery degradation, LinDistFlow, IEEE 33-bus, day-ahead bidding, voltage constraint, two-stage stochastic programming.")
    set_run_font(r, size=9, italic=True)

    add_table(
        doc,
        ["Symbol", "Meaning"],
        [
            ["t ∈ T, ω ∈ Ω", "Hour (|T|=24) and day-ahead scenario (|Ω|=K=12)"],
            ["n ∈ N, ℓ ∈ L", "Bus and branch of the IEEE 33-bus feeder"],
            ["i ∈ B, g ∈ G", "BESS (buses 6, 18, 33) and PV (buses 7, 24, 31)"],
            ["p^DA_t", "Day-ahead export at the substation (MW); negative = import"],
            ["p^ch, p^dis, q±", "BESS charge, discharge (MW) and reactive (MVAr)"],
            ["E_t, E^b", "Stored energy and nameplate (MWh)"],
            ["P_ℓ, Q_ℓ, v_n^2", "LinDistFlow flows (MW, MVAr) and squared voltage (pu)"],
            ["s_n,t", "Undervoltage slack (pu^2)"],
            ["δ+, δ−", "Short and long imbalance (MW)"],
            ["λ^DA, λ+, λ−", "DA price and two-price short/long imbalance (EUR/MWh)"],
            ["π_ω, α, β", "Scenario probability, CVaR tail 0.95, CVaR weight 0.05"],
            ["η, z_ω", "Rockafellar–Uryasev CVaR auxiliaries"],
            ["κ_m, w_m", "Xu PWL slope (EUR) and width of segment m"],
            ["c^deg", "Throughput aging, 12 EUR/MWh-throughput"],
            ["S_b, v_min", "Power base 10 MVA; voltage floor 0.93 pu"],
            ["r_t, e_n,t", "Formulated LLM risk score and FDIA residual (not trained)"],
            ["B0, B2, P1", "EV bid; CVaR+aging; CVaR+aging+voltage"],
        ],
        "NOMENCLATURE",
    )

    heading(doc, "I. INTRODUCTION")
    add_p(doc, "A virtual power plant (VPP) offers distributed generation, storage and flexible demand as one portfolio to the wholesale market [1]. Short-term trading of a stochastic resource is classically a two-stage program: a here-and-now energy bid, followed by a wait-and-see imbalance settlement [2], [3]. Risk-averse bids replace expected profit by a mean–CVaR combination [4], [5]. Storage that is dispatched against that bid ages; cycle-life and throughput costs have been attached to market LPs for a decade [6], [7]. What those LPs usually omit is the radial feeder that the batteries actually sit on.")
    add_p(doc, "That omission is the gap this paper measures. A copper-plate day-ahead bid can be tracked in real time only by pushing end-of-feeder voltages below the LinDistFlow band that a distribution operator will accept. A second, broader gap sits around that core. Risk-based VPP bids with degradation stop at the day-ahead clock [8], [9]. Safe multi-agent controllers enforce voltage under partial observability but do not bid [12], [13]. Language-model dispatch agents interpret text and produce schedules, but they are not wired to a CVaR bid or to a cell-aging row [14]. False-data-injection detectors protect measurements or bid quantities, but they are not closed with a feeder-aware correction that uses the same aging cost [15]–[17]. No published case that we can cite solves all four layers on one IEEE feeder with a proven LP. This manuscript does not claim to close that four-layer gap numerically. It closes the first coupling—day-ahead CVaR plus aging, connected to a voltage-constrained real-time LP with the same aging row—on the IEEE 33-bus feeder [10] with SMARD DE-LU prices, and it writes the remaining layers as a specification that this run does not train.")
    add_p(doc, "Contributions: (i) a mean–CVaR day-ahead energy bid with Xu-style convex cycle-depth cost [7] and linear throughput, on an aggregate of three Li-ion units; (ii) a 24-hour LinDistFlow [11] real-time LP on the Baran–Wu 33-bus feeder [10] with inverter reactive support and a 0.93 pu undervoltage slack; (iii) a same-day SMARD comparison of B0, B2 and P1 in which every euro is HiGHS kOptimal [20]; (iv) a related-work table that locates this coupling against bidding, degradation, multi-agent voltage control, language-model dispatch, and FDIA, without assigning numerical credit to layers that were not run.")

    heading(doc, "II. RELATED WORK")
    add_p(doc, "Prior VPP work falls into four clusters that only partly overlap. Table I marks six axes. A filled circle is a full treatment in the cited model; an open circle is a partial or survey treatment; a dash is absent.")
    subhead(doc, "A. Two-Stage Bidding and Battery Degradation")
    add_p(doc, "Morales, Conejo and Pérez-Ruiz set the two-stage template for a stochastic producer [2], [3]. Vahedipour-Dahraie et al. attach CVaR to VPP energy and reserve [5]. He et al. put cycle life into a storage bid [6]. Xu et al. replace rainflow with a convex piecewise-linear depth cost that an LP can carry [7]. Akkas and Cam combine risk-based VPP bidding with battery degradation and emissions, still at the day-ahead clock and without a feeder voltage row [8]. Li et al. co-optimise multiple VPPs with an active distribution network and a nonlinear capacity-fade transform, which is the closest published neighbour to this paper on the network axis, but the lower level is a revenue maximisation rather than a real-time LinDistFlow correction of a frozen wholesale bid [9]. The missing object is a single aging row that is paid both in the bid and in the voltage-aware correction.")
    subhead(doc, "B. Distributed and Safe Multi-Agent Control")
    add_p(doc, "Huang et al. coordinate EV charging stations as a VPP under partial distribution-network visibility with a Lagrangian-regularised MAPPO policy [12]. Li, Luo and Li learn community-VPP decisions with multi-agent deep RL [13]. Those controllers reduce voltage violations under limited observability. They do not submit a CVaR wholesale bid, and they do not carry Xu-style cycle depth in the reward. This paper’s Stage 2 is a centralised LP, not a trained multi-agent policy; we therefore do not tick the MARL column for the evaluated model.")
    subhead(doc, "C. Language-Model Agents in Power Dispatch")
    add_p(doc, "Cheng et al. introduce GAIA, an LLM specialised for power-dispatch tasks and scored on ElecBench [14]. In these works the language model is an interpreter or a scheduler, not a calibrated risk parameter inside a mean–CVaR LP, and none of them attach a cell-aging row or a LinDistFlow voltage slack. This run does not call a language model.")
    subhead(doc, "D. Cyber-Physical Security and FDIA")
    add_p(doc, "Singh et al. detect FDIA on VPP bid quantities and prices with an unsupervised autoencoder [15]. Wu et al. construct a topology-and-DG-output FDIA that bypasses bad-data detection on a VPP–distribution cyber-physical system [16]. Khamaneh et al. defend against coordinated N–K cyber-physical attacks with constrained RL and a projection layer [17]. Those detectors and defenders are not closed with a degradation-aware wholesale bid. This run does not inject an attack tape and does not train an autoencoder.")
    add_p(doc, "The four-cluster reading is therefore: bidding-with-degradation, safe MARL, LLM dispatch, and FDIA defence exist as separate literatures. The evaluated contribution of this paper occupies the first cluster plus a feeder voltage row. Table I records that occupancy honestly.")

    add_table(
        doc,
        ["Reference", "Two-stage bid", "Degrad.", "MARL / dist.", "Voltage", "LLM / text", "FDIA"],
        [
            ["Akkas and Cam, 2023 [8]", "●", "●", "—", "—", "—", "—"],
            ["Li et al., 2025 [9]", "●", "◐", "—", "●", "—", "—"],
            ["Huang et al., 2026 [12]", "—", "—", "●", "●", "—", "—"],
            ["Li, Luo and Li, 2024 [13]", "—", "—", "●", "◐", "—", "—"],
            ["Cheng et al. (GAIA) [14]", "—", "—", "—", "◐", "●", "—"],
            ["Singh et al., 2025 [15]", "—", "—", "—", "—", "—", "●"],
            ["Wu et al., 2025 [16]", "—", "—", "—", "◐", "—", "●"],
            ["Khamaneh et al., 2025 [17]", "—", "—", "◐", "●", "—", "●"],
            ["This paper (B0/B2/P1)", "●", "●", "—", "●", "—", "—"],
        ],
        "TABLE I. RELATED WORK. ● FULL, ◐ PARTIAL / SURVEY, — ABSENT. THIS PAPER’S ROW IS THE EVALUATED MODEL.",
    )

    heading(doc, "III. PLANT, MARKET AND DATA")
    add_p(doc, "The feeder is the Baran–Wu 33-bus radial system [10]: 12.66 kV, Sb = 10 MVA, peak load 3.715 MW + j2.300 MVAr. Three Li-ion BESS of 0.40 MW / 0.80 MWh sit at buses 6, 18 and 33. Three PV units of 0.60 MW sit at buses 7, 24 and 31. Round-trip efficiency is 0.95×0.95. SoC is box-constrained to 10–90% of nameplate and is cyclic at 50%. Fig. 1 is the siting. Fig. 2 is the two-stage chain that is actually solved.")
    add_image(doc, FIG / "Fig_feeder.png", 6.4)
    caption_fig(doc, "Fig. 1. IEEE 33-bus radial feeder used in Stage 2. BESS at buses 6, 18 and 33; PV at buses 7, 24 and 31. Bus 1 is the substation.")
    add_image(doc, FIG / "Fig_architecture.png", 6.4)
    caption_fig(doc, "Fig. 2. Evaluated decision chain. Stage 1 returns p^DA. Stage 2 tracks that bid on LinDistFlow with the same aging cost. B0, B2 and P1 differ only in which rows are active.")
    add_p(doc, "Day-ahead DE-LU prices and national solar and load shapes for 6–12 April 2026 come from SMARD via Energy-Charts [18], [19], CC BY 4.0. The operating day is 8 April 2026. Each PV unit follows the national solar shape scaled to 0.60 MW. Feeder load follows the national load shape scaled to the 33-bus peak. K = 12 day-ahead scenarios add Gaussian price noise (σ = 12 EUR/MWh) and uniform PV/load multipliers. Seed 20260827.")
    add_p(doc, "Imbalance is a two-price proxy of the day-ahead price,")
    eq(doc, "λ+_t = λ^DA_t + 18 + 0.12 |λ^DA_t|,    λ−_t = λ^DA_t − 10 − 0.08 |λ^DA_t|,", "1")
    add_p(doc, "clipped so that λ+ ≥ λ^DA+5 and λ− ≤ λ^DA−3. It is not reBAP and not a distribution LMP. Throughput aging is 12 EUR per MWh of charge plus discharge. Xu depth uses widths (0.20, 0.30, 0.30, 0.20) and slopes (8, 30, 60, 90) EUR per unit of daily SoC range over nameplate [7].")

    heading(doc, "IV. MATHEMATICAL FORMULATION")
    add_p(doc, "The evaluated model is two linear programs in sequence. Stage 1 is a here-and-now bid on an aggregate battery. Stage 2 is a wait-and-see correction on the three physical units and the feeder. Subsection E writes three layers that are specified and not trained.")
    subhead(doc, "A. Stage 1 — Mean–CVaR Day-Ahead Bid")
    add_p(doc, "Let Π_ω be scenario profit. With β ∈ [0,1] and tail α = 0.95 the Stage-1 program is")
    eq(doc, "max   (1−β) Σ_ω π_ω Π_ω + β CVaR_α(Π)", "2")
    add_p(doc, "Scenario profit is day-ahead revenue, two-price imbalance, minus throughput and Xu depth,")
    eq(doc, "Π_ω = Σ_t [ λ^DA_t,ω p^DA_t + λ−_t,ω δ−_t,ω − λ+_t,ω δ+_t,ω − c^deg (p^ch_t,ω + p^dis_t,ω) ] − Σ_m κ_m u_m,ω.", "3")
    add_p(doc, "Power balance at the substation, with net = PV − feeder peak × load factor, is")
    eq(doc, "p^DA_t + p^ch_t,ω + δ−_t,ω − p^dis_t,ω − δ+_t,ω = P^PV_t,ω − P^L,peak ℓ_t,ω.", "4")
    add_p(doc, "Stored energy on the aggregate battery, E^b = 3×0.80 MWh, obeys")
    eq(doc, "E_t,ω = E_t−1,ω + η_c p^ch_t,ω − p^dis_t,ω / η_d,    E_0,ω = E_24,ω = 0.5 E^b,", "5")
    eq(doc, "0.10 E^b ≤ E_t,ω ≤ 0.90 E^b,    0 ≤ p^ch_t,ω, p^dis_t,ω ≤ 3×0.40.", "6")
    add_p(doc, "The bid itself is boxed,")
    eq(doc, "−4 ≤ p^DA_t ≤ 4,    0 ≤ δ+_t,ω, δ−_t,ω ≤ 8.", "7")
    add_p(doc, "CVaR is the Rockafellar–Uryasev epigraph [4]. With auxiliary η ∈ ℝ and z_ω ≥ 0,")
    eq(doc, "CVaR_α(Π) = η − (1−α)^(−1) Σ_ω π_ω z_ω,    z_ω ≥ η − Π_ω.", "8")
    add_p(doc, "B0 sets β = 0 and drops the Xu and throughput rows. B2 and P1 set β = 0.05 and keep both aging rows. The first-stage bid p^DA is here-and-now: it does not depend on ω.")

    subhead(doc, "B. Cycle-Depth Aging After Xu")
    add_p(doc, "Let E^max_ω = max_t E_t,ω and E^min_ω = min_t E_t,ω. Daily depth as a fraction of nameplate is Σ_m u_m,ω = (E^max_ω − E^min_ω)/E^b, with 0 ≤ u_m,ω ≤ w_m and (w_m) = (0.20, 0.30, 0.30, 0.20). The convex cost Σ_m κ_m u_m,ω with increasing slopes κ = (8, 30, 60, 90) EUR is the LP-compatible surrogate of rainflow depth that Xu et al. justify from cell data [7]. It is not a rainflow extraction and it is not a calendar-aging term.")

    subhead(doc, "C. Stage 2 — LinDistFlow Real-Time Correction")
    add_p(doc, "Stage 2 freezes p^DA and redispatches the three BESS on the realised price, PV and load path. For each branch ℓ = (i → j) the linearised DistFlow of Farivar and Low [11], written in mixed MW / pu form with base S_b, is")
    eq(doc, "P_j,t = P^L_j,t − P^inj_j,t + Σ_{k ∈ C(j)} P_k,t,", "9")
    eq(doc, "Q_j,t = Q^L_j,t − Q^inj_j,t + Σ_{k ∈ C(j)} Q_k,t,", "10")
    eq(doc, "v^2_j,t = v^2_i,t − 2(r_ℓ P_ℓ,t + x_ℓ Q_ℓ,t)/S_b,    v^2_1,t = 1.", "11")
    add_p(doc, "Injection at a BESS bus is P^inj = p^dis − p^ch and Q^inj = q+ − q−. PV injection is active only. The 2/S_b scaling is required because P, Q are in MW while r, x are in per-unit on 10 MVA. Inverter headroom is the linear outer approximation")
    eq(doc, "p^ch_i,t + p^dis_i,t + q+_i,t + q−_i,t ≤ 1.25 p^bess_i.", "12")
    add_p(doc, "Per-unit SoC dynamics copy (5)–(6) on each physical unit, with a cyclic terminal at 50%. The substation tracks the frozen bid through imbalance,")
    eq(doc, "−P_{1→2,t} + δ+_t − δ−_t = p^DA_t.", "13")
    add_p(doc, "P1 adds an undervoltage slack s_n,t ≥ 0,")
    eq(doc, "v^2_n,t + s_n,t ≥ v_min^2,    v_min = 0.93,", "14")
    add_p(doc, "and a penalty 2500 EUR/pu^2 on s. B0 and B2 omit that penalty, so they may sit below 0.93 pu. The textbook IEEE 33-bus minimum without DER is about 0.913 pu; 0.93 pu is therefore a lift, not the ANSI C84.1 0.95 band. A hard 0.95 cut with P-only BESS is infeasible on this siting (unconstrained LinDistFlow minimum 0.873 pu). The Stage-2 objective is")
    eq(doc, "min  Σ_t [ λ+_t δ+_t − λ−_t δ−_t + c^deg Σ_i (p^ch_i,t + p^dis_i,t) + 2500 Σ_n s_n,t ].", "15")
    add_p(doc, "Realised wholesale profit, the number reported in Table II, does not include the slack penalty:")
    eq(doc, "Π^rt = Σ_t λ^DA_t p^DA_t + Σ_t (λ−_t δ−_t − λ+_t δ+_t) − c^deg Σ_{i,t} (p^ch_i,t + p^dis_i,t).", "16")

    subhead(doc, "D. What Is Linear and What Is Not")
    add_p(doc, "With LinDistFlow, PWL depth, CVaR epigraph and the linear inverter proxy, both stages are LPs. Rainflow extraction, AC power flow, and a neural policy are not in the evaluated programs. HiGHS [20] returns a kOptimal certificate or the euro is discarded.")

    subhead(doc, "E. Formulated Layers That This Run Does Not Train")
    add_p(doc, "The remainder of this section is a specification, not a result. No language model is called, no autoencoder is trained, and no MARL policy is updated. The equations are written so that the related-work gap in Section II is operational rather than rhetorical.")
    add_p(doc, "An LLM risk score, used only in Stage 1 and never in the real-time loop, would map pre-gate news and policy text to r_t ∈ [0,1],")
    eq(doc, "r_t = f_LLM(news_t, policy_t, market-report_t),", "17")
    add_p(doc, "and reweight scenario probabilities toward the tail when r_t is high. A decision-focused calibration would train the map from text embeddings to r_t against realised trading regret. That calibration is not performed here.")
    add_p(doc, "An FDIA screen on a measurement or a bid component x_n,t would be a reconstruction residual")
    eq(doc, "x̂_n,t = AE(x_n,t),    e_n,t = ||x_n,t − x̂_n,t||_2,", "18")
    add_p(doc, "with x flagged if e_n,t > θ and replaced by a LinDistFlow state estimate before Stage 2. Precision and recall of that screen are not reported, because no attack tape is injected.")
    add_p(doc, "A safe multi-agent controller would treat each BESS as an agent with local observation o_i,t ⊆ {v_n, P_n : n ∈ N_i^loc}, reward")
    eq(doc, "R_i,t = −c^deg |p_i,t| − C^Xu_i,t − λ^imb |p^DA_t − Σ_i p_i,t| − κ max(0, v_min − v_n,t),", "19")
    add_p(doc, "and a QP safety projection onto (11)–(14) after the policy head [12], [17]. No such policy is trained: Stage 2 remains the LP (15).")

    heading(doc, "V. SOLUTION METHOD AND EXPERIMENT")
    add_p(doc, "Both LPs are built in sparse coefficient form and passed to scipy.optimize.linprog(method=\"highs\") [20]. Presolve is on; time limit 60 s. A row is recorded only if success is true.")
    add_p(doc, "B0: β = 0, no Xu, no throughput in Stage 1, Stage 2 without the 2500 s term. B2: β = 0.05, α = 0.95, Xu plus throughput in Stage 1, Stage 2 without the 2500 s term. P1: the B2 first stage (identical p^DA), Stage 2 with (14) and the 2500 s term. Voltage statistics are recorded for all three, including B0 and B2 where the slack is inactive.")

    heading(doc, "VI. RESULTS")
    add_p(doc, "Table II is the recorded settlement on 8 April 2026. Fig. 3 is the first-stage bid. B2 and P1 share p^DA; the CVaR-plus-aging bid changes day-ahead energy by 0.23 MWh relative to B0 (more import) and costs 4 EUR of wholesale profit. Voltage is unchanged between B0 and B2: both sit at 0.873 pu and accumulate more than 270 bus-hours below 0.93 pu. P1 keeps the B2 bid and changes only the real-time P/Q dispatch. Minimum voltage rises to 0.93 pu. Violations drop to zero. Throughput falls by 0.30 MWh. Wholesale profit falls by 7 EUR relative to B2.")
    add_table(
        doc,
        ["Model", "DA MWh", "DA rev.", "Imb.", "Aging", "Profit", "vmin", "Viol.", "Thr. MWh"],
        [
            ["B0", "−63.41", "−6074", "+68.8", "92.3", "−6097", "0.873", "275", "7.69"],
            ["B2", "−63.65", "−6083", "+74.5", "92.3", "−6101", "0.873", "271", "7.69"],
            ["P1", "−63.65", "−6083", "+64.0", "88.6", "−6108", "0.930", "0", "7.39"],
        ],
        "TABLE II. REALISED SETTLEMENT, 8 APRIL 2026, IEEE 33-BUS. EVERY ROW IS HIGHS kOptimal, SEED 20260827.",
    )
    add_image(doc, FIG / "Fig_bids.png", 3.4)
    caption_fig(doc, "Fig. 3. Day-ahead export bid. Negative values are imports at the substation. B2 and P1 share the first-stage program.")
    add_image(doc, FIG / "Fig_profit.png", 3.4)
    caption_fig(doc, "Fig. 4. Realised wholesale profit (16). P1 pays 7 EUR versus B2 to enforce 0.93 pu.")
    add_p(doc, "The 7 EUR is not the aging bill. Aging falls from 92.3 to 88.6 EUR because the voltage penalty reduces cycling. The profit drop is extra imbalance from a more constrained real-time set (imbalance revenue +74.5 to +64.0 EUR). Fig. 5 is aging versus bus-hour violations. Fig. 6 is the hourly minimum voltage: B2 tracks unconstrained LinDistFlow; P1 sits on the 0.93 pu floor except for two midday hours where PV already lifts the feeder.")
    add_image(doc, FIG / "Fig_aging_volt.png", 3.4)
    caption_fig(doc, "Fig. 5. Aging cost and bus-hour voltage violations. P1 zeros the violations and slightly cuts throughput.")
    add_image(doc, FIG / "Fig_voltage.png", 3.4)
    caption_fig(doc, "Fig. 6. Hourly minimum bus voltage. B2 tracks the unconstrained LinDistFlow. P1 sits on the 0.93 pu floor. The ANSI 0.95 band is not claimed.")

    heading(doc, "VII. DISCUSSION")
    add_p(doc, "On this day the aging row moves the bid by a fraction of a megawatt-hour. The voltage row does not move the bid at all: P1 and B2 share p^DA. What it moves is the real-time Q support and a small cut in throughput. That is the measured content of “connect bidding to control.” The first stage can stay an energy CVaR; the second stage must see the feeder.")
    add_p(doc, "The plant is a net importer (DA energy ≈ −63 MWh) because feeder peak 3.715 MW exceeds 1.8 MW of PV plus 1.2 MW of BESS power. Negative profit is therefore not a solver failure; it is the wholesale cost of serving the feeder load at DE-LU prices, net of PV and of a small amount of storage shifting. The scientific claim is the 7 EUR / 271-violation trade-off, not a profitable arbitrage.")
    add_p(doc, "Relative to Table I, the result sits next to Akkas and Cam [8] (risk plus degradation, no feeder) and Li et al. [9] (VPP–ADN co-optimisation, no frozen wholesale bid tracked by LinDistFlow). It does not sit next to Huang et al. [12] or Cheng et al. [14] numerically, because those columns were not run.")

    heading(doc, "VIII. LIMITATIONS AND THE UNTRAINED LAYERS")
    add_p(doc, "One operating day. LinDistFlow, not a full AC power flow. Voltage floor 0.93 pu, not 0.95 pu. Three identical BESS. K = 12. Imbalance is a two-price proxy, not reBAP. Prices are SMARD DE-LU, not a distribution locational marginal price. No MARL training, no LLM agent, no FDIA autoencoder, no GNN power-flow surrogate, no IEEE 69-bus case, no week roll. Equations (17)–(19) are a specification. Reporting Precision/Recall, MARL learning curves, or an LLM ablation on this day would be an invention, and it is not done.")

    heading(doc, "IX. CONCLUSION")
    add_p(doc, "A CVaR day-ahead bid with cycle-depth aging and a LinDistFlow real-time correction were solved on the IEEE 33-bus feeder with SMARD prices of 8 April 2026. Aging without voltage leaves 271 bus-hours under 0.93 pu. Adding a voltage slack penalty clears those hours, lifts vmin from 0.873 to 0.93 pu, cuts throughput by 0.30 MWh, and costs 7 EUR. The coupling that matters on this day is the feeder correction, not a richer first-stage aging row. Closing the remaining three clusters of Table I—safe multi-agent execution, a calibrated LLM risk score, and an FDIA screen—requires trained models and an attack tape that this manuscript does not contain.")

    heading(doc, "ACKNOWLEDGMENT")
    add_p(doc, "Prices © Bundesnetzagentur | SMARD.de [18] via Energy-Charts [19], CC BY 4.0. Linear programs: HiGHS [20]. Feeder: Baran and Wu [10]. Cycle-depth PWL: Xu et al. [7]. CVaR epigraph: Rockafellar and Uryasev [4].")

    heading(doc, "REFERENCES")
    refs = [
        "D. Pudjianto, C. Ramsay, and G. Strbac, “Virtual power plant and system integration of distributed energy resources,” IET Renew. Power Gener., vol. 1, no. 1, pp. 10–16, Mar. 2007.",
        "J. M. Morales, A. J. Conejo, and J. Pérez-Ruiz, “Short-term trading for a wind power producer,” IEEE Trans. Power Syst., vol. 25, no. 1, pp. 554–564, Feb. 2010.",
        "A. J. Conejo, M. Carrión, and J. M. Morales, Decision Making Under Uncertainty in Electricity Markets. New York, NY, USA: Springer, 2010.",
        "R. T. Rockafellar and S. Uryasev, “Optimization of conditional value-at-risk,” J. Risk, vol. 2, no. 3, pp. 21–41, 2000.",
        "M. Vahedipour-Dahraie, H. Rashidizadeh-Kermani, M. Shafie-Khah, and J. P. S. Catalão, “Risk-averse optimal energy and reserve scheduling for virtual power plants incorporating demand response programs,” IEEE Trans. Smart Grid, vol. 12, no. 2, pp. 1405–1415, Mar. 2021.",
        "G. He, Q. Chen, C. Kang, P. Pinson, and Q. Xia, “Optimal bidding strategy of battery storage in power markets considering performance-based regulation and battery cycle life,” IEEE Trans. Smart Grid, vol. 7, no. 5, pp. 2359–2367, Sep. 2016.",
        "B. Xu, J. Zhao, T. Zheng, E. Litvinov, and D. S. Kirschen, “Factoring the cycle aging cost of batteries participating in electricity markets,” IEEE Trans. Power Syst., vol. 33, no. 2, pp. 2248–2257, Mar. 2018.",
        "O. P. Akkas and E. Cam, “Risk-based optimal bidding and operational scheduling of a virtual power plant considering battery degradation cost and emission,” Adv. Elect. Comput. Eng., vol. 23, no. 2, pp. 19–28, 2023.",
        "Q. Li, F. Dong, G. Zhou, C. Mu, Z. Wang, J. Liu, P. Yan, and D. Yu, “Co-optimization of virtual power plants and distribution grids: Emphasizing flexible resource aggregation and battery capacity degradation,” Appl. Energy, vol. 377, Art. no. 124519, Jan. 2025.",
        "M. E. Baran and F. F. Wu, “Network reconfiguration in distribution systems for loss reduction and load balancing,” IEEE Trans. Power Del., vol. 4, no. 2, pp. 1401–1407, Apr. 1989.",
        "M. Farivar and S. H. Low, “Branch flow model: Relaxations and convexification—Part I,” IEEE Trans. Power Syst., vol. 28, no. 3, pp. 2554–2564, Aug. 2013.",
        "C. Huang, J. Fan, W. Wang, and H. Wang, “Safe decentralized operation of EV virtual power plant with limited network visibility via multi-agent reinforcement learning,” arXiv:2604.03278, Mar. 2026.",
        "X. Li, F. Luo, and C. Li, “Multi-agent deep reinforcement learning-based autonomous decision-making framework for community virtual power plants,” Appl. Energy, vol. 360, Art. no. 122813, Apr. 2024.",
        "Y. Cheng, H. Zhao, X. Zhou, J. Zhao, Y. Cao, and C. Yang, “GAIA — A large language model for advanced power dispatch,” arXiv:2408.03847, Aug. 2024.",
        "K. N. Singh, A. K. Goswami, N. B. D. Chudhury, H. A. Shuaibu, and T. S. Ustun, “Enhancing cybersecurity in virtual power plants by detecting network based cyber attacks using an unsupervised autoencoder approach,” Sci. Rep., vol. 15, Art. no. 32374, 2025.",
        "S. Wu, J. Gong, S. Xiao, J. Yang, and X. Su, “A novel FDIA model for virtual power plant cyber–physical systems based on network topology and DG outputs,” Energies, vol. 18, no. 7, Art. no. 1597, 2025.",
        "S. Mazaheri Khamaneh, T. Wu, W. Sun, and C. Chen, “Real-time defense against coordinated cyber-physical attacks: A robust constrained reinforcement learning approach,” arXiv:2509.10999, Sep. 2025.",
        "Bundesnetzagentur, “SMARD – Strommarktdaten.” [Online]. Available: https://www.smard.de",
        "B. Burger, “Energy-Charts,” Fraunhofer ISE. [Online]. Available: https://www.energy-charts.info",
        "Q. Huangfu and J. A. J. Hall, “Parallelizing the dual revised simplex method,” Math. Program. Comput., vol. 10, pp. 119–142, 2018.",
    ]
    for i, ref in enumerate(refs, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.6)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        p.paragraph_format.space_after = Pt(3)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(f"[{i}]  {ref}")
        set_run_font(r, size=8.5)

    add_p(doc, "All euros are HiGHS kOptimal (seed 20260827). Code: src/vpp_two_stage.py, src/ieee33.py, src/run_case.py. Equations (17)–(19) have no associated number in Table II.",
          size=8.5, italic=True, space_before=8)

    doc.save(OUT)
    print("wrote", OUT, "bytes", OUT.stat().st_size)


if __name__ == "__main__":
    main()
