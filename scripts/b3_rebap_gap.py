# -*- coding: utf-8 -*-
"""B3: real OOS reBAP (6-19 Aug 2026) vs Study-A proxy two-price lambda from eq(2).
Proxy: lambda+ >= DA + 18 + 0.12|DA| ; lambda- <= DA - 10 - 0.08|DA| (long side).
Measure: daily mean gap reBAP - lambda-_proxy and reBAP - lambda+_proxy."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pandas as pd, numpy as np

P = r"C:\Users\Mahboobian\Desktop\article 6\data\processed\market_data_2026-08_oos\market_panel_15min.csv"
df = pd.read_csv(P)
df["da"] = df["da_price_eur_mwh"]
df["rebap"] = df["rebap_eur_mwh"]
lmin = df["da"] - 10 - 0.08 * df["da"].abs()
lplus = df["da"] + 18 + 0.12 * df["da"].abs()
gap_minus = df["rebap"] - (df["da"] - 10 - 0.08 * df["da"].abs())
gap_plus = df["rebap"] - (df["da"] + 18 + 0.12 * df["da"].abs())
out = pd.DataFrame({
    "day": df["day_local"],
    "da": df["da"], "rebap": df["rebap"],
    "lminus_proxy": (df["da"] - 10 - 0.08 * df["da"].abs()),
    "lplus_proxy": lplus,
    "gap_minus": gap_minus, "gap_plus": gap_plus,
})
daily = out.groupby("day").agg(
    da_mean=("da", "mean"), rebap_mean=("rebap", "mean"),
    lminus_mean=("lminus_proxy", "mean"), lplus_mean=("lplus_proxy", "mean"),
    gap_minus_mean=("gap_minus", "mean"), gap_plus_mean=("gap_plus", "mean")).reset_index()
daily["gap_minus_eur_per_mwh"] = daily["gap_minus_mean"]
print(daily.round(2).to_string())
print()
print("WINDOW MEANS: rebap %.2f, DA %.2f, lambda-_proxy %.2f, lambda+_proxy %.2f" % (
    out["rebap"].mean(), out["da"].mean(), out["lminus_proxy"].mean(), out["lplus_proxy"].mean()))
print("gap rebap - lambda-_proxy: mean %.2f, min %.2f, max %.2f" % (out["gap_minus"].mean(), out["gap_minus"].min(), out["gap_minus"].max()))
print("gap rebap - lambda+_proxy: mean %.2f, min %.2f, max %.2f" % (out["gap_plus"].mean(), out["gap_plus"].min(), out["gap_plus"].max()))
print("share of intervals rebap > lambda-_proxy: %.1f%%" % (100 * (out["gap_minus"] > 0).mean()))
print("share of intervals rebap < lambda+_proxy: %.1f%%" % (100 * (out["gap_plus"] < 0).mean()))
# what the imbalance term would earn per MWh of deficit position under each price
print()
print("If deficit (buy) priced at lambda-_proxy: mean %.2f vs actual reBAP %.2f -> under by %.2f EUR/MWh (%.1f%%)" % (
    out["lminus_proxy"].mean() if out["lminus_proxy"].mean() > 0 else out["lminus_proxy"].mean(),
    out["rebap"].mean(), out["rebap"].mean() - out["lminus_proxy"].mean(),
    100 * (out["rebap"].mean() - out["lminus_proxy"].mean()) / abs(out["lminus_proxy"].mean())))
daily.round(4).to_csv(r"C:\Users\Mahboobian\Documents\Default Project\_draft\results_check\b3_rebap_gap_daily.csv", index=False)
print("saved b3_rebap_gap_daily.csv")
