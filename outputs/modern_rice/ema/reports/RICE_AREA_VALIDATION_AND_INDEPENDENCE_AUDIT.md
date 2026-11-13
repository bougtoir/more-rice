# Rice-area reference data: validation role and independence audit

| Item | Finding |
|---|---|
| Dataset | MapSPAM 2010 v2.0 (IFPRI, 2019; Yu et al., 2020); Harvard Dataverse doi:10.7910/DVN/PRFF8V, file 3985008; CC BY 4.0; local `modern_rice/data/raw/spam2010v2r0_global_harv_area.geotiff.zip` (ledger in AG data ledger). |
| Variable | `H` = harvested area (ha), technology `A` (all) for the sweep; `I` (irrigated) used only for description. Harvested area counts multiple cropping; it is not physical paddy area. |
| Nature | Modelled allocation of national/subnational statistics to 5′ cells using cropland extent, irrigation maps and crop suitability (Yu et al., 2020). Not field observations, not remote-sensing paddy maps. |
| Grid / alignment | 5′ global grid, origin (−180, 90); rows padded to 2160 (Antarctic rows absent in file); negative/nodata set to 0. Same grid as WorldClim 5′ and GMIA 5′. |
| Nodata | Domain cells with rice > 0 but no WorldClim value: incumbent 0 ha, rice 0 ha excluded (NaN GDD10). |
| Calibration vs evaluation | T* calibrated on MapSPAM rice in Hokkaido (114 kha); evaluated on MapSPAM rice in Europe. Out of region, **not out of product**. |
| Circularity: infrastructure gate | MapSPAM irrigated technology and GMIA share irrigation-statistics lineage. 79.4% of European rice is MapSPAM-irrigated and 81.1% lies in cells with AEI ≥10%; this agreement is **not** used as validation. Note: MapSPAM classifies all French, Romanian and Hungarian rice as non-irrigated, which is agronomically implausible (Camargue, Danube paddies) and illustrates allocation error. |
| Circularity: thermal gate | MapSPAM suitability priors include climate; allocation can place rice in cells MapSPAM deems suitable. Low omission is therefore partly expected by construction and is not independent evidence of thermal adequacy. |
| Omission geography at T* | 6,858 ha in 485 cells, 66 clusters (8-connected), top-5 clusters 80%; Italy+France 85%; 96% of omitted cells (holding 64% of omitted area) have rice <1% of cell area → allocation fringe. 9 omitted cells have GDD10 = 0 (high-Alpine), holding 74.0 ha. |
| Legacy 0.87% | Equals omission restricted to rice cells with incumbent arable land; the all-rice-cell value used in EM&A is 1.37%. 4.6 kha of rice lie in cells without incumbent crops. |
| Negatives | None independent. Non-rice cropland cannot serve as true negatives. |
| Inference unit | Cells are spatially autocorrelated and share allocation inputs; no cell bootstrap. Scenario ranges: 8 one-cell shifts, 3×3 rule, 2.5′ sub-cell, 10′ native, leave-one-country-out (countries >1000 ha rice). |

## Country table (omitted ha at T*, 900, 1100)
| country | rice_mapped_ha | rice_weighted_gdd10_median | rice_irrigated_tech_share | omitted_ha_T589 | omitted_ha_T900 | omitted_ha_T1100 |
|---|---|---|---|---|---|---|
| Italy | 244162.4 | 1380.0 | 0.775 | 3146.4 | 7498.2 | 10926.3 |
| Spain | 121199.5 | 1634.0 | 0.987 | 9.0 | 59.6 | 558.7 |
| Greece | 31708.0 | 1734.0 | 1.0 | 0.0 | 0.4 | 167.3 |
| Portugal | 29185.6 | 1457.0 | 0.95 | 0.0 | 0.0 | 1377.0 |
| Ukraine | 23653.2 | 1209.0 | 0.82 | 84.2 | 1147.4 | 3620.6 |
| France | 21961.5 | 1218.0 | 0.0 | 2664.4 | 5960.1 | 8477.3 |
| Romania | 12612.6 | 1335.0 | 0.0 | 67.0 | 576.2 | 1546.2 |
| Bulgaria | 10087.9 | 1429.0 | 0.992 | 0.0 | 0.0 | 0.0 |
| North Macedonia | 3915.1 | 1122.0 | 0.044 | 886.1 | 893.8 | 913.9 |
| Hungary | 2476.3 | 1228.0 | 0.0 | 0.0 | 0.0 | 100.1 |
| Moldova | 99.8 | 1114.0 | 0.647 | 0.0 | 0.0 | 12.7 |
| Serbia | 8.8 | 1471.0 | 0.0 | 0.0 | 0.0 | 0.2 |
| Switzerland | 1.9 | 1068.0 | 0.0 | 0.0 | 0.0 | 1.9 |
| Belarus | 1.5 | 805.0 | 0.0 | 0.0 | 1.5 | 1.5 |
| Poland | 0.8 | 267.0 | 0.0 | 0.8 | 0.8 | 0.8 |
| Andorra | 0.1 | 526.0 | 0.0 | 0.1 | 0.1 | 0.1 |

## Verdict
The rice-area check is a presence-only, same-product, out-of-region coverage check. It establishes that the gate does not exclude mapped current European rice; it cannot establish validity, commission or threshold optimality.
