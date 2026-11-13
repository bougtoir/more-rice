#!/usr/bin/env python3
"""Threshold-dependent coverage of mapped existing rice area and classification stability.

One fixed primary surface: WorldClim 2.1 5' monthly tavg (1970-2000), GDD10 over the
pipeline window (29 Apr-11 Sep), Natural Earth Europe excluding Russia, SPAM 2010 v2.0
harvested area (all technologies). For each GDD10 threshold the script reports
incumbent-arable pass area (wheat+maize+barley+potato harvested area) and the mapped
SPAM rice harvested area that falls in cells failing the threshold ("omitted").
Non-rice cropland is NOT a verified negative, so no specificity/precision/AUC is computed.
Outputs: outputs/modern_rice/ema/.
"""
import os, json, numpy as np, pandas as pd, rasterio, geopandas as gpd
from rasterio.features import rasterize
from rasterio.transform import from_origin
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "data", "raw")
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
AG = os.path.join(ROOT, "outputs", "modern_rice", "applied_geography")
OUT = os.path.join(ROOT, "outputs", "modern_rice", "ema"); FIG = os.path.join(OUT, "figures"); os.makedirs(FIG, exist_ok=True)
W, E, S, N = -11.0, 45.0, 34.0, 71.5
WIN_PIPE = {4: 2, 5: 31, 6: 30, 7: 31, 8: 31, 9: 11}; WIN_CAL = {6: 30, 7: 31, 8: 31, 9: 30}
AEI_MIN = 0.10

def win(cpd): return slice(int(round((90 - N) * cpd)), int(round((90 - S) * cpd))), slice(int(round((W + 180) * cpd)), int(round((E + 180) * cpd)))
def wc(res, var, m, sl):
    with rasterio.open(os.path.join(RAW, f"wc2.1_{res}_{var}_{m:02d}.tif")) as s:
        a = s.read(1, window=((sl[0].start, sl[0].stop), (sl[1].start, sl[1].stop))).astype(np.float32)
    a[a < -1e30] = np.nan; return a
def gdd(res, wd, sl): return sum(np.maximum(wc(res, "tavg", m, sl) - 10, 0) * d for m, d in wd.items())
def spam(crop, sl, tech="A"):
    with rasterio.open(os.path.join(RAW, f"spam2010V2r0_global_H_{crop}_{tech}.tif")) as s: a = s.read(1).astype(np.float64)
    if a.shape[0] < 2160: a = np.vstack([a, np.zeros((2160 - a.shape[0], a.shape[1]))])
    a[a < 0] = 0; return a[sl]
def cell_area_ha(cpd, sl):
    lt = 90 - np.arange(sl[0].start, sl[0].stop) / cpd; lb = lt - 1 / cpd
    a = 6371.0072 ** 2 * np.deg2rad(1 / cpd) * (np.sin(np.deg2rad(lt)) - np.sin(np.deg2rad(lb))) * 100
    return np.repeat(a[:, None], sl[1].stop - sl[1].start, 1)
