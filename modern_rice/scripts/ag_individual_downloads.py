#!/usr/bin/env python3
"""Assemble FINAL_INDIVIDUAL_DOWNLOADS/ (38 numbered files), the submission ZIP (37), the independent-audit evidence
ZIP (38) and the SHA-256 manifest (29). Restricted raw data are never included."""
import os, shutil, hashlib, zipfile, csv, glob, pandas as pd, docx
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
AG = os.path.join(REPO, "outputs", "modern_rice", "applied_geography"); SUB = os.path.join(AG, "submission"); FA = os.path.join(AG, "final_audit")
DL = os.path.join(SUB, "FINAL_INDIVIDUAL_DOWNLOADS"); ART = os.path.join(SUB, "figures"); S = HERE
if os.path.isdir(DL): shutil.rmtree(DL)
os.makedirs(DL)
M = [("01_APPLIED_GEOGRAPHY_MANUSCRIPT_FINAL.docx", f"{SUB}/APPLIED_GEOGRAPHY_MANUSCRIPT_FINAL.docx"), ("02_APPLIED_GEOGRAPHY_MANUSCRIPT_REVIEW.pdf", f"{SUB}/APPLIED_GEOGRAPHY_MANUSCRIPT_INLINE_REVIEW_COPY.pdf"),
     ("03_APPLIED_GEOGRAPHY_COVER_LETTER_FINAL.docx", f"{SUB}/APPLIED_GEOGRAPHY_COVER_LETTER.docx"), ("04_FINAL_HANDOFF_AND_AUTHOR_ACTIONS.md", f"{FA}/FINAL_HANDOFF_AND_AUTHOR_ACTIONS.md"),
     ("05_GERMANY_THERMAL_CONTRAST_DECOMPOSITION.md", f"{FA}/GERMANY_THERMAL_CONTRAST_DECOMPOSITION.md"), ("06_GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv", f"{FA}/GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv"),
     ("07_GERMANY_THERMAL_CONTRAST_INDEPENDENT_CHECK.py", f"{S}/GERMANY_THERMAL_CONTRAST_INDEPENDENT_CHECK.py"), ("08_GERMANY_THERMAL_CONTRAST_INPUT_PROVENANCE.csv", f"{FA}/GERMANY_THERMAL_CONTRAST_INPUT_PROVENANCE.csv"),
     ("09_EUROPE_SPATIAL_DENOMINATOR_AUDIT.md", f"{FA}/EUROPE_SPATIAL_DENOMINATOR_AUDIT.md"), ("10_EUROPE_SPATIAL_GATE_COUNTS.csv", f"{FA}/EUROPE_SPATIAL_GATE_COUNTS.csv"),
     ("11_CLOSEST_PRIOR_STUDIES_MATRIX_FINAL.csv", f"{FA}/CLOSEST_PRIOR_STUDIES_MATRIX_FINAL.csv"), ("12_GEOGRAPHIC_NOVELTY_AND_PRIOR_WORK_AUDIT.md", f"{FA}/GEOGRAPHIC_NOVELTY_AND_PRIOR_WORK_AUDIT.md"),
     ("13_CLAIM_IMPLEMENTATION_INDEPENDENCE_MATRIX.csv", f"{FA}/CLAIM_IMPLEMENTATION_INDEPENDENCE_MATRIX.csv"), ("14_KNOWN_ANSWER_TEST_REPORT.md", f"{FA}/KNOWN_ANSWER_TEST_REPORT.md"),
     ("15_DECISION_CRITICAL_NUMERICAL_AUDIT.md", f"{FA}/DECISION_CRITICAL_NUMERICAL_AUDIT.md"), ("16_SCIENTIFIC_CORRECTION_HISTORY.md", f"{FA}/SCIENTIFIC_CORRECTION_HISTORY.md"),
     ("17_CLAIM_TO_EVIDENCE_MATRIX.csv", f"{FA}/CLAIM_TO_EVIDENCE_MATRIX.csv"), ("18_DATA_PROVENANCE_AND_ACCESS_MANIFEST.csv", f"{FA}/DATA_PROVENANCE_AND_ACCESS_MANIFEST.csv"),
     ("19_CANONICAL_RESULTS_REGISTRY.csv", f"{FA}/CANONICAL_RESULTS_REGISTRY.csv"), ("20_FIGURE_TABLE_PROVENANCE_MATRIX.csv", f"{FA}/FIGURE_TABLE_PROVENANCE_MATRIX.csv"),
     ("21_REFERENCE_CLAIM_SUPPORT_MATRIX.csv", f"{FA}/REFERENCE_CLAIM_SUPPORT_MATRIX.csv"), ("22_INDEPENDENT_AUDITOR_README.md", f"{FA}/INDEPENDENT_AUDITOR_README.md")]
M += [(os.path.basename(p), p) for p in sorted(glob.glob(f"{FA}/2[3-7]_*.md"))]
M += [("28_FINAL_PR_MERGE_RECOMMENDATION.md", f"{FA}/FINAL_PR_MERGE_RECOMMENDATION.md"), ("30_FINAL_SUBMISSION_GATE.md", f"{FA}/30_FINAL_SUBMISSION_GATE.md")]
M += [(f"{30+i}_FIGURE_{i}_FINAL.png", f"{ART}/Figure_{i}.png") for i in range(1, 6)]
assert len(M) == 34, len(M)
for dst, src in M: shutil.copy(src, os.path.join(DL, dst))
d = docx.Document(os.path.join(SUB, "APPLIED_GEOGRAPHY_TABLES_EDITABLE.docx"))
with pd.ExcelWriter(os.path.join(DL, "36_TABLES_FINAL.xlsx")) as xw:
    for k, t in enumerate(d.tables, 1):
        rows = [[c.text for c in r.cells] for r in t.rows]; pd.DataFrame(rows[1:], columns=rows[0]).to_excel(xw, sheet_name=f"Table_{k}", index=False)
