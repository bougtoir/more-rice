# RPG independence and external-validity audit

| Dependency | Assessment |
|---|---|
| MapSPAM crop allocation | Independent in spatial allocation: RPG geometry is declared by farmers and digitised on orthophotos; MapSPAM allocates statistics with cropland, irrigation and suitability priors. Totals may share upstream statistics (agricultural statistics in France draw on CAP declarations); not verified, so independence of totals is not claimed. |
| WorldClim thermal surface | Independent: RPG contains no climate information. |
| Hokkaido reference construction | Independent: T* was calibrated on MapSPAM rice in Japan; RPG was not used in calibration and was retrieved after T* was fixed. |
| Model classification outputs | Independent: RPG was not used to choose thresholds, windows or grids. |

## What RPG is not
- Not ground truth of suitability: a declaration records that rice was grown, not that the climate is sufficient without management (flooding, cultivar choice).
- Not error-free: declaration, crop-coding and digitising errors are possible; CAP controls reduce but do not remove them.
- Presence only: absence of a rice declaration is not evidence of unsuitability, so commission, specificity, precision, F1 and AUC are not computed.

## External validity
- Effective sample: 29–39 distinct 5′ cells per year, nearly all in and around the Rhône delta; parcel counts (1,407–1,703) are not independent climate observations and no parcel-level bootstrap is reported.
- Climatic range: area-weighted 5th percentile ≥1,520 GDD10; every occupied cell exceeds 802 GDD10. The check is therefore uninformative for thresholds below ~1,425 GDD10 and cannot rank T* against 900 GDD10.
- Geography: one country, one delta; not representative of the cool Italian and Ukrainian margins where MapSPAM omissions occur.
- Time: RPG 2010–2024 vs 1970–2000 normals (see feasibility check 7).

## Interpretation category (prompt)
Strong coverage agreement at all tested thresholds; **insufficient independent climatic variation / low discrimination**; material disagreement with MapSPAM France that is explained by MapSPAM allocation outside the declared district (MapSPAM omission is 0% inside RPG cells), not by a contradiction of the gate.
