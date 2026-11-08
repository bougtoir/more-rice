#!/usr/bin/env python3
"""Build the Applied Geography submission files from canonical outputs.

Every number in the text is filled from outputs/modern_rice/applied_geography
(or the registry CSVs) via placeholders in modern_rice/manuscript_ag/manuscript_template.md.
Outputs go to outputs/modern_rice/applied_geography/submission/.
"""
from docx.oxml import parse_xml
from docx.oxml.ns import qn
from docx.shared import RGBColor
import os, re, json, shutil, subprocess, zipfile, numpy as np, pandas as pd
from docx import Document
from docx.shared import Pt, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pptx import Presentation
from pptx.util import Inches as PI, Pt as PP
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MR = os.path.join(ROOT, "outputs", "modern_rice"); AG = os.path.join(MR, "applied_geography"); FIG = os.path.join(AG, "figures")
SUB = os.path.join(AG, "submission"); os.makedirs(SUB, exist_ok=True)
TPL = os.path.join(ROOT, "modern_rice", "manuscript_ag", "manuscript_template.md")
REPO_URL = "https://github.com/bougtoir/more-rice"
AUTHOR, AFFIL, EMAIL = "Onishi Tatsuki", "Data Science and AI Innovation Research Promotion Center, Shiga University, Japan", "[corresponding e-mail to be entered by the author]"

# ---------------- numbers ----------------
cal = json.load(open(os.path.join(AG, "GRID_THERMAL_CALIBRATION.json")))
win = json.load(open(os.path.join(AG, "EUROPE_WINDOW_SENSITIVITY.json")))
val = json.load(open(os.path.join(AG, "EUROPE_RICE_VALIDATION.json")))
cas = pd.read_csv(os.path.join(AG, "EUROPE_GATE_CASCADE_BY_COUNTRY.csv")).set_index("country")
tot = cas.loc["EUROPE_DOMAIN_TOTAL"]
sen = pd.read_csv(os.path.join(AG, "EUROPE_SCALE_THRESHOLD_SENSITIVITY.csv"))
pw = pd.read_csv(os.path.join(AG, "POINT_GDD_WINDOW_SENSITIVITY.csv")).set_index("point")
cw = pd.read_csv(os.path.join(AG, "POINT_GRID_CROSSWALK.csv")).set_index("point")
dd = pd.read_csv(os.path.join(AG, "DANUBE_DEMAND_VS_LOWFLOW.csv"))
reg = pd.read_csv(os.path.join(MR, "LOWER_DANUBE_HYDROLOGY_SOURCE_REGISTRY.csv"))
rb = pd.read_csv(os.path.join(AG, "RISK_PORTFOLIO_BASELINE_CORRECTED.csv")).set_index("country")
rr = pd.read_csv(os.path.join(AG, "RISK_PORTFOLIO_ROBUSTNESS.csv")).set_index("country")
sb = pd.read_csv(os.path.join(MR, "DAILY_SOIL_WATER_BALANCE.csv")).set_index("point")
cost = pd.read_csv(os.path.join(MR, "AGRICULTURAL_COST_REGISTRY.csv"))
aei = pd.read_csv(os.path.join(AG, "EUROPE_AEI_THRESHOLD_SENSITIVITY.csv")).set_index("aei_min")
gdm = pd.read_csv(os.path.join(AG, "GDD_DAILY_VS_MONTHLY.csv"))
gdp = gdm[gdm.window == "pipeline_29Apr_11Sep"].set_index("point").bias_monthly_minus_daily
dom = pd.read_csv(os.path.join(AG, "EUROPE_DOMAIN_SENSITIVITY.csv")).set_index("domain")
f0 = lambda x: f"{x:,.0f}"; f1 = lambda x: f"{x:,.1f}"; f2 = lambda x: f"{x:.2f}"; f3 = lambda x: f"{x:.3f}"
inc = tot.incumbent_ha
def sh(T, scale, col="europe_inc_share_pass"): return float(sen[(sen.threshold == T) & (sen.scale == scale)][col].iloc[0])
Ts = cal["T_star_pipeline"]
m = cw.bucket_P_flower_deficit_pct.notna(); rho, rp = spearmanr(cw.grid_D_mm[m], cw.bucket_P_flower_deficit_pct[m])
pg = cw.power_gdd_pipeline - cw.grid_gdd_pipeline
d120 = dd[(dd.seasonal_depth_mm == 1000) & (dd.season_days == 120)].set_index("area_ha")
mq = reg.loc[reg.datum.str.startswith("min flow"), "value"].iloc[0].split()[0].split("/")
ci = lambda c, k: f3(rb.loc[c, k])
lfall = pd.read_csv(os.path.join(AG, "HYDROLOGICAL_LOW_FLOW_RESULTS.csv"))
gdc = pd.read_csv(os.path.join(AG, "GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv")); gmeta = json.load(open(os.path.join(AG, "GERMANY_THERMAL_CONTRAST_META.json")))
gp1 = gdc[gdc.block == "1_threshold_path_pipeline_5m"].reset_index(drop=True); gp2 = gdc[gdc.block == "2_threshold_path_JunSep_5m"].reset_index(drop=True)
gpt = gdc[gdc.block == "3_point_location_pipeline_5m"].germany_pass_pct
grc = gdc[gdc.block == "4_resolution_recalibrated"]; grp = grc[grc.surface_window.str.startswith("pipeline")].germany_pass_pct; grj = grc[grc.surface_window.str.startswith("calendar")].germany_pass_pct
g9 = gdc[(gdc.block == "4_resolution_fixed_900") & gdc.surface_window.str.startswith("pipeline")].germany_pass_pct
g5 = float(grc[(grc.surface_resolution == "5m") & grc.surface_window.str.startswith("pipeline")].germany_pass_pct.iloc[0])
GDE = {f"dp_{k}_T": f"{gp1.threshold_gdd10[i]:,.0f}" for i, k in enumerate("abcdef")} | {f"dp_{k}_pct": f"{gp1.germany_pass_pct[i]:.1f}" for i, k in enumerate("abcdef")}
GDE |= dict(dp_q_pp=f"{gp1.germany_pass_pct[5] - gp1.germany_pass_pct[4]:.0f}", pt_lo=f"{gpt.min():.1f}", pt_hi=f"{gpt.max():.1f}", de_res_lo=f"{grp.min():.1f}", de_res_hi=f"{grp.max():.1f}",
            de_resc_lo=f"{grj.min():.1f}", de_resc_hi=f"{grj.max():.1f}", de9_lo=f"{g9.min():.1f}", de9_hi=f"{g9.max():.1f}", de_cal=f"{gp2.germany_pass_pct[5]:.1f}",
            de_res_pp=f"{(grp - g5).abs().max():.1f}", de_inc_Mha=f"{gdc.germany_incumbent_Mha.iloc[0]:.2f}",
            rice_pt_kha=f"{gmeta['spam_rice_ha_within_0.5deg_of_POWER_Hokkaido_point'] / 1e3:.1f}")
