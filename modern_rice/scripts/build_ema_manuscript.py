#!/usr/bin/env python3
"""Build the EM&A manuscript, review copy and cover letter from canonical outputs only."""
import os, re, json, subprocess, numpy as np, pandas as pd
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import qn
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MR = os.path.join(ROOT, "outputs", "modern_rice"); AG = os.path.join(MR, "applied_geography"); EMA = os.path.join(MR, "ema"); FIG = os.path.join(EMA, "figures")
SUB = os.path.join(EMA, "submission"); os.makedirs(SUB, exist_ok=True)
TPL = os.path.join(ROOT, "modern_rice", "manuscript_ema", "manuscript_template.md")
REPO_URL = "https://github.com/bougtoir/more-rice"
AUTHOR, AFFIL, ORCID = "Tatsuki Onishi", "Data Science and AI Innovation Research Promotion Center, Shiga University, Japan", "0000-0001-7261-9062"
EMAIL = "[corresponding e-mail to be entered by the author]"

cal = json.load(open(os.path.join(AG, "GRID_THERMAL_CALIBRATION.json"))); sm = json.load(open(os.path.join(EMA, "EMA_THRESHOLD_SUMMARY.json")))
cur = pd.read_csv(os.path.join(EMA, "THRESHOLD_OMISSION_CURVE.csv")).set_index("threshold_gdd10")
al = pd.read_csv(os.path.join(EMA, "OMISSION_ALIGNMENT_SENSITIVITY.csv")); st = pd.read_csv(os.path.join(EMA, "CLASSIFICATION_STABILITY_PAIRS.csv"))
geo = pd.read_csv(os.path.join(EMA, "RICE_OMISSION_BY_COUNTRY.csv")).set_index("country"); tm = pd.read_csv(os.path.join(EMA, "CLASSIFICATION_TRANSITION_MATRIX.csv"), index_col=0)
gde = pd.read_csv(os.path.join(AG, "GERMANY_THERMAL_CONTRAST_DECOMPOSITION.csv")); casc = pd.read_csv(os.path.join(AG, "EUROPE_GATE_CASCADE_BY_COUNTRY.csv")).set_index("country")
f0 = lambda x: f"{x:,.0f}"; f1 = lambda x: f"{x:.1f}"; f2 = lambda x: f"{x:.2f}"
TS = sm["T_star"]; c = lambda T, k: float(cur.loc[float(T), k])
tot = casc.loc["EUROPE_DOMAIN_TOTAL"]; inc = float(tot.incumbent_ha)
assert abs(inc / 1e6 - sm["incumbent_Mha"]) < 0.01
p1 = gde[gde.block == "1_threshold_path_pipeline_5m"].reset_index(drop=True)
rs = gde[(gde.block == "4_resolution_recalibrated") & gde.surface_window.str.startswith("pipeline")]
g5de = float(rs[rs.surface_resolution == "5m"].germany_pass_pct.iloc[0])
def jac(dom, pre): return float(st[(st.domain == dom) & st.comparison.str.startswith(pre)].jaccard_pass.iloc[0])
a = lambda T, test: float(al[(al.threshold_gdd10 == float(T)) & (al.test == test)].rice_omitted_pct.iloc[0])
shifts = al[(al.threshold_gdd10 == TS) & al.test.str.startswith("rice grid shifted")].rice_omitted_pct
lo = {int(d["threshold_gdd10"]): d for d in sm["loco"]}; cl = sm["clusters"][str(int(TS))]
s1 = st[(st.domain == "Europe") & st.comparison.str.startswith("S1")].iloc[0]
EUP05 = sm["europe_rice_gdd10_quantiles"]["P5"]
N = dict(inc_Mha=f1(inc / 1e6), T_star=f0(TS), P01=f0(cal["hokkaido_P01_pipeline"]), P10=f0(cal["hokkaido_P10_pipeline"]), P50=f0(cal["hokkaido_P50_pipeline"]), T_cal=f0(cal["T_star_calJunSep"]),
    hok_rice_kha=f0(cal["hokkaido_rice_ha"] / 1e3), t25=f0(sm["t25"]), t10=f0(sm["t10"]),
    pct_T=f1(c(TS, "cropland_pass_pct")), pct_900=f1(c(900, "cropland_pass_pct")), pct_1076=f1(c(EUP05, "cropland_pass_pct")), pass_Mha=f1(c(TS, "cropland_pass_ha") / 1e6),
    pct_aei=f1(c(TS, "cropland_thermal_aei_pct")), aei_Mha=f1(c(TS, "cropland_thermal_aei_pct") * inc / 1e8), pct_aei_900=f1(c(900, "cropland_thermal_aei_pct")),
    de_T=f1(c(TS, "germany_cropland_pass_pct")), de_900=f1(c(900, "germany_cropland_pass_pct")), de_inc_Mha=f1(sm["germany_incumbent_Mha"]),
    de_cell=f1(float(p1.germany_pass_pct[3])), de_P50=f1(float(p1.germany_pass_pct[4])), de_res_pp=f1((rs.germany_pass_pct - g5de).abs().max()),
    de_drop_pp=f1(c(TS, "germany_cropland_pass_pct") - c(900, "germany_cropland_pass_pct")),
    rice_kha=f1(sm["rice_mapped_ha"] / 1e3), rice_cells=f0(sm["rice_cells"]), rice_noinc_kha=f1(sm["rice_ha_in_cells_without_incumbent"] / 1e3),
    eu_P05=f0(EUP05), eu_P50=f0(sm["europe_rice_gdd10_quantiles"]["P50"]),
    om_P01=f2(c(cal["hokkaido_P01_pipeline"], "rice_omitted_pct")), om_T=f2(c(TS, "rice_omitted_pct")), om_P50=f2(c(cal["hokkaido_P50_pipeline"], "rice_omitted_pct")), om_900=f2(c(900, "rice_omitted_pct")),
    om_1100=f1(c(1100, "rice_omitted_pct")), om_1300=f1(c(1300, "rice_omitted_pct")), om_1400=f1(c(1400, "rice_omitted_pct")), om_T_inc=f2(c(TS, "rice_omitted_pct_incumbent_cells")),
    crop_drop_pp=f1(c(TS, "cropland_pass_pct") - c(900, "cropland_pass_pct")), crop_drop_Mha=f1((c(TS, "cropland_pass_ha") - c(900, "cropland_pass_ha")) / 1e6),
    om_rise_pp=f1(c(900, "rice_omitted_pct") - c(TS, "rice_omitted_pct")),
    om_T_ha=f0(c(TS, "rice_omitted_ha")), om_cells=f0(cl["omitted_cells"]), om_clusters=f0(cl["clusters_8conn"]), om_top5=f0(100 * cl["share_largest5_clusters"]),
    om_ital_fr=f0(100 * (geo.loc["Italy", f"omitted_ha_T{int(TS)}"] + geo.loc["France", f"omitted_ha_T{int(TS)}"]) / c(TS, "rice_omitted_ha")),
    om_fringe_cells_pct=f0(100 * cl["omitted_cells_with_rice_lt_1pct_of_cell"] / cl["omitted_cells"]), om_fringe_pct=f0(100 * cl["omitted_ha_in_cells_rice_lt_1pct"] / c(TS, "rice_omitted_ha")),
    sh_min=f2(shifts.min()), sh_max=f2(shifts.max()), nb3_T=f2(a(TS, "omitted only if all 3x3 neighbours fail")),
    loco_T=f"{lo[int(TS)]['loco_min_pct']:.2f}–{lo[int(TS)]['loco_max_pct']:.2f}%", loco_900=f"{lo[900]['loco_min_pct']:.2f}–{lo[900]['loco_max_pct']:.2f}%",
    jac_25=f2(jac("Europe", "S3")), jac_10=f2(jac("Europe", "S4")), jac_cal=f2(jac("Europe", "S2")), jac_900=f2(jac("Europe", "S1")), jac_P50=f2(jac("Europe", "S5")), jac_de_900=f2(jac("Germany", "S1")),
    dis_Mha=f1(s1.ref_only_ha / 1e6), T_om10=f0(cur.index[cur.rice_omitted_pct > 10].min()), T_om5=f0(cur.index[cur.rice_omitted_pct <= 5].max()), tm_lost_Mha=f1(float(tm.iloc[2, 0])), repo_url=REPO_URL)
