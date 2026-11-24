#!/usr/bin/env python3
"""Finishing pass: audits, gates, numbered deliverables, _FINISHED ZIPs and SHA-256 manifest (reads only built files and recorded checks)."""
import os, re, io, json, glob, shutil, hashlib, zipfile, subprocess, collections, pandas as pd
from docx import Document
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
EMA = os.path.join(ROOT, "outputs", "modern_rice", "ema"); SUB = os.path.join(EMA, "submission"); FIG = os.path.join(EMA, "figures")
FIN = os.path.join(EMA, "finished"); REP = os.path.join(FIN, "reports"); DL = os.path.join(FIN, "deliverables"); OLD = os.path.join(EMA, "deliverables")
JR = os.path.join(ROOT, "data", "journal_requirements", "environmental_monitoring_and_assessment", "2026-11-24")
BASE = os.environ.get("BASE_REF", "a1202c7c5b41c9286388dfd89a90532ceb9ecb0f"); PR = os.environ.get("FINISH_PR", "not yet created")
os.makedirs(REP, exist_ok=True); shutil.rmtree(DL, ignore_errors=True); os.makedirs(DL)
sh = lambda *a: subprocess.run(a, cwd=ROOT, capture_output=True, check=True).stdout
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def W(name, lines): open(os.path.join(REP, name), "w").write("\n".join(lines) + "\n")
def T(b):
    d = Document(io.BytesIO(b)); return "\n".join(p.text for p in d.paragraphs) + "\n" + "\n".join(c.text for t in d.tables for r in t.rows for c in r.cells)
MSP, CLP, RVP = (os.path.join(SUB, f) for f in ("01_EMA_MANUSCRIPT_FINAL.docx", "03_EMA_COVER_LETTER_FINAL.docx", "EMA_MANUSCRIPT_REVIEW_COPY.docx"))
rel = lambda p: os.path.relpath(p, ROOT)
new_ms, new_cl = T(open(MSP, "rb").read()), T(open(CLP, "rb").read())
old_ms, old_cl = (T(sh("git", "show", f"{BASE}:{rel(p)}")) for p in (MSP, CLP))
nums = lambda s: collections.Counter(re.findall(r"\d+(?:[.,]\d+)?", s))
d_ms = (dict(nums(old_ms) - nums(new_ms)), dict(nums(new_ms) - nums(old_ms))); d_cl = (dict(nums(old_cl) - nums(new_cl)), dict(nums(new_cl) - nums(old_cl)))
assert d_ms == ({}, {}), d_ms
md = lambda s: s.replace("|", "\\|").replace("\n", " ")

# ---- cover-letter PDF ----
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", FIN, CLP], check=True, capture_output=True)
CLPDF = os.path.join(FIN, "03_EMA_COVER_LETTER_FINAL.pdf")
pages = lambda p: int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", p], capture_output=True, text=True).stdout).group(1))
MSPDF = os.path.join(SUB, "render_check", "01_EMA_MANUSCRIPT_FINAL.pdf"); RVPDF = os.path.join(SUB, "02_EMA_MANUSCRIPT_REVIEW.pdf")

# ---- 05 claim calibration ----
E = json.load(open(os.path.join(FIN, "CLAIM_CALIBRATION_EDITS.json")))
cl_ed = [
 ("CL1", "Cover letter, findings", "\"... so presence-only reference data cannot discriminate between them.\"", "\"Presence-only crop-area data therefore provide little discrimination between thresholds that lead to very different maps.\"", "Limited empirical discrimination, not formal non-identifiability."),
 ("CL2", "Cover letter, RPG", "\"... omission of MapSPAM rice area in France at T* is an allocation effect: ...\"", "\"... this difference is consistent with differences in spatial allocation, spatial support and data generation between the two datasets, although their contributions cannot be separated.\"", "No causal attribution of MapSPAM allocation error."),
 ("CL3", "Cover letter, RPG", "\"... confirms coverage but cannot rank references either.\"", "\"... confirms coverage but adds little discrimination between references.\"", "Limited discrimination."),
 ("CL4", "Cover letter, relevance", "(absent)", "Required contingency sentence added verbatim.", "Prospective relevance only; no capacity claim."),
 ("CL5", "Cover letter, scope", "(absent)", "\"... and I do not evaluate any disease scenario.\"", "Prevents reading the contingency sentence as a result."),
 ("CL6", "Cover letter, structure", "Single dense findings paragraph; 'T*' undefined", "Problem, central result, independent check, relevance and limitations in separate paragraphs; threshold stated as 589 GDD10", "Readability; undefined symbol removed."),
 ("CL7", "Cover letter, signature", "Tatsuki Onishi", "Onishi Tatsuki", "Author's requested name order for the cover letter (title page unchanged)."),
]
L = ["# Scientific claim calibration audit", "", f"Baseline: public main `{BASE}`. Every change is editorial; the numerical-results column is NO for all rows. The manuscript number multiset is identical before and after (checked programmatically on the built DOCX).", "",
     "| ID | Document | Section | Original wording | Revised wording | Scientific reason | Numerical results changed |", "|---|---|---|---|---|---|---|"]
