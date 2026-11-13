# Citation ecology and journal neighborhood

Source bibliography: `modern_rice/manuscript_ag/manuscript_template.md`, section `# REFERENCES` (the final verified Applied Geography version, 37 entries; parsed 2026-11-13). The uncommitted LUP draft in `modern_rice/manuscript_lup/` is not an approved version and was not used. Per-reference coding: `REFERENCE_JOURNAL_DISTRIBUTION.csv`.

## Distributions (n = 37)

| Dimension | Counts |
|---|---|
| Source type | journal 29; dataset 6; report 1; book 1 |
| Source journal (top) | Applied Geography 10; Nature Communications 2; every other journal 1 |
| Target-candidate journals in the bibliography | EM&A 0; Land Use Policy 0; Agricultural Water Management 0; Ecological Indicators 0; Journal of Environmental Management 0 |
| Environmental-management family | Environmental Management (Springer) 1 (Snelder et al., 2023) |
| Direct methodological predecessors | yes 8; partly 5; no 24 |
| Environmental-assessment literature | yes 3; partly 6; no 28 |
| Land-use or agricultural-systems literature | yes 30; no 7 |
| Scientific role | data source 9; closest prior (method/concept/uncertainty/sensitivity/thermal/global suitability) 8; context 7; motivation 4; method 4; parameter source 3; concept 1; data validation 1 |

Research-field grouping (from the `research_field` column): geography / land suitability and land-use change 11; global agriculture, food security and crop adaptation 7; agricultural water, agronomy and engineering 6; agricultural and land-use data 4; climatology and cartography data 4; hydrology / water resources 2; statistics 1; landscape ecology 1; environmental management 1.

## Dominant scholarly neighborhood

The bibliography sits in **applied geography / land-suitability evaluation** (Applied Geography 10/37; closest priors Cornwell et al. 2020, Tenerelli & Carver 2012, Xu & Zhang 2013, Schmitter et al. 2018, Yang et al. 2023, Zabel et al. 2014, Malone et al. 2015) plus **global agriculture and food-system risk** (Gaupp et al. 2020; Mehrabi & Ramankutty 2019; Renard & Tilman 2019; Ray et al. 2015; Sloat et al. 2020). The environmental-assessment literature is thin: 3 references coded "yes" (Nouri et al. 2017; Saiko & Zonn 2000; Snelder et al. 2023), and none of them is an EM&A paper or a monitoring/assessment-methods paper.

## Comparison with candidate journals

| Journal | Overlap with the current bibliography | What its own literature would expect |
|---|---|---|
| EM&A | None. Closest EM&A papers (see `EMA_CLOSEST_PUBLISHED_PAPERS.csv`) are local GIS-MCDA suitability studies with soil sampling and yield/ROC validation, and MaxEnt climatic-suitability studies. The manuscript cites none of them and uses neither family of methods. | Field data, validation against observed outcomes, monitoring relevance. |
| Land Use Policy | None in the AG bibliography. The interrupted LUP draft added six policy references (CAP crop diversification, land-use transitions), which shows the policy neighborhood is reachable from literature already retrieved, but those additions are unapproved. | Land-use decision questions; CAP and diversification policy literature. |
| Agricultural Water Management | Indirect: FAO-56 (Allen et al.), Bouman et al. 2007, Monaco et al. 2016 | Field/regional water-management insight. Excluded for its mandatory APC anyway. |
| Ecological Indicators | None | Indicator theory and indicator development. Excluded for its mandatory APC. |
| Journal of Environmental Management | None; nearest is Environmental Management (Snelder et al., 2023), a different journal | Management application with a novelty statement and international relevance. |

## Proposed citations (only where a precise claim needs them)

These are not to be added to raise target-journal counts. Each supports a specific sentence that the existing related-work section (4.2) already makes in general terms:

1. Mohamed et al. (2019) EM&A 191:535 (doi:10.1007/s10661-019-7649-z): on the same land, the choice of evaluation method alone moved the classification from 75.0% "not suitable" (square root) to 82% S1+S2 (GIS-MCDA). This is an independent, published magnitude example for the claim that suitability classes depend on how the reference is constructed.
2. Van et al. (2022) EM&A 194:767 (doi:10.1007/s10661-022-10180-y): rice suitability zoning in which water availability and salinity, not temperature, are the governing variables. Supports the claim that water, not temperature, binds rice zoning.
3. Azadi et al. (2023) EM&A 195:1296 or Vahidi et al. (2023): method-comparison papers validated against field yield. Supports the limitations sentence that the gate screen has no yield-based validation.

Items 1–2 would also be valid in a Land Use Policy version, because they support the reference-dependence and water-constraint claims whatever the target journal.
