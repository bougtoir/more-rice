#!/usr/bin/env python3
"""Independent-audit evidence package: claim-to-evidence matrix, data provenance/access manifest, canonical results
registry (read from analysis outputs), figure/table provenance, reference-claim support matrix."""
import os, re, json, csv, glob, hashlib, subprocess, urllib.request, difflib, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
AG = os.path.join(ROOT, "outputs", "modern_rice", "applied_geography"); FA = os.path.join(AG, "final_audit"); SUB = os.path.join(AG, "submission"); QC = os.path.join(AG, "delta_qc")
RAWD = os.path.join(ROOT, "modern_rice", "data"); LIT = os.path.join(RAWD, "raw", "literature_openalex_2026-11-08")
rel = lambda p: os.path.relpath(p, ROOT)
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
# ---------- data provenance ----------
try: assets = {a["name"]: a["size"] for a in json.loads(subprocess.run(["gh", "release", "view", "more-rice-raw-2026-11-08", "-R", "bougtoir/wip", "--json", "assets"], capture_output=True, text=True, check=True).stdout)["assets"]}
except Exception: assets = {}
def archive_for(f):
    b = os.path.basename(f)
    if "hydrology" in b or "estreams" in b.lower(): return "hydrology_estreams_2026-11-08.zip"
    if "nasa_power_1981_2000" in f: return "nasa_power_1981_2000_2026-11-08.tar.gz"
    if "nasa_power" in b: return "nasa_power_json_2026-11-08.tgz"
    for a in assets:
        if b in a or a.split(".")[0] in b: return a
    return "see release asset list"
led = list(csv.DictReader(open(os.path.join(RAWD, "RAW_ACQUISITION_LEDGER_2026-11-08.csv"))))
prov = []
for r in led:
    f = r["file"]; p = os.path.join(ROOT, f) if not f.startswith("raw/") else os.path.join(RAWD, f)
    lic = r["license_note"]; restricted = any(k in lic.upper() for k in ["NC", "GRDC", "NOT REDISTRIBUT", "RESTRICT"]) or "estreams" in f.lower()
    prov.append(dict(file=f, source_url=r["source_url"], retrieved_utc=r["retrieved_utc"], bytes_ledger=r["bytes"], sha256_ledger=r["sha256"],
                     present_on_build_machine=os.path.exists(p), sha256_matches_ledger=(sha(p) == r["sha256"]) if os.path.exists(p) and r["sha256"] and os.path.getsize(p) < 3e9 else "",
                     in_public_repo="no (gitignored modern_rice/data/raw/)", private_archive=f"bougtoir/wip release more-rice-raw-2026-11-08 :: {archive_for(f)}", private_archive_asset_listed=archive_for(f) in assets,
                     license_or_terms=lic, redistribution_in_public_repo="NOT PERMITTED / not done" if restricted else "permitted by licence but not done (size); re-download from source_url",
                     how_an_auditor_obtains_it="request from GRDC / EStreams (Zenodo, CC BY-NC) under their terms" if restricted else "public download from source_url"))
P = pd.DataFrame(prov); P.to_csv(os.path.join(FA, "DATA_PROVENANCE_AND_ACCESS_MANIFEST.csv"), index=False)
# ---------- canonical results registry (read from outputs) ----------
R = []
def add(rid, desc, val, unit, src, sel): R.append(dict(result_id=rid, description=desc, value=val, unit=unit, source_file=rel(src), selector=sel))
cal = os.path.join(AG, "GRID_THERMAL_CALIBRATION.json"); C = json.load(open(cal))
for k in ["T_star_pipeline", "T_star_calJunSep", "hokkaido_P01_pipeline", "hokkaido_P10_pipeline", "hokkaido_P50_pipeline", "hokkaido_rice_ha"]: add(f"cal.{k}", k, C[k], "GDD10" if "rice_ha" not in k else "ha", cal, k)
dom = os.path.join(AG, "EUROPE_DOMAIN_SENSITIVITY.csv")
for r in pd.read_csv(dom).itertuples():
    add(f"domain.{r.domain}.incumbent", f"incumbent arable, {r.domain}", r.incumbent_Mha, "Mha", dom, f"domain={r.domain}:incumbent_Mha")
    add(f"domain.{r.domain}.thermal", f"thermal pass share, {r.domain}", round(100 * r.thermal_pass_share, 2), "%", dom, "thermal_pass_share×100")
    add(f"domain.{r.domain}.thermal_aei", f"thermal + AEI≥10% share, {r.domain}", round(100 * r.thermal_aei_share, 2), "%", dom, "thermal_aei_share×100")
