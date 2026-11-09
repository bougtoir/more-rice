#!/usr/bin/env python3
"""Lower Danube mainstem check: seasonal paddy water demand vs Iron Gates
observed Orsova (GRDC 6742200) Jun-Sep low flows from ag_danube_lowflow.py
(EStreams/GRDC, 1920-1990).
Demand is the continuous equivalent Q = A*D/T. This compares mainstem flow
only; it says nothing about allocation, conveyance or water rights."""
import os, pandas as pd
HERE = os.path.dirname(__file__); MR = os.path.join(HERE, "..", "..", "outputs", "modern_rice")
lf = pd.read_csv(os.path.join(MR, "applied_geography", "HYDROLOGICAL_LOW_FLOW_RESULTS.csv"))
o = lf[(lf.station.str.startswith("Orsova")) & (lf.period == "all")].set_index("statistic").value_m3s.astype(float)
lf_med, lf_p10, mean_q = o["JunSep_min_daily_median"], o["JunSep_min_daily_P10"], o["JunSep_mean_median"]
rows = []
for D_mm in [800, 1000, 1200]:
    for days in [120, 150]:
        for A in [10000, 50000, 100000, 250000]:
            q = A * 1e4 * D_mm / 1000 / (days * 86400)
            rows.append(dict(area_ha=A, seasonal_depth_mm=D_mm, season_days=days, demand_m3s=round(q, 1),
                             pct_of_lowflow_median=round(100 * q / lf_med, 1), pct_of_lowflow_P10=round(100 * q / lf_p10, 1), pct_of_mean=round(100 * q / mean_q, 2)))
out = pd.DataFrame(rows); out.attrs = {}
out.to_csv(os.path.join(MR, "applied_geography", "DANUBE_DEMAND_VS_LOWFLOW.csv"), index=False)
print(f"JunSep mean={mean_q} min-daily median/P10={lf_med}/{lf_p10}"); print(out[(out.seasonal_depth_mm == 1000) & (out.season_days == 120)].to_string())
