# Final scientific non-regression audit

Baseline `a1202c7c5b41c9286388dfd89a90532ceb9ecb0f` (public main) vs finishing-pass working tree.

| Check | Result |
|---|---|
| Tracked canonical CSV/JSON/PNG outputs (n = 147) changed | 0 PASS |
| Analysis scripts changed | none (only build_ema_manuscript.py, the text builder, changed) |
| Manuscript number multiset (all digits in body, tables, captions, references) | identical: True |
| Equations | 2 OMML equations, text-identical to baseline |
| Figures | PNG files byte-identical (part of canonical set); now also embedded in 01 |
| Tables | 4 tables, cell text identical |
| EM&A known-answer tests (executed now) | 24/24 PASS |
| RPG known-answer tests (executed now) | 26/26 PASS |
| Obsolete 92.2% or 0.87% present | False |

Verification anchors found in the built manuscript: 589 GDD10 ✓, 69.7 Mha ✓, 92.1% ✓, 16.0% ✓, 96.6% ✓, 3.2% ✓, 2.4 percentage points ✓, 54.9% ✓, 1.37% ✓, 3.22% ✓, 0.98 ✓, 0.60 ✓

Changed tracked files: `modern_rice/manuscript_ema/manuscript_template.md`, `modern_rice/scripts/build_ema_manuscript.py`, `outputs/modern_rice/ema/KNOWN_ANSWER_TESTS_FINAL.csv`, `outputs/modern_rice/ema/KNOWN_ANSWER_TESTS_FINAL.md`, `outputs/modern_rice/ema/submission/01_EMA_MANUSCRIPT_FINAL.docx`, `outputs/modern_rice/ema/submission/02_EMA_MANUSCRIPT_REVIEW.pdf`, `outputs/modern_rice/ema/submission/03_EMA_COVER_LETTER_FINAL.docx`, `outputs/modern_rice/ema/submission/EMA_MANUSCRIPT_REVIEW_COPY.docx`, `outputs/modern_rice/ema/submission/render_check/01_EMA_MANUSCRIPT_FINAL.pdf`

New files: `modern_rice/scripts/build_lup_manuscript.py`, `modern_rice/scripts/ema_finish_edits.py`, `modern_rice/scripts/ema_finish_reports.py`, `outputs/modern_rice/ema/finished/03_EMA_COVER_LETTER_FINAL.pdf`, `outputs/modern_rice/ema/finished/CLAIM_CALIBRATION_EDITS.json`, `outputs/modern_rice/ema/finished/CROSSREF_CHECK.json`, `outputs/modern_rice/ema/finished/PUBLIC_MAIN_REPRO_RESULT.json`, `outputs/modern_rice/ema/finished/render/03_EMA_COVER_LETTER_FINAL.pdf`, `outputs/modern_rice/ema/finished/render/cl-1.png`, `outputs/modern_rice/ema/finished/render/cl-2.png`, `outputs/modern_rice/ema/finished/render/m-01.png`, `outputs/modern_rice/ema/finished/render/m-02.png`, `outputs/modern_rice/ema/finished/render/m-03.png`, `outputs/modern_rice/ema/finished/render/m-04.png`, `outputs/modern_rice/ema/finished/render/m-05.png`, `outputs/modern_rice/ema/finished/render/m-06.png`, `outputs/modern_rice/ema/finished/render/m-07.png`, `outputs/modern_rice/ema/finished/render/m-08.png`, `outputs/modern_rice/ema/finished/render/m-09.png`, `outputs/modern_rice/ema/finished/render/m-10.png`, `outputs/modern_rice/ema/finished/render/m-11.png`, `outputs/modern_rice/ema/finished/render/m-12.png`, `outputs/modern_rice/ema/finished/render/m-13.png`, `outputs/modern_rice/ema/finished/render/m-14.png`, `outputs/modern_rice/ema/finished/render/m-15.png`, `outputs/modern_rice/ema/finished/render/m-16.png`, `outputs/modern_rice/ema/finished/render/m-17.png`, `outputs/modern_rice/ema/finished/render/m-18.png`, `outputs/modern_rice/ema/finished/render/m-19.png`, `outputs/modern_rice/ema/finished/render/m-20.png`, `outputs/modern_rice/ema/finished/render/m-21.png`, `outputs/modern_rice/ema/finished/render/m-22.png`, `outputs/modern_rice/ema/finished/render/m-23.png`, `outputs/modern_rice/ema/finished/render/m-24.png`, `outputs/modern_rice/ema/finished/render/m-25.png`, `outputs/modern_rice/ema/finished/render/m-26.png`, `outputs/modern_rice/ema/finished/render/s1.png`, `outputs/modern_rice/ema/finished/render/s2.png`, `outputs/modern_rice/ema/finished/render/scl.png`, `outputs/modern_rice/ema/finished/reports/05_SCIENTIFIC_CLAIM_CALIBRATION_AUDIT.md`, `outputs/modern_rice/ema/finished/reports/06_CONTINGENCY_APPLICATION_AND_CLAIM_BOUNDARY.md`, `outputs/modern_rice/ema/finished/reports/07_EMA_JOURNAL_REQUIREMENTS_RECHECK.md`