lfc = lfall[lfall.station.str.startswith("Orsova") & (lfall.period == "all")].set_index("statistic")
lfr = lfall[lfall.station.str.startswith("Orsova") & lfall.period.str.startswith("1972")].set_index("statistic")
lfo = lfc.value_m3s.dropna().astype(float)
N = dict(
    inc_Mha=f1(inc / 1e6), T_star=f0(Ts), T_star_cal=f0(cal["T_star_calJunSep"]),
    pct_thermal_pass=f1(100 * sh(Ts, "5m_native")), pct_pass_900=f1(100 * sh(900, "5m_native")), pct_pass_1000=f1(100 * sh(1000, "5m_native")),
    **GDE, de_T=f1(100 * sh(Ts, "5m_native", "share_Germany")), de_900=f1(100 * sh(900, "5m_native", "share_Germany")),
    ro_900_25=f1(100 * sh(900, "2.5m_native", "share_Romania")), ro_900_60=f1(100 * sh(900, "60m_aggregated", "share_Romania")),
    pct_aei=f1(100 * tot.inc_ha_thermal_pass_irrig_infra_present / inc), aei_Mha=f1(tot.inc_ha_thermal_pass_irrig_infra_present / 1e6),
    pct_deficit=f1(100 * tot.inc_ha_thermal_pass_no_irrig_infra_rainfed_deficit / inc), deficit_Mha=f1(tot.inc_ha_thermal_pass_no_irrig_infra_rainfed_deficit / 1e6),
    bal_kha=f0(tot.inc_ha_thermal_pass_no_irrig_infra_rainfed_balance_nonneg / 1e3),
    thermal_pass_Mha=f1((inc - tot.inc_ha_thermal_fail) / 1e6),
    pct_thermal_cal=f1(100 * win["inc_share_thermal_pass_calJunSep"]), pct_agree=f1(100 * win["inc_share_agree"]),
    max_scale_pts=f0(100 * max(sen.groupby("threshold").europe_inc_share_pass.agg(lambda s: s.max() - s.min()))),
    dis_900_60=f1(float(sen[(sen.threshold == 900) & (sen.scale == "60m_aggregated")].abs_disagreement_vs_2p5m_ha.iloc[0]) / 1e6),
    hok_rice_kha=f0(cal["hokkaido_rice_ha"] / 1e3), hok_p01=f0(cal["hokkaido_P01_pipeline"]), hok_p10=f0(cal["hokkaido_P10_pipeline"]), hok_p50=f0(cal["hokkaido_P50_pipeline"]),
    bound_shift=f0(round((900 - Ts) / 50) * 50),
    hok_pipe=f0(pw.loc["Hokkaido_JP", "pipeline_29Apr_11Sep"]), hok_cal=f0(pw.loc["Hokkaido_JP", "calendar_Jun_Sep"]), hok_may=f0(pw.loc["Hokkaido_JP", "calendar_May_Sep"]),
    rh_pipe=f0(pw.loc["Rhine_DE", "pipeline_29Apr_11Sep"]), rh_cal=f0(pw.loc["Rhine_DE", "calendar_Jun_Sep"]),
    sx_pipe=f0(pw.loc["Saxony_DE", "pipeline_29Apr_11Sep"]), sx_cal=f0(pw.loc["Saxony_DE", "calendar_Jun_Sep"]),
    pg_median=f0(pg.median()), pg_min=f0(pg.min()), pg_max=f0(pg.max()),
    als_grid=f0(cw.loc["Alsace_FR", "grid_gdd_pipeline"]), als_power=f0(cw.loc["Alsace_FR", "power_gdd_pipeline"]),
    eu_rice_kha=f0(val["rice_ha_total"] / 1e3), val_thermal=f1(100 * (1 - val["thermal_fail"] / (val["rice_ha_total"] - val["rice_ha_no_incumbent_cells"]))),
    val_aei=f1(100 * val["thermal_pass_irrig_infra_present"] / (val["rice_ha_total"] - val["rice_ha_no_incumbent_cells"])),
    rho=f2(rho), rho_p=f"{rp:.4f}", rho_n=str(int(m.sum())), hok_flower=f0(sb.loc["Hokkaido_JP", "P_flower_deficit_10d_pct"]),
    dan_mean=f0(lfo["JunSep_mean_median"]), dan_lf_med=f0(lfo["JunSep_min_daily_median"]), dan_lf_p10=f0(lfo["JunSep_min_daily_P10"]), dan_lf_low=f0(lfo["JunSep_min_daily_lowest"]),
    dan_lf_lo=f0(lfc.loc["JunSep_min_daily_median", "ci95_lo"]), dan_lf_hi=f0(lfc.loc["JunSep_min_daily_median", "ci95_hi"]), dan_lf_n=str(int(lfc.loc["JunSep_min_daily_median", "n_years"])),
    dan_lf_reg_p10=f0(lfr.loc["JunSep_min_daily_P10", "value_m3s"]),
    dan_q=f0(d120.loc[250000, "demand_m3s"]), dan_pct=f1(d120.loc[250000, "pct_of_lowflow_median"]), dan_pct_p10=f1(d120.loc[250000, "pct_of_lowflow_P10"]), dan_pct_mean=f1(d120.loc[250000, "pct_of_mean"]),
    dan_pct_gross=f1(lfc.loc["JunSep_min_daily_median", "gross_pct"]), dan_pct_gross_low=f1(lfc.loc["JunSep_min_daily_lowest", "gross_pct"]),
    dan_yrs10=f0(float(lfc.loc["share_years_gross_over_JunSep_min_gt_10pct", "gross_pct"])), dan_yrs20=f1(float(lfc.loc["share_years_gross_over_JunSep_min_gt_20pct", "gross_pct"])),
    dan_q_100=f0(d120.loc[100000, "demand_m3s"]), dan_pct_100=f1(d120.loc[100000, "pct_of_lowflow_median"]),
    ro_A=ci("Romania", "P_A"), ro_B=ci("Romania", "P_B_rice"), ro_D=ci("Romania", "P_D_potato"), ro_lo=ci("Romania", "diff_CI95_lo"), ro_hi=ci("Romania", "diff_CI95_hi"),
    kz_A=ci("Kazakhstan", "P_A"), kz_B=ci("Kazakhstan", "P_B_rice"), kz_lo=ci("Kazakhstan", "diff_CI95_lo"), kz_hi=ci("Kazakhstan", "diff_CI95_hi"),
    rs_B=ci("Serbia", "P_B_rice"), rs_D=ci("Serbia", "P_D_potato"),
    ro_rob=f0(100 * rr.loc["Romania", "share_B_lt_A"]), ro_excl=f0(100 * rr.loc["Romania", "share_CI_excl_0"]), kz_excl=f0(100 * rr.loc["Kazakhstan", "share_CI_excl_0"]),
    bg_rob=f0(100 * rr.loc["Bulgaria", "share_B_lt_A"]), hu_rob=f0(100 * rr.loc["Hungary", "share_B_lt_A"]), fr_rob=f0(100 * rr.loc["France", "share_B_lt_A"]),
    pct_aei5=f1(100 * aei.loc[0.05, "inc_share_thermal_pass_aei"]), pct_aei20=f1(100 * aei.loc[0.20, "inc_share_thermal_pass_aei"]),
    rice_aei5=f1(100 * aei.loc[0.05, "existing_rice_share_aei"]), rice_aei20=f1(100 * aei.loc[0.20, "existing_rice_share_aei"]),
    hok_mbias=f0(-gdp["Hokkaido_JP"]), eu_mbias_min=f0(-gdp.drop("Hokkaido_JP").max()), eu_mbias_max=f0(-gdp.drop("Hokkaido_JP").min()),
    rect_Mha=f1(dom.iloc[0].incumbent_Mha), rect_pass=f1(100 * dom.iloc[0].thermal_pass_share), rect_aei=f1(100 * dom.iloc[0].thermal_aei_share),
    eu27_pass=f1(100 * dom.loc["EU27"].thermal_pass_share), eu27_aei=f1(100 * dom.loc["EU27"].thermal_aei_share),
    aei_cond=f1(100 * tot.inc_ha_thermal_pass_irrig_infra_present / (inc - tot.inc_ha_thermal_fail)),
    dan_q_gross=f0(d120.loc[250000, "demand_m3s"] / 0.75),
    it_cost=cost.loc[cost.item == "total production cost flooded", "value"].iloc[0].replace("-", "–"),
    it_gm=cost.loc[cost.item == "gross margin conventional", "value"].iloc[0].replace("-", "–"))
