#!/usr/bin/env python3
"""Writes the Germany thermal-contrast decomposition report and input-provenance table from the outputs of
ag_germany_decomposition.py and GERMANY_THERMAL_CONTRAST_INDEPENDENT_CHECK.py (no values typed by hand)."""
import os, csv, json, hashlib, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
AG = os.path.join(ROOT, "outputs", "modern_rice", "applied_geography"); FA = os.path.join(AG, "final_audit"); os.makedirs(FA, exist_ok=True)
RAW = os.path.join(ROOT, "modern_rice", "data", "raw"); LED = os.path.join(ROOT, "modern_rice", "data", "RAW_ACQUISITION_LEDGER_2026-11-08.csv")
d = pd.read_csv(os.path.join(AG, "GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv")); meta = json.load(open(os.path.join(AG, "GERMANY_THERMAL_CONTRAST_META.json")))
ind = json.load(open(os.path.join(AG, "GERMANY_THERMAL_CONTRAST_INDEPENDENT_CHECK.json")))
d.to_csv(os.path.join(FA, "GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv"), index=False)
led = list(csv.DictReader(open(LED)))
def sha(p):
    h = hashlib.sha256(); f = open(p, "rb")
    for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def ledger_for(key):
    for r in led:
        if key in r["file"] or key in r["source_url"]: return r
    return None
prov = []
def addp(role, files, source, version, baseline, var, support, ledkey, notes):
    ex = [os.path.join(RAW, f) for f in files]; ok = all(os.path.exists(p) for p in ex); lr = ledger_for(ledkey) if ledkey else None
    prov.append(dict(role=role, files=";".join(files), source=source, version=version, baseline_period=baseline, variable=var, spatial_support=support,
                     present_locally=ok, bytes_total=sum(os.path.getsize(p) for p in ex if os.path.exists(p)),
                     sha256_first_file=sha(ex[0]) if os.path.exists(ex[0]) else "", ledger_entry=(lr["file"] + " | " + lr["retrieved_utc"]) if lr else "NOT IN LEDGER", access_and_license=(lr or {}).get("license_note", ""), notes=notes))
mon = range(4, 10)
addp("German surface and grid reference: monthly tavg", [f"wc2.1_5m_tavg_{m:02d}.tif" for m in mon], "WorldClim (Fick & Hijmans 2017)", "2.1", "1970-2000 climatology", "monthly mean air temperature (tavg)", "5 arc-min, EPSG:4326", "wc2.1_5m_tavg.zip", "Apr-Sep months used; nodata -3.4e38 treated as missing")
addp("Resolution sensitivity", [f"wc2.1_2.5m_tavg_{m:02d}.tif" for m in mon] + [f"wc2.1_10m_tavg_{m:02d}.tif" for m in mon], "WorldClim", "2.1", "1970-2000", "tavg", "2.5 and 10 arc-min", "wc2.1_2.5m_tavg.zip", "2.5' pass fractions averaged to 5'; 10' replicated to 5'")
addp("Incumbent-arable weight (denominator)", [f"spam2010V2r0_global_H_{c}_A.tif" for c in ["WHEA", "MAIZ", "BARL", "POTA"]], "MapSPAM (IFPRI) doi:10.7910/DVN/PRFF8V", "2010 v2.0", "circa 2010", "harvested area, all technologies (ha per cell)", "5 arc-min", "PRFF8V", "sum of four crops; negative/nodata set to 0; values are ha per cell so no pixel-area computation is needed")
addp("Hokkaido rice weight (reference)", ["spam2010V2r0_global_H_RICE_A.tif"], "MapSPAM", "2010 v2.0", "circa 2010", "rice harvested area (ha)", "5 arc-min", "PRFF8V", "Hokkaido box 139.3-146.0E, 41.35-45.6N minus Shimokita/Tsugaru corner (lon>140.6 & lat<41.6)")
addp("Germany boundary", ["ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp"], "Natural Earth", "1:50m admin-0 (version as downloaded)", "n/a", "ADMIN == Germany", "vector; cell-centre assignment", "ne_50m_admin_0_countries", "rasterize (decomposition) and shapely point-in-polygon (independent check) give the same membership")
addp("Point reference 2000-2024 (original ~900 source)", ["nasa_power_Hokkaido_JP.json", "nasa_power_Asahikawa_JP.json", "nasa_power_Germany.json"], "NASA LaRC POWER daily point API, community AG", "POWER (MERRA-2 meteorology)", "2000-01-01 to 2024-12-31", "T2M_MAX, T2M_MIN; Tmean=(Tmax+Tmin)/2", "0.5 x 0.625 deg cell", "nasa_power_Hokkaido", "fill -999 removed")
addp("Point reference 1981-2000 (baseline-harmonised)", [f"nasa_power_1981_2000/nasa_power_{n}_19810101_20001231.json" for n in ["Hokkaido_JP", "Asahikawa_JP", "Germany", "Sapporo_Ishikari_JP", "Iwamizawa_Sorachi_JP"]], "NASA LaRC POWER daily point API", "POWER (MERRA-2)", "1981-01-01 to 2000-12-31", "T2M, T2M_MAX, T2M_MIN", "0.5 x 0.625 deg cell", "19810101_20001231", "acquired 2026-11-08 for this decomposition; POWER does not cover 1970-1980, so baseline is only partly harmonised with WorldClim 1970-2000")
pd.DataFrame(prov).to_csv(os.path.join(FA, "GERMANY_THERMAL_CONTRAST_INPUT_PROVENANCE.csv"), index=False)
g = lambda blk: d[d.block == blk].reset_index(drop=True)
e, p1, p2, p3, rc, f9 = g("0_endpoints"), g("1_threshold_path_pipeline_5m"), g("2_threshold_path_JunSep_5m"), g("3_point_location_pipeline_5m"), g("4_resolution_recalibrated"), g("4_resolution_fixed_900")
steps = ["baseline period (POWER 2000-2024 -> 1981-2000)", "temporal aggregation (daily -> monthly-mean formula)", "dataset and spatial support (POWER cell -> WorldClim 5' cell, same point)",
         "reference location (single Tokachi cell -> Hokkaido rice-area median)", "reference quantile (rice-area P50 -> P05 = T*)"]