json.dump(N, open(os.path.join(SUB, "EMA_MANUSCRIPT_VALUES.json"), "w"), indent=1)

# ---------------- tables ----------------
def prov(T): return cur.loc[T, "reference_label"]
refT = [t for t in cur.index if isinstance(cur.loc[t, "reference_label"], str)]
TABS = {
 "data": ("Data sources and their roles in the assessment.", ["Dataset", "Version, support", "Variable used", "Role"], [
   ["WorldClim (Fick & Hijmans, 2017)", "2.1; 1970–2000 normals; 2.5′, 5′, 10′", "Monthly mean temperature", "GDD10 target surface and grid reference calibration"],
   ["MapSPAM (IFPRI, 2019; Yu et al., 2020)", "2010 v2.0; 5′", "Harvested area of wheat, maize, barley, potato; rice (all technologies)", "Incumbent arable denominator; Hokkaido calibration; European rice coverage check"],
   ["GMIA (Siebert et al., 2013)", "v5; ~2005; 5′", "Area equipped for irrigation", "Non-compensatory infrastructure gate"],
   ["NASA POWER (NASA POWER Project, 2025)", "Daily point API v2; 1981–2024", "Daily mean temperature at Hokkaido points", "Point-derived alternative reference"],
   ["Natural Earth (Natural Earth, 2024)", "Admin 0, 1:50 m, v5.1", "Country polygons, continent attribute", "European domain and country attribution"]]),
 "refs": ("Named threshold references and their consequences on the fixed primary surface (WorldClim 2.1 5′, 29 April–11 September). Cropland shares are weighted by incumbent arable harvested area; omission is weighted by mapped MapSPAM rice harvested area.",
   ["GDD10", "Reference construction", "Europe thermal pass (%)", "Europe thermal + AEI (%)", "Germany pass (%)", "Rice omitted (%)"],
   [[f0(t), prov(t), f1(cur.loc[t, "cropland_pass_pct"]), f1(cur.loc[t, "cropland_thermal_aei_pct"]), f1(cur.loc[t, "germany_cropland_pass_pct"]), f2(cur.loc[t, "rice_omitted_pct"])] for t in refT]),
 "align": ("Sensitivity of the omitted share of mapped rice harvested area to co-registration and spatial support. Ranges are scenario ranges, not confidence intervals.",
   ["Test", f"T* = {f0(TS)}", "900", "1100"],
   [[tst.replace("rice grid shifted", "Rice layer shifted").replace("omitted only if all 3x3 neighbours fail", "3 × 3 neighbourhood rule").replace("2.5' sub-cell pass fraction", "2.5′ sub-cell pass fraction").replace("10' native surface", "Native 10′ surface"),
     *[f2(a(T, tst)) for T in (TS, 900, 1100)]] for tst in ["rice grid shifted (+0,+0) cells", "rice grid shifted (-1,-1) cells", "rice grid shifted (+0,+1) cells", "omitted only if all 3x3 neighbours fail", "2.5' sub-cell pass fraction", "10' native surface"]]
   + [["Leave-one-country-out range", *[f"{lo[int(T)]['loco_min_pct']:.2f}–{lo[int(T)]['loco_max_pct']:.2f}" for T in (TS, 900, 1100)]]]),
 "stab": (f"Classification stability of the thermal gate relative to the primary specification (T* = {f0(TS)} GDD10, 5′, 29 April–11 September), weighted by incumbent arable harvested area.",
   ["Domain", "Alternative specification", "Agreement (%)", "Jaccard (pass)", "Pass in primary only (Mha)", "Pass in alternative only (Mha)"],
   [[r.domain, re.sub(r"^S\d ", "", r.comparison).replace("(primary)", ""), f1(r.agreement_pct), f2(r.jaccard_pass), f2(r.ref_only_ha / 1e6), f2(r.comp_only_ha / 1e6)] for r in st.itertuples()]),
}
FIGS = {
 "germany": ("GERMANY_CONTROLLED_CONTRAST", f"Controlled decomposition of the German thermal pass share (incumbent arable land, {N['de_inc_Mha']} Mha). (a) Threshold recomputed along a path from the point-derived reference to the grid-calibrated T* and applied to a fixed WorldClim 5′ surface. (b) Rice-area 5th-percentile reference recalibrated and applied at each resolution."),
 "curve": ("THRESHOLD_OMISSION_CURVE", "Threshold sweep on the fixed primary surface. Blue: share of incumbent arable land in Europe (cropland-area weighted) and Germany passing the thermal gate. Orange: share of mapped MapSPAM rice harvested area in Europe omitted by the gate (rice-area weighted). Dashed lines mark T*, the point-derived reference and the 5th percentile of mapped European rice area."),
 "tradeoff": ("CANDIDATE_AREA_OMISSION_TRADEOFF", "Trade-off between candidate incumbent arable area retained for next-stage assessment and omitted mapped rice harvested area across thresholds (0–1800 GDD10). Orange points are the named references in Table 2. Candidate area is not feasible land. This is not a receiver-operating-characteristic curve because non-rice cropland is not a verified negative."),
 "geo": ("RICE_AREA_OMISSION_GEOGRAPHY", f"Mapped MapSPAM 2010 rice harvested area in Europe by the GDD10 of its 5′ cell, showing where rice area is omitted at T* = {N['T_star']}, 900 and 1100 GDD10. Marker area is proportional to rice harvested area (rice-area weights). ETRS89-LAEA projection."),
 "disagree": ("CLASSIFICATION_DISAGREEMENT_MAP", f"Agreement of the thermal gate between T* = {N['T_star']} GDD10 and the point-derived 900 GDD10 on incumbent arable cells (cropland-area weights). No cell passes at 900 and fails at T*, because the thresholds are nested on one surface. ETRS89-LAEA projection, 10 km display grid; classification on the native 5′ grid."),
}
# ---------------- OMML ----------------
M = 'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'
PLAIN = '<m:rPr><m:sty m:val="p"/></m:rPr>'
def mr(t, plain=False): return '<m:r>' + (PLAIN if plain else '') + f'<m:t xml:space="preserve">{t}</m:t></m:r>'
def ms(b, s): return f"<m:sSub><m:e>{mr(b)}</m:e><m:sub>{mr(s)}</m:sub></m:sSub>"
def nary(body): return f'<m:nary><m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/><m:supHide m:val="1"/></m:naryPr><m:sub>{mr("i")}</m:sub><m:sup/><m:e>{body}</m:e></m:nary>'
def eq(lhs, w, rel):
    num = nary(ms(w, "i") + mr("1[", True) + ms("G", "i") + mr(rel, True) + mr("T") + mr("]", True)); den = nary(ms(w, "i"))
    return f'<m:oMath {M}>{mr(lhs[0])}{mr("(", True)}{mr("T")}{mr(")", True)}{mr("=", True)}<m:f><m:num>{num}</m:num><m:den>{den}</m:den></m:f></m:oMath>'
