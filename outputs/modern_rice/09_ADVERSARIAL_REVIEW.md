# 09 — Adversarial Review (4 independent personas)

## Crop physiologist / rice breeder
- **MAJOR:** Monthly-mean climatology cannot capture reproductive cold-snap sterility (the actual
  mechanism limiting marginal-zone rice). The pilot's marginal class is systematically optimistic.
  → Accepted: flagged in 07; a daily-temperature (ERA5) pass is required before any frontier claim.
- **MAJOR:** "Early-maturing/cold-tolerant varieties" treated as a modest shift — correct, but the
  feasibility raster never uses variety parameters at all; calling it "modern variety feasibility"
  overstates. It's a thermal-envelope map. → Corrected in wording: "thermal feasibility under
  parameter grid," not variety-explicit.
- **MINOR:** Paddy vs milled in the kcal comparison was caught and documented; protein column missing.

## Agricultural hydrologist / climate adaptation
- **MAJOR:** Rainfed class uses warmest-3-month rainfall ≥300mm — ignores ET0, dry-spell within season,
  soil storage. W. Europe scoring 0 rainfed cells is plausible but unproven at that rule. → Accepted:
  labeled proxy.
- **MAJOR:** feasible_irrig_dependent says nothing about *whether water exists* — Danube delta cells
  feasible thermally may have no allocable blue water (Central Asia case flagged). → barrier table
  handles it at class C only.
- **MINOR:** No groundwater/surface-water mask.

## Agricultural economist / food policy
- **MAJOR:** RQ2 cannot be answered yet — no prices, input costs, or subsidy data computed; "rice wins
  on kcal" ≠ "rice wins on profit." → Accepted: Gate B says comparison incomplete.
- **MINOR:** CAP rice-area history matters for the D-zone discussion — noted qualitatively.

## LCA / land use
- **MAJOR:** Methane liability of paddies undermines an environmental case for *new* paddy in
  margin-feasible zones; AWD mitigation exists but is itself water-institution-dependent. → Kept as a
  first-class column in framework; paddy expansion recommendation must be conditional on water
  management, not unconditional.
- **MINOR:** No land-cover opportunity-cost layer (would rice displace high-carbon-value land?).

## Pre-empted strongest objections (spec §11)
- cold-snap sterility: acknowledged as unmodeled → daily-data pass needed
- lower revenue: acknowledged — Gate B not fully met
- water competition: barrier table flags it for C-candidates
- CH4: framework column; conditional recommendation rule adopted
- processing/market infra: barrier audit column
- variety extrapolation: thermal-envelope wording
- duplication: novelty narrowed to integrated comparison + barrier audit
