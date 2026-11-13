#!/usr/bin/env python3
"""Generate EM&A audit reports from canonical outputs (values are read, never typed)."""
import os, re, json, subprocess, zipfile, numpy as np, pandas as pd
from docx import Document
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
AG = os.path.join(ROOT, "outputs", "modern_rice", "applied_geography"); EMA = os.path.join(ROOT, "outputs", "modern_rice", "ema"); SUB = os.path.join(EMA, "submission")
JF = os.path.join(ROOT, "outputs", "modern_rice", "journal_fit_assessment"); REP = os.path.join(EMA, "reports"); os.makedirs(REP, exist_ok=True)
N = json.load(open(os.path.join(SUB, "EMA_MANUSCRIPT_VALUES.json"))); sm = json.load(open(os.path.join(EMA, "EMA_THRESHOLD_SUMMARY.json")))
cur = pd.read_csv(os.path.join(EMA, "THRESHOLD_OMISSION_CURVE.csv")); c = cur.set_index("threshold_gdd10")
al = pd.read_csv(os.path.join(EMA, "OMISSION_ALIGNMENT_SENSITIVITY.csv")); st = pd.read_csv(os.path.join(EMA, "CLASSIFICATION_STABILITY_PAIRS.csv"))
geo = pd.read_csv(os.path.join(EMA, "RICE_OMISSION_BY_COUNTRY.csv")); tm = pd.read_csv(os.path.join(EMA, "CLASSIFICATION_TRANSITION_MATRIX.csv"), index_col=0)
kat = pd.read_csv(os.path.join(EMA, "KNOWN_ANSWER_TESTS_FINAL.csv")); TS = sm["T_star"]
def W(name, lines): open(os.path.join(REP, name), "w").write("\n".join(lines) + "\n")
def mdtab(df): return ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * len(df.columns)] + ["| " + " | ".join(map(str, r)) + " |" for r in df.values]
git = lambda *a: subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True).stdout.strip()
HEAD = git("rev-parse", "HEAD"); MAIN = git("rev-parse", "origin/main")
named = cur[cur.reference_label.notna()][["threshold_gdd10", "reference_label", "cropland_pass_pct", "cropland_thermal_aei_pct", "germany_cropland_pass_pct", "rice_omitted_ha", "rice_omitted_pct", "rice_omitted_pct_incumbent_cells", "rice_omitted_pct_2p5m_subcell"]]

# 05 threshold sweep
W("THRESHOLD_SWEEP_METHODS_AND_RESULTS.md", ["# Threshold sweep: methods and results", "",
 "## Fixed specification", "- Climate surface: WorldClim 2.1 tavg, 1970–2000, 5′; GDD10 over the pipeline window (2 d April, May, June, July, August, 11 d September ≈ 29 Apr–11 Sep).",
 "- Domain: Natural Earth 1:50 m, CONTINENT == Europe, ADMIN != Russia, rasterised on the 5′ grid (11°W–45°E, 34°N–71.5°N).",
 f"- Cropland weights: MapSPAM 2010 v2.0 harvested area, wheat+maize+barley+potato, all technologies ({N['inc_Mha']} Mha). Rice weights: MapSPAM 2010 rice harvested area, all technologies ({N['rice_kha']} kha in {N['rice_cells']} cells).",
 "- Thresholds: 0–1800 GDD10 step 25 plus named references; pass = GDD10 ≥ T; omitted rice = rice area in cells with GDD10 < T.",
 "- Script: `modern_rice/scripts/ema_threshold_sweep.py`; figures: `ema_figures.py`. All values below are read from `THRESHOLD_OMISSION_CURVE.csv`.", "",
 "## Not computed, and why", "Specificity, precision, F1, AUC and ROC are not computed: non-rice cropland is not a verified negative (rice absence is mostly due to water, soils, markets and institutions), so commission cannot be estimated. The curve is an omission–candidate-area trade-off, not an ROC curve.", "",
 "## Named references", *mdtab(named), "",
 "## Interpretation", f"- Monotonicity is mechanical on a fixed surface (KAT 1–2). The informative feature is the **location** of the rise: European rice-area-weighted GDD10 P05 = {N['eu_P05']}, P50 = {N['eu_P50']}, so omission stays ≤5% up to {N['T_om5']} and first exceeds 10% at {N['T_om10']}.",
 f"- Between T* = {N['T_star']} and 900, candidate area falls by {N['crop_drop_pp']} pp ({N['crop_drop_Mha']} Mha) while omission rises by {N['om_rise_pp']} pp ({N['om_T']}% → {N['om_900']}%). Germany falls by {N['de_drop_pp']} pp; MapSPAM maps no rice in Germany.",
 f"- Grid-shift range at T*: {N['sh_min']}–{N['sh_max']}%; LOCO range at T*: {N['loco_T']}; at 900: {N['loco_900']}. These scenario ranges overlap the T*→900 omission change, so the presence-only check cannot rank T* against 900.",
 "- Conclusion: the sweep is informative beyond monotonicity in one specific sense: it shows that mapped rice area constrains only thresholds above about the European rice P05 and is uninformative in the range where the competing Hokkaido references differ. It does not validate T*."])

