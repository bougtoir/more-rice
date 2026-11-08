#!/usr/bin/env python3
"""Bias of the monthly-mean GDD10 approximation (used on the WorldClim grid)
relative to daily accumulation, both computed from the same NASA POWER daily
series (2000-2024) at the point cells. Output: GDD_DAILY_VS_MONTHLY.csv."""
import os, json, numpy as np, pandas as pd
HERE = os.path.dirname(__file__); RAW = os.path.join(HERE, "..", "data", "raw")
OUT = os.path.join(HERE, "..", "..", "outputs", "modern_rice", "applied_geography")
WINS = {"calendar_Jun_Sep": ("06-01", "09-30"), "pipeline_29Apr_11Sep": ("04-29", "09-11")}
rows = []
for n in ["Hokkaido_JP", "Rhine_DE", "Saxony_DE", "Alsace_FR", "Berlin_DE", "Loire_FR", "LowerDanube_RO"]:
    f = os.path.join(RAW, f"nasa_power_{n}.json")
    if not os.path.exists(f): continue
    p = json.load(open(f))["properties"]["parameter"]
    df = pd.DataFrame({k: pd.Series(v) for k, v in p.items()}); df.index = pd.to_datetime(df.index, format="%Y%m%d"); df = df.replace(-999, np.nan)
    T = df["T2M"] if "T2M" in df else (df.T2M_MAX + df.T2M_MIN) / 2
    for lab, (a, b) in WINS.items():
        dd, mm = [], []
        for y in sorted(set(T.index.year)):
            s = T[f"{y}-{a}":f"{y}-{b}"].dropna()
            if len(s) < 90: continue
            dd.append(np.maximum(s - 10, 0).sum())
            mm.append(sum(np.maximum(g.mean() - 10, 0) * len(g) for _, g in s.groupby(s.index.month)))
        rows.append(dict(point=n, window=lab, n_years=len(dd), gdd_daily=round(np.mean(dd), 1), gdd_monthly_mean=round(np.mean(mm), 1),
                         bias_monthly_minus_daily=round(np.mean(mm) - np.mean(dd), 1)))
pd.DataFrame(rows).to_csv(os.path.join(OUT, "GDD_DAILY_VS_MONTHLY.csv"), index=False); print(pd.DataFrame(rows).to_string())
