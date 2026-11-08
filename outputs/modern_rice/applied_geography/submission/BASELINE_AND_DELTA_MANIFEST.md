# Baseline and delta manifest
- Repository: bougtoir/more-rice; PR #1 (not merged); branch `devin/1794122489-applied-geography-retarget`
- Baseline for this delta QC: `2d462b36ce119053502f98b6f5780b3e90b80432` (PR #1 head when QC started); main base `6202551`
- Canonical Agricultural Systems manuscript `outputs/modern_rice/manuscript/MANUSCRIPT_FINAL_ORDER_CORRECTED.docx`: untouched (verify with `git diff 2d462b3 -- outputs/modern_rice/manuscript/`).
- Package paths: `outputs/modern_rice/applied_geography/submission/` (submission files, `figures/`), `.../FINAL_INDIVIDUAL_DOWNLOADS/` (numbered files + SHA-256 manifest), `.../delta_qc/` (audits; `indep/` = independent check code and logs).

## Changed code (dependency chain rerun)
| Script | Change | Rerun downstream |
|---|---|---|
| `ag_grid_gates.py` | Europe mask (Natural Earth CONTINENT=Europe, excl. Russia); `EUROPE_DOMAIN_TOTAL`; `EUROPE_DOMAIN_SENSITIVITY.csv` | grid outputs → figures → manuscript |
| `ag_risk_portfolio_v2.py` | paddy→milled factor 0.67 | risk outputs → Figure 5, Table 3 → manuscript |
| `ag_gdd_daily_vs_monthly.py` (new) | monthly-mean vs daily GDD10 bias from POWER | manuscript limitations |
| `build_ag_manuscript.py` | new placeholders; 80% caption; first-person cover letter; OMML equation; T* rendering bug; black headings | all submission files |
| `manuscript_template.md` | domain, Q99 conditional wording, gross/net water, milling, 80%, Savoini et al. reference, highlights | all submission files |
| `ag_delta_qc_reports.py`, `ag_individual_downloads.py` (new) | audits, downloads, manifest, ZIP | — |

Not rerun (unchanged inputs): raw-data acquisition, Danube demand script, point-GDD script.

## Old → new headline numbers
| Quantity | Baseline 2d462b3 | Now |
|---|---|---|
| Denominator | 107.1 Mha (rectangle incl. N Africa/Anatolia) | 69.7 Mha (Europe excl. Russia) |
| Thermal pass | 94.2% | 92.2% |
| Thermal + AEI ≥10% | 17.6% | 16.0% (17.4% of thermal-pass land) |
| Kazakhstan CI excl. 0 | 79% of configs | 58% |
| Romania CI excl. 0 | 42% | 17% |
| Q99 1,100 m³/s | stated as fact | reported statistic, source unverified |
| Shortfall threshold (text) | 90% | 80% (= code) |
