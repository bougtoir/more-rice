#!/usr/bin/env python3
"""Medieval rice climate feasibility — sensitivity analysis (Task 2).

Replaces the single 20 C threshold with a parameter grid.
No hardcoded verdicts: every verdict is computed from documented input ranges.

Parameter classes (labeled per spec):
  [class 1] modern observed climate normals (approx. July means)
  [class 3] historical reconstruction: Luterbacher et al. 2016 ERL European
            summer reconstruction — MCA peaks 10th c. & late 12th-early 13th c.;
            anomaly range +0.0 to +1.0 C vs recent normals (uncertainty band)
  [class 5] agronomic thresholds: flowering-critical mean range and GDD, taken
            as RANGES with sensitivity, not single values.
"""
import csv, os, itertools

OUT = os.path.join(os.path.dirname(__file__), "..", "outputs",
                   "MEDIEVAL_RICE_CLIMATE_SENSITIVITY.csv")

# Agronomic requirement grid (documented ranges, S16/S17/S18):
#   flowering/grain-formation critical warmest-month mean temp: 18-22 C band
#   required growing degree days (base 10 C): 1800-2600 for early japonica
#   frost-free period needed: 110-150 days
FLOWER_MEAN_LO, FLOWER_MEAN_HI = 18.0, 22.0
GDD_LO, GDD_HI = 1800, 2600
FROSTFREE_LO, FROSTFREE_HI = 110, 150

# Region inputs: [July mean C (modern), est. GDD base-10 Apr-Oct, frost-free days,
#                 seasonal rain mm Apr-Oct, irrigation available?]
REGIONS = {
    "England (S/SE)":        dict(jul=16.5, gdd=1400, ff=150, rain=350, irrig=False),
    "Northern France":       dict(jul=18.5, gdd=1700, ff=170, rain=350, irrig=False),
    "German territories":    dict(jul=18.0, gdd=1600, ff=150, rain=400, irrig=False),
    "Mediterranean France":  dict(jul=24.5, gdd=2900, ff=220, rain=150, irrig=True),
    "Northern Iberia":       dict(jul=19.5, gdd=1900, ff=200, rain=500, irrig=False),
    "Eastern Iberia (Valencia)": dict(jul=25.5, gdd=3100, ff=250, rain=100, irrig=True),
    "Southern Iberia":       dict(jul=26.5, gdd=3300, ff=280, rain=80,  irrig=True),
}

MCA_ANOMALY = [0.0, 0.5, 1.0]  # degC, reconstruction band (Luterbacher 2016)

def classify(r, anomaly, flower_thresh, gdd_req, ff_req):
    jul = r["jul"] + anomaly
    gdd = r["gdd"] + anomaly * 180  # rough: +1C ~ +180 GDD over season
    temp_ok = jul >= flower_thresh
    gdd_ok = gdd >= gdd_req
    ff_ok = r["ff"] >= ff_req
    water_ok = r["irrig"] or r["rain"] >= 400  # upland needs ~reliable in-season rain
    if temp_ok and gdd_ok and ff_ok and water_ok:
        return "feasible"
    if (jul >= flower_thresh - 2.0) and gdd_ok and ff_ok:
        return "marginal"
    return "infeasible"

def main():
    rows = []
    for region, r in REGIONS.items():
        counts = {"feasible": 0, "marginal": 0, "infeasible": 0}
        combos = list(itertools.product(
            MCA_ANOMALY, [FLOWER_MEAN_LO, (FLOWER_MEAN_LO+FLOWER_MEAN_HI)/2,
                          FLOWER_MEAN_HI],
            [GDD_LO, GDD_HI], [FROSTFREE_LO, FROSTFREE_HI]))
        for a, ft, gr, fr in combos:
            counts[classify(r, a, ft, gr, fr)] += 1
        n = len(combos)
        rows.append({
            "region": region,
            "pct_feasible": round(100*counts["feasible"]/n),
            "pct_marginal": round(100*counts["marginal"]/n),
            "pct_infeasible": round(100*counts["infeasible"]/n),
            "verdict": (
                "feasible across parameter grid" if counts["feasible"] == n
                else "infeasible across parameter grid" if counts["infeasible"] == n
                else "marginal/parametric-uncertain"),
            "irrigated_required": not (r["rain"] >= 400),
        })
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    for r in rows:
        print(f'{r["region"]}: {r["verdict"]} '
              f'(feasible {r["pct_feasible"]}%, marginal {r["pct_marginal"]}%, '
              f'infeasible {r["pct_infeasible"]}%) irrig_req={r["irrigated_required"]}')

if __name__ == "__main__":
    main()
