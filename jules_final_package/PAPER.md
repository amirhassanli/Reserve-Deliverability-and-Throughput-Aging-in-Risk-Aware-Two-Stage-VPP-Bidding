# Reserve Rent, Error Dependence, and Feeder Voltage: A Controlled Ablation of VPP Bidding Components

**Authors:** Amir Hassanli and Ali Reza Abbasi

## Abstract

Virtual power plants (VPPs) must commit day-ahead positions before price, load, and renewable output are known. This paper reports two linear-programming studies on SMARD DE-LU data, kept separate because they use different plants. A mean–CVaR energy-and-reserve bidding study for a 5 MW-class portfolio uses shaped proxy reserve and two-price imbalance prices, so its results are simulations rather than cleared-market revenue. The settlement decomposition attributes nearly all of the P1−B0 gap to reserve capacity (ΔReserve +589, ΔImbalance +398, ΔDA −448, ΔDG −10; net +549 on 19 August 2026; EUR 151 without the imbalance proxy). Over 14 chronological out-of-sample days P1 exceeds B0 by EUR 563/day (4.8%, Wilcoxon p = 1.2×10⁻⁴); joint versus independent error sampling changes P1 by EUR 6, and energy-only CVaR is indistinguishable from B0 (p = 0.33). A seven-day IEEE 33-bus feeder ablation shows that omitting aging pricing overstates realizable profit by about EUR 90/day and shifts violations from 242 to 276 LinDistFlow bus-hours/day; real-time P–Q correction removes them at EUR 4.3/day, with a 0.937 pu setpoint verified by Newton–Raphson. A physics-residual screen detects voltage-channel attacks but not bid or price manipulation. Reserve and imbalance prices remain proxies; both windows are short.

**Index Terms:** Battery degradation, conditional value-at-risk, day-ahead bidding, LinDistFlow, out-of-sample validation, reserve deliverability, virtual power plant.


## I. Introduction

A virtual power plant (VPP) aggregates photovoltaic (PV) and wind generation, battery storage, flexible demand, and small dispatchable units into a single market-facing portfolio [1]. In a day-ahead market the VPP must submit its position before renewable output, load, and prices are realized; the physical portfolio then absorbs whatever occurs. This gives the familiar two-stage structure of a here-and-now commitment followed by recourse [2], [3]. Conditional value-at-risk (CVaR) [4] is the standard linearizable device for limiting tail outcomes in such problems and has been applied to joint energy and reserve scheduling of VPPs [5].

Two modeling questions are frequently conflated: how the joint forecast errors of price, load, and renewable output are represented, and which products the portfolio may sell. A third concerns the physical layer. Battery degradation [6]–[8] and the voltage limits of the feeder that hosts the resources [9]–[11] can change both the value and the feasibility of a schedule. This paper separates these questions and reports a controlled attribution of each mechanism.

Two LP studies are reported. Study A (market bidding) compares expected-value bidding (B0), CVaR bidding with independent error draws (B1), CVaR bidding with joint daily error blocks (B2), and CVaR bidding with an SoC-feasible reserve product (P1) on SMARD DE-LU data, with a single-day settlement decomposition and a 14-day strictly chronological rolling out-of-sample (OOS) evaluation. Study B (feeder ablation) uses the IEEE 33-bus feeder and a disjoint seven-day window to isolate the effects of CVaR, throughput aging, real-time P–Q voltage correction, and first-stage feeder awareness. The two studies use structurally different plants, data windows and objectives and are NOT pooled; Study A addresses market bidding on SMARD DE-LU data, while Study B is a separate feeder ablation on the IEEE 33-bus system and should be read as an independent technical appendix. feeder-layer models carry an F- prefix (F-B0, F-B1, F-B2, F-P1, F-S1V) to prevent confusion with the market-bidding models.

An evidence-first standard is adopted: a claim is reported only where the corresponding experiment was solved to optimality (HiGHS status kOptimal). Extensions often combined with this core—distributionally robust optimization (DRO) [12], conformal calibration of price intervals [13], safe multi-agent reinforcement learning [14], large language model (LLM) interfaces [15], and neural false-data-injection (FDIA) detectors [16]—are not trained or evaluated here.

The contributions are: (1) a mean–CVaR day-ahead energy LP and a companion SoC-feasible reserve LP evaluated on the same plant and data; (2) an isolation experiment separating the economic effect of joint-versus-independent error dependence from that of a deliverable reserve product; (3) a strict chronological rolling-OOS validation with paired inference over 14 unseen days; (4) a controlled feeder ablation quantifying CVaR, throughput aging, real-time P–Q correction, and a first-stage feeder-aware bid (F-S1V); and (5) a physics-residual FDIA screen that reports both what it detects and what it cannot.


## II. Related Work


### A. Risk-Aware VPP Bidding

Stochastic VPP bidding under renewable and price uncertainty is usually formulated as a scenario-based two-stage program [2], [3]. Vahedipour-Dahraie et al. [5] formulate a two-stage risk-constrained VPP problem spanning day-ahead, real-time, and spinning-reserve markets with demand response, Xiao et al. [17] extend CVaR-constrained bidding to multiple reserve services and mobile storage, and Sadeghi et al. [18] pair a deep-learning forecast with day-ahead energy and frequency-regulation bidding. Akkas and Cam [8] combine CVaR, emissions, and battery cost in a day-ahead VPP model. Yang et al. [19] show that a renewable-based VPP retains part of its controllable capacity for self-balancing before committing any of it externally — the distinction between internally retained flexibility and a sold reserve product that this paper makes operational. At larger scale, mean-field co-optimization couples stochastic bidding with frequency-regulation aggregation [20]. DRO protects against ambiguity in the scenario distribution, typically through a Wasserstein ball around the empirical measure [12], at the price of added conservatism and computation; the evaluated core of this paper remains CVaR-based.


### B. Battery Degradation

Degradation enters market scheduling through cycle-life and performance-based-regulation costs [6] and through a piecewise-linear convex cycle-aging cost [7]; degradation is also included in VPP bidding [8] and in VPP–distribution-grid co-optimization [9]. What is rarely isolated experimentally is how the cost is charged—throughput versus a state-of-charge (SoC) range proxy—on the same plant and data. Section VI-L does so.


### C. Network-Aware Operation

Co-optimizing VPPs with active distribution networks changes the feasible flexibility envelope [9]. For tractability, such studies rely on linearized radial power flow; the LinDistFlow model used here traces to Baran and Wu [10] and the branch-flow formulation of Farivar and Low [11].


### D. Uncertainty Calibration and Extensions

Conformal prediction has been used to calibrate day-ahead and balancing-market price intervals [13]. Singh et al. [21] integrate renewable forecasting with carbon-market strategies in a risk-aware VPP bidding model. Safe decentralized VPP control under limited network visibility has been studied with multi-agent reinforcement learning [14], LLMs have been proposed for power-dispatch tasks [15], and autoencoder-based FDIA detection for VPP telemetry has been reported [16]. A multi-temporal formulation additionally links day-ahead commitments to real-time regulation response under uncertainty [22]. These directions are compatible with the framework studied here, but none is trained or evaluated in this paper. Table I positions the present study.

TABLE ICompact Literature Placement


| Study | Uncertainty | Risk | Reserve / data |
| --- | --- | --- | --- |
| Vahedipour-Dahraie et al. [5] | Scenario-based, independent | CVaR | Energy + spinning reserve; test VPP |
| Akkas and Cam [8] | RES scenarios | CVaR | DA energy; battery cost |
| Gao and Kleywegt [12] | Wasserstein ambiguity set | Worst-case expectation | — |
| O’Connor et al. [13] | Conformal intervals | Forecast only | DA and balancing prices |
| This work | Joint vs. independent daily error blocks | Linear CVaR | SoC-feasible reserve; SMARD |


## III. Plants and Market Setting


### A. Market-Bidding Plant (Study A)

The price-taking VPP is a 5 MW-class portfolio: 4 MW PV, 2 MW wind, a 2.5 MW/5 MWh battery (efficiency η = 0.95, SoC 10–90%), and a 1.8 MW dispatchable gas unit with a marginal cost of 68 EUR/MWh. The CVaR weight is β = 0.05, the tail parameter is α = 0.95, and K = 50 scenarios are retained; a convergence check over K = 50/100/200 is reported as a limitation because 50 scenarios leave only about 2.5 draws in the 5% tail used for CVaR. Imbalance settlement uses a two-price form whose escalating magnitudes are documented against real September 2026 reBAP data (Section V-A), and reserve capacity is priced from shaped day-ahead quantities, with real September 2026 mFRR/FCR capacity clears as the documented anchor scale (Section V-A). Demand response appears in the algebra but is never activated, so no result concerns its value.


### B. Feeder Plant (Study B)

