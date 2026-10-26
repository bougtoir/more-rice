# MEDIEVAL RICE CLIMATE REASSESSMENT (Task 2)

## Method change

The previous audit used a single "July mean ≥ 20 °C" rule. This is replaced by a
sensitivity grid over agronomic parameter ranges (`scripts/climate_sensitivity.py`,
output `MEDIEVAL_RICE_CLIMATE_SENSITIVITY.csv`). Inputs are labeled by evidence
class: modern normals (class 1), historical reconstruction anomaly band
+0.0/+0.5/+1.0 °C (class 3, Luterbacher et al. 2016 ERL European summer
reconstruction — MCA peaks 10th c. and late 12th–early 13th c.), agronomic
threshold ranges (class 5).

Parameter ranges tested: warmest-month mean for flowering/grain formation
18–22 °C; growing degree days (base 10 °C) 1800–2600; frost-free period
110–150 days; seasonal rain ≥400 mm OR irrigation for water.

## Results (computed, see CSV)

| Region | Feasible combos | Verdict |
|---|---|---|
| England (S/SE) | 0% | **Infeasible across the whole parameter grid** — robust even at +1 °C MCA anomaly |
| Northern France | 0% feasible / 11% marginal | **Parametric-uncertain** — cannot be declared impossible; upland-only window at best |
| German territories | 0% | **Infeasible across grid** |
| Mediterranean France | 100% | **Feasible** (irrigation-conditioned) |
| Northern Iberia | 28% feasible / 17% marginal | **Parametric-uncertain** — coastal/valley microsites possible |
| Eastern Iberia (Valencia) | 100% | **Feasible** (irrigated) |
| Southern Iberia | 100% | **Feasible** (irrigated) |

## Reassessed findings

1. **England/Germany conclusion survives sensitivity analysis**: under every
   admissible combination of threshold, GDD, frost-free period and the warmest
   defensible MCA anomaly, rice does not reach feasibility. This is now a
   *range-based* statement, not a threshold artifact.

2. **Northern France and northern Iberia must be upgraded** from "infeasible"
   to **parametric-uncertain/marginal**: a warm MCA extreme plus a tolerant
   early cultivar plus a favorable microsite could in principle support a
   marginal upland crop. We report this as *uncertainty*, not as feasibility —
   no medieval cultivar performance data exist for this zone, so the spec's
   instruction ("where historical agronomic evidence is insufficient, report
   feasibility as uncertain") applies.

3. **Upland vs irrigated separated**: every "feasible" region in the grid is
   feasible *for irrigated rice*; nowhere north of the Mediterranean littoral
   is feasible for upland rice, which additionally needs reliable in-season
   rain AND the same thermal budget — and loses the weed-suppression benefit
   of flooding.

4. **What this changes in the audit**: non-adoption in England/Germany remains
   fully explained by climate; in northern France the climate explanation is
   weaker than claimed before (marginal, not impossible) — the knowledge and
   infrastructure barriers carry more of the explanatory load there.

5. **Not computed**: no historical yield estimates were produced; none are
   supportable.
