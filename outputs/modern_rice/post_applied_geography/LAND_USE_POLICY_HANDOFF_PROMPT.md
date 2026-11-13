# Handoff prompt: more-rice → Land Use Policy (new thread)

Paste this into a new Devin session. Communicate with the user in Japanese. Attach every deliverable individually in addition to any ZIP.

## Objective
Retarget the rice cultivation-system transfer manuscript (desk-rejected by Applied Geography, Ms. No. JAPG-D-26-05309, "falls within the aim and scope … declined due to lack of sufficient novelty") to **Land Use Policy** (Elsevier; regular paper; subscription route, no publication fee). Target journal approved by the user on 2026-11-13. Produce a submission-ready package and a submission-gate verdict. Do not submit, contact editors, pay an APC, or merge without explicit authorization.

## Repository and state
- Repo `bougtoir/more-rice`; work on branch `devin/1794546202-next-journal-retarget` (or a fork branch from it). AG version: merge `4cd8d5e`, content head `5c9cb51`.
- Post-AG files: `outputs/modern_rice/post_applied_geography/` (verbatim letter, REJECTION_RESPONSE_MATRIX.csv, REPRODUCTION_CHECK_2026-11-13.md, NEXT_JOURNAL_CANDIDATE_COMPARISON.md).
- Official LUP pages archived: `data/journal_requirements/land_use_policy/` (aims & scope, guide for authors, open-access options). Re-read the guide before formatting; ScienceDirect needs the browser (Chrome CDP at localhost:29229), curl fails.
- Raw data: private release `bougtoir/wip` tag `more-rice-raw-2026-11-08` → extract into `modern_rice/data/raw/` (gitignored; never public). Ledger `modern_rice/data/RAW_ACQUISITION_LEDGER_2026-11-08.csv`. NASA POWER/EStreams/Natural Earth come as archives — extract; create aliases `raw/estream_indices -> hydrology/estreams_indices`, `raw/estreams_gauges -> hydrology/estreams_gauges`. With this, all 11 canonical `modern_rice/scripts/ag_*.py` reruns were byte-identical to main on 2026-11-13.
- Python deps: python-docx, python-pptx, rasterio, geopandas, shapely, pyproj, openpyxl, playwright; LibreOffice for PDF.
- Builder to copy (do not edit in place): `modern_rice/scripts/build_ag_manuscript.py` + `modern_rice/manuscript_ag/manuscript_template.md`. New output dir: `outputs/modern_rice/land_use_policy/`. Leave AgSys/AG outputs untouched.

## LUP requirements (from archived guide; verify again)
- Regular paper; double-anonymized: separate title page (author, affiliation, declarations) + anonymized manuscript (no self-identifying text, file metadata scrubbed, code/data links anonymized or "withheld for review").
- Abstract ≤250 words; 1–7 keywords; 3–5 highlights each ≤85 characters incl. spaces (separate file).
- Single-column editable Word; figures as separate files; native Word equations and tables; generative-AI declaration; CRediT; data availability; competing interests; funding.
- Reference style applied at proof; keep APA 7 author–year consistently.

## Reframing (no new numbers)
AG rejected on perceived novelty, not method. For LUP: pose a land-use-policy question — how should crop-transfer / crop-diversification proposals for European incumbent arable land be screened? Lead with: (1) a transferred thermal threshold is a fragile screen (Germany 3.2% vs 96.6% on one surface depending on reference construction; resolution ≤2.4 pp); (2) irrigation infrastructure binds (Europe thermal pass 92.2% → thermal+AEI≥10% 16.0%; Jun–Sep rainfed deficit 76.0%); (3) river discharge ≠ allocable water (Lower Danube 250,000 ha → 241.1 m³/s net, 321.5 gross); (4) food-supply risk gains robust only for Kazakhstan (58% of 24 configurations), Romania 17%. Add an "Implications for land-use screening" section (screening sequence, what evidence each gate needs, what remains a later feasibility question) without claiming policy effects, optimization, observed land-use change or implementation feasibility. State prior precedents upfront and claim only the non-duplicated part (CLOSEST_PRIOR_STUDIES_MATRIX_FINAL.csv).

## Scientific freeze
Do not change canonical results without new evidence; never restore withdrawn Q99 21.9%/29.2% ratios or the Serbia potato-dominance claim; 589 GDD10 is a transferred reference (Hokkaido rice-area P05), not universal/physiological; AEI ≠ rice-ready land / water rights / delivery capacity. All numeric prose generated from canonical outputs (no hard-coding). No fabricated references (37 entries, Crossref-checked).

## Author metadata
Sole author Onishi Tatsuki, Data Science and AI Innovation Research Promotion Center, Shiga University, Japan. Email, ORCID, suggested reviewers: left for the user — do not guess.

## QC and delivery
Hostile editor/reviewer review (LUP lens: policy relevance, novelty) before mechanical QC; rerun independent audit, numeric consistency, reference/citation and figure/table-citation checks; render and inspect every PDF page; check anonymization of the blinded files. Public-repo reproducibility check (public code + data named in the paper; public repo names must not contain a journal name). Deliver: anonymized manuscript DOCX/PDF, title page, highlights, cover letter, editable figures (PPTX + separate image files), editable tables, declarations, QC reports, draft lock, final handoff, numbered individual files + ZIP + SHA-256 manifest; focused commits; PR on request only.
