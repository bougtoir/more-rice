# Applied Geography manuscript (modern rice)

**Title:** Spatial constraints on transferring rice cultivation systems beyond traditional growing regions: A multi-scale assessment of thermal suitability and irrigation infrastructure

`manuscript_template.md` holds the text with `{placeholders}`; `../scripts/build_ag_manuscript.py` fills every number from the canonical analysis outputs in `outputs/modern_rice/applied_geography/` and writes the submission files to `outputs/modern_rice/applied_geography/submission/`.

## Rebuild order

```bash
cd modern_rice/scripts
python3 ag_grid_gates.py                              # European gates, T*, scale/threshold/domain sensitivity
python3 ag_point_window_sensitivity.py; python3 ag_gdd_daily_vs_monthly.py
python3 ag_danube_demand.py; python3 ag_danube_lowflow.py   # needs private EStreams archive (see ledger)
python3 ag_risk_portfolio_v2.py
python3 ag_germany_decomposition.py; python3 GERMANY_THERMAL_CONTRAST_INDEPENDENT_CHECK.py; python3 ag_germany_report.py
python3 ag_europe_denominator_audit.py; python3 ag_prior_work_matrix.py; python3 ag_final_independent_audit.py
python3 ag_figures.py; python3 build_ag_manuscript.py
python3 ag_evidence_package.py; python3 ag_final_qc_reports.py; python3 ag_individual_downloads.py
```

Raw inputs are listed with URL, UTC time, size, SHA-256 and licence in `modern_rice/data/RAW_ACQUISITION_LEDGER_2026-11-08.csv`. Inputs that may not be redistributed (EStreams/GRDC; WorldClim, GMIA bulk files) are archived privately and are not in this repository.