The radial IEEE 33-bus feeder [10] runs at 12.66 kV on a 10 MVA base with a peak load of 3.715 MW + j2.300 MVAr. Three batteries at buses 6, 18, and 33 are rated 0.30/0.60, 0.40/0.80, and 0.50/1.00 MW/MWh (aggregate 1.20 MW, 2.40 MWh). PV of 0.60 MW nameplate sits at buses 7, 24, and 31. Efficiencies are 0.95/0.95, SoC is limited to 10–90% with a cyclic 50% boundary, and inverter headroom is |P| + |Q| ≤ 1.25 Prated. This plant is deliberately smaller and structurally different from that of Study A.


## IV. Mathematical Formulation

Let t index hours, ω index scenarios with probability πω, and let β denote the CVaR weight (λ always denotes a price). Sign convention: PtDA > 0 is export; Pt,ωch, Pt,ωdis ≥ 0 are battery charge and discharge; δt,ω-, δt,ω+ ≥ 0 are long and short imbalance.

Scenario Profit, Imbalance Prices, and CVaR


$$
\Pi_{t,\omega} = \lambda^{\mathrm{DA}}_{t,\omega} P^{\mathrm{DA}}_t + \lambda^-_{t,\omega} \delta^-_{t,\omega} - \lambda^+_{t,\omega} \delta^+_{t,\omega} - C^{\mathrm{deg}}_{t,\omega} \tag{1}
$$


$$
\lambda^+_t = \lambda^{\mathrm{DA}}_t + 18 + 0.12 |\lambda^{\mathrm{DA}}_t|, \quad \lambda^-_t = \lambda^{\mathrm{DA}}_t - 10 - 0.08 |\lambda^{\mathrm{DA}}_t| \tag{2}
$$

whereas the feeder study uses flat clips λ+ ≥ λDA + 5 and λ− ≤ λDA − 3. Loss is defined as L = -Pi (negative scenario profit) and CVaR_alpha(L) is the Rockafellar-Uryasev conditional value-at-risk of that loss; the objective max (1-beta) E[Pi] + beta (eta - (1-alpha)^-1 E[zeta]) with z >= eta - Pi, z >= 0 is the Rockafellar-Uryasev dual of the blend (1-beta) E[Pi] + beta CVaR_alpha(Pi), i.e. E[Pi] - beta (E[Pi] - CVaR_alpha(Pi)): beta scales the gap between mean profit and its lower-tail conditional value at risk, rather than placing a 5 percent weight on a loss distribution as such — with beta = 0.05 the risk term shifts the objective by only five percent of that spread. Thus beta = 0 recovers expected-value bidding; the full beta sweep 0–0.50 moves F-P1 profit by only 77 EUR (Section VI-K), so the risk weight is inert at the operating point. The mean-CVaR objective in Rockafellar-Uryasev form [4] is the blend above. The symbol η inside the CVaR block is the value-at-risk threshold at level α and is unrelated to the battery efficiencies ηc, ηd; the dual roles are kept distinct by context and by the nomenclature.


$$
\max \quad (1-\beta) \sum_\omega \pi_\omega \Pi_\omega + \beta \left[ \eta - \frac{1}{1-\alpha} \sum_\omega \pi_\omega z_\omega \right] \tag{3}
$$


$$
z_\omega \ge \eta - \Pi_\omega, \quad z_\omega \ge 0 \tag{4}
$$

so that β = 0 recovers expected-value bidding. The first-stage variables are the day-ahead position pDA_t and, in P1, the two-sided reserve position r↑, r↓; all remaining variables (charging, SoC, imbalance, voltage slack, CVaR auxiliaries) are scenario-dependent recourse.


### B. Market Balance and Battery Dynamics


$$
P^{\mathrm{DA}}_t + P^{\mathrm{ch}}_{t,\omega} + \delta^-_{t,\omega} - \delta^+_{t,\omega} - P^{\mathrm{dis}}_{t,\omega} = P^{\mathrm{PV}}_{t,\omega} - P^{\mathrm{LD}}_{t,\omega} \tag{5}
$$


$$
E_{t,\omega} = E_{t-1,\omega} + \eta_c P^{\mathrm{ch}}_{t,\omega} - \frac{P^{\mathrm{dis}}_{t,\omega}}{\eta_d}, \quad E_{0,\omega} = E_{24,\omega} \tag{6}
$$

with SoC and power bounds on Et,ω, Pch, and Pdis. Aging is charged to throughput rather than inferred from the SoC range,


$$
C^{\mathrm{deg}} = c^{\mathrm{deg}} (P^{\mathrm{ch}}_t + P^{\mathrm{dis}}_t) \Delta t \tag{7}
$$

with cdeg = 12 EUR/MWh in the feeder study. A four-segment Xu-type piecewise-linear daily-depth cost [7] (widths 0.20/0.30/0.30/0.20, slopes 8/30/60/90 EUR) is evaluated alongside as a secondary proxy.


### C. SoC-Feasible Reserve (P1)

In P1 the two-sided reserve position (upward r↑, downward r↓) is co-optimized with the energy position and must remain physically deliverable in every scenario: each side is restricted jointly by battery power and stored-energy headroom and by dispatchable-unit headroom, so a reserve bid cannot be created by declaring availability alone. Downward reserve is energy-absorbing, and the reserve-capacity revenue in Table III combines both sides. In the reported formulation the deliverability block per scenario ω and hour t is: r↑ ≤ P_B − p_dis, r↓ ≤ P_B − p_ch, r↑ + r↓ ≤ Ṝ (sold quantity 1.5 MW in the reported run), E ≥ E_min + τ↑ r↑/η_d, and E + η_c τ↓ r↓ ≤ E_max; the delivery-window shares τ↑, τ↓ ≤ Τ are carried as constants of the unrecovered solver file and will be printed with the re-derived program (Section VIII). This is a deliverability constraint, not an asset-outage N−1 security criterion. On formulation scope: the display equation (1) states the energy-side settlement identity that evaluates every model's realized profit; it does not restate the reserve-capacity revenue term, which enters the P1 objective through the reserve positions r↑/r→ and r↓ priced at the shaped capacity price of Section III, and whose settlement decomposition Table III reports. As printed, the objective omits the reserve-revenue term; whether the solved program priced the reserve positions economically cannot be verified from this text because the Study-A solver artifacts were not recovered. The EUR 589 line of Table III is the settlement-reported revenue (1.5 MW × 16.36 (EUR/MW)/h × 24 h), and pinning the objective to that term with the printed deliverability constraints is part of the re-derivation program in Section VIII.


### D. Feeder Layer (Study B)

Stage 2 minimizes real-time imbalance cost, throughput aging, and an undervoltage slack penalty,


$$
\min \quad \sum_t \left[ \lambda^+_t \delta^+_t - \lambda^-_t \delta^-_t + c^{\mathrm{deg}} \sum_b (p^{\mathrm{ch}}_{b,t} + p^{\mathrm{dis}}_{b,t}) + \rho_s \sum_n s_{n,t} \right] \tag{8}
$$

subject to unit-level battery dynamics and the LinDistFlow relations [10], [11]


$$
P_{i,t} - \sum_{k \in \mathcal{C}(i)} P_{k,t} = P^{\mathrm{L,pk}}_i \ell_t - P^{\mathrm{PV}}_{i,t} - (p^{\mathrm{dis}} - p^{\mathrm{ch}})\big|_{b=i} \tag{9}
$$


$$
Q_{i,t} - \sum_{k \in \mathcal{C}(i)} Q_{k,t} = Q^{\mathrm{L,pk}}_i \ell_t - (q^+ - q^-)\big|_{b=i} \tag{10}
$$


$$
v_{j,t}^2 = v_{i,t}^2 - 2 \frac{r_{i,j} P_{ij,t} + x_{i,j} Q_{ij,t}}{S_b}, \quad v_{1,t}^2 = 1.0 \tag{11}
$$


$$
v_{n,t} + s_{n,t} \ge (v^{\mathrm{op}})^2, \quad s_{n,t} \ge 0 \tag{12}
$$

where lt is the load factor, ρs = 2500 EUR/pu², and inverter headroom is pch+pdis+q++q− ≤ 1.25 Pb. In (9)–(12) the variable v is the squared voltage magnitude: the 0.93 pu operational floor is imposed as v ≥ 0.93², the slack s is expressed in squared-voltage units and charged at ρs = 2500 EUR per pu², and constraint (12) as printed below is the linear form v + s ≥ vop² that the LP formulation solves (the earlier second-power notation on v and s was a typesetting slip). The operational floor vop = 0.93 pu (0.95 pu in the inverter ablation) is distinct from the wide numerical box 0.80–1.15 pu on |V| that keeps LinDistFlow defined. Reported profit excludes ρs; where the optimum has s = 0 it equals the full Stage-2 objective. Rows that retain violations (P-only, Table IX) were optimized with the penalty but are reported without it and are therefore a theoretical ablation. F-S1V copies (9)–(12) into each of the K = 12 first-stage scenarios while keeping one common pDA.


