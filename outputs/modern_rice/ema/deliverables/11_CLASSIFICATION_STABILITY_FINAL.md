# Classification stability (thermal gate)

Reference: T* = 589 GDD10, 5′, pipeline window. Weights: incumbent arable harvested area. Script: `ema_threshold_sweep.py`.

| domain | comparison | both_pass_ha | ref_only_ha | comp_only_ha | both_fail_ha | agreement_pct | jaccard_pass | rice_omitted_pct_comp |
|---|---|---|---|---|---|---|---|---|
| Europe | 900, 5', pipeline | 38288801.0 | 25935361.0 | 0.0 | 5473731.0 | 62.79 | 0.5962 | 3.221 |
| Europe | P05 recalibrated Jun-Sep (664), 5' | 59594512.0 | 4629649.0 | 13.0 | 5473717.0 | 93.36 | 0.9279 | 1.497 |
| Europe | P05 recalibrated 2.5' (612), majority of sub-cells | 63219257.0 | 1004904.0 | 37553.0 | 5436178.0 | 98.5 | 0.9838 | 1.197 |
| Europe | P05 recalibrated 10' (552) | 64138898.0 | 85263.0 | 1482865.0 | 3990866.0 | 97.75 | 0.9761 | 1.623 |
| Europe | Hokkaido P50 (859), 5' | 41395590.0 | 22828571.0 | 0.0 | 5473731.0 | 67.25 | 0.6445 | 2.934 |
| Germany | 900, 5', pipeline | 184074.0 | 5313637.0 | 0.0 | 195125.0 | 6.66 | 0.0335 | nan |
| Germany | P05 recalibrated Jun-Sep (664), 5' | 4881298.0 | 616413.0 | 0.0 | 195125.0 | 89.17 | 0.8879 | nan |
| Germany | P05 recalibrated 2.5' (612), majority of sub-cells | 5403267.0 | 94444.0 | 4013.0 | 191112.0 | 98.27 | 0.9821 | nan |
| Germany | P05 recalibrated 10' (552) | 5489484.0 | 8227.0 | 109827.0 | 85297.0 | 97.93 | 0.9789 | nan |
| Germany | Hokkaido P50 (859), 5' | 512763.0 | 4984948.0 | 0.0 | 195125.0 | 12.43 | 0.0933 | nan |

## Transition matrix T* → 900 (Mha; 3 gate classes on incumbent cells)
| index | 900: thermal not met | 900: thermal met, AEI <10% | 900: thermal met, AEI >=10% |
|---|---|---|---|
| T*=589: thermal not met | 5.474 | 0.0 | 0.0 |
| T*=589: thermal met, AEI <10% | 24.709 | 28.357 | 0.0 |
| T*=589: thermal met, AEI >=10% | 1.227 | 0.0 | 9.932 |

## Three separate questions
1. **Stability between specifications**: high for support/window changes with recalibration (Jaccard ≥ 0.93), low for reference changes (Jaccard 0.60 vs 900; 0.64 vs Hokkaido P50; Germany 0.03).
2. **Coverage of mapped rice**: rice omission under each alternative is in `CLASSIFICATION_STABILITY_PAIRS.csv` (column rice_omitted_pct_comp); all are ≤ 3.22%.
3. **Agronomic validity**: not established by either 1 or 2.

Disagreement map: `figures/CLASSIFICATION_DISAGREEMENT_MAP.png` (25.9 Mha pass at T* only).