EQS = {"candidate": (eq("C", "a", " ≥ "), "1"), "omission": (eq("O", "r", " &lt; "), "2")}

def base_doc():
    d = Document(); s = d.styles["Normal"]; s.font.name = "Times New Roman"; s.font.size = Pt(12); s.font.color.rgb = RGBColor(0, 0, 0)
    s.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "Times New Roman")
    s.paragraph_format.line_spacing = 2.0; s.paragraph_format.space_after = Pt(0)
    for hn in ["Heading 1", "Heading 2", "Title"]:
        hs = d.styles[hn]; hs.font.name = "Times New Roman"; hs.font.color.rgb = RGBColor(0, 0, 0); hs.font.size = Pt(12 if hn != "Title" else 14); hs.font.bold = True; hs.font.italic = hn == "Heading 2"
        rf = hs.element.get_or_add_rPr().get_or_add_rFonts()
        for at in ["w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"]: rf.attrib.pop(qn(at), None)
        rf.set(qn("w:ascii"), "Times New Roman"); rf.set(qn("w:hAnsi"), "Times New Roman")
    for sec in d.sections:
        sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Inches(1)
        ln = OxmlElement("w:lnNumType"); ln.set(qn("w:countBy"), "1"); ln.set(qn("w:restart"), "continuous"); ln.set(qn("w:distance"), "360"); sec._sectPr.append(ln)
        fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER; r = fp.add_run()
        for t, x in [("begin", None), (None, "PAGE"), ("end", None)]:
            if t: e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), t)
            else: e = OxmlElement("w:instrText"); e.text = x
            r._r.append(e)
    return d
