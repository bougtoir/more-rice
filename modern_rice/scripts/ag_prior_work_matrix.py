#!/usr/bin/env python3
"""Closest-prior-studies matrix and geographic-novelty audit. Bibliographic fields are read from the saved
Crossref / OpenAlex / Semantic Scholar / publisher-page records in modern_rice/data/raw/literature_openalex_2026-11-08;
the content columns are the author's reading of the saved abstracts/highlights (source recorded per row)."""
import os, json, glob, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
L = os.path.join(ROOT, "modern_rice", "data", "raw", "literature_openalex_2026-11-08"); FA = os.path.join(ROOT, "outputs", "modern_rice", "applied_geography", "final_audit"); os.makedirs(FA, exist_ok=True)
s2 = {(w or {}).get("externalIds", {}).get("DOI", "").lower(): w for w in json.load(open(os.path.join(L, "semanticscholar_batch_2026-11-08.json"))) if w}
def rec(doi):
    d = doi.lower(); out = {"doi": doi}
    oa = os.path.join(L, "doi_" + doi.replace("/", "_") + ".json"); cr = os.path.join(L, "crossref_" + doi.replace("/", "_") + ".json"); pb = os.path.join(L, "publisher_abstracts", doi.replace("/", "_") + ".json")
    if os.path.exists(cr):
        m = json.load(open(cr))["message"]; out |= dict(title_record=m["title"][0], venue_record=(m.get("container-title") or [""])[0], year_record=(m.get("published-print") or m.get("issued"))["date-parts"][0][0], bib_source="Crossref")
    elif os.path.exists(oa):
        w = json.load(open(oa)); out |= dict(title_record=w["display_name"], venue_record=((w.get("primary_location") or {}).get("source") or {}).get("display_name", ""), year_record=w["publication_year"], bib_source="OpenAlex")
    elif d in s2:
        w = s2[d]; out |= dict(title_record=w["title"], venue_record=w.get("venue", ""), year_record=w.get("year"), bib_source="Semantic Scholar")
    if os.path.exists(pb) and json.load(open(pb)).get("abstract"): out["content_source"] = "publisher page abstract/highlights (" + os.path.relpath(pb, ROOT) + ")"
    elif d in s2 and s2[d].get("abstract"): out["content_source"] = "abstract via Semantic Scholar record"
    else: out["content_source"] = "NOT VERIFIED BEYOND TITLE/BIBLIOGRAPHY"
    return out