for k in ["ro_lo", "ro_hi", "kz_lo", "kz_hi"]: N[k] = N[k].replace("-", "−")
json.dump(N, open(os.path.join(SUB, "MANUSCRIPT_NUMBERS.json"), "w"), indent=1, ensure_ascii=False)

# ---------------- parse template ----------------
raw = open(TPL, encoding="utf-8").read()
miss = sorted(set(re.findall(r"\{([A-Za-z0-9_]+)\}", raw)) - set(N))
assert not miss, f"unfilled placeholders: {miss}"
txt = re.sub(r"\{([A-Za-z0-9_]+)\}", lambda mm: N[mm.group(1)], raw)
sec, cur = {}, None; body = []
for line in txt.split("\n"):
    if line.startswith("# ") and line[2:].isupper() and line[2:] in {"TITLE", "ABSTRACT", "KEYWORDS", "HIGHLIGHTS", "DECLARATIONS", "REFERENCES"}:
        cur = line[2:]; sec[cur] = []; continue
    if line.startswith("# ") or line.startswith("## "):
        if cur in (None, "TITLE", "ABSTRACT", "KEYWORDS", "HIGHLIGHTS") or (cur not in ("DECLARATIONS", "REFERENCES")): cur = "BODY"
    sec.setdefault(cur, []).append(line)
