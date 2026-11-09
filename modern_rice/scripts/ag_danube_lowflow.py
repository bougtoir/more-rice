#!/usr/bin/env python3
"""Observed Lower Danube low-flow statistics replacing the unverified CT-UPT (2014) Q99.
Input: EStreams v1.4 streamflow indices (do Nascimento et al., 2024; Zenodo 10.5281/zenodo.17598150),
computed from GRDC daily mean discharge, units mm/d (specific discharge). Stations:
ROGR0001 = GRDC 6742200 Orsova (Drobeta-Turnu Severin until 1971), 1920-1990;
ROGR0002 = GRDC 6742201 Bazias (upstream of the Iron Gates reservoir), 1991-2008.
Daily series are not available, so the flow-duration Q99 cannot be computed; instead the
Jun-Sep minimum daily discharge per year (= min of Jun-Sep monthly minima of daily means)
and the Jun-Sep mean discharge are used. Demand: Q = A*D/T (net), gross = net/0.75."""
import os, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "..", "data", "raw", "hydrology")
OUT = os.path.join(HERE, "..", "..", "outputs", "modern_rice", "applied_geography")
IDX = os.path.join(RAW, "estreams_indices", "streamflow_indices", "monthly")
ST = {"ROGR0001": dict(name="Orsova (GRDC 6742200)", area_official=576232.0, area_estreams=568599.188, lat=44.70, lon=22.42),
      "ROGR0002": dict(name="Bazias (GRDC 6742201)", area_official=570896.0, area_estreams=563290.254, lat=44.8147, lon=21.3794)}
NET = 2.5e9 / (120 * 86400); GROSS = NET / 0.75
def load(f):
    d = pd.read_csv(os.path.join(IDX, f), index_col=0, usecols=lambda c: c in ST or c.startswith("Unnamed"))
    d.index = pd.to_datetime(d.index); return d
mn, mm = load("monthly_streamflow_min.csv"), load("monthly_streamflow_mean.csv")
rng = np.random.default_rng(20261108); rows, yrs_out = [], []
def boot(x, q):
    b = [np.quantile(rng.choice(x, len(x)), q) for _ in range(2000)]; return np.percentile(b, [2.5, 97.5])
for sid, s in ST.items():
    k = s["area_official"] * 1000 / 86400
    js = mn[sid][mn.index.month.isin([6, 7, 8, 9])].dropna()
    jm = mm[sid][mm.index.month.isin([6, 7, 8, 9])].dropna()
    g = js.groupby(js.index.year); full = g.size()[g.size() == 4].index
    smin = (g.min()[full] * k); smean = (jm.groupby(jm.index.year).mean()[full] * k)
    ann = mn[sid].dropna(); ag = ann.groupby(ann.index.year); afull = ag.size()[ag.size() == 12].index
    amin = ag.min()[afull] * k
    for y in full: yrs_out.append(dict(station=s["name"], year=y, JunSep_min_daily_m3s=round(smin[y]), JunSep_mean_m3s=round(smean[y]),
                                       gross_over_min=round(GROSS / smin[y], 3)))
    periods = {"all": full}
    if sid == "ROGR0001": periods.update({"1920-1971 (pre-Iron Gates I)": [y for y in full if y <= 1971], "1972-1990 (regulated)": [y for y in full if y >= 1972]})
    for lab, ys in periods.items():
        x = smin[list(ys)].values; xm = smean[list(ys)].values
        for stat, val, ci in [("JunSep_min_daily_median", np.median(x), boot(x, 0.5)), ("JunSep_min_daily_P10", np.quantile(x, 0.1), boot(x, 0.1)),
                              ("JunSep_min_daily_lowest", x.min(), [np.nan, np.nan]), ("JunSep_mean_median", np.median(xm), boot(xm, 0.5))]:
            rows.append(dict(station=s["name"], period=lab, n_years=len(x), statistic=stat, value_m3s=round(val), ci95_lo=round(ci[0]) if np.isfinite(ci[0]) else "",
                             ci95_hi=round(ci[1]) if np.isfinite(ci[1]) else "", net_pct=round(100 * NET / val, 1), gross_pct=round(100 * GROSS / val, 1),
                             area_sensitivity_pct=round(100 * (s["area_estreams"] / s["area_official"] - 1), 1)))
        if lab == "all":
            rows.append(dict(station=s["name"], period=lab, n_years=len(afull), statistic="annual_min_daily_median", value_m3s=round(np.median(amin)), ci95_lo="", ci95_hi="",
                             net_pct=round(100 * NET / np.median(amin), 1), gross_pct=round(100 * GROSS / np.median(amin), 1), area_sensitivity_pct=""))
            for t in [0.10, 0.20, 0.30]:
                rows.append(dict(station=s["name"], period=lab, n_years=len(x), statistic=f"share_years_gross_over_JunSep_min_gt_{int(t*100)}pct",
                                 value_m3s="", ci95_lo="", ci95_hi="", net_pct="", gross_pct=round(100 * np.mean(GROSS / x > t), 1), area_sensitivity_pct=""))
YR = os.path.join(RAW, "estreams_indices", "streamflow_indices", "yearly")
for sid, s in ST.items():
    k = s["area_official"] * 1000 / 86400
    for f, lab in [("yearly_streamflow_min7days.csv", "annual_7day_min"), ("yearly_streamflow_min.csv", "annual_min_daily")]:
        x = pd.read_csv(os.path.join(YR, f), index_col=0, usecols=lambda c: c == sid or c.startswith("Unnamed"))[sid].dropna().values * k
        for stat, val in [("median", np.median(x)), ("P10", np.quantile(x, 0.1)), ("lowest", x.min())]:
            rows.append(dict(station=s["name"], period="all", n_years=len(x), statistic=f"{lab}_{stat}", value_m3s=round(val), ci95_lo="", ci95_hi="",
                             net_pct=round(100 * NET / val, 1), gross_pct=round(100 * GROSS / val, 1), area_sensitivity_pct=""))
    js = mn[sid][mn.index.month.isin([6, 7, 8, 9])].dropna(); g = js.groupby(js.index.year); full = g.size()[g.size() == 4].index
    x = (g.min()[full] * k).values
    for m in ["linear", "lower", "median_unbiased", "weibull"]:
        rows.append(dict(station=s["name"], period="all", n_years=len(x), statistic=f"JunSep_min_daily_P10_estimator_{m}", value_m3s=round(np.quantile(x, 0.1, method=m)),
                         ci95_lo="", ci95_hi="", net_pct=round(100 * NET / np.quantile(x, 0.1, method=m), 1), gross_pct=round(100 * GROSS / np.quantile(x, 0.1, method=m), 1), area_sensitivity_pct=""))
res = pd.DataFrame(rows); res.to_csv(os.path.join(OUT, "HYDROLOGICAL_LOW_FLOW_RESULTS.csv"), index=False)
pd.DataFrame(yrs_out).to_csv(os.path.join(OUT, "HYDROLOGICAL_LOW_FLOW_BY_YEAR.csv"), index=False)
print(f"net={NET:.1f} gross={GROSS:.1f}"); print(res.to_string())
