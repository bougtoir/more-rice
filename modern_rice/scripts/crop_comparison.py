#!/usr/bin/env python3
"""FAOSTAT crop comparison: yields -> edible kcal/ha for focal countries."""
import pandas as pd, os, csv

RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "modern_rice")
os.makedirs(OUT, exist_ok=True)

F = os.path.join(RAW, "Production_Crops_Livestock_E_All_Data_(Normalized).csv")
items = ["Rice", "Wheat", "Barley", "Maize (corn)", "Potatoes"]
areas = ["United Kingdom of Great Britain and Northern Ireland", "France", "Germany",
         "Italy", "Spain", "Portugal", "Japan", "China, mainland", "India",
         "United States of America", "Bangladesh", "Egypt", "Nigeria", "Brazil",
         "Poland", "Ukraine", "Netherlands", "Denmark", "Sweden", "Finland"]

d = pd.read_csv(F, usecols=["Area","Item","Element","Year","Value","Unit"], low_memory=False)
d = d[d.Item.isin(items) & d.Area.isin(areas)]
y = d[d.Element=="Yield"].groupby(["Area","Item"]).apply(
    lambda g: g.loc[g.Year==g.Year.max()].Value.iloc[0], include_groups=False)
# kg/ha -> check unit
KCAL = {"Rice": 3.65,   # paddy*milled-equiv approx; see notes
        "Wheat": 3.4, "Barley": 3.5, "Maize (corn)": 3.6, "Potatoes": 0.8}
rows=[]
for (a,i),v in y.items():
    rows.append([a,i,round(v,0),round(v*KCAL[i]*1000,0)])  # kg/ha -> kcal/ha? kg*kcal/g = kg*1000 kcal/kg... kcal/kg = KCAL*1000
df = pd.DataFrame(rows, columns=["Area","Item","yield_kg_ha","edible_kcal_ha"])
df.to_csv(os.path.join(OUT,"CROP_YIELD_KCAL_COMPARISON.csv"), index=False)
# pivot kcal
p = df.pivot(index="Area",columns="Item",values="edible_kcal_ha")
p.to_csv(os.path.join(OUT,"KCAL_PER_HA_PIVOT.csv"))
print(df.head(30).to_string())
