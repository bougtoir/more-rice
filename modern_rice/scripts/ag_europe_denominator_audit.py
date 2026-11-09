#!/usr/bin/env python3
"""Independent audit of the European spatial denominator and gate counts. Does not import project modules.
Re-implements: domain membership (shapely point-in-polygon on SPAM cell centres, global grid), GDD10 (daily-count
expansion of monthly means), AEI share (GMIA ha / ellipsoidal WGS84 cell area from pyproj.Geod, vs spherical in the
pipeline). The rainfed-deficit split of the thermal-pass/no-infrastructure class is read from the canonical class
raster (not re-implemented). Writes gate counts, provenance/audit Markdown and a diagnostic map."""
import os, json, datetime as dt, numpy as np, pandas as pd, rasterio, shapely, geopandas as gpd, pyproj, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
RAW = os.path.join(ROOT, "modern_rice", "data", "raw"); AG = os.path.join(ROOT, "outputs", "modern_rice", "applied_geography"); FA = os.path.join(AG, "final_audit"); os.makedirs(FA, exist_ok=True)
TSTAR = json.load(open(os.path.join(AG, "GRID_THERMAL_CALIBRATION.json")))["T_star_pipeline"]; AEI_MIN = 0.10
BOX = (-11.0, 45.0, 34.0, 71.5)
def rd(p):
    with rasterio.open(p) as s: return s.read(1, masked=True).filled(np.nan).astype(float), s.transform
inc = None
for c in ["WHEA", "MAIZ", "BARL", "POTA"]:
    a, tr = rd(os.path.join(RAW, f"spam2010V2r0_global_H_{c}_A.tif")); a = np.where(a > 0, a, 0); inc = a if inc is None else inc + a
rice, _ = rd(os.path.join(RAW, "spam2010V2r0_global_H_RICE_A.tif")); rice = np.where(rice > 0, rice, 0)
d = dt.date(2001, 4, 29); cnt = np.zeros(13)
while d <= dt.date(2001, 9, 11): cnt[d.month] += 1; d += dt.timedelta(days=1)
g = sum(cnt[m] * np.clip(rd(os.path.join(RAW, f"wc2.1_5m_tavg_{m:02d}.tif"))[0] - 10, 0, None) for m in range(4, 10))
aei = np.loadtxt(os.path.join(RAW, "gmia_v5_aei_ha.asc"), skiprows=6); aei = np.where(aei > 0, aei, 0)
r, c = np.nonzero(inc); lon, lat = (np.array(v) for v in rasterio.transform.xy(tr, r, c))
geod = pyproj.Geod(ellps="WGS84"); h = 1 / 24
ulat = np.unique(lat); area_lat = {la: abs(geod.polygon_area_perimeter([0, 1 / 12, 1 / 12, 0], [la - h, la - h, la + h, la + h])[0]) / 1e4 for la in ulat}
cell_ha = np.array([area_lat[x] for x in lat])
ne = gpd.read_file(os.path.join(RAW, "ne_50m_admin_0_countries", "ne_50m_admin_0_countries.shp"))
country = np.full(len(r), "", dtype=object); cont = np.full(len(r), "", dtype=object)
sub = (lon > -32) & (lon < 70) & (lat > 25) & (lat < 82)
for _, f in ne.iterrows():
    b = f.geometry.bounds; m = sub & (lon >= b[0]) & (lon <= b[2]) & (lat >= b[1]) & (lat <= b[3]) & (country == "")
    if m.any():
        k = np.where(m)[0][shapely.contains_xy(f.geometry, lon[m], lat[m])]; country[k] = f.ADMIN; cont[k] = f.CONTINENT
inbox = (lon >= BOX[0]) & (lon <= BOX[1]) & (lat >= BOX[2]) & (lat <= BOX[3])
G = g[r, c]; I = inc[r, c]; R = rice[r, c]; A = np.clip(aei[r, c] / cell_ha, 0, 1)
with rasterio.open(os.path.join(AG, "EUROPE_GATE_CLASS_5m.tif")) as s:
    cls = s.read(1); ctr = s.transform
cr, cc = rasterio.transform.rowcol(ctr, lon, lat); cr, cc = np.array(cr), np.array(cc); okc = inbox & (cr >= 0) & (cr < cls.shape[0]) & (cc >= 0) & (cc < cls.shape[1])
K = np.zeros(len(r), np.int8); K[okc] = cls[cr[okc], cc[okc]]
EU27 = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"]
dom = {"Europe_excl_Russia (primary)": inbox & (cont == "Europe") & (country != "Russia"), "EU27 (sensitivity)": inbox & np.isin(country, EU27),
       "Europe_incl_Russia_west_of_45E (sensitivity)": inbox & (cont == "Europe"), "rectangle_-11_45E_34_71.5N (sensitivity, superseded headline)": inbox}
