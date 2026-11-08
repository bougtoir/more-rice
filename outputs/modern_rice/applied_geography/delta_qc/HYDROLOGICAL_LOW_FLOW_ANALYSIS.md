# Lower Danube observed low-flow analysis
Script: `modern_rice/scripts/ag_danube_lowflow.py` (seed 20261108). Inputs: EStreams v1.4 monthly minimum and mean of daily discharge, and yearly minimum / minimum 7-day discharge (mm/d), stations Orsova (GRDC 6742200, 1920–1990) and Bazias (GRDC 6742201, 1991–2008). Converted to m³/s with the official GRDC catchment area (Orsova 576,232 km²); using the EStreams-delineated area lowers all flows by 1.3%.

## Definitions
- **Jun–Sep minimum daily discharge (per year)**: minimum of the June, July, August and September monthly minima of daily mean discharge; years with all four months present only (Orsova 71 years; Bazias 18). The window matches the 120-day June–September demand scenario.
- **Annual minimum daily / 7-day discharge**: EStreams yearly indices (calendar years).
- Across-year summaries: median and 10th percentile (numpy linear, Hyndman–Fan type 7; P10 alternative estimators reported in the CSV, range 2,123–2,199 m³/s). 95% CIs: 2,000 bootstrap resamples of whole years (daily serial correlation is avoided by resampling annual values).
- **Not computed**: flow-duration Q99 (discharge equalled or exceeded on 99% of days) and the distribution of daily demand/discharge ratios — both need the daily series, which is not openly available (GRDC request text in CT_UPT_SOURCE_RESOLUTION.md). Return-period estimates were not fitted.

## Results (Orsova)
| period                       |   n_years | statistic                                      |   value_m3s |   ci95_lo |   ci95_hi |   net_pct |   gross_pct |
|:-----------------------------|----------:|:-----------------------------------------------|------------:|----------:|----------:|----------:|------------:|
| all                          |        71 | JunSep_min_daily_median                        |        2749 |      2473 |      2858 |       8.8 |        11.7 |
| all                          |        71 | JunSep_min_daily_P10                           |        2199 |      1879 |      2269 |      11   |        14.6 |
| all                          |        71 | JunSep_min_daily_lowest                        |        1410 |       nan |       nan |      17.1 |        22.8 |
| all                          |        71 | JunSep_mean_median                             |        5051 |      4691 |      5400 |       4.8 |         6.4 |
| all                          |        71 | annual_min_daily_median                        |        2239 |       nan |       nan |      10.8 |        14.4 |
| 1920-1971 (pre-Iron Gates I) |        52 | JunSep_min_daily_median                        |        2802 |      2534 |      3002 |       8.6 |        11.5 |
| 1920-1971 (pre-Iron Gates I) |        52 | JunSep_min_daily_P10                           |        2241 |      2077 |      2371 |      10.8 |        14.3 |
| 1920-1971 (pre-Iron Gates I) |        52 | JunSep_min_daily_lowest                        |        1813 |       nan |       nan |      13.3 |        17.7 |
| 1920-1971 (pre-Iron Gates I) |        52 | JunSep_mean_median                             |        5094 |      4603 |      5527 |       4.7 |         6.3 |
| 1972-1990 (regulated)        |        19 | JunSep_min_daily_median                        |        2470 |      2260 |      2838 |       9.8 |        13   |
| 1972-1990 (regulated)        |        19 | JunSep_min_daily_P10                           |        1854 |      1410 |      2310 |      13   |        17.3 |
| 1972-1990 (regulated)        |        19 | JunSep_min_daily_lowest                        |        1410 |       nan |       nan |      17.1 |        22.8 |
| 1972-1990 (regulated)        |        19 | JunSep_mean_median                             |        4859 |      4512 |      5459 |       5   |         6.6 |
| all                          |        71 | annual_7day_min_median                         |        2381 |       nan |       nan |      10.1 |        13.5 |
| all                          |        71 | annual_7day_min_P10                            |        1803 |       nan |       nan |      13.4 |        17.8 |
| all                          |        71 | annual_7day_min_lowest                         |        1362 |       nan |       nan |      17.7 |        23.6 |
| all                          |        71 | annual_min_daily_median                        |        2239 |       nan |       nan |      10.8 |        14.4 |
| all                          |        71 | annual_min_daily_P10                           |        1680 |       nan |       nan |      14.4 |        19.1 |
| all                          |        71 | annual_min_daily_lowest                        |        1074 |       nan |       nan |      22.4 |        29.9 |
| all                          |        71 | JunSep_min_daily_P10_estimator_linear          |        2199 |       nan |       nan |      11   |        14.6 |
| all                          |        71 | JunSep_min_daily_P10_estimator_lower           |        2199 |       nan |       nan |      11   |        14.6 |
| all                          |        71 | JunSep_min_daily_P10_estimator_median_unbiased |        2148 |       nan |       nan |      11.2 |        15   |
| all                          |        71 | JunSep_min_daily_P10_estimator_weibull         |        2123 |       nan |       nan |      11.4 |        15.1 |

Gross abstraction (321.5 m³/s) exceeded 10% of the Jun–Sep minimum in 76.1% of years, 20% in 1.4% and 30% in none. Bazias (1991–2008) gives a median Jun–Sep minimum of 2,534 m³/s and lowest 1,490 m³/s.

## Interpretation limits
- Discharge at a mainstem gauge is not allocable irrigation water: navigation, Iron Gates hydropower, environmental flows, existing abstractions and transboundary agreements have prior claims.
- Demand is a seasonal-average equivalent; peak (puddling) rates are higher and are not modelled. No daily demand curve was constructed.
- Record ends in 1990; 19 years post-dam. Upstream regulation, climate change and riverbed incision since 1990 are not represented.
- The ratios are descriptive; they do not establish feasibility.
