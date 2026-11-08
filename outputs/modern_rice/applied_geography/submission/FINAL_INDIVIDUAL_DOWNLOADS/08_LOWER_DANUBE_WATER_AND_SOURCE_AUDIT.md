# Lower Danube water gate — arithmetic and source audit
Verdict: **DEMAND PASS; Q99 SOURCE UNVERIFIED → HOLD**

## Independent arithmetic
V = 250,000 ha × 10⁴ m²/ha × 1.000 m = 2.50 × 10⁹ m³. T = 120 d × 86,400 s/d = 1.0368 × 10⁷ s. Q = V/T = **241.1 m³/s** (net field requirement). The pipeline value (241 m³/s) uses exactly these assumptions (`ag_danube_demand.py`: `A*1e4*D_mm/1000/(days*86400)`). The legacy ~24 m³/s was a factor-of-10 error.
- Gross abstraction at conveyance efficiency 0.75: 321 m³/s; at 0.6: 402 m³/s. Return flows (percolation/drainage) partly re-enter the river downstream; not modelled.
- Temporal demand: the 120-day continuous equivalent understates peak demand during land soaking/puddling.
- Ratio to reported mean discharge 5,420 m³/s: 4.4%; to reported 1,100 m³/s: 21.9%.

## Source verification
- The values (mean 5,420; "minimum flow with 90/95/99% certainty" 1,460/1,320/1,100 m³/s; annual stock 174 × 10⁹ m³) come from the project registry `LOWER_DANUBE_HYDROLOGY_SOURCE_REGISTRY.csv`, entry "CT-UPT Iron Gates ecohydrology (2014)", tagged "peer-reviewed" in an earlier session.
- Searches on 2026-11-08 (Crossref bibliographic queries; web search) did not locate the primary document, its author list, the gauge (Iron Gates I / Orsova / Drobeta), the period or the exceedance definition. **The existence and content of this source are therefore unconfirmed.** "Minimum flow with 99% certainty" may be a duration-curve or annual-minimum statistic; it is not confirmed to equal Q99.
- Manuscript action taken: the 1,100 m³/s value is now described as "a reported low-flow statistic", explicitly stated as not confirmed against the primary document; ratios are "indicative only"; the text states that river discharge is not allocable irrigation water (environmental flow, navigation, hydropower, existing abstractions; the demand would sit on tributaries/canal commands rather than at the gauge).
- Required evidence to lift HOLD: the CT-UPT primary document (or an alternative citable source such as GRDC/INHGA station statistics for Orsova/Iron Gates with period and exceedance definition). If no source is produced, remove the Q99 ratio and keep only the absolute demand (241 m³/s) and the mean-discharge comparison from a verified source.
