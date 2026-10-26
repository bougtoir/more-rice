# 07 — Pilot Results and Uncertainty

## What was computed
1. Global 10-arcmin suitability raster (`suitability_class_10m.tif`) — 4 classes + param-uncertain flag.
2. Validation vs SPAM2010 observed rice area: 95.8% ha-weighted coverage in feasible classes.
3. Regional cell summaries (`REGIONAL_SUITABILITY_SUMMARY.csv`).
4. FAOSTAT edible-energy comparison for 20 countries × 5 crops.

## Answers to the pre-registered questions (pilot level)
- **RQ1:** temperate non-traditional feasibility exists but is small and largely coincides with existing
  rice zones (Po, Camargue, Ebro, Rhône delta, Danube fringe). England/Germany/Nordics: infeasible across
  the parameter grid — the modern-era answer converges with the medieval result: ~1–2°C cultivar gain
  cannot bridge a ~4–6°C deficit.
- **RQ2:** where rice already grows in Europe, its *paddy* kcal/ha is ~1–2.7× wheat; *milled-edible*
  ≈ 0.85–1.75×. Real but modest; France is at parity.
- **RQ3:** in feasible-margin zones the fitting system is **irrigated lowland** (rainfed class = 0 cells in
  W. Europe: warm-season rain too low); AWD is a management option on top, not a category.
- **RQ4:** the sensitivity band (param_uncertain ≈ 54.6k cells) is where variety/AWD/irrigation gains could
  expand feasibility — mostly monsoon-margin tropics/subtropics, not N. Europe.
- **RQ5:** the interesting frontier cells for barrier analysis are temperate-margin zones where class≥1 but
  no SPAM rice: S. Japan fringe case aside, the clearest candidates are in **Eastern Europe (Lower Danube/
  Balkans), S. Ukraine/Russia steppe margins, central Chile, S. Brazil/Uruguay, parts of C. Asia** — pending
  finer analysis.
- **RQ6:** rotation insertion (summer rice after winter cereal) is the plausible form for marginal zones —
  consistent with existing Po Valley practice (rice+wheat/soy rotations).

## Uncertainty inventory (honest)
- 10-arcmin grid is coarse: micro-basins and irrigation-district boundaries are lost → pilot only.
- Monthly means, not daily: cold-snap sterility risk (the real killer at margins) is not modeled —
  *systematically optimistic* for marginal zones.
- Rain proxy uses warmest-3-month prec; real water balance needs ET0 + soil storage.
- Validation is circular-leaning (climate-trained expectations vs climate-driven actual production);
  a proper spatial-block external validation is deferred.
- Economic/GHG/water columns are qualitative flags, not computed values.
- "No SPAM rice" ≠ "can't grow rice" — institutional non-adoption confounds the negative class
  (spec §5 warning honoured: non-cultivation is NOT labeled unsuitable).
