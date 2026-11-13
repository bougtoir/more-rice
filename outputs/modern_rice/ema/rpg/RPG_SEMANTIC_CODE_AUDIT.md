# RPG semantic code audit

| Concept | Implementation | Where / test |
|---|---|---|
| Rice records | only code_cultu RIZ (2015–2024) / 14 (2010) features retrieved by server-side filter | rpg_fetch_rice.py CQL_FILTER; crop-code report |
| Domain | metropolitan France; overseas excluded by representative-point bounding box (-5…10°E, 41…51.5°N) | rpg_validation.load |
| Area | geodesic area in EPSG:2154; 2010 weight = surf_cultu (rice-group area within îlot) distributed in proportion to îlot geometry | load / overlay |
| Cell assignment | polygon ∩ 5′ cell overlay; centroid assignment as sensitivity | overlay, cell_of; KAT 1–4, 9 |
| Climate surface | same canonical ema_layers_5m.npz g5 (WorldClim 2.1, 29 Apr–11 Sep) as the manuscript | load of EMA npz |
| Estimand | area-weighted share of declared rice area in cells with GDD10 < T (strict); nodata excluded from denominator (0 ha in practice) | omit; KAT 3, 6, 10 |
| Effective support | distinct (row, col) cells | climate_cells; KAT 4 |
| MapSPAM comparison | France = modal country id among RPG 2020 cells (id 51); verified: MapSPAM rice under this id equals canonical RICE_OMISSION_BY_COUNTRY France total (builder assertion) | build_ema_manuscript.py assertion; KAT 11–12 |
| Camargue share | coordinate box lon ≥ 4.2°E, lat ≤ 43.8°N, labelled as approximate | share_area_… column |
| Uncertainty | no parcel bootstrap; year-to-year range and centroid sensitivity reported instead | manuscript §2.6 |

Known-answer tests: 26/26 PASS (`RPG_KNOWN_ANSWER_TESTS.md`). Issue found and fixed during audit: a zero-area test parcel exposed that the area filter was inline in `load`; it was factored into `clean_area` and tested directly.