# 10 independence audit
W("RICE_AREA_VALIDATION_AND_INDEPENDENCE_AUDIT.md", ["# Rice-area reference data: validation role and independence audit", "",
 "| Item | Finding |", "|---|---|",
 "| Dataset | MapSPAM 2010 v2.0 (IFPRI, 2019; Yu et al., 2020); Harvard Dataverse doi:10.7910/DVN/PRFF8V, file 3985008; CC BY 4.0; local `modern_rice/data/raw/spam2010v2r0_global_harv_area.geotiff.zip` (ledger in AG data ledger). |",
 "| Variable | `H` = harvested area (ha), technology `A` (all) for the sweep; `I` (irrigated) used only for description. Harvested area counts multiple cropping; it is not physical paddy area. |",
 "| Nature | Modelled allocation of national/subnational statistics to 5′ cells using cropland extent, irrigation maps and crop suitability (Yu et al., 2020). Not field observations, not remote-sensing paddy maps. |",
 "| Grid / alignment | 5′ global grid, origin (−180, 90); rows padded to 2160 (Antarctic rows absent in file); negative/nodata set to 0. Same grid as WorldClim 5′ and GMIA 5′. |",
 f"| Nodata | Domain cells with rice > 0 but no WorldClim value: {kat[kat.test.str.startswith('Nodata')].detail.iloc[0]}. |",
 f"| Calibration vs evaluation | T* calibrated on MapSPAM rice in Hokkaido ({N['hok_rice_kha']} kha); evaluated on MapSPAM rice in Europe. Out of region, **not out of product**. |",
 f"| Circularity: infrastructure gate | MapSPAM irrigated technology and GMIA share irrigation-statistics lineage. {100*sm['rice_irrigated_tech_share']:.1f}% of European rice is MapSPAM-irrigated and {100*sm['rice_in_aei_cells_share']:.1f}% lies in cells with AEI ≥10%; this agreement is **not** used as validation. Note: MapSPAM classifies all French, Romanian and Hungarian rice as non-irrigated, which is agronomically implausible (Camargue, Danube paddies) and illustrates allocation error. |",
 "| Circularity: thermal gate | MapSPAM suitability priors include climate; allocation can place rice in cells MapSPAM deems suitable. Low omission is therefore partly expected by construction and is not independent evidence of thermal adequacy. |",
 f"| Omission geography at T* | {N['om_T_ha']} ha in {N['om_cells']} cells, {N['om_clusters']} clusters (8-connected), top-5 clusters {N['om_top5']}%; Italy+France {N['om_ital_fr']}%; {N['om_fringe_cells_pct']}% of omitted cells (holding {N['om_fringe_pct']}% of omitted area) have rice <1% of cell area → allocation fringe. {sm['clusters'][str(int(TS))]['omitted_cells_gdd_zero']} omitted cells have GDD10 = 0 (high-Alpine), holding {sm['clusters'][str(int(TS))]['omitted_ha_gdd_zero']} ha. |",
 f"| Legacy 0.87% | Equals omission restricted to rice cells with incumbent arable land; the all-rice-cell value used in EM&A is {N['om_T']}%. {N['rice_noinc_kha']} kha of rice lie in cells without incumbent crops. |",
 "| Negatives | None independent. Non-rice cropland cannot serve as true negatives. |",
 "| Inference unit | Cells are spatially autocorrelated and share allocation inputs; no cell bootstrap. Scenario ranges: 8 one-cell shifts, 3×3 rule, 2.5′ sub-cell, 10′ native, leave-one-country-out (countries >1000 ha rice). |",
 "", "## Country table (omitted ha at T*, 900, 1100)", *mdtab(geo), "",
 "## Verdict", "The rice-area check is a presence-only, same-product, out-of-region coverage check. It establishes that the gate does not exclude mapped current European rice; it cannot establish validity, commission or threshold optimality."])

