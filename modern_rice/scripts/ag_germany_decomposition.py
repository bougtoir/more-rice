#!/usr/bin/env python3
"""Controlled decomposition of the Germany thermal-gate contrast (97% at T* = 589 vs 3% at 900 GDD10).
Both endpoints apply a threshold to the same German surface (WorldClim 2.1 1970-2000 monthly tavg, 5', pipeline
window 29 Apr-11 Sep, SPAM 2010 incumbent-arable weights, Natural Earth Germany). They differ only in the threshold,
whose construction differs in dataset, baseline, temporal aggregation, support and reference location/quantile.
This script varies those factors one at a time (and factorially where valid) and reports Germany's pass share."""
import os, json, numpy as np, pandas as pd, rasterio, geopandas as gpd
from rasterio.features import rasterize
from rasterio.transform import from_origin
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "..", "data", "raw")
OUT = os.path.join(HERE, "..", "..", "outputs", "modern_rice", "applied_geography")
WIN = {"pipeline_29Apr_11Sep": {4: 2, 5: 31, 6: 30, 7: 31, 8: 31, 9: 11}, "calendar_Jun_Sep": {6: 30, 7: 31, 8: 31, 9: 30}}
DOY = {"pipeline_29Apr_11Sep": (119, 254), "calendar_Jun_Sep": (152, 273)}   # inclusive day-of-year (non-leap)
CPD = {"2.5m": 24, "5m": 12, "10m": 6}
def rd(res, m, w, e, s, n):
    c = CPD[res]
    with rasterio.open(os.path.join(RAW, f"wc2.1_{res}_tavg_{m:02d}.tif")) as src:
        a = src.read(1, window=((int(round((90 - n) * c)), int(round((90 - s) * c))), (int(round((w + 180) * c)), int(round((e + 180) * c))))).astype(np.float64)
    a[a < -1e30] = np.nan; return a
def gdd(res, win, box): return sum(np.maximum(rd(res, m, *box) - 10, 0) * d for m, d in WIN[win].items())
def spam(crop, box):
    w, e, s, n = box
    with rasterio.open(os.path.join(RAW, f"spam2010V2r0_global_H_{crop}_A.tif")) as src: a = src.read(1).astype(np.float64)
    if a.shape[0] < 2160: a = np.vstack([a, np.zeros((2160 - a.shape[0], a.shape[1]))])
    a[a < 0] = 0; return a[int(round((90 - n) * 12)):int(round((90 - s) * 12)), int(round((w + 180) * 12)):int(round((e + 180) * 12))]
def to5(a, res):     # map a native-resolution field onto the 5' grid (mean of 2.5' sub-cells / replicate 10')
    if res == "5m": return a
    if res == "2.5m": h, w = a.shape[0] // 2 * 2, a.shape[1] // 2 * 2; return np.nanmean(a[:h, :w].reshape(h // 2, 2, w // 2, 2), axis=(1, 3))
    return np.repeat(np.repeat(a, 2, 0), 2, 1)
def wq(v, wt, q):
    m = np.isfinite(v) & (wt > 0); o = np.argsort(v[m]); cw = np.cumsum(wt[m][o]) / wt[m].sum(); return float(v[m][o][np.searchsorted(cw, q)])
# ---- Hokkaido rice reference (same masking as ag_grid_gates.calib) ----
HB = (139.3, 146.0, 41.35, 45.6)
rH = spam("RICE", HB); lat = 90 - (np.arange(int(round((90 - 45.6) * 12)), int(round((90 - 41.35) * 12))) + .5) / 12
lon = -180 + (np.arange(int(round((139.3 + 180) * 12)), int(round((146 + 180) * 12))) + .5) / 12
LA, LO = np.meshgrid(lat, lon, indexing="ij"); rH[(LO > 140.6) & (LA < 41.6)] = 0
def ref_grid(res, win, q):
    g = to5(gdd(res, win, HB), res)[:rH.shape[0], :rH.shape[1]]; return wq(g, rH, q)
