#!/usr/bin/env python3
"""Recompute the September 2026 anchors from the archived panel.

Inputs : data/market/sept_2026/market_panel_15min.csv
         data/market/sept_2026/fcr_capacity_clearing_4h.csv
         data/market/sept_2026/mfrr_capacity_clearing_4h.csv
Output : results/market/sept_2026_anchors.json
"""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SEP = ROOT / "data" / "market" / "sept_2026"
OUT = ROOT / "results" / "market"
OUT.mkdir(parents=True, exist_ok=True)

panel = pd.read_csv(SEP / "market_panel_15min.csv")
reb = panel["rebap_eur_mwh"].dropna()
anchors = {
    "rebap": {
        "intervals": int(reb.shape[0]),
        "mean_eur_mwh": round(float(reb.mean()), 2),
        "min_eur_mwh": round(float(reb.min()), 2),
        "max_eur_mwh": round(float(reb.max()), 2),
        "share_abs_ge_100_pct": round(float((reb.abs() >= 100).mean() * 100), 1),
    },
    "da": {"mean_eur_mwh": round(float(panel["da_price_eur_mwh"].dropna().mean()), 2)},
}

fcr = pd.read_csv(SEP / "fcr_capacity_clearing_4h.csv")
fcol = "germany_settlement_capacity_price_eur_per_mw"
p = fcr[fcol].dropna()
daily = fcr.groupby("delivery_date")[fcol].mean()
anchors["fcr"] = {
    "column": fcol,
    "products": int(p.shape[0]),
    "mean_eur_per_mw": round(float(p.mean()), 2),
    "min_eur_per_mw": round(float(p.min()), 2),
    "max_eur_per_mw": round(float(p.max()), 2),
    "daily_mean_min": round(float(daily.min()), 2),
    "daily_mean_max": round(float(daily.max()), 2),
    "daily_sum_mean": round(float(fcr.groupby("delivery_date")[fcol].sum().mean()), 2),
    "daily_sum_min": round(float(fcr.groupby("delivery_date")[fcol].sum().min()), 2),
    "daily_sum_max": round(float(fcr.groupby("delivery_date")[fcol].sum().max()), 2),
}

mfrr = pd.read_csv(SEP / "mfrr_capacity_clearing_4h.csv")
mcol = [c for c in mfrr.columns if "germany" in c.lower() and "marginal" in c.lower()][0]
anchors["mfrr"] = {
    "column": mcol,
    "mean_eur_per_mw_h": round(float(mfrr[mcol].dropna().mean()), 2),
}

anchors["not_archived"] = [
    "German aFRR capacity clearing for September 2026 (no result file in the supplied export)",
    "Anonymised aFRR energy bid lists used for the 2249.80 EUR/MWh monthly mean",
]

with open(OUT / "sept_2026_anchors.json", "w", encoding="utf-8") as f:
    json.dump(anchors, f, indent=2)
print(json.dumps(anchors, indent=2))
print("written:", OUT / "sept_2026_anchors.json")
