#!/usr/bin/env python3
"""RPG feasibility, provenance, crop-code, independence, semantic-audit and post-RPG fit reports, from saved raw files and RPG outputs only."""
import os, json, hashlib, collections, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
RAW = os.path.join(ROOT, "modern_rice", "data", "raw", "rpg"); OUT = os.path.join(ROOT, "outputs", "modern_rice", "ema", "rpg")
N = json.load(open(os.path.join(ROOT, "outputs", "modern_rice", "ema", "submission", "EMA_MANUSCRIPT_VALUES.json")))
V = pd.read_csv(os.path.join(OUT, "RPG_RICE_PARCEL_VALIDATION.csv")).set_index("source"); K = pd.read_csv(os.path.join(OUT, "RPG_KNOWN_ANSWER_TESTS.csv"))
def md(df): return "\n".join(["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * len(df.columns)] + ["| " + " | ".join(map(str, r)) + " |" for r in df.values])
def W(n, L): open(os.path.join(OUT, n), "w").write("\n".join(L) + "\n")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
LIC = "Licence Ouverte / Open Licence 2.0 (etalab-2.0), stated on the official IGN dataset page"
REDIS = "Licence permits reuse and redistribution with attribution; raw geometries nevertheless kept out of the public repository (gitignored); only derived cell-level tables are published"
rows = []
for l in open(os.path.join(RAW, "LEDGER.txt")):
    f = l.split()
    if len(f) < 5: continue
    fn, t, size, h, url = f[0], f[1], int(f[2]), f[3], " ".join(f[4:]); p = os.path.join(RAW, fn); ok = os.path.exists(p) and sha(p) == h and os.path.getsize(p) == size; url = url.split(" [")[0]
    yr = next((y for y in ("2010", "2015", "2020", "2024") if f"rpg{y}" in fn), "")
    kind = "rice features (WFS GetFeature)" if fn.endswith(".geojson") else "crop codebook" if "codes" in fn else "WFS capabilities" if "capabilities" in fn else "schema/feature probe" if "probe" in fn else "official dataset page" if fn.endswith(".html") else "data.gouv.fr catalogue search" + (" (empty result)" if size < 200 else "")
    filt = "code_cultu='14' (îlot layer, group 14 = RIZ)" if yr == "2010" and fn.endswith(".geojson") else "code_cultu='RIZ'" if fn.endswith(".geojson") else ""
    layer = ("RPG.2010:rpg_2010" if yr == "2010" else f"RPG.{yr}:parcelles_graphiques") if fn.endswith(".geojson") or "probe" in fn else ""
    geom = ""
    if fn.endswith(".geojson"):
        d = json.load(open(p)); geom = "/".join(sorted(collections.Counter(x["geometry"]["type"] for x in d["features"]))); nf = len(d["features"]); nm = d.get("numberMatched")
    rows.append(dict(file=fn, kind=kind, dataset="IGN Registre parcellaire graphique" if yr or "codes" in fn or "capabilities" in fn else "", layer=layer, year=yr, retrieved_utc=t, bytes=size, sha256=h, sha256_verified=ok,
        crs="EPSG:4326 (requested SRSNAME); areas computed in EPSG:2154" if fn.endswith(".geojson") else "", filter=filt, geometry=geom,
        features=nf if fn.endswith(".geojson") else "", number_matched=nm if fn.endswith(".geojson") else "", complete_retrieval=(nf == nm and nf < 5000) if fn.endswith(".geojson") else "",
        coverage="France incl. overseas; analysis restricted to metropolitan France" if fn.endswith(".geojson") else "", licence=LIC if yr or "codes" in fn else "", redistribution=REDIS if fn.endswith(".geojson") else "",
        local_path=os.path.relpath(p, ROOT), url=url))
pv = pd.DataFrame(rows); last = pv.groupby("file").cumcount(ascending=False) == 0
pv["ledger_status"] = ["current" if l else "superseded (file re-saved later; earlier snapshot not retained)" for l in last]
pv.to_csv(os.path.join(OUT, "RPG_DATA_PROVENANCE.csv"), index=False); assert pv[last].sha256_verified.all() and (pv[~last].kind == "official dataset page").all(); pv = pv[last]
cb = pd.read_csv(os.path.join(RAW, "rpg_latest_codes_cultures.csv")); g14 = cb[cb.code_groupe_culture.astype(str) == "14"]
riz = cb[cb.libelle_culture.str.lower().str.contains("riz")]
cnt = {}
for y in ("2010", "2015", "2020", "2024"):
    fn = [r.file for r in pv.itertuples() if r.year == y and r.file.endswith(".geojson")][0]; d = json.load(open(os.path.join(RAW, fn)))
    cnt[y] = {k: dict(collections.Counter(str(x["properties"].get(k)) for x in d["features"])) for k in ("code_cultu", "code_group", "nom_cultu") if k in d["features"][0]["properties"]}
    sec = collections.Counter(str(x["properties"].get("culture_d1")) for x in d["features"] if x["properties"].get("culture_d1")); cnt[y]["culture_d1 (secondary/catch crop, non-empty)"] = dict(sec)
W("RPG_CROP_CODE_VERIFICATION.md", ["# RPG crop-code verification", "", f"Source: official codebook layer `RPG.LATEST:codes_cultures` ({len(cb)} codes), saved as `rpg_latest_codes_cultures.csv`.", "",
 "## Codes in crop group 14", "", md(g14), "", "## Codes whose label contains 'riz'", "", md(riz), "",
 f"Group 14 contains exactly {len(g14)} crop code, so `RIZ` is rice-specific and is not a broad group (verdict: **RICE-SPECIFIC**). The 2010 îlot layer uses the older numeric group code `14`, whose label in the retrieved features is `RIZ`; in 2010 a feature is an agricultural block (îlot) and `surf_cultu` gives the area of the rice group within it, which the analysis uses as the area weight.", "",
 "## Values in the retrieved features", "", *[f"- {y}: {json.dumps(v, ensure_ascii=False)}" for y, v in cnt.items()], "",
 "The main-crop code is RIZ (or 14 in 2010) for every retrieved feature. A few 2020/2024 parcels also report a secondary (catch) crop in `culture_d1`; the main crop remains rice and these parcels are retained. Rice is irrigated paddy rice in the Camargue context, but the code does not distinguish cultivars or water management; no claim depends on that distinction."])
yrs = ["RPG 2010", "RPG 2015", "RPG 2020", "RPG 2024"]
FEAS = [("1 Public RPG years", "PASS", "WFS layers RPG.2010 … RPG.2024 listed in Géoplateforme capabilities; 2010, 2015, 2020, 2024 retrieved"),
 ("2 Rice crop code", "PASS", "RIZ (label Riz), group 14; 2010 group code 14 = RIZ"), ("3 Rice-specific vs broad", "PASS", f"group 14 has {len(g14)} code; see RPG_CROP_CODE_VERIFICATION.md"),
 ("4 Parcel geometry", "PASS", "MultiPolygon for every feature; 2010 is îlot (block) geometry, 2015–2024 parcel geometry"),
 ("5 Area", "PASS", "surf_parc (2015–2024) and surf_cultu (2010); geodesic area recomputed in EPSG:2154 agrees with declared totals within 0.1%"),
 ("6 Camargue coverage", "PASS", f"≥{N['rpg_camargue']}% of area south of 43.8°N and east of 4.2°E (coordinate box, not an official Camargue boundary)"),
 ("7 Overlap with climate period", "LIMITATION", "WorldClim normals 1970–2000 do not overlap RPG years (2010–2024); RPG 2010 matches the MapSPAM reference year. Warming since 2000 implies present GDD10 is probably higher, which can only reduce omission"),
 ("8 Independence from MapSPAM", "PARTIAL", "geometry and spatial allocation independent; national/subnational area totals may share the same declarations upstream (not verified)"),
 ("9 Built with climatic suitability model?", "PASS (no)", "administrative CAP declarations with anonymised parcel geometry; no climatic or suitability layer is used in construction (official dataset description)"),
 ("10 Licence for analysis and derived statistics", "PASS", LIC), ("11 Redistribution of geometries", "PASS (not exercised)", REDIS),
 ("12 Spatial resolution adequacy", "PASS with caveat", f"parcels ≪ 5′ cell; support is {N['rpg_cells_lo']}–{N['rpg_cells_hi']} distinct cells, so the effective climatic sample is small")]
W("RPG_DATA_FEASIBILITY_AND_INDEPENDENCE.md", ["# RPG data feasibility and independence", "", "**Verdict: RPG VALIDATION FEASIBLE** — usable as an independent check of observed-land-use coverage in France; not usable to estimate specificity, commission or true suitability accuracy, and its climatic range is too narrow to discriminate between competing thresholds.", "",
 "| Check | Status | Evidence |", "|---|---|---|", *[f"| {a} | {b} | {c} |" for a, b, c in FEAS], "",
 "Acquisition was limited to rice-coded features (four requests, one page each; `numberMatched` equals features returned, so no pagination truncation). Raw files are stored in `modern_rice/data/raw/rpg/` (gitignored) with `LEDGER.txt`; see `RPG_DATA_PROVENANCE.csv`. Seven data.gouv.fr catalogue searches returned empty responses (94 bytes) and were not used."])
W("RPG_INDEPENDENCE_AND_EXTERNAL_VALIDITY_AUDIT.md", ["# RPG independence and external-validity audit", "",
 "| Dependency | Assessment |", "|---|---|",
 "| MapSPAM crop allocation | Independent in spatial allocation: RPG geometry is declared by farmers and digitised on orthophotos; MapSPAM allocates statistics with cropland, irrigation and suitability priors. Totals may share upstream statistics (agricultural statistics in France draw on CAP declarations); not verified, so independence of totals is not claimed. |",
 "| WorldClim thermal surface | Independent: RPG contains no climate information. |",
 "| Hokkaido reference construction | Independent: T* was calibrated on MapSPAM rice in Japan; RPG was not used in calibration and was retrieved after T* was fixed. |",
 "| Model classification outputs | Independent: RPG was not used to choose thresholds, windows or grids. |", "",
 "## What RPG is not", "- Not ground truth of suitability: a declaration records that rice was grown, not that the climate is sufficient without management (flooding, cultivar choice).",
 "- Not error-free: declaration, crop-coding and digitising errors are possible; CAP controls reduce but do not remove them.", "- Presence only: absence of a rice declaration is not evidence of unsuitability, so commission, specificity, precision, F1 and AUC are not computed.", "",
 "## External validity", f"- Effective sample: {N['rpg_cells_lo']}–{N['rpg_cells_hi']} distinct 5′ cells per year, nearly all in and around the Rhône delta; parcel counts ({N['rpg_np_lo']}–{N['rpg_np_hi']}) are not independent climate observations and no parcel-level bootstrap is reported.",
 f"- Climatic range: area-weighted 5th percentile ≥{N['rpg_p05']} GDD10; every occupied cell exceeds {N['rpg_min_cell']} GDD10. The check is therefore uninformative for thresholds below ~{N['rpg_T1pct']} GDD10 and cannot rank T* against 900 GDD10.",
 "- Geography: one country, one delta; not representative of the cool Italian and Ukrainian margins where MapSPAM omissions occur.", "- Time: RPG 2010–2024 vs 1970–2000 normals (see feasibility check 7).", "",
 "## Interpretation category (prompt)", "Strong coverage agreement at all tested thresholds; **insufficient independent climatic variation / low discrimination**; material disagreement with MapSPAM France that is explained by MapSPAM allocation outside the declared district (MapSPAM omission is 0% inside RPG cells), not by a contradiction of the gate."])
SEM = [("Rice records", "only code_cultu RIZ (2015–2024) / 14 (2010) features retrieved by server-side filter", "rpg_fetch_rice.py CQL_FILTER; crop-code report"),
 ("Domain", "metropolitan France; overseas excluded by representative-point bounding box (-5…10°E, 41…51.5°N)", "rpg_validation.load"),
 ("Area", "geodesic area in EPSG:2154; 2010 weight = surf_cultu (rice-group area within îlot) distributed in proportion to îlot geometry", "load / overlay"),
 ("Cell assignment", "polygon ∩ 5′ cell overlay; centroid assignment as sensitivity", "overlay, cell_of; KAT 1–4, 9"),
 ("Climate surface", "same canonical ema_layers_5m.npz g5 (WorldClim 2.1, 29 Apr–11 Sep) as the manuscript", "load of EMA npz"),
 ("Estimand", "area-weighted share of declared rice area in cells with GDD10 < T (strict); nodata excluded from denominator (0 ha in practice)", "omit; KAT 3, 6, 10"),
 ("Effective support", "distinct (row, col) cells", "climate_cells; KAT 4"),
 ("MapSPAM comparison", f"France = modal country id among RPG 2020 cells (id {json.load(open(os.path.join(OUT, 'RPG_SUMMARY.json')))['spam_france']['france_cid']}); verified: MapSPAM rice under this id equals canonical RICE_OMISSION_BY_COUNTRY France total (builder assertion)", "build_ema_manuscript.py assertion; KAT 11–12"),
 ("Camargue share", "coordinate box lon ≥ 4.2°E, lat ≤ 43.8°N, labelled as approximate", "share_area_… column"),
 ("Uncertainty", "no parcel bootstrap; year-to-year range and centroid sensitivity reported instead", "manuscript §2.6")]
W("RPG_SEMANTIC_CODE_AUDIT.md", ["# RPG semantic code audit", "", "| Concept | Implementation | Where / test |", "|---|---|---|", *[f"| {a} | {b} | {c} |" for a, b, c in SEM], "",
 f"Known-answer tests: {(K.result == 'PASS').sum()}/{len(K)} PASS (`RPG_KNOWN_ANSWER_TESTS.md`). Issue found and fixed during audit: a zero-area test parcel exposed that the area filter was inline in `load`; it was factored into `clean_area` and tested directly."])
W("POST_RPG_NOVELTY_AND_JOURNAL_FIT_AUDIT.md", ["# Post-RPG novelty and EM&A fit", "",
 "## What RPG adds", f"- Converts the previously stated limitation 'no independent observation' into a tested statement for France: declared rice ({N['rpg_kha_lo']}–{N['rpg_kha_hi']} kha) is never omitted at T* and at most {N['rpg_om_max']}% at 900/1100 GDD10.",
 f"- Shows that MapSPAM's French omission ({N['spam_fr_om_T']}% at T*) arises from allocation outside the declared district ({N['spam_in_rpg_pct']}% of MapSPAM French rice lies in RPG cells), supporting the manuscript's existing low-density-margin interpretation with independent evidence.",
 "- Reinforces, rather than overturns, the central claim: independent presence data are also unable to rank references because they occupy only warm cells.", "",
 "## What RPG does not add", "- No discrimination between T* and 900 GDD10; no specificity; one delta only; no new author-collected field data.", "",
 "## Effect on desk-rejection risk 1 (field-data preference)", "Reduced from HIGH to MEDIUM–HIGH: the paper now includes an independent, field-declared parcel dataset, but it is administrative open data rather than author-collected monitoring. The novelty boundary (empirical reliability assessment, not a new method) is unchanged.", "",
 "## Gate", "**Scientific-value gate: PASS (modest).** The revision is limited to one Methods subsection, one Results subsection, one figure, one Table 1 row, one reference and short edits to abstract, introduction, discussion, limitations, conclusions, data availability and cover letter. No previously reported number changed."])
print("ok", len(pv), "provenance rows")
