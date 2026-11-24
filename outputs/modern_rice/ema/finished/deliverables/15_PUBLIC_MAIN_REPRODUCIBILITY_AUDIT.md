# Public main reproducibility audit

Status: **PASS for public main `3a46db97836d8a2fca25f79b65ebb92c92df5340`** (Merge pull request #3 from bougtoir/devin/1795496123-ema-finishing-pass), i.e. after the finishing pass was merged.

| Item | Result |
|---|---|
| Repository accessible anonymously | YES (https://github.com/bougtoir/more-rice) |
| Clone | fresh anonymous HTTPS clone (GIT_TERMINAL_PROMPT=0) |
| Verified at (UTC) | 2026-11-24T05:14:05Z |
| Raw inputs | durable local store linked into the clone; 62 ledgered files SHA-256-verified, 0 mismatched/missing |
| Scripts run (exit codes) | ag_grid_gates=0; ag_germany_decomposition=0; ema_threshold_sweep=0; ema_figures=0; ema_reports=0; rpg_validation=0; rpg_reports=0; ema_known_answer_tests=0; rpg_known_answer_tests=0; build_ema_manuscript=0 |
| Canonical CSV/JSON/PNG outputs changed by re-run | 0 |
| DOCX/PDF re-run vs committed | CANDIDATE_AREA_OMISSION_TRADEOFF.pdf: extracted text identical; CLASSIFICATION_DISAGREEMENT_MAP.pdf: extracted text identical; GERMANY_CONTROLLED_CONTRAST.pdf: extracted text identical; RICE_AREA_OMISSION_GEOGRAPHY.pdf: extracted text identical; THRESHOLD_OMISSION_CURVE.pdf: extracted text identical; 01_EMA_MANUSCRIPT_FINAL.docx: document.xml + media identical; 02_EMA_MANUSCRIPT_REVIEW.pdf: extracted text identical; 03_EMA_COVER_LETTER_FINAL.docx: document.xml + media identical; EMA_MANUSCRIPT_REVIEW_COPY.docx: document.xml + media identical; 01_EMA_MANUSCRIPT_FINAL.pdf: extracted text identical (PDF/DOCX bytes differ only in render metadata) |
| Prose audit reports regenerated with different text | EMA_JOURNAL_REQUIREMENTS_FINAL.md, WORD_RENDER_AND_EQUATION_AUDIT.md |
| Tests | EM&A 24/24; RPG 26/26 |
| Tracked .geojson files | 0 |
| Data / Code Availability URL | https://github.com/bougtoir/more-rice (HTTP 200) |
| Acquisition ledgers | RAW_ACQUISITION_LEDGER_2026-11-08.csv; rpg/LEDGER.txt (WFS URLs via rpg_fetch_rice.py) |
| Licences | WorldClim CC BY 4.0; MapSPAM CC BY 4.0; GMIA (FAO, not redistributed); RPG Licence Ouverte 2.0 (geometries not redistributed) |

The two prose reports listed above are legacy pre-finishing audit files whose committed copies carried stale descriptive values (abstract word count 249 instead of 250; archive directory listing). They contain no manuscript or analysis numbers; the regenerated copies are committed by the post-merge verification PR.

Earlier pre-merge check of `a1202c7c5b41c9286388dfd89a90532ceb9ecb0f`: PASS (see PUBLIC_MAIN_REPRO_RESULT.json).

Limitation: raw inputs were taken from the durable local store (SHA-256-verified against the acquisition ledgers) rather than re-downloaded from every provider (≈13 GB).
