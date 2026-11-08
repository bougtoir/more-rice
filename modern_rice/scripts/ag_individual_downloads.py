#!/usr/bin/env python3
"""Assemble FINAL_INDIVIDUAL_DOWNLOADS/ (numbered, individually downloadable files),
the SHA-256 manifest and the convenience ZIP."""
import os, shutil, hashlib, zipfile, csv, pandas as pd, docx
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
AG = os.path.join(REPO, "outputs", "modern_rice", "applied_geography"); SUB = os.path.join(AG, "submission")
QC = os.path.join(AG, "delta_qc"); DL = os.path.join(SUB, "FINAL_INDIVIDUAL_DOWNLOADS"); ART = os.path.join(SUB, "figures")
if os.path.isdir(DL): shutil.rmtree(DL)
os.makedirs(DL)
H = os.path.join(AG, "delta_qc")
M = [("01_APPLIED_GEOGRAPHY_MANUSCRIPT_FINAL.docx", os.path.join(SUB, "APPLIED_GEOGRAPHY_MANUSCRIPT_FINAL.docx")),
     ("02_APPLIED_GEOGRAPHY_MANUSCRIPT_REVIEW.pdf", os.path.join(SUB, "APPLIED_GEOGRAPHY_MANUSCRIPT_INLINE_REVIEW_COPY.pdf")),
     ("03_APPLIED_GEOGRAPHY_COVER_LETTER_FINAL.docx", os.path.join(SUB, "APPLIED_GEOGRAPHY_COVER_LETTER.docx")),
     ("04_FINAL_HANDOFF_AND_AUTHOR_ACTIONS.md", os.path.join(QC, "FINAL_HANDOFF_AND_AUTHOR_ACTIONS.md")),
     ("05_CT_UPT_SOURCE_RESOLUTION.md", os.path.join(QC, "CT_UPT_SOURCE_RESOLUTION.md")),
     ("06_HYDROLOGICAL_STATION_AND_DATA_PROVENANCE.csv", os.path.join(QC, "HYDROLOGICAL_STATION_AND_DATA_PROVENANCE.csv")),
     ("07_HYDROLOGICAL_LOW_FLOW_ANALYSIS.md", os.path.join(QC, "HYDROLOGICAL_LOW_FLOW_ANALYSIS.md")),
     ("08_HYDROLOGICAL_LOW_FLOW_RESULTS.csv", os.path.join(AG, "HYDROLOGICAL_LOW_FLOW_RESULTS.csv")),
     ("09_IRRIGATION_DEMAND_INDEPENDENT_CHECK.md", os.path.join(QC, "IRRIGATION_DEMAND_INDEPENDENT_CHECK.md")),
     ("10_HYDROLOGICAL_CLAIM_CHANGELOG.md", os.path.join(QC, "HYDROLOGICAL_CLAIM_CHANGELOG.md")),
     ("11_SCIENTIFIC_CLAIM_DIFF_FINAL.csv", os.path.join(QC, "SCIENTIFIC_CLAIM_DIFF.csv")),
     ("12_REFERENCE_AND_SOURCE_AUDIT_FINAL.md", os.path.join(QC, "REFERENCE_AND_SOURCE_AUDIT.md")),
     ("13_TEXT_FIGURE_TABLE_NUMERIC_CONSISTENCY_FINAL.md", os.path.join(QC, "TEXT_FIGURE_TABLE_NUMERIC_CONSISTENCY_AUDIT.md")),
     ("14_HOSTILE_SCIENTIFIC_REVIEW_FINAL.md", os.path.join(QC, "HOSTILE_SCIENTIFIC_AND_DESK_REVIEW.md")),
     ("15_APPLIED_GEOGRAPHY_SCOPE_AND_NOVELTY_FINAL.md", os.path.join(QC, "APPLIED_GEOGRAPHY_SCOPE_AND_NOVELTY_FINAL.md"))]
for i in range(1, 6): M.append((f"{16+i}_FIGURE_{i}_FINAL.png", os.path.join(ART, f"Figure_{i}.png")))
for dst, src in M: shutil.copy(src, os.path.join(DL, dst))
# 24: tables as xlsx from the editable Word tables
d = docx.Document(os.path.join(SUB, "APPLIED_GEOGRAPHY_TABLES_EDITABLE.docx"))
with pd.ExcelWriter(os.path.join(DL, "22_TABLES_FINAL.xlsx")) as xw:
    for k, t in enumerate(d.tables, 1):
        rows = [[c.text for c in r.cells] for r in t.rows]
        pd.DataFrame(rows[1:], columns=rows[0]).to_excel(xw, sheet_name=f"Table_{k}", index=False)
CODE = os.path.join(DL, "23_HYDROLOGICAL_ANALYSIS_CODE.zip")
with zipfile.ZipFile(CODE, "w", zipfile.ZIP_DEFLATED) as z:
    for f in ["ag_danube_lowflow.py", "ag_danube_demand.py", "ag_hydro_evidence.py"]: z.write(os.path.join(HERE, f), f"scripts/{f}")
    for f in ["HYDROLOGICAL_LOW_FLOW_RESULTS.csv", "HYDROLOGICAL_LOW_FLOW_BY_YEAR.csv", "DANUBE_DEMAND_VS_LOWFLOW.csv"]: z.write(os.path.join(AG, f), f"derived/{f}")
    z.writestr("README.md", "Inputs (not redistributed): EStreams v1.4, doi:10.5281/zenodo.17598150 (CC BY-NC 4.0), files streamflow_indices.zip -> monthly/monthly_streamflow_{min,mean}.csv, yearly/yearly_streamflow_{min,min7days}.csv and streamflow_gauges.zip, placed under modern_rice/data/raw/hydrology/ (see RAW_ACQUISITION_LEDGER_2026-11-08.csv for SHA-256). Run: python ag_danube_lowflow.py; python ag_danube_demand.py; python ag_hydro_evidence.py.\n")
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
man = os.path.join(DL, "16_FINAL_FILE_MANIFEST_SHA256.csv")
with open(man, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["file", "bytes", "sha256"])
    for fn in sorted(os.listdir(DL)):
        if fn.startswith("16_"): continue
        p = os.path.join(DL, fn); w.writerow([fn, os.path.getsize(p), sha(p)])
    w.writerow(["24_APPLIED_GEOGRAPHY_FINAL_SUBMISSION_PACKAGE.zip", "", "contains files 01-23; its own checksum is reported separately (cannot be self-referenced)"])
Z = os.path.join(SUB, "APPLIED_GEOGRAPHY_FINAL_SUBMISSION_PACKAGE.zip")
with zipfile.ZipFile(Z, "w", zipfile.ZIP_DEFLATED) as z:
    for fn in sorted(os.listdir(DL)): z.write(os.path.join(DL, fn), f"FINAL_INDIVIDUAL_DOWNLOADS/{fn}")
    for fn in sorted(os.listdir(SUB)):
        p = os.path.join(SUB, fn)
        if os.path.isfile(p) and not fn.endswith(".zip"): z.write(p, f"submission/{fn}")
    for fn in sorted(os.listdir(ART)): z.write(os.path.join(ART, fn), f"submission/artwork/{fn}")
shutil.copy(Z, os.path.join(DL, "24_APPLIED_GEOGRAPHY_FINAL_SUBMISSION_PACKAGE.zip"))
print(open(man).read()); print("zip", os.path.getsize(Z), sha(Z))
