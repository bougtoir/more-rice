#!/usr/bin/env python3
"""Independent RPG rice coverage check on the canonical WorldClim 5' GDD10 surface.
Area-weighted parcel/grid intersection (primary) and centroid assignment (sensitivity); MapSPAM 2010 France comparison on the same surface."""
import os, glob, json, numpy as np, pandas as pd, geopandas as gpd
from shapely.geometry import box
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
RAW = os.path.join(HERE, "..", "data", "raw", "rpg"); EMA = os.path.join(ROOT, "outputs", "modern_rice", "ema"); OUT = os.path.join(EMA, "rpg"); os.makedirs(OUT, exist_ok=True)
W, N, R = -11.0, 71.5, 1 / 12
L = np.load(os.path.join(EMA, "ema_layers_5m.npz")); g5, rice, inc, valid, cid = L["g5"], L["rice"], L["inc"], L["valid"], L["cid"]
SEL = (589, 900, 1100); TH = sorted(set(range(0, 1801, 25)) | set(SEL))

def cell_of(lon, lat): return ((N - lat) / R).astype(int), ((lon - W) / R).astype(int)

def clean_area(p):
    p = p[p.geo_ha > 0].copy(); p["pid"] = range(len(p)); return p
def load(tag):
    if tag == "2010":
        p = pd.concat([gpd.read_file(f) for f in sorted(glob.glob(os.path.join(RAW, "rpg2010_ilots_grp14_p*.geojson")))])
        p = p[p.code_cultu.astype(str) == "14"].copy(); p["w"] = p.surf_cultu.astype(float); unit = "ilot (rice-group area surf_cultu)"
    else:
        p = pd.concat([gpd.read_file(f) for f in sorted(glob.glob(os.path.join(RAW, f"rpg{tag}_riz_p*.geojson")))])
        p = p[p.code_cultu == "RIZ"].copy(); p["w"] = np.nan; unit = "parcel (geodesic area)"
    p = p.set_crs(4326, allow_override=True); nall = len(p); rp = p.geometry.representative_point()
    p = p[(rp.x > -5) & (rp.x < 10) & (rp.y > 41) & (rp.y < 51.5)].copy()  # metropolitan France (excludes overseas departments)
    p3 = p.to_crs(2154); p["geo_ha"] = p3.area / 1e4; p["w"] = p.w.fillna(p.geo_ha); p = clean_area(p)
    return p, nall, unit

def overlay(p):
    minx, miny, maxx, maxy = p.total_bounds
    c0, c1 = int((minx - W) / R), int((maxx - W) / R) + 1; r0, r1 = int((N - maxy) / R), int((N - miny) / R) + 1
    cells = gpd.GeoDataFrame([dict(r=r, c=c, geometry=box(W + c * R, N - (r + 1) * R, W + (c + 1) * R, N - r * R)) for r in range(r0, r1) for c in range(c0, c1)], crs=4326)
    ix = gpd.overlay(p[["pid", "geometry"]], cells, how="intersection", keep_geom_type=True).to_crs(2154)
    ix["frac"] = ix.area / 1e4 / p.set_index("pid").geo_ha.reindex(ix.pid).values
    ix["a"] = ix.frac * p.set_index("pid").w.reindex(ix.pid).values; ix["g"] = g5[ix.r, ix.c]
    return ix

def omit(a, g, T):
    ok = np.isfinite(g); return float(a[ok & (g < T)].sum() / a[ok].sum())

def wq(a, g, q):
    o = np.argsort(g); return float(np.interp(q, np.cumsum(a[o]) / a.sum(), g[o]))