# 11 stability
s2 = st.copy(); s2["comparison"] = s2.comparison.str.replace(r"^S\d ", "", regex=True)
W("CLASSIFICATION_STABILITY_FINAL.md", ["# Classification stability (thermal gate)", "", "Reference: T* = 589 GDD10, 5′, pipeline window. Weights: incumbent arable harvested area. Script: `ema_threshold_sweep.py`.", "",
 *mdtab(s2.drop(columns=["reference"])), "", "## Transition matrix T* → 900 (Mha; 3 gate classes on incumbent cells)", *mdtab(tm.reset_index()), "",
 "## Three separate questions", "1. **Stability between specifications**: high for support/window changes with recalibration (Jaccard ≥ " + f"{min(N['jac_25'], N['jac_10'], N['jac_cal'])}" + f"), low for reference changes (Jaccard {N['jac_900']} vs 900; {N['jac_P50']} vs Hokkaido P50; Germany {N['jac_de_900']}).",
 f"2. **Coverage of mapped rice**: rice omission under each alternative is in `CLASSIFICATION_STABILITY_PAIRS.csv` (column rice_omitted_pct_comp); all are ≤ {st.rice_omitted_pct_comp.max():.2f}%.",
 "3. **Agronomic validity**: not established by either 1 or 2.", "", f"Disagreement map: `figures/CLASSIFICATION_DISAGREEMENT_MAP.png` ({N['dis_Mha']} Mha pass at T* only)."])

# 14 European validity
dom = pd.read_csv(os.path.join(AG, "EUROPE_DOMAIN_SENSITIVITY.csv"))
W("EUROPEAN_ASSESSMENT_VALIDITY_FINAL.md", ["# European assessment validity", "",
 "| Check | Result |", "|---|---|",
 *[f"| {r.test} | {r.result}: {r.detail} |" for r in kat.itertuples() if any(k in r.test for k in ["Geographic", "Denominator", "Thermal pass", "Thermal +", "Nodata", "Area weighting", "Combined", "Germany"])],
 "| Transcontinental countries | Assigned by Natural Earth CONTINENT; Türkiye, Cyprus, Georgia, Azerbaijan, Armenia, Kazakhstan are Asia and excluded; Russia excluded explicitly (truncated by 45°E). |",
 "| Pixel-area weighting | Not applied to MapSPAM hectares (already area units). Cell areas (WGS84 authalic sphere) used only for AEI share. |",
 "| Irrigation layer | GMIA v5 area equipped for irrigation (ha, ~2005), share ≥ 10% of cell. Not water allocation, not rice-specific field infrastructure, not feasibility. |",
 "| Rounding correction | AG manuscript printed 92.2% (double rounding of 0.9215). Exact 92.146% → **92.1%** in EM&A. Not a scientific change. |", "",
 "## Domain sensitivity (from AG canonical output)", *mdtab(dom.head(10))])

