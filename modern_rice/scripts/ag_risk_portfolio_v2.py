#!/usr/bin/env python3
"""Food-supply tail-risk scenarios, corrected and sensitivity-tested.

Correction vs risk_portfolio.py: for countries without an own FAOSTAT rice
yield series, the original script used an analog rice *shock* series but the
country's own (missing) rice *yield level*, so rice contributed nothing and
scenario B collapsed to 0.8 x A. Here an analog country supplies both the
shock series and the yield level, and such rows are flagged
evidence_class = 'analog' (lower evidence than 'own').

Sensitivity grid: substitution share f in {0.1,0.2,0.3}; detrending
{linear, quadratic}; rice yield level scale {1.0, 0.75} (yield penalty for
expansion beyond current rice districts); shortfall threshold relative to
{own scenario mean (as original), baseline A mean}. Moving-block bootstrap
(block 3 yr, 2000 draws) gives a 95% interval for P_B - P_A.
Rice yields are converted from paddy to milled equivalent (x0.67) before
applying the milled-rice energy density.
Outputs are modeled scenario statistics, not observed food-crisis incidence.
"""
import os, numpy as np, pandas as pd
HERE = os.path.dirname(__file__)
RAW = os.path.join(HERE, "..", "data", "raw")
OUT = os.path.join(HERE, "..", "..", "outputs", "modern_rice", "applied_geography")
os.makedirs(OUT, exist_ok=True)
import importlib.util
spec = importlib.util.spec_from_file_location("rp_cfg", os.path.join(HERE, "risk_portfolio.py"))
_src = open(os.path.join(HERE, "risk_portfolio.py")).read().split("d = pd.read_csv")[0]
cfg = {"__file__": os.path.join(HERE, "risk_portfolio.py")}; exec(compile(_src, "risk_portfolio_cfg", "exec"), cfg)
KCAL, COUNTRIES, ANALOG, F = cfg["KCAL"], cfg["COUNTRIES"], cfg["ANALOG"], cfg["F"]
d = pd.read_csv(F, usecols=["Area", "Item", "Element", "Year", "Value"], low_memory=False)
d = d[d.Area.isin(set(COUNTRIES) | set(ANALOG.values())) & d.Item.isin(KCAL)]
yld = d[d.Element == "Yield"].pivot_table(index=["Area", "Item", "Year"], values="Value").reset_index()
area = d[d.Element == "Area harvested"]
latest = yld.sort_values("Year").groupby(["Area", "Item"]).Value.last()
ares = area.sort_values("Year").groupby(["Area", "Item"]).Value.last()

def resid(deg):
    R = {}
    for (a, i), g in yld.groupby(["Area", "Item"]):
        if len(g) < 12: continue
        x = g.Year.values.astype(float); y = np.log(np.clip(g.Value.values, 1, None))
        b = np.polyfit(x - x.mean(), y, deg)
        R[(a, i)] = pd.Series(y - np.polyval(b, x - x.mean()), index=g.Year.values)
    return R

