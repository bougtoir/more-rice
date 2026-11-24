#!/usr/bin/env python3
"""Finishing pass: apply the recorded claim-calibration and contingency edits to the EM&A template and builder (idempotent)."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TPL = os.path.join(ROOT, "modern_rice", "manuscript_ema", "manuscript_template.md")
OUT = os.path.join(ROOT, "outputs", "modern_rice", "ema", "finished", "CLAIM_CALIBRATION_EDITS.json")
CP = ("Beyond long-term agricultural adaptation, spatial suitability screening could also provide a preliminary input to contingency crop-substitution planning after a widespread crop-specific disease outbreak; a severe disruption to wheat production, for example, could prompt an assessment of alternative crops. This study did not evaluate any disease scenario, and its results do not identify rice as a preferred alternative. They do indicate why thermal screening alone would be insufficient for such planning: the candidate area depends strongly on reference construction, and mapped irrigation infrastructure, which is not evidence of available water, imposes a further constraint. Operational substitution capacity would require separate assessment of water availability, seed supply, machinery, seasonal timing, conversion costs and attainable yields.")
E = [  # (id, section, construct, original, revised, reason)
 ("T1", "Abstract", "threshold discrimination", "warm cells and cannot rank references.", "warm cells and barely discriminates between references.",
  "Limited empirical discrimination in the evaluated data, not formal non-identifiability."),
 ("T2", "Abstract", "threshold strictness", "Presence-only coverage constrains only implausibly strict thresholds;", "Presence-only coverage constrains only thresholds that omit much recorded rice;",
  "Physiological implausibility is not established; the evidence is observed-land-use omission."),
 ("T3", "2.4", "threshold discrimination", "over thresholds that the rice data cannot distinguish.", "over thresholds that the rice data barely distinguish.",
  "Omission does change (1.37% to 3.22%); 'cannot' overstates."),
 ("T4", "3.4", "threshold discrimination", "The mapped rice data therefore reject thresholds that would exclude much of current Mediterranean and Danubian rice production but cannot discriminate among the Hokkaido-derived references",
  "The mapped rice data therefore weigh against thresholds that would exclude much of current Mediterranean and Danubian rice production but provide little discrimination among the Hokkaido-derived references",
  "No formal test of rejection; limited, not zero, discrimination."),
 ("T5", "3.5", "threshold discrimination", "reinforcing that the omission check cannot rank these references.", "so the omission check has little power to rank these references.",
  "Scenario ranges comparable to the T*-900 difference imply low, not zero, power."),
 ("T6", "3.7", "MapSPAM allocation", "The omission of MapSPAM rice area in France is therefore an allocation effect outside the declared rice district, consistent with the low-density margin cells identified in Section 3.5, rather than evidence that the gate excludes current production.",
  "The omission of MapSPAM rice area in France therefore occurs outside the declared rice district. This is consistent with differences in spatial allocation, spatial support and data-generation procedures between the two datasets, including the low-density margin cells identified in Section 3.5, although their individual contributions cannot be isolated; it does not indicate that the gate excludes declared production.",
  "The RPG-MapSPAM comparison is descriptive; allocation, support, reference-year and data-generation causes are not separated."),
 ("T7", "3.7", "threshold discrimination", "The independent records do not, however, help to rank references:", "The independent records, however, provide little discrimination between references:",
  "Limited discrimination in the evaluated data."),
 ("T8", "4.1", "coverage vs validity", "Third, the available reference data on existing rice area validate neither specification in the critical range. Low omission at T* demonstrates that the gate does not exclude current European rice production, but because",
  "Third, the available reference data on existing rice area provide little empirical discrimination between the specifications in the critical range. Low omission at T* indicates that the gate excludes little of the mapped and declared European rice area, but because",
  "'demonstrates ... does not exclude' overstates a 1.37% omission; 'validate' conflates coverage with agronomic validity."),
 ("T9", "4.2", "MapSPAM allocation", "it can separate allocation effects from omission of real production.", "it can help to distinguish omissions that arise from spatial allocation from omissions of declared production.",
  "The register does not causally separate allocation effects."),
 ("T10", "5", "coverage vs validity", "confirm that the gate does not exclude current European production, but neither can discriminate between references",
  "indicate that the gate excludes little current European production, but neither provides much discrimination between references",
  "Calibrated to the observed omission and to limited discrimination."),
 ("T11", "4.2 (new paragraph)", "contingency application", "## 4.3 Limitations and external validation", CP + "\n\n## 4.3 Limitations and external validation",
  "Prospective application only; no disease scenario, capacity or food-security claim."),
 ("T12", "Abstract", "length (editorial)", "Omissions fall mainly in low-density allocation cells at climatic margins.", "Omissions fall mainly in marginal low-density allocation cells.",
  "Keeps the abstract within the 250-word limit after T1-T2; same meaning."),
 ("T13", "Abstract", "length (editorial)", "In a controlled contrast for Germany, the pass share", "In a controlled German contrast, the pass share",
  "Keeps the abstract within the 250-word limit; same meaning."),
]
t = open(TPL, encoding="utf-8").read(); log = []
for i, sec, k, o, r, why in E:
    if r in t and not (i == "T11" and t.count("## 4.3") == 1 and CP not in t): pass
    else: assert t.count(o) == 1, (i, t.count(o)); t = t.replace(o, r)
    assert r in t, i
    log.append(dict(id=i, document="manuscript", section=sec, construct=k, original=o, revised=r, reason=why, numerical_results_changed="NO"))
open(TPL, "w", encoding="utf-8").write(t)
json.dump(log, open(OUT, "w"), indent=1, ensure_ascii=False); print(len(log), "edits recorded")