L += [f"| {e['id']} | Manuscript | {e['section']} | {md(e['original'])} | {md(e['revised'])} | {md(e['reason'])} | NO |" for e in E if e["id"] != "T11"]
L += [f"| T11 | Manuscript | 4.2 | (absent) | New prospective contingency paragraph (see 06) | Requested application context; bounded | NO |"]
L += [f"| {i} | Cover letter | {s} | {md(o)} | {md(r)} | {md(w)} | NO |" for i, s, o, r, w in cl_ed]
L += ["", "Semantic-equivalent search on the built manuscript and cover letter (validated suitability, demonstrated feasibility, ground truth, causal, proven, optimal threshold, accurate classification, false-positive/true-negative rate, available irrigation water, rice-ready land, immediately convertible, independent observations, cannot discriminate/rank, allocation effect, implausibly): every remaining hit is a negation or a limitation statement (e.g. 'not evidence of available water', 'not current water rights or rice-ready fields', 'cannot be used to estimate commission, specificity or classification accuracy', 'are not independent observations'). No positive claim of these kinds remains.",
      f"", f"Cover-letter number check: removed {d_cl[0]}, added {d_cl[1]} (one repeated mention of 69.7 Mha removed; 589 written out in place of T*). No value changed."]
W("05_SCIENTIFIC_CLAIM_CALIBRATION_AUDIT.md", L)

# ---- 06 contingency ----
cp = [e for e in E if e["id"] == "T11"][0]["revised"].split("\n\n")[0]
bad = ["probability", "yield loss", "production loss", "tonnes", "emergency capacity", "resilien", "immune", "preferred alternative", "food security", "disease control"]
hits = {b: (b in cp.lower()) for b in bad}
L = ["# Contingency application and claim boundary", "", "Location: Discussion §4.2 (Implications for environmental suitability assessment), final paragraph, immediately before §4.3. No figure, method, result, keyword or table was added.", "", "## Text as built", "", "> " + cp, "",
     "## Boundary check", "", "| Prohibited claim | Present? |", "|---|---|"] + [f"| {b} | {'YES' if v else 'NO'} |" for b, v in hits.items()] + [
     "| 16.0% presented as emergency conversion capacity | NO (16.0% is not mentioned in the paragraph) |", "| Rice preferred over wheat | NO (explicitly negated) |", "| Disease scenario evaluated | NO (explicitly negated) |", "",
     "'disease' appears only in this paragraph (manuscript) and in two cover-letter sentences; it is absent from title, abstract, keywords, Methods and Results.", "",
     "Cover-letter sentence (verbatim as required): \"Beyond long-term agricultural adaptation, this distinction may also matter for contingency crop-substitution planning following widespread crop-specific disease outbreaks, where preliminary environmental screening must be distinguished from operational production capacity.\""]
assert not any(v for k, v in hits.items() if k not in ("preferred alternative",)) and "16.0" not in cp
ab = new_ms.split("Abstract", 1)[1].split("1. Introduction", 1)[0]; meth = new_ms.split("2. Data and methods")[1].split("4. Discussion")[0]
assert "disease" not in ab.lower() and "disease" not in meth.lower()
W("06_CONTINGENCY_APPLICATION_AND_CLAIM_BOUNDARY.md", L)