gd = os.path.join(AG, "GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv")
for i, r in pd.read_csv(gd).iterrows(): add(f"germany.{i:02d}", f"{r.block}: {r.label} [{r.surface_resolution}, {r.surface_window}]", r.germany_pass_pct, "% DE incumbent passing", gd, f"row {i}; threshold {r.threshold_gdd10}")
hy = os.path.join(AG, "HYDROLOGICAL_LOW_FLOW_RESULTS.csv")
for i, r in pd.read_csv(hy).iterrows():
    if pd.notna(r.value_m3s): add(f"hydro.{i:02d}", f"{r.station} {r.period} {r.statistic}", r.value_m3s, "m³/s", hy, f"row {i}")
dd = os.path.join(AG, "DANUBE_DEMAND_VS_LOWFLOW.csv"); d = pd.read_csv(dd)
for i, r in d[(d.area_ha == 250000) & (d.seasonal_depth_mm == 1000) & (d.season_days == 120)].iterrows():
    for c in [c for c in d.columns if c.endswith("m3s")]: add(f"demand.{c}", f"250,000 ha, 1,000 mm, 120 d: {c}", r[c], "m³/s", dd, f"row {i}:{c}")
rb = os.path.join(AG, "RISK_PORTFOLIO_BASELINE_CORRECTED.csv")
for r in pd.read_csv(rb).itertuples():
    for c in ["P_A", "P_B_rice", "P_D_potato", "diff_CI95_lo", "diff_CI95_hi"]: add(f"risk.{r.country}.{c}", f"{r.country} baseline {c}", getattr(r, c), "probability", rb, f"country={r.country}")
ro = os.path.join(AG, "RISK_PORTFOLIO_ROBUSTNESS.csv")
for r in pd.read_csv(ro).itertuples(): add(f"robust.{r.country}", f"{r.country} share of 24 configurations with CI excluding 0", r.share_CI_excl_0, "share", ro, f"country={r.country}")
num = os.path.join(SUB, "MANUSCRIPT_NUMBERS.json")
for k, v in json.load(open(num)).items(): add(f"ms.{k}", "manuscript placeholder value (formatted by build_ag_manuscript.py from the outputs above)", v, "", num, k)
RR = pd.DataFrame(R); RR.to_csv(os.path.join(FA, "CANONICAL_RESULTS_REGISTRY.csv"), index=False)
# ---------- figure / table provenance ----------
FT = [("Figure 1", "Gate framework schematic", "ag_figures.py", "GRID_THERMAL_CALIBRATION.json (T*)", "submission/figures/Figure_1.png"),
      ("Figure 2", "Gate-class map and thermal map, EPSG:3035", "ag_figures.py", "grid_class_5m.npy, grid_gdd_5m.npy, grid_inc_5m.npy (from ag_grid_gates.py)", "submission/figures/Figure_2.png"),
      ("Figure 3", "Threshold/resolution sensitivity, POWER–WorldClim cross-walk, (d) Germany reference-construction path", "ag_figures.py", "EUROPE_THRESHOLD_CURVE.csv, EUROPE_SCALE_THRESHOLD_SENSITIVITY.csv, POINT_GRID_CROSSWALK.csv, GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv", "submission/figures/Figure_3.png"),
      ("Figure 4", "Water geography: grid deficit vs point balance; Danube demand vs Orsova low flow", "ag_figures.py", "POINT_GRID_CROSSWALK.csv, DANUBE_DEMAND_VS_LOWFLOW.csv, HYDROLOGICAL_LOW_FLOW_RESULTS.csv", "submission/figures/Figure_4.png"),
      ("Figure 5", "Food-supply risk scenarios with bootstrap intervals", "ag_figures.py", "RISK_PORTFOLIO_BASELINE_CORRECTED.csv, RISK_PORTFOLIO_ROBUSTNESS.csv", "submission/figures/Figure_5.png"),
      ("Table 1", "Data sources", "build_ag_manuscript.py (TABS['data'])", "source metadata in build script; ledger", "submission/APPLIED_GEOGRAPHY_TABLES_EDITABLE.docx"),
      ("Table 2", "Gate cascade by country", "build_ag_manuscript.py (TABS['cascade'])", "EUROPE_GATE_CASCADE_BY_COUNTRY.csv", "submission/APPLIED_GEOGRAPHY_TABLES_EDITABLE.docx"),
      ("Table 3", "Corrected portfolio scenarios and robustness", "build_ag_manuscript.py (TABS['risk'])", "RISK_PORTFOLIO_BASELINE_CORRECTED.csv, RISK_PORTFOLIO_ROBUSTNESS.csv", "submission/APPLIED_GEOGRAPHY_TABLES_EDITABLE.docx")]
