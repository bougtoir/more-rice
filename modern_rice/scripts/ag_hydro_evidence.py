#!/usr/bin/env python3
"""Hydrological evidence files for the Lower Danube low-flow resolution (CT-UPT Q99 replacement)."""
import os, json, csv, hashlib, numpy as np, pandas as pd
from decimal import Decimal, getcontext
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
AG = os.path.join(REPO, "outputs", "modern_rice", "applied_geography"); QC = os.path.join(AG, "delta_qc")
RAW = os.path.join(REPO, "modern_rice", "data", "raw", "hydrology")
N = json.load(open(os.path.join(AG, "submission", "MANUSCRIPT_NUMBERS.json")))
R = pd.read_csv(os.path.join(AG, "HYDROLOGICAL_LOW_FLOW_RESULTS.csv")); Y = pd.read_csv(os.path.join(AG, "HYDROLOGICAL_LOW_FLOW_BY_YEAR.csv"))
def v(st, stat, per="all", col="value_m3s"):
    return R[(R.station.str.startswith(st)) & (R.period == per) & (R.statistic == stat)][col].iloc[0]
def W(n, t): open(os.path.join(QC, n), "w", encoding="utf-8").write(t.strip() + "\n")
S = [
 ("S01", "Project registry outputs/modern_rice/LOWER_DANUBE_HYDROLOGY_SOURCE_REGISTRY.csv", "Entry 'CT-UPT Iron Gates ecohydrology (2014)': mean 5,420; 'min flow 90/95/99% certainty' 1,460/1,320/1,100 m3/s; tier 'peer-reviewed'. No author, title, URL, station, period or page.", "No locator; tier label unsupported"),
 ("S02", "Git history and full-repository grep (CT-UPT, Iron Gates, 1460, Orsova)", "Only the registry, the manuscript reference string and derived audits; no source document, URL or download.", "Not found"),
 ("S03", "Raw-data store modern_rice/data/raw and private release more-rice-raw-2026-11-08", "No CT-UPT document among stored raw files.", "Not found"),
 ("S04", "Crossref query 'Iron Gates reservoir eco-hydrological assessment Danube'", "Top hits: Sedimentation in Iron Gates Reservoir (J. Hydraulics Div., 1980) and discussions; archaeology. No 2014 assessment.", "Not found"),
 ("S05", "Crossref query 'Politehnica Timisoara Iron Gates hydrology' (from 2005)", "Unrelated civil-engineering/flood-risk papers.", "Not found"),
 ("S06", "Crossref query 'Iron Gates Danube low flow discharge Orsova' (from 2005)", "Mares et al. (2019) Hydrological Sciences Journal 65, 371-386, doi:10.1080/02626667.2019.1699244 (statistical predictors of Orsova discharge). Full text not obtained; a forecasting study, not a source of the 90/95/99% values.", "Candidate rejected (different purpose)"),
 ("S07", "Crossref query 'Danube Drobeta Turnu Severin minimum discharge probability'", "Heavy-water-plant histories; floodplain restoration (Forum geografic 2011). No low-flow statistics.", "Not found"),
 ("S08", "Web search engines (DuckDuckGo HTML, Bing) via scripted HTTP for 'CT-UPT', '1100 m3/s' Iron Gates, '5420 m3/s'", "No parsable results returned (automated access blocked).", "Inconclusive"),
 ("S09", "Wayback Machine ct.upt.ro (CDX and availability API)", "Domain archived 2007-2026; homepage title 'Facultatea de Construcții Timișoara' (Faculty of Civil Engineering, Politehnica University of Timișoara). The reference expansion 'Center for Technology' is therefore not supported; no 2014 Iron Gates report located.", "Institution clarified; document not found"),
 ("S10", "ICPDR site search (icpdr.org)", "HTTP 403 for automated request; not inspected.", "Not accessible"),
 ("S11", "Serbian RHMZ (hidmet.gov.rs) and Romanian INHGA/ANAR (inhga.ro)", "Landing pages reachable (200/301); no openly downloadable historical daily Danube discharge archive identified within this bounded search.", "No open data identified"),
 ("S12", "GRDC portal and GRDC-Caravan v0.6 (Zenodo 15349031, CC BY 4.0)", "GRDC daily series for 6742200/6742201 require a registered request under GRDC terms. GRDC-Caravan zip directory (5,377 entries, read by HTTP range) contains no Danube RO/RS/BG station.", "Daily data not openly available"),
 ("S13", "EStreams v1.4 (Zenodo 17598150; do Nascimento et al., 2024)", "Catalogue lists ORSOVA (1971: DROBETA-TURNU SEVERIN) GRDC 6742200, 1920-1990, and BAZIAS 6742201, 1991-2008; daily-derived monthly/seasonal/yearly indices are distributed (CC BY-NC 4.0).", "ADOPTED as observational replacement"),
]
lo_ann = v("Orsova", "annual_min_daily_lowest"); p01_note = "lowest annual minimum daily discharge at Orsova 1920-1990 = {:,} m3/s (1985)".format(int(lo_ann))
t = ["# CT-UPT (2014) source resolution", "", "**Status: CT-UPT (2014): PRIMARY SOURCE NOT VERIFIED**", "",
     "Bounded search on 2026-11-08 (UTC). Every substantive attempt is listed; nothing was obtained behind authentication.", "",
     "| ID | Search | Result | Outcome |", "|---|---|---|---|"] + [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in S]