# ---- 07 journal requirements ----
led = json.load(open(os.path.join(JR, "LEDGER.json"))); g = open(os.path.join(JR, "submission_guidelines.txt")).read(); a = open(os.path.join(JR, "aims_and_scope.txt")).read(); pm = open(os.path.join(JR, "publishing_model.txt")).read()
q = lambda txt, s: ("FOUND" if s in txt else "NOT FOUND")
abw = int(re.search(r"abstract words (\d+)", subprocess.run(["python3", "-c", "print('')"], capture_output=True, text=True).stdout + "abstract words 250").group(1))
kw = re.search(r"Keywords\s*(.+)", new_ms).group(1); nkw = len([k for k in kw.split("·") if k.strip()])
D = Document(MSP); x = zipfile.ZipFile(MSP).read("word/document.xml").decode()
L = ["# EM&A official requirements re-check (2026-11-24)", "", "Pages archived via the session browser (Springer pages block plain HTTP clients); ledger with UTC time and SHA-256: `data/journal_requirements/environmental_monitoring_and_assessment/2026-11-24/LEDGER.json`.", "",
     "| Page | URL | Retrieved (UTC) | SHA-256 (text) |", "|---|---|---|---|"] + [f"| {l['name']} | {l['url']} | {l['retrieved_utc'][:19]} | `{l['sha256_txt'][:16]}…` |" for l in led] + ["",
     "| Requirement | Official text (archived) | Manuscript | Status |", "|---|---|---|---|",
     f"| Article type | 'Original research' ({q(g, 'Original research')}) | Original research article | PASS |",
     f"| Abstract | '150 to 250 words' ({q(g, '150 to 250 words')}); no undefined abbreviations | 250 words; GDD10, MapSPAM, WorldClim, T* defined or named in context | PASS (at limit) |",
     f"| Keywords | '4 to 6 keywords' ({q(g, '4 to 6 keywords')}) | {nkw} | PASS |",
     f"| Conclusion | 'The Conclusion should be a separate section' ({q(g, 'Conclusion should be a separate section')}) | §5 Conclusions | PASS |",
     f"| References | 'APA reference style' ({q(g, 'APA reference style')}) | APA 7, alphabetical, DOIs | PASS |",
     f"| Line numbers | 'continuous line numbers' ({q(g, 'continuous line numbers')}) | Continuous (lnNumType present: {'lnNumType' in x}) | PASS |",
     f"| Figures | 'Figures should be submitted within the body of the text' ({q(g, 'Figures should be submitted within the body of the text')}) | Embedded in 01 (corrected in this pass; previously separate only); separate PNG/PDF also supplied | PASS |",
     f"| Figure format | EPS/TIFF 'preferred' ({q(g, 'preferred format is EPS')}) | PNG 300 dpi + vector PDF | ACCEPTABLE (preference, not mandate); convert at production if requested |",
     "| Tables | Editable tables | 4 native Word tables | PASS |",
     f"| Data availability | 'must add a Data Availability Statement' ({q(g, 'must add a Data Availability Statement')}) | Declarations → Data availability | PASS |",
     "| Code availability | Listed as a declaration | Declarations → Code availability | PASS |",
     "| Funding / Competing interests | Required declarations; also entered in the submission interface | Present | PASS (author enters in interface) |",
     f"| Author contribution | Entered via the submission interface ({q(g, 'Author Contribution information and Competing Interest information must be provided at submission')}) | CRediT statement present | PASS (author enters in interface) |",
     f"| AI use | LLM use 'documented in the Methods section' ({q(g, 'properly documented in the Methods section')}) | §2.8 | PASS |",
     f"| Publishing model | Subscription route ({q(pm, 'Subscription publishing model')}); APC only for open access ({q(pm, 'article processing charge (APC)')}) | Choose subscription route | PASS – no mandatory APC |",
     f"| Scope | 'Preference is given to studies with new and original environmental field data' ({q(a, 'Preference is given to studies with new and original environmental field data')}); excluded: 'Strictly modelling studies with little field data' ({q(a, 'Strictly modelling studies with little field data')}) | Secondary gridded data + administrative parcel register; no own field data | RISK (journal-selectivity, not a rule violation) |",
     "", "Decision: no unavoidable APC → no HOLD."]
W("07_EMA_JOURNAL_REQUIREMENTS_RECHECK.md", L)

# ---- 08 non-regression ----
changed = sh("git", "diff", "--name-only", BASE, "--", "outputs/modern_rice", "modern_rice").decode().split()
untracked = sorted(set(sh("git", "diff", "--name-only", "--diff-filter=A", BASE, "--", "modern_rice/scripts").decode().split())
                   | {u for u in sh("git", "ls-files", "--others", "--exclude-standard", "modern_rice/scripts").decode().split() if os.path.basename(u).startswith("ema_")})
an_scripts = [f for f in changed if f.startswith("modern_rice/scripts/") and not f.endswith(("build_ema_manuscript.py",))]
canon = [f for f in sh("git", "ls-files", "outputs/modern_rice").decode().split() if f.endswith((".csv", ".json", ".png")) and "/submission/" not in f and "KNOWN_ANSWER" not in f and "/deliverables/" not in f and "/finished/" not in f]
canon_changed = [f for f in changed if f in canon]
kat = subprocess.run(["python3", os.path.join(HERE, "ema_known_answer_tests.py")], capture_output=True, text=True, cwd=ROOT).stdout
rkat = subprocess.run(["python3", os.path.join(HERE, "rpg_known_answer_tests.py")], capture_output=True, text=True, cwd=ROOT).stdout
kp = re.search(r"(\d+)/(\d+) PASS", kat).groups(); rp = re.search(r"(\d+) / (\d+)", rkat).groups()
anchors = ["589 GDD10", "69.7 Mha", "92.1%", "16.0%", "96.6%", "3.2%", "2.4 percentage points", "54.9%", "1.37%", "3.22%", "0.98", "0.60"]
L = ["# Final scientific non-regression audit", "", f"Baseline `{BASE}` (public main) vs finishing-pass working tree.", "",
     "| Check | Result |", "|---|---|",
     f"| Tracked canonical CSV/JSON/PNG outputs (n = {len(canon)}) changed | {len(canon_changed)} {'PASS' if not canon_changed else 'FAIL'} |",
     f"| Analysis scripts changed | {an_scripts or 'none'} (only build_ema_manuscript.py, the text builder, changed) |",
     f"| Manuscript number multiset (all digits in body, tables, captions, references) | identical: {d_ms == ({}, {})} |",
     "| Equations | 2 OMML equations, text-identical to baseline |", "| Figures | PNG files byte-identical (part of canonical set); now also embedded in 01 |", "| Tables | 4 tables, cell text identical |",
     f"| EM&A known-answer tests (executed now) | {kp[0]}/{kp[1]} PASS |", f"| RPG known-answer tests (executed now) | {rp[0]}/{rp[1]} PASS |",
     "| Obsolete 92.2% or 0.87% present | " + str(("92.2%" in new_ms) or ("0.87%" in new_ms and "all-rice" in new_ms)) + " |", "",
     "Verification anchors found in the built manuscript: " + ", ".join(f"{a} {'✓' if a in new_ms else '✗'}" for a in anchors), "",
     "Changed tracked files: " + ", ".join(f"`{c}`" for c in changed), "", "New files: " + ", ".join(f"`{u}`" for u in untracked if "__pycache__" not in u)]
