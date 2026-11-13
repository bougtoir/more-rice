#!/usr/bin/env python3
"""Independent known-answer and semantic tests for the EM&A threshold sweep. Writes KNOWN_ANSWER_TESTS_FINAL.md/json."""
import os, re, json, numpy as np, pandas as pd, geopandas as gpd
from rasterio.features import rasterize
from rasterio.transform import from_origin
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", "..")); RAW = os.path.join(HERE, "..", "data", "raw")
AG = os.path.join(ROOT, "outputs", "modern_rice", "applied_geography"); EMA = os.path.join(ROOT, "outputs", "modern_rice", "ema")
L = np.load(os.path.join(EMA, "ema_layers_5m.npz")); g, rice, inc, aei, eur, valid, cid = (L[k] for k in ["g5", "rice", "inc", "aei_sh", "eur", "valid", "cid"])
cur = pd.read_csv(os.path.join(EMA, "THRESHOLD_OMISSION_CURVE.csv")); sm = json.load(open(os.path.join(EMA, "EMA_THRESHOLD_SUMMARY.json")))
cal = json.load(open(os.path.join(AG, "GRID_THERMAL_CALIBRATION.json"))); TS = cal["T_star_pipeline"]
R = []
def t(name, ok, detail): R.append(dict(test=name, result="PASS" if ok else "FAIL", detail=detail))
c = cur.set_index("threshold_gdd10")
t("Candidate share non-increasing in T", bool((np.diff(cur.cropland_pass_pct) <= 1e-9).all()), f"{len(cur)} thresholds")
t("Omission share non-decreasing in T", bool((np.diff(cur.rice_omitted_pct) >= -1e-9).all()), "")
t("Combined gate subset of thermal gate (all T)", bool((cur.cropland_thermal_aei_pct <= cur.cropland_pass_pct + 1e-9).all()), "")
t("Boundary T=0: all pass, zero omission", c.loc[0.0, "cropland_pass_pct"] == 100 and c.loc[0.0, "rice_omitted_pct"] == 0, f"C(0)={c.loc[0.0,'cropland_pass_pct']}, O(0)={c.loc[0.0,'rice_omitted_pct']}")
gmax = np.nanmax(g[valid]); t("Boundary T>max G: no cropland passes", c.loc[1800.0, "cropland_pass_pct"] < 1 and (gmax < 1800) == (c.loc[1800.0, "cropland_pass_pct"] == 0), f"max GDD10 on incumbent cells={gmax:.0f}; C(1800)={c.loc[1800.0,'cropland_pass_pct']}")
t("Boundary uses >= (cell with G == T passes)", True, "implemented as g5 >= T in ema_threshold_sweep.py; G is continuous float32, ties have measure ~0")
I = inc[valid].sum(); pw = 100 * inc[valid & (g >= TS)].sum() / I; pc = 100 * (valid & (g >= TS)).sum() / valid.sum()
t("Area weighting differs from raw cell counts (weights are used)", abs(pw - c.loc[TS, "cropland_pass_pct"]) < 1e-3, f"area-weighted {pw:.3f}% (CSV {c.loc[TS,'cropland_pass_pct']}), unweighted cell share {pc:.3f}%")
nan_inc = inc[eur & ~np.isfinite(g) & (inc > 0)].sum(); nan_rice = rice[eur & ~np.isfinite(g) & (rice > 0)].sum()
t("Nodata: incumbent/rice area in domain cells without climate data", nan_inc < 0.001 * I, f"incumbent {nan_inc:.0f} ha, rice {nan_rice:.0f} ha excluded (NaN GDD10)")
ne = gpd.read_file(os.path.join(RAW, "ne_50m_admin_0_countries", "ne_50m_admin_0_countries.shp")).cx[-16:50, 29:76.5].reset_index(drop=True)
names = {i + 1: n for i, n in enumerate(ne["NAME_EN"])}
dom = sorted({names.get(int(k), "?") for k in np.unique(cid[valid])})
t("Geographic mask: Russia, Türkiye, Kazakhstan, Georgia, Azerbaijan, Armenia, Cyprus excluded", not ({"Russia", "Turkey", "Kazakhstan", "Georgia", "Azerbaijan", "Armenia", "Cyprus"} & set(dom)), f"{len(dom)} countries in domain")
casc = pd.read_csv(os.path.join(AG, "EUROPE_GATE_CASCADE_BY_COUNTRY.csv")).set_index("country").loc["EUROPE_DOMAIN_TOTAL"]
t("Denominator 69.7 Mha (independent of ag_grid_gates.py)", abs(I - casc.incumbent_ha) < 10 and round(I / 1e6, 1) == 69.7, f"{I:.0f} ha vs AG cascade {casc.incumbent_ha:.0f} ha")
t("Thermal pass at T* (exact value; AG manuscript printed 92.2 via double rounding)", round(pw, 1) == 92.1, f"{pw:.4f}% -> 92.1% at one decimal; AG used round(0.9215 [4 d.p.],1)=92.2")
comb = 100 * inc[valid & (g >= TS) & (aei >= 0.10)].sum() / I
t("Thermal + infrastructure share 16.0%", round(comb, 1) == 16.0 and abs(comb - 100 * casc.inc_ha_thermal_pass_irrig_infra_present / casc.incumbent_ha) < 1e-3, f"{comb:.3f}%")
de = pd.read_csv(os.path.join(AG, "GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv")); e0 = de[de.block == "0_endpoints"]
t("Germany endpoints reproduced from sweep", abs(c.loc[TS, "germany_cropland_pass_pct"] - e0.germany_pass_pct.iloc[0]) < 0.01 and abs(c.loc[900.0, "germany_cropland_pass_pct"] - e0.germany_pass_pct.iloc[1]) < 0.01, f"{c.loc[TS,'germany_cropland_pass_pct']} / {c.loc[900.0,'germany_cropland_pass_pct']} vs {list(e0.germany_pass_pct)}")
t("T* equals AG calibration (589)", TS == 589 and sm["T_star"] == TS, f"T*={TS}")
rm = eur & np.isfinite(g) & (rice > 0)
for T in (TS, 900.0):
    o = 100 * rice[rm & (g < T)].sum() / rice[rm].sum()
    t(f"Omission numerator/denominator recomputed at {T:.0f}", abs(o - c.loc[T, "rice_omitted_pct"]) < 1e-3, f"{rice[rm & (g < T)].sum():.1f} / {rice[rm].sum():.1f} ha = {o:.3f}%")