def paras(lines):
    out, buf = [], []
    for l in lines:
        s = l.strip()
        if not s or s.startswith("#") or s.startswith("[[") or s.startswith("- "):
            if buf: out.append(" ".join(buf)); buf = []
            if s: out.append(s)
        else: buf.append(s)
    if buf: out.append(" ".join(buf))
    return out
title = " ".join(paras(sec["TITLE"])); abstract = " ".join(paras(sec["ABSTRACT"])); keywords = " ".join(paras(sec["KEYWORDS"]))
highlights = [p[2:] for p in paras(sec["HIGHLIGHTS"])]
body_p, decl_p, refs = paras(sec["BODY"]), paras(sec["DECLARATIONS"]), [l.strip() for l in sec["REFERENCES"] if l.strip()]
assert len(abstract.split()) <= 250, len(abstract.split())
assert 3 <= len(highlights) <= 5 and all(len(h) <= 85 for h in highlights), [len(h) for h in highlights]
assert 1 <= len(keywords.split(";")) <= 7

# ---------------- figures and tables ----------------
FIGS = {"framework": ("Figure_framework", "Gate framework. Five sequential, non-compensatory gates evaluated for a transferable cold-region japonica rice system on incumbent arable land. Passing all gates identifies a candidate for next-stage feasibility assessment, not an allocation or converted area."),
        "map": ("Figure_map_gates", f"(a) GDD10 for 29 April–11 September from WorldClim 2.1 (5′, 1970–2000), with the grid-calibrated Hokkaido bound T* = {N['T_star']} (white) and the point-derived 900 GDD10 (red, dashed). (b) Gate class of 5′ cells with incumbent arable land ≥1% of cell area. AEI, area equipped for irrigation (GMIA v5). Circles mark NASA POWER point cells. ETRS89-LAEA projection. Cells outside the European domain (Natural Earth Europe excluding Russia) are not classified."),
        "scale": ("Figure_scale_sensitivity", "Sensitivity of the thermal gate. (a) Share of incumbent arable land passing as a function of the GDD10 threshold for two seasonal windows (vertical lines: T* and 900). (b) Share passing by native resolution (2.5′, 5′, 10′) and after aggregation of 5′ GDD10 to 30′ and 60′. (c) NASA POWER point-cell GDD10 (2000–2024) versus the containing WorldClim 5′ cell (1970–2000); dotted line 1:1. (d) Share of German incumbent arable land passing along a controlled reference-construction path from a single NASA POWER Hokkaido point to T*, for each window (bar labels: threshold, GDD10)."),
        "water": ("Figure_water", f"Water geography. (a) Grid Jun–Sep climatic deficit D (WorldClim 10′) versus the share of years with >10 flowering-stage deficit days from the daily bucket model at NASA POWER point cells (Spearman ρ = {N['rho']}, n = {N['rho_n']}); colour shows latitude. (b) Continuous-equivalent paddy water demand on the Lower Danube as a percentage of the median Jun–Sep minimum daily discharge observed at Orsova (GRDC 6742200, {N['dan_lf_n']} years 1920–1990; {N['dan_lf_med']} m³/s) for three seasonal depths over 120 days; mainstem comparison only, not allocable water."),
        "risk": ("Figure_risk", "Corrected food-supply portfolio scenarios. (a) Modeled probability that portfolio calories fall below 80% of their mean for the incumbent portfolio (A), 20% rice substitution (B) and 20% potato comparator (D). (b) Change B − A with 95% moving-block bootstrap intervals (3-year blocks, 2,000 resamples). * Rice shocks and yield level from an analog country.")}
