#!/usr/bin/env python3
"""Lower Danube mainstem check: seasonal paddy water demand vs Iron Gates
low-flow statistics. The flow statistics come from the literature-extracted
registry outputs/modern_rice/LOWER_DANUBE_HYDROLOGY_SOURCE_REGISTRY.csv.
Demand is the continuous equivalent Q = A*D/T. This compares mainstem flow
only; it says nothing about allocation, conveyance or water rights."""
import os, pandas as pd
HERE = os.path.dirname(__file__); MR = os.path.join(HERE, "..", "..", "outputs", "modern_rice")
reg = pd.read_csv(os.path.join(MR, "LOWER_DANUBE_HYDROLOGY_SOURCE_REGISTRY.csv"))
mean_q = float(reg.loc[reg.datum.str.startswith("mean discharge"), "value"].iloc[0].split()[0])
q90, q95, q99 = [float(x) for x in reg.loc[reg.datum.str.startswith("min flow"), "value"].iloc[0].split()[0].split("/")]
rows = []
for D_mm in [800, 1000, 1200]:
    for days in [120, 150]:
        for A in [10000, 50000, 100000, 250000]:
            q = A * 1e4 * D_mm / 1000 / (days * 86400)
            rows.append(dict(area_ha=A, seasonal_depth_mm=D_mm, season_days=days, demand_m3s=round(q, 1),
                             pct_of_Q99=round(100 * q / q99, 1), pct_of_Q95=round(100 * q / q95, 1), pct_of_mean=round(100 * q / mean_q, 2)))
out = pd.DataFrame(rows); out.attrs = {}
out.to_csv(os.path.join(MR, "applied_geography", "DANUBE_DEMAND_VS_LOWFLOW.csv"), index=False)
print(f"mean={mean_q} Q90/95/99={q90}/{q95}/{q99}"); print(out[(out.seasonal_depth_mm == 1000) & (out.season_days == 120)].to_string())
