# Final semantic code audit

| File | Change | Effect on results |
|---|---|---|
| modern_rice/manuscript_ema/manuscript_template.md | 13 wording edits + 1 Discussion paragraph (applied by ema_finish_edits.py with exact-match assertions) | None: no placeholder or number changed |
| modern_rice/scripts/build_ema_manuscript.py | Cover-letter text; `build(True, MS)` embeds figures in the submission manuscript; cover-letter guard (no `{`, `N[`, we/our); `CL_AUTHOR` | None: same canonical inputs and assertions |
| modern_rice/scripts/ema_finish_edits.py (new) | Records and applies the calibration edits | None |
| modern_rice/scripts/ema_finish_reports.py (new) | Audits, gates, packaging | None (reads built files only) |

All values in the cover letter are injected from the same canonical `N` dictionary as the manuscript; no literal result was introduced. KAT 22 (no hard-coded headline results in the template) passes.

Builder diff: 12 added / 7 removed lines.
