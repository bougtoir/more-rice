# CT-UPT (2014) source resolution

**Status: CT-UPT (2014): PRIMARY SOURCE NOT VERIFIED**

Bounded search on 2026-11-08 (UTC). Every substantive attempt is listed; nothing was obtained behind authentication.

| ID | Search | Result | Outcome |
|---|---|---|---|
| S01 | Project registry outputs/modern_rice/LOWER_DANUBE_HYDROLOGY_SOURCE_REGISTRY.csv | Entry 'CT-UPT Iron Gates ecohydrology (2014)': mean 5,420; 'min flow 90/95/99% certainty' 1,460/1,320/1,100 m3/s; tier 'peer-reviewed'. No author, title, URL, station, period or page. | No locator; tier label unsupported |
| S02 | Git history and full-repository grep (CT-UPT, Iron Gates, 1460, Orsova) | Only the registry, the manuscript reference string and derived audits; no source document, URL or download. | Not found |
| S03 | Raw-data store modern_rice/data/raw and private release more-rice-raw-2026-11-08 | No CT-UPT document among stored raw files. | Not found |
| S04 | Crossref query 'Iron Gates reservoir eco-hydrological assessment Danube' | Top hits: Sedimentation in Iron Gates Reservoir (J. Hydraulics Div., 1980) and discussions; archaeology. No 2014 assessment. | Not found |
| S05 | Crossref query 'Politehnica Timisoara Iron Gates hydrology' (from 2005) | Unrelated civil-engineering/flood-risk papers. | Not found |
| S06 | Crossref query 'Iron Gates Danube low flow discharge Orsova' (from 2005) | Mares et al. (2019) Hydrological Sciences Journal 65, 371-386, doi:10.1080/02626667.2019.1699244 (statistical predictors of Orsova discharge). Full text not obtained; a forecasting study, not a source of the 90/95/99% values. | Candidate rejected (different purpose) |
| S07 | Crossref query 'Danube Drobeta Turnu Severin minimum discharge probability' | Heavy-water-plant histories; floodplain restoration (Forum geografic 2011). No low-flow statistics. | Not found |
| S08 | Web search engines (DuckDuckGo HTML, Bing) via scripted HTTP for 'CT-UPT', '1100 m3/s' Iron Gates, '5420 m3/s' | No parsable results returned (automated access blocked). | Inconclusive |
| S09 | Wayback Machine ct.upt.ro (CDX and availability API) | Domain archived 2007-2026; homepage title 'Facultatea de Construcții Timișoara' (Faculty of Civil Engineering, Politehnica University of Timișoara). The reference expansion 'Center for Technology' is therefore not supported; no 2014 Iron Gates report located. | Institution clarified; document not found |
| S10 | ICPDR site search (icpdr.org) | HTTP 403 for automated request; not inspected. | Not accessible |
| S11 | Serbian RHMZ (hidmet.gov.rs) and Romanian INHGA/ANAR (inhga.ro) | Landing pages reachable (200/301); no openly downloadable historical daily Danube discharge archive identified within this bounded search. | No open data identified |
| S12 | GRDC portal and GRDC-Caravan v0.6 (Zenodo 15349031, CC BY 4.0) | GRDC daily series for 6742200/6742201 require a registered request under GRDC terms. GRDC-Caravan zip directory (5,377 entries, read by HTTP range) contains no Danube RO/RS/BG station. | Daily data not openly available |
| S13 | EStreams v1.4 (Zenodo 17598150; do Nascimento et al., 2024) | Catalogue lists ORSOVA (1971: DROBETA-TURNU SEVERIN) GRDC 6742200, 1920-1990, and BAZIAS 6742201, 1991-2008; daily-derived monthly/seasonal/yearly indices are distributed (CC BY-NC 4.0). | ADOPTED as observational replacement |

## Candidate record
| Field | CT-UPT (2014) as cited | Mares et al. (2019) |
|---|---|---|
| Bibliographic metadata | 'CT-UPT (2014). Eco-hydrological assessment of the Iron Gates reservoir, Lower Danube. Center for Technology, UPT' (no author, no locator) | Mares, I., Mares, C., Dobrica, V., Demetrescu, C. Hydrol. Sci. J. 65, 371-386 |
| Official/archival locator | none found | doi:10.1080/02626667.2019.1699244 |
| Full text obtained | no | no |
| Passage/table with statistic | not available | not applicable |
| Station/location | unknown (Iron Gates I? Orsova? Drobeta?) | Orsova |
| Observation period | unknown | not inspected |
| Statistic definition | 'minimum flow with 99% certainty' - undefined (flow-duration, annual-minimum frequency or return period?) | not applicable |
| Supports Q99 = 1,100 m3/s | cannot be assessed | no |
| Verification status | PRIMARY SOURCE NOT VERIFIED | rejected (different purpose) |

## Alternative interpretations checked
- Institution: ct.upt.ro is the Faculty of Civil Engineering (Construcții) of UPT, not a 'Center for Technology'; the expansion in the old reference was itself unsupported.
- Year/title: no 2014 document with a matching or translated title was found in Crossref or the archive checks above.
- Statistic: 1,100 m3/s is far below any flow-duration percentile plausible for Orsova but close to the lowest annual minimum daily discharge at Orsova 1920-1990 = 1,074 m3/s (1985); it is therefore more consistent with an annual-minimum frequency statistic than with a flow-duration Q99. This is an inference and was not used.
- Secondary citation: the registry was compiled in an earlier AI-assisted session; the value may originate from a secondary source that was not recorded.

## Decision
Case B/C: CT-UPT is unverified, daily data are not openly available, but authoritative daily-derived summary indices are. The 1,100 m3/s Q99, the 21.9%/29.2% ratios and the CT-UPT reference were removed. The comparison now uses observed June-September minimum daily discharge at Orsova (HYDROLOGICAL_LOW_FLOW_ANALYSIS.md). A flow-duration Q99 is not reported.

## GRDC request (optional, for the author)
To: GRDC (grdc@bafg.de) via the GRDC Data Portal. Stations 6742200 (Danube at Orsova) and 6742201 (Danube at Bazias); variable: daily mean discharge (m3/s) with quality flags; period: full record to latest available; purpose: non-commercial research on irrigation-demand ratios; no redistribution of raw data.