def add_runs(par, text, size=None):
    text = re.sub(r"(?<!\*)T\*", "\x00", text)
    for chunk in re.split(r"(\*[^*]+\*)", text):
        if not chunk: continue
        it = chunk.startswith("*") and chunk.endswith("*") and len(chunk) > 2
        for part in re.split(r"(\x00)", chunk[1:-1] if it else chunk):
            if not part: continue
            if part == "\x00":
                r = par.add_run("T"); r.italic = True; r2 = par.add_run("*"); r2.italic = it
                if size: r.font.size = r2.font.size = Pt(size)
                continue
            r = par.add_run(part); r.italic = it
            if size: r.font.size = Pt(size)
def caption(d, label, cap):
    p = d.add_paragraph(); p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(12); p.paragraph_format.line_spacing = 1.15
    r = p.add_run(label + " "); r.bold = True; r.font.size = Pt(10); add_runs(p, cap, 10); return p
TABNUM, FIGNUM = {}, {}
def add_table(d, key):
    cap, hdr, rows = TABS[key]; TABNUM.setdefault(key, len(TABNUM) + 1)
    p = caption(d, f"Table {TABNUM[key]}", cap); p.paragraph_format.keep_with_next = True
    t = d.add_table(rows=1 + len(rows), cols=len(hdr)); t.style = "Table Grid"
    for j, h in enumerate(hdr): t.cell(0, j).text = h
    for i, row in enumerate(rows):
        for j, v in enumerate(row): t.cell(i + 1, j).text = str(v)
    WID = {"data": [1.4, 1.4, 1.7, 1.8], "refs": [0.7, 2.3, 0.85, 0.85, 0.8, 0.8], "align": [2.6, 1.2, 1.2, 1.3], "stab": [0.75, 2.2, 0.85, 0.75, 0.85, 0.9]}[key]
    t.autofit = False
    for j, col in enumerate(t.columns): col.width = Inches(WID[j])
    for i, row in enumerate(t.rows):
        for j, cc in enumerate(row.cells): cc.width = Inches(WID[j])
    for i, row in enumerate(t.rows):
        for cc in row.cells:
            for pp in cc.paragraphs:
                pp.paragraph_format.line_spacing = 1.0
                for rr in pp.runs: rr.font.size = Pt(9); rr.bold = i == 0
    d.add_paragraph()