RESTRICT = ("data/raw", "estreams", "EStreams", ".nc", "hydrology_estreams")
def safe(arc):
    assert not any(r in arc for r in RESTRICT if r not in ("EStreams",)) and "/raw/" not in arc, arc; return arc
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
# 38: independent audit evidence ZIP
Z38 = os.path.join(DL, "38_INDEPENDENT_AUDIT_EVIDENCE_PACKAGE.zip")
with zipfile.ZipFile(Z38, "w", zipfile.ZIP_DEFLATED) as z:
    for fn in sorted(os.listdir(DL)):
        if fn[:2] in {f"{i:02d}" for i in range(4, 31)}: z.write(os.path.join(DL, fn), safe(f"numbered/{fn}"))
    for p in sorted(glob.glob(f"{FA}/*")): z.write(p, safe(f"final_audit/{os.path.basename(p)}"))
    for p in sorted(glob.glob(f"{AG}/*.csv") + glob.glob(f"{AG}/*.json")): z.write(p, safe(f"derived_outputs/{os.path.basename(p)}"))
    for p in sorted(glob.glob(f"{AG}/delta_qc/*.md") + glob.glob(f"{AG}/delta_qc/*.csv")): z.write(p, safe(f"earlier_delta_qc/{os.path.basename(p)}"))
    for p in sorted(glob.glob(f"{S}/ag_*.py") + glob.glob(f"{S}/build_ag_manuscript.py") + glob.glob(f"{S}/GERMANY_*.py") + [f"{S}/risk_portfolio.py", f"{S}/fetch_nasa_power.py"]): z.write(p, safe(f"scripts/{os.path.basename(p)}"))
    z.write(os.path.join(REPO, "modern_rice", "manuscript_ag", "manuscript_template.md"), "manuscript/manuscript_template.md"); z.write(os.path.join(REPO, "modern_rice", "manuscript_ag", "README.md"), "manuscript/README.md")
    z.write(os.path.join(REPO, "modern_rice", "data", "RAW_ACQUISITION_LEDGER_2026-11-08.csv"), "ledger/RAW_ACQUISITION_LEDGER_2026-11-08.csv")
    z.write(os.path.join(SUB, "MANUSCRIPT_NUMBERS.json"), "manuscript/MANUSCRIPT_NUMBERS.json")
    z.writestr("README.md", open(f"{FA}/INDEPENDENT_AUDITOR_README.md").read() + "\n\nRaw input data are NOT included (licence/size); see ledger and DATA_PROVENANCE_AND_ACCESS_MANIFEST.csv.\n")
# 37: submission ZIP
Z37 = os.path.join(DL, "37_APPLIED_GEOGRAPHY_FINAL_SUBMISSION_PACKAGE.zip")
with zipfile.ZipFile(Z37, "w", zipfile.ZIP_DEFLATED) as z:
    for fn in sorted(os.listdir(DL)):
        if fn[:2] in {f"{i:02d}" for i in range(1, 37)}: z.write(os.path.join(DL, fn), safe(f"FINAL_INDIVIDUAL_DOWNLOADS/{fn}"))
    for fn in sorted(os.listdir(SUB)):
        p = os.path.join(SUB, fn)
        if os.path.isfile(p) and not fn.endswith(".zip"): z.write(p, safe(f"submission/{fn}"))
    for fn in sorted(os.listdir(ART)): z.write(os.path.join(ART, fn), safe(f"submission/artwork/{fn}"))
for zz in [Z37, Z38]:
    names = zipfile.ZipFile(zz).namelist(); assert not any("/raw/" in n or "hydrology_estreams" in n or n.endswith((".tif", ".nc", ".npy")) for n in names), zz
man = os.path.join(DL, "29_FINAL_FILE_MANIFEST_SHA256.csv")
with open(man, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["file", "bytes", "sha256", "in_submission_zip_37", "in_audit_zip_38"])
    n37, n38 = set(zipfile.ZipFile(Z37).namelist()), set(zipfile.ZipFile(Z38).namelist())
    for fn in sorted(os.listdir(DL)):
        if fn.startswith("29_"): continue
        p = os.path.join(DL, fn); w.writerow([fn, os.path.getsize(p), sha(p), f"FINAL_INDIVIDUAL_DOWNLOADS/{fn}" in n37, f"numbered/{fn}" in n38])
    w.writerow(["29_FINAL_FILE_MANIFEST_SHA256.csv", "", "self (not self-referenced)", False, False])
shutil.copy(Z37, os.path.join(SUB, "APPLIED_GEOGRAPHY_FINAL_SUBMISSION_PACKAGE.zip"))
fs = sorted(os.listdir(DL)); assert len(fs) == 38 and all(os.path.getsize(os.path.join(DL, f)) > 0 for f in fs), fs
print(open(man).read()); print("37", os.path.getsize(Z37), "38", os.path.getsize(Z38))
