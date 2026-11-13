#!/usr/bin/env python3
"""Write hostile review, PR recommendation, gate and handoff; assemble numbered deliverables, ZIPs and SHA-256 manifest."""
import os, re, json, shutil, hashlib, zipfile, subprocess, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
EMA = os.path.join(ROOT, "outputs", "modern_rice", "ema"); SUB = os.path.join(EMA, "submission"); REP = os.path.join(EMA, "reports"); FIG = os.path.join(EMA, "figures")
DL = os.path.join(EMA, "deliverables"); shutil.rmtree(DL, ignore_errors=True); os.makedirs(DL)
N = json.load(open(os.path.join(SUB, "EMA_MANUSCRIPT_VALUES.json"))); kat = pd.read_csv(os.path.join(EMA, "KNOWN_ANSWER_TESTS_FINAL.csv"))
git = lambda *a: subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True).stdout.strip()
HEAD, MAIN, BR = git("rev-parse", "HEAD"), git("rev-parse", "origin/main"), git("rev-parse", "--abbrev-ref", "HEAD")
outside = [f for f in git("diff", "--name-only", "origin/main...HEAD").split("\n") if f and not re.match(r"^(outputs/modern_rice/(ema|journal_fit_assessment|post_applied_geography)/|modern_rice/(manuscript_ema/|scripts/(ema_|build_ema))|data/(raw_public|journal_requirements)/|\.gitignore$)", f)]
private = [f for f in git("ls-files").split("\n") if f.startswith("modern_rice/data/raw/") and ("literature" in f or f.endswith(".pdf"))]
kp = f"{int((kat.result == 'PASS').sum())}/{len(kat)}"
def W(name, lines): open(os.path.join(REP, name), "w").write("\n".join(lines) + "\n")
W("HOSTILE_EMA_EDITOR_REVIEW_FINAL.md", ["# Hostile EM&A editorial review (performed before mechanical QC)", "",
 "| Question | Assessment |", "|---|---|",
 "| Environmental assessment or GIS crop mapping? | Framed as reliability of an environmental suitability assessment; still uses crop maps and a crop-transfer case. An editor can read it as GIS crop mapping. |",
 f"| Beyond deterministic monotonicity? | Yes, partly: the informative result is where omission rises (≤5% up to {N['T_om5']}, >10% from {N['T_om10']}) relative to the competing references, and that the check cannot discriminate T* from 900. The monotonic shape itself is not claimed. |",
 "| Rice map independent? | No: same product as calibration (MapSPAM), allocation uses suitability/irrigation priors. Disclosed in §2.5 and §4.3. |",
 f"| High inclusion from permissive gate? | Yes, this is stated explicitly (§4.1): low omission ({N['om_T']}%) is mechanically expected for any permissive threshold. |",
 "| Validates actual cultivation? | No. Presence-only, modelled allocation. Stated. |",
 "| Independent negatives? | None. No specificity/precision/AUC computed. |",
 "| Literature already establishes the insight? | Threshold and MAUP sensitivity are known (Malone 2015; Xu & Zhang 2013; Jelinski & Wu 1996; Snelder 2023). New: controlled decomposition plus demonstration that mapped-cultivation coverage is uninformative in the decisive range. Modest. |", "",
 "## Five strongest desk-rejection risks", "| # | Risk | Evidence | Severity | Resolution in this version | Next action |", "|---|---|---|---|---|---|",
 "| 1 | Scope: no new author-collected field data; 'strictly modelling studies with little field data support' excluded | EM&A Aims & Scope (archived) | HIGH | Framed as assessment of monitoring/census-derived products; 8/19 audited EM&A papers had no new field data | Optional: add independent parcel-level rice presence (e.g., open French RPG parcel register, crop code for rice) as external omission check |",
 "| 2 | Omission analysis judged trivial (monotone) | Reviewer logic | MEDIUM | Location-of-rise and non-discrimination result; scenario ranges (shifts, LOCO) | None required |",
 "| 3 | Circular validation (MapSPAM used for calibration and evaluation) | §2.5 | MEDIUM | Disclosed; not used as validation of infrastructure gate | Independent parcel data (as in 1) would resolve |",
 "| 4 | Crop-management / economic exclusion | Aims & Scope exclusions 6, 8 | LOW–MEDIUM | Economic parity, hydrology and food-risk removed from narrative | None |",
 "| 5 | Insufficient novelty (cf. AG desk reject) | AG decision letter | MEDIUM | Novelty boundary explicit; no method claims | Cover letter states incremental contribution |", "",
 "## Minor", f"- Length ~3,200 words vs EM&A average ~9,000 (no limit). Acceptable.", "- Single case (Hokkaido → Europe); generality argued, not shown."])
