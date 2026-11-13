# Word render and equation audit

- Fonts declared in main DOCX runs/styles: ['Courier', 'Times New Roman']; body 12 pt Times New Roman black; captions and table text 10/9 pt.
- Character-spacing (`w:spacing w:val`) elements: 0.
- Native OMML equations: 2 in main, 2 in review copy (equations 1–2).
- Inline images: main 0, review copy 5 (5 expected).
- Line numbering: continuous; page numbers in footer: yes.
- Review PDF: 22 pages (LibreOffice render). Replacement glyphs (U+FFFD) in extracted text: 0. Stray Markdown asterisks other than T*: 0.
- Embedded fonts (pdffonts):
```
name                                 type              encoding         emb sub uni object ID
------------------------------------ ----------------- ---------------- --- --- --- ---------
BAAAAA+LiberationSerif-Bold          TrueType          WinAnsi          yes yes yes     87  0
CAAAAA+LiberationSerif               TrueType          WinAnsi          yes yes yes    102  0
DAAAAA+DejaVuSerif                   TrueType          WinAnsi          yes yes yes    112  0
EAAAAA+LiberationSerif-BoldItalic    TrueType          WinAnsi          yes yes yes     92  0
FAAAAA+LiberationSerif-Italic        TrueType          WinAnsi          yes yes yes     97  0
GAAAAA+OpenSymbol                    TrueType          WinAnsi          yes yes yes    107  0
```
- All 22 pages were rasterised and inspected (contact sheets in `submission/render_check/png/`): no clipping, captions below figures and above tables, equations render with fraction and summation, references hanging-indented and alphabetical. Word itself was not available; rendering was checked with LibreOffice 7.
