# Final scientific non-regression audit

Baseline `a1202c7c5b41c9286388dfd89a90532ceb9ecb0f` (public main) vs finishing-pass working tree.

| Check | Result |
|---|---|
| Tracked canonical CSV/JSON/PNG outputs (n = 147) changed | 0 PASS |
| Analysis scripts changed | ['modern_rice/scripts/ema_finish_edits.py', 'modern_rice/scripts/ema_finish_reports.py'] (only build_ema_manuscript.py, the text builder, changed) |
| Manuscript number multiset (all digits in body, tables, captions, references) | identical: True |
| Equations | 2 OMML equations, text-identical to baseline |
| Figures | PNG files byte-identical (part of canonical set); now also embedded in 01 |
| Tables | 4 tables, cell text identical |
| EM&A known-answer tests (executed now) | 24/24 PASS |
| RPG known-answer tests (executed now) | 26/26 PASS |
| Obsolete 92.2% or 0.87% present | False |

Verification anchors found in the built manuscript: 589 GDD10 ✓, 69.7 Mha ✓, 92.1% ✓, 16.0% ✓, 96.6% ✓, 3.2% ✓, 2.4 percentage points ✓, 54.9% ✓, 1.37% ✓, 3.22% ✓, 0.98 ✓, 0.60 ✓

Changed tracked files: `modern_rice/manuscript_ema/manuscript_template.md`, `modern_rice/scripts/build_ema_manuscript.py`, `modern_rice/scripts/ema_finish_edits.py`, `modern_rice/scripts/ema_finish_reports.py`, `outputs/modern_rice/ema/KNOWN_ANSWER_TESTS_FINAL.csv`, `outputs/modern_rice/ema/KNOWN_ANSWER_TESTS_FINAL.md`, `outputs/modern_rice/ema/finished/03_EMA_COVER_LETTER_FINAL.pdf`, `outputs/modern_rice/ema/finished/CLAIM_CALIBRATION_EDITS.json`, `outputs/modern_rice/ema/finished/CROSSREF_CHECK.json`, `outputs/modern_rice/ema/finished/PUBLIC_MAIN_REPRO_RESULT.json`, `outputs/modern_rice/ema/finished/reports/05_SCIENTIFIC_CLAIM_CALIBRATION_AUDIT.md`, `outputs/modern_rice/ema/finished/reports/06_CONTINGENCY_APPLICATION_AND_CLAIM_BOUNDARY.md`, `outputs/modern_rice/ema/finished/reports/07_EMA_JOURNAL_REQUIREMENTS_RECHECK.md`, `outputs/modern_rice/ema/finished/reports/08_FINAL_SCIENTIFIC_NONREGRESSION_AUDIT.md`, `outputs/modern_rice/ema/finished/reports/09_FINAL_SEMANTIC_CODE_AUDIT.md`, `outputs/modern_rice/ema/finished/reports/10_FINAL_CLAIM_BOUNDARY_AUDIT.md`, `outputs/modern_rice/ema/finished/reports/11_FINAL_REFERENCE_AND_CLAIM_AUDIT.md`, `outputs/modern_rice/ema/finished/reports/12_FINAL_TEXT_FIGURE_TABLE_CONSISTENCY_AUDIT.md`, `outputs/modern_rice/ema/finished/reports/13_FINAL_WORD_RENDER_AND_OMML_AUDIT.md`, `outputs/modern_rice/ema/finished/reports/14_FINAL_HOSTILE_EMA_EDITOR_REVIEW.md`, `outputs/modern_rice/ema/finished/reports/15_PUBLIC_MAIN_REPRODUCIBILITY_AUDIT.md`, `outputs/modern_rice/ema/finished/reports/16_PR_AND_MERGE_STATUS.md`, `outputs/modern_rice/ema/finished/reports/17_FINAL_PREMERGE_GATE.md`, `outputs/modern_rice/ema/finished/reports/18_FINAL_SUBMISSION_GATE.md`, `outputs/modern_rice/ema/reports/EMA_JOURNAL_REQUIREMENTS_FINAL.md`, `outputs/modern_rice/ema/reports/WORD_RENDER_AND_EQUATION_AUDIT.md`, `outputs/modern_rice/ema/submission/01_EMA_MANUSCRIPT_FINAL.docx`, `outputs/modern_rice/ema/submission/02_EMA_MANUSCRIPT_REVIEW.pdf`, `outputs/modern_rice/ema/submission/03_EMA_COVER_LETTER_FINAL.docx`, `outputs/modern_rice/ema/submission/EMA_MANUSCRIPT_REVIEW_COPY.docx`, `outputs/modern_rice/ema/submission/render_check/01_EMA_MANUSCRIPT_FINAL.pdf`

New files: `modern_rice/scripts/ema_finish_edits.py`, `modern_rice/scripts/ema_finish_reports.py`, `modern_rice/scripts/ema_postmerge_verify.py`