### E. Rolling Out-of-Sample Protocol

Let D be the ordered set of target days and Hd-1 the information available strictly before day d. Calibration, first-stage decisions, and settlement are


$$
\theta_d = \mathcal{F}\big(\{y_t : t \in \mathcal{H}_{d-1}\}\big), \quad x^*_d = \arg\max_x \mathbb{E}_\omega [\Pi(x; \theta_{d,\omega})] - \text{risk penalty} \tag{13}
$$


$$
\Pi^{\mathrm{real}}_d = \mathcal{S}(x^*_d, y_d, \lambda_d), \quad \Delta_d = \Pi^{\mathrm{real}}_{d,A} - \Pi^{\mathrm{real}}_{d,B} \tag{14}
$$

with no component of yd entering θd. Paired daily differences Δd support a paired t-statistic, the Wilcoxon signed-rank test, and bootstrap confidence intervals obtained by resampling the paired differences directly, because both models share the same daily realizations.


## V. Data and Experimental Design


### A. Study A

Data are Bundesnetzagentur/SMARD DE-LU observations [23] obtained via Energy-Charts [24] (CC BY 4.0). All series are national aggregates scaled to a 5 MW-class portfolio (proxy), not metered VPP telemetry; DST transitions and 15-min to hourly aggregation are handled as described in the Data Dictionary (supplementary). Copula and autocorrelation diagnostics use 1 January 2024–30 September 2025; settlement and rolling evaluation use 1 June–21 August 2026, with 19 August 2026 as the isolation day and 6–19 August 2026 as the 14-day OOS window. Joint scenarios are daily block bootstraps; independent scenarios draw a different historical day for each of price, load, PV, and wind, retaining marginals but removing cross-variable dependence. A Student-t copula fitted on the 2024–2025 window gives nu = 18.55. This value alone does not prove tail independence: a formal tail-dependence test (upper/lower tail coefficients, Gaussian vs. Student-t comparison on out-of-sample joint extremes) is required before claiming a heavy-tail explanation is unsupported. Information sets I_d: the public aFRR capacity tender calendar for 1-30 September 2026 [26] confirms the decision chronology the simulation assumes - for delivery day d, gate opens d-7 10:00 CEST, gate closes d-1 09:00 CEST, allocation is published d-1 09:30 CEST, traded as six 4-hour block products (POS/NEG). In the model all stage-1 variables for day d therefore depend only on information released at or before the corresponding day-ahead gate closure, and stage-2 recourse uses day-of realization only. The scenario-construction and price-shaping rules of the two-price imbalance proxy (eq. (2)) are specified in the Data Dictionary supplement; the LP implementations, fixed seeds and settlement scripts are available from the author on reasonable request.

Real-market anchor (1-30 September 2026). Four public settlement series covering the month were retrieved on 2026-10-12 from Netztransparenz [27] and regelleistung.net [26], in 15-minute resolution, and verified against the raw Netzreglung exports (2,880 intervals; the 96 intervals of 30 September are published as N.A. and excluded): the reBAP imbalance price (mean 148.65 EUR/MWh over the 2,784 published intervals of 1-29 September; range -7208.55 to +4993.15 EUR/MWh; |reBAP| >= 100 EUR/MWh in 66.3% of intervals), the anonymised aFRR energy-market bid lists (allocated-capacity-weighted average price of cleared positive-energy bids 2249.80 EUR/MWh; daily means 1580-2989 EUR/MWh), the cleared FCR capacity settlement for Germany (102.15 EUR/MW mean day price; 38.49-442.00 EUR/MW) and the cleared mFRR capacity margins for Germany (13.01 (EUR/MW)/h mean marginal). Recomputing these statistics from the September export archived with this submission reproduces the reBAP figures exactly (2,784 intervals, mean 148.65, range −7208.55 to +4993.15 EUR/MWh, |reBAP| ≥ 100 in 66.3%) and the mFRR marginal mean exactly (13.01 (EUR/MW)/h); the archived FCR export contains 180 German four-hour settlement products averaging 90.10 EUR/MW (9.03–210.42, daily means 59.70–123.88), so the 102.15 EUR/MW day-price aggregate quoted here is retained from the retrieval records rather than recomputed from that export, and the anonymised aFRR energy bid lists behind the 2249.80 EUR/MWh mean were not archived. Historical IGCC settlement prices (2011-2022, Netzregelverbund) were exported as background context only. The September download itself contains no cleared aFRR capacity result file, so no aFRR capacity price is claimed for September; the cleared aFRR capacity settlement for Germany was retrieved separately for the 6-19 Aug 2026 OOS evaluation window (regelleistung.net [26], 168 hourly POS/NEG rows): the German average capacity price averages 14.55 (EUR/MW)/h (median 4.85, range 0.34-92.50), within 12% of the 16.36 (EUR/MW)/h implied by the EUR 589 proxy (= 1.5 MW x 16.36 x 24). Because the Study-A LP artifacts were not recovered in this revision, the 14 OOS days could not be re-settled on this hourly series; it is reported as an empirical plausibility anchor for the flat proxy level, not as a re-executed settlement (Section VIII). Fig. 11 visualises the three settlement series. The simulated reserve product is two-sided (r↑/r↓): the FCR clear in Fig. 11(c) is a symmetric two-sided product and the mFRR clear is traded in both POS and NEG directions, so the capacity panels document the two-sided capacity-price scale relevant to the offer, while the reserve-revenue proxy itself is shaped from day-ahead quantities (Section III). These adjacent-month prices document the magnitude regime the two-price imbalance proxy assumes, but they do not cover the June-August 2026 evaluation window; all reported results still use the shaped proxies (the OOS-window aFRR capacity clearing above is a realism anchor for the level, not a re-executed settlement).

Fig. 11. Real September 2026 settlement data used as adjacent-month anchors: (a) 15-minute reBAP price for 1–29 September (2,784 published intervals; 30 September published as N.A.), with the extreme of +4993/−7209 EUR/MWh marked; (b) allocated-capacity-weighted daily mean price of cleared positive aFRR energy bids (monthly mean 2249.80 EUR/MWh, dashed); (c) daily-mean cleared capacity prices for Germany: FCR settlement, mFRR marginal, and the flat 77 EUR/MW interruptible-load price. Sources: [26], [27].

Eight configurations share the isolation day: H0 (point-forecast bid), B0, B1, B2, P1-ind (reserve, independent errors), P1 (reserve, joint blocks), and two perfect-foresight bounds, PF-energy and PF-reserve. B1 and B2 are also evaluated on a common joint scenario set. The rolling evaluation carries forward B0, B2, and P1. Because the numerical program uses the day-ahead decision and settlement only, and the public SMARD extract has no intraday order book, intraday re-trading is not modeled.


### B. Study B

Study B uses the 6–12 April 2026 window, disjoint from Study A, with K = 12 equally weighted first-stage scenarios. F-B0 is deterministic with neither CVaR nor aging in the optimizer (Study B is a separate feeder ablation; its profits are negative because the objective is net cost of serving a fixed load, not trading profit); F-B1 adds CVaR; F-B2 adds throughput aging; F-P1 adds the real-time voltage floor. Programs that are specified but not evaluated (FDIA-hardened and learning-augmented variants) are not reported. All 42 weekly programs were solved with HiGHS [25] to kOptimal at zero gap. Attack tapes (voltage bias, ramp, stealth, coordinated; bid manipulation; price spoofing) are evaluated independently over n = 120 instances for the voltage-channel tapes.


## VI. Results


### A. Reserve-Value Isolation, 19 August 2026

Table II reports the isolation day. Energy-only CVaR (B1, B2) lands within EUR 35/day of B0, whereas both reserve-capable models (P1-ind, P1) are about EUR 550/day above it. Switching P1 from joint blocks to independent errors changes realized profit by only EUR 6/day, so on this day the dependence structure is not the economic lever; the reserve product is. Perfect-foresight energy adds only EUR 117/day to B0, perfect-foresight reserve reaches EUR 11,657/day, and P1 comes within EUR 170/day of it. The point-forecast heuristic H0 trails B0 by EUR 906/day.

TABLE IIReserve-Value Isolation, 19 August 2026 (EUR/day)


