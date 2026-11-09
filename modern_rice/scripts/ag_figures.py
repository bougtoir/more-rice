#!/usr/bin/env python3
"""Applied Geography figures from canonical outputs in outputs/modern_rice/applied_geography."""
import os, json, numpy as np, pandas as pd, geopandas as gpd, rasterio, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from rasterio.warp import reproject, Resampling, calculate_default_transform
from rasterio.transform import from_origin
HERE = os.path.dirname(__file__); RAW = os.path.join(HERE, "..", "data", "raw")
O = os.path.join(HERE, "..", "..", "outputs", "modern_rice", "applied_geography"); FIG = os.path.join(O, "figures"); os.makedirs(FIG, exist_ok=True)
W, E, S, N = -11.0, 45.0, 34.0, 71.5
cls = np.load(os.path.join(O, "grid_class_5m.npy")).astype(np.float32); g5 = np.load(os.path.join(O, "grid_gdd_5m.npy")); inc = np.load(os.path.join(O, "grid_inc_5m.npy"))
cal = json.load(open(os.path.join(O, "GRID_THERMAL_CALIBRATION.json"))); T = cal["T_star_pipeline"]
area_frac = inc / (1e4 * 0)  if False else None
tr = from_origin(W, N, 1 / 12, 1 / 12); crs = "EPSG:3035"
dt, w, h = calculate_default_transform("EPSG:4326", crs, cls.shape[1], cls.shape[0], W, S, E, N, resolution=10000)
def proj(a, rs):
    o = np.full((h, w), np.nan, np.float32)
    reproject(a.astype(np.float32), o, src_transform=tr, src_crs="EPSG:4326", dst_transform=dt, dst_crs=crs, resampling=rs, src_nodata=np.nan, dst_nodata=np.nan); return o
c = cls.copy(); c[cls == 0] = np.nan
lat = 90 - (np.arange(int((90 - N) * 12), int((90 - S) * 12)) + 0.5) / 12
ha = (6371.0072**2 * np.deg2rad(1 / 12)**2 * np.cos(np.deg2rad(lat)) * 100)[:, None]
share = inc / ha; c[share < 0.01] = np.nan
cp = proj(c, Resampling.nearest); gp = proj(np.where(np.isfinite(g5), g5, np.nan), Resampling.bilinear)
ext = [dt.c, dt.c + dt.a * w, dt.f + dt.e * h, dt.f]
ne = gpd.read_file(os.path.join(RAW, "ne_50m_admin_0_countries", "ne_50m_admin_0_countries.shp")).cx[W - 5:E + 5, S - 5:N + 5].to_crs(crs)
pts = pd.read_csv(os.path.join(O, "POINT_GRID_CROSSWALK.csv"))
pg = gpd.GeoDataFrame(pts, geometry=gpd.points_from_xy(pts.lon, pts.lat), crs="EPSG:4326").to_crs(crs)
cand = ["LowerDanube_RO", "Rhine_DE", "Alsace_FR", "Loire_FR", "Berlin_DE", "Saxony_DE", "PoValley_IT", "Vercelli_IT"]
def deco(ax, title):
    ne.boundary.plot(ax=ax, lw=0.3, color="k"); ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_xticks([]); ax.set_yticks([])
    x0, y0 = ext[0] + 2e5, ext[2] + 2e5; ax.plot([x0, x0 + 5e5], [y0, y0], "k-", lw=3); ax.text(x0 + 2.5e5, y0 + 6e4, "500 km", ha="center", fontsize=7)
    ax.set_title(title, fontsize=9, loc="left")