canon = pd.read_csv(os.path.join(AG, "EUROPE_DOMAIN_SENSITIVITY.csv")).set_index("domain")
cmap = {"Europe_excl_Russia (primary)": "Europe_excl_Russia (primary)", "EU27 (sensitivity)": "EU27", "Europe_incl_Russia_west_of_45E (sensitivity)": "Europe_incl_Russia_west_of_45E", "rectangle_-11_45E_34_71.5N (sensitivity, superseded headline)": "rectangle_-11_45E_34_71.5N"}
rows = []
for k, m in dom.items():
    fin = np.isfinite(G); v = m & fin; th = v & (G >= TSTAR); ta = th & (A >= AEI_MIN)
    cr_ = canon.loc[cmap[k]]
    rows.append(dict(domain=k, n_cells=int(v.sum()), incumbent_ha=round(I[v].sum()), incumbent_ha_missing_climate=round(I[m & ~fin].sum()), n_cells_missing_climate=int((m & ~fin).sum()),
                     thermal_fail_ha=round(I[v & (G < TSTAR)].sum()), thermal_pass_ha=round(I[th].sum()), thermal_pass_aei_ha=round(I[ta].sum()),
                     thermal_pass_no_infra_deficit_ha=round(I[th & (A < AEI_MIN) & (K == 2)].sum()) if k.startswith("Europe_excl") else np.nan,
                     thermal_pass_no_infra_nonneg_balance_ha=round(I[th & (A < AEI_MIN) & (K == 3)].sum()) if k.startswith("Europe_excl") else np.nan,
                     thermal_pass_pct=round(100 * I[th].sum() / I[v].sum(), 2), thermal_aei_pct=round(100 * I[ta].sum() / I[v].sum(), 2), spam_rice_ha=round(R[v].sum()),
                     spam_rice_in_thermal_aei_ha=round(R[ta].sum()), canonical_incumbent_Mha=cr_.incumbent_Mha, canonical_thermal_pass_pct=round(100 * cr_.thermal_pass_share, 2),
                     canonical_thermal_aei_pct=round(100 * cr_.thermal_aei_share, 2)))
gc = pd.DataFrame(rows); gc["abs_diff_incumbent_Mha"] = (gc.incumbent_ha / 1e6 - gc.canonical_incumbent_Mha).abs().round(3)
gc["abs_diff_thermal_pp"] = (gc.thermal_pass_pct - gc.canonical_thermal_pass_pct).abs().round(2); gc["abs_diff_thermal_aei_pp"] = (gc.thermal_aei_pct - gc.canonical_thermal_aei_pct).abs().round(2)
gc.to_csv(os.path.join(FA, "EUROPE_SPATIAL_GATE_COUNTS.csv"), index=False)
# excluded regions inside the rectangle
ex = inbox & ~dom["Europe_excl_Russia (primary)"]
grp = np.where(country == "Russia", "Russia (European part, west of 45E)", np.where(cont == "Africa", "North Africa", np.where(np.isin(country, ["Turkey"]), "Anatolia and East Thrace (Turkey)",
      np.where(np.isin(country, ["Georgia", "Armenia", "Azerbaijan"]), "South Caucasus", np.where(np.isin(country, ["Cyprus", "Northern Cyprus"]), "Cyprus (NE: Asia)",
      np.where(country == "Kazakhstan", "Kazakhstan west of 45E", np.where(country == "", "no NE country at cell centre (coast)", "Other Asia (Levant, Iraq, Iran)")))))))