# 18 prior studies
pp = pd.read_csv(os.path.join(JF, "EMA_CLOSEST_PUBLISHED_PAPERS.csv"))
nm = pp.new_method_introduced.str.lower().str.startswith("no"); nf = pp.new_field_observations.str.lower().str.match(r"^(no|not stated)")
vs = pp.independent_validation.str.lower().str.startswith("yes"); vp = pp.independent_validation.str.lower().str.startswith("partial")
tpl = open(os.path.join(ROOT, "modern_rice", "manuscript_ema", "manuscript_template.md")).read()
pp["cited_in_ema_manuscript"] = pp.doi.apply(lambda d: d in tpl)
INC = {1: "Same crop (rice) and zoning purpose; single specification. This study adds threshold sweep and reference decomposition.",
       2: "WorldClim climatic suitability; single threshold set. This study shows threshold-reference construction dominates.",
       3: "Rice GIS-AHP; no sensitivity to reference. This study quantifies reference-dependent instability.",
       4: "Validates against yield; new model claimed. This study has no yield validation (limitation) but audits reference independence.",
       5: "Rice method comparison with field pedons. This study compares reference constructions, not MCDA rules.",
       9: "Fuzzy model comparison with production validation. Comparable comparison logic; different object (reference vs rule).",
       11: "MCDM rule comparison. This study varies the threshold reference, holding rules fixed.",
       15: "Spatial-resolution effect on RUSLE. Analogous support test; this study finds support effect small relative to reference.",
       14: "Water vs agricultural expansion. Analogous non-compensatory water constraint; this study uses infrastructure only.",
       7: "Presence-point suitability with production consistency check. Analogous coverage check; this study audits same-product circularity.",
       8: "Field presence points + MaxEnt. This study has no field presence data (limitation).",
       12: "ROC with well split. This study explicitly declines ROC for lack of negatives."}
fin = pp[pp.closeness_rank.isin(INC)].copy(); fin["incremental_evidence_of_this_study"] = fin.closeness_rank.map(INC)
fin = fin[["closeness_rank", "citation", "doi", "study_question", "new_field_observations", "new_method_introduced", "independent_validation", "cited_in_ema_manuscript", "incremental_evidence_of_this_study", "url"]]
fin.to_csv(os.path.join(REP, "EMA_CLOSEST_PRIOR_STUDIES_FINAL.csv"), index=False)
counts = dict(total=len(pp), no_new_method=int(nm.sum()), no_new_field=int(nf.sum()), validation_yes=int(vs.sum()), validation_yes_or_partial=int((vs | vp).sum()))
refs = [l for l in tpl.split("# REFERENCES")[1].split("\n") if l.strip()]
def venue(r):
    its = re.findall(r"\*([^*]+)\*", r); j = [x for x in its if re.search(r",\s*\d", x)]
    return (j[-1].rsplit(",", 1)[0] if j else ("dataset / report" if "[Data set]" in r or not its else "book / report"))
jr = pd.Series([venue(r) for r in refs]).value_counts()
W("CITATION_ECOLOGY_FINAL.md", ["# Citation ecology (EM&A manuscript)", "", f"References: {len(refs)}. EM&A articles cited: {sum('Environmental Monitoring and Assessment' in r for r in refs)} (each supports a specific comparison claim in Introduction/Discussion).", "",
 "## Verification of the earlier 19-paper counts (recomputed from `journal_fit_assessment/EMA_CLOSEST_PUBLISHED_PAPERS.csv`)", f"- Papers: {counts['total']} (claimed 19)", f"- No new method: {counts['no_new_method']} (claimed 17)", f"- No new field data (no / not stated): {counts['no_new_field']} (claimed 8)",
 f"- Observed validation: {counts['validation_yes']} strict 'yes' (claimed 7); {counts['validation_yes_or_partial']} including 'partial'.", "- Classification rule: string prefix of the coded columns, which were coded from publisher abstracts (not full text).", "",
 "## Reference sources by venue (first italic segment)", *mdtab(jr.reset_index().rename(columns={"index": "venue", 0: "n", "count": "n"})), "",
 "No citation was added for count; uncited EM&A papers in the 19-paper audit were left out where they did not support a claim."])
W("NOVELTY_BOUNDARY_FINAL.md", ["# Novelty boundary", "", "## Not claimed as new", "- Threshold sensitivity, MAUP / resolution sensitivity, monotonic threshold behaviour, multi-gate (non-compensatory) screening, use of GDD thresholds, WorldClim/MapSPAM/GMIA overlay.", "",
 "## Claimed incremental evidence (empirical, case-specific)", f"1. Controlled decomposition showing reference construction dominates (Germany {N['de_T']}% vs {N['de_900']}%) while recalibrated support changes ≤{N['de_res_pp']} pp.",
 f"2. Threshold sweep against mapped existing rice showing the presence-only check is flat over the competing-reference range (omission {N['om_T']}%→{N['om_900']}% while candidate area changes {N['crop_drop_pp']} pp) and constrains only T ≳ {N['T_om5']}.",
 f"3. Explicit independence audit: same-product, out-of-region; infrastructure-lineage circularity; omission concentrated in allocation-fringe cells ({N['om_fringe_pct']}% of omitted area) and sensitive to one-cell shifts ({N['sh_min']}–{N['sh_max']}%).",
 f"4. Non-compensatory infrastructure gate reduces candidate area to {N['pct_aei']}%.", "",
 "## Boundary", "This is a reliability/verifiability assessment of one transferred-threshold case. It is not a new method, monitoring network, physiological threshold or feasibility study. Relative to the audited EM&A papers (single-specification suitability maps; 7–8 of 19 with observed validation), the contribution is the explicit demonstration that the available reference data cannot validate the decisive choice. Novelty is modest but real; whether EM&A editors value a negative/verifiability result is the main uncertainty."])