| Model | Errors | Reserve | E[π] | CVaR | Realized |
| --- | --- | --- | --- | --- | --- |
| H0 (heuristic) | Point forecast | No | 10,677 | 9,010 | 10,032 |
| B0 (expected value) | Mean | No | 11,498 | 9,986 | 10,938 |
| B1 (CVaR) | Independent | No | 11,505 | 10,014 | 10,971 |
| B2 (CVaR) | Joint | No | 11,508 | 10,027 | 10,965 |
| P1-ind | Independent | Yes | 11,986 | 10,407 | 11,493 |
| P1 | Joint | Yes | 11,992 | 10,440 | 11,487 |
| PF-energy | Actuals | No | — | — | 11,055 |
| PF-reserve | Actuals | Yes | — | — | 11,657 |

To ground the analysis in the underlying data, Fig. 1 compares the day-ahead price forecast against the realized SMARD DE-LU series on 19 August 2026. The observed deviations between the predicted and actual trajectories underscore the magnitude of uncertainty that the scenario generation must effectively capture.


* Fig. 1. Forecast versus realized SMARD price series, 19 August 2026.*

The joint daily-block uncertainty is visually captured in Fig. 2, where the scenario fans reveal how cross-variable dependence shapes the intraday forecast envelope. The widening bands during peak hours reflect the joint daily-block construction; the formal joint-versus-independent comparison is deferred to Table II.


* Fig. 2. Joint daily-block scenario fans, K = 50.*

The forecast-error marginals were examined on a 58-day diagnostic window; that kernel-density panel is not included in this revision because its day-retention rule cannot be reconstructed from the available artifacts, so the marginals are described rather than plotted. For transparency about horizons: the full evaluation span 1 June–21 August 2026 covers 82 calendar days, and the 58 days used in the diagnostic are a subsample, distinct from both the 2024–2025 copula-fitting window of Section V-A and the 14-day out-of-sample window. These marginals must be read cautiously: the price-error density is unimodal with a pronounced central peak but shows tail excursions up to roughly ±300 EUR/MWh, and the load, PV and wind errors are visibly skewed, so the marginals are not formally Gaussian. Marginal shape does not determine the dependence structure: tail behaviour across the variables is a property of the copula, not of the marginals, so the fitted Student-t copula (ν = 18.55 on the 2024–2025 window) is a fitted approximation rather than evidence of tail independence. Formal Jarque–Bera tests of the marginals and a formal tail-dependence test remain future verification.


### B. Settlement Decomposition

Table III decomposes the EUR 549 gap between P1 and B0. Load service is exogenous and identical; the day-ahead energy, imbalance, and fuel/degradation lines net to −40 EUR, so the EUR 589 reserve-capacity revenue accounts for the entire gain. Componentwise: ΔDA = −448 (from −3,895 to −4,343), ΔReserve = +589, ΔImbalance = +398 (from −223 to +175), ΔDG-cost = −10 (cost 2,968 → 2,958), sum +549. The imbalance channel carries EUR 398 of the gap: with the two-price imbalance spread removed, the P1−B0 gap would fall to EUR 151 (−73%), so a large share of the reported gain is carried by the two-price imbalance proxy rather than by reserve revenue — consistent with the single-price German reBAP evidence of Section VIII. Because the reserve price is a proxy, a first-order sensitivity is informative: holding the P1 schedule fixed, the single-day gain remains positive as long as reserve revenue exceeds about EUR 40, roughly 7% of the proxy value. This sensitivity is a report-time calculation on the Table III decomposition rather than a re-solved run; re-solving the model under the proxy price and under cleared prices is the required next experiment (Section VIII). Two clarifications on scale: load service is the exogenous revenue line of the Table III decomposition (EUR 18,024), identical for B0, B2 and P1 by construction, so it cancels in every model comparison but inflates the absolute profit level; the reported 4.8% is therefore a ratio to the full simulated profit of the synthetic 5 MW-class portfolio, not to controllable profit—measured against the controllable settlement lines alone (reserve capacity EUR 589 less the EUR 40 net of energy, fuel and degradation), the isolation-day gap is EUR 549. A re-solved reserve-price sweep (0–150% of the proxy value), a re-solved P1 run at reserve price zero, and settlement-grade re-execution against real prices are the three required experiments of the re-execution program in Section VIII; In addition, the flat proxy prices make the identification issue explicit: with one price for both directions the objective sees only the sum r↑ + r↓, so the EUR 589 revenue is effectively a capacity rent at a fixed sold quantity rather than a price-responsive decision; re-execution with POS/NEG-separated real prices is what makes r↑ and r↓ separately identified and reports how often sells sit at the ceiling. The first two need the LP artifacts rather than new data, whereas the third is blocked by missing LP artifacts, not by missing data: the market inputs have since been retrieved — the cleared German aFRR capacity series for the window (mean 14.55, median 4.85 (EUR/MW)/h, 168 hourly rows; Section V-A) and the June–August 2026 reBAP record (7,872 quarter-hours; OOS-window mean 142.53 EUR/MWh against 131.01 DA; Section VIII) — but re-settlement of the 14 days on the real series requires the Study-A dispatch artifacts, which were not recovered in this revision.

TABLE IIISettlement Decomposition, 19 August 2026 (EUR)


| Component | B0 | B2 | P1 |
| --- | --- | --- | --- |
| Load service (exogenous) | 18,024 | 18,024 | 18,024 |
| DA energy | −3,895 | −4,255 | −4,343 |
| Reserve capacity | 0 | 0 | 589 |
| Imbalance | −223 | 163 | 175 |
| DG fuel / degradation (cost) | 2,968 | 2,968 | 2,958 |
| Net | 10,938 | 10,965 | 11,487 |

Expected scenario profit, scenario CVaR and realized settlement profit are three distinct quantities (Table II reports the first two, Table III the third); their reconciliation is: realized = expected +/- forecast-error and imbalance-settlement effects +/- proxy-reserve revenue. The economic value added by the reserve product is isolated in Fig. 3, which decomposes the expected profit against the realized settlement. This breakdown clearly separates the performance gap relative to the B0 benchmark, attributing the gains directly to the reserve-capable bidding strategy.


* Fig. 3. Expected profit versus realized settlement, and the gap relative to B0 (IS: in-sample scenario distribution).*

Turning to the risk-return trade-off, Fig. 4 depicts the expected-profit-to-CVaR slope and the resulting tail gap for each bidding strategy. This visualization highlights the marginal cost of risk mitigation, showing how different configurations balance profitability against tail-risk exposure. The tail gaps are nearly identical (EUR 1,512, 1,481, and 1,552 for B0, B2, and P1), so the higher realized profit of P1 is not purchased with a deeper scenario tail.


* Fig. 4. Expected-profit-to-CVaR slope and tail gap across configurations.*

To further evaluate tail-risk protection, Fig. 5 plots the empirical cumulative distribution functions of the scenario profits under the 50 joint draws. Fig. 4 and Fig. 5 must be read together: the tail gaps are nearly identical across strategies (EUR 1,512, 1,481 and 1,552 for B0, B2 and P1), so the lower-tail ECDF separation is modest and should be read as confirming comparable downside exposure, not superior downside protection. Realized out-of-sample CVaR was not computed; the tail evidence available is the scenario-level CVaR as plotted.


* Fig. 5. Empirical CDF of the K = 50 joint-scenario profits.*

The first-stage day-ahead energy positions are mapped against the realized DE-LU price in Fig. 6. This alignment illustrates how the bidding strategy dynamically responds to expected price signals, adjusting its market position throughout the operating day to maximize value.


* Fig. 6. First-stage day-ahead energy position and realized DE-LU price.*

Fig. 7 tracks the battery state-of-charge profiles across the bidding models. Notably, the P1 model strategically retains overnight energy to ensure the physical deliverability of its upward reserve commitments, distinguishing its operational behavior from the baselines.


* Fig. 7. Battery SoC; P1 retains overnight energy to support reserve deliverability.*

The scheduled upward reserve positions are presented in Fig. 8. Unlike B0 and B2, which sell no reserve, the P1 model actively participates in the reserve market, emphasizing the additional market participation enabled by the SoC-feasible deliverability constraint.


* Fig. 8. P1 two-sided reserve position (upward positive, downward negative); B0 and B2 sell no reserve.*


### C. Solver Performance

All reported LPs return kOptimal. Even P1 (K = 50, reserve feasibility in every scenario) solves in 0.303 s, which is compatible with a day-ahead workflow (Table IV).

TABLE IVHiGHS Model Size and Solution Time


| Model | K | Variables / inequalities | Status | Time (s) |
| --- | --- | --- | --- | --- |
| B0 | 1 | 216 / 46 | kOptimal | 0.011 |
| B2 | 50 | 7,323 / 2,350 | kOptimal | 0.173 |
| P1 | 50 | 7,323 / 7,150 | kOptimal | 0.303 |


### D. Rolling Out-of-Sample Performance