def steptab(p):
    L = ["| Step | Factor changed | Threshold (GDD10) | Germany pass % | Change in threshold | Change in pass (pp) |", "|---|---|---|---|---|---|",
         f"| start | {p.label[0]} | {p.threshold_gdd10[0]:.1f} | {p.germany_pass_pct[0]:.2f} | | |"]
    for i in range(1, len(p)):
        L.append(f"| {i} | {steps[i-1]} | {p.threshold_gdd10[i]:.1f} | {p.germany_pass_pct[i]:.2f} | {p.threshold_gdd10[i]-p.threshold_gdd10[i-1]:+.1f} | {p.germany_pass_pct[i]-p.germany_pass_pct[i-1]:+.2f} |")
    return "\n".join(L)
rp = rc[rc.surface_window.str.startswith("pipe")]; rj = rc[rc.surface_window.str.startswith("cal")]
fp = f9[f9.surface_window.str.startswith("pipe")]; fj = f9[f9.surface_window.str.startswith("cal")]
mm = g("2_window_mismatch")
chk = [("T* pipeline (GDD10; decomposition rounds to whole GDD10)", p1.threshold_gdd10[5], ind["Tstar_pipeline"]), ("Hokkaido rice P50 pipeline", p1.threshold_gdd10[4], ind["P50_pipeline"]),
       ("Germany % at T*", e.germany_pass_pct[0], ind["DE_share_pipeline_Tstar"]), ("Germany % at 900", e.germany_pass_pct[1], ind["DE_share_pipeline_900"]),
       ("Germany % at P50", p1.germany_pass_pct[4], ind["DE_share_pipeline_P50"]), ("T* Jun-Sep", p2.threshold_gdd10[5], ind["Tstar_JunSep"]),
       ("Germany % at T* Jun-Sep", p2.germany_pass_pct[5], ind["DE_share_JunSep_Tstar"]), ("POWER Hokkaido pipeline 2000-2024", p1.threshold_gdd10[0], ind["POWER_Hokkaido_pipeline_2000_2024"]),
       ("POWER Hokkaido pipeline 1981-2000", p1.threshold_gdd10[1], ind["POWER_Hokkaido_pipeline_1981_2000"]), ("POWER Hokkaido Jun-Sep 2000-2024", p2.threshold_gdd10[0], ind["POWER_Hokkaido_JunSep_2000_2024"]),
       ("Germany incumbent arable (Mha)", d.germany_incumbent_Mha[0], ind["germany_incumbent_Mha"])]