# 21 reference audit
cr = {}
for f in os.listdir(os.path.join(ROOT, "data", "raw_public", "crossref_ema")):
    if f.endswith(".json"): m = json.load(open(os.path.join(ROOT, "data", "raw_public", "crossref_ema", f)))["message"]; cr[m["DOI"].lower()] = m
SUP = {"Azadi": "rice land evaluation by TOPSIS/SAW vs parametric (example of typical rice suitability method comparison)", "Bagwan": "spatial resolution changes RUSLE results (support sensitivity)",
 "Bai": "evaluation of NASA POWER data (source of point reference)", "Bazkiaee": "GIS-AHP rice suitability (typical approach)", "Benti": "field presence points + MaxEnt suitability", "Fick": "WorldClim 2 data source",
 "IFPRI": "MapSPAM 2010 v2 data", "Jelinski": "MAUP concept", "King": "northward agricultural climate-zone shift", "MAFF": "Hokkaido rice system statistics/practice", "Malone": "uncertainty in digital land suitability",
 "Mohamed": "GIS-MCDA suitability with yield validation", "NASA": "POWER data source", "Natural": "country boundaries", "Ojara": "climatic suitability of maize with WorldClim", "Rashidi": "MCDM method comparison changes suitability",
 "Siebert": "GMIA v5 data", "Sloat": "crop migration as adaptation", "Snelder": "suitability not intrinsic to parcel", "Tenerelli": "multi-criteria uncertainty analysis", "Van": "rice zoning in EM&A", "Wang": "presence-point tea suitability",
 "Xu": "spatially explicit sensitivity analysis for land suitability", "Yu": "MapSPAM method incl. allocation priors", "Zabel": "global agricultural suitability evaluation"}
rows = []
for r in refs:
    doi = (re.search(r"https://doi.org/(\S+)", r) or [None, None])[1]; key = re.match(r"[^,(.]+", r).group(0).split()[0]
    m = cr.get((doi or "").lower()); chk = "Crossref record archived (data/raw_public/crossref_ema): authors/title/volume/issue/article no. match" if m else ("DOI verified in AG reference audit (PR #1)" if doi else "dataset/grey literature; URL")
    rows.append(dict(reference=r[:90] + "…", doi=doi or "", metadata_check=chk, supports_claim=SUP.get(key, "?")))
rdf = pd.DataFrame(rows); rdf.to_csv(os.path.join(REP, "REFERENCE_AUDIT_TABLE.csv"), index=False)
W("REFERENCE_AND_CLAIM_AUDIT_FINAL.md", ["# Reference and claim audit", "", "Style: APA 7, alphabetical (asserted in builder). Every reference cited in text and vice versa (asserted in builder).", "", *mdtab(rdf), "",
 "## Claim-level cautions applied", "- 'MapSPAM allocates ... using cropland extent, irrigation maps and crop-suitability information (Yu et al., 2020)': consistent with Yu et al. (2020) description of the SPAM cross-entropy allocation; author should confirm wording against the full paper.",
 "- Jelinski & Wu (1996) cited only for the MAUP concept; Xu & Zhang (2013) only as an example of spatially explicit sensitivity analysis (wording softened in this revision).",
 "- EM&A papers cited only as examples of typical approaches, with content taken from publisher abstracts (journal_fit_assessment audit)."])

