# Independent auditor README

Repository: https://github.com/bougtoir/more-rice (PR #1, branch `devin/1794122489-applied-geography-retarget`).

## 1. Final manuscript
* `outputs/modern_rice/applied_geography/submission/APPLIED_GEOGRAPHY_MANUSCRIPT_FINAL.docx` (anonymized, figures separate) and `..._INLINE_REVIEW_COPY.pdf` (figures inline).
* Text source: `modern_rice/manuscript_ag/manuscript_template.md`; every number is a `{placeholder}` filled by `modern_rice/scripts/build_ag_manuscript.py` from analysis outputs (`submission/MANUSCRIPT_NUMBERS.json` records the values used).

## 2. Main claims → evidence
`CLAIM_TO_EVIDENCE_MATRIX.csv` (claim, manuscript location, canonical result ids, evidence files, independent check id). Canonical values: `CANONICAL_RESULTS_REGISTRY.csv`, read from the output files by `ag_evidence_package.py`.

## 3. Source data
`DATA_PROVENANCE_AND_ACCESS_MANIFEST.csv` lists every raw file (URL, UTC retrieval time, bytes, SHA-256, licence, private archive asset). Raw data are not in the public repository. Public sources (WorldClim, SPAM, GMIA, FAOSTAT, NASA POWER, Natural Earth) can be re-downloaded from the listed URLs and checked against the SHA-256 values. Hydrological inputs (EStreams v1.4, GRDC-derived, CC BY-NC; GRDC terms) are archived privately (`bougtoir/wip` release `more-rice-raw-2026-11-08`) and must be obtained from EStreams/GRDC by the auditor.

## 4. Verifying key calculations (independent code; no project imports)
| Claim | Independent script | Output |
|---|---|---|
| T*, Germany 96.6%/3.2%, decomposition endpoints | `modern_rice/scripts/GERMANY_THERMAL_CONTRAST_INDEPENDENT_CHECK.py` | `GERMANY_THERMAL_CONTRAST_INDEPENDENT_CHECK.json` |
| Europe denominator and gate counts | `modern_rice/scripts/ag_europe_denominator_audit.py` | `EUROPE_SPATIAL_GATE_COUNTS.csv` |
| Demand, low-flow ratios, risk baselines, KATs | `modern_rice/scripts/ag_final_independent_audit.py` | `CLAIM_IMPLEMENTATION_INDEPENDENCE_MATRIX.csv`, `KNOWN_ANSWER_TEST_REPORT.md` |
Shared assumptions that these checks do not test are stated in each report (e.g. GDD10 definition, Hokkaido box, P05 choice, AEI threshold).

## 5. Reproducing changed figures
`python3 modern_rice/scripts/ag_germany_decomposition.py && python3 modern_rice/scripts/ag_figures.py` regenerates Figure 3 (panel d new). Provenance and SHA-256 of every artwork file: `FIGURE_TABLE_PROVENANCE_MATRIX.csv`. Full rebuild order: `modern_rice/manuscript_ag/README.md`.

## 6. Private-data limitations
Hydrological statistics (Orsova/Bazias) cannot be reproduced from public files alone; the per-year derived table `HYDROLOGICAL_LOW_FLOW_BY_YEAR.csv` is public and the independent check recomputes the summary statistics from it. No flow-duration Q99 is computed because daily series are not redistributable.

## 7. Unresolved issues
See `26_HOSTILE_APPLIED_GEOGRAPHY_REVIEW_FINAL.md` (residual reviewer risks) and `30_FINAL_SUBMISSION_GATE.md` (author actions: e-mail, date, suggested reviewers, Editorial Manager subscription choice and login-only checklist).
