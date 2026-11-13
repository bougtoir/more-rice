# Threshold sweep: methods and results

## Fixed specification
- Climate surface: WorldClim 2.1 tavg, 1970–2000, 5′; GDD10 over the pipeline window (2 d April, May, June, July, August, 11 d September ≈ 29 Apr–11 Sep).
- Domain: Natural Earth 1:50 m, CONTINENT == Europe, ADMIN != Russia, rasterised on the 5′ grid (11°W–45°E, 34°N–71.5°N).
- Cropland weights: MapSPAM 2010 v2.0 harvested area, wheat+maize+barley+potato, all technologies (69.7 Mha). Rice weights: MapSPAM 2010 rice harvested area, all technologies (501.1 kha in 20,356 cells).
- Thresholds: 0–1800 GDD10 step 25 plus named references; pass = GDD10 ≥ T; omitted rice = rice area in cells with GDD10 < T.
- Script: `modern_rice/scripts/ema_threshold_sweep.py`; figures: `ema_figures.py`. All values below are read from `THRESHOLD_OMISSION_CURVE.csv`.

## Not computed, and why
Specificity, precision, F1, AUC and ROC are not computed: non-rice cropland is not a verified negative (rice absence is mostly due to water, soils, markets and institutions), so commission cannot be estimated. The curve is an omission–candidate-area trade-off, not an ROC curve.

## Named references
| threshold_gdd10 | reference_label | cropland_pass_pct | cropland_thermal_aei_pct | germany_cropland_pass_pct | rice_omitted_ha | rice_omitted_pct | rice_omitted_pct_incumbent_cells | rice_omitted_pct_2p5m_subcell |
|---|---|---|---|---|---|---|---|---|
| 487.0 | Hokkaido SPAM rice-area P01, WorldClim 5' (grid) | 97.269 | 16.502 | 99.669 | 4936.6 | 0.985 | 0.535 | 0.991 |
| 589.0 | T*: Hokkaido SPAM rice-area P05, WorldClim 5' (grid; primary) | 92.146 | 16.01 | 96.572 | 6858.0 | 1.369 | 0.875 | 1.329 |
| 637.0 | Hokkaido SPAM rice-area P10, WorldClim 5' (grid) | 88.442 | 15.761 | 91.429 | 7881.9 | 1.573 | 1.055 | 1.54 |
| 750.0 | WorldClim 5' cell at the Hokkaido POWER point (grid point) | 76.46 | 15.191 | 49.968 | 10614.0 | 2.118 | 1.545 | 2.162 |
| 767.0 | POWER Hokkaido point 1981-2000 monthly formula | 74.083 | 15.045 | 41.502 | 10994.7 | 2.194 | 1.6 | 2.272 |
| 832.0 | POWER Hokkaido point 1981-2000 daily | 63.127 | 14.659 | 14.695 | 13249.4 | 2.644 | 2.041 | 2.71 |
| 859.0 | Hokkaido SPAM rice-area P50, WorldClim 5' (grid) | 59.393 | 14.515 | 9.007 | 14700.3 | 2.934 | 2.33 | 2.879 |
| 900.0 | ~900: rounded POWER Hokkaido point 2000-2024 daily (earlier numerical reference) | 54.935 | 14.25 | 3.233 | 16138.1 | 3.221 | 2.586 | 3.226 |
| 903.0 | POWER Hokkaido point 2000-2024 daily (unrounded) | 54.627 | 14.222 | 3.1 | 16209.1 | 3.235 | 2.6 | 3.247 |
| 1036.0 | All SPAM rice north of 35N, rice-area P05 (grid) | 42.7 | 12.63 | 0.122 | 22275.6 | 4.446 | 3.748 | 4.586 |
| 1076.0 | European SPAM rice-area P05 (in-sample for Europe; diagnostic only) | 39.103 | 12.041 | 0.0 | 25051.6 | 5.0 | 4.282 | 5.144 |

## Interpretation
- Monotonicity is mechanical on a fixed surface (KAT 1–2). The informative feature is the **location** of the rise: European rice-area-weighted GDD10 P05 = 1,076, P50 = 1,413, so omission stays ≤5% up to 1,076 and first exceeds 10% at 1,225.
- Between T* = 589 and 900, candidate area falls by 37.2 pp (25.9 Mha) while omission rises by 1.9 pp (1.37% → 3.22%). Germany falls by 93.3 pp; MapSPAM maps no rice in Germany.
- Grid-shift range at T*: 1.32–2.53%; LOCO range at T*: 0.88–1.80%; at 900: 2.12–4.23%. These scenario ranges overlap the T*→900 omission change, so the presence-only check cannot rank T* against 900.
- Conclusion: the sweep is informative beyond monotonicity in one specific sense: it shows that mapped rice area constrains only thresholds above about the European rice P05 and is uninformative in the range where the competing Hokkaido references differ. It does not validate T*.