fig_order = [k for p in body_p if p.startswith("[[FIGURE:") for k in [p[9:-2]]]
FIGNUM = {k: i + 1 for i, k in enumerate(fig_order)}
TABS = {}
TABS["data"] = ("Data sources and their role.", ["Dataset", "Version / period", "Resolution", "Role", "Licence"], [
    ["NASA POWER daily (T2M_MAX, T2M_MIN, PRECTOTCORR)", "v2, 2000–2024", "0.5° point cells (43)", "Point GDD10, daily bucket", "Public domain (NASA)"],
    ["WorldClim 2.1 tavg, tmin, tmax, prec", "1970–2000 monthly", "2.5′, 5′, 10′", "Grid GDD10, ET0, deficit D", "Free for research; redistribution restricted"],
    ["MapSPAM 2010 v2.0 harvested area (all technologies)", "circa 2010", "5′", "Incumbent arable denominator, rice validation, Hokkaido calibration", "CC BY 4.0"],
    ["FAO GMIA v5 area equipped for irrigation", "circa 2005–2008", "5′", "Irrigation-infrastructure gate", "CC BY-NC-SA 3.0 IGO"],
    ["FAOSTAT QCL yields", "1961–2024", "national", "Portfolio risk scenarios", "CC BY 4.0"],
    ["Natural Earth admin-0", "1:50m v5.1", "vector", "Country assignment", "Public domain"],
    ["GRDC daily discharge via EStreams v1.4 indices (Orsova, Bazias); WEAP allocation", "1920–1990 / 1991–2008", "station", "Lower Danube mainstem check", "CC BY-NC 4.0 (EStreams); GRDC terms"]])
sel = ["Spain", "Italy", "France", "Romania", "Bulgaria", "Hungary", "Ukraine", "Serbia", "Croatia", "Germany", "Poland", "United Kingdom"]
rows = []
for c in sel + ["EUROPE_DOMAIN_TOTAL"]:
    r = cas.loc[c]; i = r.incumbent_ha
    rows.append(["Europe domain total" if c == "EUROPE_DOMAIN_TOTAL" else c, f1(i / 1e6), f1(100 * r.inc_ha_thermal_fail / i), f1(100 * r.inc_ha_thermal_pass_no_irrig_infra_rainfed_deficit / i),
                 f1(100 * r.inc_ha_thermal_pass_irrig_infra_present / i), f0(r.rice_ha_SPAM2010 / 1e3)])
TABS["cascade"] = (f"Exposure of incumbent arable land to the gate cascade by country (T* = {N['T_star']} GDD10; AEI ≥10%). Percentages of incumbent arable area; the remainder (thermal gate met, no infrastructure, D ≤ 0) is <1% everywhere.",
                   ["Country", "Incumbent arable (Mha)", "Thermal not met (%)", "Thermal met, no AEI, D>0 (%)", "Thermal met, AEI ≥10% (%)", "Rice 2010 (kha)"], rows)
rsel = ["Romania", "Bulgaria", "Hungary", "Serbia", "Croatia", "France", "Kazakhstan"]
TABS["risk"] = ("Corrected portfolio scenarios and robustness over 24 configurations. P, modeled shortfall probability; CI, 95% moving-block bootstrap interval of B − A.",
                ["Country", "Rice evidence", "Years", "P(A)", "P(B) rice", "P(D) potato", "B − A (95% CI)", "B < A (% configs)", "CI excludes 0 (% configs)"],
                [[c, rb.loc[c, "rice_source"].replace("analog:", "analog: "), str(int(rb.loc[c, "n_years"])), f3(rb.loc[c, "P_A"]), f3(rb.loc[c, "P_B_rice"]), f3(rb.loc[c, "P_D_potato"]),
                  f"{rb.loc[c, 'P_B_rice'] - rb.loc[c, 'P_A']:.3f} ({rb.loc[c, 'diff_CI95_lo']:.3f}, {rb.loc[c, 'diff_CI95_hi']:.3f})".replace("-", "−"),
                  f0(100 * rr.loc[c, "share_B_lt_A"]), f0(100 * rr.loc[c, "share_CI_excl_0"])] for c in rsel])