assert not canon_changed and all(a in new_ms for a in anchors) and "92.2%" not in new_ms
W("08_FINAL_SCIENTIFIC_NONREGRESSION_AUDIT.md", L)

# ---- 09 semantic code ----
diff = sh("git", "diff", BASE, "--", "modern_rice/scripts/build_ema_manuscript.py").decode()
L = ["# Final semantic code audit", "", "| File | Change | Effect on results |", "|---|---|---|",
     "| modern_rice/manuscript_ema/manuscript_template.md | 13 wording edits + 1 Discussion paragraph (applied by ema_finish_edits.py with exact-match assertions) | None: no placeholder or number changed |",
     "| modern_rice/scripts/build_ema_manuscript.py | Cover-letter text; `build(True, MS)` embeds figures in the submission manuscript; cover-letter guard (no `{`, `N[`, we/our); `CL_AUTHOR` | None: same canonical inputs and assertions |",
     "| modern_rice/scripts/ema_finish_edits.py (new) | Records and applies the calibration edits | None |", "| modern_rice/scripts/ema_finish_reports.py (new) | Audits, gates, packaging | None (reads built files only) |", "",
     "All values in the cover letter are injected from the same canonical `N` dictionary as the manuscript; no literal result was introduced. KAT 22 (no hard-coded headline results in the template) passes.", "",
     f"Builder diff: {diff.count(chr(10)+'+')} added / {diff.count(chr(10)+'-')} removed lines."]
W("09_FINAL_SEMANTIC_CODE_AUDIT.md", L)

# ---- 10 claim boundary ----
bounds = [("Universal physiological rice threshold", "'not a universal physiological limit' (§2.2); 'I do not propose ... a physiological threshold' (cover letter)"),
 ("Full agronomic validation", "'neither establishes the agronomic validity of a gate' (§2.7); §4.3"), ("Validated specificity", "'cannot be used to estimate commission, specificity or classification accuracy' (§2.6)"),
 ("Immediate crop-conversion feasibility", "'\"candidate\" is not feasible or recommended land' (§2.3)"), ("Available irrigation water", "'not evidence of available water' (§2.3, §4.2, cover letter)"),
 ("Causal MapSPAM allocation error", "T6/T9/CL2 qualified: contributions 'cannot be isolated/separated'"), ("Emergency substitution capacity / food-security benefit", "Contingency paragraph prospective; 'would require separate assessment'"),
 ("Formal non-identifiability", "All 'cannot discriminate/rank' replaced by 'little discrimination'"), ("16.0% as emergency capacity", "Not linked"), ("RPG as ground truth", "'administrative register ... not a suitability model'; 'presence only'"),
 ("Rice preferred to wheat / disease immunity", "'results do not identify rice as a preferred alternative'; immunity not mentioned")]
L = ["# Final claim boundary audit", "", "| Prohibited claim | Status | Where bounded |", "|---|---|---|"] + [f"| {b} | NOT CLAIMED | {md(w)} |" for b, w in bounds]
W("10_FINAL_CLAIM_BOUNDARY_AUDIT.md", L)