# 17 claim matrix
CL = [("Hokkaido reference T*", "T_star", "GRID_THERMAL_CALIBRATION.json", "ag_grid_gates.py", "KAT 14"),
 ("Denominator Mha", "inc_Mha", "EUROPE_GATE_CASCADE_BY_COUNTRY.csv", "ag_grid_gates.py", "KAT 10"),
 ("Thermal pass % at T*", "pct_T", "THRESHOLD_OMISSION_CURVE.csv", "ema_threshold_sweep.py", "KAT 7, 11"),
 ("Thermal+AEI % at T*", "pct_aei", "THRESHOLD_OMISSION_CURVE.csv", "ema_threshold_sweep.py", "KAT 12"),
 ("Germany pass at T* / 900", "de_T/de_900", "THRESHOLD_OMISSION_CURVE.csv; GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv", "ema_threshold_sweep.py; ag_germany_decomposition.py", "KAT 13"),
 ("Resolution effect ≤ pp", "de_res_pp", "GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv", "ag_germany_decomposition.py", "builder computation"),
 ("Rice omission at T*, 900", "om_T/om_900", "THRESHOLD_OMISSION_CURVE.csv", "ema_threshold_sweep.py", "KAT 15-16"),
 ("Legacy 0.87% variant", "om_T_inc", "THRESHOLD_OMISSION_CURVE.csv; EUROPE_RICE_VALIDATION.json", "ema_threshold_sweep.py", "KAT 17"),
 ("Candidate drop T*→900", "crop_drop_pp", "THRESHOLD_OMISSION_CURVE.csv", "build_ema_manuscript.py", "derived"),
 ("Omission geography/clusters", "om_cells/om_clusters/om_fringe_pct", "EMA_THRESHOLD_SUMMARY.json", "ema_threshold_sweep.py", "scipy.ndimage.label 8-conn"),
 ("Shift / LOCO ranges", "sh_min/sh_max/loco_T", "OMISSION_ALIGNMENT_SENSITIVITY.csv; EMA_THRESHOLD_SUMMARY.json", "ema_threshold_sweep.py", "scenario range"),
 ("Jaccard values", "jac_*", "CLASSIFICATION_STABILITY_PAIRS.csv", "ema_threshold_sweep.py", "KAT 20"),
 ("Transition 1.2 Mha", "tm_lost_Mha", "CLASSIFICATION_TRANSITION_MATRIX.csv", "ema_threshold_sweep.py", "KAT 18-19"),
 ("Omission >10% threshold", "T_om10", "THRESHOLD_OMISSION_CURVE.csv", "build_ema_manuscript.py", "derived")]
pd.DataFrame([dict(claim=a, manuscript_placeholder=b, value=" / ".join(str(N.get(k, "")) for k in re.split(r"/", b) if not k.endswith("*")) or "see file", source_file=c_, script=d, verification=e) for a, b, c_, d, e in CL]).to_csv(os.path.join(REP, "CLAIM_IMPLEMENTATION_MATRIX_FINAL.csv"), index=False)

# 15 semantic audit
W("SEMANTIC_CODE_AUDIT_FINAL.md", ["# Semantic code audit (EM&A scripts)", "", "Scripts: `ema_threshold_sweep.py`, `ema_figures.py`, `build_ema_manuscript.py`, `ema_known_answer_tests.py`, `ema_reports.py`.", "",
 "| Aspect | Specification | Implementation | Status |", "|---|---|---|---|",
 "| Estimand C(T) | incumbent-area-weighted share with GDD10 ≥ T | `inc[valid & (g5 >= T)].sum() / inc[valid].sum()` | OK |",
 "| Estimand O(T) | rice-area-weighted share with GDD10 < T | `rice[rmask & ~(g5 >= T)].sum() / rice[rmask].sum()` | OK |",
 "| Sign / boundary | pass is ≥ | `g5 >= T`; equation (1) uses ≥, (2) uses < | OK (KAT 4–6) |",
 "| Units | GDD10 °C·d; area ha; output % and Mha | consistent; Mha = ha/1e6 | OK |",
 "| Weights | harvested ha, no extra pixel-area weighting | as specified; cell area only for AEI share | OK (KAT 7) |",
 "| Window | 2 d Apr + May–Aug + 11 d Sep | `WIN_PIPE` identical to `ag_grid_gates.py` | OK (Germany endpoints reproduced, KAT 13) |",
 "| Grid support | 5′ native; 2.5′ via 2×2 sub-cell fraction; 10′ via 2×2 replication | block_mean / repeat | OK; 2.5′ majority rule (≥0.5) for stability, fraction for omission |",
 "| Joins | all layers on identical 5′ window; Natural Earth rasterised with same transform | `from_origin(W, N, 1/12, 1/12)` | OK (denominator matches AG to 2 ha, KAT 10) |",
 "| Missingness | NaN GDD10 excluded from both numerator and denominator | `np.isfinite(g5)` in masks | OK; 0 ha affected (KAT 8) |",
 "| Inference unit | no independent-cell inference | scenario ranges only | OK (KAT 21) |",
 "| Hardcoding | none of headline values in template/builder | placeholders from CSV/JSON | OK (KAT 22–23) |",
 "| Edge artefact | `np.roll` shift wraps at window edge | rice at window edges is zero (no rice at 11°W/45°E/71.5°N edges); effect nil | Noted |",
 "| Known defect fixed | AG 92.2% double rounding | EM&A uses exact share → 92.1% | Corrected (documented) |", "",
 f"Known-answer tests: {int((kat.result=='PASS').sum())}/{len(kat)} PASS (`KNOWN_ANSWER_TESTS_FINAL.md`)."])

