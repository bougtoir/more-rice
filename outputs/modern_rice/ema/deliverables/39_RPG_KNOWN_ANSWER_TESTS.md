# RPG known-answer tests

Oracle: planar shapely areas (degrees) on a synthetic 2 × 2 grid of 0.1° cells and plain numpy loops over saved cell tables; production functions `overlay`, `omit`, `cell_of` from `rpg_validation.py` are the units under test. Tolerance for projected-vs-planar area fractions: 0.005.

| # | Test | Result | Detail |
|---|---|---|---|
| 1 | 1 parcel inside one cell -> single intersection, frac 1 | PASS | frac=1.000000 |
| 2 | 2 parcel crossing two cells -> area split matches planar oracle | PASS | prod=[0.5 0.5] oracle=[0.5 0.5] |
| 3 | 2b crossing parcel omission at 589 equals share in 500-GDD cell | PASS | 0.5000 vs 0.5000 |
| 4 | 3 parcel overlapping nodata cell -> nodata share excluded from denominator | PASS | nodata share=0.6157 |
| 5 | 4 two parcels in same cell -> one climate cell | PASS |  |
| 6 | 5 zero-area parcel removed by clean_area before overlay | PASS |  |
| 7 | 6 threshold equal to cell GDD (589) -> passes (strict <) | PASS |  |
| 8 | 7 omission non-decreasing in threshold (RPG 2020 cells) | PASS |  |
| 9 | 8 area-weighted omission within [0,1] | PASS |  |
| 10 | 9 centroid and intersection agree for parcel inside one cell | PASS |  |
| 11 | 10 RPG 2010 omission at T=589 reproduced from cell table | PASS | 0.00000 |
| 12 | 10 RPG 2015 omission at T=589 reproduced from cell table | PASS | 0.00000 |
| 13 | 10 RPG 2020 omission at T=589 reproduced from cell table | PASS | 0.00000 |
| 14 | 10 RPG 2024 omission at T=589 reproduced from cell table | PASS | 0.00000 |
| 15 | 10 RPG 2010 omission at T=900 reproduced from cell table | PASS | 0.00000 |
| 16 | 10 RPG 2015 omission at T=900 reproduced from cell table | PASS | 0.00012 |
| 17 | 10 RPG 2020 omission at T=900 reproduced from cell table | PASS | 0.00000 |
| 18 | 10 RPG 2024 omission at T=900 reproduced from cell table | PASS | 0.00022 |
| 19 | 10 RPG 2010 omission at T=1100 reproduced from cell table | PASS | 0.00000 |
| 20 | 10 RPG 2015 omission at T=1100 reproduced from cell table | PASS | 0.00012 |
| 21 | 10 RPG 2020 omission at T=1100 reproduced from cell table | PASS | 0.00015 |
| 22 | 10 RPG 2024 omission at T=1100 reproduced from cell table | PASS | 0.00022 |
| 23 | 11 MapSPAM France share in RPG 2010 cells reproduced by loop | PASS | 0.0406 |
| 24 | 12 MapSPAM France omission at T=589 reproduced | PASS |  |
| 25 | 12 MapSPAM France omission at T=900 reproduced | PASS |  |
| 26 | 13 France area sum equals declared area (RPG 2020, <0.1%) | PASS |  |

**Summary: 26/26 PASS.**