tab_order = [p[8:-2] for p in body_p if p.startswith("[[TABLE:")]
TABNUM = {k: i + 1 for i, k in enumerate(tab_order)}
def resolve(p):
    for k, n in FIGNUM.items(): p = p.replace(f"Figure {{fig:{k}}}", f"Figure {n}")
    return p
fig_refs = {"framework": "Figure 1", "map": "Figure 2", "scale": "Figure 3", "water": "Figure 4", "risk": "Figure 5"}
assert all(fig_refs[k] == f"Figure {n}" for k, n in FIGNUM.items()), FIGNUM
assert TABNUM == {"data": 1, "cascade": 2, "risk": 3}, TABNUM

# ---------------- docx helpers ----------------
def base_doc():
    d = Document(); st = d.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12)
    st.paragraph_format.line_spacing = 2.0; st.paragraph_format.space_after = Pt(0)
    for hn in ["Heading 1", "Heading 2", "Heading 3", "Title"]:
        hs = d.styles[hn]; hs.font.name = "Times New Roman"; hs.font.color.rgb = RGBColor(0, 0, 0)
        rpr = hs.element.get_or_add_rPr(); rf = rpr.find(qn("w:rFonts"))
        if rf is not None:
            for a in ["w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"]: rf.attrib.pop(qn(a), None)
    for s in d.sections: s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Inches(1)
    return d
OMML_Q = ('<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>Q=</m:t></m:r>'
          '<m:f><m:num><m:r><m:t>A\u00b7D</m:t></m:r></m:num><m:den><m:r><m:t>T</m:t></m:r></m:den></m:f></m:oMath>')
def add_runs(par, text):
    text = re.sub(r"\bT\*(?=[\s,.;:)=}\]]|$)", "\x00", text)
    for seg in re.split(r"(Q = A·D/T)", text):
        if seg == "Q = A·D/T":
            par._p.append(parse_xml(OMML_Q)); continue
        for chunk in re.split(r"(\*[^*]+\*)", seg):
            if not chunk: continue
            ital = chunk.startswith("*") and chunk.endswith("*")
            for part in re.split(r"(³|\x00)", chunk[1:-1] if ital else chunk):
                if part in ("³", "\x00"):
                    if part == "\x00": r = par.add_run("T"); r.italic = True
                    sr = par.add_run("3" if part == "³" else "*"); sr.font.superscript = True; sr.italic = ital
                elif part:
                    r = par.add_run(part); r.italic = ital
def add_table(d, key):
    cap, hdr, rows = TABS[key]
    p = d.add_paragraph(); p.paragraph_format.space_before = Pt(18); p.paragraph_format.keep_with_next = True
    r = p.add_run(f"Table {TABNUM[key]}. "); r.bold = True; add_runs(p, cap)
    t = d.add_table(rows=1 + len(rows), cols=len(hdr)); t.style = "Table Grid"
    for j, h in enumerate(hdr):
        c = t.cell(0, j); c.text = h; c.paragraphs[0].runs[0].bold = True
    for i, row in enumerate(rows):
        for j, v in enumerate(row): t.cell(i + 1, j).text = v
    for row in t.rows:
        for c in row.cells:
            for pp in c.paragraphs:
                pp.paragraph_format.line_spacing = 1.0
                for rr_ in pp.runs: rr_.font.size = Pt(10)
    d.add_paragraph()
def add_figure(d, key, embed=True):
    fn, cap = FIGS[key]
    if embed:
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.line_spacing = 1.0
        p.add_run().add_picture(os.path.join(FIG, fn + ".png"), width=Inches(6.3))
    p = d.add_paragraph(); p.paragraph_format.space_before = Pt(18)
    r = p.add_run(f"Figure {FIGNUM[key]}. "); r.bold = True; add_runs(p, cap)