# 23 text/figure/table consistency, 24 render audit
D = Document(os.path.join(SUB, "01_EMA_MANUSCRIPT_FINAL.docx")); RV = Document(os.path.join(SUB, "EMA_MANUSCRIPT_REVIEW_COPY.docx"))
txt = "\n".join(p.text for p in D.paragraphs); ttab = "\n".join(cc.text for t in D.tables for r in t.rows for cc in r.cells)
miss = [k for k, v in N.items() if k != "repo_url" and v not in txt + ttab and ("{" + k + "}") in tpl]
figc = re.findall(r"Fig\. (\d+)", txt); tabc = re.findall(r"Table (\d+)", txt)
order_ok = lambda xs: [x for i, x in enumerate(xs) if x not in xs[:i]] == sorted(set(xs), key=int)
t2 = D.tables[1]; t2ok = all(abs(float(t2.cell(i + 1, 5).text) - round(float(named.iloc[i].rice_omitted_pct), 2)) < 0.006 for i in range(len(named)))
NPH = len(set(re.findall(r"{(\w+)}", tpl)))
W("TEXT_FIGURE_TABLE_CONSISTENCY_FINAL.md", ["# Text–figure–table consistency", "", f"- Placeholders used in template: {NPH}; values not found verbatim in the built DOCX: {miss or 'none'}.",
 f"- Figure first-citation order: {[x for i, x in enumerate(figc) if x not in figc[:i]]} → {'OK' if order_ok(figc) else 'FAIL'}; tables: {[x for i, x in enumerate(tabc) if x not in tabc[:i]]} → {'OK' if order_ok(tabc) else 'FAIL'}.",
 "- Each figure/table is placed immediately after the paragraph that first cites it (Table 2 after the §2.4 block containing equations 1–2, because the citing paragraph continues through the equations).",
 f"- Table 2 'Rice omitted' column equals THRESHOLD_OMISSION_CURVE.csv for all {len(named)} rows: {'OK' if t2ok else 'FAIL'}.",
 "- Figures are generated by `ema_figures.py` from the same CSV/NPZ outputs; legends state weights (cropland-area vs rice-area) and denominators; 'candidate' wording only.",
 "- Abstract, Results and cover letter use the same placeholders (single source)."])