fig, axs = plt.subplots(1, 2, figsize=(11, 5.6), constrained_layout=True)
im = axs[0].imshow(gp, extent=ext, origin="upper", cmap="viridis", vmin=200, vmax=2000)
axs[0].contour(np.linspace(ext[0], ext[1], w), np.linspace(ext[3], ext[2], h), gp, levels=[T, 900], colors=["white", "red"], linewidths=[0.8, 0.8], linestyles=["-", "--"])
deco(axs[0], f"(a) GDD10, 29 Apr–11 Sep (WorldClim 2.1, 5′, 1970–2000)\nwhite: grid-calibrated T* = {T:.0f}; red dashed: 900")
fig.colorbar(im, ax=axs[0], shrink=0.7, label="GDD10 (°C·d)")
cols = ["#999999", "#E69F00", "#56B4E9", "#0072B2"]
axs[1].imshow(cp, extent=ext, origin="upper", cmap=ListedColormap(cols), norm=BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5], 4), interpolation="nearest")
deco(axs[1], "(b) Gate class of cells with incumbent arable ≥1% of cell area\n(SPAM 2010 wheat+maize+barley+potato harvested area)")
from matplotlib.patches import Patch
axs[1].legend(handles=[Patch(color=cols[0], label="thermal gate not met"), Patch(color=cols[1], label="thermal met; AEI <10%; rainfed deficit D>0"),
                       Patch(color=cols[2], label="thermal met; AEI <10%; D≤0"), Patch(color=cols[3], label="thermal met; AEI ≥10% (irrigation infrastructure)")], loc="upper left", fontsize=6.5, framealpha=0.9)
for ax in axs:
    sub = pg[pg.point.isin(cand)]; ax.scatter(sub.geometry.x, sub.geometry.y, s=14, facecolor="none", edgecolor="k", lw=0.8)
fig.text(0.01, 0.005, "Projection: ETRS89-LAEA Europe (EPSG:3035), 10 km display grid. Circles: NASA POWER point cells used in the point analysis. Classes are exposure of existing arable area to gates, not convertible area.", fontsize=6.5)
for ext_ in ["png", "svg", "pdf"]: fig.savefig(os.path.join(FIG, f"Figure_map_gates.{ext_}"), dpi=600 if ext_ == "png" else None)
plt.close(fig)
# scale / threshold sensitivity
s = pd.read_csv(os.path.join(O, "EUROPE_SCALE_THRESHOLD_SENSITIVITY.csv")); cv = pd.read_csv(os.path.join(O, "EUROPE_THRESHOLD_CURVE.csv"))
fig, axs = plt.subplots(2, 2, figsize=(11, 7.6), constrained_layout=True); axs = axs.ravel()
axs[0].plot(cv["T"], cv.share_pipeline * 100, label="29 Apr–11 Sep window"); axs[0].plot(cv["T"], cv.share_calJunSep * 100, "--", label="calendar Jun–Sep")
axs[0].axvline(T, color="k", lw=0.8); axs[0].axvline(900, color="r", lw=0.8, ls="--"); axs[0].set_xlabel("GDD10 threshold"); axs[0].set_ylabel("% incumbent arable passing"); axs[0].legend(fontsize=7); axs[0].set_title("(a) Threshold dependence (5′)", fontsize=9, loc="left")
for thr, mk in [(T, "o"), (900, "s"), (1000, "^")]:
    q = s[s.threshold == thr]; axs[1].plot(range(len(q)), q.europe_inc_share_pass * 100, marker=mk, label=f"T={thr:.0f}")
axs[1].set_xticks(range(5)); axs[1].set_xticklabels(["2.5′", "5′", "10′", "30′ agg", "60′ agg"]); axs[1].set_ylabel("% incumbent arable passing"); axs[1].legend(fontsize=7); axs[1].set_title("(b) Resolution / aggregation", fontsize=9, loc="left")
axs[2].scatter(pts.power_gdd_pipeline, pts.grid_gdd_pipeline, s=12); lim = [200, 2300]; axs[2].plot(lim, lim, "k:", lw=0.8)
for _, r in pts[pts.point.isin(cand)].iterrows(): axs[2].annotate(r.point.split("_")[0], (r.power_gdd_pipeline, r.grid_gdd_pipeline), fontsize=6)
axs[2].set_xlabel("NASA POWER point cell, 2000–2024"); axs[2].set_ylabel("WorldClim 5′ cell, 1970–2000"); axs[2].set_title("(c) Source/scale cross-walk of GDD10", fontsize=9, loc="left")
dc = pd.read_csv(os.path.join(O, "GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv"))
for blk, off, col, lab in [("1_threshold_path_pipeline_5m", -0.2, "C0", "29 Apr–11 Sep"), ("2_threshold_path_JunSep_5m", 0.2, "C1", "Jun–Sep")]:
    q = dc[dc.block == blk].reset_index(drop=True); axs[3].bar(np.arange(len(q)) + off, q.germany_pass_pct, 0.38, color=col, label=lab)
    for i, r in q.iterrows(): axs[3].text(i + off, r.germany_pass_pct + 1.5, f"{r.threshold_gdd10:.0f}", ha="center", fontsize=5.5, rotation=90)
