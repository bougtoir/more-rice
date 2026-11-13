# RPG data feasibility and independence

**Verdict: RPG VALIDATION FEASIBLE** — usable as an independent check of observed-land-use coverage in France; not usable to estimate specificity, commission or true suitability accuracy, and its climatic range is too narrow to discriminate between competing thresholds.

| Check | Status | Evidence |
|---|---|---|
| 1 Public RPG years | PASS | WFS layers RPG.2010 … RPG.2024 listed in Géoplateforme capabilities; 2010, 2015, 2020, 2024 retrieved |
| 2 Rice crop code | PASS | RIZ (label Riz), group 14; 2010 group code 14 = RIZ |
| 3 Rice-specific vs broad | PASS | group 14 has 1 code; see RPG_CROP_CODE_VERIFICATION.md |
| 4 Parcel geometry | PASS | MultiPolygon for every feature; 2010 is îlot (block) geometry, 2015–2024 parcel geometry |
| 5 Area | PASS | surf_parc (2015–2024) and surf_cultu (2010); geodesic area recomputed in EPSG:2154 agrees with declared totals within 0.1% |
| 6 Camargue coverage | PASS | ≥99% of area south of 43.8°N and east of 4.2°E (coordinate box, not an official Camargue boundary) |
| 7 Overlap with climate period | LIMITATION | WorldClim normals 1970–2000 do not overlap RPG years (2010–2024); RPG 2010 matches the MapSPAM reference year. Warming since 2000 implies present GDD10 is probably higher, which can only reduce omission |
| 8 Independence from MapSPAM | PARTIAL | geometry and spatial allocation independent; national/subnational area totals may share the same declarations upstream (not verified) |
| 9 Built with climatic suitability model? | PASS (no) | administrative CAP declarations with anonymised parcel geometry; no climatic or suitability layer is used in construction (official dataset description) |
| 10 Licence for analysis and derived statistics | PASS | Licence Ouverte / Open Licence 2.0 (etalab-2.0), stated on the official IGN dataset page |
| 11 Redistribution of geometries | PASS (not exercised) | Licence permits reuse and redistribution with attribution; raw geometries nevertheless kept out of the public repository (gitignored); only derived cell-level tables are published |
| 12 Spatial resolution adequacy | PASS with caveat | parcels ≪ 5′ cell; support is 29–39 distinct cells, so the effective climatic sample is small |

Acquisition was limited to rice-coded features (four requests, one page each; `numberMatched` equals features returned, so no pagination truncation). Raw files are stored in `modern_rice/data/raw/rpg/` (gitignored) with `LEDGER.txt`; see `RPG_DATA_PROVENANCE.csv`. Seven data.gouv.fr catalogue searches returned empty responses (94 bytes) and were not used.