rng = np.random.default_rng(20261108)
MILL = 0.67  # FAOSTAT rice yield is paddy; KCAL["Rice"] is per g milled rice (milling extraction ~0.67)
def pshort(x, thr): return float((x < thr).mean())
rows = []
for deg, dname in [(1, "linear"), (2, "quadratic")]:
    R = resid(deg)
    for c in COUNTRIES:
        mains = [i for i in ["Wheat", "Barley", "Maize (corn)"] if (c, i) in R]
        if not mains: continue
        if (c, "Rice") in R and len(R[(c, "Rice")]) >= 15 and np.isfinite(latest.get((c, "Rice"), np.nan)):
            rs, rlev, src, ev = R[(c, "Rice")], latest[(c, "Rice")], c, "own"
        elif ANALOG.get(c) and (ANALOG[c], "Rice") in R:
            a = ANALOG[c]; rs, rlev, src, ev = R[(a, "Rice")], latest[(a, "Rice")], "analog:" + a, "analog"
        else: continue
        sh = {i: ares.get((c, i), np.nan) for i in mains}
        tot = np.nansum(list(sh.values()))
        sh = {i: (v / tot if np.isfinite(v) else 1 / len(mains)) for i, v in sh.items()}
        yrs = sorted(set.intersection(*[set(R[(c, i)].index) for i in mains]) & set(rs.index))
        if len(yrs) < 12: continue
        base = np.array([sum(sh[i] * latest[(c, i)] * np.exp(R[(c, i)][y]) * KCAL[i] for i in mains) for y in yrs])
        pot = None
        if (c, "Potatoes") in R:
            pr = R[(c, "Potatoes")]
            pot = np.array([latest[(c, "Potatoes")] * np.exp(pr.get(y, 0.0)) * KCAL["Potatoes"] for y in yrs])
        for scale in [1.0, 0.75]:
            rice = np.array([scale * MILL * rlev * np.exp(rs[y]) * KCAL["Rice"] for y in yrs])
            for f in [0.1, 0.2, 0.3]:
                A = base; B = (1 - f) * base + f * rice
                D = (1 - f) * base + f * pot if pot is not None else None
                for tb in ["own_mean", "baseline_mean"]:
                    def P(x): return pshort(x, 0.8 * (x.mean() if tb == "own_mean" else A.mean()))
                    n = len(yrs); nb = int(np.ceil(n / 3)); diffs = []
                    for _ in range(2000):
                        st = rng.integers(0, n - 2, nb); idx = np.concatenate([np.arange(s, s + 3) for s in st])[:n]
                        a_, b_ = A[idx], B[idx]
                        ta = 0.8 * a_.mean(); tbv = 0.8 * (b_.mean() if tb == "own_mean" else a_.mean())
                        diffs.append((b_ < tbv).mean() - (a_ < ta).mean())
                    rows.append(dict(country=c, evidence_class=ev, rice_source=src, n_years=n, detrend=dname,
                                     rice_yield_scale=scale, f=f, threshold_basis=tb,
                                     P_A=round(P(A), 3), P_B_rice=round(P(B), 3),
                                     P_D_potato=round(P(D), 3) if D is not None else np.nan,
                                     diff_B_minus_A=round(P(B) - P(A), 3),
                                     diff_CI95_lo=round(np.percentile(diffs, 2.5), 3),
                                     diff_CI95_hi=round(np.percentile(diffs, 97.5), 3),
                                     cv_A=round(A.std() / A.mean(), 3), cv_B=round(B.std() / B.mean(), 3)))
out = pd.DataFrame(rows)
out.to_csv(os.path.join(OUT, "RISK_PORTFOLIO_SENSITIVITY.csv"), index=False)
base = out[(out.detrend == "linear") & (out.rice_yield_scale == 1.0) & (out.f == 0.2) & (out.threshold_basis == "own_mean")]
base.to_csv(os.path.join(OUT, "RISK_PORTFOLIO_BASELINE_CORRECTED.csv"), index=False)
print(base[["country", "evidence_class", "n_years", "P_A", "P_B_rice", "P_D_potato", "diff_CI95_lo", "diff_CI95_hi"]].to_string())
# robustness: share of sensitivity cells in which B < A, by country
rob = out.groupby(["country", "evidence_class"]).apply(lambda g: pd.Series({"n_cells": len(g), "share_B_lt_A": round((g.diff_B_minus_A < 0).mean(), 3), "share_CI_excl_0": round((g.diff_CI95_hi < 0).mean(), 3), "share_D_le_B": round((g.P_D_potato <= g.P_B_rice).mean(), 3)}), include_groups=False).reset_index()
rob.to_csv(os.path.join(OUT, "RISK_PORTFOLIO_ROBUSTNESS.csv"), index=False)
print(rob.to_string())