W("FINAL_PR_MERGE_RECOMMENDATION.md", ["# PR and merge recommendation", "", f"- origin/main: `{MAIN}`", "- PR #1 (Applied Geography): merged into main (https://github.com/bougtoir/more-rice/pull/1). Not modified here.",
 f"- PR #2: https://github.com/bougtoir/more-rice/pull/2, base `main`, head `{BR}`; evaluated head `{HEAD}` (later commits on this branch add only these generated report/deliverable files).",
 "- Mergeability: GitHub reports mergeable, no conflicts; `git merge-tree` shows 0 conflict markers.", "- CI: NOT CONFIGURED (no `.github/workflows`).",
 f"- Files outside EM&A/assessment/journal-archive paths: {outside or 'none'}. AG manuscript and AG canonical outputs unchanged.", f"- Restricted/private raw data tracked: {private or 'none'} (literature copies are gitignored and in private release).",
 "- Reason for continuing PR #2 rather than a new PR: the EM&A revision is the direct continuation of the EM&A feasibility assessment already on this branch, all new work is in new directories, and PR #1 (the AG baseline) is already merged into main, so the AG version is preserved in main history. A second PR would overlap the same branch history.",
 "", "**Recommendation: MERGE** (after the PR title/description update performed in this session). Do not merge before the author has read the gate; merging is not required for submission."])
gate = "SCIENTIFICALLY READY — AUTHOR ACTIONS PENDING"
W("FINAL_SUBMISSION_GATE.md", ["# Final submission gate (EM&A)", "", f"**Verdict: {gate}**", "",
 "| Criterion | Status |", "|---|---|", "| EM&A fit | Conditional: within scope topics (assessment, GIS, agriculture); HIGH desk-reject risk from field-data preference |",
 f"| Empirical stability and omission evidence | Present: Jaccard {N['jac_900']} (reference change) vs ≥{min(N['jac_25'], N['jac_10'])} (support change); omission {N['om_T']}%→{N['om_900']}% while candidate −{N['crop_drop_pp']} pp |",
 "| Source-independence caveats | Stated (same product, allocation priors, no negatives) |", f"| Geography/denominators | Verified ({N['inc_Mha']} Mha; {N['pct_T']}% exact; {N['pct_aei']}%) |",
 f"| Claims/references | 25 refs; EM&A refs Crossref-archived; claim matrix; KAT {kp} PASS |", "| Rendered DOCX/PDF | Inspected all pages (LibreOffice) |", "| PR recommendation | MERGE |", "| Individual deliverables | 28 numbered files + figures + tables + 2 ZIPs |", "",
 "## Author actions before submission", "1. Enter corresponding e-mail on the title page and in the cover letter.", "2. Confirm affiliation and ORCID.", "3. Select the subscription (no-APC) route in the submission system.", "4. Decide whether to add an independent parcel-level rice presence check (risk 1) before submitting.", "5. Upload figures as separate files (PNG 600 dpi or PDF vector; convert to TIFF/EPS if requested).",
 "", "Nothing has been submitted; no editor was contacted; no payment was authorised."])
W("FINAL_HANDOFF_AND_AUTHOR_ACTIONS.md", ["# Handoff (EM&A revision)", "", f"Branch `{BR}` (PR #2), evaluated head `{HEAD}`.", "",
 "## Rebuild order", "```", "python3 modern_rice/scripts/ag_grid_gates.py          # canonical AG layers (needs raw data, see AG ledger)", "python3 modern_rice/scripts/ema_threshold_sweep.py", "python3 modern_rice/scripts/ema_figures.py", "python3 modern_rice/scripts/build_ema_manuscript.py", "python3 modern_rice/scripts/ema_known_answer_tests.py", "python3 modern_rice/scripts/ema_reports.py", "python3 modern_rice/scripts/ema_package.py", "```",
 "## What changed scientifically", f"- New: threshold sweep, omission geography, alignment/LOCO scenario ranges, classification stability. Correction: thermal pass at T* is {N['pct_T']}% (AG printed 92.2% by double rounding).", "- Removed from narrative (kept in AG outputs, unchanged): Lower Danube hydrology, economic parity, food-supply risk portfolio.", "- Not restored: Q99 1,100 m³/s, 24 m³/s, 94.2%/17.6%, Serbia potato claim, Romania risk-reduction claim.",
 "", f"## Verdict: {gate}", "See `28_FINAL_SUBMISSION_GATE.md` for author actions."])

SRC = [("01_EMA_MANUSCRIPT_FINAL.docx", SUB), ("02_EMA_MANUSCRIPT_REVIEW.pdf", SUB), ("03_EMA_COVER_LETTER_FINAL.docx", SUB), ("FINAL_HANDOFF_AND_AUTHOR_ACTIONS.md", REP), ("THRESHOLD_SWEEP_METHODS_AND_RESULTS.md", REP),
 ("THRESHOLD_OMISSION_CURVE.csv", EMA), ("THRESHOLD_OMISSION_CURVE.png", FIG), ("CANDIDATE_AREA_OMISSION_TRADEOFF.png", FIG), ("RICE_AREA_OMISSION_GEOGRAPHY.png", FIG), ("RICE_AREA_VALIDATION_AND_INDEPENDENCE_AUDIT.md", REP),
 ("CLASSIFICATION_STABILITY_FINAL.md", REP), ("CLASSIFICATION_TRANSITION_MATRIX.csv", EMA), ("CLASSIFICATION_DISAGREEMENT_MAP.png", FIG), ("EUROPEAN_ASSESSMENT_VALIDITY_FINAL.md", REP), ("SEMANTIC_CODE_AUDIT_FINAL.md", REP),
 ("KNOWN_ANSWER_TESTS_FINAL.md", EMA), ("CLAIM_IMPLEMENTATION_MATRIX_FINAL.csv", REP), ("EMA_CLOSEST_PRIOR_STUDIES_FINAL.csv", REP), ("CITATION_ECOLOGY_FINAL.md", REP), ("NOVELTY_BOUNDARY_FINAL.md", REP),
 ("REFERENCE_AND_CLAIM_AUDIT_FINAL.md", REP), ("HOSTILE_EMA_EDITOR_REVIEW_FINAL.md", REP), ("TEXT_FIGURE_TABLE_CONSISTENCY_FINAL.md", REP), ("WORD_RENDER_AND_EQUATION_AUDIT.md", REP), ("EMA_JOURNAL_REQUIREMENTS_FINAL.md", REP),
 ("FINAL_PR_MERGE_RECOMMENDATION.md", REP), None, ("FINAL_SUBMISSION_GATE.md", REP)]
