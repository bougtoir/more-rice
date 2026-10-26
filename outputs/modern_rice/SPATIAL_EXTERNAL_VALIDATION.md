# Gate 4 — Spatially Blocked External Validation

Method: 30°×30° spatial blocks over the SPAM2010 rice harvested-area raster; per-block detection rate = share of block's rice ha inside feasible classes (suitability_class_10m.tif). Table: SPATIAL_BLOCK_VALIDATION.csv (31 rice-bearing blocks).

Results:
- Median per-block feasible coverage 0.996; weighted (area) mean ≈ 0.87.
- Weakest block (block_lat 1, block_lon 3: 0.397) — high-latitude northern fringe where Hokkaido-type japonica cultivation sits below model thresholds (known cold-edge miss).
- Tiny blocks with near-zero area show noisy 0/1 values.

Interpretation (per spec caveats): this is detection of EXISTING rice area, NOT independent yield validation; it does not demonstrate predictive skill for new regions. Specificity cannot be cleanly computed (rice-free land may still be suitable) — flagged, not claimed.
