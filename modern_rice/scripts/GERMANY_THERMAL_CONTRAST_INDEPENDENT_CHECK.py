#!/usr/bin/env python3
"""Independent re-implementation of the Germany thermal-contrast endpoints. Does NOT import any project module.
Differences from ag_germany_decomposition.py: full-raster reads with coordinate lookup via the raster transform;
Germany membership by shapely point-in-polygon on cell centres (not rasterio.rasterize); weighted quantile by
pandas cumulative-sum; daily POWER GDD by explicit calendar date ranges per year; GDD integrated per day by
expanding monthly means to a daily series (equivalent definition, different code path)."""
import os, json, datetime as dt, numpy as np, pandas as pd, rasterio, shapely, geopandas as gpd
RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")
def monthly_stack(res):
    out = []
    for m in range(1, 13):
        with rasterio.open(os.path.join(RAW, f"wc2.1_{res}_tavg_{m:02d}.tif")) as s:
            a = s.read(1, masked=True).filled(np.nan).astype(float); tr = s.transform
        out.append(a)
    return np.array(out), tr
def window_days(start, end):  # list of month numbers, one per day, non-leap template year
    d, e, ms = dt.date(2001, *start), dt.date(2001, *end), []
    while d <= e: ms.append(d.month); d += dt.timedelta(days=1)
    return np.bincount(ms, minlength=13)
WP, WJ = window_days((4, 29), (9, 11)), window_days((6, 1), (9, 30))
def gdd_from_monthly(st, cnt): return np.tensordot(cnt[1:], np.clip(st - 10, 0, None), axes=1)
def spam_full(c):
    with rasterio.open(os.path.join(RAW, f"spam2010V2r0_global_H_{c}_A.tif")) as s:
        a = s.read(1).astype(float); tr = s.transform
    return np.where(a > 0, a, 0), tr
def wquant(v, w, q):
    d = pd.DataFrame({"v": v, "w": w}).dropna(); d = d[d.w > 0].sort_values("v"); c = d.w.cumsum() / d.w.sum()
    return float(d.v[c >= q].iloc[0])
st5, tr5 = monthly_stack("5m"); rice, trs = spam_full("RICE")
assert abs(trs.a - tr5.a) < 1e-6 and abs(trs.c - tr5.c) < 1e-6 and abs(trs.f - tr5.f) < 1e-6
H, W = rice.shape
res = {}
for nm, cnt in [("pipeline", WP), ("JunSep", WJ)]:
    g = gdd_from_monthly(st5[:, :H, :W], cnt)
    r, c = np.nonzero(rice)
    lon, lat = rasterio.transform.xy(tr5, r, c); lon, lat = np.array(lon), np.array(lat)
    hk = (lon >= 139.3) & (lon <= 146.0) & (lat >= 41.35) & (lat <= 45.6) & ~((lon > 140.6) & (lat < 41.6))
    res[f"Tstar_{nm}"] = wquant(g[r[hk], c[hk]], rice[r[hk], c[hk]], 0.05)
    res[f"P50_{nm}"] = wquant(g[r[hk], c[hk]], rice[r[hk], c[hk]], 0.50)
    res[f"hokkaido_rice_ha"] = float(rice[r[hk], c[hk]].sum())
    inc = sum(spam_full(k)[0] for k in ["WHEA", "MAIZ", "BARL", "POTA"])
    r2, c2 = np.nonzero(inc); lo2, la2 = (np.array(x) for x in rasterio.transform.xy(tr5, r2, c2))
    ne = gpd.read_file(os.path.join(RAW, "ne_50m_admin_0_countries", "ne_50m_admin_0_countries.shp"))
    geom = ne.loc[ne.ADMIN == "Germany", "geometry"].iloc[0]
    box = (lo2 > 5) & (lo2 < 16) & (la2 > 47) & (la2 < 56)
    inde = np.zeros_like(box); inde[box] = shapely.contains_xy(geom, lo2[box], la2[box])
    gv, wv = g[r2[inde], c2[inde]], inc[r2[inde], c2[inde]]; ok = np.isfinite(gv)
    res[f"germany_incumbent_Mha"] = float(wv[ok].sum() / 1e6)
    for lab, T in [("Tstar", round(res[f"Tstar_{nm}"])), ("900", 900.0), ("P50", round(res[f"P50_{nm}"]))]:  # thresholds rounded to whole GDD10 (project convention)
        res[f"DE_share_{nm}_{lab}"] = float(100 * wv[ok][gv[ok] >= T].sum() / wv[ok].sum())
def power_gdd(f, start, end):
    p = json.load(open(f))["properties"]["parameter"]; tx, tn = p["T2M_MAX"], p["T2M_MIN"]; yrs = sorted({int(k[:4]) for k in tx}); tot = []
    for y in yrs:
        days = pd.date_range(f"{y}-{start}", f"{y}-{end}").strftime("%Y%m%d")
        v = [max((tx[k] + tn[k]) / 2 - 10, 0) for k in days if k in tx and tx[k] > -900 and tn[k] > -900]
        tot.append(sum(v))
    return float(np.mean(tot))
res["POWER_Hokkaido_pipeline_2000_2024"] = power_gdd(os.path.join(RAW, "nasa_power_Hokkaido_JP.json"), "04-29", "09-11")
res["POWER_Hokkaido_pipeline_1981_2000"] = power_gdd(os.path.join(RAW, "nasa_power_1981_2000", "nasa_power_Hokkaido_JP_19810101_20001231.json"), "04-29", "09-11")
res["POWER_Hokkaido_JunSep_2000_2024"] = power_gdd(os.path.join(RAW, "nasa_power_Hokkaido_JP.json"), "06-01", "09-30")
out = {k: round(v, 2) for k, v in res.items()}
json.dump(out, open(os.path.join(RAW, "..", "..", "..", "outputs", "modern_rice", "applied_geography", "GERMANY_THERMAL_CONTRAST_INDEPENDENT_CHECK.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
