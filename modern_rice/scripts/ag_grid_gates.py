#!/usr/bin/env python3
"""European grid screen: thermal transfer, irrigation infrastructure and
rainfed climatic water balance, weighted by incumbent arable harvested area.

Inputs (modern_rice/data/raw): WorldClim 2.1 monthly tavg (2.5', 5', 10'),
tmin/tmax/prec (10'); MapSPAM 2010 v2.0 harvested area (5', all
technologies) for rice, wheat, maize, barley, potato; FAO GMIA v5 area
equipped for irrigation (ha, 5'); Natural Earth 1:50m admin-0.

Thermal metric: GDD10 over the pipeline window (29 Apr-11 Sep) from monthly
means with fractional month lengths, plus calendar Jun-Sep. Threshold T* is
calibrated on the same grid as the rice-area-weighted 5th percentile of
GDD10 across SPAM rice cells in Hokkaido (system-specific cold bound).
Water: AEI share of cell area (>=10% = existing irrigation infrastructure);
rainfed climatic balance D = sum_Jun-Sep (Kc*ET0_Hargreaves - P) with the
Kc schedule of upland_water_balance.py. Denominator: SPAM 2010 harvested
area of wheat+maize+barley+potato ('incumbent arable', ha); outputs are
exposure of incumbent arable area to gate classes, NOT convertible area.
"""
import os, ast, json, numpy as np, pandas as pd, rasterio, geopandas as gpd
from rasterio.features import rasterize
from rasterio.transform import from_origin
HERE = os.path.dirname(__file__)
RAW = os.path.join(HERE, "..", "data", "raw")
OUT = os.path.join(HERE, "..", "..", "outputs", "modern_rice", "applied_geography")
os.makedirs(OUT, exist_ok=True)
W, E, S, N = -11.0, 45.0, 34.0, 71.5          # Europe window
RES = {"2.5m": 24, "5m": 12, "10m": 6}         # cells per degree
WIN_PIPE = {4: 2, 5: 31, 6: 30, 7: 31, 8: 31, 9: 11}
WIN_CAL = {6: 30, 7: 31, 8: 31, 9: 30}
AEI_MIN = 0.10

def win(cpd, w=W, e=E, s=S, n=N):
    return slice(int(round((90 - n) * cpd)), int(round((90 - s) * cpd))), slice(int(round((w + 180) * cpd)), int(round((e + 180) * cpd)))

def wc(res, var, m, sl):
    with rasterio.open(os.path.join(RAW, f"wc2.1_{res}_{var}_{m:02d}.tif")) as s:
        a = s.read(1, window=((sl[0].start, sl[0].stop), (sl[1].start, sl[1].stop))).astype(np.float32)
        a[a < -1e30] = np.nan
    return a

def gdd(res, wdays, sl):
    return sum(np.maximum(wc(res, "tavg", m, sl) - 10, 0) * d for m, d in wdays.items())

def up(a, k, shape=None):
    r = np.repeat(np.repeat(a, k, 0), k, 1)
    if shape is None: return r
    o = np.full(shape, np.nan, np.float32); h, w = min(shape[0], r.shape[0]), min(shape[1], r.shape[1]); o[:h, :w] = r[:h, :w]; return o