def cell_at(res, win, la, lo):
    c = CPD[res]; g = gdd(res, win, (lo - 0.5, lo + 0.5, la - 0.5, la + 0.5)); return float(g[int((la + 0.5 - la) * c), int((lo - (lo - 0.5)) * c)])
# ---- NASA POWER point references ----
def power(name, period, win, monthly=False):
    f = os.path.join(RAW, f"nasa_power_{name}.json") if period == "2000-2024" else os.path.join(RAW, "nasa_power_1981_2000", f"nasa_power_{name}_19810101_20001231.json")
    p = json.load(open(f))["properties"]["parameter"]
    df = pd.DataFrame({"tx": p["T2M_MAX"], "tn": p["T2M_MIN"]}); df.index = pd.to_datetime(df.index); df = df[(df.tx > -900) & (df.tn > -900)]
    df["t"] = (df.tx + df.tn) / 2
    if monthly:  # climatological monthly means, then the fractional-month formula used on WorldClim
        mm = df.t.groupby(df.index.month).mean(); return float(sum(max(mm[m] - 10, 0) * d for m, d in WIN[win].items()))
    a, b = DOY[win]; doy = df.index.dayofyear - ((df.index.is_leap_year) & (df.index.month > 2)).astype(int)
    s = df[(doy >= a) & (doy <= b)]; return float(np.maximum(s.t - 10, 0).groupby(s.index.year).sum().mean())
# ---- German surface ----
GB = (5.5, 15.5, 47.0, 55.5)
ne = gpd.read_file(os.path.join(RAW, "ne_50m_admin_0_countries", "ne_50m_admin_0_countries.shp"))
ny, nx = int(round((55.5 - 47) * 12)), int(round((15.5 - 5.5) * 12))
de = rasterize([(ne[ne.ADMIN == "Germany"].geometry.iloc[0], 1)], out_shape=(ny, nx), transform=from_origin(5.5, 55.5, 1 / 12, 1 / 12), fill=0, dtype="uint8").astype(bool)
inc = sum(spam(c, GB) for c in ["WHEA", "MAIZ", "BARL", "POTA"])
G5 = {w: gdd("5m", w, GB) for w in WIN}; valid = de & (inc > 0) & np.isfinite(G5["pipeline_29Apr_11Sep"])
def de_share(T, res, win):
    p = (gdd(res, win, GB) >= T).astype(float); p[~np.isfinite(gdd(res, win, GB))] = np.nan; p = to5(p, res)[:ny, :nx]
    ok = valid & np.isfinite(p); return float((inc * p)[ok].sum() / inc[ok].sum())
rows = []
def add(block, label, T, res, win, note=""):
    T = float(round(T))  # thresholds rounded to whole GDD10, as in ag_grid_gates (T* = round(P05))
    rows.append(dict(block=block, label=label, threshold_gdd10=round(T, 1), surface_resolution=res, surface_window=win, germany_pass_pct=round(100 * de_share(T, res, win), 2),
                     germany_incumbent_Mha=round(inc[valid].sum() / 1e6, 3), note=note))
P, J = "pipeline_29Apr_11Sep", "calendar_Jun_Sep"
# 0. endpoint reproduction
add("0_endpoints", "T* = Hokkaido rice-area P05, WorldClim 5', pipeline window", ref_grid("5m", P, .05), "5m", P, "manuscript 97% endpoint")
add("0_endpoints", "900 GDD10 (rounded NASA POWER Hokkaido point, 2000-2024)", 900, "5m", P, "manuscript 3% endpoint")
# 1. threshold path (pipeline window, 5' German surface held fixed)
path = [("a POWER point 43.2N 143.0E, daily, 2000-2024", power("Hokkaido_JP", "2000-2024", P)),
        ("b same point, daily, 1981-2000 (baseline harmonised)", power("Hokkaido_JP", "1981-2000", P)),
        ("c same point, 1981-2000, monthly-mean GDD formula", power("Hokkaido_JP", "1981-2000", P, monthly=True)),
        ("d WorldClim 5' cell at the same point (1970-2000)", cell_at("5m", P, 43.2, 143.0)),
        ("e WorldClim rice-area P50 (Hokkaido)", ref_grid("5m", P, .50)),
        ("f WorldClim rice-area P05 (= T*)", ref_grid("5m", P, .05))]