S = [  # doi, short cite, cited_in_manuscript, closeness, dimensions, demonstrates, does_not, this_study
("10.1016/j.apgeog.2022.102822", "Yang et al. (2023)", "yes", "high", "threshold-based rice-limit mapping; crop-system transfer",
 "Maps potential northern limits and safe/risky promotion areas of a specific rice system (ratoon rice) in China with a MaxEnt model", "Does not test how the mapped limit depends on reference construction, climate source or grid support; no land denominator",
 "Decomposes the dependence of a cold-region bound on quantile, location, period, temporal aggregation and resolution (Germany 3% vs 97%) and reports exposure of an explicit incumbent-arable denominator"),
("10.1016/j.apgeog.2022.102667", "Liu et al. (2022)", "yes", "high", "cold-margin paddy expansion; land-use adaptation",
 "Satellite-mapped paddy expansion into mid-high latitudes of Northeast China (net +2.6×10^4 km² 1990–2018) alongside northward isotherm shifts", "Not a transfer assessment for regions without paddy tradition; does not separate thermal from infrastructure gates",
 "Screens a region with almost no paddy and separates thermal compatibility from irrigation infrastructure and rainfed balance; claims no observed expansion"),
("10.1016/j.apgeog.2010.11.005", "Gao & Liu (2011)", "yes", "medium", "warming and rice land-use change",
 "Associates climate warming with land-use change toward paddy in Heilongjiang", "No causal identification; no infrastructure or water allocation analysis", "Treats the observed Chinese case only as context; does not infer a European trajectory"),
("10.1016/j.apgeog.2020.102248", "Cornwell et al. (2020)", "added", "high", "biophysical + irrigation-potential suitability; system-specific cropping",
 "Projects biophysical and catchment irrigation-potential suitability for traditional sub-alpine cropping; irrigation-potential deficits drive suitability loss more than farm-level biophysics", "Uses weighted multi-criteria suitability; no test of threshold reference construction",
 "Applies the same insight (water access binds before climate) with non-compensatory gates on a continental denominator, and quantifies reference-construction sensitivity of the thermal gate"),
("10.1016/j.apgeog.2013.08.005", "Xu & Zhang (2013)", "yes", "high", "spatially explicit sensitivity of suitability",
 "Spatially explicit sensitivity metric for MCDM land-suitability evaluation (wheat): robust overall but locally sensitive", "Sensitivity to criteria weights, not to climate source, reference quantile or grid support",
 "Shows a comparable 'globally stable, locally sensitive' pattern for resolution, but that reference construction, not weights or resolution, drives national outcomes"),
("10.1016/j.apgeog.2011.08.013", "Tenerelli & Carver (2012)", "yes", "medium", "uncertainty analysis in crop-conversion suitability",
 "GIS multi-criteria land capability for energy-crop conversion with simulation-based uncertainty analysis (Yorkshire and the Humber)", "Weighted, compensatory framework; uncertainty in inputs, not in reference definition",
 "Uses non-compensatory gates and explicit reference-construction decomposition; no allocation optimum claimed"),
("10.1016/j.apgeog.2023.102937", "Safanelli et al. (2023)", "yes", "medium", "suitability index vs observed land-use change",
 "Grain-cropping suitability index (climate, soil, terrain, crop simulation) compared with historical land-use change in Brazil", "Does not address transfer of a cultivation system or infrastructure gates",
 "Adds a system-specific transfer reference and infrastructure gate; validates against observed European rice distribution only as consistency"),
("10.1016/j.apgeog.2018.02.008", "Schmitter et al. (2018)", "added", "medium", "irrigation-infrastructure / water-access suitability mapping",
 "Multi-criteria GIS suitability for solar PV irrigation pumps in Ethiopia; water-resource accessibility drives scenarios; checked against well-depth data", "Targets a technology, not a crop transfer; weighted overlay",
 "Treats mapped irrigation equipment (GMIA AEI) as a necessary but not sufficient gate and distinguishes it from allocable water"),
("10.1016/j.apgeog.2017.02.006", "Nouri et al. (2017)", "yes", "medium", "suitability with basin water conservation",
 "GIS multi-stage land suitability to relocate agricultural/residential development away from Urmia Lake", "No crop-transfer gate; conservation-driven allocation", "Treats basin water sustainability as unresolved and makes no allocation claim"),
("10.1016/s0143-6228(00)00014-x", "Saiko & Zonn (2000)", "yes", "medium", "irrigation expansion consequences",
 "Documents desertification dynamics following large-scale irrigation expansion in the Aral region", "Not a suitability assessment", "Motivates the refusal to equate river discharge with allocable irrigation water"),
("10.7717/peerj.1366", "Malone et al. (2015)", "added", "high", "threshold/input uncertainty in land suitability",
 "Propagating input uncertainty changes an enterprise suitability assessment from 56% suitable (error-free) to mostly unsuitable in simulations", "Input-error uncertainty, not reference construction or spatial support",
 "Complements input uncertainty with reference-construction uncertainty of a single binding threshold"),
("10.1007/s00267-022-01764-y", "Snelder et al. (2023)", "added", "medium", "suitability as a relational, not intrinsic, property",
 "Land-use suitability evaluated with productive potential, relative contribution and pressure indicators; suitability depends on receiving environments", "Nitrogen/water-quality focus; no climate-threshold transfer",
 "Supports framing suitability as dependent on the reference and context in which it is defined"),
("10.1371/journal.pone.0107522", "Zabel et al. (2014)", "yes", "high", "global high-resolution crop suitability incl. rice",
 "Global fuzzy-logic suitability for 16 crops at 30″ including irrigated areas, current and future climate", "No system-specific (cold-region japonica) transfer reference; no decomposition of threshold construction",
 "System-specific calibration of the thermal bound and explicit irrigation-infrastructure gate"),
("10.5194/gmd-18-1067-2025", "Zabel et al. (2025)", "no (context only)", "medium", "crop-suitability model, climate variability, downscaling",
 "CropSuite: open-source crop suitability model including climate variability and spatial downscaling", "General model; not a decomposition of a transferred threshold", "Positions the decomposition as complementary to model-based suitability"),
("10.1038/s41467-020-15076-4", "Sloat et al. (2020)", "added", "high", "crop migration as adaptation",
 "Global rainfed crop-area migration (1973–2012) has moderated growing-season warming exposure; irrigation expansion also contributed", "Observed migration, not a forward screen; no gate separation", "Forward pre-feasibility screen for transfer of a system; separates thermal and infrastructure constraints"),
("10.1038/s41598-018-26321-8", "King et al. (2018)", "added", "medium", "GDD-based northward shift of agricultural climate zones",
 "Uses GDD thresholds with GCM scenarios to delineate northward expansion of small-cereal climate zones", "Single climate gate; threshold taken as fixed", "Shows that the GDD threshold itself depends on how the reference is constructed"),
("10.1038/ncomms12608", "Pugh et al. (2016)", "no (context only)", "low", "climate analogues for crop potential",
 "Climate analogues combined with attainable yields suggest limited intensification potential on current cropland", "Analogue climate, not system transfer with infrastructure", "Context only"),
("10.1007/bf02447512", "Jelinski & Wu (1996)", "yes", "high", "MAUP",
 "Classic statement of the modifiable areal unit problem for landscape ecology", "—", "Separates resolution/aggregation (MAUP) from reference-construction effects and shows the latter dominate here"),
("10.5194/hess-19-1521-2015", "Siebert et al. (2015)", "no (data context)", "medium", "irrigation-infrastructure mapping",
 "Historical gridded area equipped for irrigation 1900–2005 at 5′", "Equipment extent, not water availability or rice readiness", "Uses AEI only as a screening gate and states its limits"),
]
rows = []
for doi, cite, inms, cl, dim, dem, no, this in S:
    r = rec(doi); r |= dict(short_citation=cite, cited_in_manuscript=inms, closeness=cl, dimensions=dim, what_it_demonstrates=dem, what_it_does_not=no, contribution_of_this_study=this); rows.append(r)