exr = pd.DataFrame({"g": grp[ex], "I": I[ex]}).groupby("g").I.sum().div(1e6).round(2).sort_values(ascending=False)
eur_out = (cont == "Europe") & ~inbox & (country != "Russia"); out_c = pd.DataFrame({"c": country[eur_out], "I": I[eur_out]}).groupby("c").I.sum().div(1e3).round(1).sort_values(ascending=False)
# diagnostic map
ny, nx = int((BOX[3] - BOX[2]) * 12), int((BOX[1] - BOX[0]) * 12); M = np.zeros((ny, nx), np.int8)
ii = ((BOX[3] - lat[inbox]) * 12).astype(int); jj = ((lon[inbox] - BOX[0]) * 12).astype(int); ok = (ii < ny) & (jj < nx)
pri = dom["Europe_excl_Russia (primary)"][inbox]; code = np.where(pri, np.where(~np.isfinite(G[inbox]), 6, np.where(G[inbox] < TSTAR, 1, np.where(A[inbox] >= AEI_MIN, 3, 2))), np.where(country[inbox] == "Russia", 4, 5))
M[ii[ok], jj[ok]] = code[ok]
fig, ax = plt.subplots(figsize=(8, 6.2), constrained_layout=True)
cm = ListedColormap(["white", "#2b6cb0", "#f6e05e", "#2f855a", "#a0aec0", "#e2b4b4", "black"])
ax.imshow(M, cmap=cm, vmin=0, vmax=6, extent=[BOX[0], BOX[1], BOX[2], BOX[3]], interpolation="nearest")
ne.cx[BOX[0]:BOX[1], BOX[2]:BOX[3]].boundary.plot(ax=ax, lw=0.2, color="k"); ax.set_xlim(BOX[0], BOX[1]); ax.set_ylim(BOX[2], BOX[3])
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=cm(i / 6), label=l) for i, l in [(1, "primary: thermal fail"), (2, "primary: thermal pass, AEI<10%"), (3, "primary: thermal pass, AEI≥10%"), (4, "excluded: Russia"), (5, "excluded: N Africa/Anatolia/Caucasus/Cyprus/other"), (6, "primary: missing climate")]], fontsize=6.5, loc="lower left")
ax.set_title(f"Primary denominator (Europe excl. Russia, {gc.incumbent_ha[0]/1e6:.1f} Mha incumbent arable) and excluded cropland, 5′ cells", fontsize=8)
fig.savefig(os.path.join(FA, "EUROPE_DENOMINATOR_DIAGNOSTIC_MAP.png"), dpi=200); plt.close(fig)
p = gc.iloc[0]
prov = f"""# Europe domain and mask provenance

Generated by `modern_rice/scripts/ag_europe_denominator_audit.py`.

| Element | Definition used in the pipeline (`ag_grid_gates.py`) | Source / version |
|---|---|---|
| Analysis grid | 5′ (1/12°) regular latitude–longitude grid aligned to WorldClim/SPAM/GMIA global origin (−180, 90); CRS EPSG:4326. Figures are reprojected to EPSG:3035 for display only | WorldClim 2.1; MapSPAM 2010 v2.0; FAO GMIA v5 |
| Processing window | rectangle {BOX[0]}–{BOX[1]}°E, {BOX[2]}–{BOX[3]}°N (used only to clip arrays) | — |
| Primary domain | Natural Earth admin-0 polygons with CONTINENT = Europe, excluding ADMIN = Russia, inside the rectangle; cell-centre assignment (`rasterize`, all_touched = False) | Natural Earth 1:50m admin-0 countries |
| Transcontinental / boundary cases | Turkey, Georgia, Armenia, Azerbaijan, Kazakhstan, Cyprus and Northern Cyprus carry CONTINENT = Asia in Natural Earth and are excluded; Russia is CONTINENT = Europe but excluded by rule; Iceland, the Faroes, the Azores, Madeira and the Canaries lie outside the rectangle | Natural Earth attribute CONTINENT |
| Cyprus | excluded from the primary domain (NE: Asia) but included in the EU27 sensitivity domain | — |
| Denominator ("incumbent arable") | SPAM 2010 harvested area (all technologies, ha per 5′ cell) of wheat + maize + barley + potato; cells with zero incumbent area are outside the denominator | MapSPAM 2010 v2.0, doi:10.7910/DVN/PRFF8V |
| Pixel area | not needed for the denominator (SPAM is already in ha per cell); used only to convert GMIA area equipped (ha) into a share of cell area: spherical cell area, R = 6371.0072 km | FAO GMIA v5 (aei_ha) |
| Missing data | cells without a WorldClim value excluded from numerator and denominator ({p.n_cells_missing_climate} cells, {p.incumbent_ha_missing_climate:,.0f} ha incumbent in the primary domain); GMIA nodata (−9) and SPAM negatives set to 0 | — |
| Thermal gate | GDD10 over 29 Apr–11 Sep from WorldClim 2.1 monthly tavg ≥ T* = {TSTAR:.0f} | — |
| Irrigation-infrastructure gate | GMIA area equipped for irrigation ≥ {AEI_MIN:.0%} of cell area (AEI ≥ 10%); sensitivity in `EUROPE_AEI_THRESHOLD_SENSITIVITY.csv` | FAO GMIA v5 |
| Rainfed-balance gate | Jun–Sep crop water deficit D = Σ(Kc·ET0,Hargreaves − P) at 10′ (WorldClim tmin/tmax/prec), replicated to 5′; D > 0 = deficit | WorldClim 2.1 10′ |
| Gate logic | non-compensatory: class 1 thermal fail; class 4 thermal pass and AEI ≥ 10%; classes 2/3 thermal pass, AEI < 10%, with D > 0 / D ≤ 0 | — |
| Interpretation | AEI marks mapped irrigation equipment presence in ~2005 (GMIA v5). It does not establish rice-ready land, water rights, delivery capacity, permits or economic feasibility | — |
"""
open(os.path.join(FA, "EUROPE_DOMAIN_AND_MASK_PROVENANCE.md"), "w").write(prov)
tab = gc[["domain", "n_cells", "incumbent_ha", "thermal_pass_pct", "canonical_thermal_pass_pct", "thermal_aei_pct", "canonical_thermal_aei_pct", "abs_diff_incumbent_Mha"]]
aud = f"""# Europe spatial denominator audit

Generated by `modern_rice/scripts/ag_europe_denominator_audit.py` (independent of `ag_grid_gates.py`: no shared code; different country assignment, GDD integration and cell-area method). Diagnostic map: `EUROPE_DENOMINATOR_DIAGNOSTIC_MAP.png`.

## Independent recomputation vs canonical outputs

| Domain | Cells | Incumbent ha (independent) | Thermal pass % (indep.) | Thermal pass % (canonical) | Thermal + AEI % (indep.) | Thermal + AEI % (canonical) | |Δ| Mha |
|---|---|---|---|---|---|---|---|
""" + "\n".join(f"| {a.domain} | {a.n_cells:,} | {a.incumbent_ha:,.0f} | {a.thermal_pass_pct:.2f} | {a.canonical_thermal_pass_pct:.2f} | {a.thermal_aei_pct:.2f} | {a.canonical_thermal_aei_pct:.2f} | {a.abs_diff_incumbent_Mha:.3f} |" for a in tab.itertuples()) + f"""

Primary-domain hectares (independent): incumbent {p.incumbent_ha:,.0f}; thermal fail {p.thermal_fail_ha:,.0f}; thermal pass {p.thermal_pass_ha:,.0f}; thermal pass with AEI ≥ 10% {p.thermal_pass_aei_ha:,.0f}; thermal pass, AEI < 10%, rainfed deficit {p.thermal_pass_no_infra_deficit_ha:,.0f}; thermal pass, AEI < 10%, non-negative balance {p.thermal_pass_no_infra_nonneg_balance_ha:,.0f}. SPAM rice in the domain {p.spam_rice_ha:,.0f} ha, of which {p.spam_rice_in_thermal_aei_ha:,.0f} ha in thermal + AEI cells.

Maximum differences against canonical: {gc.abs_diff_incumbent_Mha.max():.3f} Mha, {gc.abs_diff_thermal_pp.max():.2f} pp (thermal), {gc.abs_diff_thermal_aei_pp.max():.2f} pp (thermal + AEI). Residual differences come from boundary cells (rasterize vs point-in-polygon on identical cell centres; overlapping polygons) and from the ellipsoidal vs spherical cell area in the AEI share.

## Incumbent arable inside the processing rectangle but outside the primary domain (Mha)

| Region | Mha |
|---|---|
""" + "\n".join(f"| {k} | {v:.2f} |" for k, v in exr.items()) + f"""

## European (NE CONTINENT = Europe, excl. Russia) incumbent arable outside the rectangle (kha)

| Country | kha |
|---|---|
""" + "\n".join(f"| {k} | {v:.1f} |" for k, v in out_c.items() if v > 0) + """

## Decisions

* The headline denominator is the primary domain (Europe excluding Russia). The rectangle result (which adds North Africa, Anatolia, the Caucasus and European Russia) is reported only as a sensitivity and is the superseded headline of the earlier draft.
* EU27 and Europe-including-Russia are sensitivities.
* Mapped irrigation presence (AEI) is a screening indicator only; it is not operational rice feasibility.
"""
open(os.path.join(FA, "EUROPE_SPATIAL_DENOMINATOR_AUDIT.md"), "w").write(aud)
print(tab.to_string()); print(exr); print(out_c.head())