Table V reports the strict chronological evaluation over 6–19 August 2026. P1 has the highest mean realized profit, EUR 12,207.64/day versus 11,644.19 (B0) and 11,637.69 (B2), and all 14 paired differences against B0 are positive, which is what the exact test below encodes (Fig. 9). Its mean advantage is EUR 563.44/day (4.84%) over B0 and EUR 569.95/day (4.90%) over B2.

TABLE VStrict Rolling OOS Performance, 14 Days (EUR/day)


| Model | Mean | Std | Min | Max | P1 gain |
| --- | --- | --- | --- | --- | --- |
| B0 | 11,644.19 | 1,592.85 | 8,556.87 | 14,043.97 | — |
| B2 | 11,637.69 | 1,584.89 | 8,575.89 | 14,058.87 | — |
| P1 | 12,207.64 | 1,572.89 | 9,203.67 | 14,689.32 | 4.84% / 4.90% |

Fig. 9 reports the day-by-day realized profits across the 14-day rolling out-of-sample window. The day-level pattern shows that the P1 advantage is distributed across the window rather than carried by one or two days; the exact two-sided test in Table VI cannot be explained by a single outlier.


* Fig. 9. Daily realized profit of B0, B2, and P1 over the 14-day strict rolling OOS window (6–19 August 2026). All 14 paired differences against B0 are positive (exact p = 2/2¹⁴).*


### E. Paired Statistical Tests

Both models face the same 14 daily realizations, so paired tests are used (Table VI; 5000 bootstrap resamples of the paired differences). The P1−B0 and P1−B2 differences are significant, while B2−B0 is not. The Wilcoxon p ≈ 1.2×10⁻⁴ equals 2/2¹⁴, the smallest attainable two-sided exact value for n = 14, as expected when all 14 differences share one sign. The days are consecutive and may be serially correlated, so the tests describe this window rather than a long-run population. The bootstrap resamples are paired block resamples that keep each day's paired difference intact; no day-level independence is assumed. Three qualifications frame the table: because the proxy reserve revenue is essentially the same every day, the uniform sign of P1−B0 across the window reflects that near-constant revenue component rather than day-specific adaptive skill; the study design (proxy level, plant, β, K) was fixed before this window and the isolation day of 19 August sits inside it, so no hyperparameter was tuned on the window; and the sample length does not support external-validity inference. A Diebold–Mariano test with HAC variance, a moving-block bootstrap, and a multi-season extension with a full β-sweep are the required follow-up experiments (Section VIII).

TABLE VIPaired OOS Tests (n = 14, N_boot = 5000)


| Comparison | Mean Δ | 95% bootstrap CI | Paired t p | Wilcoxon p | d | Result |
| --- | --- | --- | --- | --- | --- | --- |
| P1 − B0 | 563.44 | [533.73, 593.65] | 2.86×10⁻¹⁴ | ≈1.2×10⁻⁴ | 9.39 | Significant |
| P1 − B2 | 569.95 | [546.91, 593.69] | 1.02×10⁻¹⁵ | ≈1.2×10⁻⁴ | 12.15 | Significant |
| B2 − B0 | −6.50 | [−18.80, 5.77] | 0.329 | 0.33 | −0.27 | Not significant |

Finally, Fig. 10 illustrates the daily profit advantage of P1 over B0. All 14 bars are positive, which is the same statement as the exact p = 2/2¹⁴ in Table VI, and the paired test correspondingly rejects a zero median difference.


* Fig. 10. Daily realized-profit advantage of P1 relative to B0; all 14 values are positive (exact p = 2/2¹⁴).*


### F. Feeder Ablation (Study B)

Table VII gives the seven-day ablation. Adding CVaR alone changes mean profit by EUR 0.2/day and violations by about one bus-hour/day. Removing the throughput-aging cost from the optimizer overstates realizable mean profit by about EUR 90/day; this figure is the magnitude of the modeling error, not a market property: with aging priced, the aging bill falls from 170 to 69 EUR/day at a cost of about 11 EUR/day in energy terms, and LinDistFlow bus-hour violations rise from 242 to 276/day. Re-executed across c^deg in {3,...,20} EUR/MWh, the benefit scales approximately as 7.5*c^deg - 10.7 EUR/day (+15 at c=3, +90 at c=12, +165 at c=20), and the 242-to-276 violation increase occurs on all seven days because aging pricing changes the midday/evening dispatch path: total battery throughput (charge + discharge) falls from 27.3 MWh/day (B0) to 3.8–7.7 MWh/day (B1a/B2/P1), which is where the previously quoted 'up to 23.5 MWh/day' figure came from — it is the total-throughput reduction on 6 April, whose discharge-only half is 11.1 MWh; on 8 April the discharge-only reduction B0−P1 is 3.3 MWh, consistent with the §VI-L EFC arithmetic (2.98 − 1.54) × 2.4 ≈ 3.5 MWh. The two quantities refer to different days and definitions, not a contradiction; the aging-priced dispatch deepens far-end voltage sags on all seven days (e5 diagnostics CSV). Adding the real-time voltage floor removes 276 ± 50 bus-hours/day of sub-0.93 pu violations, where ± denotes the cross-day standard deviation, at a mean cost of EUR 4.3/day (≈ EUR 0.016 per removed bus-hour, 276/day; Wilcoxon p = 0.016, the smallest attainable for n = 7). With a day-to-day profit standard deviation of about EUR 2,485, two orders above this premium, voltage correction is best read as constraint satisfaction rather than a profitability lever. Note that with K = 12 scenarios and α = 0.95, the CVaR tail contains only 0.6 expected scenarios, so the CVaR column of F-B1 effectively evaluates the worst-scenario profit rather than a smooth tail mean; an α/K recalibration (e.g., α = 0.9 or K ≥ 100) is a required experiment (Section VIII).

TABLE VIIFeeder Ablation (n = 7 days; HiGHS kOptimal, zero gap)


| Model | CVaR | Aging | V safety | Profit (EUR/d) | Worst day (EUR/d) | Viol. /day | Aging (EUR/d) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F-B0 | No | No | No | −5195.0 | −8828.1 | 241 | 170 |
| F-B1 | Yes | No | No | −5194.8 | −8829.0 | 242 | 169 |
| F-B2 | Yes | Yes | No | −5104.7 | −8816.2 | 276 | 69 |
| F-P1 | Yes | Yes | Yes | −5109.0 | −8826.6 | 0 | 67 |


### G. Peak Day, 8 April 2026

On 8 April, a high-price-spread day, aging is 172/169 EUR for F-B0/F-B1 versus 92/89 EUR for F-B2/F-P1 (more cycling on volatile days explains why this exceeds the weekly mean of 69 EUR). Only F-P1 holds the minimum voltage at the 0.93 pu floor; the voltage-blind models sag to 0.873 pu with more than 240 bus-hours of violation (Table VIII).

TABLE VIIIPeak Day, 8 April 2026 (EUR; |V| in pu)


| Model | DA revenue | Imbalance | Aging | Profit | V_min | Viol. |
| --- | --- | --- | --- | --- | --- | --- |
| F-B0 | −6067 | +61 | 172 | −6178 | 0.873 | 243 |
| F-B1 | −6080 | +73 | 169 | −6176 | 0.873 | 245 |
| F-B2 | −6083 | +75 | 92 | −6101 | 0.873 | 281 |
| F-P1 | −6083 | +63 | 89 | −6109 | 0.930 | 0 |


### H. P–Q Inverter Ablation

Table IX isolates active and reactive control on the F-P1 bid. P-only control cannot hold either floor. Q-only control holds 0.93 pu but freezes battery arbitrage (aging 0): in this mode the inverter reactive headroom consumes the |P|+|Q| <= 1.25 P_rated budget. Re-executed with an inscribed octagonal (circular) inverter envelope, the P-Q gain moves by only +1.8 to +11.1 EUR/day and reactive use stays 13.7-20.1 MVArh/day, so the 'P-Q is the only practical option' conclusion does not depend on the diamond envelope, leaving negligible active-power capacity for the battery, so its profit is worse than unconstrained F-B0; at the 0.95 pu floor it still leaves 63 violations. Joint P–Q control is the only mode that meets both floors while keeping the battery useful. Q-only is therefore a theoretical ablation, not an operating mode. Two study-design caveats attach: the |P|+|Q| envelope is a diamond, whereas a physical inverter capability curve is circular, so this envelope tends to over-value reactive capacity; and in the Q-only scenario the active-power variables are constrained to zero by construction, which makes the zero-aging outcome partly definitional. P and Q time profiles and a circular-envelope replication are required experiments (Section VIII).

TABLE IXInverter Ablation on the F-P1 Bid, 8 April 2026