def block_mean(a, k):
    h, w = a.shape[0] // k * k, a.shape[1] // k * k
    return np.nanmean(a[:h, :w].reshape(h // k, k, w // k, k), axis=(1, 3))

sl5, sl25, sl10 = win(12), win(24), win(6); ny, nx = sl5[0].stop - sl5[0].start, sl5[1].stop - sl5[1].start
g5 = gdd("5m", WIN_PIPE, sl5); g5c = gdd("5m", WIN_CAL, sl5); g25 = gdd("2.5m", WIN_PIPE, sl25); g10 = gdd("10m", WIN_PIPE, sl10)
inc = sum(spam(c, sl5) for c in ["WHEA", "MAIZ", "BARL", "POTA"]); rice = spam("RICE", sl5); rice_I = spam("RICE", sl5, "I")
aei = np.loadtxt(os.path.join(RAW, "gmia_v5_aei_ha.asc"), skiprows=6)[sl5]; aei[aei < 0] = 0
area = cell_area_ha(12, sl5); aei_sh = np.clip(aei / area, 0, 1)
ne = gpd.read_file(os.path.join(RAW, "ne_50m_admin_0_countries", "ne_50m_admin_0_countries.shp")).cx[W - 5:E + 5, S - 5:N + 5].reset_index(drop=True)
tr5 = from_origin(W, N, 1 / 12, 1 / 12)
cid = rasterize([(g, i + 1) for i, g in enumerate(ne.geometry)], out_shape=(ny, nx), transform=tr5, fill=0, dtype="int32")
names = {i + 1: n for i, n in enumerate(ne["NAME_EN"])}; names[0] = "unassigned"
eur = rasterize([(g, 1) for g in ne[(ne["CONTINENT"] == "Europe") & (ne["ADMIN"] != "Russia")].geometry], out_shape=(ny, nx), transform=tr5, fill=0, dtype="uint8").astype(bool)
cal = json.load(open(os.path.join(AG, "GRID_THERMAL_CALIBRATION.json"))); TS = cal["T_star_pipeline"]
gde = pd.read_csv(os.path.join(AG, "GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv"))
valid = np.isfinite(g5) & (inc > 0) & eur                      # incumbent-arable denominator cells
rmask = np.isfinite(g5) & eur & (rice > 0)                      # all mapped rice cells in domain
R = rice[rmask].sum(); I = inc[valid].sum()
de_id = [k for k, v in names.items() if v == "Germany"][0]; de = valid & (cid == de_id)

def wq(v, w, q):
    o = np.argsort(v); c = np.cumsum(w[o]) / w.sum(); return float(v[o][np.searchsorted(c, q)])
eu_q = {f"P{int(q*1000)/10:g}": round(wq(g5[rmask], rice[rmask], q), 0) for q in [0.01, 0.05, 0.10, 0.25, 0.50]}

# ---------------- named references (provenance differs; different estimands) ----------------
p1 = gde[gde.block == "1_threshold_path_pipeline_5m"].reset_index(drop=True)
REFS = {cal["hokkaido_P01_pipeline"]: "Hokkaido SPAM rice-area P01, WorldClim 5' (grid)",
        TS: "T*: Hokkaido SPAM rice-area P05, WorldClim 5' (grid; primary)",
        cal["hokkaido_P10_pipeline"]: "Hokkaido SPAM rice-area P10, WorldClim 5' (grid)",
        float(p1.threshold_gdd10[3]): "WorldClim 5' cell at the Hokkaido POWER point (grid point)",
        float(p1.threshold_gdd10[2]): "POWER Hokkaido point 1981-2000 monthly formula",
        float(p1.threshold_gdd10[1]): "POWER Hokkaido point 1981-2000 daily",
        cal["hokkaido_P50_pipeline"]: "Hokkaido SPAM rice-area P50, WorldClim 5' (grid)",
        900.0: "~900: rounded POWER Hokkaido point 2000-2024 daily (earlier numerical reference)",
        float(p1.threshold_gdd10[0]): "POWER Hokkaido point 2000-2024 daily (unrounded)",
        cal["NH35plus_P05_pipeline"]: "All SPAM rice north of 35N, rice-area P05 (grid)",
        eu_q["P5"]: "European SPAM rice-area P05 (in-sample for Europe; diagnostic only)"}
TH = sorted(set(range(0, 1801, 25)) | set(REFS))

def row(T):
    tp = g5 >= T; comb = tp & (aei_sh >= AEI_MIN)
    om = rice[rmask & ~tp].sum(); om_inc = rice[rmask & ~tp & (inc > 0)].sum(); r_inc = rice[rmask & (inc > 0)].sum()
    return dict(threshold_gdd10=T, reference_label=REFS.get(T, ""),
                cropland_pass_ha=round(inc[valid & tp].sum(), 0), cropland_pass_pct=round(100 * inc[valid & tp].sum() / I, 3),
                cropland_thermal_aei_pct=round(100 * inc[valid & comb].sum() / I, 3),
                germany_cropland_pass_pct=round(100 * inc[de & tp].sum() / inc[de].sum(), 3),
                rice_mapped_ha=round(R, 1), rice_pass_ha=round(rice[rmask & tp].sum(), 1), rice_omitted_ha=round(om, 1), rice_omitted_pct=round(100 * om / R, 3),
                rice_omitted_pct_incumbent_cells=round(100 * om_inc / r_inc, 3),
                rice_in_thermal_aei_pct=round(100 * rice[rmask & comb].sum() / R, 3),
                rice_omitted_pct_2p5m_subcell=round(100 * float((rice * (1 - np.nan_to_num(block_mean(np.where(np.isnan(g25), np.nan, (g25 >= T).astype(np.float32)), 2)[:ny, :nx], nan=0)))[rmask].sum()) / R, 3))
curve = pd.DataFrame([row(T) for T in TH]); curve.to_csv(os.path.join(OUT, "THRESHOLD_OMISSION_CURVE.csv"), index=False)

# ---------------- grid alignment / support sensitivity at key thresholds ----------------
KEY = [TS, 900.0, 1100.0]
al = []
for T in KEY:
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            rs = np.roll(np.roll(rice, di, 0), dj, 1); m = np.isfinite(g5) & eur & (rs > 0)
            al.append(dict(threshold_gdd10=T, test=f"rice grid shifted ({di:+d},{dj:+d}) cells", rice_omitted_pct=round(100 * rs[m & (g5 < T)].sum() / rs[m].sum(), 3)))
    gmax = ndimage.maximum_filter(np.nan_to_num(g5, nan=-1), size=3)
    al.append(dict(threshold_gdd10=T, test="omitted only if all 3x3 neighbours fail", rice_omitted_pct=round(100 * rice[rmask & (gmax < T)].sum() / R, 3)))
    al.append(dict(threshold_gdd10=T, test="2.5' sub-cell pass fraction", rice_omitted_pct=float(curve.set_index("threshold_gdd10").loc[T, "rice_omitted_pct_2p5m_subcell"]) if T in TH else np.nan))
    g10u = np.repeat(np.repeat(g10, 2, 0), 2, 1)[:ny, :nx]
    al.append(dict(threshold_gdd10=T, test="10' native surface", rice_omitted_pct=round(100 * rice[rmask & np.isfinite(g10u) & (g10u < T)].sum() / R, 3)))
pd.DataFrame(al).to_csv(os.path.join(OUT, "OMISSION_ALIGNMENT_SENSITIVITY.csv"), index=False)

# ---------------- omission geography ----------------
geo = []
for c in np.unique(cid[rmask]):
    m = rmask & (cid == c); r = dict(country=names[c], rice_mapped_ha=round(rice[m].sum(), 1),
        rice_weighted_gdd10_median=round(wq(g5[m], rice[m], 0.5), 0), rice_irrigated_tech_share=round(rice_I[m].sum() / rice[m].sum(), 3))
    for T in KEY: r[f"omitted_ha_T{int(T)}"] = round(rice[m & (g5 < T)].sum(), 1)
    geo.append(r)
geo = pd.DataFrame(geo).sort_values("rice_mapped_ha", ascending=False); geo.to_csv(os.path.join(OUT, "RICE_OMISSION_BY_COUNTRY.csv"), index=False)
loo = []
for T in KEY:
    vals = [100 * rice[rmask & (cid != c) & (g5 < T)].sum() / rice[rmask & (cid != c)].sum() for c in np.unique(cid[rmask]) if rice[rmask & (cid == c)].sum() > 1000]
    loo.append(dict(threshold_gdd10=T, loco_min_pct=round(min(vals), 3), loco_max_pct=round(max(vals), 3)))
clus = {}
for T in KEY:
    om = rmask & (g5 < T); lab, n = ndimage.label(om, structure=np.ones((3, 3)))
    sizes = np.sort(ndimage.sum(rice, lab, range(1, n + 1)))[::-1] if n else np.array([0.0])
    clus[str(int(T))] = dict(omitted_cells=int(om.sum()), clusters_8conn=int(n), share_largest5_clusters=round(float(sizes[:5].sum() / max(sizes.sum(), 1e-9)), 3),
                             omitted_cells_with_rice_lt_1pct_of_cell=int((om & (rice / area < 0.01)).sum()),
                             omitted_ha_in_cells_rice_lt_1pct=round(float(rice[om & (rice / area < 0.01)].sum()), 1),
                             omitted_cells_gdd_zero=int((om & (g5 <= 0)).sum()), omitted_ha_gdd_zero=round(float(rice[om & (g5 <= 0)].sum()), 1))

# ---------------- classification stability ----------------
g25p = lambda T: np.nan_to_num(block_mean(np.where(np.isnan(g25), np.nan, (g25 >= T).astype(np.float32)), 2)[:ny, :nx], nan=0) >= 0.5
g10p = lambda T: np.repeat(np.repeat(g10 >= T, 2, 0), 2, 1)[:ny, :nx]
rc = gde[gde.block == "4_resolution_recalibrated"]
t25 = float(rc[(rc.surface_resolution == "2.5m") & rc.surface_window.str.startswith("pipeline")].threshold_gdd10.iloc[0]); t10 = float(rc[(rc.surface_resolution == "10m") & rc.surface_window.str.startswith("pipeline")].threshold_gdd10.iloc[0])
SPECS = {"S0 T*=589, 5', pipeline (primary)": g5 >= TS, "S1 900, 5', pipeline": g5 >= 900, f"S2 P05 recalibrated Jun-Sep ({cal['T_star_calJunSep']:.0f}), 5'": g5c >= cal["T_star_calJunSep"],
         f"S3 P05 recalibrated 2.5' ({t25:.0f}), majority of sub-cells": g25p(t25), f"S4 P05 recalibrated 10' ({t10:.0f})": g10p(t10), f"S5 Hokkaido P50 ({cal['hokkaido_P50_pipeline']:.0f}), 5'": g5 >= cal["hokkaido_P50_pipeline"]}
st = []
k0 = list(SPECS)[0]; A = SPECS[k0]
for dom, dm in [("Europe", valid), ("Germany", de)]:
    for k, B in SPECS.items():
        if k == k0: continue
        w = inc[dm]; a, b = A[dm], B[dm]
        st.append(dict(domain=dom, reference=k0, comparison=k, both_pass_ha=round(w[a & b].sum(), 0), ref_only_ha=round(w[a & ~b].sum(), 0), comp_only_ha=round(w[~a & b].sum(), 0), both_fail_ha=round(w[~a & ~b].sum(), 0),
                       agreement_pct=round(100 * w[a == b].sum() / w.sum(), 2), jaccard_pass=round(w[a & b].sum() / max(w[a | b].sum(), 1e-9), 4),
                       rice_omitted_pct_comp=round(100 * rice[rmask & ~B].sum() / R, 3) if dom == "Europe" else np.nan))
pd.DataFrame(st).to_csv(os.path.join(OUT, "CLASSIFICATION_STABILITY_PAIRS.csv"), index=False)
# 4-class gate transition T* -> 900
def cls(T):
    th = g5 >= T; c = np.zeros((ny, nx), np.int8)
    c[valid & ~th] = 1; c[valid & th & (aei_sh < AEI_MIN)] = 2; c[valid & th & (aei_sh >= AEI_MIN)] = 3; return c
c0, c1 = cls(TS), cls(900.0); LB = {1: "thermal not met", 2: "thermal met, AEI <10%", 3: "thermal met, AEI >=10%"}
tm = pd.DataFrame([[round(inc[valid & (c0 == i) & (c1 == j)].sum() / 1e6, 3) for j in LB] for i in LB], index=[f"T*={TS:.0f}: {LB[i]}" for i in LB], columns=[f"900: {LB[j]}" for j in LB])
tm.to_csv(os.path.join(OUT, "CLASSIFICATION_TRANSITION_MATRIX.csv"))

summ = dict(T_star=TS, incumbent_Mha=round(I / 1e6, 2), rice_mapped_ha=round(R, 1), rice_cells=int(rmask.sum()), europe_rice_gdd10_quantiles=eu_q,
            rice_irrigated_tech_share=round(float(rice_I[rmask].sum() / R), 4), rice_in_aei_cells_share=round(float(rice[rmask & (aei_sh >= AEI_MIN)].sum() / R), 4),
            rice_ha_in_cells_without_incumbent=round(float(rice[rmask & ~(inc > 0)].sum()), 1), loco=loo, clusters=clus,
            germany_incumbent_Mha=round(inc[de].sum() / 1e6, 3), t25=t25, t10=t10)
json.dump(summ, open(os.path.join(OUT, "EMA_THRESHOLD_SUMMARY.json"), "w"), indent=1)
np.savez_compressed(os.path.join(OUT, "ema_layers_5m.npz"), g5=g5, rice=rice, inc=inc, aei_sh=aei_sh, eur=eur, valid=valid, cid=cid)
print(json.dumps(summ, indent=1)); print(curve[curve.reference_label != ""].to_string()); print(pd.DataFrame(al).to_string()); print(tm); print(pd.DataFrame(st).to_string()); print(geo.head(12).to_string())
