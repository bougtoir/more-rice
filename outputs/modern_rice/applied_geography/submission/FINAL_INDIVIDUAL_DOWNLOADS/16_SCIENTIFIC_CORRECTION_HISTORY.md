# Scientific correction history

From the Agricultural Systems version (main @ 6202551, `MANUSCRIPT_FINAL_ORDER_CORRECTED.docx`, unchanged in this PR) to the Applied Geography version (PR #1). Each correction was found by re-running or independently re-implementing the calculation, not by comparing script and text.

| # | Round | Issue | Found by | Correction | Effect on conclusions |
|---|---|---|---|---|---|
| 1 | retarget | Lower Danube demand reported as ~24 m³/s | recomputation Q = A·D/T | ~241 m³/s net (321.5 gross at 75%) | demand is 10× larger; mainstem argument weakened |
| 2 | retarget | GDD window described as Jun–Sep; code used pseudo-DOY 29 Apr–11 Sep | code reading + day counts | both windows reported, pipeline window labelled | Rhine/Saxony ranking vs Hokkaido reverses under Jun–Sep |
| 3 | retarget | Analog-country rice contribution zero (NaN level) | minimal synthetic example | shocks and level from the same analog | Serbia potato-dominance conclusion withdrawn |
| 4 | retarget | ~900 GDD10 point bound applied to a grid | same-grid recalibration | T* = 589 GDD10 (Hokkaido rice-area P05, WorldClim 5′) | temperature no longer the binding gate |
| 5 | retarget | White (2011) non-existent; You (2014) wrong journal | Crossref | Bai et al. (2010); Yu et al. (2020) | none |
| 6 | delta QC | "Europe" computed on a rectangle incl. N Africa, Anatolia, Caucasus, European Russia (107.1 Mha) | country-mask audit | Natural Earth Europe excl. Russia, 69.7 Mha; rectangle kept as labelled sensitivity | 94.2%→92.2% thermal; 17.6%→16.0% thermal + AEI |
| 7 | delta QC | Paddy yields multiplied by milled-rice energy | unit audit | × 0.67 milled equivalent | Kazakhstan robust share 79%→58%; Romania 42%→17% |
| 8 | delta QC | Text 90% shortfall threshold vs code 80% | text–code audit | 80% in text and captions | none numerically |
| 9 | delta QC | "Guglielmo et al. 2025" | publisher record | Savoini et al. (2025) | none |
| 10 | delta QC | `T*` asterisk lost / `TT*` rendering | DOCX XML inspection | font-based superscript placeholder | none |
| 11 | hydrology | CT-UPT (2014) Q99 = 1,100 m³/s unverifiable | 13 documented searches | removed with 21.9%/29.2% ratios; replaced by EStreams/GRDC Orsova Jun–Sep minimum daily discharge (median 2,749 m³/s) | no flow-duration Q99 claimed; no allocation/feasibility claim |
| 12 | final | Germany 97% vs 3% described as data/scale dependence | controlled decomposition + independent script | reframed as a reference-construction (estimand) contrast; resolution ≤2.4 pp in primary window; Figure 3d added | headline retained only with the corrected interpretation |
| 13 | final | Title | author decision | "Spatial constraints on transferring rice cultivation systems beyond traditional growing regions: A multi-scale assessment of thermal suitability and irrigation infrastructure" | none |
| 14 | final | Prior-work positioning thin on irrigation-potential and threshold-uncertainty literature | targeted search, publisher abstracts | 6 Crossref-verified references added (Cornwell 2020; King 2018; Malone 2015; Schmitter 2018; Sloat 2020; Snelder 2023) | contribution statement narrowed |
