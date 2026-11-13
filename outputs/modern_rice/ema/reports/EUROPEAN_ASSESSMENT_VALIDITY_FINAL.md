# European assessment validity

| Check | Result |
|---|---|
| Combined gate subset of thermal gate (all T) | PASS: nan |
| Area weighting differs from raw cell counts (weights are used) | PASS: area-weighted 92.146% (CSV 92.146), unweighted cell share 77.854% |
| Nodata: incumbent/rice area in domain cells without climate data | PASS: incumbent 0 ha, rice 0 ha excluded (NaN GDD10) |
| Geographic mask: Russia, Türkiye, Kazakhstan, Georgia, Azerbaijan, Armenia, Cyprus excluded | PASS: 40 countries in domain |
| Denominator 69.7 Mha (independent of ag_grid_gates.py) | PASS: 69697892 ha vs AG cascade 69697894 ha |
| Thermal pass at T* (exact value; AG manuscript printed 92.2 via double rounding) | PASS: 92.1465% -> 92.1% at one decimal; AG used round(0.9215 [4 d.p.],1)=92.2 |
| Thermal + infrastructure share 16.0% | PASS: 16.010% |
| Germany endpoints reproduced from sweep | PASS: 96.572 / 3.233 vs [96.57, 3.23] |
| Transcontinental countries | Assigned by Natural Earth CONTINENT; Türkiye, Cyprus, Georgia, Azerbaijan, Armenia, Kazakhstan are Asia and excluded; Russia excluded explicitly (truncated by 45°E). |
| Pixel-area weighting | Not applied to MapSPAM hectares (already area units). Cell areas (WGS84 authalic sphere) used only for AEI share. |
| Irrigation layer | GMIA v5 area equipped for irrigation (ha, ~2005), share ≥ 10% of cell. Not water allocation, not rice-specific field infrastructure, not feasibility. |
| Rounding correction | AG manuscript printed 92.2% (double rounding of 0.9215). Exact 92.146% → **92.1%** in EM&A. Not a scientific change. |

## Domain sensitivity (from AG canonical output)
| domain | incumbent_Mha | thermal_pass_share | thermal_aei_share | aei_share_among_thermal_pass |
|---|---|---|---|---|
| rectangle_-11_45E_34_71.5N | 107.12 | 0.9421 | 0.176 | 0.1868 |
| Europe_excl_Russia (primary) | 69.7 | 0.9215 | 0.1601 | 0.1737 |
| Europe_incl_Russia_west_of_45E | 85.62 | 0.9337 | 0.1381 | 0.1479 |
| EU27 | 46.59 | 0.931 | 0.2023 | 0.2173 |