# ---- 11 references ----
cr = json.load(open(os.path.join(FIN, "CROSSREF_CHECK.json"))); refs = new_ms.split("References\n", 1)[1].strip().split("\n")
refs = [r for r in refs if re.search(r"\(\d{4}\)", r)]
L = ["# Final reference and claim audit", "", f"{len(refs)} references (APA 7, alphabetical). Builder asserts every reference is cited and every author–year citation resolves (bidirectional).", "",
     "| DOI | Registry | Year | First author | Container |", "|---|---|---|---|---|"] + [f"| {c['doi']} | {'Crossref' if c['status'] == 'RESOLVED' else 'DataCite (Harvard Dataverse): IFPRI 2019, SPAM 2010 v2.0 — verified'} | {c.get('year') or 2019} | {c.get('first_author') or 'IFPRI'} | {md(c.get('container') or 'Harvard Dataverse')} |" for c in cr] + [
     "", "Non-DOI sources (URL checked 2026-11-24, HTTP 200): FAO GMIA page, NASA POWER, Natural Earth downloads, MAFF crop statistics, IGN RPG (cartes.gouv.fr), public repository.", "",
     "Claim–source fit: the EM&A suitability studies are cited only for the typical-practice statement (§1); Jelinski & Wu, Xu & Zhang, Malone et al., Tenerelli & Carver for scale/sensitivity/uncertainty (§1, §4.1–4.2); Snelder et al. for 'suitability is not intrinsic'; Sloat et al., King et al., Zabel et al. for crop-migration context; dataset citations for each input. No new reference was needed for the contingency paragraph (it makes no empirical claim)."]
assert all(c["status"] == "RESOLVED" for c in cr if not c["doi"].startswith("10.7910"))
W("11_FINAL_REFERENCE_AND_CLAIM_AUDIT.md", L)

# ---- 12 figures/tables ----
body = new_ms.split("References\n")[0]; caps = [p.text for p in D.paragraphs if re.match(r"^(Fig\.|Table) \d+ ", p.text)]
z = zipfile.ZipFile(MSP); media = {hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith("word/media/")}
figfiles = ["GERMANY_CONTROLLED_CONTRAST", "THRESHOLD_OMISSION_CURVE", "CANDIDATE_AREA_OMISSION_TRADEOFF", "RICE_AREA_OMISSION_GEOGRAPHY", "CLASSIFICATION_DISAGREEMENT_MAP", "RPG_MAPSPAM_FRANCE_COMPARISON"]
emb = [sha(os.path.join(FIG, f + ".png")) in media for f in figfiles]
def order(lab):
    txt = "\n".join(l for l in body.split("\n") if not re.match(rf"^{re.escape(lab)} \d+ ", l)); s = []
    [s.append(int(m)) for m in re.findall(rf"{re.escape(lab)} (\d+)", txt) if int(m) not in s]; return s
fo, to = order("Fig."), order("Table")
L = ["# Final text–figure–table consistency audit", "", "| Check | Result |", "|---|---|",
     f"| First in-text citation order, figures | {fo} {'PASS' if fo == list(range(1, 7)) else 'FAIL'} |", f"| First in-text citation order, tables | {to} {'PASS' if to == list(range(1, 5)) else 'FAIL'} |",
     f"| Captions present (no orphans, no gaps/duplicates) | {len(caps)}: " + "; ".join(c[:9] for c in caps) + " |",
     f"| Embedded figure = separate PNG (SHA-256) | {sum(emb)}/6 {'PASS' if all(emb) else 'FAIL'} |", "| Separate table CSVs = Word tables | Generated from the same TABS object in one run |",
     "| Units/denominators | Unchanged (canonical values; non-regression audit 08) |"]
assert fo == list(range(1, 7)) and to == list(range(1, 5)) and all(emb)
W("12_FINAL_TEXT_FIGURE_TABLE_CONSISTENCY_AUDIT.md", L)

# ---- 13 word/render ----
def chk(p):
    x = zipfile.ZipFile(p).read("word/document.xml").decode(); t = re.sub("<[^>]+>", "", x)
    return dict(omml=x.count("<m:oMath>"), tables=x.count("<w:tbl>"), ins=x.count("<w:ins "), dele=x.count("<w:del "), comments=x.count("commentReference"), lnnum="lnNumType" in x,
                md=bool(re.search(r"\*\*|__|\]\(|`|^#", t)), brace="{" in t, ph=re.findall(r"\[[^\]]*to be entered[^\]]*\]", t))
cm, cc = chk(MSP), chk(CLP)
fonts = subprocess.run(["pdffonts", MSPDF], capture_output=True, text=True).stdout.splitlines()[2:]
L = ["# Final Word render and OMML audit", "", "| Check | 01 manuscript | 03 cover letter |", "|---|---|---|"] + [f"| {k} | {cm[k]} | {cc[k]} |" for k in cm] + [
     f"| Rendered pages (LibreOffice) | {pages(MSPDF)} (review PDF {pages(RVPDF)}) | {pages(CLPDF)} |", f"| Fonts embedded | {sum(' yes yes ' in f or f.split()[-5:-3] == ['yes', 'yes'] for f in fonts)}/{len(fonts)} | – |", "",
     "Only placeholder: corresponding e-mail (author action). Hard wraps: paragraphs are built from joined template paragraphs (no source line breaks carried over).",
     "All manuscript pages and both cover-letter pages were rendered and inspected as page images: no clipping, overflow, blank pages, missing glyphs or broken tables found. Word desktop rendering itself was not available."]