out = []
for i, s in enumerate(SRC, 1):
    if s is None: continue
    fn, d = s; dst = os.path.join(DL, fn if re.match(r"^\d\d_", fn) else f"{i:02d}_{fn}"); shutil.copy(os.path.join(d, fn), dst); out.append(dst)
for f in sorted(os.listdir(FIG)):
    if f.endswith((".png", ".pdf")) and f.split(".")[0] in ("GERMANY_CONTROLLED_CONTRAST", "THRESHOLD_OMISSION_CURVE", "CANDIDATE_AREA_OMISSION_TRADEOFF", "RICE_AREA_OMISSION_GEOGRAPHY", "CLASSIFICATION_DISAGREEMENT_MAP"):
        k = ["GERMANY_CONTROLLED_CONTRAST", "THRESHOLD_OMISSION_CURVE", "CANDIDATE_AREA_OMISSION_TRADEOFF", "RICE_AREA_OMISSION_GEOGRAPHY", "CLASSIFICATION_DISAGREEMENT_MAP"].index(f.split(".")[0]) + 1
        dst = os.path.join(DL, f"Fig{k}_{f}"); shutil.copy(os.path.join(FIG, f), dst); out.append(dst)
for f in sorted(os.listdir(os.path.join(SUB, "tables"))): dst = os.path.join(DL, f); shutil.copy(os.path.join(SUB, "tables", f), dst); out.append(dst)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
zs = os.path.join(DL, "EMA_FINAL_SUBMISSION_PACKAGE.zip")
with zipfile.ZipFile(zs, "w", zipfile.ZIP_DEFLATED) as z:
    for p in out:
        b = os.path.basename(p)
        if b.startswith(("01_", "02_", "03_", "Fig", "Table_")): z.write(p, b)
za = os.path.join(DL, "EMA_INDEPENDENT_AUDIT_EVIDENCE_PACKAGE.zip")
with zipfile.ZipFile(za, "w", zipfile.ZIP_DEFLATED) as z:
    for p in out:
        if not os.path.basename(p).startswith(("01_", "02_", "03_", "Fig")): z.write(p, os.path.basename(p))
    for f in ["KNOWN_ANSWER_TESTS_FINAL.csv", "OMISSION_ALIGNMENT_SENSITIVITY.csv", "CLASSIFICATION_STABILITY_PAIRS.csv", "RICE_OMISSION_BY_COUNTRY.csv", "EMA_THRESHOLD_SUMMARY.json"]: z.write(os.path.join(EMA, f), "evidence/" + f)
    z.write(os.path.join(SUB, "EMA_MANUSCRIPT_VALUES.json"), "evidence/EMA_MANUSCRIPT_VALUES.json"); z.write(os.path.join(REP, "REFERENCE_AUDIT_TABLE.csv"), "evidence/REFERENCE_AUDIT_TABLE.csv")
    for f in ["ema_threshold_sweep.py", "ema_figures.py", "build_ema_manuscript.py", "ema_known_answer_tests.py", "ema_reports.py", "ema_package.py"]: z.write(os.path.join(HERE, f), "code/" + f)
    z.write(os.path.join(ROOT, "modern_rice", "manuscript_ema", "manuscript_template.md"), "code/manuscript_template.md")
    for f in sorted(os.listdir(os.path.join(ROOT, "data", "raw_public", "crossref_ema"))): z.write(os.path.join(ROOT, "data", "raw_public", "crossref_ema", f), "evidence/crossref_ema/" + f)
for zz in (zs, za):
    names = zipfile.ZipFile(zz).namelist(); assert not any("literature" in n or n.endswith((".tif", ".asc", ".nc")) for n in names)
man = [dict(file=os.path.basename(p), bytes=os.path.getsize(p), sha256=sha(p)) for p in out + [zs, za]]
pd.DataFrame(man).to_csv(os.path.join(DL, "27_FINAL_FILE_MANIFEST_SHA256.csv"), index=False)
assert all(m["bytes"] > 0 for m in man)
print(len(man), "files"); print(pd.DataFrame(man)[["file", "bytes"]].to_string())
