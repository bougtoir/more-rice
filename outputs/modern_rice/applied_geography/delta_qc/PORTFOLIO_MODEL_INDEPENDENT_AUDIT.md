# Portfolio (food-supply risk) model — independent audit
Verdict: **PASS WITH LIMITATIONS (two further corrections applied)**

## Independent reimplementation
Separate code (`delta_qc/indep/risk_indep.txt`) re-derived scenario A and B shortfall probabilities from FAOSTAT QCL (linear log-detrending, area-share weights from the latest year, f = 0.2, threshold 0.8 × own mean). Before the milling correction it reproduced the pipeline baseline exactly (Romania 0.203/0.109; Serbia with Hungarian analog 0.211/0.000; Kazakhstan 0.212/0.030).
- Minimal nonzero example: A = [10,10,10,10,7], rice = 10 each year, B = 0.8A + 0.2·rice ⇒ last-year B = 7.6, versus 5.6 under the legacy zero-rice bug; the corrected branch gives a nonzero rice contribution.
- Serbia: analog branch uses Hungarian rice shocks *and* level; the legacy potato-dominance claim is withdrawn.

## Corrections applied in this delta
1. **Paddy vs milled energy**: FAOSTAT "Rice" yields are paddy (kg/ha); the energy density 3.65 kcal/g is for milled rice. Rice yields are now multiplied by 0.67 (milled equivalent). Effect: Kazakhstan P_B 0.030 → 0.061 and CI-excludes-zero share 79% → 58%; Romania 42% → 17%.
2. **Text/code mismatch**: the manuscript described shortfall as < 90% of mean; code uses 80%. Text and Figure 5 caption corrected.

## Corrected results (baseline: linear, f = 0.2, scale 1.0, own-mean threshold)
| country    | rice_source    |   n |   P_A |   P_B |   P_D | CI              |   share_B_lt_A |   share_CI_excl_0 |
|:-----------|:---------------|----:|------:|------:|------:|:----------------|---------------:|------------------:|
| Romania    | Romania        |  64 | 0.203 | 0.109 | 0.172 | -0.156 to 0.0   |          1     |             0.167 |
| Bulgaria   | Bulgaria       |  64 | 0.203 | 0.172 | 0.188 | -0.094 to 0.016 |          0.375 |             0     |
| Serbia     | analog:Hungary |  19 | 0.211 | 0     | 0.053 | -0.263 to 0.0   |          0.375 |             0     |
| Kazakhstan | Kazakhstan     |  33 | 0.212 | 0.061 | 0.091 | -0.242 to 0.0   |          1     |             0.583 |
| Hungary    | Hungary        |  64 | 0.188 | 0.156 | 0.156 | -0.062 to 0.031 |          0.333 |             0     |
| France     | France         |  64 | 0.109 | 0.094 | 0.125 | -0.109 to 0.0   |          0.125 |             0     |

## Method checks
- Bootstrap: moving blocks of 3 years, non-circular, 2,000 draws, percentile 95% interval; single RNG stream (seed 20261108) shared across the 24 configurations, so results are reproducible but order-dependent. Blocks preserve within-country cross-crop correlation because all crops are resampled with the same year indices.
- Many intervals have an upper bound of exactly 0.000 because shortfall probabilities are discrete fractions of n years; "excludes zero" requires the upper bound < 0.
- No multiplicity correction across 24 configurations × countries; robustness shares are descriptive.
- Model is national, calorie-only, ignores trade, storage and price; substitution is hypothetical.

## Recommendation
The portfolio analysis is ancillary to the geographic contribution. It is kept short (one section, one figure, one table) and phrased as scenario statistics. Moving it to supplementary material is a reasonable alternative if an editor considers it off-scope.
