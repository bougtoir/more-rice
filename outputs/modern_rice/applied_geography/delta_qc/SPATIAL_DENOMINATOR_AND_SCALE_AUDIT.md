# Spatial gate — denominator, domain and scale audit
Verdict: **FAIL → REPAIRED → PASS WITH LIMITATIONS**

## Defect found
The baseline (`2d462b3`) computed all "European" shares over the rectangle 11°W–45°E, 34°N–71.5°N with `valid = finite(GDD) & incumbent>0`, without a country mask. The rectangle contains North Africa, Anatolia, the Caucasus and western Russia. Independent recomputation (own code from raw rasters) shows that 21.3 Mha of the 107.1 Mha denominator lies in non-European countries, with 33% of it in the thermal+infrastructure class, inflating the European infrastructure share.

## Repair
`ag_grid_gates.py` now rasterises Natural Earth 1:50 m countries with CONTINENT = Europe, excluding Russia (truncated by the 45°E edge), and applies the mask to the cascade, validation, scale, threshold-curve, window and AEI sensitivities. The dependency chain (grid gates → figures → manuscript build) was rerun.

## Numerators and denominators (incumbent arable = SPAM 2010 harvested area of wheat+maize+barley+potato, all technologies, ha summed per 5′ cell; no pixel-area weighting is needed because SPAM values are already hectares; cell areas are used only to convert GMIA hectares to an AEI share)
| domain                         |   incumbent_Mha |   thermal_pass_share |   thermal_aei_share |   aei_share_among_thermal_pass |
|:-------------------------------|----------------:|---------------------:|--------------------:|-------------------------------:|
| rectangle_-11_45E_34_71.5N     |          107.12 |               0.9421 |              0.176  |                         0.1868 |
| Europe_excl_Russia (primary)   |           69.7  |               0.9215 |              0.1601 |                         0.1737 |
| Europe_incl_Russia_west_of_45E |           85.62 |               0.9337 |              0.1381 |                         0.1479 |
| EU27                           |           46.59 |               0.931  |              0.2023 |                         0.2173 |

Primary domain: thermal pass = 64.2 Mha / 69.7 Mha = 92.2%; thermal + AEI≥10% = 11.2 Mha / 69.7 Mha = 16.0%; conditional on thermal pass = 17.4%.
Independent reproduction (separate code, `delta_qc/indep/spatial_indep.txt`) of rectangle values: 107.12 Mha, 94.2%, 17.6% (exact); Europe-excluding-Russia values match the repaired pipeline.

## Other checks
- Grids aligned: SPAM, GMIA (ASCII, xll −180, yll −90, 1/12°) and WorldClim 5′ share origin and resolution; the SPAM padding branch is never triggered.
- Nodata: SPAM −1 → 0; WorldClim nodata → NaN and excluded through `isfinite(GDD)`; GMIA missing → 0 (no infrastructure).
- Coastline: country assignment by rasterised polygon centre; coastal cells partially outside polygons are excluded (small).
- Scale: 2.5′/5′/10′ native and 30′/60′ aggregated sensitivity retained; at T* the Europe-wide share changes by ≤4 points across scales.
- AEI cut-off 5/10/20% reported. AEI is area *equipped* for irrigation c. 2005–2010: it does not establish water availability, permits, delivery capacity, field levelling for paddy, economic feasibility or environmental constraints. The manuscript wording uses "infrastructure presence" and "candidate for next-stage assessment" only.