for lab, T in path: add("1_threshold_path_pipeline_5m", lab, T, "5m", P)
# 2. window: each reference re-derived in the Jun-Sep window and applied to the Jun-Sep surface
for lab, T in [("a POWER point daily 2000-2024", power("Hokkaido_JP", "2000-2024", J)), ("b POWER point daily 1981-2000", power("Hokkaido_JP", "1981-2000", J)),
               ("c POWER point monthly 1981-2000", power("Hokkaido_JP", "1981-2000", J, True)), ("d WorldClim cell at point", cell_at("5m", J, 43.2, 143.0)),
               ("e WorldClim rice P50", ref_grid("5m", J, .5)), ("f WorldClim rice P05", ref_grid("5m", J, .05))]:
    add("2_threshold_path_JunSep_5m", lab, T, "5m", J)
add("2_window_mismatch", "pipeline T* (589) applied to Jun-Sep surface (invalid mix)", ref_grid("5m", P, .05), "5m", J, "window-inconsistent; shown only to expose the mismatch")
add("2_window_mismatch", "900 applied to Jun-Sep surface (invalid mix)", 900, "5m", J, "window-inconsistent")
# 3. alternative point references (location of the single point)
for nm, la, lo in [("Asahikawa_JP", 43.8, 142.4), ("Iwamizawa_Sorachi_JP", 43.2, 141.8), ("Sapporo_Ishikari_JP", 43.2, 141.5)]:
    add("3_point_location_pipeline_5m", f"POWER {nm} daily 1981-2000", power(nm, "1981-2000", P), "5m", P)
    add("3_point_location_pipeline_5m", f"WorldClim 5' cell at {nm}", cell_at("5m", P, la, lo), "5m", P)
add("3_point_location_pipeline_5m", "POWER Asahikawa_JP daily 2000-2024", power("Asahikawa_JP", "2000-2024", P), "5m", P)
# 4. resolution: reference recalibrated on the same grid as the German surface; and fixed threshold across grids
for res in ["2.5m", "5m", "10m"]:
    for win in [P, J]:
        add("4_resolution_recalibrated", f"rice-area P05 recalibrated at {res}", ref_grid(res, win, .05), res, win)
        add("4_resolution_fixed_900", "900 fixed", 900, res, win)
rice_pt = float(rH[int((45.6 - 43.2) * 12) - 6:int((45.6 - 43.2) * 12) + 6, int((143.0 - 139.3) * 12) - 6:int((143.0 - 139.3) * 12) + 6].sum())
df = pd.DataFrame(rows); df.to_csv(os.path.join(OUT, "GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv"), index=False)
json.dump({"spam_rice_ha_within_0.5deg_of_POWER_Hokkaido_point": round(rice_pt), "hokkaido_rice_ha": round(float(rH.sum())),
           "germany_point_POWER_pipeline_2000_2024": round(power("Germany", "2000-2024", P)), "germany_point_POWER_pipeline_1981_2000": round(power("Germany", "1981-2000", P))},
          open(os.path.join(OUT, "GERMANY_THERMAL_CONTRAST_META.json"), "w"), indent=1)
pd.set_option("display.width", 250); print(df[["block", "label", "threshold_gdd10", "surface_resolution", "surface_window", "germany_pass_pct"]].to_string()); print(open(os.path.join(OUT, "GERMANY_THERMAL_CONTRAST_META.json")).read())
