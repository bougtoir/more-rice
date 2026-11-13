#!/usr/bin/env python3
"""EM&A figures, generated only from outputs of ema_threshold_sweep.py and ag_grid_gates.py."""
import os, json, numpy as np, pandas as pd, geopandas as gpd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from rasterio.transform import from_origin
from rasterio.warp import reproject, Resampling
from pyproj import Transformer
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "..", "data", "raw")
ROOT = os.path.abspath(os.path.join(HERE, "..", "..")); AG = os.path.join(ROOT, "outputs", "modern_rice", "applied_geography")
OUT = os.path.join(ROOT, "outputs", "modern_rice", "ema"); FIG = os.path.join(OUT, "figures")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 8.5, "savefig.dpi": 600})
W, E, S, N = -11.0, 45.0, 34.0, 71.5; CRS = "EPSG:3035"
cur = pd.read_csv(os.path.join(OUT, "THRESHOLD_OMISSION_CURVE.csv")); sm = json.load(open(os.path.join(OUT, "EMA_THRESHOLD_SUMMARY.json")))
L = np.load(os.path.join(OUT, "ema_layers_5m.npz")); g5, rice, inc, aei, valid, eur = L["g5"], L["rice"], L["inc"], L["aei_sh"], L["valid"], L["eur"]
gde = pd.read_csv(os.path.join(AG, "GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv"))
TS = sm["T_star"]; P05EU = sm["europe_rice_gdd10_quantiles"]["P5"]
ne = gpd.read_file(os.path.join(RAW, "ne_50m_admin_0_countries", "ne_50m_admin_0_countries.shp")).cx[W - 5:E + 5, S - 5:N + 5].to_crs(CRS)
def save(fig, name):
    for ext in ("png", "pdf"): fig.savefig(os.path.join(FIG, f"{name}.{ext}"), bbox_inches="tight")
    plt.close(fig)
def mapax(ax):
    ne.boundary.plot(ax=ax, lw=0.25, color="0.35"); ax.set_xlim(2.55e6, 6.6e6); ax.set_ylim(1.35e6, 5.45e6); ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect("equal")
REF = {TS: f"T* = {TS:.0f}\n(Hokkaido P05)", 900.0: "900\n(point-derived)", float(P05EU): f"{P05EU:.0f}\n(European rice P05)"}

# Fig A: threshold sweep
fig, ax = plt.subplots(figsize=(6.3, 3.4))
ax.plot(cur.threshold_gdd10, cur.cropland_pass_pct, color="#2c7fb8", lw=1.6, label="Incumbent arable area passing the thermal gate (% of 69.7 Mha; cropland-area weighted)".replace("69.7", f"{sm['incumbent_Mha']:.1f}"))
ax.plot(cur.threshold_gdd10, cur.rice_omitted_pct, color="#d95f0e", lw=1.6, label="Mapped SPAM rice harvested area omitted by the thermal gate (% of rice area; rice-area weighted)")
ax.plot(cur.threshold_gdd10, cur.germany_cropland_pass_pct, color="#2c7fb8", lw=1.0, ls=":", label="Germany incumbent arable area passing (%)")
for t, lab in REF.items():
    ax.axvline(t, color="0.4", lw=0.7, ls="--"); ax.text(t + 12, 62, lab.replace("\n", " "), fontsize=6.2, rotation=90, va="bottom")
ax.set_xlim(0, 1800); ax.set_ylim(0, 100); ax.set_xlabel("GDD10 threshold (29 April–11 September; WorldClim 2.1 5′, 1970–2000)"); ax.set_ylabel("Percent")
ax.legend(loc="upper center", fontsize=6.3, frameon=False, bbox_to_anchor=(0.5, -0.17)); save(fig, "THRESHOLD_OMISSION_CURVE")

# Fig B: trade-off
fig, ax = plt.subplots(figsize=(4.6, 3.6))
ax.plot(cur.rice_omitted_pct, cur.cropland_pass_ha / 1e6, color="k", lw=1.2)
n = cur[cur.reference_label.fillna("") != ""]
ax.scatter(n.rice_omitted_pct, n.cropland_pass_ha / 1e6, s=14, color="#d95f0e", zorder=3)
for _, r in n.iterrows():
    if r.threshold_gdd10 in REF: ax.annotate(f"{r.threshold_gdd10:.0f}", (r.rice_omitted_pct, r.cropland_pass_ha / 1e6), xytext=(5, 2), textcoords="offset points", fontsize=6.5)
ax.set_xscale("symlog", linthresh=1); ax.set_xlim(0, 100)
ax.set_xlabel("Mapped rice harvested area omitted (%; symlog axis)"); ax.set_ylabel("Candidate incumbent arable area for\nnext-stage assessment (Mha)")
ax.text(0.02, 0.03, "Each point on the curve is one GDD10 threshold\n(0–1800, step 25). Orange: named reference\nconstructions. Candidate area is not feasible land.", transform=ax.transAxes, ha="left", va="bottom", fontsize=6)
save(fig, "CANDIDATE_AREA_OMISSION_TRADEOFF")