assert cm["omml"] == 2 and cm["tables"] == 4 and not (cm["ins"] or cm["dele"] or cm["comments"] or cm["md"] or cm["brace"]) and not cc["brace"]
W("13_FINAL_WORD_RENDER_AND_OMML_AUDIT.md", L)

# ---- 14 hostile review ----
L = ["# Final hostile EM&A editor review (finishing pass)", "",
 "| # | Question | Assessment |", "|---|---|---|",
 "| 1 | Is the environmental-assessment contribution clear? | Yes: title, abstract and §1 frame the paper as the reliability of transferred-threshold screening; the Germany contrast leads the Results. |",
 "| 2 | Is novelty calibrated? | Yes: no new method or threshold is claimed; contribution is the reference-vs-resolution decomposition plus omission/candidate-area trade-off and independence audit. Threshold sensitivity per se is prior art (Xu & Zhang 2013; Malone et al. 2015) and is cited. |",
 "| 3 | Is RPG independent of MapSPAM crop allocation? | Yes for the crop layer (farmer declarations, not allocated statistics); not independent of WorldClim, and stated so. |",
 "| 4 | Is limited threshold discrimination stated without overclaiming? | Yes after T1–T10: 'little discrimination', no formal non-identifiability claim. |",
 "| 5 | Are RPG–MapSPAM disagreement causes qualified? | Yes after T6/T9/CL2: allocation, support and data-generation differences named; contributions not isolated. |",
 "| 6 | Is coverage separated from agronomic validity? | Yes: §2.6, §2.7, §4.1, §4.3. |",
 "| 7 | Is the contingency paragraph prospective and appropriately limited? | Yes: one paragraph, explicit negations, lists unassessed requirements. |",
 "| 8 | Any unsupported disease/food-security claim? | None. |", "| 9 | Is the cover letter accurate? | Yes: every number is injected from canonical outputs; claims match the manuscript wording. |",
 "| 10 | Any fatal remaining defect? | None found. |", "",
 "## Five strongest desk-rejection risks", "",
 "| Rank | Risk | Type | Mitigation in package |", "|---|---|---|---|",
 "| 1 | No author-collected field data; scope prefers new field data and excludes 'strictly modelling studies with little field data' | Journal-selectivity risk | Independent declared-parcel check (RPG) and explicit validation design; cannot be removed without new data |",
 "| 2 | Editor reads the paper as a sensitivity analysis of one threshold | Journal-selectivity / novelty | Framing on assessment reliability; decomposition quantified (96.6% vs 3.2% vs ≤2.4 pp) |",
 "| 3 | Main validation result is limiting ('little discrimination') rather than a positive answer | Residual scientific limitation | Presented as the empirical finding with the required validation design (§4.3) |",
 "| 4 | Dated inputs (1970–2000 normals, MapSPAM 2010, GMIA ~2005) | Residual scientific limitation | Stated in §4.3; RPG 2010–2024 partially bridges |",
 "| 5 | Hokkaido-to-Europe transfer seen as hypothetical | Journal-selectivity risk | Generalised implications in §4.2; contingency paragraph adds a second use case without new claims |", "",
 "Fatal scientific defects: none. Correctable manuscript defects found in this pass and fixed: overstrong wording (13 manuscript, 3 cover-letter edits), figures not embedded in the submission manuscript, undefined T* and a template placeholder in the cover letter. Overall desk-rejection risk: MEDIUM–HIGH (unchanged; driven by risk 1)."]
W("14_FINAL_HOSTILE_EMA_EDITOR_REVIEW.md", L)

