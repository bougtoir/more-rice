# 06 — Crop Comparison Framework (multi-objective, no single score)

## Computed indicator 1: edible energy yield (FAOSTAT 2025-snapshot, latest year)
`CROP_YIELD_KCAL_COMPARISON.csv`, `KCAL_PER_HA_PIVOT.csv` (script: crop_comparison.py).
Units: yield kg/ha (FAOSTAT "Rice" = paddy, unmilled); kcal/ha = kg/ha × kcal/g×1000.
**Paddy caveat:** rice values are unmilled-equivalent; milled-edible ≈ 0.65× listed (documented in code).
Reported kcal/ha (paddy basis, ×10⁶):
- France: Rice 19.5 vs Wheat 20.3 — **parity**, not dominance
- Italy: 23.4 vs 12.4 — rice ~1.9×
- Spain: 25.7 vs 12.4 — ~2.1×
- Egypt: 33.3 vs 23.0 — ~1.4×
- Japan: 25.4 vs 15.1 — ~1.7×
- USA: 31.7 vs 11.7 — ~2.7×
- Bangladesh: 19.3 vs 12.8 — ~1.5×
- India: 15.7 vs 12.1 — ~1.3×
After the ~0.65 milled discount, *milled-edible* rice ≈ 0.85–1.75× wheat in these regions — a real but
modest edge, confirming H2.

## Indicators defined (computed where data allows; flagged missing otherwise)
1. Edible kcal/ha — DONE (above).
2. Protein/ha — partial (rice ~7% vs wheat ~12%: rice loses on protein basis) — flagged, not computed per country.
3. Net revenue — MISSING (needs prices+input costs; FAOSTAT prices audit deferred).
4. Labor productivity — MISSING (no harmonized labor data fetched).
5. Blue/green water — partial: rice rainfed-vs-irrigated split in suitability classes; consumptive-use
   numbers deferred (AQUASTAT/GMIA not yet fetched).
6. GHG — flagged: paddy CH4 is the known liability; AWD mitigation evidence noted (04 csv).
   Literature factors (Poore-Nemecek) — cited, not recomputed.
7. Yield variability — MISSING (needs detrended series; flagged for phase 4).
8. Capital/tech constraints — qualitative (barrier table 08).
9. Seasonality/rotation fit — qualitative + thermal-window overlap from rasters.

## Rule for conclusions
No single composite score. Pareto/threshold presentation: rice recommended only where it is not
dominated on (energy AND water AND GHG AND economics) by the local incumbent.