axs[3].set_xticks(range(6)); axs[3].set_xticklabels(["POWER pt\n2000–24", "POWER pt\n1981–2000", "monthly\nformula", "WorldClim\ncell at pt", "Hokkaido\nrice P50", "Hokkaido\nrice P05"], fontsize=6.5)
axs[3].set_ylim(0, 112); axs[3].set_ylabel("% German incumbent arable passing"); axs[3].legend(fontsize=7, loc="upper left"); axs[3].set_title("(d) Germany: reference-construction path (5′ surface)", fontsize=9, loc="left")
for ext_ in ["png", "svg", "pdf"]: fig.savefig(os.path.join(FIG, f"Figure_scale_sensitivity.{ext_}"), dpi=600 if ext_ == "png" else None)
print("figs ok")
# ---------------- Figure 1: gate framework ----------------
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(11, 3.6)); ax.axis("off"); ax.set_xlim(0, 11); ax.set_ylim(0, 3.6)
boxes = [("G1 Thermal transfer", "system-specific\ncold bound calibrated\non the same grid\n(Hokkaido rice cells)"),
         ("G2 Water access", "irrigation infrastructure\n(GMIA AEI share)\nmainstem low flow vs demand\nallocation: unresolved"),
         ("G3 Rainfed balance", "Jun–Sep Kc·ET0 − P\n(grid, 10′)\ndaily root-zone bucket\n(points)"),
         ("G4 Economic parity", "break-even vs\nincumbent margin\n(observed costs\nonly for Italy)"),
         ("G5 Supply-risk effect", "scenario shortfall\nprobability, potato\ncomparator, block-\nbootstrap CI")]
for i, (t, d) in enumerate(boxes):
    x = 0.15 + i * 2.15
    ax.add_patch(FancyBboxPatch((x, 0.9), 1.9, 2.2, boxstyle="round,pad=0.05", fc=["#f0f0f0", "#deebf7", "#fde0c5", "#e5f5e0", "#efedf5"][i], ec="k", lw=0.8))
    ax.text(x + 0.95, 2.8, t, ha="center", va="center", fontsize=9, weight="bold"); ax.text(x + 0.95, 1.85, d, ha="center", va="center", fontsize=7.2)
    if i < 4: ax.annotate("", (x + 2.12, 2.0), (x + 1.98, 2.0), arrowprops=dict(arrowstyle="->", lw=1.2))
ax.text(5.5, 0.45, "Unit of analysis: 5′ cells of incumbent arable land (SPAM 2010 wheat+maize+barley+potato harvested area); gates G1–G3 are mapped, G4–G5 are evaluated for candidate regions and countries.\n"
        "Passing all gates identifies a candidate for next-stage feasibility assessment, not an allocation, a converted area, or implemented irrigation.", ha="center", fontsize=7.2)