def add_figure(d, key, embed):
    fn, cap = FIGS[key]; FIGNUM.setdefault(key, len(FIGNUM) + 1)
    if embed:
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.line_spacing = 1.0; p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(os.path.join(FIG, fn + ".png"), width=Inches(6.0 if key in ("curve", "germany") else 5.0))
    caption(d, f"Fig. {FIGNUM[key]}", cap)
def add_eq(d, key):
    x, n = EQS[key]; p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p._p.append(parse_xml(x)); p.add_run(f"\u2003\u2003({n})")

# ---------------- parse template ----------------
tpl = open(TPL, encoding="utf-8").read()
for k in set(re.findall(r"\{(\w+)\}", tpl)): assert k in N, k
txt = tpl.format(**N) if False else re.sub(r"\{(\w+)\}", lambda m: N[m.group(1)], tpl)
sec = {}; cur_h = None
for line in txt.split("\n"):
    if line.startswith("# ") and line[2:].isupper(): cur_h = line[2:]; sec[cur_h] = []; continue
    sec.setdefault(cur_h, []).append(line)
first = lambda k: next(l for l in sec[k] if l.strip()).strip()
title, abstract, keywords = first("TITLE"), first("ABSTRACT"), first("KEYWORDS")
body = [l for l in txt.split("# KEYWORDS")[1].split("\n# DECLARATIONS")[0].split("\n")[2:]]
decl = sec["DECLARATIONS"]; refs = [l for l in sec["REFERENCES"] if l.strip()]
wc = lambda s: len(re.findall(r"\S+", s))
assert 150 <= wc(abstract) <= 250, wc(abstract)
kw = [k.strip() for k in keywords.split(";")]; assert 4 <= len(kw) <= 6
assert all(k.lower() not in title.lower() for k in kw)
assert refs == sorted(refs, key=lambda r: re.sub(r"[^a-z]", "", r.lower()))