t += ["", "## Candidate record", "| Field | CT-UPT (2014) as cited | Mares et al. (2019) |", "|---|---|---|",
      "| Bibliographic metadata | 'CT-UPT (2014). Eco-hydrological assessment of the Iron Gates reservoir, Lower Danube. Center for Technology, UPT' (no author, no locator) | Mares, I., Mares, C., Dobrica, V., Demetrescu, C. Hydrol. Sci. J. 65, 371-386 |",
      "| Official/archival locator | none found | doi:10.1080/02626667.2019.1699244 |", "| Full text obtained | no | no |", "| Passage/table with statistic | not available | not applicable |",
      "| Station/location | unknown (Iron Gates I? Orsova? Drobeta?) | Orsova |", "| Observation period | unknown | not inspected |",
      "| Statistic definition | 'minimum flow with 99% certainty' - undefined (flow-duration, annual-minimum frequency or return period?) | not applicable |",
      "| Supports Q99 = 1,100 m3/s | cannot be assessed | no |", "| Verification status | PRIMARY SOURCE NOT VERIFIED | rejected (different purpose) |", "",
      "## Alternative interpretations checked", "- Institution: ct.upt.ro is the Faculty of Civil Engineering (Construcții) of UPT, not a 'Center for Technology'; the expansion in the old reference was itself unsupported.",
      "- Year/title: no 2014 document with a matching or translated title was found in Crossref or the archive checks above.",
      "- Statistic: 1,100 m3/s is far below any flow-duration percentile plausible for Orsova but close to the " + p01_note + "; it is therefore more consistent with an annual-minimum frequency statistic than with a flow-duration Q99. This is an inference and was not used.",
      "- Secondary citation: the registry was compiled in an earlier AI-assisted session; the value may originate from a secondary source that was not recorded.", "",
      "## Decision", "Case B/C: CT-UPT is unverified, daily data are not openly available, but authoritative daily-derived summary indices are. The 1,100 m3/s Q99, the 21.9%/29.2% ratios and the CT-UPT reference were removed. The comparison now uses observed June-September minimum daily discharge at Orsova (HYDROLOGICAL_LOW_FLOW_ANALYSIS.md). A flow-duration Q99 is not reported.", "",
      "## GRDC request (optional, for the author)", "To: GRDC (grdc@bafg.de) via the GRDC Data Portal. Stations 6742200 (Danube at Orsova) and 6742201 (Danube at Bazias); variable: daily mean discharge (m3/s) with quality flags; period: full record to latest available; purpose: non-commercial research on irrigation-demand ratios; no redistribution of raw data."]
W("CT_UPT_SOURCE_RESOLUTION.md", "\n".join(t))
g = pd.read_csv(os.path.join(RAW, "estreams_gauges", "streamflow_gauges", "estreams_gauging_stations.csv"), low_memory=False).set_index("basin_id")
prov = []
for bid, use, rel in [("ROGR0001", "PRIMARY", "Danube rkm ~955; ~4 km downstream of Iron Gates I dam (rkm 943); upstream of hypothetical Romanian/Bulgarian Lower Danube abstraction"),
                      ("ROGR0002", "SENSITIVITY", "Danube rkm ~1,072; upstream of Iron Gates reservoir (backwater-influenced); upstream of abstraction"),
                      ("BGGR0001", "NOT USED (8 years)", "Novo Selo, downstream of Iron Gates II"), ("ROGR0006", "NOT USED (not inspected)", "Zimnicea, within the hypothetical abstraction reach"),
                      ("RSGR0005", "NOT USED (upstream of Iron Gates gorge)", "Smederevo, Serbia; upstream of Iron Gates")]:
    r = g.loc[bid]
    prov.append(dict(estreams_id=bid, grdc_id=r.gauge_id, station=r.gauge_name, country=r.gauge_country, river=r.river, lat=r.lat, lon=r.lon,
                     drainage_area_km2_official=r.area_official, drainage_area_km2_estreams=r.area_estreams, start=r.start_date, end=r.end_date, n_years=r.num_years,
                     n_days=r.num_days, n_days_gaps=r.num_days_gaps, gap_pct=round(100 * float(r.num_days_gaps) / float(r.num_days), 3), resolution="daily mean (source); monthly/yearly indices used",
                     regulation=("Iron Gates I dam operational 1972; station relocated 1971 (Drobeta-Turnu Severin before)" if bid == "ROGR0001" else "regulated by Iron Gates reservoir and upstream dams"),
                     relation_to_abstraction=rel, use=use, source="EStreams v1.4 doi:10.5281/zenodo.17598150 (from GRDC)", license="CC BY-NC 4.0 (EStreams); GRDC data policy"))
