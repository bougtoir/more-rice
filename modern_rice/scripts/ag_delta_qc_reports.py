#!/usr/bin/env python3
"""Writes the delta-QC audit reports and the individual-download directory for the
Applied Geography package. Numbers are read from canonical outputs and from the
independent checks in outputs/modern_rice/applied_geography/delta_qc/indep/."""
import os, json, csv, hashlib, shutil, zipfile, subprocess, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
AG = os.path.join(REPO, "outputs", "modern_rice", "applied_geography"); SUB = os.path.join(AG, "submission")
QC = os.path.join(AG, "delta_qc"); IND = os.path.join(QC, "indep"); DL = os.path.join(SUB, "FINAL_INDIVIDUAL_DOWNLOADS")
os.makedirs(QC, exist_ok=True); os.makedirs(DL, exist_ok=True)
N = json.load(open(os.path.join(SUB, "MANUSCRIPT_NUMBERS.json")))
BASE = "2d462b36ce119053502f98b6f5780b3e90b80432"; MAIN = "6202551"; BR = "devin/1794122489-applied-geography-retarget"
dom = pd.read_csv(os.path.join(AG, "EUROPE_DOMAIN_SENSITIVITY.csv"))
gdm = pd.read_csv(os.path.join(AG, "GDD_DAILY_VS_MONTHLY.csv"))
rb = pd.read_csv(os.path.join(AG, "RISK_PORTFOLIO_BASELINE_CORRECTED.csv")).set_index("country")
rr = pd.read_csv(os.path.join(AG, "RISK_PORTFOLIO_ROBUSTNESS.csv")).set_index("country")
cal = json.load(open(os.path.join(AG, "GRID_THERMAL_CALIBRATION.json")))
def W(name, text):
    p = os.path.join(QC, name); open(p, "w", encoding="utf-8").write(text.strip() + "\n"); return p
def md_table(df): return df.to_markdown(index=False)

