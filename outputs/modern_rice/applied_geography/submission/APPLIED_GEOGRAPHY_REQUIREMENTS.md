# Applied Geography: official requirements (verified)

Access date: 2026-11-08 (UTC 07:21–07:22). Pages were captured with the session's Chrome browser over CDP because plain `curl` got HTTP 403. Archived copies (HTML and text) are in `data/journal_requirements/applied_geography/`.

| Source | URL | Archived file |
|---|---|---|
| Guide for authors | https://www.sciencedirect.com/journal/applied-geography/publish/guide-for-authors | guide_for_authors.{html,txt} |
| Aims and scope | https://www.sciencedirect.com/journal/applied-geography/about/aims-and-scope | aims_and_scope.{html,txt} |
| Open access options | https://www.sciencedirect.com/journal/applied-geography/publish/open-access-options | open_access_options.{html,txt} |
| Journal home | https://www.sciencedirect.com/journal/applied-geography | journal_home.{html,txt} |

Line numbers below refer to `guide_for_authors.txt`.

| Requirement | Official text (paraphrased only where noted) | How this package complies |
|---|---|---|
| Scope | Geographic approaches (human, physical, nature–society, GIScience) applied to human problems that have a spatial dimension, including the assessment, management and allocation of physical and human resources (aims_and_scope). | The study is reframed as a spatially explicit, multi-scale gate analysis of where rice transfer is worth assessing in incumbent arable land. |
| Article type | Research article, 4,500–8,000 words, counting captions, tables and references (l.98). | Research article. Word count is checked by the build script (see `NUMERICAL_AND_SPATIAL_CONSISTENCY_AUDIT.md`). |
| Review model | Double-anonymized. The title page (authors, affiliations, corresponding email, acknowledgments, competing interests) and the anonymized manuscript are separate files (l.392–404). | `APPLIED_GEOGRAPHY_TITLE_PAGE.docx` plus an anonymized `APPLIED_GEOGRAPHY_MANUSCRIPT_FINAL.docx`. The repository URL is masked in the anonymized file. |
| Abstract | No more than 250 words, no references (l.410–426). | Checked by the build. |
| Keywords | 1–7 (l.430). | 7. |
| Highlights | 3–5 bullets, each at most 85 characters including spaces, as a separate editable file with "highlights" in the file name (l.436–442). | `APPLIED_GEOGRAPHY_highlights.docx`. Lengths are checked by the build. |
| Graphical abstract | Encouraged, not required. Separate file; TIFF, EPS, PDF or MS Office (l.446–460). | Optional. The existing AgSys graphical abstract is not reused because its message (900 GDD as a fixed gate) is superseded. Decision: none submitted (see FINAL_HANDOFF). |
| Tables | Editable. Placed next to the relevant text or at the end, cited and numbered in order (l.480–494). | Native Word tables, placed inline right after first citation. |
| Figures | Supplied as separate files named logically (Figure_1, …), all cited, numbered in order of appearance (l.498–). | Separate `Figure_N.png/.pdf` files. Inline copies in the review manuscript, per the author's own rule. |
| Sections | Numbered 1, 1.1, …; abstract not numbered (l.715–725). | Followed. |
| References | APA 7th edition, alphabetical then chronological, with a/b suffixes; data references tagged [dataset] (l.802–). | Author–year APA style with [dataset] tags. |
| Generative AI | A declaration is required, under a section titled "Declaration of generative AI and AI-assisted technologies in the manuscript preparation process" (l.230–259). | Section included. The earlier AgSys statement ("No generative AI wrote the scientific content") is not reused. The author must confirm the final wording. |
| Competing interests | Use the declarations tool (l.184–214). | The author completes it at submission. A statement is also on the title page. |
| CRediT | Required (l.731). | Single-author CRediT statement on the title page. |
| Research data | Option B (deposit encouraged, otherwise a statement) plus a data statement (l.664–680). | Data statement: code and derived outputs in a public repository; licence-restricted raw data are re-downloadable from cited sources. |
| File format | .docx, single column; a PDF is not accepted as the source file (l.360–362). | .docx source. The PDF is for QA only. |
| Open access / APC | Two routes: Open access (APC payable) and Subscription ("No open access publication fee") (open_access_options). The APC applies only to OA (l.899). | **Subscription route available, no mandatory APC.** No irrevocable publishing option has been selected. |

Not verified: the exact APC amount (not needed for the subscription route) and the submission-system file-type checklist, which is only visible after login.