def render_body(d, lines, embed):
    for l in lines:
        if not l.strip(): continue
        if l.startswith("## "): d.add_heading(l[3:], level=2); continue
        if l.startswith("# "): d.add_heading(l[2:], level=1); continue
        m = re.match(r"\[\[(TABLE|FIG|EQ):(\w+)\]\]", l)
        if m:
            {"TABLE": lambda k: add_table(d, k), "FIG": lambda k: add_figure(d, k, embed), "EQ": lambda k: add_eq(d, k)}[m.group(1)](m.group(2)); continue
        p = d.add_paragraph(); p.paragraph_format.first_line_indent = Inches(0.3); add_runs(p, l)
def build(embed, path):
    TABNUM.clear(); FIGNUM.clear(); d = base_doc()
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; r = p.add_run(title); r.bold = True; r.font.size = Pt(14)
    for l in [AUTHOR, f"{AFFIL}", f"ORCID: {ORCID}", f"Corresponding author: {AUTHOR}. E-mail: {EMAIL}"]:
        q = d.add_paragraph(l); q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    d.add_heading("Abstract", level=1); add_runs(d.add_paragraph(), abstract)
    p = d.add_paragraph(); r = p.add_run("Keywords "); r.bold = True; p.add_run(" · ".join(kw))
    render_body(d, body, embed)
    d.add_heading("Declarations", level=1)
    for l in decl:
        if l.startswith("## "): d.add_heading(l[3:], level=2)
        elif l.strip(): add_runs(d.add_paragraph(), l)
    d.add_heading("References", level=1)
    for rf in refs:
        p = d.add_paragraph(); p.paragraph_format.left_indent = Inches(0.5); p.paragraph_format.first_line_indent = Inches(-0.5); add_runs(p, rf)
    d.save(path); return d
os.makedirs(os.path.join(SUB, "tables"), exist_ok=True)
for i, (k, (cap, hdr, rows)) in enumerate(TABS.items(), 1): pd.DataFrame(rows, columns=hdr).to_csv(os.path.join(SUB, "tables", f"Table_{i}.csv"), index=False)
MS = os.path.join(SUB, "01_EMA_MANUSCRIPT_FINAL.docx"); RV = os.path.join(SUB, "EMA_MANUSCRIPT_REVIEW_COPY.docx")
build(False, MS); build(True, RV)
assert list(FIGNUM) == ["germany", "curve", "tradeoff", "geo", "disagree"] and list(TABNUM) == ["data", "refs", "align", "stab"]

# citation order check: first citation of Fig./Table n in body text must be ascending
btxt = " ".join(l for l in body if not l.startswith("[["))
for lab in ("Fig.", "Table"):
    firsts = [int(m) for m in re.findall(rf"{re.escape(lab)} (\d+)", btxt)]
    seen = []; [seen.append(x) for x in firsts if x not in seen]; assert seen == sorted(seen) == list(range(1, len(seen) + 1)), (lab, seen)
