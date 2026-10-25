# more-rice — Medieval rice adoption feasibility audit

Evidence-first historical audit: was rice cultivation politically suppressed in
medieval Western Europe (AD 1000–1300)?

## Verdict

**CONDITIONAL GO** — comparative institutional study. The affirmative suppression
hypothesis is a **NO-GO**: zero documents restrict rice; documented interventions
(Valencia Furs 1238–1276, Sforza 1475) promoted or protected it; the early-Sicily
claim rests on the Vella forgeries. Non-adoption is overdetermined by climate,
irrigation infrastructure and the Arabic–Latin knowledge barrier.

## Layout

- `outputs/` — all 12 audit deliverables (report docx + registries + reviews)
- `data/raw/` — downloaded legally accessible source PDFs
- `data/ACQUISITION_LEDGER.csv`, `data/SHA256SUMS.txt` — provenance + checksums
- `scripts/productivity_comparison.py` — generates the productivity CSV
  (documented inputs only; no hardcoded results)
- `scripts/build_report.py` — regenerates `RESEARCH_FEASIBILITY_REPORT.docx`
- `docs/spec.txt` — the original audit specification

## Reproduce

```bash
pip install python-docx
python3 scripts/productivity_comparison.py   # -> outputs/MEDIEVAL_PRODUCTIVITY_COMPARISON.csv
python3 scripts/build_report.py              # -> outputs/RESEARCH_FEASIBILITY_REPORT.docx
```

Environment: Python ≥3.10, python-docx. No other dependencies for the CSVs/MDs.