# ---------------- anonymized manuscript ----------------
def build_ms(embed, path):
  d = base_doc()
  p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; r = p.add_run(title); r.bold = True; r.font.size = Pt(14)
  d.add_heading("Abstract", level=1); add_runs(d.add_paragraph(), abstract)
  p = d.add_paragraph(); r = p.add_run("Keywords: "); r.bold = True; p.add_run(keywords)
  for bp in body_p:
      if bp.startswith("## "): d.add_heading(bp[3:], level=2)
      elif bp.startswith("# "): d.add_heading(bp[2:], level=1)
      elif bp.startswith("[[FIGURE:"): add_figure(d, bp[9:-2], embed)
      elif bp.startswith("[[TABLE:"): add_table(d, bp[8:-2])
      else: add_runs(d.add_paragraph(), resolve(bp))
  for dp in decl_p:
      if dp.startswith("## "): d.add_heading(dp[3:], level=2)
      else: d.add_paragraph(dp)
  d.add_heading("References", level=1)
  for ref in refs:
      p = d.add_paragraph(); p.paragraph_format.left_indent = Cm(1.27); p.paragraph_format.first_line_indent = Cm(-1.27); add_runs(p, ref)
  for cp in d.paragraphs:
      if re.match(r"(Figure|Table) \d+\. ", cp.text):
          for cr in cp.runs: cr.font.size = Pt(10)
  d.save(path)
MS = os.path.join(SUB, "APPLIED_GEOGRAPHY_MANUSCRIPT_FINAL.docx"); build_ms(False, MS)
MSI = os.path.join(SUB, "APPLIED_GEOGRAPHY_MANUSCRIPT_INLINE_REVIEW_COPY.docx"); build_ms(True, MSI)

# ---------------- title page ----------------
t = base_doc()
p = t.add_paragraph(); r = p.add_run(title); r.bold = True; r.font.size = Pt(14)
for line in [f"Author: {AUTHOR}", f"Affiliation: {AFFIL}", f"Corresponding author: {AUTHOR}, {AFFIL}. E-mail: {EMAIL}",
             f"Code and data repository: {REPO_URL}",
             "ORCID: 0000-0001-7261-9062", "CRediT author contribution statement: Onishi Tatsuki: Conceptualization, Methodology, Software, Formal analysis, Data curation, Visualization, Writing – original draft, Writing – review & editing.",
             "Declaration of competing interest: The author declares no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.",
             "Acknowledgments: None.", "Funding: This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors."]:
    t.add_paragraph(line)
t.save(os.path.join(SUB, "APPLIED_GEOGRAPHY_TITLE_PAGE.docx"))
h = base_doc(); h.add_heading("Highlights", level=1)
for x in highlights: h.add_paragraph(x, style="List Bullet")
h.save(os.path.join(SUB, "APPLIED_GEOGRAPHY_highlights.docx"))
tb = base_doc()
for k in tab_order: add_table(tb, k)
tb.save(os.path.join(SUB, "APPLIED_GEOGRAPHY_TABLES_EDITABLE.docx"))
prs = Presentation(); prs.slide_width, prs.slide_height = PI(13.333), PI(7.5)
from PIL import Image
for k in fig_order:
    fn, cap = FIGS[k]; s = prs.slides.add_slide(prs.slide_layouts[6])
    tbx = s.shapes.add_textbox(PI(0.4), PI(0.15), PI(12.5), PI(0.5)); tbx.text_frame.text = f"Figure {FIGNUM[k]}"; tbx.text_frame.paragraphs[0].runs[0].font.size = PP(20)
    w, hh = Image.open(os.path.join(FIG, fn + ".png")).size; sc = min(12.5 / w, 5.4 / hh)
    s.shapes.add_picture(os.path.join(FIG, fn + ".png"), PI((13.333 - w * sc) / 2), PI(0.75), PI(w * sc), PI(hh * sc))
    cb = s.shapes.add_textbox(PI(0.4), PI(6.3), PI(12.5), PI(1.1)); cb.text_frame.word_wrap = True; cb.text_frame.text = cap
    cb.text_frame.paragraphs[0].runs[0].font.size = PP(10)
prs.save(os.path.join(SUB, "APPLIED_GEOGRAPHY_FIGURES_EDITABLE.pptx"))
ART = os.path.join(SUB, "figures"); os.makedirs(ART, exist_ok=True)
for k in fig_order:
    for e in ["png", "pdf"]: shutil.copy(os.path.join(FIG, f"{FIGS[k][0]}.{e}"), os.path.join(ART, f"Figure_{FIGNUM[k]}.{e}"))