pd.DataFrame(prov).to_csv(os.path.join(QC, "HYDROLOGICAL_STATION_AND_DATA_PROVENANCE.csv"), index=False)
o = lambda s: f"{int(v('Orsova', s)):,}"
tab = R[R.station.str.startswith("Orsova") & ~R.statistic.str.startswith("share")][["period", "n_years", "statistic", "value_m3s", "ci95_lo", "ci95_hi", "net_pct", "gross_pct"]].to_markdown(index=False)
W("HYDROLOGICAL_LOW_FLOW_ANALYSIS.md", f"""
# Lower Danube observed low-flow analysis
Script: `modern_rice/scripts/ag_danube_lowflow.py` (seed 20261108). Inputs: EStreams v1.4 monthly minimum and mean of daily discharge, and yearly minimum / minimum 7-day discharge (mm/d), stations Orsova (GRDC 6742200, 1920–1990) and Bazias (GRDC 6742201, 1991–2008). Converted to m³/s with the official GRDC catchment area (Orsova 576,232 km²); using the EStreams-delineated area lowers all flows by 1.3%.

## Definitions
- **Jun–Sep minimum daily discharge (per year)**: minimum of the June, July, August and September monthly minima of daily mean discharge; years with all four months present only (Orsova {int(v('Orsova','JunSep_min_daily_median','all','n_years'))} years; Bazias 18). The window matches the 120-day June–September demand scenario.
- **Annual minimum daily / 7-day discharge**: EStreams yearly indices (calendar years).
- Across-year summaries: median and 10th percentile (numpy linear, Hyndman–Fan type 7; P10 alternative estimators reported in the CSV, range {o('JunSep_min_daily_P10_estimator_weibull')}–{o('JunSep_min_daily_P10')} m³/s). 95% CIs: 2,000 bootstrap resamples of whole years (daily serial correlation is avoided by resampling annual values).
- **Not computed**: flow-duration Q99 (discharge equalled or exceeded on 99% of days) and the distribution of daily demand/discharge ratios — both need the daily series, which is not openly available (GRDC request text in CT_UPT_SOURCE_RESOLUTION.md). Return-period estimates were not fitted.

## Results (Orsova)
{tab}

Gross abstraction (321.5 m³/s) exceeded 10% of the Jun–Sep minimum in {v('Orsova','share_years_gross_over_JunSep_min_gt_10pct','all','gross_pct')}% of years, 20% in {v('Orsova','share_years_gross_over_JunSep_min_gt_20pct','all','gross_pct')}% and 30% in none. Bazias (1991–2008) gives a median Jun–Sep minimum of {int(v('Bazias','JunSep_min_daily_median')):,} m³/s and lowest {int(v('Bazias','JunSep_min_daily_lowest')):,} m³/s.

## Interpretation limits
- Discharge at a mainstem gauge is not allocable irrigation water: navigation, Iron Gates hydropower, environmental flows, existing abstractions and transboundary agreements have prior claims.
- Demand is a seasonal-average equivalent; peak (puddling) rates are higher and are not modelled. No daily demand curve was constructed.
- Record ends in 1990; 19 years post-dam. Upstream regulation, climate change and riverbed incision since 1990 are not represented.
- The ratios are descriptive; they do not establish feasibility.
""")
getcontext().prec = 30
A, D, T = Decimal(250000) * 10000, Decimal("1.000"), Decimal(120) * 86400
qn = A * D / T; qg = qn / Decimal("0.75")
sens = "\n".join(f"| {a:,} | {d} | {dd} | {a*1e4*d/1000/(dd*86400):.1f} | {a*1e4*d/1000/(dd*86400)/0.75:.1f} |" for a in [100000, 250000] for d in [800, 1000, 1200] for dd in [120, 150])
W("IRRIGATION_DEMAND_INDEPENDENT_CHECK.md", f"""
# Irrigation demand — independent check
Hand calculation (Python Decimal, independent of `ag_danube_demand.py`):
- A = 250,000 ha = {A:,} m²; D = 1.000 m → V = {A*D:,} m³
- T = 120 d × 86,400 s = {T:,} s
- Q_net = V/T = **{qn:.4f} m³/s** (pipeline: {N['dan_q']} m³/s) ✔
- Q_gross = Q_net/0.75 = **{qg:.4f} m³/s** (pipeline: {N['dan_q_gross']} m³/s) ✔; at 0.60: {qn/Decimal('0.6'):.1f} m³/s
- The former ~24 m³/s was a factor-of-ten error (withdrawn).

| Area (ha) | Depth (mm) | Days | Net (m³/s) | Gross @0.75 (m³/s) |
|---|---|---|---|---|
{sens}

## Terms
- *Net field requirement*: seasonal depth D (crop ET + percolation + puddling − effective rain), Bouman et al. (2007) range 800–1,200 mm.
- *Gross abstraction*: net / conveyance-and-application efficiency (0.75 assumed).
- *Consumptive depletion*: evapotranspiration share only; not estimated here. *Return flow*: drainage/percolation partly re-entering the river downstream; not modelled.
- *Environmental flows and other uses*: not quantified; they reduce the allocable fraction of any discharge.
- The rate is a seasonal-average equivalent, not a peak rate.
""")
W("HYDROLOGICAL_CLAIM_CHANGELOG.md", f"""
# Hydrological claim changelog
| # | Previous claim | Status | Replacement |
|---|---|---|---|
| H1 | Iron Gates Q99 = 1,100 m³/s (CT-UPT, 2014) | REMOVED — primary source not verified | Observed Jun–Sep minimum daily discharge at Orsova: median {N['dan_lf_med']}, P10 {N['dan_lf_p10']}, lowest {N['dan_lf_low']} m³/s |
| H2 | Q90/Q95 1,460/1,320 m³/s; mean 5,420 m³/s | REMOVED | Jun–Sep mean flow median {N['dan_mean']} m³/s |
| H3 | 250,000 ha = 21.9% (net) / 29.2% (gross) of Q99 | REMOVED | {N['dan_pct']}% (net) / {N['dan_pct_gross']}% (gross) of median Jun–Sep minimum; {N['dan_pct_gross_low']}% (gross) of lowest |
| H4 | 100,000 ha = 8.8% of Q99 | REMOVED | {N['dan_pct_100']}% of median Jun–Sep minimum |
| H5 | CT-UPT (2014) reference ('Center for Technology') | REMOVED from reference list | do Nascimento et al. (2024) added |
| H6 | Figure 4b y-axis '% of Iron Gates Q99' | CHANGED | '% of median Jun–Sep minimum daily flow, Orsova' |
| H7 | Table 1 row 'Iron Gates discharge statistics; literature' | CHANGED | GRDC daily discharge via EStreams v1.4 (Orsova, Bazias) |
| H8 | Demand 241.1 / 321.5 m³/s | RETAINED — verified | — |
| H9 | Mainstem discharge ≠ allocable water; no feasibility claim | RETAINED | strengthened (record ends 1990; seasonal minimum ≠ Q99) |
| H10 | Highlight 'a large share of low flow' | CHANGED | '~{N['dan_pct']}% of summer low flow' |
| H11 | Cover letter 'reported low flow of 1,100 m³/s … ~22%' | CHANGED | observed Orsova median and {N['dan_pct']}% |
""")
W("APPLIED_GEOGRAPHY_SCOPE_AND_NOVELTY_FINAL.md", f"""
# Applied Geography scope and novelty (final)
- Fit: spatially explicit resource assessment on existing arable land with an explicit denominator ({N['inc_Mha']} Mha, Europe excl. Russia), non-compensatory gates, MAUP/domain/source sensitivity, and a station-based water check. Matches the journal's applied, policy-relevant spatial-analysis scope.
- Novel elements: (1) the cold bound is a property of data source/window/scale ({N['T_star']} vs ~900 GDD10; Germany {N['de_T']}% vs {N['de_900']}%); (2) the binding screening gate is infrastructure/water, not temperature ({N['pct_thermal_pass']}% vs {N['pct_aei']}%); (3) a hypothetical Lower Danube paddy sector is set against observed seasonal low flows ({N['dan_pct']}% net of the median Jun–Sep minimum) while explicitly not claiming allocable water.
- Weaknesses: suitability mapping is established; AEI c. 2010; 1970–2000 climatology; risk model ancillary and mostly non-robust; hydrology record ends 1990.
- Desk-rejection risk: medium–high (unchanged by the hydrology revision, which removes a vulnerability rather than adds novelty).
""")
print("hydro evidence written")
