# GDD gate — independent audit
Verdict: **PASS WITH LIMITATIONS**

Baseline commit 2d462b36ce119053502f98b6f5780b3e90b80432. Independent code: `delta_qc/indep/spatial_indep.py`, `delta_qc/indep/gdd_check.txt`, `ag_gdd_daily_vs_monthly.py`.

## Data definitions checked
- Variable: WorldClim 2.1 `tavg` monthly normals 1970–2000 at 2.5′, 5′, 10′ (files `wc2.1_<res>_tavg_MM.tif`); nodata −3.4e38 masked. Grid origin (−180, 90), 1/12° at 5′, EPSG:4326 — identical to SPAM 2010 and GMIA v5 grids (checked from raster headers), so no resampling is needed at 5′.
- Formula: GDD10 = Σ_month max(T̄_month − 10, 0) × days-in-window. Pipeline window 29 Apr–11 Sep = Apr 2 + May 31 + Jun 30 + Jul 31 + Aug 31 + Sep 11 = 136 days; calendar Jun–Sep = 122 days. No leap-year dependence (climatological normals).
- Point data: NASA POWER daily T2M 2000–2024; legacy window from pseudo-DOY (month×30.4+day) = 150–285 → ~29 Apr–11 Sep.

## Independent reconstruction
- Hokkaido calibration recomputed with separate code (window by rasterio bounds, SPAM RICE >0 as weights, lat/lon box 139.3–146.0 E, 41.35–45.6 N): rice area 113,968 ha; weighted P05 = 589.6 (pipeline), P01 = 487.9, P50 = 861.2 — matches the pipeline (589/487/859).
- Representative cells (rasterio.sample at POWER coordinates, WorldClim 5′, pipeline/calendar): Hokkaido point 645/718; Rhine 901/872; Saxony 808/786; Alsace 617/631; Berlin 938/888; Lower Danube 1498/1425.
- Rhine/Saxony reversal: reproduced from POWER daily data — pipeline window 957 and 969 > Hokkaido 903; Jun–Sep 931 and 935 < Hokkaido 941. It is a window artefact of a warm late season in Hokkaido versus warm spring in the Rhine/Saxony; it does not affect the grid-calibrated gate.

## Daily vs monthly approximation (same POWER daily data)
| point          | window               |   n_years |   gdd_daily |   gdd_monthly_mean |   bias_monthly_minus_daily |
|:---------------|:---------------------|----------:|------------:|-------------------:|---------------------------:|
| Hokkaido_JP    | calendar_Jun_Sep     |        25 |       941   |              938.3 |                       -2.8 |
| Hokkaido_JP    | pipeline_29Apr_11Sep |        25 |       903.2 |              873.9 |                      -29.4 |
| Rhine_DE       | calendar_Jun_Sep     |        25 |       931.1 |              930.7 |                       -0.3 |
| Rhine_DE       | pipeline_29Apr_11Sep |        25 |       956.8 |              947.4 |                       -9.5 |
| Saxony_DE      | calendar_Jun_Sep     |        25 |       935.2 |              931.8 |                       -3.4 |
| Saxony_DE      | pipeline_29Apr_11Sep |        25 |       969.2 |              956.3 |                      -12.9 |
| Alsace_FR      | calendar_Jun_Sep     |        25 |      1037   |             1035.9 |                       -1   |
| Alsace_FR      | pipeline_29Apr_11Sep |        25 |      1079.6 |             1073.3 |                       -6.4 |
| Berlin_DE      | calendar_Jun_Sep     |        25 |      1049   |             1048.5 |                       -0.5 |
| Berlin_DE      | pipeline_29Apr_11Sep |        25 |      1089.3 |             1082.5 |                       -6.8 |
| Loire_FR       | calendar_Jun_Sep     |        25 |      1100.6 |             1100.6 |                       -0   |
| Loire_FR       | pipeline_29Apr_11Sep |        25 |      1107.5 |             1104.4 |                       -3.1 |
| LowerDanube_RO | calendar_Jun_Sep     |        25 |      1668.3 |             1668.3 |                        0   |
| LowerDanube_RO | pipeline_29Apr_11Sep |        25 |      1750.4 |             1750.4 |                       -0.1 |

The monthly approximation underestimates daily accumulation most where monthly means are near 10 °C (April/September at Hokkaido). Because the bias is larger at the calibration site than at European points, the grid bound is slightly conservative (lower T* ⇒ more land passes; the effect is <30 GDD10, small relative to the 589 vs 900 contrast).

## Limitations retained
- 589 is the 5th percentile of current Hokkaido rice area on one gridded climatology; it is an empirical reference for one cultivation system (ultra-early japonica, heated nursery, transplanting), not a physiological threshold. Cold-water damage at booting, cultivar availability and management are not modelled.
- Climate periods differ (WorldClim 1970–2000 vs POWER 2000–2024); calibration is within-source.
- Spatial support: 5′ cells vs point cells; the point–grid offset is reported in the manuscript.

The 589 bound and the thermal-pass share do not depend on invalid aggregation: the Europe-wide pass share at T* differs by at most 4 percentage points across native 2.5′/5′/10′ and aggregated 30′/60′ resolutions.