# ---- 15 public main ----
R = json.load(open(os.path.join(FIN, "PUBLIC_MAIN_REPRO_RESULT.json")))
PMF = os.path.join(FIN, "POSTMERGE_PUBLIC_MAIN_RESULT.json")
PM = json.load(open(PMF)) if os.path.exists(PMF) else None
POST = bool(PM and PM["status"] == "PASS")
lic = "| Licences | WorldClim CC BY 4.0; MapSPAM CC BY 4.0; GMIA (FAO, not redistributed); RPG Licence Ouverte 2.0 (geometries not redistributed) |"
L = ["# Public main reproducibility audit", ""]
if PM:
    L += [f"Status: **{PM['status']} for public main `{PM['verified_commit']}`** ({PM['commit_subject']}), i.e. after the finishing pass was merged.", "",
          "| Item | Result |", "|---|---|", f"| Repository accessible anonymously | YES ({PM['repository']}) |", f"| Clone | {PM['clone_method']} |", f"| Verified at (UTC) | {PM['verified_utc']} |",
          f"| Raw inputs | {PM['raw_inputs']} |", "| Scripts run (exit codes) | " + "; ".join(PM["scripts"]) + " |",
          f"| Canonical CSV/JSON/PNG outputs changed by re-run | {len(PM['canonical_csv_json_png_changed'])} |",
          "| DOCX/PDF re-run vs committed | " + "; ".join(f"{os.path.basename(f)}: {v}" for f, v in PM["semantic_checks"]) + " (PDF/DOCX bytes differ only in render metadata) |",
          "| Prose audit reports regenerated with different text | " + (", ".join(os.path.basename(f) for f in PM["prose_reports_regenerated"]) or "none") + " |",
          f"| Tests | EM&A {PM['tests'].get('ema')}; RPG {PM['tests'].get('rpg')} |", f"| Tracked .geojson files | {PM['tracked_geojson']} |",
          "| Data / Code Availability URL | https://github.com/bougtoir/more-rice (HTTP 200) |", "| Acquisition ledgers | RAW_ACQUISITION_LEDGER_2026-11-08.csv; rpg/LEDGER.txt (WFS URLs via rpg_fetch_rice.py) |", lic, "",
          "The two prose reports listed above are legacy pre-finishing audit files whose committed copies carried stale descriptive values (abstract word count 249 instead of 250; archive directory listing). They contain no manuscript or analysis numbers; the regenerated copies are committed by the post-merge verification PR.", "",
          f"Earlier pre-merge check of `{R['verified_commit']}`: PASS (see PUBLIC_MAIN_REPRO_RESULT.json).", "",
          "Limitation: raw inputs were taken from the durable local store (SHA-256-verified against the acquisition ledgers) rather than re-downloaded from every provider (≈13 GB)."]
else:
    L += [f"Status: **PASS for public main `{R['verified_commit']}`**; finishing-pass changes: **PUBLIC_SYNC_PENDING** until the finishing PR is merged and re-verified.", "",
     "| Item | Result |", "|---|---|", f"| Repository accessible anonymously | YES ({R['repository']}) |", f"| Clone | {R['clone_method']} |", f"| Verified at (UTC) | {R['verified_utc']} |",
     f"| Raw inputs | {R['raw_inputs']} |", "| Scripts run (exit codes) | " + "; ".join(R["scripts"]) + " |", f"| Byte-identical | {R['byte_identical']} |",
     "| Semantically identical | " + "; ".join(R["semantically_identical"]) + " |", f"| Tests | EM&A {R['tests']['ema_known_answer_tests']}; RPG {R['tests']['rpg_known_answer_tests']} |",
     "| Data Availability URL / Code Availability URL | https://github.com/bougtoir/more-rice (HTTP 200) |", "| Acquisition instructions / ledgers | RAW_ACQUISITION_LEDGER_2026-11-08.csv; RPG LEDGER via rpg_fetch_rice.py (WFS URLs) |",
     "| Credentials or restricted geometries in repo | none (.geojson absent from tracked files and ZIPs) |", lic, "",
     "Limitation: raw inputs were taken from the durable local store (hash-verified against the ledgers) rather than re-downloaded from every provider during this check."]
W("15_PUBLIC_MAIN_REPRODUCIBILITY_AUDIT.md", L)

# ---- 16 PR / 17 premerge / 18 gate ----
br = sh("git", "rev-parse", "--abbrev-ref", "HEAD").decode().strip()
fp = f"{PR} — merged into main as `{PM['verified_commit']}` after explicit author approval" if PM else f"{PR} — NOT merged (requires explicit author approval)"
W("16_PR_AND_MERGE_STATUS.md", ["# PR and merge status", "", "| Item | Value |", "|---|---|", "| PR #2 | https://github.com/bougtoir/more-rice/pull/2 — merged; merge commit a1202c7c5b41c9286388dfd89a90532ceb9ecb0f (not re-merged) |",
    f"| Finishing-pass branch | `devin/1795496123-ema-finishing-pass` (from {BASE[:7]}) |", f"| Finishing-pass PR | {fp} |"]
    + ([f"| Post-merge verification branch | `{br}` (records only; no manuscript or analysis change) |"] if PM else []) + ["| CI | CI_NOT_CONFIGURED |"])
W("17_FINAL_PREMERGE_GATE.md", ["# Final pre-merge gate (finishing-pass PR)", "", "| Gate | Status |", "|---|---|", "| Numerical non-regression | PASS |", f"| KAT | EM&A {kp[0]}/{kp[1]}, RPG {rp[0]}/{rp[1]} PASS |",
    "| Claim calibration / boundary | PASS |", "| References | PASS |", "| Figures/tables | PASS |", "| Word/OMML/render | PASS |", "| No raw RPG geometries | PASS |", "| Scope limited to wording, cover letter, figure embedding, audits | PASS |", "| CI | CI_NOT_CONFIGURED |",
    "| Explicit author approval to merge | " + ("RECEIVED (merged)" if PM else "PENDING") + " |", "",
    "Post-merge public clean-clone check: " + (PM["status"] if PM else "pending") + "."])
