# -*- coding: utf-8 -*-
"""Study A break-even reserve price vs REAL cleared aFRR capacity (OOS window 6-19 Aug 2026)."""
import sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pandas as pd
base = r"C:\Users\Mahboobian\Desktop\article 6\data\processed\market_data_2026-08_oos"
df = pd.read_csv(os.path.join(base, "afrr_capacity.csv"))
print("cols:", [c[:40] for c in df.columns][:14])
print("rows:", len(df))
print("TYPE_OF_RESERVES values:", df["TYPE_OF_RESERVES"].unique()[:6])
print("PRODUCT values:", df["PRODUCT"].unique()[:8])
c = "GERMANY_AVERAGE_CAPACITY_PRICE_[(EUR/MW)/h]"
cm = "GERMANY_MARGINAL_CAPACITY_PRICE_[(EUR/MW)/h]"
print("\nGermany avg price summary (all rows):")
print(df[c].describe().to_string())
print("\nby TYPE_OF_RESERVES x PRODUCT:")
g = df.groupby(["TYPE_OF_RESERVES", "PRODUCT"])[c].agg(["count", "mean", "min", "max"])
print(g.to_string())
print("\nmarginal, by type:")
g2 = df.groupby(["TYPE_OF_RESERVES"])[cm].agg(["count", "mean", "min", "max"])
print(g2.to_string())
# break-even of the manuscript proxy
for mw, name in ((1.5, "1.5MW reserve"), (1.0, "1.0MW"), (2.0, "2.0MW")):
    be = 589.0 / (mw * 24)
    print(f"\nbreak-even for 589 EUR/day at {name}: {be:.2f} EUR/MW/h")
print("\nNote: proxy 589/(1.5*24)=16.36 EUR/MW/h; avg/marginal cleared prices above are the real anchors.")
# Summer + September sets too
for tag, path in (("summer(1Jun-21Aug)", r"market_data_2026-summer\afrr_capacity.csv"),
                  ("Jun-Aug", r"market_data_2026-06-01_to_2026-08-21\afrr_capacity.csv")):
    p = os.path.join(os.path.dirname(base), path)
    if os.path.exists(p):
        d2 = pd.read_csv(p)
        print(f"\n== {tag}: rows {len(d2)}, avg price mean {d2[c].mean():.2f}, marginal mean {d2[cm].mean():.2f}")