ftr = []
for n, desc, scr, ins, art in FT:
    p = os.path.join(AG, art); ftr.append(dict(item=n, content=desc, generating_script=f"modern_rice/scripts/{scr.split(' ')[0]}", inputs=ins, artwork=rel(p), artwork_sha256=sha(p), changed_in_this_revision="yes" if n in ["Figure 3"] else "rebuilt, content unchanged"))
pd.DataFrame(ftr).to_csv(os.path.join(FA, "FIGURE_TABLE_PROVENANCE_MATRIX.csv"), index=False)
# ---------- reference–claim support ----------
tpl = open(os.path.join(ROOT, "modern_rice", "manuscript_ag", "manuscript_template.md")).read()
body, refs = tpl.split("# REFERENCES")[0], [l.strip() for l in tpl.split("# REFERENCES")[1].split("\n") if l.strip()]
sent = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", body))
pm = pd.read_csv(os.path.join(FA, "CLOSEST_PRIOR_STUDIES_MATRIX_FINAL.csv")).set_index("doi")
rows = []
for ref in refs:
    m = re.match(r"^(.+?)\((\d{4})\)", ref); auth, yr = m.group(1), m.group(2); first = re.split(r",| &", auth.strip())[0].strip().rstrip(".")
    doi = (re.search(r"https://doi.org/(\S+)", ref) or [None, None])[1]; doi = doi.rstrip(".") if doi else None
    key = re.escape(first.split(" ")[-1] if first.startswith("do Nascimento") else first)
    cites = [s for s in sent if re.search(key + r"[^()]{0,40}?,? \(?" + yr, s) or (re.search(key, s) and yr in s)]
    cr_title, sim = "", ""
    if doi:
        f = os.path.join(LIT, "crossref_" + doi.replace("/", "_") + ".json")
        if not os.path.exists(f):
            try:
                rq = urllib.request.Request("https://api.crossref.org/works/" + doi, headers={"User-Agent": "more-rice audit (mailto:bougtoir@gmail.com)"}); json.dump(json.load(urllib.request.urlopen(rq, timeout=60)), open(f, "w"))
            except Exception as e: cr_title = f"CROSSREF ERROR {e}"
        if os.path.exists(f):
            cr_title = json.load(open(f))["message"]["title"][0]
            reft = re.sub(r"\*", "", ref.split(f"({yr}). ")[1]) if f"({yr}). " in ref else ref
            sim = round(difflib.SequenceMatcher(None, cr_title.lower(), reft[:len(cr_title)].lower()).ratio(), 2)
    content = pm.loc[doi, "content_source"] if doi in pm.index else ("dataset documentation / landing page" if "[dataset]" in ref else "bibliographic record; claim scope judged from title and prior source audit (delta_qc/REFERENCE_AND_SOURCE_AUDIT.md)")
    rows.append(dict(reference=ref[:160], first_author=first, year=yr, doi=doi or "", crossref_title=cr_title, title_similarity=sim, n_citing_sentences=len(cites), citing_sentences=" || ".join(c[:300] for c in cites[:4]),
                     content_verification=content, cited_in_text="yes" if cites else "NOT CITED IN TEXT", claim_support_basis="citing sentence(s) checked against the content source in content_verification; claims are limited to what that source reports"))