def main():
    rows, curve, comp, cellsets = [], [], [], {}
    for tag in ("2010", "2015", "2020", "2024"):
        p, nall, unit = load(tag); ix = overlay(p)
        cen = p.to_crs(2154).geometry.centroid.to_crs(4326); rr, cc = cell_of(cen.x.values, cen.y.values); gc = g5[rr, cc]
        cg = ix[np.isfinite(ix.g)].groupby(["r", "c"]).agg(a=("a", "sum"), g=("g", "first")).reset_index(); cellsets[tag] = cg
        cg.assign(source=f"RPG{tag}").to_csv(os.path.join(OUT, f"rpg{tag}_cells.csv"), index=False)
        cam = cg[(cg.c >= int((4.2 - W) / R)) & (cg.r <= int((N - 43.3) / R))].a.sum() / cg.a.sum()
        rows.append(dict(source=f"RPG {tag}", unit=unit, features_all_france=nall, features_metropolitan=len(p), rice_area_ha=round(ix.a.sum(), 1),
                         area_ha_declared=round(float(p.surf_cultu.astype(float).sum() if tag == "2010" else p.surf_parc.sum()), 1),
                         climate_cells=len(cg), area_in_nodata_cells_ha=round(ix.a[~np.isfinite(ix.g)].sum(), 2), share_area_lon_ge_4p2E_lat_le_43p8N_approx_camargue=round(cam, 3),
                         largest_cell_area_share=round(cg.a.max() / cg.a.sum(), 3), gdd10_min_cell=round(cg.g.min(), 0),
                         gdd10_aw_p05=round(wq(cg.a.values, cg.g.values, .05), 0), gdd10_aw_median=round(wq(cg.a.values, cg.g.values, .5), 0),
                         **{f"omit_area_T{T}": round(omit(ix.a.values, ix.g.values, T), 5) for T in SEL},
                         **{f"omit_area_centroid_T{T}": round(omit(p.w.values, gc, T), 5) for T in SEL},
                         **{f"omit_count_centroid_T{T}": round(float((gc[np.isfinite(gc)] < T).mean()), 5) for T in SEL},
                         **{f"omit_cells_T{T}": int((cg.g < T).sum()) for T in SEL}))
        for T in TH:
            curve.append(dict(source=f"RPG {tag}", threshold_gdd10=T, omitted_area_frac=round(omit(ix.a.values, ix.g.values, T), 5),
                              omitted_area_frac_centroid=round(omit(p.w.values, gc, T), 5), omitted_count_frac_centroid=round(float((gc[np.isfinite(gc)] < T).mean()), 5)))
    fr = int(np.bincount(cid[cellsets["2020"].r.values, cellsets["2020"].c.values]).argmax()); frm = cid == fr  # France = country id holding the RPG cells
    sm = frm & np.isfinite(g5) & (rice > 0)
    c10 = np.zeros_like(sm); c10[cellsets["2010"].r.values, cellsets["2010"].c.values] = True
    for T in TH:
        curve.append(dict(source="MapSPAM 2010 France", threshold_gdd10=T, omitted_area_frac=round(omit(rice[sm], g5[sm], T), 5)))
        curve.append(dict(source="MapSPAM 2010 Europe (context)", threshold_gdd10=T, omitted_area_frac=round(omit(rice[np.isfinite(g5) & L["eur"] & (rice > 0)], g5[np.isfinite(g5) & L["eur"] & (rice > 0)], T), 5)))
    fv = frm & valid
    for T in SEL:
        d = dict(threshold_gdd10=T, france_incumbent_cropland_pass_pct=round(100 * inc[fv & (g5 >= T)].sum() / inc[fv].sum(), 2))
        for r_ in rows: d[f"{r_['source']} omit_area_pct"] = round(100 * r_[f"omit_area_T{T}"], 3)
        d["MapSPAM2010 France omit_area_pct"] = round(100 * omit(rice[sm], g5[sm], T), 3); d["MapSPAM2010 France rice_ha"] = round(rice[sm].sum(), 1)
        d["MapSPAM2010 France cells"] = int(sm.sum()); d["MapSPAM2010 France share_in_RPG2010_cells"] = round(rice[sm & c10].sum() / rice[sm].sum(), 4)
        d["MapSPAM2010 France omit_area_pct_in_RPG2010_cells"] = round(100 * omit(rice[sm & c10], g5[sm & c10], T), 3)
        d["MapSPAM2010 France omit_area_pct_outside_RPG2010_cells"] = round(100 * omit(rice[sm & ~c10], g5[sm & ~c10], T), 3)
        comp.append(d)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "RPG_RICE_PARCEL_VALIDATION.csv"), index=False)
    cv = pd.DataFrame(curve); cv.to_csv(os.path.join(OUT, "RPG_THRESHOLD_OMISSION_CURVE.csv"), index=False)
    pd.DataFrame(comp).to_csv(os.path.join(OUT, "RPG_VS_MAPSPAM_COMPARISON.csv"), index=False)
    spam_fr = dict(rice_ha=round(rice[sm].sum(), 1), cells=int(sm.sum()), cells_ge_100ha=int((sm & (rice >= 100)).sum()), max_cell_ha=round(rice[sm].max(), 1),
                   gdd10_aw_p05=round(wq(rice[sm], g5[sm], .05)), gdd10_aw_median=round(wq(rice[sm], g5[sm], .5)), gdd10_aw_p95=round(wq(rice[sm], g5[sm], .95)), france_cid=fr)
    json.dump(dict(spam_france=spam_fr, rpg=rows), open(os.path.join(OUT, "RPG_SUMMARY.json"), "w"), indent=1, default=float)
    # Figure: map
    lat0, lat1, lon0, lon1 = 42.3, 51.2, -5.0, 8.3
    rs, re_ = int((N - lat1) / R), int((N - lat0) / R); cs, ce = int((lon0 - W) / R), int((lon1 - W) / R)
    fig, ax = plt.subplots(1, 2, figsize=(11, 5.2), constrained_layout=True)
    G = np.where(frm, g5, np.nan)[rs:re_, cs:ce]; ext = (lon0, lon1, lat0, lat1)
    for k, ttl in enumerate(("(a) MapSPAM 2010 rice harvested area", "(b) RPG 2020 declared rice parcels")):
        im = ax[k].imshow(G, extent=ext, cmap="Greys", vmin=0, vmax=1800, origin="upper")
        ax[k].contour(np.linspace(lon0, lon1, G.shape[1]), np.linspace(lat1, lat0, G.shape[0]), G, levels=[589, 900], colors=["#1f77b4", "#d62728"], linewidths=0.8)
        ax[k].set_title(ttl, fontsize=10); ax[k].set_xlabel("Longitude (°E)"); ax[k].set_ylabel("Latitude (°N)")
    yy, xx = np.nonzero(sm[rs:re_, cs:ce]); ax[0].scatter(lon0 + (xx + .5) * R, lat1 - (yy + .5) * R, s=2 + rice[rs:re_, cs:ce][yy, xx] / 2, c="#2ca02c", alpha=.7, lw=0)
    cg = cellsets["2020"]; ax[1].scatter(W + (cg.c + .5) * R, N - (cg.r + .5) * R, s=2 + cg.a / 20, c="#2ca02c", alpha=.7, lw=0)
    for a in ax: a.plot([], [], c="#1f77b4", lw=.8, label="589 GDD10 contour"); a.plot([], [], c="#d62728", lw=.8, label="900 GDD10 contour"); a.legend(loc="upper left", fontsize=8)
    fig.colorbar(im, ax=ax, shrink=.8, label="GDD10, 29 Apr–11 Sep (WorldClim 1970–2000)")
    fig.savefig(os.path.join(OUT, "RPG_RICE_PARCEL_VALIDATION_MAP.png"), dpi=300); plt.close(fig)
    fig, ax = plt.subplots(figsize=(6.5, 4.2), constrained_layout=True)
    for s, st in (("MapSPAM 2010 Europe (context)", dict(c="0.6", ls=":")), ("MapSPAM 2010 France", dict(c="#2ca02c")), ("RPG 2010", dict(c="#9467bd")), ("RPG 2020", dict(c="#1f77b4", ls="--"))):
        d = cv[cv.source == s]; ax.plot(d.threshold_gdd10, 100 * d.omitted_area_frac, label=s, **st)
    for T in (589, 900): ax.axvline(T, c="0.3", lw=.6, ls="--")
    ax.set_xlabel("Thermal threshold (GDD10)"); ax.set_ylabel("Rice area below threshold (%)"); ax.legend(fontsize=8); ax.set_xlim(0, 1800); ax.set_ylim(0, 100)
    fig.savefig(os.path.join(OUT, "RPG_THRESHOLD_OMISSION_CURVE.png"), dpi=300); plt.close(fig)
    from PIL import Image
    a_, b_ = Image.open(os.path.join(OUT, "RPG_RICE_PARCEL_VALIDATION_MAP.png")), Image.open(os.path.join(OUT, "RPG_THRESHOLD_OMISSION_CURVE.png"))
    b_ = b_.resize((int(b_.width * a_.height * 0.9 / b_.height), int(a_.height * 0.9)))
    c_ = Image.new("RGB", (a_.width, a_.height + b_.height + 40), "white"); c_.paste(a_, (0, 0)); c_.paste(b_, ((a_.width - b_.width) // 2, a_.height + 40))
    from PIL import ImageDraw, ImageFont
    ImageDraw.Draw(c_).text(((a_.width - b_.width) // 2, a_.height + 5), "(c)", fill="black", font=ImageFont.load_default(size=48))
    c_.save(os.path.join(EMA, "figures", "RPG_MAPSPAM_FRANCE_COMPARISON.png"), dpi=(300, 300))
    print(pd.DataFrame(rows).T.to_string()); print(pd.DataFrame(comp).T.to_string()); print(spam_fr)


if __name__ == "__main__":
    main()