def block_mean(a, k):
    h, w = a.shape[0] // k * k, a.shape[1] // k * k
    b = a[:h, :w].reshape(h // k, k, w // k, k)
    return np.nanmean(b, axis=(1, 3))

def spam(crop, sl):
    with rasterio.open(os.path.join(RAW, f"spam2010V2r0_global_H_{crop}_A.tif")) as s:
        a = s.read(1).astype(np.float64)
    a = np.vstack([a, np.zeros((2160 - a.shape[0], a.shape[1]))]) if a.shape[0] < 2160 else a
    a[a < 0] = 0
    return a[sl]

def cell_area_ha(cpd, sl):
    lat_top = 90 - np.arange(sl[0].start, sl[0].stop) / cpd
    lat_bot = lat_top - 1 / cpd
    R = 6371.0072
    a = R**2 * np.deg2rad(1 / cpd) * (np.sin(np.deg2rad(lat_top)) - np.sin(np.deg2rad(lat_bot))) * 100
    return np.repeat(a[:, None], sl[1].stop - sl[1].start, 1)

def hargreaves_monthly(sl10):
    lat = 90 - (np.arange(sl10[0].start, sl10[0].stop) + 0.5) / 6
    phi = np.deg2rad(lat)[:, None]
    out = {}
    mid = {6: 166, 7: 197, 8: 228, 9: 258}
    for m, doy in mid.items():
        dr = 1 + 0.033 * np.cos(2 * np.pi * doy / 365); dec = 0.409 * np.sin(2 * np.pi * doy / 365 - 1.39)
        ws = np.arccos(np.clip(-np.tan(phi) * np.tan(dec), -1, 1))
        Ra = 37.6 * dr * (ws * np.sin(phi) * np.sin(dec) + np.cos(phi) * np.cos(dec) * np.sin(ws))
        tx, tn = wc("10m", "tmax", m, sl10), wc("10m", "tmin", m, sl10)
        out[m] = 0.0023 * Ra * 0.408 * np.sqrt(np.clip(tx - tn, 0, None)) * ((tx + tn) / 2 + 17.8) * WIN_CAL[m]
    return out

# ---------------- base 5' layers ----------------
sl5 = win(12); sl10 = win(6); sl25 = win(24)
ny, nx = sl5[0].stop - sl5[0].start, sl5[1].stop - sl5[1].start
g5 = gdd("5m", WIN_PIPE, sl5); g5cal = gdd("5m", WIN_CAL, sl5)
inc = sum(spam(c, sl5) for c in ["WHEA", "MAIZ", "BARL", "POTA"])
rice = spam("RICE", sl5)
aei = np.loadtxt(os.path.join(RAW, "gmia_v5_aei_ha.asc"), skiprows=6)[sl5]; aei[aei < 0] = 0
area = cell_area_ha(12, sl5)
aei_sh = np.clip(aei / area, 0, 1)
KC = {6: (25 * 1.05 + 5 * 1.10) / 30, 7: 1.10, 8: (9 * 1.10 + 22 * 1.20) / 31, 9: (3 * 1.20 + 25 * 1.05) / 28}
et0 = hargreaves_monthly(sl10)
D10 = sum(KC[m] * et0[m] * (28 / 30 if m == 9 else 1) - wc("10m", "prec", m, sl10) * (28 / 30 if m == 9 else 1) for m in [6, 7, 8, 9])
D = up(D10, 2)[:ny, :nx]

# countries
ne = gpd.read_file(os.path.join(RAW, "ne_50m_admin_0_countries", "ne_50m_admin_0_countries.shp"))
ne = ne.cx[W - 5:E + 5, S - 5:N + 5].reset_index(drop=True)
tr5 = from_origin(W, N, 1 / 12, 1 / 12)
cid = rasterize([(g, i + 1) for i, g in enumerate(ne.geometry)], out_shape=(ny, nx), transform=tr5, fill=0, dtype="int32")
names = {i + 1: n for i, n in enumerate(ne["NAME_EN"] if "NAME_EN" in ne else ne["NAME"])}
# study domain: Natural Earth CONTINENT == Europe, excluding Russia (truncated by the 45E window edge);
# the rectangle alone would also include North Africa, Anatolia and the Caucasus
EUR_SEL = (ne["CONTINENT"] == "Europe") & (ne["ADMIN"] != "Russia")
eur = rasterize([(g, 1) for g in ne[EUR_SEL].geometry], out_shape=(ny, nx), transform=tr5, fill=0, dtype="uint8").astype(bool)

# ---------------- calibration on the same grid ----------------
def calib():
    slH = win(12, 139.3, 146.0, 41.35, 45.6)
    gH = gdd("5m", WIN_PIPE, slH); gHc = gdd("5m", WIN_CAL, slH); rH = spam("RICE", slH)
    lat = 90 - (np.arange(slH[0].start, slH[0].stop) + 0.5) / 12; lon = -180 + (np.arange(slH[1].start, slH[1].stop) + 0.5) / 12
    LA, LO = np.meshgrid(lat, lon, indexing="ij")
    rH[(LO > 140.6) & (LA < 41.6)] = 0                     # drop Shimokita (Honshu)
    def wq(v, w, q):
        m = np.isfinite(v) & (w > 0); o = np.argsort(v[m]); cw = np.cumsum(w[m][o]) / w[m].sum()
        return float(v[m][o][np.searchsorted(cw, q)])
    r = {"hokkaido_rice_ha": float(rH.sum())}
    for q in [0.01, 0.05, 0.10, 0.50]:
        r[f"hokkaido_P{int(q*100):02d}_pipeline"] = round(wq(gH, rH, q), 0)
        r[f"hokkaido_P{int(q*100):02d}_calJunSep"] = round(wq(gHc, rH, q), 0)
    slG = win(12, -180, 180, 35, 60)
    gG = gdd("5m", WIN_PIPE, slG); rG = spam("RICE", slG)
    for q in [0.01, 0.05]:
        r[f"NH35plus_P{int(q*100):02d}_pipeline"] = round(wq(gG, rG, q), 0)
    r["NH35plus_rice_ha"] = float(rG.sum())
    return r
cal = calib()
TSTAR = cal["hokkaido_P05_pipeline"]; TSTARc = cal["hokkaido_P05_calJunSep"]
json.dump(cal | {"T_star_pipeline": TSTAR, "T_star_calJunSep": TSTARc}, open(os.path.join(OUT, "GRID_THERMAL_CALIBRATION.json"), "w"), indent=1)
print("calibration", cal)

# ---------------- point cross-walk (POWER vs WorldClim grid) ----------------
src = open(os.path.join(HERE, "fetch_nasa_power.py")).read()
POINTS = ast.literal_eval(src.split("POINTS = ", 1)[1].split("\n}\n", 1)[0] + "\n}")
pw = pd.read_csv(os.path.join(OUT, "POINT_GDD_WINDOW_SENSITIVITY.csv")).set_index("point")
sb = pd.read_csv(os.path.join(HERE, "..", "..", "outputs", "modern_rice", "DAILY_SOIL_WATER_BALANCE.csv")).set_index("point")
cw = []
for k, (la, lo) in POINTS.items():
    if not (W <= lo < E and S <= la < N) or k not in pw.index: continue
    i, j = int((N - la) * 12), int((lo - W) * 12)
    cw.append(dict(point=k, lat=la, lon=lo, power_gdd_pipeline=pw.loc[k, "pipeline_29Apr_11Sep"], grid_gdd_pipeline=round(float(g5[i, j]), 0),
                   power_gdd_calJunSep=pw.loc[k, "calendar_Jun_Sep"], grid_gdd_calJunSep=round(float(g5cal[i, j]), 0),
                   grid_D_mm=round(float(D[i, j]), 0), bucket_P_flower_deficit_pct=sb.P_flower_deficit_10d_pct.get(k, np.nan),
                   aei_share=round(float(aei_sh[i, j]), 3), incumbent_ha=round(float(inc[i, j]), 0)))
cw = pd.DataFrame(cw); cw.to_csv(os.path.join(OUT, "POINT_GRID_CROSSWALK.csv"), index=False)
print(cw.to_string())

# ---------------- gate cascade ----------------
thermal = g5 >= TSTAR
cls = np.zeros((ny, nx), np.int8)
valid = np.isfinite(g5) & (inc > 0) & eur
cls[valid & ~thermal] = 1
cls[valid & thermal & (aei_sh < AEI_MIN) & (D > 0)] = 2
cls[valid & thermal & (aei_sh < AEI_MIN) & (D <= 0)] = 3
cls[valid & thermal & (aei_sh >= AEI_MIN)] = 4
LAB = {1: "thermal_fail", 2: "thermal_pass_no_irrig_infra_rainfed_deficit", 3: "thermal_pass_no_irrig_infra_rainfed_balance_nonneg", 4: "thermal_pass_irrig_infra_present"}
np.save(os.path.join(OUT, "grid_class_5m.npy"), cls)
np.save(os.path.join(OUT, "grid_gdd_5m.npy"), g5); np.save(os.path.join(OUT, "grid_inc_5m.npy"), inc)
with rasterio.open(os.path.join(OUT, "EUROPE_GATE_CLASS_5m.tif"), "w", driver="GTiff", height=ny, width=nx, count=1, dtype="int8", crs="EPSG:4326", transform=tr5, compress="deflate") as d:
    d.write(cls, 1)
rows = []
for c in np.unique(cid[valid]):
    if c == 0: continue
    m = (cid == c) & valid
    r = dict(country=names[c], incumbent_ha=round(inc[m].sum(), 0), rice_ha_SPAM2010=round(rice[(cid == c)].sum(), 0))
    for k, l in LAB.items(): r[f"inc_ha_{l}"] = round(inc[m & (cls == k)].sum(), 0)
    r["aei_ha_in_thermal_pass"] = round(aei[m & thermal].sum(), 0)
    for k in [1, 4]: r[f"rice_ha_in_{LAB[k]}"] = round(rice[(cid == c) & (cls == k)].sum(), 0)
    rows.append(r)
ct = pd.DataFrame(rows).sort_values("incumbent_ha", ascending=False)
tot = ct.drop(columns="country").sum(); tot["country"] = "EUROPE_DOMAIN_TOTAL"
ct = pd.concat([ct, tot.to_frame().T]); ct.to_csv(os.path.join(OUT, "EUROPE_GATE_CASCADE_BY_COUNTRY.csv"), index=False)
print(ct.tail(25).to_string())

# ---------------- validation: existing European rice in gate classes ----------------
vr = {"rice_ha_total": float(rice[np.isfinite(g5) & eur].sum())}
for k, l in LAB.items(): vr[l] = float(rice[(cls == k) & eur].sum())
vr["rice_ha_no_incumbent_cells"] = float(rice[np.isfinite(g5) & (inc <= 0) & eur].sum())
json.dump(vr, open(os.path.join(OUT, "EUROPE_RICE_VALIDATION.json"), "w"), indent=1); print("validation", vr)

# ---------------- scale / aggregation / threshold sensitivity ----------------
g25 = gdd("2.5m", WIN_PIPE, sl25)
def pass_share_5m(T):
    p25 = (g25 >= T).astype(np.float32); p25[np.isnan(g25)] = np.nan
    return {"2.5m_native": up(block_mean(p25, 2), 1, (ny, nx)),
            "5m_native": (g5 >= T).astype(np.float32),
            "10m_native": up((gdd("10m", WIN_PIPE, sl10) >= T).astype(np.float32), 2, (ny, nx)),
            "30m_aggregated": up(np.where(np.isnan(block_mean(g5, 6)), np.nan, block_mean(g5, 6) >= T).astype(np.float32), 6, (ny, nx)),
            "60m_aggregated": up(np.where(np.isnan(block_mean(g5, 12)), np.nan, block_mean(g5, 12) >= T).astype(np.float32), 12, (ny, nx))}
srows = []
focus = ["Germany", "France", "Poland", "Romania", "Hungary", "Serbia", "Bulgaria", "Ukraine", "Italy", "Spain", "United Kingdom", "Denmark", "Sweden", "Lithuania", "Czech Republic", "Czechia", "Austria", "Netherlands", "Belgium"]
for T in [TSTAR, 800, 900, 1000, 1100]:
    ps = pass_share_5m(T); ref = ps["2.5m_native"]
    for nm, p in ps.items():
        ok = valid & np.isfinite(p) & np.isfinite(ref)
        r = dict(threshold=T, scale=nm, europe_inc_ha_pass=round(float((inc * p)[ok].sum()), 0), europe_inc_share_pass=round(float((inc * p)[ok].sum() / inc[ok].sum()), 4),
                 abs_disagreement_vs_2p5m_ha=round(float((inc * np.abs(p - ref))[ok].sum()), 0))
        for cn in focus:
            ids = [k for k, v in names.items() if v == cn]
            if not ids: continue
            mm = ok & (cid == ids[0])
            if inc[mm].sum() > 0: r[f"share_{cn.replace(' ', '_')}"] = round(float((inc * p)[mm].sum() / inc[mm].sum()), 4)
        srows.append(r)
sdf = pd.DataFrame(srows); sdf.to_csv(os.path.join(OUT, "EUROPE_SCALE_THRESHOLD_SENSITIVITY.csv"), index=False)
print(sdf.iloc[:, :6].to_string())
# threshold curve at 5' for both windows
curve = []
for T in range(500, 1801, 25):
    curve.append(dict(T=T, share_pipeline=float((inc * (g5 >= T))[valid].sum() / inc[valid].sum()),
                      share_calJunSep=float((inc * (g5cal >= T))[valid & np.isfinite(g5cal)].sum() / inc[valid].sum())))
pd.DataFrame(curve).to_csv(os.path.join(OUT, "EUROPE_THRESHOLD_CURVE.csv"), index=False)
# calendar-window cascade sensitivity
thc = g5cal >= TSTARc
json.dump({"T_star_calJunSep": TSTARc, "inc_share_thermal_pass_pipeline": float(inc[valid & thermal].sum() / inc[valid].sum()),
           "inc_share_thermal_pass_calJunSep": float(inc[valid & thc].sum() / inc[valid].sum()),
           "inc_share_agree": float(inc[valid & (thermal == thc)].sum() / inc[valid].sum())},
          open(os.path.join(OUT, "EUROPE_WINDOW_SENSITIVITY.json"), "w"), indent=1)

# AEI threshold sensitivity
ar = []
for a_ in [0.05, 0.10, 0.20]:
    ar.append(dict(aei_min=a_, inc_share_thermal_pass_aei=float(inc[valid & thermal & (aei_sh >= a_)].sum() / inc[valid].sum()),
                   existing_rice_share_aei=float(rice[valid & thermal & (aei_sh >= a_)].sum() / rice[valid].sum())))
pd.DataFrame(ar).to_csv(os.path.join(OUT, "EUROPE_AEI_THRESHOLD_SENSITIVITY.csv"), index=False); print(pd.DataFrame(ar))
# domain sensitivity (rectangle vs Europe definitions)
dom = []
for lab, sel in [("rectangle_-11_45E_34_71.5N", None), ("Europe_excl_Russia (primary)", EUR_SEL), ("Europe_incl_Russia_west_of_45E", ne["CONTINENT"] == "Europe"),
                 ("EU27", ne["ADMIN"].isin(["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"]))]:
    mk = np.ones((ny, nx), bool) if sel is None else rasterize([(g, 1) for g in ne[sel].geometry], out_shape=(ny, nx), transform=tr5, fill=0, dtype="uint8").astype(bool)
    v = np.isfinite(g5) & (inc > 0) & mk
    dom.append(dict(domain=lab, incumbent_Mha=round(inc[v].sum() / 1e6, 2), thermal_pass_share=round(inc[v & thermal].sum() / inc[v].sum(), 4),
                    thermal_aei_share=round(inc[v & thermal & (aei_sh >= AEI_MIN)].sum() / inc[v].sum(), 4),
                    aei_share_among_thermal_pass=round(inc[v & thermal & (aei_sh >= AEI_MIN)].sum() / inc[v & thermal].sum(), 4)))
pd.DataFrame(dom).to_csv(os.path.join(OUT, "EUROPE_DOMAIN_SENSITIVITY.csv"), index=False); print(pd.DataFrame(dom).to_string())
print("done")
