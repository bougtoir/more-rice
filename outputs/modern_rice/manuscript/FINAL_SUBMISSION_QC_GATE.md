# Final Pre-Submission QC Gate

Baseline: public main @ 938fcd4; Phase 10 audits executed on a clean public clone, not the local tree.

## Verification tiers
- **Independently reproduced:** NASA POWER re-fetch + upland water balance for Hokkaido_JP / Morioka_JP / LowerDanube_RO -> identical regenerated metrics (48.0/8.0, 20.0/8.0, 100.0/92.0).
- **Verified against retained inputs:** suitability screening, risk-portfolio values, cost registry (raw data retained locally with ledger + SHA256; restricted/large data not committed).
- **Checked only against prior outputs:** figure renderings, docx layout.
- **Unverified:** none material (Romania rice-cost observations remain absent by design - break-even framing only).

## Input-perturbation test (Task 2)
Changing TAW 100->60mm in the clone and re-running the pipeline changed every downstream metric (Hokkaido flower-deficit 48.0->36.0%, Morioka 20.0->24.0%, LowerDanube unchanged at ceiling 100.0%) -> the pipeline recalculates; outputs are not frozen literals.

## Gates
A scientific validity PASS / B reproduction PASS / C consistency PASS / D references PASS / E docx PASS / F adversarial PASS / G journal fit (Agricultural Systems) PASS.

## Decision
**SUBMIT** — manuscript and cover letter ready for author approval. Submission is NOT executed; it requires explicit user approval.