# Fig C: omission geography (rice cells by threshold band)
iy, ix = np.where(np.isfinite(g5) & eur & (rice > 0)); lon = W + (ix + 0.5) / 12; lat = N - (iy + 0.5) / 12
x, y = Transformer.from_crs("EPSG:4326", CRS, always_xy=True).transform(lon, lat); g = g5[iy, ix]; r = rice[iy, ix]
bands = [(-1, TS, "#b2182b", f"< {TS:.0f} (omitted at T*)"), (TS, 900, "#ef8a62", f"{TS:.0f}–899 (omitted at 900 only)"), (900, 1100, "#fddbc7", "900–1099 (omitted at 1100 only)"), (1100, 1e9, "#4393c3", "≥ 1100 (retained at all three)")]
fig, ax = plt.subplots(figsize=(5.6, 5.4)); mapax(ax)
for lo, hi, c, lab in bands[::-1]:
    m = (g >= lo) & (g < hi); ax.scatter(x[m], y[m], s=np.clip(r[m] / 40, 0.3, 25), color=c, lw=0, label=f"{lab}: {r[m].sum()/1e3:.1f} kha")
ax.legend(loc="upper left", fontsize=6.3, title="Cell GDD10; mapped SPAM rice harvested area", title_fontsize=6.3, frameon=True, markerscale=2.5)
ax.text(0.01, 0.01, "Marker area ∝ SPAM 2010 rice harvested area in the 5′ cell (rice-area weighted).\nETRS89-LAEA (EPSG:3035). Europe excluding Russia.", transform=ax.transAxes, fontsize=5.8)
save(fig, "RICE_AREA_OMISSION_GEOGRAPHY")

# Fig D: classification disagreement T* vs 900 on incumbent arable cells
ny, nx = g5.shape; cl = np.zeros((ny, nx), np.float32)
share = inc / np.maximum(1, inc.max()); m = valid
cl[m & (g5 >= 900)] = 1; cl[m & (g5 >= TS) & (g5 < 900)] = 2; cl[m & (g5 < TS)] = 3
dst = np.zeros((420, 410), np.float32); dtr = from_origin(2.55e6, 5.45e6, 1e4, 1e4)
reproject(cl, dst, src_transform=from_origin(W, N, 1 / 12, 1 / 12), src_crs="EPSG:4326", dst_transform=dtr, dst_crs=CRS, resampling=Resampling.nearest, src_nodata=0, dst_nodata=0)
st = pd.read_csv(os.path.join(OUT, "CLASSIFICATION_STABILITY_PAIRS.csv")); s1 = st[(st.domain == "Europe") & st.comparison.str.startswith("S1")].iloc[0]
fig, ax = plt.subplots(figsize=(5.6, 5.4)); mapax(ax)
ax.imshow(np.ma.masked_equal(dst, 0), extent=(2.55e6, 2.55e6 + 410e4, 5.45e6 - 420e4, 5.45e6), cmap=ListedColormap(["#1a9850", "#fdae61", "#762a83"]), vmin=0.5, vmax=3.5, interpolation="nearest")
ne.boundary.plot(ax=ax, lw=0.25, color="0.35")
for c, lab, v in [("#1a9850", "Pass under both T* and 900", s1.both_pass_ha), ("#fdae61", "Pass under T* only (disagreement)", s1.ref_only_ha), ("#762a83", "Fail under both", s1.both_fail_ha)]:
    ax.scatter([], [], marker="s", color=c, label=f"{lab}: {v/1e6:.1f} Mha")
ax.legend(loc="upper left", fontsize=6.3, title=f"Incumbent arable cells (cropland-area weighted); Jaccard = {s1.jaccard_pass:.2f}", title_fontsize=6.3)
ax.text(0.01, 0.01, "No cell passes 900 but fails T* (nested thresholds on a fixed surface).\nETRS89-LAEA, 10 km display grid; classification on the native 5′ grid.", transform=ax.transAxes, fontsize=5.8)
save(fig, "CLASSIFICATION_DISAGREEMENT_MAP")

# Fig E: Germany controlled contrast (reference construction vs grid support)
p = gde[gde.block == "1_threshold_path_pipeline_5m"]; rs = gde[(gde.block == "4_resolution_recalibrated") & gde.surface_window.str.startswith("pipeline")]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 2.9), gridspec_kw=dict(width_ratios=[2.2, 1]), sharey=True)
a1.barh(range(len(p)), p.germany_pass_pct, color="#2c7fb8"); a1.set_yticks(range(len(p))); a1.set_yticklabels([f"{l} ({t:.0f})" for l, t in zip(p.label, p.threshold_gdd10)], fontsize=6.2); a1.invert_yaxis()
a1.set_xlabel("Germany incumbent arable area passing (%)"); a1.set_title("(a) Reference construction, fixed 5′ surface")
for i, v in enumerate(p.germany_pass_pct): a1.text(v + 1, i, f"{v:.1f}", va="center", fontsize=6)
a2.barh(range(len(rs)), rs.germany_pass_pct, color="#7fbc41"); a2.set_title("(b) P05 recalibrated per resolution")
for i, (v, res, t) in enumerate(zip(rs.germany_pass_pct, rs.surface_resolution, rs.threshold_gdd10)): a2.text(2, i, f"{res}: T={t:.0f}, {v:.1f}%", va="center", fontsize=6, color="k")
a2.set_xlabel("Germany passing (%)"); a1.set_xlim(0, 110); a2.set_xlim(0, 110); save(fig, "GERMANY_CONTROLLED_CONTRAST")
print(sorted(os.listdir(FIG)))
