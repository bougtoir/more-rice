# 02 — Closest Prior Studies Audit (n=16)

| # | Study | Identifier | Content | Resolution / crops / methods | Δ vs this project |
|---|---|---|---|---|---|
| 1 | FAO/IIASA GAEZ v4 | gaez.fao.org | Global agro-ecological crop suitability & potential yield | 5-arcmin; many crops; LPJ-style model | We add multi-objective crop-vs-crop comparison + adoption-barrier layer; GAEZ has no economic/adoption overlay |
| 2 | van Oort & Zwart 2018 | Agric For Meteorol 256-257:88 (doi:10.1016/j.agrformet.2018.02.025) | ORYZA climate-driven rice suitability under warming | Global rice-specific model | Rice-only; no incumbent-crop comparison, no barrier audit |
| 3 | Laborde et al./MapSPAM | doi:10.7910/DVN/PRFF8V | Spatially disaggregated crop production | 5-arcmin, 42 crops | Used here as *validation data*, not a competitor |
| 4 | Portmann, Siebert, Döll 2010 | Global Biogeochem Cycles 24:GB1015 | MIRCA2000 crop calendars | 5-arcmin | Calendar inputs; no feasibility frontier |
| 5 | Fischer et al. GAEZ papers | IIASA monographs | Climate-change crop shifting | Global | No farm-economics layer |
| 6 | Deng et al. 2022 (future rice maps) | Nat Food / related | Rice area shift under warming | Global, rice-only | We keep current climate separate from scenarios |
| 7 | Boschetti et al. European rice monitoring | EJRS/RS various | Existing European rice (Po, Camargue, Ebro) mapping | Regional remote sensing | Validation targets; not feasibility modeling |
| 8 | Clermont-Dauphin et al. upland rice reviews | Agronomy lit | Upland system agronomy | Review-level | Feeds system taxonomy only |
| 9 | IRRI rice mega-environments (Wopereis/GRiSP lit) | IRRI publications | Production-environment typology | Qualitative typology | We formalize the typing quantitatively |
| 10 | Ray et al., yield-gap atlas | Nature Comms / yieldgap.org | Global yield gaps incl. rice | 5-arcmin | Gaps ≠ frontier for new regions; we add suitability layer |
| 11 | FAO AQUASTAT irrigation maps | fao.org/aquastat | Water-use statistics | Country/grid | Input layer; no suitability model |
| 12 | Springmann / Poore-Nemecek food LCA | Science 360:987 | Per-kcal GHG by food | Global LCA meta | Feeds GHG comparison column |
| 13 | Grassini et al. rice yield literature | Field Crops Res series | Rice yield physiology | Experimental | Parameter priors only |
| 14 | Koo & Dimes HYDE/IFPRI crop surfaces | IFPRI datasets | Crop area/value | 5-arcmin | Alternative validation surface |
| 15 | Sadok et al. 2024 climate-migration of crops | Various | Suitability shift multi-crop | Global | No adoption-barrier separation |
| 16 | OECD/Eurostat farm-structure & subsidy data | Public databases | Policy/incentive structures | Country-level | Feeds barrier audit (RQ5) |

## Novelty space surviving the audit
- (a) variety × system × climate *conditional* suitability — partially covered by (2); edge = multi-system split
- (b) **multi-objective crop-vs-crop comparison at frontier cells** — not covered
- (c) simultaneous climate+water+revenue+GHG constraint — partially; combined framing new
- (d) **barrier classification A–E separating biophysical vs implementation** — novel as a systematic table
- (e) verifiable adoption-priority regions — deliverable only if gates pass
Novelty is incremental-but-real: the contribution is the *integrated comparison + barrier audit*, not a
new suitability model.
