# 05 — Global Suitability Feasibility (pilot)

## Method (no single threshold)
10-arcmin WorldClim 2.1: consecutive-month heat rules (parameter grid: 3–4 months ≥18°C or ≥20°C),
GDD10 ≥1800, ≥4 frost-free months; rain proxy = precipitation over each cell's 3/4 warmest months
(rainfed ≥300mm). Classes: `infeasible / marginal / feasible_irrig_dependent / feasible_rainfed`, plus a
`param_uncertain` flag where the 4 thermal combos disagree. Script: `modern_rice/scripts/suitability_pilot.py`.
Observed suitability (SPAM rice cells) vs modelled potential kept strictly separate (spec §5).

## Validation vs observed production (SPAM2010)
Share of world rice harvested area (ha-weighted) falling in each class:
- feasible_rainfed **62.8%**, feasible_irrig_dependent **33.0%**, marginal 0.16%, infeasible **4.0%**
→ ~95.8% of real rice area inside feasible classes at 10-arcmin. The 4% residue is expected error
(resampling, cool-plateau rice, boundary cells) — acceptable for a pilot; not calibration-grade.

## Regional summary (cells, 10-arcmin)
- **Europe_W:** infeasible 30,663 / marginal 507 / feasible_irrig 639 / rainfed 0. Feasible cells cluster
  on Po Valley, Rhône delta, Iberian coast — i.e., *where rice already grows*. Northern Europe: essentially
  none beyond marginal.
- **EastAsia/SEAsia/SAsia:** large rainfed+irrigated feasible areas, matching production.
- **NAmerica:** 9,481 feasible_irrig + 6,391 rainfed cells (California, Gulf, Mississippi valley — real).
- **WAfrica/SubSahara:** large feasible areas — consistent with the actual ongoing rice expansion.
- **param_uncertain band** ~54,580 cells: mostly monsoon-margin and temperate-margin zones — honest
  uncertainty region.

## Key finding for RQ1
Non-traditional temperate feasibility is **real but geographically tiny**: in W. Europe the feasible band
essentially coincides with existing rice zones (Po, Camargue, Ebro). The *novel* marginal zones are small
(S. England micro-basins? none at 10-arcmin; Danube delta fringe; Lower Rhône). England/Germany/Nordics
fail thermal rules across the whole parameter grid — consistent with the medieval-era result but now
established on modern normals and modern variety parameters (variety improvement moves the floor ~1–2°C
in effective terms, not the ~4°C needed).