| Floor (pu) |  | P | Q | Aging (EUR) | V_min (pu) | Viol. | Profit (EUR) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.93 |  | Yes | No | 73 | 0.921 | 61 | −6215 |
| 0.93 |  | No | Yes | 0 | 0.930 | 0 | −6638 |
| 0.93 |  | Yes | Yes | 89 | 0.930 | 0 | −6109 |
| 0.95 |  | Yes | No | 53 | 0.916 | 330 | −6258 |
| 0.95 |  | No | Yes | 0 | 0.942 | 63 | −6638 |
| 0.95 |  | Yes | Yes | 77 | 0.950 | 0 | −6161 |


## I. LinDistFlow Versus Newton–Raphson

Table X compares LinDistFlow with a Newton–Raphson (NR) solution on the same 8 April injections; all 24 hourly NR solves converged. The mean absolute discrepancy is 0.17% for F-P1 and the largest observed discrepancy is 0.0068 pu (F-B2). A margin of 0.007 pu is therefore a reasonable numerical safety margin for linearized voltage limits on this day, but it is an empirical value from one peak day and not a guarantee for other operating conditions. Re-executed again at a 0.937 pu LD setpoint on all seven days, the LD violations are zero by construction and the NR solution gives V_min 0.9338–0.9344 on every day (≥ 0.930), with maximum LD–NR deviation 0.0032 pu, at a weekly-mean profit cost of EUR 5.4/day (P1 mean −5109.00 → −5114.40 EUR/day); the empirical NR residual shortfall relative to the 0.930 pu floor is therefore removed by the higher setpoint. In the 0.930-pu base case re-executed on all seven Study-B days, the F-P1 LinDistFlow minimum of 0.930 pu corresponds to an NR minimum of 0.9261-0.9277 pu (maximum LD-NR deviation 0.0082 pu on 10 April), so the 'zero voltage violations' statement is a LinDistFlow result and the empirical AC margin is about 0.004 pu. This margin is empirical rather than a guarantee: the same table reports NR V_min = 0.926 pu for F-P1, i.e., the AC solution dips below the 0.930 pu linear-model floor even though the linear model records zero violations, so AC-side violations must be verified by NR for every day and every strategy before any feasibility claim (Section VIII).

TABLE XLinDistFlow vs. Newton–Raphson, 8 April 2026


| Model | LD V_min | NR V_min | NR mean |ΔV| | NR max |ΔV| |
| --- | --- | --- | --- | --- |
| F-B2 | 0.873 | 0.867 | 0.0029 | 0.0068 |
| F-P1 | 0.930 | 0.926 | 0.0017 | 0.0038 |


### J. First-Stage Feeder-Aware Bidding (F-S1V)

F-S1V embeds LinDistFlow in all 12 first-stage scenarios (42,445 variables, mean 0.77 s, 7/7 kOptimal) and settles the resulting bid on the same Stage-2 LP as F-P1. The bid moves: the weekly mean L1 distance is 0.84 MWh/day, L∞ = 0.20 MW, and about 6.7 h/day differ by more than 0.01 MW. Realized profit improves from −5109.0 to −5106.7 EUR/day, a gain of EUR 2.3/day (0.05% of |profit|; Wilcoxon W = 0, p = 0.016, n = 7, all seven differences positive). First-stage feeder awareness is therefore measurable but economically small once the Stage-2 correction exists.


### K. Residual FDIA Screening

A physics-residual/z-score screen was tested offline against six attack tapes (Table XI). It detects every voltage-channel tape, including a stealth tape, but only against the same LinDistFlow twin: recall rises from 0.01 at delta = 0.002 pu to 0.93 at delta = 0.008 pu and 1.00 at delta >= 0.010 pu, with threshold theta = 0.0132 pu (99th percentile of 200 clean residual draws). Against an independent Newton-Raphson measurement the same threshold gives recall 0.09/0.68/1.00 and precision 0.56/0.86/0.89 at delta = 0.004/0.008/0.012 pu (FPR up to 0.12), so the 0.90 figure is a same-twin result, not an independent-detector result. The screen cannot detect bid or price manipulation because those variables are not observable through a feeder-voltage residual. The screen is evaluated against the same LinDistFlow twin that defines the residual, so its recall is an upper bound; an independent physical model or real measurements are required before any cyber-resilience claim; the experiment supports a bounded detection claim, not general cyber-resilience.

TABLE XIPhysics-Residual / z-Score Screen (n = 120)


| Attack tape | Prec. | Rec. | F1 | Effect if missed |
| --- | --- | --- | --- | --- |
| Voltage bias +0.05 pu | 1.00 | 1.00 | 1.00 | — |
| Voltage ramp | 1.00 | 1.00 | 1.00 | — |
| Voltage stealth +0.008 pu | 1.00 | 0.93 (same-twin) / 0.68 (NR) | 0.95 | — |
| Voltage coordinated | 1.00 | 1.00 | 1.00 | — |
| Bid +0.40 MW | — | — | — | −226 EUR/day |
| Price +25 EUR/MWh | — | — | — | −1565 EUR/day |


### L. CVaR Sensitivity and Throughput Versus Xu Aging

Sweeping β ∈ {0, 0.05, 0.15, 0.30, 0.50} on 8 April moves F-P1 profit from about −6105 to −6182 EUR and the day-ahead position from −63.4 to −67.8 MWh: CVaR can affect the solution at higher weights but is economically inert at the operating β = 0.05. The Xu daily-range cost is 85.8 EUR for every model on 8 April because all units saturate the 10–90% SoC box, so it does not discriminate between strategies. Throughput aging does: equivalent full cycles of the 2.4 MWh fleet are 2.98 for F-B0 versus 1.54 for F-P1. Re-executed over alpha in {0.8, 0.9, 0.95} x K in {12, 100}, mean profit varies by at most 6.1 EUR (0.2%), so the operating choice (alpha = 0.95, K = 12) is not load-bearing. Xu is retained as a convex approximation, not as evidence of a superior aging law.


## VII. Discussion

Table XII summarizes which mechanisms the evidence supports. All Study-B figures (Tables VII-XI) were re-executed from the recovered code and data (HiGHS, 7 days, K=12, seed 20260827): the week ablation, Wilcoxon (W=0, p=0.015625), P/Q ablation, AC triple (LD 0.9300 to NR 0.9262), and FDIA suite reproduce exactly; the new experiments above (NR on all 7 days, c^deg sweep, (alpha,K) grid, circular envelope, FDIA radius/mismatch) are reported with their CSVs. In Study A the reserve product, not the error-dependence model, explains the gain: removing dependence changes P1 by EUR 6 on the isolation day, the fitted Student-t copula has a near-Gaussian tail profile (nu = 18.55 on the 2024–2025 window; a formal tail-dependence test remains open), and B2 is indistinguishable from B0 over 14 days. This is a narrower and more falsifiable statement than attributing the gain to “stochastic optimization.” It rests on a proxy reserve price; if cleared capacity prices were materially lower, the advantage would shrink toward the roughly EUR 40/day that the non-reserve lines of Table III contribute in the opposite direction, and could vanish.

In Study B, throughput aging is the only lever that moves euros materially. Real-time P–Q correction is technically decisive but economically modest, and first-stage feeder awareness is real but small. The two studies share a lesson: components of a sophisticated VPP architecture contribute unequally, and a controlled ablation, rather than a single proposed-versus-baseline comparison, is needed to attribute value.

TABLE XIIEvidence Status of Mechanisms


| Mechanism | Evidence | Status |
| --- | --- | --- |
| Reserve deliverability | Tables II, III, V, VI | Supported (proxy capacity price; real Sep-2026 reBAP/energy anchors); real aFRR capacity clearing in the 6-19 Aug 2026 OOS window averages 14.55 EUR/MW/h (median 4.85, range 0.34-92.50) against the 16.36 EUR/MW/h implied by the 589 EUR/day proxy, so the level is plausible (+12%) but the flat shape is not. |
| Joint-error dependence | P1 vs. P1-ind: EUR 6/day | Not supported |
| Energy-only CVaR (β = 0.05) | B2−B0 p = 0.33; +0.2 EUR/d | Not supported |
| Throughput aging | +90 EUR/d; 170→69 | Supported |
| Real-time P–Q voltage slack | 276→0 viol. (LD); −4.3 EUR/d; ·0.937 pu LD setpoint re-run: NR V_min 0.9338–0.9344 all 7 days, +5.4 EUR/d | Supported (technical) |
| First-stage feeder bid | +2.3 EUR/d; L₁ 0.84 MWh | Real, small |
| Voltage-residual FDIA screen | Recall 0.93 at delta=0.008 pu (same-twin); 0.68 (NR) | Bounded |
| Bid/price FDIA resilience | Missed: −226/−1565 EUR/d | Not supported |
| DRO, MARL, LLM, neural FDIA | Not evaluated | No claim |


## VIII. Limitations and Future Work

