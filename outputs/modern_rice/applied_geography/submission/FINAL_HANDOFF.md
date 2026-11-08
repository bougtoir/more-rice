# FINAL HANDOFF: Applied Geography retarget

## Verdict: **HOLD**
The science, reproducibility and formatting gates pass. Submission is held for the author action items below, plus one fact to verify. Nothing has been submitted, sent, paid or selected.

## QC gates
| Gate | Result | Note |
|---|---|---|
| G1 Scientific validity | PASS after corrections | Three material errors in the AgSys version were fixed: the GDD window, the analog-country risk, and the Lower Danube 10× error (NUMERICAL audit E1–E3) |
| G2 Novelty / prior art | CONDITIONAL | The contribution is modest and methodological-geographic (bound source/scale dependence, gate cascade). There is a risk of a novelty-based desk rejection |
| G3 Reproducibility | PASS (with note) | `build_ag_manuscript.py` and all `ag_*.py` scripts regenerate every number and figure. Raw data are archived privately: bougtoir/wip release `more-rice-raw-2026-11-08`, plus a ledger with SHA-256 |
| G4 Text–figure–table | PASS | Numbering is asserted in order; 0 newlines in DOCX runs |
| G5 References | PASS (with note) | All 31 references are cited in the text and all citations are in the list; checked against Crossref/DataCite. Two AgSys reference errors were fixed. CT-UPT (2014) is grey literature |
| G6 Hostile review | PASS | 9 objections answered or listed as limitations. AEI cut-off sensitivity was added (5/10/20%) |
| G7 Word/PDF rendering | PASS | 5,091 words (limit 4,500–8,000); abstract 236 words (≤250); 7 keywords; highlights ≤81 characters; PDF of 20 pages inspected visually |
| G8 Cover letter | PASS | States the previous AgSys consideration and the corrections; reviewers are a placeholder |

## Author action required before submission
1. Re-verify the Iron Gates low-flow values (mean 5,420; Q90/Q95/Q99 1,460/1,320/1,100 m³/s) against the CT-UPT (2014) original.
2. Enter the corresponding e-mail (title page) and suggested reviewers (cover letter).
3. In Editorial Manager: choose Subscription. Check the login-only checklist, which was not verified.
4. Check the Guglielmo et al. (2025) author names against the article PDF.
5. Approve the new title, or revert to the AgSys title.

## Files
- Anonymized manuscript: `APPLIED_GEOGRAPHY_MANUSCRIPT_FINAL.docx/.pdf`. Figures are supplied separately; captions appear inline at their placement points.
- `APPLIED_GEOGRAPHY_MANUSCRIPT_INLINE_REVIEW_COPY.docx/.pdf`: figures embedded, for reading.
- `APPLIED_GEOGRAPHY_TITLE_PAGE.docx`, `APPLIED_GEOGRAPHY_highlights.docx`, `APPLIED_GEOGRAPHY_TABLES_EDITABLE.docx`, `APPLIED_GEOGRAPHY_FIGURES_EDITABLE.pptx`, `figures/Figure_1–5.{png,pdf}`
- `APPLIED_GEOGRAPHY_COVER_LETTER.docx`, `APPLIED_GEOGRAPHY_ABSTRACT_AND_METADATA.txt`
- Audits: REQUIREMENTS, PRIOR_WORK_MATRIX, GAP_REGISTER, NOVELTY_AND_FIT, NUMERICAL_AND_SPATIAL, REFERENCES, FIGURE_TABLE_ORDER, HOSTILE_REVIEW, REJECTION_RESPONSE_MATRIX, JOURNAL_RETARGET_DECISION

## Rebuild
```
python3 modern_rice/scripts/ag_point_window_sensitivity.py
python3 modern_rice/scripts/ag_grid_gates.py        # ~10 min, needs raw/ (WorldClim, SPAM, GMIA, NE)
python3 modern_rice/scripts/ag_danube_demand.py
python3 modern_rice/scripts/ag_risk_portfolio_v2.py
python3 modern_rice/scripts/ag_figures.py
python3 modern_rice/scripts/build_ag_manuscript.py  # needs LibreOffice for PDF
```
Raw inputs can be recovered with `gh release download more-rice-raw-2026-11-08 -R bougtoir/wip` and then extracted into `modern_rice/data/raw/`. They can also be re-downloaded from the ledger URLs.

## Not done or out of scope
- Future climate (CMIP6)
- Farm-level water allocation
- Observed costs outside Italy
- Repository README mismatch: the README describes a medieval-history project and should be updated separately
- The canonical `MANUSCRIPT_FINAL_ORDER_CORRECTED.docx` is unchanged