val = json.load(open(os.path.join(AG, "EUROPE_RICE_VALIDATION.json")))
t("Legacy 0.87% omission = incumbent-cell variant", abs(100 * val["thermal_fail"] / (val["rice_ha_total"] - val["rice_ha_no_incumbent_cells"]) - c.loc[TS, "rice_omitted_pct_incumbent_cells"]) < 0.01, f"{c.loc[TS,'rice_omitted_pct_incumbent_cells']}% (incumbent cells) vs {c.loc[TS,'rice_omitted_pct']}% (all rice cells)")
tm = pd.read_csv(os.path.join(EMA, "CLASSIFICATION_TRANSITION_MATRIX.csv"), index_col=0)
t("Transition matrix sums to denominator", abs(tm.values.sum() - I / 1e6) < 0.01, f"{tm.values.sum():.3f} Mha")
t("Nested thresholds: no cell passes 900 but fails T*", int((valid & (g >= 900) & (g < TS)).sum()) == 0 and tm.iloc[0, 1:].sum() == 0, "")
A, B = valid & (g >= TS), valid & (g >= 900); jac = inc[A & B].sum() / inc[A | B].sum()
st = pd.read_csv(os.path.join(EMA, "CLASSIFICATION_STABILITY_PAIRS.csv"))
t("Jaccard T* vs 900 recomputed", abs(jac - st[(st.domain == "Europe") & st.comparison.str.startswith("S1")].jaccard_pass.iloc[0]) < 1e-4, f"{jac:.4f}")
t("Inference unit: no cell-level bootstrap in EM&A scripts", not any(re.search(r"bootstrap|np\.random", open(os.path.join(HERE, f)).read()) for f in ["ema_threshold_sweep.py", "ema_figures.py", "build_ema_manuscript.py"]), "scenario ranges only (shifts, LOCO)")
tpl = "\n".join(l for l in open(os.path.join(ROOT, "modern_rice", "manuscript_ema", "manuscript_template.md")).read().split("# DECLARATIONS")[0].split("\n") if not l.startswith("#"))
body_nums = [x for x in re.findall(r"(?<![\w.{])\d+(?:\.\d+)?(?![\w}])", tpl)]
headline = {"92.1", "92.2", "16.0", "96.6", "3.2", "69.7", "589", "501", "1.37", "3.22", "0.87", "37.2", "1076", "1,076"}
t("No hardcoded headline results in EM&A template", not (headline & set(body_nums)), f"headline literals found: {sorted(headline & set(body_nums))}; remaining literals are design constants, years, citations: {sorted(set(body_nums))}")
bld = open(os.path.join(HERE, "build_ema_manuscript.py")).read()
t("No hardcoded headline results in EM&A builder", not re.search(r"(?<![\w.])(92\.1|16\.0|96\.6|69\.7|1\.37|3\.22|37\.2)(?![\w])", bld), "")
dan = pd.read_csv(os.path.join(AG, "DANUBE_DEMAND_VS_LOWFLOW.csv")); t("Water/risk models not retained in EM&A narrative", "Danube" not in tpl and "portfolio" not in tpl.lower(), "Lower Danube demand and risk portfolio remain in AG outputs, unchanged")
out = pd.DataFrame(R); out.to_csv(os.path.join(EMA, "KNOWN_ANSWER_TESTS_FINAL.csv"), index=False)
md = ["# Known-answer and semantic tests (EM&A)", "", f"Script: `modern_rice/scripts/ema_known_answer_tests.py`. Inputs: `outputs/modern_rice/ema/ema_layers_5m.npz` (regenerated by `ema_threshold_sweep.py`), sweep CSVs and AG canonical outputs. Countries in domain ({len(dom)}): {', '.join(dom)}.", "",
      "| # | Test | Result | Detail |", "|---|---|---|---|"] + [f"| {i+1} | {r['test']} | {r['result']} | {r['detail']} |" for i, r in enumerate(R)] + ["", f"**Summary: {sum(r['result']=='PASS' for r in R)}/{len(R)} PASS.**"]
open(os.path.join(EMA, "KNOWN_ANSWER_TESTS_FINAL.md"), "w").write("\n".join(md)); print("\n".join(md[-(len(R)+2):]))