The rolling-OOS window is 14 summer days and the feeder window is seven April days; neither establishes seasonal generalization, and the two are not pooled. Scenario counts (K = 50 and K = 12) and the risk weight (beta = 0.05) are fixed apart from the one-day beta sweep; convergence over K and a multi-season OOS window remain open. Reserve and imbalance prices are shaped proxies, so the reported gains are simulation results. Market-design realism also remains open: the simulated reserve offer is not constrained by the 1 MW minimum bid size and unit bid increment, by FCR's symmetric two-sided delivery requirement, or by TSO prequalification and SCADA integration; and the two-price imbalance proxy retains the coefficient choices of eq. (2) (EUR 18/0.12 and EUR 10/0.08) even though the German reBAP is a single price applied symmetrically to surplus and deficit alike—the September 2026 anchors (mean 148.65 EUR/MWh over 2,784 published 15-min intervals; range −7208.55 to +4993.15 EUR/MWh) lie far outside the proxy spread. Direct reBAP settlement is future work. Cleared-real re-execution remains necessary before any market claim: the September 2026 reBAP and aFRR-energy series we retrieved document the relevant magnitudes, but the aFRR capacity result file was in a separate settlement source and the June-August 2026 reBAP record has since been retrieved (7,872 quarter-hours through 21 Aug; OOS-window mean 142.53 EUR/MWh against 131.01 DA), but the Study-A dispatch artifacts needed to re-settle the 14 days on the real series were not recovered, so direct aFRR/reBAP settlement remains unexecuted. SMARD is national aggregated data scaled to a portfolio, not metered VPP telemetry. Reserve and imbalance prices are shaped proxies rather than cleared FCR/aFRR or reBAP prices, and the SoC-feasible reserve constraint is not an N−1 criterion. Only day-ahead decisions and settlement are simulated; there is no intraday re-trading. Demand response is unused. Scenario counts (K = 50 and K = 12) and the risk weight (β = 0.05) are fixed, apart from the one-day β sweep. Stage 1 of the feeder study uses an aggregate battery while Stage 2 resolves three units, which can create a small mismatch between bid and realized aging. LinDistFlow is checked against Newton–Raphson on one peak day, not across a full-year AC study. The FDIA screen is offline, evaluated against its own twin, and blind to bid and price attacks. Four further disclosures bound the reading. Reproducibility: the Study-B artifacts were recovered, and every Study-B figure was re-executed from them (Section VI): the week ablation, Wilcoxon, P/Q ablation, AC triple, FDIA suite, plus the new NR/c^deg/(α,K)/envelope/FDIA-radius experiments. The Study-A LP artifacts (the solver, the per-run scenario files and the settlement scripts) were not recovered; the Study-A numbers (Tables II–VI, Figs. 1–10) are carried forward from earlier revisions of this study and cannot be re-derived from the material accompanying this submission, so they should be read as simulations on proxy prices pending artifact recovery. The recovered code, data panels, and re-execution results accompany this submission as supplementary material. Stage-2 recourse observes the full within-day realization of each scenario (intra-day foresight), so realized Stage-2 performance is an optimistic bound on multi-stage operation. The LP formulation imposes no explicit charge/discharge exclusivity, and the overlap of simultaneous charging and discharging is not reported for Study A. For Study B it is computed directly from the archived LP solutions: on the two archived days (6 and 8 April) the models without priced aging (B0, B1b, P0) overlap by 8.53 and 2.46 MWh/day respectively, while every aging-priced model (B1a, B2, P1) has exactly zero overlap — pricing throughput removes the double-counting on these days. Finally, cdeg = 12 EUR/MWh is a study parameter rather than a cell-data derivation (a 3–20 EUR/MWh sweep is required), and the day-retention rule behind the 58-day KDE diagnostic is not reconstructable from the available artifacts, so that panel is omitted from the figure set rather than reported. Measured directly on the real OOS panel (6–19 August 2026), the single German reBAP averages 142.53 EUR/MWh while the proxy long-side price λ− averages 110.50 EUR/MWh: the realized gap averages +32.03 EUR/MWh (reBAP above the proxy long side in 67.9% of intervals) and its daily mean spans −2.8 to +99.3 EUR/MWh — so the ≈5-EUR/MWh-scale sign of the imbalance channel (about −400 EUR/day in the proxy) is not stable across days, which is why the imbalance-free reading (EUR 151 gap) is presented as the robust decomposition.

Real-data anchors for reserve-price realism (added on re-execution): in the 1 Jun-21 Aug 2026 market panel (7,872 quarter-hours), reBAP is a single price (undercovered = overcovered = reBAP) with mean 121.20 EUR/MWh against 113.66 DA, CV 1.03 against 0.61, and 47.5% of hours reBAP > DA; in the 6-19 Aug 2026 OOS window reBAP averages 142.53 EUR/MWh against 131.01 DA (+8.8%). The September 2026 reBAP dispersion (mean 148.65 over 2,784 intervals, range -7208.55 to +4993.15, |reBAP| >= 100 in 66.3%) remains the immutable anchor. Future work should extend the evaluation across seasons and, where possible, to metered data; test the reserve finding against cleared aFRR/FCR capacity prices; integrate the feeder-aware first stage with the reserve product on one consistent plant; perform a longer AC feasibility study; and report DRO, conformal calibration, MARL, LLM, and neural FDIA components only after independent training, calibration, and OOS verification under the same protocol.


## IX. Conclusion

Within the tested SMARD DE-LU data, proxy pricing, and short windows, a deliverable SoC-feasible reserve product is the dominant source of the simulated market-bidding gain: EUR 549/day on the isolation day and EUR 563/day (4.8%) over 14 unseen days, while joint-versus-independent error sampling and energy-only CVaR contribute little. On the IEEE 33-bus feeder, throughput battery aging carries the material economic effect, real-time P–Q correction enforces LinDistFlow feasibility at a cost of EUR 4.3/day, with Newton–Raphson verification showing a residual shortfall of about 0.004 pu relative to the 0.930 pu linear-model floor, and first-stage feeder awareness changes the bid but recovers only EUR 2.3/day. Voltage-residual screening is useful but blind to bid and price manipulation. These conclusions are deliberately narrow, and the main open tests are reserve-price realism and direct reBAP settlement: the two-price proxy is structurally unlike the single-price German reBAP, whose September 2026 dispersion (mean 148.65 EUR/MWh; range −7208.55 to +4993.15 EUR/MWh) far exceeds the proxy spread, so settlement conclusions remain unvalidated until re-execution.

Acknowledgment

SMARD data [23] via Energy-Charts [24] are used under CC BY 4.0. Programs were solved with HiGHS [25]. Code and data artifacts supporting the reported simulations accompany this submission as supplementary material and in a public repository (a citable DOI will be assigned upon acceptance), including the recovered Study-B solver code and archived LP solutions, the market data panels and their extraction manifests, the re-execution results, and the reBAP/aFRR statistics scripts; the unrecovered Study-A LP solver and per-run artifacts are listed in Section VIII. AI-assisted drafting and language editing were used in preparing this manuscript; the authors verified the technical content, numerical results, and citations and remain responsible for them.

References

[1]D. Pudjianto, C. Ramsay, and G. Strbac, “Virtual power plant and system integration of distributed energy resources,” IET Renew. Power Gener., vol. 1, no. 1, pp. 10–16, Mar. 2007.

[2]J. M. Morales, A. J. Conejo, and J. Pérez-Ruiz, “Short-term trading for a wind power producer,” IEEE Trans. Power Syst., vol. 25, no. 1, pp. 554–564, Feb. 2010.

[3]A. J. Conejo, M. Carrión, and J. M. Morales, Decision Making Under Uncertainty in Electricity Markets. New York, NY, USA: Springer, 2010.

[4]R. T. Rockafellar and S. Uryasev, “Optimization of conditional value-at-risk,” J. Risk, vol. 2, no. 3, pp. 21–41, 2000.

[5]M. Vahedipour-Dahraie, H. Rashidizadeh-Kermani, M. Shafie-khah, and J. P. S. Catalão, “Risk-averse optimal energy and reserve scheduling for virtual power plants incorporating demand response programs,” IEEE Trans. Smart Grid, vol. 12, no. 2, pp. 1405–1415, Mar. 2021.

[6]G. He, Q. Chen, C. Kang, P. Pinson, and Q. Xia, “Optimal bidding strategy of battery storage in power markets considering performance-based regulation and battery cycle life,” IEEE Trans. Smart Grid, vol. 7, no. 5, pp. 2359–2367, Sep. 2016.

[7]B. Xu, J. Zhao, T. Zheng, E. Litvinov, and D. S. Kirschen, “Factoring the cycle aging cost of batteries participating in electricity markets,” IEEE Trans. Power Syst., vol. 33, no. 2, pp. 2248–2259, Mar. 2018, doi: 10.1109/TPWRS.2017.2733339.

