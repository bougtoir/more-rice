# Public main reproducibility audit

Status: **PASS for public main `a1202c7c5b41c9286388dfd89a90532ceb9ecb0f`**; finishing-pass changes: **PUBLIC_SYNC_PENDING** until the finishing PR is merged and re-verified.

| Item | Result |
|---|---|
| Repository accessible anonymously | YES (https://github.com/bougtoir/more-rice) |
| Clone | git clone https://github.com/bougtoir/more-rice.git (anonymous HTTPS, no credentials) |
| Verified at (UTC) | 2026-11-24T05:02:38Z |
| Raw inputs | modern_rice/data/raw symlinked to the durable local raw store whose files match RAW_ACQUISITION_LEDGER_2026-11-08.csv and modern_rice/data/raw/rpg/LEDGER.txt (public sources; RPG geometries not redistributed) |
| Scripts run (exit codes) | ag_grid_gates exit=0; ag_germany_decomposition exit=0; ema_threshold_sweep exit=0; ema_figures exit=0; ema_reports exit=0; rpg_validation exit=0; rpg_reports exit=0; ema_known_answer_tests exit=0; rpg_known_answer_tests exit=0; build_ema_manuscript exit=0 |
| Byte-identical | all tracked CSV, JSON and PNG outputs under outputs/modern_rice (git status clean for these) |
| Semantically identical | 5 figure PDFs under outputs/modern_rice/ema/figures (identical after removing CreationDate/ModDate/ID metadata); 01_EMA_MANUSCRIPT_FINAL.docx, EMA_MANUSCRIPT_REVIEW_COPY.docx, 03_EMA_COVER_LETTER_FINAL.docx (identical paragraph and table text); 02_EMA_MANUSCRIPT_REVIEW.pdf (identical extracted text); KNOWN_ANSWER_TESTS_FINAL.csv/.md: same 24/24 PASS; only the informational literal list of test 22 differs because the committed file predated the RPG template text |
| Tests | EM&A 24/24 PASS; RPG 26/26 PASS |
| Data Availability URL / Code Availability URL | https://github.com/bougtoir/more-rice (HTTP 200) |
| Acquisition instructions / ledgers | RAW_ACQUISITION_LEDGER_2026-11-08.csv; RPG LEDGER via rpg_fetch_rice.py (WFS URLs) |
| Credentials or restricted geometries in repo | none (.geojson absent from tracked files and ZIPs) |
| Licences | WorldClim CC BY 4.0; MapSPAM CC BY 4.0; GMIA (FAO, not redistributed); RPG Licence Ouverte 2.0 (geometries not redistributed) |

Limitation: raw inputs were taken from the durable local store (hash-verified against the ledgers) rather than re-downloaded from every provider during this check.
