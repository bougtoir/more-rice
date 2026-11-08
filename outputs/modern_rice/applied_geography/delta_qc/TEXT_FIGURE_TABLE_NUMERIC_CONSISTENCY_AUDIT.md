# Text–figure–table numeric consistency audit
- All manuscript numbers are filled from `MANUSCRIPT_NUMBERS.json`, generated from canonical outputs by `build_ag_manuscript.py`; the build fails on unfilled placeholders.
- Independent checks (not script agreement): domain shares (`spatial_indep.txt`), Hokkaido P05, Danube arithmetic, risk baseline reimplementation — see gate audits.
- DOCX XML (final manuscript): 0 `wp:anchor`, figures supplied as separate files; 3 native `w:tbl`; 1 OMML equation (Q = A·D/T as a fraction); headings Times New Roman black; body Times New Roman 12 pt.
- Inline review copy: 5 `wp:inline`, 0 `wp:anchor`; order of first appearance Figure 1, Table 1, Figure 2, Table 2, Figure 3, Figure 4, Figure 5, Table 3, each placed after its first-citing paragraph; rendered PDF pages inspected (no cropping).
- Literal markdown asterisks: fixed a bug where `T*` pairs were consumed as italic markers (e.g. "from 92.2% at T to 54.9%"); `T*` is now italic T with superscript asterisk.
- Withdrawn claims searched across manuscript, inline copy, cover letter, highlights, metadata, tables and README: no remaining "~24 m³/s", "~2% of Q99", "17.6%/94.2% of European arable land" (now only as explicitly labelled rectangle sensitivity), "90% of mean", or Serbia potato dominance as a finding. README does not contain these claims (README describes the repository's other project; unchanged).
- Highlights, abstract and cover letter use the same values: 92.2%, 16.0%, 241 m³/s, 58%/17%.
