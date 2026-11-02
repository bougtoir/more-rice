# Graphical Abstract — Source Map

Every label/number → manuscript section and canonical source.

| Element | Claim shown | Manuscript section | Canonical source |
|---|---|---|---|
| Panel 1 title "Technology changes feasibility" | climate-only screen fails; management enables | §3.2 Hokkaido false-negative analysis | Phase 5 Hokkaido audit |
| "~900 GDD10 (Jun–Sep)" | empirical lower bound for ultra-early japonica + heated nursery + transplant + warm-water system | §3.2, Methods §2.2 (GDD10 definition) | DAILY_CLIMATE_POINT_METRICS.csv (Hokkaido 903, Asahikawa 901, Morioka 1136); labeled system-specific, NOT universal |
| "Hokkaido OBSERVED" | existing commercial rice region | §3.2 | NARO/observed cultivation |
| "European candidate cells (Rhine, Alsace, Loire, Saxony…) hypothetical transfer — field validation required" | B-tier cells exceed ~900 GDD10 but lack cultivar pool + management infrastructure | §3.3 | DAILY_CLIMATE_POINT_METRICS.csv (Rhine 957, Alsace 1080, Loire 1108, Berlin 1089, Saxony 969) |
| Panel 2 three systems | irrigated lowland / rainfed upland / supplemental irrigation | §3.4–3.5 | upland_water_balance.py outputs |
| "conditional in Lower Danube — delivery & infrastructure, not discharge" | river discharge ≈2% of Q99 demand; allocation is the constraint | §3.4 | LOWER_DANUBE_HYDROLOGY_SOURCE_REGISTRY.csv |
| "modeled flowering moisture deficit 88–100% of yrs (continental EU cells)" | modeled soil-water deficit frequency | §3.5 | DAILY_SOIL_WATER_BALANCE.csv (Lower Danube 100%, Osijek 100%, Kherson 100%, Loire 100%, Beauce 100%, Berlin 88%); Nordic/Baltic 64–84% omitted from graphic to avoid range mixing (documented in QC) |
| "deficits are modeled soil-moisture shortfalls, not observed crop failure" | scope qualifier | §3.5 limitations | model caveat registry |
| Panel 3 wheat alone vs wheat + rice | portfolio diversification only helps under low joint-failure dependence | §3.6 | FOOD_SECURITY_TAIL_RISK.csv |
| "Romania 20.3% → 10.9%; Kazakhstan 21.2% → 3.0%" | modeled severe-shortfall probabilities under B_rice20 scenario | §3.6 | FOOD_SECURITY_TAIL_RISK.csv; labeled scenario outcomes, not observed famine |
| "Serbia — potato outperforms rice" | mandatory non-rice comparator | §3.6 | FOOD_SECURITY_TAIL_RISK.csv (potato 0.053 vs rice 0.211) |
| Conclusion strip | conditional resilience; field trials only at selected irrigated sites; no universal claim | §4 Discussion, §5 Conclusions | manuscript conclusions |
| Legend observed/modeled/hypothetical | evidence-tier distinction used throughout | throughout | CLAIM_EVIDENCE_MATRIX.csv tiers |

No element depicts: dead crops, observed yield collapse, a European map shaded as established rice region, farm-level irrigation proof from river discharge, or global feasibility.