df = pd.DataFrame(rows)[["short_citation", "doi", "title_record", "venue_record", "year_record", "bib_source", "content_source", "cited_in_manuscript", "closeness", "dimensions", "what_it_demonstrates", "what_it_does_not", "contribution_of_this_study"]]
df.to_csv(os.path.join(FA, "CLOSEST_PRIOR_STUDIES_MATRIX_FINAL.csv"), index=False)
nv = (df.content_source == "NOT VERIFIED BEYOND TITLE/BIBLIOGRAPHY").sum(); nag = (df.venue_record == "Applied Geography").sum()
md = f"""# Geographic novelty and prior-work audit

Generated by `modern_rice/scripts/ag_prior_work_matrix.py`. Matrix: `CLOSEST_PRIOR_STUDIES_MATRIX_FINAL.csv` ({len(df)} studies; {nag} in Applied Geography; {len(df)-nv} with content verified from a saved publisher abstract/highlights or an indexed abstract; {nv} verified only bibliographically).

Search record: OpenAlex queries (saved as `search_*.json`) restricted to Applied Geography (source S115443327) and unrestricted, on: crop suitability × spatial resolution; land suitability × threshold uncertainty; irrigation infrastructure mapping; MAUP × agriculture; northward crop expansion; rice suitability mapping; spatial decision support; climate-analogue transfer. Bibliographic metadata from Crossref/OpenAlex; content from ScienceDirect pages captured through the browser and from Semantic Scholar abstracts.

## Closest studies and what they leave open

""" + "\n".join(f"* **{r.short_citation}** ({r.venue_record}; closeness {r.closeness}) – {r.what_it_demonstrates}. Open: {r.what_it_does_not}. Content source: {r.content_source.split(' (')[0]}." for r in df.itertuples()) + f"""

## Assessment

1. Threshold- and model-based mapping of rice limits (Yang et al., 2023), observed cold-margin paddy expansion (Liu et al., 2022; Gao & Liu, 2011) and global suitability (Zabel et al., 2014) already exist; a suitability map of rice in Europe would not be novel.
2. Sensitivity of suitability to weights and inputs is established (Xu & Zhang, 2013; Tenerelli & Carver, 2012; Malone et al., 2015). What is not, in the studies found, is a controlled decomposition of a *transferred* cultivation-system reference into quantile, location, period, temporal aggregation, data source and spatial support. The German result (3% vs 97% on an identical surface) shows that these reference-construction choices, not grid resolution, dominate.
3. Water access binding before climate is reported for other systems (Cornwell et al., 2020; Schmitter et al., 2018); the present contribution is to show it with non-compensatory gates on an explicit 69.7 Mha denominator and with explicit domain sensitivity.
4. Residual novelty risk: moderate. The work is a careful geographic re-analysis rather than a new method. The contribution must be stated as (i) reference construction and spatial support of transferred thresholds, (ii) explicit denominators, (iii) non-compensatory infrastructure gates and (iv) the distinction between mapped suitability and operational feasibility.

## Contribution statement (manuscript and cover letter)

This study shows that the suitability of land for a transferred cultivation system depends on how the climatic reference is constructed – its quantile, location, period, temporal aggregation and data source – far more than on grid resolution; it reports exposure of an explicit land denominator to non-compensatory thermal and irrigation-infrastructure gates; and it separates mapped suitability from operational feasibility.
"""
open(os.path.join(FA, "GEOGRAPHIC_NOVELTY_AND_PRIOR_WORK_AUDIT.md"), "w").write(md)
print(df[["short_citation", "venue_record", "year_record", "bib_source", "content_source"]].to_string())
