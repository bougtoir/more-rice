# Gate 2 — Daily Climate Risk Validation (NASA POWER 2000–2024)

Daily T2M_MAX/T2M_MIN/PRECTOTCORR for 17 control+candidate points (fetch_nasa_power.py). Metrics: seasonal GDD10 (Jun–Sep NH / Dec–Mar SH), cold-snap nights (Tmin<12°C), hot days >35°C, frost-free days, minimum-year GDD10. Table: DAILY_CLIMATE_POINT_METRICS.csv.

Verdicts:
- England 722 GDD / 91 cold nights; N. France 983/71; Germany 899/73 → INFEASIBLE (monthly-mean result confirmed by daily data).
- Central Chile 766/103 → OVERTURNED: previous monthly-mean candidate is infeasible.
- Lower Danube 1750/20, Danube Delta 1678/11, Kherson 1672/22, Osijek 1606/27 → marginal-feasible (cold-snap counts flag reproductive risk; japonica-type varieties needed).
- Tashkent 2129/11 (+53 hot days) → thermally feasible.
- Hokkaido 903/69 → fails thresholds yet rice is grown (ultra-early japonica + transplanting): documented exception — model under-predicts at the cold extreme.
- Camargue 1677/8, Ebro 1390/46, Po ~1556/19 → consistent with existing cultivation.

Daily data therefore both confirms the thermal verdict and adds the reproductive-cold layer reviewers required.