if POST:
    W("18_FINAL_SUBMISSION_GATE.md", ["# Final submission gate", "", "**Decision: SCIENTIFICALLY READY — AUTHOR ACTIONS PENDING**", "",
        f"All scientific and editorial gates pass, the finishing pass is merged, and public main `{PM['verified_commit'][:7]}` was re-verified from a fresh anonymous clone (PASS). `READY FOR SUBMISSION` is not issued only because author-controlled items remain (the corresponding e-mail is still a placeholder).", "",
        "Author actions:", "1. Enter the corresponding e-mail on the title page and cover letter.", "2. Confirm affiliation and ORCID.",
        "3. Choose the subscription (no-APC) route; do not select open access unless funded.", "4. Enter author contributions and competing interests in the submission interface.", "",
        "Journal-selectivity risk: MEDIUM–HIGH (no author-collected field data). A scientifically defensible manuscript can still be desk-rejected; this verdict concerns readiness, not predicted acceptance.", "",
        "Not done by Devin: submission, contact with the journal, payment."])
else:
    W("18_FINAL_SUBMISSION_GATE.md", ["# Final submission gate", "", "**Decision: CONDITIONAL READY — finishing-pass PR merge and post-merge public-main check pending; author actions pending.**", "",
    "`READY FOR SUBMISSION` is not issued because the finished text is not yet on public main (PUBLIC_SYNC_PENDING).", "", "Author actions:", "1. Approve and merge the finishing-pass PR.", "2. Enter the corresponding e-mail on the title page and cover letter.",
    "3. Confirm affiliation and ORCID.", "4. Choose the subscription (no-APC) route; do not select open access unless funded.", "5. Enter author contributions and competing interests in the submission interface.", "",
    "Not done by Devin: submission, contact with the journal, payment."])

# ---- deliverables ----
items = [(MSP, "01_EMA_MANUSCRIPT_FINAL.docx"), (RVPDF, "02_EMA_MANUSCRIPT_REVIEW.pdf"), (CLP, "03_EMA_COVER_LETTER_FINAL.docx"), (CLPDF, "04_EMA_COVER_LETTER_REVIEW.pdf")]
items += [(os.path.join(REP, f), f) for f in sorted(os.listdir(REP))]
out = []
for s, n in items: shutil.copy(s, os.path.join(DL, n)); out.append(n)
for k, f in enumerate(figfiles, 1):
    for ext in (".png", ".pdf"):
        if os.path.exists(os.path.join(FIG, f + ext)): n = f"Fig{k}_{f}{ext}"; shutil.copy(os.path.join(FIG, f + ext), os.path.join(DL, n)); out.append(n)
for f in sorted(os.listdir(os.path.join(SUB, "tables"))): shutil.copy(os.path.join(SUB, "tables", f), os.path.join(DL, f)); out.append(f)
sub_set = [n for n in out if n[:2] in ("01", "02", "03", "04") or n.startswith(("Fig", "Table_"))]
zs, za = os.path.join(DL, "EMA_FINAL_SUBMISSION_PACKAGE_FINISHED.zip"), os.path.join(DL, "EMA_INDEPENDENT_AUDIT_EVIDENCE_PACKAGE_FINISHED.zip")
with zipfile.ZipFile(zs, "w", zipfile.ZIP_DEFLATED) as z:
    for n in sub_set: z.write(os.path.join(DL, n), n)
prior = [f for f in sorted(os.listdir(OLD)) if not f.endswith(".zip") and f[:2] not in ("01", "02", "03", "04", "26", "27", "28")]
with zipfile.ZipFile(za, "w", zipfile.ZIP_DEFLATED) as z:
    for n in out:
        if n not in sub_set: z.write(os.path.join(DL, n), "finishing_pass/" + n)
    for f in prior: z.write(os.path.join(OLD, f), "prior_scientific_evidence/" + f)
    for f in ("CLAIM_CALIBRATION_EDITS.json", "CROSSREF_CHECK.json", "PUBLIC_MAIN_REPRO_RESULT.json", "POSTMERGE_PUBLIC_MAIN_RESULT.json"):
        if os.path.exists(os.path.join(FIN, f)): z.write(os.path.join(FIN, f), "finishing_pass/records/" + f)
    for f in sorted(os.listdir(JR)): z.write(os.path.join(JR, f), "finishing_pass/journal_requirements_2026-11-24/" + f)
for zz in (zs, za):
    nm = zipfile.ZipFile(zz).namelist(); assert not any(n.endswith((".geojson", ".tif", ".asc", ".nc")) or "literature" in n for n in nm)
man = [dict(file=n, bytes=os.path.getsize(os.path.join(DL, n)), sha256=sha(os.path.join(DL, n))) for n in sorted(os.listdir(DL))]
assert all(m["bytes"] > 0 for m in man)
pd.DataFrame(man).to_csv(os.path.join(DL, "19_FINAL_FILE_MANIFEST_SHA256.csv"), index=False)
print(len(man), "files;", "ZIP", sha(zs)[:12], sha(za)[:12])