for e in ["png", "svg", "pdf"]: fig.savefig(os.path.join(FIG, f"Figure_framework.{e}"), dpi=600 if e == "png" else None, bbox_inches="tight")
plt.close(fig)
# ---------------- Figure 4: water geography ----------------
dd = pd.read_csv(os.path.join(O, "DANUBE_DEMAND_VS_LOWFLOW.csv"))
fig, axs = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
m = pts.bucket_P_flower_deficit_pct.notna()
sc = axs[0].scatter(pts.grid_D_mm[m], pts.bucket_P_flower_deficit_pct[m], c=pts.lat[m], cmap="coolwarm_r", s=28, edgecolor="k", lw=0.4)
for _, r in pts[m].iterrows(): axs[0].annotate(r.point.split("_")[0], (r.grid_D_mm, r.bucket_P_flower_deficit_pct), fontsize=6, xytext=(2, 2), textcoords="offset points")
from scipy.stats import spearmanr
rho, p = spearmanr(pts.grid_D_mm[m], pts.bucket_P_flower_deficit_pct[m])
axs[0].set_xlabel("Grid climatic deficit D, Jun–Sep (mm; WorldClim 10′)"); axs[0].set_ylabel("Years with >10 flowering deficit days (%)\n(daily bucket, NASA POWER 2000–2024)")
axs[0].set_title(f"(a) Rainfed balance: point model vs grid (Spearman ρ = {rho:.2f}, n = {m.sum()})", fontsize=9, loc="left"); fig.colorbar(sc, ax=axs[0], label="latitude (°N)")
q = dd[(dd.season_days == 120)]
for D_mm, mk in [(800, "o"), (1000, "s"), (1200, "^")]:
    s_ = q[q.seasonal_depth_mm == D_mm]; axs[1].plot(s_.area_ha / 1000, s_.pct_of_lowflow_median, marker=mk, label=f"{D_mm} mm / 120 d")
axs[1].set_xlabel("Paddy area (thousand ha)"); axs[1].set_ylabel("Net demand (% of median Jun–Sep\nminimum daily flow, Orsova)"); axs[1].legend(fontsize=7)
axs[1].set_title("(b) Lower Danube: demand vs observed Jun–Sep low flow (Orsova)", fontsize=9, loc="left")
for e in ["png", "svg", "pdf"]: fig.savefig(os.path.join(FIG, f"Figure_water.{e}"), dpi=600 if e == "png" else None)
plt.close(fig)
# ---------------- Figure 5: corrected risk ----------------
rb = pd.read_csv(os.path.join(O, "RISK_PORTFOLIO_BASELINE_CORRECTED.csv"))
sel = ["Romania", "Bulgaria", "Hungary", "Serbia", "Croatia", "Ukraine", "France", "Germany", "Poland", "Kazakhstan", "Uzbekistan", "Italy"]
rb = rb[rb.country.isin(sel)].set_index("country").loc[sel].reset_index()
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 4.2), constrained_layout=True, gridspec_kw={"width_ratios": [2.2, 1]}); x = np.arange(len(rb))
lab = [c + ("*" if e == "analog" else "") for c, e in zip(rb.country, rb.evidence_class)]
ax.bar(x - 0.25, rb.P_A, 0.25, label="A incumbent", color="#999999"); ax.bar(x, rb.P_B_rice, 0.25, label="B 20% rice substitution", color="#0072B2")
ax.bar(x + 0.25, rb.P_D_potato, 0.25, label="D 20% potato comparator", color="#E69F00")
ax.set_xticks(x); ax.set_xticklabels(lab, rotation=30, fontsize=8); ax.set_ylabel("Modeled P(kcal shortfall)"); ax.legend(fontsize=7)
ax.set_title("(a) Corrected scenario (linear detrend, f = 0.2, own-mean threshold); * analog rice shocks", fontsize=8, loc="left")
d = rb.P_B_rice - rb.P_A; y = np.arange(len(rb))[::-1]
ax2.errorbar(d, y, xerr=[d - rb.diff_CI95_lo, rb.diff_CI95_hi - d], fmt="o", color="#0072B2", ecolor="k", capsize=2, ms=4)
ax2.axvline(0, color="k", lw=0.6); ax2.set_yticks(y); ax2.set_yticklabels(lab, fontsize=8); ax2.set_xlabel("B − A (95% moving-block bootstrap CI)")
ax2.set_title("(b) Change in shortfall probability", fontsize=8, loc="left")
for e in ["png", "svg", "pdf"]: fig.savefig(os.path.join(FIG, f"Figure_risk.{e}"), dpi=600 if e == "png" else None)
print("all figs ok")
