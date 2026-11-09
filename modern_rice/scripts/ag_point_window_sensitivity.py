#!/usr/bin/env python3
"""Point-level GDD10 window sensitivity (NASA POWER daily, 2000-2024).

The original pipeline (fetch_nasa_power.py) builds a pseudo day-of-year as
month*30.4+day and keeps 150..285, i.e. calendar 29 Apr-11 Sep (NH).
This script recomputes seasonal GDD10 for that window and for calendar
Jun 1-Sep 30 and May 1-Sep 30 so that the documented window and the
transfer ranking can be checked. Southern-hemisphere points are skipped.
"""
import os, json, ast, numpy as np, pandas as pd
HERE = os.path.dirname(__file__)
RAW = os.path.join(HERE, "..", "data", "raw")
OUT = os.path.join(HERE, "..", "..", "outputs", "modern_rice", "applied_geography")
os.makedirs(OUT, exist_ok=True)
src = open(os.path.join(HERE, "fetch_nasa_power.py")).read()
POINTS = ast.literal_eval(src.split("POINTS = ", 1)[1].split("\n}\n", 1)[0] + "\n}")
rows = []
for k, (la, lo) in POINTS.items():
    if la < 0: continue
    p = json.load(open(os.path.join(RAW, f"nasa_power_{k}.json")))["properties"]["parameter"]
    df = pd.DataFrame({"tmax": p["T2M_MAX"], "tmin": p["T2M_MIN"]})
    df.index = pd.to_datetime(df.index); df = df[(df.tmax > -900) & (df.tmin > -900)]
    df["gdd"] = np.maximum((df.tmax + df.tmin) / 2 - 10, 0)
    pseudo = df.index.month * 30.4 + df.index.day
    md = df.index.month * 100 + df.index.day
    wins = {"pipeline_29Apr_11Sep": (pseudo >= 150) & (pseudo <= 285),
            "calendar_Jun_Sep": (md >= 601) & (md <= 930),
            "calendar_May_Sep": (md >= 501) & (md <= 930)}
    r = {"point": k, "lat": la, "lon": lo}
    for w, m in wins.items():
        r[w] = round(df[m].groupby(df.index[m].year).gdd.sum().mean(), 0)
    rows.append(r)
d = pd.DataFrame(rows)
for w in ["calendar_Jun_Sep", "calendar_May_Sep"]:
    ref = d.loc[d.point == "Hokkaido_JP", w].iloc[0]
    d[f"{w}_ratio_to_Hokkaido"] = (d[w] / ref).round(3)
ref = d.loc[d.point == "Hokkaido_JP", "pipeline_29Apr_11Sep"].iloc[0]
d["pipeline_ratio_to_Hokkaido"] = (d["pipeline_29Apr_11Sep"] / ref).round(3)
d.to_csv(os.path.join(OUT, "POINT_GDD_WINDOW_SENSITIVITY.csv"), index=False)
print(d[["point", "pipeline_29Apr_11Sep", "calendar_Jun_Sep", "calendar_May_Sep", "pipeline_ratio_to_Hokkaido", "calendar_Jun_Sep_ratio_to_Hokkaido"]].to_string())