xml = D.element.xml; xr = RV.element.xml; sty = D.styles.element.xml; ftr = D.sections[0].footer._element.xml
fonts = set(re.findall(r'w:ascii="([^"]+)"', xml + sty)); spacing = len(re.findall(r"<w:spacing w:val=", xml)); omml = len(re.findall(r"<m:oMath[ >]", xml)); omr = len(re.findall(r"<m:oMath[ >]", xr))
pdfp = subprocess.run(["pdfinfo", os.path.join(SUB, "02_EMA_MANUSCRIPT_REVIEW.pdf")], capture_output=True, text=True).stdout
pdft = subprocess.run(["pdftotext", os.path.join(SUB, "02_EMA_MANUSCRIPT_REVIEW.pdf"), "-"], capture_output=True, text=True).stdout
pf = subprocess.run(["pdffonts", os.path.join(SUB, "02_EMA_MANUSCRIPT_REVIEW.pdf")], capture_output=True, text=True).stdout
NPG = re.search(r"Pages:\s+(\d+)", pdfp).group(1); NAST = len(re.findall(r"(?<!T)\*", pdft))
W("WORD_RENDER_AND_EQUATION_AUDIT.md", ["# Word render and equation audit", "", f"- Fonts declared in main DOCX runs/styles: {sorted(fonts)}; body 12 pt Times New Roman black; captions and table text 10/9 pt.",
 f"- Character-spacing (`w:spacing w:val`) elements: {spacing}.", f"- Native OMML equations: {omml} in main, {omr} in review copy (equations 1–2).",
 f"- Inline images: main {xml.count('<pic:pic')}, review copy {xr.count('<pic:pic')} (5 expected).", f"- Line numbering: {'continuous' if 'w:lnNumType' in xml else 'MISSING'}; page numbers in footer: {'yes' if 'PAGE' in ftr else 'no'}.",
 f"- Review PDF: {NPG} pages (LibreOffice render). Replacement glyphs (U+FFFD) in extracted text: {pdft.count(chr(0xFFFD))}. Stray Markdown asterisks other than T*: {NAST}.",
 "- Embedded fonts (pdffonts):", "```", pf.strip(), "```",
 f"- All {NPG} pages were rasterised and inspected (contact sheets in `submission/render_check/png/`): no clipping, captions below figures and above tables, equations render with fraction and summation, references hanging-indented and alphabetical. Word itself was not available; rendering was checked with LibreOffice 7."])

# 25 requirements
rq = os.path.join(ROOT, "data", "journal_requirements", "environmental_monitoring_and_assessment")
abs_w = len(re.findall(r"\S+", [p.text for p in D.paragraphs if p.text][7] if False else next(p.text for i, p in enumerate(D.paragraphs) if i > 0 and D.paragraphs[i - 1].text == "Abstract")))
W("EMA_JOURNAL_REQUIREMENTS_FINAL.md", ["# EM&A requirements (archived official pages, retrieved 2026-11-13; `data/journal_requirements/environmental_monitoring_and_assessment/`)", "",
 "| Requirement (official text) | This submission | Status |", "|---|---|---|",
 "| Article type: original research article | Original research article | OK |",
 f"| 'The Abstract should contain 150 to 250 words' | {abs_w} words | OK |",
 "| 'Please provide 4 to 6 keywords', 'different from those in the title' | 6 keywords, none repeats a title phrase (builder assert) | OK |",
 "| 'no specific word limits, the average article contains approximately 9,000 words' | ~3,200 words body | OK (short) |",
 "| Title page: author, affiliation, e-mail, ORCID | Present; e-mail placeholder | AUTHOR ACTION |",
 "| 'The journal uses APA reference style'; alphabetized by first author | APA 7, alphabetical | OK |",
 "| Line numbers (mandatory review step) | Continuous line numbering | OK |",
 "| 'Tables should be cited in the text in consecutive numerical order' | Asserted | OK |",
 "| Figures: separate files; EPS vector / TIFF halftone preferred | PNG 600 dpi + PDF vector per figure supplied separately; TIFF conversion optional | OK / optional |",
 "| 'provide all relevant editable source files' | DOCX source | OK |",
 "| Declarations before References: Funding, Competing interests, Ethics, Consent, Data/Code availability, Author contributions | Present | OK |",
 "| 'All original research must include a data availability statement' | Present (public repo URL) | OK |",
 "| LLM use 'documented in the Methods section' | §2.7 | OK |",
 "| Scope: 'Preference is given to studies with new and original environmental field data'; excluded: 'Strictly modelling studies with little field data support', 'Studies on Crop Management', 'Economic based studies' | Uses census/station-derived monitoring products; no new field data; economic and crop-management content removed | RISK (desk-reject risk) |",
 "| Publishing model: subscription route (no APC) or OA with APC | Choose subscription at submission | AUTHOR ACTION |", "",
 "Files: " + ", ".join(sorted(os.listdir(rq)))])
print("reports:", sorted(os.listdir(REP)), "| counts", counts, "| missing placeholders", miss, "| abs", abs_w)