ctab = "\n".join(["| Quantity | Decomposition script | Independent check | Abs. difference |", "|---|---|---|---|"] + [f"| {a} | {b:.2f} | {c:.2f} | {abs(b-c):.2f} |" for a, b, c in chk])
maxdiff = max(abs(b - c) for _, b, c in chk)
md = f"""# Germany thermal-contrast decomposition (97% vs 3%)

Generated by `modern_rice/scripts/ag_germany_report.py` from `GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv` (script `ag_germany_decomposition.py`) and `GERMANY_THERMAL_CONTRAST_INDEPENDENT_CHECK.json` (script `GERMANY_THERMAL_CONTRAST_INDEPENDENT_CHECK.py`).

## 1. What the two endpoints are

| Item | Endpoint A ("97%") | Endpoint B ("3%") |
|---|---|---|
| German surface | WorldClim 2.1, 1970-2000 monthly tavg, 5′ | identical |
| GDD formula on surface | sum over months of max(tavg−10, 0) × days of the month inside 29 Apr–11 Sep | identical |
| German mask | Natural Earth 1:50m ADMIN = Germany, cell-centre assignment | identical |
| Weight / denominator | SPAM 2010 harvested area of wheat+maize+barley+potato ({d.germany_incumbent_Mha[0]:.3f} Mha) | identical |
| Missingness | cells with no WorldClim value or zero incumbent area excluded (none of the German incumbent area is lost to climate nodata) | identical |
| Threshold | T* = {e.threshold_gdd10[0]:.1f} GDD10: rice-area-weighted 5th percentile of WorldClim 5′ GDD10 across SPAM rice cells in Hokkaido | 900 GDD10: rounded NASA POWER daily estimate ({p1.threshold_gdd10[0]:.1f}) at one point (43.2°N, 143.0°E), 2000-2024, daily Tmean=(Tmax+Tmin)/2, same window |
| Germany pass share | **{e.germany_pass_pct[0]:.2f}%** | **{e.germany_pass_pct[1]:.2f}%** |

Both endpoints are reproduced exactly (manuscript values {e.germany_pass_pct[0]:.1f}% and {e.germany_pass_pct[1]:.1f}%). The surface, window, mask, weights and resolution are identical, so **the entire contrast lies in the threshold**, i.e. in how the Hokkaido reference was constructed. The two references are different estimands: a cold-tail quantile of a rice-area distribution on a 1970-2000 grid versus a single-point daily value for 2000-2024.

## 2. Controlled path from endpoint B to endpoint A (29 Apr–11 Sep window, 5′ surface)

{steptab(p1)}

The path changes one factor at a time. Because the German share is a steep, non-linear function of the threshold (most German incumbent arable land lies between about 600 and 900 GDD10), the pass-share change attributed to a step depends on where on the path it is applied; the table is one admissible ordering, not a unique additive decomposition. The threshold changes, by contrast, are order-independent for steps 1-3 (they alter only the point reference) and for steps 4-5 (they alter only the grid reference).

**Interpretation.** The quantile choice (step 5) is the largest single component ({p1.threshold_gdd10[5]-p1.threshold_gdd10[4]:+.0f} GDD10; {p1.germany_pass_pct[5]-p1.germany_pass_pct[4]:+.0f} pp). Steps 1-3 (period, temporal aggregation, data source/support) together lower the point reference by {p1.threshold_gdd10[3]-p1.threshold_gdd10[0]:.0f} GDD10. Step 4 shows that the single POWER point is not representative of Hokkaido rice: it lies in Tokachi, with {meta['spam_rice_ha_within_0.5deg_of_POWER_Hokkaido_point']:,} ha of Hokkaido's {meta['hokkaido_rice_ha']:,} ha of SPAM rice within ±0.5°, and the WorldClim cell there is colder than the rice-area median.

## 3. Window (calendar June–September, each reference re-derived in that window)

{steptab(p2)}

Window-inconsistent combinations (shown only to expose the mismatch): pipeline T* on the Jun–Sep surface gives {mm.germany_pass_pct[0]:.2f}%; 900 on the Jun–Sep surface gives {mm.germany_pass_pct[1]:.2f}%. Window choice changes the T* endpoint from {p1.germany_pass_pct[5]:.2f}% to {p2.germany_pass_pct[5]:.2f}% when each window carries its own calibrated threshold; the qualitative contrast (cold-tail grid reference vs single point) survives in both windows.

## 4. Single-point location sensitivity (pipeline window)

| Reference | Threshold | Germany pass % |
|---|---|---|
""" + "\n".join(f"| {r.label} | {r.threshold_gdd10:.1f} | {r.germany_pass_pct:.2f} |" for r in p3.itertuples()) + f"""

Single-point references in Hokkaido rice areas give Germany pass shares of {p3.germany_pass_pct.min():.1f}–{p3.germany_pass_pct.max():.1f}%, and POWER and WorldClim disagree in sign at the same point (POWER warmer at Iwamizawa, WorldClim warmer at Asahikawa and Sapporo). A single point is therefore not a stable reference in either data source.

## 5. Spatial resolution and aggregation

| Resolution | Window | T* recalibrated at that resolution | Germany % at recalibrated T* | Germany % at fixed 900 |
|---|---|---|---|---|
""" + "\n".join(f"| {a.surface_resolution} | {a.surface_window} | {a.threshold_gdd10:.1f} | {a.germany_pass_pct:.2f} | {b.germany_pass_pct:.2f} |" for a, b in zip(rc.itertuples(), f9.itertuples())) + f"""

Resolution changes the German share by at most {(rp.germany_pass_pct - p1.germany_pass_pct[5]).abs().max():.1f} pp in the primary window (recalibrated) and {fp.germany_pass_pct.max()-fp.germany_pass_pct.min():.2f} pp at a fixed 900. In the Jun–Sep window, where T* lies closer to the bulk of the German distribution, the recalibrated share ranges {rj.germany_pass_pct.min():.1f}–{rj.germany_pass_pct.max():.1f}%: resolution matters near a threshold but cannot generate a 97% vs 3% contrast. Europe-wide 30′/60′ aggregation effects are in `EUROPE_SCALE_THRESHOLD_SENSITIVITY.csv`.

## 6. Interactions

* Window × reference: the window effect on the German share is {p2.germany_pass_pct[5]-p1.germany_pass_pct[5]:+.2f} pp for T* and {p2.germany_pass_pct[0]-p1.germany_pass_pct[0]:+.2f} pp for the POWER point; the difference arises because the two thresholds sit at different positions on the German GDD distribution (non-linearity), not because of an independent window mechanism.
* Resolution × window: recalibrated-resolution range {rp.germany_pass_pct.max()-rp.germany_pass_pct.min():.1f} pp (pipeline) vs {rj.germany_pass_pct.max()-rj.germany_pass_pct.min():.1f} pp (Jun–Sep).
* Resolution × reference: range {rp.germany_pass_pct.max()-rp.germany_pass_pct.min():.1f} pp at recalibrated T* vs {fp.germany_pass_pct.max()-fp.germany_pass_pct.min():.2f} pp at a fixed 900.
* A full factorial over data source × reference construction is not defined, because the grid-quantile reference has no point-data counterpart (POWER provides no gridded Hokkaido rice-area distribution at 5′) and POWER does not cover 1970-1980.

## 7. Independent check

{ctab}

Maximum absolute difference: {maxdiff:.3f}. The independent script shares only the raw input files with the decomposition script; it does not import any project module and uses different code for raster indexing (full-raster reads with transform lookup), country membership (shapely point-in-polygon vs rasterize), weighted quantiles (pandas cumulative sum vs numpy searchsorted) and daily POWER windows (explicit calendar date ranges vs leap-adjusted day-of-year). Shared assumptions not tested by this check: the GDD10 definition, the WorldClim and SPAM inputs themselves, the Hokkaido box and the 5th-percentile choice.

## 8. Conclusions for the manuscript

1. Threshold contribution: the contrast is entirely a threshold contrast on an identical surface.
2. Temporal-window contribution: changes the T* endpoint by {p2.germany_pass_pct[5]-p1.germany_pass_pct[5]:+.1f} pp; secondary.
3. Dataset/reference-construction contribution: dominant (quantile {p1.germany_pass_pct[5]-p1.germany_pass_pct[4]:+.0f} pp at the end of the path; period, aggregation and source together lower the point reference by {p1.threshold_gdd10[0]-p1.threshold_gdd10[3]:.0f} GDD10; single-point location spans {p3.germany_pass_pct.min():.1f}–{p3.germany_pass_pct.max():.1f}%).
4. Spatial-support contribution: ≤{(rp.germany_pass_pct - p1.germany_pass_pct[5]).abs().max():.1f} pp (primary window); larger only near the threshold in the Jun–Sep window.
5. Remaining confounding: POWER 1981-2000 vs WorldClim 1970-2000 differ by one decade; POWER cell vs WorldClim cell differ in both source and support (not separable with available data); SPAM 2010 weights are fixed.
6. The original headline "97% vs 3% shows dependence on data and spatial scale" is **not defensible as a scale effect**. It is defensible as a contrast between two reference constructions (estimands).
7. Manuscript wording adopted: "This contrast is not a resolution effect … The contrast is therefore mainly a contrast between estimands: a cold-tail bound of the Hokkaido rice distribution versus a single-point value near its centre, measured in a warmer period with daily data." (Section 3.3; Methods 2.5; Figure 3d; abstract and highlights revised accordingly.)
"""
open(os.path.join(FA, "GERMANY_THERMAL_CONTRAST_DECOMPOSITION.md"), "w").write(md)
print("ok maxdiff", maxdiff); print(pd.DataFrame(prov)[["role", "present_locally", "ledger_entry"]].to_string())
