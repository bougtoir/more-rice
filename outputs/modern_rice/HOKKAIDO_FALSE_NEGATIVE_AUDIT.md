# Hokkaido False-Negative Investigation

**Finding:** E-Hokkaido point shows 903 GDD10 (Jun–Sep), 68.6 cold-snap nights, only 195 frost-free days — below model thresholds — yet commercial rice is grown. Asahikawa (901 GDD) and Morioka (1136) replicate the pattern → consistent false-negative class, not a single-site artifact.

**Mechanisms that explain the mismatch (ranked by evidence weight):**
1. **Genetic adaptation** — ultra-early temperate japonica cultivars selected for Hokkaido; GDD requirement ~900–1100 vs ~1500 conventional. Documented cultivar class (CULTIVAR_PARAMETER_REGISTRY.csv).
2. **Agronomic management** — transplanting seedlings raised in heated/nursery conditions shifts effective season start ~4–6 weeks; warm-water irrigation reduces flowering-stage cold injury.
3. **Local microclimate** — paddy water buffering; low elevation basins vs grid-mean point.
4. **Spatial-resolution artifact** — single POWER point vs distributed paddy microclimates.
5. **Model misspecification** — monthly-mean + generic-threshold model cannot express cultivar×management classes; this is the structural cause.

**Independent cold-region validation (COLD_REGION_EXTERNAL_VALIDATION.csv):** Shenyang 1627 / Seoul 1578 / Vercelli 1224 are documented rice areas consistent with feasible; Japanese sites 901–1136 define the empirical cold bound.

**Rule adopted:** documented cold bound for cultivated rice ≈ **900 GDD10 seasonal** under japonica + transplant management; generic threshold retained for non-japonica context. Hokkaido treated as external validation case, NOT a calibration target.
