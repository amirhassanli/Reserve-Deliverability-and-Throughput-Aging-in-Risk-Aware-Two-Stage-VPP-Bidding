# -*- coding: utf-8 -*-
"""Single-price reBAP vs DA statistics from the summer panel (real data)."""
import sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pandas as pd, numpy as np
base = r"C:\Users\Mahboobian\Desktop\article 6\data\processed\market_data_2026-summer"
df = pd.read_csv(os.path.join(base, "market_panel_15min.csv"))
print("rows", len(df), "days", df["day_local"].nunique())
# hourly aggregation
df["hour"] = pd.to_datetime(df["timestamp_utc"], utc=True).dt.floor("h")
h = df.groupby("hour", as_index=False).agg(
    da=("da_price_eur_mwh","mean"), rebap=("rebap_eur_mwh","mean"),
    rebap_uc=("rebap_undercovered_eur_mwh","mean"),
    rebap_oc=("rebap_overcovered_eur_mwh","mean"),
    load=("load_actual_mw","mean"), solar=("solar_generation_mw","mean"),
    won=("wind_onshore_generation_mw","mean"), woff=("wind_offshore_generation_mw","mean"))
print("hourly rows", len(h))
print("\nDA price: mean %.2f median %.2f min %.2f max %.2f std %.2f" % (h.da.mean(), h.da.median(), h.da.min(), h.da.max(), h.da.std()))
print("reBAP:    mean %.2f median %.2f min %.2f max %.2f std %.2f" % (h.rebap.mean(), h.rebap.median(), h.rebap.min(), h.rebap.max(), h.rebap.std()))
print("reBAP-DA: mean %.2f median %.2f min %.2f max %.2f" % ((h.rebap-h.da).mean(), (h.rebap-h.da).median(), (h.rebap-h.da).min(), (h.rebap-h.da).max()))
print("corr(DA,reBAP) = %.4f" % h.da.corr(h.rebap))
print("share hours reBAP>DA: %.1f%%  reBAP<DA: %.1f%%  equal: %.1f%%" % (
    100*(h.rebap>h.da).mean(), 100*(h.rebap<h.da).mean(), 100*(h.rebap==h.da).mean()))
print("single-price check: undercovered==overcovered==rebap all rows:", bool((df.rebap_undercovered_eur_mwh==df.rebap_eur_mwh).all() and (df.rebap_overcovered_eur_mwh==df.rebap_eur_mwh).all()))
# two-price spread proxy comparison: manuscript's da±spread vs reBAP
spread = 2.0
print("\nManuscript two-price proxy settlement revenue per MWh imbalance (da±spread) vs single reBAP:")
print("  mean |da-spread - rebap| = %.2f  mean |da+spread - rebap| = %.2f" % (
    (h.da-spread-h.rebap).abs().mean(), (h.da+spread-h.rebap).abs().mean()))
# daily aggregation: how many days does reBAP exceed DA on average
daily = h.groupby(h.hour.dt.date).agg(da=("da","mean"), rebap=("rebap","mean"))
daily["diff"] = daily.rebap - daily.da
print("\ndaily reBAP-DA: mean %.2f, min %.2f, max %.2f, share days rebap>da %.1f%%" % (
    daily["diff"].mean(), daily["diff"].min(), daily["diff"].max(), 100*(daily["diff"]>0).mean()))
print("n days:", len(daily))
# volatility
print("\nreBAP hourly std/mean (CV): %.3f ; DA CV: %.3f" % (h.rebap.std()/h.rebap.mean(), h.da.std()/h.da.mean()))
# OOS window subset
oos = df[(df["day_local"]>="2026-08-06") & (df["day_local"]<="2026-08-19")]
print("\nOOS window 6-19 Aug: hours=%d days=%d" % (len(oos), oos["day_local"].nunique()))
ho = oos.groupby(oos["timestamp_utc"].str[:13], as_index=False).agg(da=("da_price_eur_mwh","mean"), rebap=("rebap_eur_mwh","mean"))
print("OOS DA mean %.2f reBAP mean %.2f diff %.2f corr %.4f" % (ho.da.mean(), ho.rebap.mean(), (ho.rebap-ho.da).mean(), ho.da.corr(ho.rebap)))
# save summary
out = pd.DataFrame([{
    "panel":"summer 2026 (1 Jun-21 Aug)", "n_hourly":len(h), "n_days":h.hour.dt.date.nunique(),
    "da_mean":h.da.mean(),"da_median":h.da.median(),"da_min":h.da.min(),"da_max":h.da.max(),"da_std":h.da.std(),
    "rebap_mean":h.rebap.mean(),"rebap_median":h.rebap.median(),"rebap_min":h.rebap.min(),"rebap_max":h.rebap.max(),"rebap_std":h.rebap.std(),
    "rebap_minus_da_mean":(h.rebap-h.da).mean(),"rebap_minus_da_median":(h.rebap-h.da).median(),
    "corr_da_rebap":h.da.corr(h.rebap),
    "share_hours_rebap_gt_da":(h.rebap>h.da).mean(),
    "single_price":bool((df.rebap_undercovered_eur_mwh==df.rebap_eur_mwh).all()),
}])
out.to_csv(r"C:\Users\Mahboobian\Documents\Default Project\_draft\rebap_summary.csv", index=False)
print("\nSAVED rebap_summary.csv")
print(out.T.to_string())
