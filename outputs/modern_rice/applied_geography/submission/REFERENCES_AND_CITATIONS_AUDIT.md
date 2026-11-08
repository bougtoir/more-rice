# References and citations audit (G5)

- Style: APA 7th edition. Entries are alphabetical, and datasets are tagged [dataset].
- The list has 31 references. A script checks that every reference is cited in the text and that every author–year citation appears in the list (after the fix, no uncited references and no missing ones).
- Metadata were verified against Crossref (journal DOIs) and DataCite (IFPRI Dataverse 10.7910/DVN/PRFF8V; Zenodo 10.5281/zenodo.7491458) on 2026-11-08. Authors, year, volume, issue and pages were checked against the API records.

## Errors in the Agricultural Systems reference list (corrected here)
| AgSys entry | Problem | Correction |
|---|---|---|
| White, Hoogenboom, Stackhouse & Hoell (2011), Comput. Electron. Agric. 79(2) | **Chimera.** The cited title is Bai et al. (2010), *Agronomy Journal* 102(1), 9–16, doi:10.2134/agronj2009.0085. The DOI 10.1016/j.compag.2011.10.003 is an unrelated paper. | Bai et al. (2010) |
| You et al. (2014), Earth Syst. Sci. Data 6, 73–88 | Wrong venue/DOI. The title is in *Agricultural Systems* 127, 53–60 (doi:10.1016/j.agsy.2014.01.002). | Replaced by Yu et al. (2020) ESSD and the IFPRI (2019) dataset |
| van Oort & Zwart (2018) | Issued online in 2017, volume 24 (2018) | Not cited in the AG version |

## Grey or institutional sources (flagged)
- CT-UPT (2014), the Iron Gates eco-hydrology report, has no DOI. The values come from the project registry `LOWER_DANUBE_HYDROLOGY_SOURCE_REGISTRY.csv`. **The author should re-verify against the original document before submission.**
- MAFF (2024): an institutional statistics portal.
- Guglielmo et al. (2025) is in MDPI *Agriculture*. The author list on Crossref has given names that look like surnames ("Pietro, D. M.", "Andrea, C."). This is reproduced as registered, but should be checked against the article PDF.
