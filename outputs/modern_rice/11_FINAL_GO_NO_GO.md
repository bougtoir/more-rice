# 11 — Final GO / NO-GO (modern rice feasibility phase)

## Gate results
| Gate | Criterion | Result |
|---|---|---|
| A — public-data feasibility | Can the analysis be done on open data? | **PASS** — WorldClim + MapSPAM + FAOSTAT acquired, licensed, hashed, and used in a re-runnable pipeline |
| B — agronomic validity of crop/system comparison | Is the comparison fair and complete? | **PARTIAL-PASS** — energy comparison computed; revenue/labor/water-quant/GHG columns missing or flagged |
| C — external validation + uncertainty | Adequate? | **PARTIAL-PASS** — 95.8% SPAM coverage validation; but resampling-toward-target, no spatial-block CV, no daily cold-snap model |
| D — novelty | Clear delta vs ≥15 prior studies | **PARTIAL-PASS** — incremental integration, not a new method |
| E — concrete adoption-priority regions | Named regions under joint econ+water+env constraints | **FAIL** — candidates identified (Lower Danube/Balkans, steppe margins, Central Asia) but *conditional* on unfetched water/econ layers; spec requires them conditioned on all three |

## Verdict: **CONDITIONAL GO → no manuscript**
Feasibility of the research programme is established (Gate A firmly passes; the pipeline works and
validates). But the deliverable-level question — "name specific adoption-priority regions under
simultaneous economic/water/environmental constraints" — is **not yet answerable** at the spec's standard:
economic and water-availability layers are audited but not fetched, and the daily-weather sterility-risk
layer the physiologist requires is missing.

## What would flip to GO (all achievable on public data, no human blockers — unlike the medieval archive gap)
1. Fetch GMIA/AQUASTAT irrigated-area + water-stress layers; mask feasible_irrig cells by actual water.
2. Fetch ERA5-Land (or CHELSA daily) → reproductive cold-snap risk layer for marginal cells.
3. Fetch FAOSTAT producer prices + input aggregates → net-revenue column for candidate regions.
4. Spatial-block external validation on the suitability model.
5. Re-run → if ≥3 candidate regions survive all constraints → GO to Global Food Security /
   Agricultural Systems.

## Negative results already certified (worth keeping regardless)
- England/Germany/Nordics: biophysically infeasible across the entire modern-parameter grid — the
  medieval conclusion holds under modern technology; do not investigate further.
- Rice's edible-energy edge over wheat in feasible Europe is ~0.85–1.75× (milled basis), not the
  multi-fold advantage naive comparison suggests; France is at parity.
