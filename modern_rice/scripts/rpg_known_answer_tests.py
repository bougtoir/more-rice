#!/usr/bin/env python3
"""Known-answer tests for the RPG overlay/omission logic. Oracle: planar shapely areas in degrees and plain numpy (not the production functions)."""
import os, sys, numpy as np, pandas as pd, geopandas as gpd
from shapely.geometry import box, Polygon
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import rpg_validation as V
OUT = V.OUT; res = []
def check(name, ok, detail=""): res.append(dict(test=name, result="PASS" if ok else "FAIL", detail=detail))
# synthetic 2x2 grid of 0.1-degree cells inside France
V.W, V.N, V.R = 4.0, 44.0, 0.1
V.g5 = np.array([[500.0, 1000.0], [np.nan, 589.0]], dtype="float32")
def P(geoms, w=None):
    p = gpd.GeoDataFrame(dict(geometry=geoms), crs=4326); p["geo_ha"] = p.to_crs(2154).area / 1e4; p["w"] = p.geo_ha if w is None else w; p["pid"] = range(len(p)); return p
inside = box(4.02, 43.92, 4.08, 43.98); cross = box(4.05, 43.92, 4.15, 43.98); nod = box(4.02, 43.82, 4.08, 43.95)
ix = V.overlay(P([inside])); check("1 parcel inside one cell -> single intersection, frac 1", len(ix) == 1 and abs(ix.frac.iloc[0] - 1) < 1e-6, f"frac={ix.frac.iloc[0]:.6f}")
ix = V.overlay(P([cross])); fr = ix.sort_values("c").frac.values; ora = [cross.intersection(box(4.0, 43.9, 4.1, 44.0)).area / cross.area, cross.intersection(box(4.1, 43.9, 4.2, 44.0)).area / cross.area]
check("2 parcel crossing two cells -> area split matches planar oracle", np.allclose(fr, ora, atol=5e-3), f"prod={np.round(fr,4)} oracle={np.round(ora,4)}")
o = V.omit(ix.a.values, ix.g.values, 589); check("2b crossing parcel omission at 589 equals share in 500-GDD cell", abs(o - ora[0]) < 5e-3, f"{o:.4f} vs {ora[0]:.4f}")
ix = V.overlay(P([nod])); fin = np.isfinite(ix.g); ora_in = nod.intersection(box(4.0, 43.9, 4.1, 44.0)).area / nod.area
check("3 parcel overlapping nodata cell -> nodata share excluded from denominator", abs(ix.a[~fin].sum() / ix.a.sum() - (1 - ora_in)) < 5e-3 and V.omit(ix.a.values, ix.g.values, 589) == 1.0, f"nodata share={ix.a[~fin].sum()/ix.a.sum():.4f}")
ix = V.overlay(P([inside, box(4.01, 43.91, 4.03, 43.93)])); check("4 two parcels in same cell -> one climate cell", ix.groupby(["r", "c"]).ngroups == 1)
z = P([inside, Polygon([(4.05, 43.95), (4.05, 43.95), (4.05, 43.95), (4.05, 43.95)])]); zc = V.clean_area(z)
check("5 zero-area parcel removed by clean_area before overlay", len(zc) == 1 and z.geo_ha.iloc[1] == 0 and abs(V.overlay(zc).a.sum() - z.geo_ha.iloc[0]) < 1e-6)
ix = V.overlay(P([box(4.12, 43.82, 4.18, 43.88)])); check("6 threshold equal to cell GDD (589) -> passes (strict <)", V.omit(ix.a.values, ix.g.values, 589) == 0.0 and V.omit(ix.a.values, ix.g.values, 589.01) == 1.0)
cg = pd.read_csv(os.path.join(OUT, "rpg2020_cells.csv")); TH = np.arange(0, 1801, 25)
om = np.array([cg.a[cg.g < T].sum() / cg.a.sum() for T in TH]); check("7 omission non-decreasing in threshold (RPG 2020 cells)", (np.diff(om) >= 0).all())
check("8 area-weighted omission within [0,1]", ((om >= 0) & (om <= 1)).all())
ix = V.overlay(P([inside])); cen = P([inside]).to_crs(2154).geometry.centroid.to_crs(4326); r, c = V.cell_of(cen.x.values, cen.y.values)
check("9 centroid and intersection agree for parcel inside one cell", (r[0], c[0]) == (ix.r.iloc[0], ix.c.iloc[0]) and V.omit(ix.a.values, ix.g.values, 900) == V.omit(np.ones(1), V.g5[r, c], 900))
val = pd.read_csv(os.path.join(OUT, "RPG_RICE_PARCEL_VALIDATION.csv")).set_index("source")
for T in (589, 900, 1100):
    for y in (2010, 2015, 2020, 2024):
        cy = pd.read_csv(os.path.join(OUT, f"rpg{y}_cells.csv")); ind = cy.a[cy.g < T].sum() / cy.a.sum()
        check(f"10 RPG {y} omission at T={T} reproduced from cell table", abs(ind - val.loc[f"RPG {y}", f"omit_area_T{T}"]) < 1e-5, f"{ind:.5f}")
L = np.load(os.path.join(V.EMA, "ema_layers_5m.npz")); g5, rice, cid = L["g5"], L["rice"], L["cid"]
c10 = pd.read_csv(os.path.join(OUT, "rpg2010_cells.csv")); fr = np.bincount(cid[cg.r, cg.c]).argmax(); sm = (cid == fr) & np.isfinite(g5) & (rice > 0)
cmp_ = pd.read_csv(os.path.join(OUT, "RPG_VS_MAPSPAM_COMPARISON.csv")).set_index("threshold_gdd10")
inn = sum(rice[r_, c_] for r_, c_ in zip(c10.r, c10.c) if sm[r_, c_]) / rice[sm].sum()
check("11 MapSPAM France share in RPG 2010 cells reproduced by loop", abs(inn - cmp_.loc[589, "MapSPAM2010 France share_in_RPG2010_cells"]) < 1e-4, f"{inn:.4f}")
for T in (589, 900):
    check(f"12 MapSPAM France omission at T={T} reproduced", abs(100 * rice[sm & (g5 < T)].sum() / rice[sm].sum() - cmp_.loc[T, "MapSPAM2010 France omit_area_pct"]) < 1e-3)
check("13 France area sum equals declared area (RPG 2020, <0.1%)", abs(val.loc["RPG 2020", "rice_area_ha"] / val.loc["RPG 2020", "area_ha_declared"] - 1) < 1e-3)
df = pd.DataFrame(res); df.to_csv(os.path.join(OUT, "RPG_KNOWN_ANSWER_TESTS.csv"), index=False)
open(os.path.join(OUT, "RPG_KNOWN_ANSWER_TESTS.md"), "w").write("# RPG known-answer tests\n\nOracle: planar shapely areas (degrees) on a synthetic 2 × 2 grid of 0.1° cells and plain numpy loops over saved cell tables; production functions `overlay`, `omit`, `cell_of` from `rpg_validation.py` are the units under test. Tolerance for projected-vs-planar area fractions: 0.005.\n\n| # | Test | Result | Detail |\n|---|---|---|---|\n" + "\n".join(f"| {i+1} | {r.test} | {r.result} | {r.detail} |" for i, r in df.iterrows()) + f"\n\n**Summary: {(df.result=='PASS').sum()}/{len(df)} PASS.**\n")
print(df.to_string()); print((df.result == "PASS").sum(), "/", len(df))