# ---------------- cover letter ----------------
c = base_doc(); c.styles["Normal"].paragraph_format.line_spacing = 1.15; c.styles["Normal"].paragraph_format.space_after = Pt(8)
for x in ["[Date]", "The Editors, Applied Geography", f"Re: Submission of a research article, \u201c{title}\u201d",
          "Dear Editors,",
          f"I am submitting a research article that asks a geographic question: on which existing arable land in Europe could a cold-region rice cultivation system be transferred beyond traditional growing regions, and how far does the answer depend on how the climatic reference is constructed and on the spatial support at which it is applied? Proposals for rice outside its traditional regions usually rest on a single climatic threshold. My analysis shows that such a threshold is as much a property of its construction and data support as of the crop.",
          f"Calibrating the Hokkaido cold bound on the WorldClim grid gives {N['T_star']} GDD10 (the 5th percentile of Hokkaido rice area). On an explicit denominator of {N['inc_Mha']} Mha of incumbent arable land in Europe (Russia excluded; domain and EU27 sensitivities reported), {N['pct_thermal_pass']}% meets this thermal gate, but only {N['pct_aei']}% also has mapped irrigation infrastructure. Because the gates are non-compensatory, thermal suitability cannot offset missing infrastructure. A controlled decomposition for Germany, where the pass share is {N['de_T']}% at T* but {N['de_900']}% at a point-derived ~900 GDD10, shows that the contrast arises mainly from reference construction (the quantile, location, period and temporal aggregation of the reference) and only marginally from grid resolution (at most {N['de_res_pp']} percentage points in the primary window). I treat {N['T_star']} GDD10 as an empirical, system-specific reference rather than a physiological constant.",
          "The manuscript speaks to the journal's interest in spatially explicit resource assessment and land-use decision problems. It builds on land-suitability, cold-margin rice and irrigation studies published in Applied Geography and adds an explicit land denominator, non-compensatory gates and an analysis of the modifiable areal unit problem. I state plainly that climate suitability and mapped infrastructure are not operational feasibility: the gates identify candidates for next-stage assessment, not converted area, water allocations or policy effects, and no field validation is claimed.",
          f"In preparing this version I re-analysed the work and corrected several errors in an earlier draft. The Lower Danube demand of a 250,000 ha paddy scenario is ~{N['dan_q']} m³/s net, not ~24 m³/s, and it is now compared with observed June–September minimum daily discharge at Orsova (GRDC data, 1920–1990; median {N['dan_lf_med']} m³/s), about {N['dan_pct']}%, replacing an unverified low-flow value. The European shares are computed for Europe only, rice yields are converted from paddy to milled equivalent, an analog-country error in the risk model is fixed, and the modeled supply-risk results are not robust in most countries.",
          "The work is original, is not under consideration elsewhere, and I am its sole author. All code and derived outputs are openly available; the repository link is on the title page. I declare no competing interests. My use of AI-assisted tools is declared in the manuscript. I intend to publish under the subscription model.",
          "Suggested reviewers: [to be supplied by the author].", "Sincerely,", f"{AUTHOR}", AFFIL]:
    add_runs(c.add_paragraph(), x)
CL = os.path.join(SUB, "APPLIED_GEOGRAPHY_COVER_LETTER.docx"); c.save(CL)

# ---------------- metadata + checks ----------------
def wc(s): return len(re.findall(r"\S+", s))
words = wc(abstract) + wc(keywords) + sum(wc(re.sub(r"^#+ ", "", p)) for p in body_p if not p.startswith("[[")) + sum(wc(FIGS[k][1]) for k in FIGS) \
        + sum(wc(TABS[k][0]) + sum(wc(" ".join(r)) for r in [TABS[k][1]] + TABS[k][2]) for k in TABS) + sum(wc(r) for r in refs) + sum(wc(p) for p in decl_p) + wc(title)
assert 4500 <= words <= 8000, words
cited = set(re.findall(r"([A-Z][A-Za-zü\-]+(?: (?:&|et al\.)(?: [A-Z][A-Za-zü\-]+)?)?),? \(?(\d{4})", " ".join(body_p)))
dx = Document(MS); nl = sum(("\n" in r.text or "\r" in r.text) for pp in dx.paragraphs for r in pp.runs)
assert nl == 0, nl
assert not any("³" in r.text for pp in dx.paragraphs for r in pp.runs), "unicode superscript in docx"
assert REPO_URL not in " ".join(pp.text for pp in dx.paragraphs) and "Onishi" not in " ".join(pp.text for pp in dx.paragraphs)
with open(os.path.join(SUB, "APPLIED_GEOGRAPHY_ABSTRACT_AND_METADATA.txt"), "w") as f:
    f.write(f"Title: {title}\n\nArticle type: Research article\n\nAbstract ({wc(abstract)} words):\n{abstract}\n\nKeywords ({len(keywords.split(';'))}): {keywords}\n\nHighlights:\n")
    for x in highlights: f.write(f"- {x} ({len(x)} chars)\n")
    f.write(f"\nTotal word count (title, abstract, keywords, text, captions, tables, declarations, references): {words}\nFigures: {len(fig_order)}; Tables: {len(tab_order)}; References: {len(refs)}\n")
    f.write("Publishing route intended: Subscription (no open access fee). No option selected in any system.\n")
for pth in [MS, MSI, CL]: subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", SUB, pth], check=True, capture_output=True)
print(json.dumps({"words": words, "abstract_words": wc(abstract), "highlights_len": [len(x) for x in highlights], "figs": FIGNUM, "tabs": TABNUM, "refs": len(refs), "newlines_in_runs": nl}, indent=0))
