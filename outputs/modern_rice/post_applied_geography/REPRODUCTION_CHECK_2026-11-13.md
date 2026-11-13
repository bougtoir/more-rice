# Reproduction check after the Applied Geography decision (2026-11-13)

Raw inputs restored from the private release `bougtoir/wip@more-rice-raw-2026-11-08` into `modern_rice/data/raw/` (gitignored). All ledger files present in the release matched their SHA-256 in `RAW_ACQUISITION_LEDGER_2026-11-08.csv`; NASA POWER, EStreams and Natural Earth members were restored by extracting their archive files.

Scripts rerun from `modern_rice/scripts/` (all exit 0): ag_grid_gates.py, ag_point_window_sensitivity.py, ag_gdd_daily_vs_monthly.py, ag_danube_demand.py, ag_danube_lowflow.py, ag_risk_portfolio_v2.py, ag_germany_decomposition.py, GERMANY_THERMAL_CONTRAST_INDEPENDENT_CHECK.py, ag_germany_report.py, ag_europe_denominator_audit.py, ag_final_independent_audit.py.

Result: `git status` shows no modified tracked output under `outputs/modern_rice/applied_geography/`, i.e. every canonical CSV/JSON is byte-identical to main (4cd8d5e). Independent audit: all claims MATCH (Orsova n = 71, median 2,749 m³/s, P10 2,199, lowest 1,410; gross demand 11.7% / 22.8%).