[8]O. P. Akkas and E. Cam, “Risk-based optimal bidding and operational scheduling of a virtual power plant considering battery degradation cost and emission,” Adv. Elect. Comput. Eng., vol. 23, no. 2, pp. 19–28, 2023, doi: 10.4316/AECE.2023.02003.

[9]Q. Li et al., “Co-optimization of virtual power plants and distribution grids: Emphasizing flexible resource aggregation and battery capacity degradation,” Appl. Energy, vol. 377, Art. no. 124519, Jan. 2025, doi: 10.1016/j.apenergy.2024.124519.

[10]M. E. Baran and F. F. Wu, “Network reconfiguration in distribution systems for loss reduction and load balancing,” IEEE Trans. Power Del., vol. 4, no. 2, pp. 1401–1407, Apr. 1989.

[11]M. Farivar and S. H. Low, “Branch flow model: Relaxations and convexification—Part I,” IEEE Trans. Power Syst., vol. 28, no. 3, pp. 2554–2564, Aug. 2013.

[12]R. Gao and A. J. Kleywegt, “Distributionally robust stochastic optimization with Wasserstein distance,” Math. Oper. Res., vol. 48, no. 2, pp. 603–655, 2023, doi: 10.1287/moor.2022.1275.

[13]C. O’Connor et al., “Conformal prediction for electricity price forecasting in the day-ahead and real-time balancing market,” Energy AI, vol. 21, Art. no. 100571, 2025, doi: 10.1016/j.egyai.2025.100571.

[14]C. Huang, J. Fan, W. Wang, and H. Wang, “Safe decentralized operation of EV virtual power plant with limited network visibility via multi-agent reinforcement learning,” in Proc. IEEE Power Energy Soc. Gen. Meeting (PESGM), Montreal, QC, Canada, 2026, pp. 1–5, doi: 10.1109/PESGM58988.2026.11693326.

[15]Y. Cheng, H. Zhao, X. Zhou, J. Zhao, Y. Cao, and C. Yang, “GAIA—A large language model for advanced power dispatch,” arXiv:2408.03847, Aug. 2024.

[16]K. N. Singh, A. K. Goswami, N. B. D. Chudhury, H. A. Shuaibu, and T. S. Ustun, “Enhancing cybersecurity in virtual power plants by detecting network based cyber attacks using an unsupervised autoencoder approach,” Sci. Rep., vol. 15, Sep. 2025, doi: 10.1038/s41598-025-01863-w.

[17]  D. Xiao, H. Sun, D. Nikovski, S. Kitamura, K. Mori, and H. Hashimoto, “CVaR-constrained stochastic bidding strategy for a virtual power plant with mobile energy storages,” in Proc. IEEE PES Innov. Smart Grid Technol. Europe (ISGT-Europe), 2020, pp. 1171–1175, doi: 10.1109/ISGT-Europe47291.2020.9248799.

[18]  S. Sadeghi, H. Jahangir, B. Vatandoust, M. A. Golkar, A. Ahmadian, and A. Elkamel, “Optimal bidding strategy of a virtual power plant in day-ahead energy and frequency regulation markets: A deep learning-based approach,” Int. J. Electr. Power Energy Syst., vol. 127, Art. no. 106646, 2021, doi: 10.1016/j.ijepes.2020.106646.

[19]  C. Yang, X. Du, D. Xu, J. Tang, X. Lin, K. Xie, and W. Li, “Optimal bidding strategy of renewable-based virtual power plant in the day-ahead market,” Int. J. Electr. Power Energy Syst., vol. 144, Art. no. 108557, 2023, doi: 10.1016/j.ijepes.2022.108557.

[20]  M. A. Niazi, V. Kumar, T. Chen, and M. Zhu, “Scalable co-optimization of virtual power plants in frequency regulation markets: Integrating stochastic bidding and mean field games,” Energy, vol. 358, Art. no. 141360, 2026, doi: 10.1016/j.energy.2026.141360.

[21]  K. N. Singh, A. K. Goswami, N. B. D. Chudhury, U. Cali, and T. S. Ustun, “A risk-aware bidding model for virtual power plants: Integrating renewable energy forecasting and carbon market strategies,” Energy Rep., vol. 14, pp. 1222–1239, 2025, doi: 10.1016/j.egyr.2025.07.032.

[22]  W. Qin, X. Li, X. Jing, Z. Zhu, R. Lu, and X. Han, “Multi-temporal optimization of virtual power plant in energy-frequency regulation market under uncertainties,” J. Mod. Power Syst. Clean Energy, vol. 13, no. 2, pp. 675–687, 2024, doi: 10.35833/mpce.2024.000118.

[23]Bundesnetzagentur, “SMARD—Strommarktdaten.” [Online]. Available: https://www.smard.de

[24]B. Burger, “Energy-Charts,” Fraunhofer Institute for Solar Energy Systems ISE. [Online]. Available: https://www.energy-charts.info

[25]Q. Huangfu and J. A. J. Hall, “Parallelizing the dual revised simplex method,” Math. Program. Comput., vol. 10, no. 1, pp. 119–142, 2018.

[26]  regelleistung.net, “Balancing capacity and balancing energy market (aFRR/mFRR/FCR): product rules, tendering and settlement,” [Online]. Available: https://www.regelleistung.net. Accessed: 2026.

[27]  Netztransparenz, “Activation data for balancing energy (reBAP),” [Online]. Available: https://www.netztransparenz.de. Accessed: 2026.

Nomenclature Table (Appendix)


| Symbol | Type | Description |
| --- | --- | --- |
| Indices and Sets |  |  |
| t | Index | Hour index |
| ω | Index | Scenario index |
| b | Index | Battery index |
| n,i,k | Index | Bus/Node index in the distribution network |
| d | Index | Day index |
| Hd-1 | Set | Information set available before day d |
| Ci | Set | Set of children nodes connected to node i |
| Parameters and Constants |  |  |
| πω | Parameter | Probability of scenario ω |
| β | Parameter | CVaR weight (e.g., 0.05) |
| α | Parameter | Tail parameter (e.g., 0.95) |
| K | Parameter | Number of scenarios |
| η | Parameter | Battery efficiency (e.g., 0.95); η inside the CVaR block of (3)–(4) denotes the value-at-risk threshold at level α |
| λtDA | Parameter | Day-ahead market price |
| λt+,λt- | Parameter | Long/short imbalance prices (two-price proxy, eq. (2): long surplus settled at the low price, short deficit charged the high price) |
| cdeg | Parameter | Degradation cost coefficient (12 EUR/MWh) |
| ρs | Parameter | Voltage slack penalty (2500 EUR/pu²) |
| Prated | Parameter | Inverter rated power |
| vnmin | Parameter | Minimum voltage limit (0.93 or 0.95 pu) |
| Δt | Parameter | Time step (1 hour) |
| Sb | Parameter | Base power (10 MVA) |
| θd | Calibration (parameter) | First-stage decisions/calibration |
| xd* | Solver output (held decision) | Optimal first-stage decision |
| rij,xij | Parameter | Line resistance and reactance |
| Decision Variables |  |  |
| pt,ωDA | Continuous | Day-ahead energy position (export > 0) |
| pt,ωch,pt,ωdis | Continuous | Battery charge/discharge power |
| δt,ω+,δt,ω- | Continuous | Long/short imbalance |
| rt | Continuous | Two-sided reserve as separate first-stage variables in P1: upward r↑ and downward r↓ each bounded by the deliverability constraints |
| Et,ω | Continuous | State of Charge (SoC) |
| zω | Continuous | CVaR auxiliary variable |
| Pi,t,Qi,t | Continuous | Active/Reactive line flow |
| vi,t | Continuous | Squared voltage magnitude (v = |V|², pu²); the 0.93 pu floor is v ≥ 0.93² |
| sn,t | Continuous | Voltage slack variable (expressed in squared-voltage units, pu²) |
| Functions and Metrics |  |  |
| It,ω | Function | Scenario profit |
| Cdeg | Function | Total degradation cost |
| Πdreal | Metric | Realized settlement profit |
| Δd | Metric | Paired profit difference |
| Acronyms |  |  |
| VPP | Acronym | Virtual Power Plant |
| LP | Acronym | Linear Programming |
| CVaR | Acronym | Conditional Value-at-Risk |
| OOS | Acronym | Out-of-Sample |
| SoC | Acronym | State of Charge |
| PV | Acronym | Photovoltaic |
| DRO | Acronym | Distributionally Robust Optimization |
| FDIA | Acronym | False Data Injection Attack |
| DA | Acronym | Day-Ahead |
| FCR / aFRR | Acronym | Frequency Containment Reserve / automatic Frequency Restoration Reserve |
