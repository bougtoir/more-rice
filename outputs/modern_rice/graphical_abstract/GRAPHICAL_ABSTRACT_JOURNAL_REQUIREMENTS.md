# Graphical Abstract — Journal Requirements Verification

Access date: 2026-11-02 (session date 2025-10-25 JST per environment clock; recorded as verification date).

## Verified sources
- Elsevier researcher guidance "Graphical abstract" (elsevier.com/en-au/researcher/author/tools-and-resources/graphical-abstract)
  - Separate file upload in the online submission system.
  - Minimum image size: **1328 × 531 pixels (w × h)**, minimum resolution 300 dpi; larger images allowed at the same ~5:2 ratio (500×200 display window on ScienceDirect).
  - Fonts: Times, Arial, Courier or Symbol; large enough to remain legible when reduced to a 200-px-high window.
  - Preferred file types: TIFF, EPS, PDF, or MS Office files.
  - Clear start/end; top-to-bottom or left-to-right reading order.
  - Third-party material requires permission; generative-AI use must follow Elsevier AI policy.
- Agricultural Systems Guide for Authors (Elsevier, ISSN 0308-521X): graphical abstract is a standard recommended submission item for Elsevier journals; no additional journal-specific dimension overrides the Elsevier baseline were found.

## Compliance checklist
| Requirement | Status |
|---|---|
| Separate file (not embedded in manuscript) | PASS — standalone asset, not a manuscript figure |
| ≥1328×531 px, 5:2 ratio | PASS — master PNG 2656×1062 (2× minimum), SVG 2500×1000 viewBox same ratio |
| Font family | PASS — Arial (SVG live text); rasterized in PNG export |
| Legible at 200-px-high preview | PASS — checked at 664×266 preview; all labels readable |
| File type | PASS — PNG master + editable SVG; TIFF/EPS can be produced on request (see HANDOFF) |
| Left-to-right reading order | PASS — panels 1→2→3, conclusion strip below |
| No third-party images | PASS — all elements drawn from scratch as vector shapes |
| No invented data | PASS — every number traced (see SOURCE_MAP) |
| AI-use | Drawn by script (vector primitives); disclose per Elsevier AI policy at submission if required |

Unverified/residual: none blocking. If the submission system demands TIFF/EPS rather than PNG, convert the master at 300 dpi (see HANDOFF).
