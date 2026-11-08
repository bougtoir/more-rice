#!/usr/bin/env python3
"""Assemble FINAL_INDIVIDUAL_DOWNLOADS/ (numbered, individually downloadable files),
the SHA-256 manifest and the convenience ZIP."""
import os, shutil, hashlib, zipfile, csv, pandas as pd, docx
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
AG = os.path.join(REPO, "outputs", "modern_rice", "applied_geography"); SUB = os.path.join(AG, "submission")
QC = os.path.join(AG, "delta_qc"); DL = os.path.join(SUB, "FINAL_INDIVIDUAL_DOWNLOADS"); ART = os.path.join(SUB, "figures")
if os.path.isdir(DL): shutil.rmtree(DL)
os.makedirs(DL)
M = [("01_APPLIED_GEOGRAPHY_MANUSCRIPT_FINAL.docx", os.path.join(SUB, "APPLIED_GEOGRAPHY_MANUSCRIPT_FINAL.docx")),
     ("02_APPLIED_GEOGRAPHY_MANUSCRIPT_REVIEW.pdf", os.path.join(SUB, "APPLIED_GEOGRAPHY_MANUSCRIPT_INLINE_REVIEW_COPY.pdf")),
     ("03_APPLIED_GEOGRAPHY_COVER_LETTER_FINAL.docx", os.path.join(SUB, "APPLIED_GEOGRAPHY_COVER_LETTER.docx")),
     ("04_FINAL_HANDOFF_AND_AUTHOR_ACTIONS.md", os.path.join(QC, "FINAL_HANDOFF_AND_AUTHOR_ACTIONS.md")),
     ("05_SCIENTIFIC_CLAIM_DIFF.csv", os.path.join(QC, "SCIENTIFIC_CLAIM_DIFF.csv")),
     ("06_GDD_INDEPENDENT_AUDIT.md", os.path.join(QC, "GDD_INDEPENDENT_AUDIT.md")),
     ("07_SPATIAL_DENOMINATOR_AND_SCALE_AUDIT.md", os.path.join(QC, "SPATIAL_DENOMINATOR_AND_SCALE_AUDIT.md")),
     ("08_LOWER_DANUBE_WATER_AND_SOURCE_AUDIT.md", os.path.join(QC, "LOWER_DANUBE_WATER_AND_SOURCE_AUDIT.md")),
     ("09_PORTFOLIO_MODEL_INDEPENDENT_AUDIT.md", os.path.join(QC, "PORTFOLIO_MODEL_INDEPENDENT_AUDIT.md")),
     ("10_CLOSEST_PRIOR_STUDIES_MATRIX.csv", os.path.join(QC, "CLOSEST_PRIOR_STUDIES_MATRIX.csv")),
     ("11_REFERENCE_AND_SOURCE_AUDIT.md", os.path.join(QC, "REFERENCE_AND_SOURCE_AUDIT.md")),
     ("12_TEXT_FIGURE_TABLE_NUMERIC_CONSISTENCY_AUDIT.md", os.path.join(QC, "TEXT_FIGURE_TABLE_NUMERIC_CONSISTENCY_AUDIT.md")),
     ("13_HOSTILE_SCIENTIFIC_AND_DESK_REVIEW.md", os.path.join(QC, "HOSTILE_SCIENTIFIC_AND_DESK_REVIEW.md")),
     ("14_JOURNAL_REQUIREMENTS_VERIFIED.md", os.path.join(QC, "JOURNAL_REQUIREMENTS_VERIFIED.md")),
     ("16_REVIEWER_AND_SUBMISSION_METADATA_TEMPLATE.md", os.path.join(QC, "REVIEWER_AND_SUBMISSION_METADATA_TEMPLATE.md"))]
for i in range(1, 6): M.append((f"{18+i}_FIGURE_{i}_FINAL.png", os.path.join(ART, f"Figure_{i}.png")))
for dst, src in M: shutil.copy(src, os.path.join(DL, dst))
# 24: tables as xlsx from the editable Word tables
d = docx.Document(os.path.join(SUB, "APPLIED_GEOGRAPHY_TABLES_EDITABLE.docx"))
with pd.ExcelWriter(os.path.join(DL, "24_TABLES_FINAL.xlsx")) as xw:
    for k, t in enumerate(d.tables, 1):
        rows = [[c.text for c in r.cells] for r in t.rows]
        pd.DataFrame(rows[1:], columns=rows[0]).to_excel(xw, sheet_name=f"Table_{k}", index=False)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
man = os.path.join(DL, "15_FINAL_FILE_MANIFEST_SHA256.csv")
with open(man, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["file", "bytes", "sha256"])
    for fn in sorted(os.listdir(DL)):
        if fn.startswith("15_"): continue
        p = os.path.join(DL, fn); w.writerow([fn, os.path.getsize(p), sha(p)])
    w.writerow(["17_GRAPHICAL_ABSTRACT_FINAL.png / 18_GRAPHICAL_ABSTRACT_EDITABLE.svg", "", "NOT SUPPLIED: graphical abstract is encouraged, not required, by Applied Geography; deliberately omitted"])
Z = os.path.join(SUB, "APPLIED_GEOGRAPHY_FINAL_SUBMISSION_PACKAGE.zip")
with zipfile.ZipFile(Z, "w", zipfile.ZIP_DEFLATED) as z:
    for fn in sorted(os.listdir(DL)): z.write(os.path.join(DL, fn), f"FINAL_INDIVIDUAL_DOWNLOADS/{fn}")
    for fn in sorted(os.listdir(SUB)):
        p = os.path.join(SUB, fn)
        if os.path.isfile(p) and not fn.endswith(".zip"): z.write(p, f"submission/{fn}")
    for fn in sorted(os.listdir(ART)): z.write(os.path.join(ART, fn), f"submission/artwork/{fn}")
print(open(man).read()); print("zip", os.path.getsize(Z), sha(Z))