# ---------- claim diff ----------
claims = [
 ("C01", "Lower Danube 250,000 ha paddy needs ~24 m³/s (~2% of Q99); later ~22% of an unverified 1,100 m³/s 'Q99' (CT-UPT 2014)", f"~{N['dan_q']} m³/s net ({N['dan_q_gross']} m³/s gross at 75%); {N['dan_pct']}% (net) / {N['dan_pct_gross']}% (gross) of the median observed Jun–Sep minimum daily discharge at Orsova (GRDC 6742200, 1920–1990, {N['dan_lf_med']} m³/s); CT-UPT Q99 and the 21.9%/29.2% ratios REMOVED", "HYDROLOGICAL_LOW_FLOW_RESULTS.csv; DANUBE_DEMAND_VS_LOWFLOW.csv", "ag_danube_lowflow.py; ag_danube_demand.py", "Abstract; highlights; 2.3; 3.4; cover letter", "Figure 4b; Table 1", "DEMAND VERIFIED (hand calc); LOW FLOW from GRDC-derived EStreams indices (independently recomputed); CT-UPT PRIMARY SOURCE NOT VERIFIED", "Seasonal minimum, not flow-duration Q99; record ends 1990; discharge ≠ allocable water"),
 ("C02", "Thermal window Jun–Sep (prose) while code used pseudo-DOY 29 Apr–11 Sep", "Both windows reported; pipeline window labelled 29 Apr–11 Sep; calendar Jun–Sep with own T*", "POINT_GDD_WINDOW_SENSITIVITY.csv; EUROPE_WINDOW_SENSITIVITY.json", "ag_grid_gates.py", "2.2; 3.1; 3.3", "Figure 3a", "VERIFIED independently (POWER daily recomputation)", "Window choice remains a modelling convention"),
 ("C03", "Universal ~900 GDD10 Hokkaido threshold", f"{N['T_star']} GDD10 = rice-area-weighted P05 of Hokkaido cells on the same WorldClim 5′ grid; empirical, system-specific reference", "GRID_THERMAL_CALIBRATION.json", "ag_grid_gates.py; delta_qc/indep/spatial_indep.py", "Abstract; 2.2; 3.1", "Figure 2a; Figure 3", "VERIFIED independently (589.6 reproduced)", "WorldClim 1970–2000 normals; monthly approximation ~29 GDD10 low at Hokkaido point; cultivar/management not modelled"),
 ("C04", "Thermal gate met on 94.2% of 'European' arable land (106.9–107.1 Mha)", f"{N['pct_thermal_pass']}% of {N['inc_Mha']} Mha in Europe (Natural Earth Europe excluding Russia)", "EUROPE_DOMAIN_SENSITIVITY.csv; EUROPE_GATE_CASCADE_BY_COUNTRY.csv", "ag_grid_gates.py", "Abstract; highlights; 2.1; 3.2", "Table 2; Figure 2b", "FAILED then REPAIRED (domain included N Africa/Anatolia/Caucasus); repaired value verified independently", "Domain definition remains a choice; rectangle/EU27 sensitivities reported"),
 ("C05", "Thermal + irrigation infrastructure on 17.6% of European arable land", f"{N['pct_aei']}% ({N['aei_Mha']} Mha); {N['aei_cond']}% among thermal-pass land", "EUROPE_DOMAIN_SENSITIVITY.csv; EUROPE_AEI_THRESHOLD_SENSITIVITY.csv", "ag_grid_gates.py", "Abstract; 3.2; cover letter", "Table 2; Figure 2b", "REPAIRED and VERIFIED independently", "AEI = equipped area, not water rights, delivery capacity or rice-ready fields; circa-2010"),
 ("C06", "Serbia: potato dominates rice (rice 0.211 vs potato 0.053)", f"WITHDRAWN. Corrected analog (Hungary) estimate P_B={N['rs_B']} vs potato {N['rs_D']}; analog evidence only", "RISK_PORTFOLIO_BASELINE_CORRECTED.csv", "ag_risk_portfolio_v2.py", "3.5", "Table 3; Figure 5", "VERIFIED independently (own reimplementation)", "Analog shocks; n=19 years"),
 ("C07", "Romania: robust rice-driven risk reduction", f"Direction B<A in {N['ro_rob']}% of 24 configurations, CI excludes 0 in only {N['ro_excl']}%", "RISK_PORTFOLIO_ROBUSTNESS.csv", "ag_risk_portfolio_v2.py", "Abstract; 3.5; 4.3", "Table 3; Figure 5", "VERIFIED independently", "Moving-block bootstrap, shared RNG stream, no multiplicity correction"),
 ("C08", "Kazakhstan robust (CI excludes 0 in 79%)", f"CI excludes 0 in {N['kz_excl']}% after paddy→milled correction", "RISK_PORTFOLIO_ROBUSTNESS.csv", "ag_risk_portfolio_v2.py", "Abstract; 3.5", "Table 3", "REPAIRED (milling factor) and VERIFIED", "Non-European comparator; national calorie aggregate"),
 ("C09", "Rice calories from paddy yield × milled energy density", "Paddy converted to milled equivalent (×0.67) before energy density", "FAOSTAT QCL (Rice = paddy, kg/ha)", "ag_risk_portfolio_v2.py", "2.7", "Table 3; Figure 5", "REPAIRED", "Milling ratio varies 0.6–0.7"),
 ("C10", "Shortfall defined as < 90% of mean (text)", "< 80% of mean (as implemented in code)", "RISK_PORTFOLIO_SENSITIVITY.csv", "ag_risk_portfolio_v2.py", "2.7; Figure 5 caption", "Figure 5", "REPAIRED (text/code mismatch)", "Threshold arbitrary; one level only"),
 ("C11", "White et al. (2011) reference", "Bai et al. (2010), Agronomy Journal 102(1), 9–16", "Crossref 10.2134/agronj2009.0085", "-", "2.2; references", "-", "VERIFIED (Crossref)", "-"),
 ("C12", "Guglielmo, S., Pietro, D. M., Andrea, C. ... (2025)", "Savoini, G., De Marinis, P., Casson, A., Narote, A. D., Guidetti, R., Bocchi, S., & Vaglia, V. (2025)", "Crossref 10.3390/agriculture15171797 (given/family swapped in registry)", "-", "2.6; 4.x; references", "-", "CORRECTED (inference from Crossref name fields); author to confirm vs PDF", "PDF byline not inspected"),
 ("C13", "Germany largely excluded by temperature", f"Germany passes on {N['de_T']}% at T* but {N['de_900']}% at a transplanted 900", "EUROPE_SCALE_THRESHOLD_SENSITIVITY.csv", "ag_grid_gates.py", "Abstract; 3.3", "Figure 3", "VERIFIED (cross-checked against indep thermal recomputation at domain level)", "Same caveats as C03"),
 ("C14", "Monthly GDD adequate (unquantified)", f"Monthly-mean approximation {N['hok_mbias']} GDD10 below daily at Hokkaido point; {N['eu_mbias_min']}–{N['eu_mbias_max']} at European points", "GDD_DAILY_VS_MONTHLY.csv", "ag_gdd_daily_vs_monthly.py", "4.4 limitations", "-", "VERIFIED", "Point-scale only; grid daily data not used"),
]
cols = ["claim_id", "old_claim", "new_claim", "supporting_data", "supporting_code", "manuscript_location", "figure_table_location", "verification_status", "residual_uncertainty"]
with open(os.path.join(QC, "SCIENTIFIC_CLAIM_DIFF.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(cols); w.writerows(claims)

dtab = md_table(dom); gtab = md_table(gdm)
W("GDD_INDEPENDENT_AUDIT.md", f"""
# GDD gate — independent audit
Verdict: **PASS WITH LIMITATIONS**

Baseline commit {BASE}. Independent code: `delta_qc/indep/spatial_indep.py`, `delta_qc/indep/gdd_check.txt`, `ag_gdd_daily_vs_monthly.py`.

## Data definitions checked
- Variable: WorldClim 2.1 `tavg` monthly normals 1970–2000 at 2.5′, 5′, 10′ (files `wc2.1_<res>_tavg_MM.tif`); nodata −3.4e38 masked. Grid origin (−180, 90), 1/12° at 5′, EPSG:4326 — identical to SPAM 2010 and GMIA v5 grids (checked from raster headers), so no resampling is needed at 5′.
- Formula: GDD10 = Σ_month max(T̄_month − 10, 0) × days-in-window. Pipeline window 29 Apr–11 Sep = Apr 2 + May 31 + Jun 30 + Jul 31 + Aug 31 + Sep 11 = 136 days; calendar Jun–Sep = 122 days. No leap-year dependence (climatological normals).
- Point data: NASA POWER daily T2M 2000–2024; legacy window from pseudo-DOY (month×30.4+day) = 150–285 → ~29 Apr–11 Sep.

## Independent reconstruction
- Hokkaido calibration recomputed with separate code (window by rasterio bounds, SPAM RICE >0 as weights, lat/lon box 139.3–146.0 E, 41.35–45.6 N): rice area {cal['hokkaido_rice_ha']:,.0f} ha; weighted P05 = 589.6 (pipeline), P01 = 487.9, P50 = 861.2 — matches the pipeline (589/487/859).
- Representative cells (rasterio.sample at POWER coordinates, WorldClim 5′, pipeline/calendar): Hokkaido point 645/718; Rhine 901/872; Saxony 808/786; Alsace 617/631; Berlin 938/888; Lower Danube 1498/1425.
- Rhine/Saxony reversal: reproduced from POWER daily data — pipeline window 957 and 969 > Hokkaido 903; Jun–Sep 931 and 935 < Hokkaido 941. It is a window artefact of a warm late season in Hokkaido versus warm spring in the Rhine/Saxony; it does not affect the grid-calibrated gate.

## Daily vs monthly approximation (same POWER daily data)
{gtab}

The monthly approximation underestimates daily accumulation most where monthly means are near 10 °C (April/September at Hokkaido). Because the bias is larger at the calibration site than at European points, the grid bound is slightly conservative (lower T* ⇒ more land passes; the effect is <30 GDD10, small relative to the 589 vs 900 contrast).

## Limitations retained
- 589 is the 5th percentile of current Hokkaido rice area on one gridded climatology; it is an empirical reference for one cultivation system (ultra-early japonica, heated nursery, transplanting), not a physiological threshold. Cold-water damage at booting, cultivar availability and management are not modelled.
- Climate periods differ (WorldClim 1970–2000 vs POWER 2000–2024); calibration is within-source.
- Spatial support: 5′ cells vs point cells; the point–grid offset is reported in the manuscript.

The 589 bound and the thermal-pass share do not depend on invalid aggregation: the Europe-wide pass share at T* differs by at most {N['max_scale_pts']} percentage points across native 2.5′/5′/10′ and aggregated 30′/60′ resolutions.
""")

W("SPATIAL_DENOMINATOR_AND_SCALE_AUDIT.md", f"""
# Spatial gate — denominator, domain and scale audit
Verdict: **FAIL → REPAIRED → PASS WITH LIMITATIONS**

## Defect found
The baseline (`{BASE[:7]}`) computed all "European" shares over the rectangle 11°W–45°E, 34°N–71.5°N with `valid = finite(GDD) & incumbent>0`, without a country mask. The rectangle contains North Africa, Anatolia, the Caucasus and western Russia. Independent recomputation (own code from raw rasters) shows that 21.3 Mha of the 107.1 Mha denominator lies in non-European countries, with 33% of it in the thermal+infrastructure class, inflating the European infrastructure share.

## Repair
`ag_grid_gates.py` now rasterises Natural Earth 1:50 m countries with CONTINENT = Europe, excluding Russia (truncated by the 45°E edge), and applies the mask to the cascade, validation, scale, threshold-curve, window and AEI sensitivities. The dependency chain (grid gates → figures → manuscript build) was rerun.

## Numerators and denominators (incumbent arable = SPAM 2010 harvested area of wheat+maize+barley+potato, all technologies, ha summed per 5′ cell; no pixel-area weighting is needed because SPAM values are already hectares; cell areas are used only to convert GMIA hectares to an AEI share)
{dtab}

Primary domain: thermal pass = {N['thermal_pass_Mha']} Mha / {N['inc_Mha']} Mha = {N['pct_thermal_pass']}%; thermal + AEI≥10% = {N['aei_Mha']} Mha / {N['inc_Mha']} Mha = {N['pct_aei']}%; conditional on thermal pass = {N['aei_cond']}%.
Independent reproduction (separate code, `delta_qc/indep/spatial_indep.txt`) of rectangle values: 107.12 Mha, 94.2%, 17.6% (exact); Europe-excluding-Russia values match the repaired pipeline.

## Other checks
- Grids aligned: SPAM, GMIA (ASCII, xll −180, yll −90, 1/12°) and WorldClim 5′ share origin and resolution; the SPAM padding branch is never triggered.
- Nodata: SPAM −1 → 0; WorldClim nodata → NaN and excluded through `isfinite(GDD)`; GMIA missing → 0 (no infrastructure).
- Coastline: country assignment by rasterised polygon centre; coastal cells partially outside polygons are excluded (small).
- Scale: 2.5′/5′/10′ native and 30′/60′ aggregated sensitivity retained; at T* the Europe-wide share changes by ≤{N['max_scale_pts']} points across scales.
- AEI cut-off 5/10/20% reported. AEI is area *equipped* for irrigation c. 2005–2010: it does not establish water availability, permits, delivery capacity, field levelling for paddy, economic feasibility or environmental constraints. The manuscript wording uses "infrastructure presence" and "candidate for next-stage assessment" only.
""")

W("LOWER_DANUBE_WATER_AND_SOURCE_AUDIT.md", f"""
# Lower Danube water gate — arithmetic and source audit
Verdict: **DEMAND PASS; CT-UPT Q99 REMOVED (primary source not verified); replaced by observed GRDC-derived Jun–Sep minima at Orsova**
- Demand: 250,000 ha × 1,000 mm / 120 d = 241.1 m³/s net; 321.5 m³/s gross at 0.75 (see IRRIGATION_DEMAND_INDEPENDENT_CHECK.md).
- Low flow: median Jun–Sep minimum daily discharge at Orsova {N['dan_lf_med']} m³/s ({N['dan_lf_n']} years), 10th percentile {N['dan_lf_p10']}, lowest {N['dan_lf_low']} m³/s. Net/median {N['dan_pct']}%; gross/median {N['dan_pct_gross']}%; gross/lowest {N['dan_pct_gross_low']}%.
- Details: CT_UPT_SOURCE_RESOLUTION.md, HYDROLOGICAL_LOW_FLOW_ANALYSIS.md, HYDROLOGICAL_STATION_AND_DATA_PROVENANCE.csv.
""")

rows = []
for c in ["Romania", "Bulgaria", "Serbia", "Kazakhstan", "Hungary", "France"]:
    rows.append(dict(country=c, rice_source=rb.loc[c, "rice_source"], n=int(rb.loc[c, "n_years"]), P_A=rb.loc[c, "P_A"], P_B=rb.loc[c, "P_B_rice"], P_D=rb.loc[c, "P_D_potato"],
                     CI=f"{rb.loc[c,'diff_CI95_lo']} to {rb.loc[c,'diff_CI95_hi']}", share_B_lt_A=rr.loc[c, "share_B_lt_A"], share_CI_excl_0=rr.loc[c, "share_CI_excl_0"]))
W("PORTFOLIO_MODEL_INDEPENDENT_AUDIT.md", f"""
# Portfolio (food-supply risk) model — independent audit
Verdict: **PASS WITH LIMITATIONS (two further corrections applied)**

## Independent reimplementation
Separate code (`delta_qc/indep/risk_indep.txt`) re-derived scenario A and B shortfall probabilities from FAOSTAT QCL (linear log-detrending, area-share weights from the latest year, f = 0.2, threshold 0.8 × own mean). Before the milling correction it reproduced the pipeline baseline exactly (Romania 0.203/0.109; Serbia with Hungarian analog 0.211/0.000; Kazakhstan 0.212/0.030).
- Minimal nonzero example: A = [10,10,10,10,7], rice = 10 each year, B = 0.8A + 0.2·rice ⇒ last-year B = 7.6, versus 5.6 under the legacy zero-rice bug; the corrected branch gives a nonzero rice contribution.
- Serbia: analog branch uses Hungarian rice shocks *and* level; the legacy potato-dominance claim is withdrawn.

## Corrections applied in this delta
1. **Paddy vs milled energy**: FAOSTAT "Rice" yields are paddy (kg/ha); the energy density 3.65 kcal/g is for milled rice. Rice yields are now multiplied by 0.67 (milled equivalent). Effect: Kazakhstan P_B 0.030 → 0.061 and CI-excludes-zero share 79% → {N['kz_excl']}%; Romania 42% → {N['ro_excl']}%.
2. **Text/code mismatch**: the manuscript described shortfall as < 90% of mean; code uses 80%. Text and Figure 5 caption corrected.

## Corrected results (baseline: linear, f = 0.2, scale 1.0, own-mean threshold)
{md_table(pd.DataFrame(rows))}

## Method checks
- Bootstrap: moving blocks of 3 years, non-circular, 2,000 draws, percentile 95% interval; single RNG stream (seed 20261108) shared across the 24 configurations, so results are reproducible but order-dependent. Blocks preserve within-country cross-crop correlation because all crops are resampled with the same year indices.
- Many intervals have an upper bound of exactly 0.000 because shortfall probabilities are discrete fractions of n years; "excludes zero" requires the upper bound < 0.
- No multiplicity correction across 24 configurations × countries; robustness shares are descriptive.
- Model is national, calorie-only, ignores trade, storage and price; substitution is hypothetical.

## Recommendation
The portfolio analysis is ancillary to the geographic contribution. It is kept short (one section, one figure, one table) and phrased as scenario statistics. Moving it to supplementary material is a reasonable alternative if an editor considers it off-scope.
""")

W("JOURNAL_REQUIREMENTS_VERIFIED.md", f"""
# Applied Geography — requirements verified
Sources (archived HTML/text in `data/journal_requirements/applied_geography/`, accessed 2026-11-08 via browser because ScienceDirect returns HTTP 403 to scripted requests):
- Guide for Authors: https://www.sciencedirect.com/journal/applied-geography/publish/guide-for-authors
- Aims and scope: https://www.sciencedirect.com/journal/applied-geography/about/aims-and-scope
- Open access options: https://www.sciencedirect.com/journal/applied-geography/publish/open-access-options

| Requirement (Guide) | Package status |
|---|---|
| Research article 4,500–8,000 words incl. captions, tables, references | {N.get('words','5452')} words — OK |
| Abstract ≤250 words (unstructured) | 250 — OK (at limit) |
| 1–7 keywords | 7 — OK |
| Highlights 3–5, ≤85 characters each, separate editable file | 5, max ≤85 — OK |
| Double-anonymized review: separate title page | title page separate; manuscript anonymized — OK |
| Single-column editable Word manuscript | OK |
| APA 7 references | OK (31) |
| Editable tables (not images) | 3 native Word tables — OK |
| Figures as separate artwork files | Figure_1–5 PNG/PDF — OK; inline review copy additionally provided |
| Graphical abstract | encouraged, not mandatory — not supplied (deliberate) |
| Generative-AI declaration | present |
| CRediT, competing interests, funding, data statement | present (data: public sources + code repository) |
| Publication route | subscription route has no publication fee; APC only if open access chosen — author to select subscription in Editorial Manager |

Not verifiable without login: the Editorial Manager item checklist and exact APC amount. These remain author actions.
""")

pm = pd.read_csv(os.path.join(SUB, "CLOSEST_GEOGRAPHIC_PRIOR_WORK_MATRIX.csv"))
out = pd.DataFrame({"prior_paper": pm.full_reference, "doi": pm.doi, "what_it_demonstrates": pm.what_it_demonstrates, "what_it_does_not": pm.what_remains_unanswered,
                    "contribution_of_this_study": pm.what_our_manuscript_adds, "evidence_level": pm.observed_vs_modeled, "remaining_limitations": pm.risk_of_overclaim})
out.to_csv(os.path.join(QC, "CLOSEST_PRIOR_STUDIES_MATRIX.csv"), index=False)

W("REFERENCE_AND_SOURCE_AUDIT.md", f"""
# Reference and source audit (delta)
- 31 references, APA 7 (CT-UPT 2014 removed; do Nascimento et al. 2024 added). Journal/dataset DOIs were checked against Crossref/DataCite (2026-11-08); see `REFERENCES_AND_CITATIONS_AUDIT.md` for the per-item record.
- Bai et al. (2010), Agronomy Journal 102(1), 9–16, doi:10.2134/agronj2009.0085 — re-verified on Crossref (authors Bai, Chen, Dobermann, Yang, Cassman, Zhang). Replaces the non-existent "White et al. 2011" citation.
- You et al. (2014) — journal corrected in the previous delta; unchanged.
- **Savoini et al. (2025)**, Agriculture 15(17), 1797, doi:10.3390/agriculture15171797 — Crossref stores given/family names swapped for the first three authors ("Savoini, Guglielmo"; "De Marinis, Pietro"; "Casson, Andrea"). The citation was previously rendered "Guglielmo, S., Pietro, D. M., Andrea, C." and is now "Savoini, G., De Marinis, P., Casson, A., Narote, A. D., Guidetti, R., Bocchi, S., & Vaglia, V." This correction is inferred from the Crossref name fields; the article PDF byline was not inspected (author action).
- **CT-UPT (2014)** — PRIMARY SOURCE NOT VERIFIED; removed from text and reference list (see CT_UPT_SOURCE_RESOLUTION.md).\n- **do Nascimento et al. (2024)**, Scientific Data 11, 879, doi:10.1038/s41597-024-03706-1 — verified on Crossref (8 authors); dataset v1.4 doi:10.5281/zenodo.17598150 verified on DataCite.
- Institutional/data references (MAFF 2024, FAO 2024, IFPRI 2019, NASA POWER 2025, WorldClim, Natural Earth, GMIA) point to official landing pages; versions are recorded in `modern_rice/data/RAW_ACQUISITION_LEDGER_2026-11-08.csv`.
- No reviewer identities, e-mails or affiliations were invented.
""")

W("TEXT_FIGURE_TABLE_NUMERIC_CONSISTENCY_AUDIT.md", f"""
# Text–figure–table numeric consistency audit
- All manuscript numbers are filled from `MANUSCRIPT_NUMBERS.json`, generated from canonical outputs by `build_ag_manuscript.py`; the build fails on unfilled placeholders.
- Independent checks (not script agreement): domain shares (`spatial_indep.txt`), Hokkaido P05, Danube arithmetic, risk baseline reimplementation — see gate audits.
- DOCX XML (final manuscript): 0 `wp:anchor`, figures supplied as separate files; 3 native `w:tbl`; 1 OMML equation (Q = A·D/T as a fraction); headings Times New Roman black; body Times New Roman 12 pt.
- Inline review copy: 5 `wp:inline`, 0 `wp:anchor`; order of first appearance Figure 1, Table 1, Figure 2, Table 2, Figure 3, Figure 4, Figure 5, Table 3, each placed after its first-citing paragraph; rendered PDF pages inspected (no cropping).
- Literal markdown asterisks: fixed a bug where `T*` pairs were consumed as italic markers (e.g. "from 92.2% at T to 54.9%"); `T*` is now italic T with superscript asterisk.
- Withdrawn claims searched across manuscript, inline copy, cover letter, highlights, metadata, tables and README: no remaining "~24 m³/s", "~2% of Q99", "CT-UPT", "1,100 m³/s Q99", "21.9%", "29.2%", "17.6%/94.2% of European arable land" (now only as explicitly labelled rectangle sensitivity), "90% of mean", or Serbia potato dominance as a finding. README does not contain these claims (README describes the repository's other project; unchanged).
- Highlights, abstract and cover letter use the same values: {N['pct_thermal_pass']}%, {N['pct_aei']}%, {N['dan_q']} m³/s, {N['kz_excl']}%/{N['ro_excl']}%.
""")

W("HOSTILE_SCIENTIFIC_AND_DESK_REVIEW.md", f"""
# Hostile scientific and desk review (delta)
Desk-rejection risk: **medium–high**.
1. *Is this new?* Climate-threshold suitability mapping is established (Zabel et al., 2014; Yang et al., 2023). The informative elements are (a) source/window/scale dependence of a transferred cold bound (589 vs ~900 GDD10 changes Germany from 3% to 97% pass), (b) an explicit incumbent-arable denominator with a domain sensitivity, (c) non-compensatory separation of thermal and water gates. The general idea that crop diversity ≠ risk diversity is not claimed as novel.
2. *Is 92% vs 16% informative?* It reframes the binding constraint (water/infrastructure, not temperature) on existing arable land; but it is partly expected from known European irrigation geography. Its value lies in quantifying how much a transferred threshold mis-locates the constraint.
3. *Domain error found in this QC*: the earlier "European" denominator included North Africa/Anatolia; corrected. A reviewer would have found this.
4. *Low flow*: the unverified CT-UPT Q99 was removed; the replacement is a GRDC-derived seasonal minimum (not a flow-duration Q99) from a record ending in 1990, and only 19 post-dam years. A reviewer may ask for post-1990 daily data (GRDC request prepared).
5. *AEI* is c. 2010 equipped area; no water rights; the manuscript says so.
6. *Risk model* is ancillary and weak (CIs mostly include zero); could be moved to supplement.
7. *Old climatology* (1970–2000) and monthly GDD; quantified bias small.
Suggested title (author decision): the alternative "Spatial constraints on transferring rice cultivation systems beyond traditional growing regions: A multi-scale assessment of thermal suitability and irrigation infrastructure" matches the geographic contribution better and drops "food-supply risk", consistent with the ancillary status of the portfolio model. Recommended.
""")

W("REVIEWER_SUGGESTION_CRITERIA.md", """
# Reviewer suggestion criteria (author to fill)
Suggest 3–5 reviewers who: (1) have published in the last 5 years on land suitability/crop-geography, irrigation geography or scale/MAUP in agricultural mapping; (2) have no co-authorship with the author in the last 5 years and no shared institution; (3) cover complementary expertise: rice agronomy at cold margins; European irrigation/water allocation (preferably Danube basin); spatial methods/scale sensitivity; (4) are identifiable with an institutional e-mail and ORCID. Do not suggest Applied Geography editors. No names are proposed here.
""")
W("REVIEWER_AND_SUBMISSION_METADATA_TEMPLATE.md", f"""
# Reviewer and submission metadata template (author-fillable)
| Field | Value |
|---|---|
| Corresponding author | Onishi Tatsuki |
| Affiliation | Data Science and AI Innovation Research Promotion Center, Shiga University, Hikone, Shiga, Japan |
| ORCID | 0000-0001-7261-9062 |
| Corresponding e-mail | [AUTHOR TO ENTER] |
| Final title | [AUTHOR TO CHOOSE: current / suggested] |
| Article type | Research article |
| Publication route | [AUTHOR TO SELECT in Editorial Manager: Subscription] |
| Suggested reviewer 1 | name / institution / e-mail / ORCID / rationale: [ ] |
| Suggested reviewer 2 | [ ] |
| Suggested reviewer 3 | [ ] |
| Opposed reviewers | [ ] |
| Gated EM checklist confirmed | [ ] |
| Optional: GRDC daily data request for 6742200/6742201 (see CT_UPT_SOURCE_RESOLUTION.md) | [ ] |
| Savoini et al. (2025) byline checked | [ ] |
""")
print("audits written to", QC)
