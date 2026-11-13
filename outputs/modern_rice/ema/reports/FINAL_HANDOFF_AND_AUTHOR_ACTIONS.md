# Handoff (EM&A revision)

Branch `devin/1794546202-next-journal-retarget` (PR #2), evaluated head `3c6be210d019e400bd6501c2b6568c41cfa25ebc`.

## Rebuild order
```
python3 modern_rice/scripts/ag_grid_gates.py          # canonical AG layers (needs raw data, see AG ledger)
python3 modern_rice/scripts/ema_threshold_sweep.py
python3 modern_rice/scripts/ema_figures.py
python3 modern_rice/scripts/rpg_fetch_rice.py 2015 2020 2024   # network; 2010 îlots: see LEDGER.txt URL
python3 modern_rice/scripts/rpg_validation.py
python3 modern_rice/scripts/rpg_known_answer_tests.py
python3 modern_rice/scripts/build_ema_manuscript.py
python3 modern_rice/scripts/rpg_reports.py
python3 modern_rice/scripts/ema_known_answer_tests.py
python3 modern_rice/scripts/ema_reports.py
python3 modern_rice/scripts/ema_package.py
```
## What changed scientifically
- New: threshold sweep, omission geography, alignment/LOCO scenario ranges, classification stability. Correction: thermal pass at T* is 92.1% (AG printed 92.2% by double rounding).
- New (RPG revision): independent check against French RPG declared rice parcels (§2.6, §3.7, Fig. 6, Table 1 row, IGN 2026 reference); no previously reported number changed.
- Removed from narrative (kept in AG outputs, unchanged): Lower Danube hydrology, economic parity, food-supply risk portfolio.
- Not restored: Q99 1,100 m³/s, 24 m³/s, 94.2%/17.6%, Serbia potato claim, Romania risk-reduction claim.

## Verdict: SCIENTIFICALLY READY — AUTHOR ACTIONS PENDING
See `28_FINAL_SUBMISSION_GATE.md` for author actions.
