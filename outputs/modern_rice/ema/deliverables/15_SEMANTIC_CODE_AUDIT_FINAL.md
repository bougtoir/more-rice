# Semantic code audit (EM&A scripts)

Scripts: `ema_threshold_sweep.py`, `ema_figures.py`, `build_ema_manuscript.py`, `ema_known_answer_tests.py`, `ema_reports.py`.

| Aspect | Specification | Implementation | Status |
|---|---|---|---|
| Estimand C(T) | incumbent-area-weighted share with GDD10 ≥ T | `inc[valid & (g5 >= T)].sum() / inc[valid].sum()` | OK |
| Estimand O(T) | rice-area-weighted share with GDD10 < T | `rice[rmask & ~(g5 >= T)].sum() / rice[rmask].sum()` | OK |
| Sign / boundary | pass is ≥ | `g5 >= T`; equation (1) uses ≥, (2) uses < | OK (KAT 4–6) |
| Units | GDD10 °C·d; area ha; output % and Mha | consistent; Mha = ha/1e6 | OK |
| Weights | harvested ha, no extra pixel-area weighting | as specified; cell area only for AEI share | OK (KAT 7) |
| Window | 2 d Apr + May–Aug + 11 d Sep | `WIN_PIPE` identical to `ag_grid_gates.py` | OK (Germany endpoints reproduced, KAT 13) |
| Grid support | 5′ native; 2.5′ via 2×2 sub-cell fraction; 10′ via 2×2 replication | block_mean / repeat | OK; 2.5′ majority rule (≥0.5) for stability, fraction for omission |
| Joins | all layers on identical 5′ window; Natural Earth rasterised with same transform | `from_origin(W, N, 1/12, 1/12)` | OK (denominator matches AG to 2 ha, KAT 10) |
| Missingness | NaN GDD10 excluded from both numerator and denominator | `np.isfinite(g5)` in masks | OK; 0 ha affected (KAT 8) |
| Inference unit | no independent-cell inference | scenario ranges only | OK (KAT 21) |
| Hardcoding | none of headline values in template/builder | placeholders from CSV/JSON | OK (KAT 22–23) |
| Edge artefact | `np.roll` shift wraps at window edge | rice at window edges is zero (no rice at 11°W/45°E/71.5°N edges); effect nil | Noted |
| Known defect fixed | AG 92.2% double rounding | EM&A uses exact share → 92.1% | Corrected (documented) |

Known-answer tests: 24/24 PASS (`KNOWN_ANSWER_TESTS_FINAL.md`).
