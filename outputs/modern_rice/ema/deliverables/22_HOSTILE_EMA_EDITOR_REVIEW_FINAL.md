# Hostile EM&A editorial review (performed before mechanical QC)

| Question | Assessment |
|---|---|
| Environmental assessment or GIS crop mapping? | Framed as reliability of an environmental suitability assessment; still uses crop maps and a crop-transfer case. An editor can read it as GIS crop mapping. |
| Beyond deterministic monotonicity? | Yes, partly: the informative result is where omission rises (≤5% up to 1,076, >10% from 1,225) relative to the competing references, and that the check cannot discriminate T* from 900. The monotonic shape itself is not claimed. |
| Rice map independent? | MapSPAM: no (same product as calibration, allocation priors; §2.5). New: French parcel register (RPG) is independent in spatial allocation (§2.6, §3.7). |
| High inclusion from permissive gate? | Yes, this is stated explicitly (§4.1): low omission (1.37%) is mechanically expected for any permissive threshold. |
| Validates actual cultivation? | Partly, for France only: declared rice parcels are never omitted at T* (≤0.02% up to 1100 GDD10), but they occupy 29–39 warm cells and cannot rank references. Presence only. |
| Independent negatives? | None. No specificity/precision/AUC computed. |
| Literature already establishes the insight? | Threshold and MAUP sensitivity are known (Malone 2015; Xu & Zhang 2013; Jelinski & Wu 1996; Snelder 2023). New: controlled decomposition plus demonstration that mapped-cultivation coverage is uninformative in the decisive range. Modest. |

## Five strongest desk-rejection risks
| # | Risk | Evidence | Severity | Resolution in this version | Next action |
|---|---|---|---|---|---|
| 1 | Scope: no new author-collected field data; 'strictly modelling studies with little field data support' excluded | EM&A Aims & Scope (archived) | MEDIUM–HIGH | Framed as assessment of monitoring/census-derived products; 8/19 audited EM&A papers had no new field data; independent RPG parcel check added (administrative open data, not author-collected) | None feasible without new field campaigns |
| 2 | Omission analysis judged trivial (monotone) | Reviewer logic | MEDIUM | Location-of-rise and non-discrimination result; scenario ranges (shifts, LOCO) | None required |
| 3 | Circular validation (MapSPAM used for calibration and evaluation) | §2.5 | MEDIUM | Disclosed; RPG check shows French MapSPAM omission is an allocation effect (0% omission inside RPG cells) | Resolved for France only |
| 4 | Crop-management / economic exclusion | Aims & Scope exclusions 6, 8 | LOW–MEDIUM | Economic parity, hydrology and food-risk removed from narrative | None |
| 5 | Insufficient novelty (cf. AG desk reject) | AG decision letter | MEDIUM | Novelty boundary explicit; no method claims | Cover letter states incremental contribution |

## Minor
- Body ~3,800 words vs EM&A average ~9,000 (no limit). Acceptable.
- Single case (Hokkaido → Europe); generality argued, not shown.