# in-text citation <-> reference list
cited = set(re.findall(r"([A-Z][A-Za-z\-]+)(?: et al\.| & [A-Z][A-Za-z\-]+)?,? \(?(\d{4})\)?", btxt))
surn = {(re.match(r"([A-Za-z\- ]+?),", r) or re.match(r"([A-Za-z\- ]+?)\.", r)).group(1).split()[-1]: r for r in refs}
for s_, y in [(re.match(r"[^,(.]+", r).group(0).split()[-1], re.search(r"\((\d{4})\)", r).group(1)) for r in refs]:
    assert re.search(rf"{s_}[^()]*?,? {y}", btxt) or f"{s_} Project, {y}" in btxt or f"{s_}, {y}" in btxt, ("uncited reference", s_, y)
for dd in (MS, RV):
    D = Document(dd); alltxt = "\n".join(p.text for p in D.paragraphs) + "\n".join(c.text for t in D.tables for row in t.rows for c in row.cells)
    assert "*" not in alltxt.replace("T*", "") and "{" not in alltxt and "[[" not in alltxt, dd
    assert "Applied Geography" not in alltxt.split("References")[0]
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", SUB, RV], check=True, capture_output=True)
os.replace(os.path.join(SUB, "EMA_MANUSCRIPT_REVIEW_COPY.pdf"), os.path.join(SUB, "02_EMA_MANUSCRIPT_REVIEW.pdf"))
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.join(SUB, "render_check"), MS], check=True, capture_output=True)

# ---------------- cover letter ----------------
d = base_doc()
for sct in d.sections: sct._sectPr.remove(sct._sectPr.find(qn("w:lnNumType")))
d.styles["Normal"].paragraph_format.line_spacing = 1.15; d.styles["Normal"].paragraph_format.space_after = Pt(8)
CL = [f"{AUTHOR}", AFFIL, f"E-mail: {EMAIL}", "", "To the Editor-in-Chief, Environmental Monitoring and Assessment", "",
 f"Dear Editor,",
 f"I submit the original research article “{title}” for consideration in Environmental Monitoring and Assessment.",
 f"The manuscript addresses the reliability of spatial environmental suitability assessments that transfer a climatic threshold from a reference region. Using WorldClim 2.1 climate normals, MapSPAM 2010 crop harvested areas and the Global Map of Irrigation Areas on one 5′ grid, I assess a growing-degree-day gate for transferring the cold-region rice system of Hokkaido to {N['inc_Mha']} Mha of incumbent arable land in Europe.",
 f"The main findings are as follows. First, in a controlled contrast for Germany, the thermal pass share is {N['de_T']}% with a grid-calibrated reference and {N['de_900']}% with a point-derived reference, whereas recalibration across 2.5′–10′ grids changes it by at most {N['de_res_pp']} percentage points; reference construction, not resolution, dominates. Second, a full threshold sweep against {N['rice_kha']} thousand ha of mapped European rice harvested area shows that omission stays between {N['om_T']}% and {N['om_900']}% between the competing references while candidate area changes by {N['crop_drop_pp']} percentage points, so presence-only reference data cannot discriminate between them. Third, a non-compensatory irrigation-infrastructure gate reduces the candidate area to {N['pct_aei']}% of incumbent arable land.",
 "The incremental contribution relative to suitability studies recently published in the journal, which typically apply multi-criteria or distribution models with a single threshold set, is an explicit assessment of reference-dependent instability together with an omission-versus-candidate-area analysis and an audit of the independence of the reference data. I do not propose a new monitoring network, a physiological threshold or an operational feasibility assessment. The mapped rice data are a modelled allocation of statistics rather than field observations, non-rice cropland is not a verified negative, and the manuscript states these limitations explicitly.",
 "This manuscript has not been published and is not under consideration elsewhere. I have no competing interests to declare, and the study received no specific funding. All code and derived data are available in a public repository.",
 "Sincerely,", AUTHOR]
for l in CL: d.add_paragraph(l)
d.save(os.path.join(SUB, "03_EMA_COVER_LETTER_FINAL.docx"))
print("abstract words", wc(abstract), "| body words", wc(" ".join(l for l in body if not l.startswith("[["))), "| refs", len(refs))
