#!/usr/bin/env python3
"""Pilot global rice biophysical suitability screening.

Inputs: WorldClim 2.1 10-arcmin bioclim + monthly tavg + monthly prec.
Method: parameterized rule grid (no single threshold).
  Thermal feasibility: >= N consecutive months with tavg >= T_REQ,
  within frost-free window (months with tavg > 0), plus GDD10 >= GDD_REQ.
  Rainfed water: precipitation accumulated over the N warmest consecutive
  months >= P_REQ (irrigated class ignores precip).
Classes: feasible_irrigated / feasible_rainfed / marginal / infeasible.
Validation: SPAM2010 v2.0 rice harvested-area fraction per cell (resampled)
must fall mostly inside feasible cells; report sensitivity/specificity-style
diagnostics and per-region summaries.
"""
import os, glob, csv, numpy as np, rasterio
from rasterio.warp import reproject, Resampling

RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "modern_rice")
os.makedirs(OUT, exist_ok=True)

def read(name):
    with rasterio.open(os.path.join(RAW, name)) as s:
        a = s.read(1).astype(np.float32)
        a[a == s.nodata] = np.nan
        return a

def path(p): return os.path.join(RAW, p)

# --- inputs ---
bio10 = read("wc2.1_10m_bio_10.tif")   # mean temp warmest quarter (C x10)
bio11 = read("wc2.1_10m_bio_11.tif")   # mean temp coldest quarter
bio12 = read("wc2.1_10m_bio_12.tif")   # annual precip mm
tavg = np.stack([read(f"wc2.1_10m_tavg_{m:02d}.tif") for m in range(1, 13)])
prec = np.stack([read(f"wc2.1_10m_prec_{m:02d}.tif") for m in range(1, 13)])
bio10, bio11 = bio10 / 10.0, bio11 / 10.0

# monthly stats
days = np.array([31,28,31,30,31,30,31,31,30,31,30,31], dtype=np.float32)
gdd10 = (np.maximum(tavg - 10.0, 0) * days[:, None, None]).sum(axis=0)
frost_free_months = (tavg > 0.0).sum(axis=0)

def longest_run(mask):
    """longest run of True along axis 0 (circular, allows wrap-around)."""
    m2 = np.concatenate([mask, mask], axis=0)
    out = np.zeros(mask.shape[1:], dtype=np.int16)
    for i in range(24):
        cur = m2[i]
        out = np.where(cur & (i > 0), out + 1, out)
        out = np.where(cur & (i == 0), 1, out)
    # correct: recompute properly with running counter
    run = np.zeros(mask.shape[1:], dtype=np.int16)
    best = np.zeros_like(run)
    for i in range(24):
        run = np.where(m2[i], run + 1, 0)
        best = np.maximum(best, run)
    return best

warm18 = longest_run(tavg >= 18.0)
warm20 = longest_run(tavg >= 20.0)
# precip over the 4-month window centered on warmest months: use prec of the
# 4 months with highest tavg (per cell) as growing-season rain proxy
order = np.argsort(-tavg, axis=0)
warm4_prec = np.take_along_axis(prec, order[:4], axis=0).sum(axis=0)
warm3_prec = np.take_along_axis(prec, order[:3], axis=0).sum(axis=0)

# --- classification grid ---
# thermal parameter combos
combos = [
    ("strict20x4", warm20 >= 4),
    ("20x3",       warm20 >= 3),
    ("18x4",       warm18 >= 4),
    ("18x3",       warm18 >= 3),
]
GDD_REQ = 1800
thermal_strict = warm20 >= 4
thermal_loose  = (warm18 >= 3) & (gdd10 >= GDD_REQ) & (frost_free_months >= 4)
RAIN_REQ = 300  # mm over warmest-3-month season proxy for rainfed

cls = np.zeros(thermal_strict.shape, dtype=np.int8)  # 0 infeasible
cls[thermal_loose] = 1                                # marginal
cls[thermal_strict] = 2                               # feasible(irrig-dependent)
cls[(thermal_strict | thermal_loose) & (warm3_prec >= RAIN_REQ)] = 3  # feasible rainfed

# consistency across parameter combos: agreement fraction
agree = sum(c.astype(np.int8) for c in combos for _ in [0]) if False else None
n_feas = sum(c.sum() for _, c in combos)
agreement = sum(c.astype(np.int16) for _, c in combos)
param_uncertain = (agreement > 0) & (agreement < 4)

with rasterio.open(path("wc2.1_10m_bio_10.tif")) as s:
    profile = s.profile
profile.update(dtype="int8", count=1, nodata=-1)
cls[~np.isfinite(bio10)] = -1
with rasterio.open(os.path.join(OUT, "suitability_class_10m.tif"), "w", **profile) as d:
    d.write(cls, 1)

# --- validation vs SPAM rice ---
with rasterio.open(path("spam2010V2r0_global_H_RICE_A.tif")) as s:
    spam_prof = s.profile
    rice = np.empty((s.height, s.width), dtype=np.float32)
    reproject(cls, rice,
              src_transform=s.transform if False else profile["transform"],
              src_crs="EPSG:4326", dst_transform=s.transform,
              dst_crs="EPSG:4326", resampling=Resampling.nearest)
    with rasterio.open(path("spam2010V2r0_global_H_RICE_A.tif")) as s2:
        area = s2.read(1).astype(np.float32)
        area[area == s2.nodata] = np.nan
rice_class = np.nan_to_num(rice, nan=-1).astype(np.int8)
has_rice = (area > 0) & (rice_class >= 0)
tot = np.nansum(area[has_rice])
stats = {c: float(np.nansum(area[has_rice & (rice_class == c)])) for c in [0,1,2,3]}
with open(os.path.join(OUT, "VALIDATION_VS_SPAM.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["class", "rice_harv_area_ha_in_class", "share"])
    for c, lab in [(0,"infeasible"),(1,"marginal"),(2,"feasible_irrig_dependent"),(3,"feasible_rainfed")]:
        w.writerow([lab, round(stats[c],1), round(stats[c]/tot,4) if tot else ""])
    w.writerow(["param_uncertain_cells", int(param_uncertain.sum()), ""])

# --- regional summary ---
regions = {
 "Europe_W": (-12, 35, 40, 72),
 "EastAsia": (95, 145, 15, 50), "SAsia": (65, 95, 5, 35),
 "SSAmerica": (-75, -35, -40, 5), "SubSahara": (-20, 55, -35, 15),
 "NAmerica": (-125, -60, 20, 55), "Oceania": (110, 160, -45, -10),
 "WAfrica": (-20, 25, 0, 20), "SEAsia": (95, 145, -10, 25),
}
tf = profile["transform"]; inv = ~tf
with open(os.path.join(OUT, "REGIONAL_SUITABILITY_SUMMARY.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["region","infeasible","marginal","feas_irrig_dep","feas_rainfed","param_uncertain"])
    for r,(x0,x1,y0,y1) in regions.items():
        c0,r0 = map(int, inv*(x0,y1)); c1,r1 = map(int, inv*(x1,y0))
        sub = cls[r0:r1, c0:c1]; subu = param_uncertain[r0:r1, c0:c1]
        v = sub[sub>=0]
        w.writerow([r]+[int((v==k).sum()) for k in [0,1,2,3]]+[int(subu.sum())])
print("done")
