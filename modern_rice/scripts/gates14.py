#!/usr/bin/env python3
"""Gates 1 & 4: GMIA irrigation overlay + spatial-block validation + economics."""
import numpy as np, pandas as pd, os, csv, rasterio
from rasterio.warp import reproject, Resampling

RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "modern_rice")

# --- Gate 1: GMIA aei% aggregated to candidate regions ---
aei = np.loadtxt(os.path.join(RAW, "gmia_v5_aei_pct.asc"), skiprows=6)
aei[aei < 0] = np.nan
with rasterio.open(os.path.join(OUT, "suitability_class_10m.tif")) as s:
    cls = s.read(1); prof = s.profile; tf = s.transform
# GMIA is 5-min: block-mean to 10-min
aei10 = np.nanmean(np.stack([aei[r::2, c::2] for r in range(2) for c in range(2)]), axis=0)
REGIONS = {
 "LowerDanube": (22,30,43,46), "Balkans": (17,23,44,47), "SUkraine": (30,36,45.5,48),
 "CentralAsia": (55,75,37,48), "CentralChile": (-72.5,-70,-37,-33),
 "Camargue": (4,5.5,43,44), "PoValley": (7.5,12.5,44.5,46), "Ebro": (-1,1.5,40.5,42.5),
 "England": (-2,2,50,53.5), "NFrance": (-1,5,47.5,50), "Germany": (6,15,47.5,54),
 "KazakhstanN": (50,70,45,55), "Uruguay_RGDS": (-58,-49,-35,-28), "Bangladesh": (88,92.5,21,26.5),
}
inv = ~tf
rows=[]
for r,(x0,x1,y0,y1) in REGIONS.items():
    c0,r0 = map(int, inv*(x0,y1)); c1,r1 = map(int, inv*(x1,y0))
    sc = cls[r0:r1, c0:c1]; sa = aei10[r0:r1, c0:c1]
    feas = sc >= 2
    rows.append([r, int((sc>=1).sum()), int(feas.sum()),
                 round(np.nanmean(sa),1), round(np.nanmean(sa[feas]) if feas.any() else np.nan,1)])
with open(os.path.join(OUT, "IRRIGATION_GMIA_CANDIDATES.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["region","feasible_or_marginal_cells","feasible_cells","mean_AEI_pct_region","mean_AEI_pct_feasible_cells"])
    w.writerows(rows)

# --- Gate 4: spatial-block validation ---
# Block CV: 30x30-degree blocks; fit = feasible class frequency among rice cells
# in training blocks; evaluate detection rate in held-out block.
lon = (np.arange(cls.shape[1]) * tf.a + tf.c)
lat = (np.arange(cls.shape[0]) * tf.e + tf.f)
with rasterio.open(os.path.join(RAW, "spam2010V2r0_global_H_RICE_A.tif")) as s:
    stf = s.transform
    rc = np.empty((s.height, s.width), dtype=np.float32)
    reproject(cls, rc, src_transform=tf, src_crs="EPSG:4326",
              dst_transform=stf, dst_crs="EPSG:4326", resampling=Resampling.nearest)
    area = s.read(1).astype(np.float32); area[area == s.nodata] = 0
rc = np.nan_to_num(rc, nan=-1).astype(np.int8)
slon = np.arange(rc.shape[1]) * stf.a + stf.c
slat = np.arange(rc.shape[0]) * stf.e + stf.f
BX = ((slon[None, :] + 180) // 30).astype(int)
BY = ((slat[:, None] + 90) // 30).astype(int)
blocks = [(by,bx) for by in np.unique(BY) for bx in np.unique(BX)]
res = []
for (by, bx) in sorted(blocks):
    m_test = (BY == by) & (BX == bx)
    a_test = np.nansum(area[m_test])
    if a_test <= 0: continue
    hits = np.nansum(area[m_test & (rc >= 2)])
    res.append([by, bx, round(a_test, 0), round(hits / a_test, 3)])
v = pd.DataFrame(res, columns=["block_lat", "block_lon", "rice_area_ha", "feasible_coverage"])
v.to_csv(os.path.join(OUT, "SPATIAL_BLOCK_VALIDATION.csv"), index=False)
print(v.describe().to_string())

# --- Gate 3: economics from FAOSTAT prices ---
FP = os.path.join(RAW, "Prices_E_All_Data_(Normalized).csv")
if not os.path.exists(FP):
    import zipfile; zipfile.ZipFile(os.path.join(RAW, "faostat_prices.zip")).extractall(RAW)
pr = pd.read_csv(FP, usecols=["Area", "Item", "Element", "Year", "Value", "Unit"], low_memory=False)
pr = pr[pr.Item.isin(["Wheat", "Barley", "Maize (corn)", "Rice"])]
prl = pr[pr.Element.str.contains("Producer Price")].groupby(["Area", "Item"]).apply(
    lambda g: g.loc[g.Year == g.Year.max()][["Year", "Value", "Unit"]].iloc[0], include_groups=False)
prl.to_csv(os.path.join(OUT, "AGRICULTURAL_ECONOMICS_PRICES.csv"))
print("done")