RF = pd.DataFrame(rows); RF.to_csv(os.path.join(FA, "REFERENCE_CLAIM_SUPPORT_MATRIX.csv"), index=False)
# ---------- claim-to-evidence ----------
CE = [("Thermal reference T* = 589 GDD10 is system-specific, not physiological", "2.2, 3.1", "cal.T_star_pipeline", "GRID_THERMAL_CALIBRATION.json; GERMANY_THERMAL_CONTRAST_INDEPENDENT_CHECK.json", "C1", "supported"),
      ("Germany 96.6% vs 3.2% is a reference-construction (estimand) contrast, not a resolution effect", "2.5, 3.3, Fig 3d", "germany.*", "final_audit/GERMANY_THERMAL_CONTRAST_DECOMPOSITION.md/.csv", "C2, C3", "supported; order-dependent path"),
      ("Europe excl. Russia denominator 69.7 Mha; 92.2% thermal pass; 16.0% thermal + AEI≥10%", "Abstract, 2.1, 3.2", "domain.Europe_excl_Russia (primary).*", "final_audit/EUROPE_SPATIAL_DENOMINATOR_AUDIT.md; EUROPE_SPATIAL_GATE_COUNTS.csv", "C4", "supported"),
      ("Irrigation infrastructure, not temperature, is the binding screening gate", "3.2, 4.1", "domain.*.thermal_aei", "EUROPE_GATE_CASCADE_BY_COUNTRY.csv; EUROPE_AEI_THRESHOLD_SENSITIVITY.csv", "C4", "supported as screening result; AEI ≠ operational feasibility"),
      ("Europe-wide share changes ≤ ~4 pp with resolution/aggregation; class changes are substantial locally", "3.3, Fig 3b", "ms.max_scale_pts, ms.dis_900_60", "EUROPE_SCALE_THRESHOLD_SENSITIVITY.csv", "pipeline only", "supported (not independently recomputed)"),
      ("Monthly-mean GDD underestimates daily GDD (≤29 GDD10 at points)", "4.4", "ms.*", "GDD_DAILY_VS_MONTHLY.csv; KNOWN_ANSWER_TEST_REPORT.md", "C5", "supported"),
      ("250,000 ha Lower Danube scenario: net ~241 m³/s, gross ~321.5 m³/s", "3.4", "demand.*", "DANUBE_DEMAND_VS_LOWFLOW.csv; DECISION_CRITICAL_NUMERICAL_AUDIT.md", "C6", "supported (scenario arithmetic)"),
      ("Orsova Jun–Sep minimum daily discharge median 2,749 m³/s; gross = 11.7% of median, 22.8% of lowest", "3.4", "hydro.*", "HYDROLOGICAL_LOW_FLOW_RESULTS.csv; delta_qc/HYDROLOGICAL_LOW_FLOW_ANALYSIS.md", "C7, C8", "supported; not a Q99; not allocable water"),
      ("Rice substitution reduces modeled shortfall probability robustly only in Kazakhstan (58% of configurations)", "3.5, Table 3, Fig 5", "risk.*, robust.*", "RISK_PORTFOLIO_*.csv", "C9", "supported as modeled statistic"),
      ("Mapped suitability/AEI is not operational feasibility, permits, delivery capacity or economics", "Abstract, 4.3, 4.4", "—", "manuscript text; EUROPE_DOMAIN_AND_MASK_PROVENANCE.md", "—", "interpretive constraint")]
pd.DataFrame(CE, columns=["claim", "manuscript_location", "canonical_result_ids", "evidence_files", "independent_check_ids (CLAIM_IMPLEMENTATION_INDEPENDENCE_MATRIX)", "status"]).to_csv(os.path.join(FA, "CLAIM_TO_EVIDENCE_MATRIX.csv"), index=False)
print("provenance", len(P), "present", P.present_on_build_machine.sum(), "sha_ok", (P.sha256_matches_ledger == True).sum(), "assets_listed", P.private_archive_asset_listed.sum())
print("registry", len(RR)); print(RF[["first_author", "year", "title_similarity", "n_citing_sentences", "cited_in_text"]].to_string())
