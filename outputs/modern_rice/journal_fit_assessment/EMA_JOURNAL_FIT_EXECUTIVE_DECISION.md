# EM&A journal-fit executive decision

**Verdict: EM&A CONDITIONAL GO**

This is a feasibility decision only. The manuscript has not been rewritten, and no frozen result has changed. Rewriting starts only after the author approves the journal.

## Basis (evidence files in this package)

1. **Eligibility and APC** (`JOURNAL_ELIGIBILITY_AND_APC_MATRIX.csv`). EM&A is hybrid; its subscription route has "no APC charges apply" and no page charges. LUP and JEM also have no-fee subscription routes. AWM (USD 3510) and Ecological Indicators (USD 4620) are open access with no subscription route, so they are excluded under the no-mandatory-APC rule.
2. **Published analogues** (`EMA_CLOSEST_PUBLISHED_PAPERS.csv`, 19 papers, 2019–2026, abstracts read from publisher pages). EM&A regularly publishes crop and land suitability assessments:
   - 17/19 introduce no new method;
   - 8/19 state no new field observations;
   - 7/19 validate against observed yield, presence (ROC) or field experiments.
   
   No analogue separates reference construction from spatial-support effects or applies a gate cascade at continental scale.
3. **Novelty** (`NOVELTY_AND_SIGNIFICANCE_BOUNDARY.md`). The defensible contributions are a novel empirical finding and a methodological caution, not a new method:
   - reference construction moves Germany's thermal pass from 96.6% to 3.2%;
   - grid resolution moves results by ≤2.4 points;
   - infrastructure, not temperature, binds the screen (92.2% → 16.0%).
   
   Against EM&A's published record, this is above the typical novelty level. Against Applied Geography's bar, it was not enough.
4. **Scope risk** (`HOSTILE_EMA_EDITORIAL_ASSESSMENT.md`). The binding EM&A risk is its stated preference for the authors' own field data and its exclusion of "Strictly modelling studies with little field data support" and of "Economic based studies". Novelty is not the binding risk there. Existing evidence partly answers the field-data objection: all inputs are observational datasets, and there is an out-of-sample omission check (0.87% of 501,075 ha of observed European rice fails the Hokkaido-derived gate). The objection cannot be fully resolved.
5. **Citation ecology** (`CITATION_ECOLOGY_AND_JOURNAL_NEIGHBORHOOD.md`). 0/37 references come from any of the five candidate journals; 10/37 are from Applied Geography. EM&A citations should be added only where they support a specific claim (three are proposed).

## Conditions for GO (all from `EMA_MINIMAL_CHANGE_FEASIBILITY.md`; no new data)

- C1. Reframe the title, abstract and introduction around the reliability of threshold-transfer suitability assessment. The 150–250-word abstract must state the novelty against current knowledge (an EM&A requirement).
- C2. Lead the results with the reference-construction vs spatial-support decomposition. Report the routine sensitivities briefly.
- C3. Move economic parity to supplementary material (or remove it). Keep the food-risk section short and keep its null-leaning results.
- C4. Restate the existing omission validation and its limit (no commission test is possible while the gate passes 92.2% of land). Disclose that the study collected no new field data.
- C5. Add EM&A literature only where it supports a precise claim (Mohamed 2019; Van 2022; Azadi 2023 or Vahidi 2023).
- C6. EM&A format: 4–6 keywords, continuous line numbers, Statements and Declarations, data availability, editable Word source, figures as separate files.
- Optional (new analysis, author approval needed): an omission-rate curve across thresholds using existing SPAM data.

Estimated effort: 3–5 sessions (+1 for the optional item). Residual desk-rejection risk: moderate to high.

## Comparison

| Journal | Decision | Why |
|---|---|---|
| EM&A | Conditional go | Analogous work is published; novelty is relatively strong for this venue; field-data preference is the main risk |
| Land Use Policy | Alternative | Strong scope fit for a land-use screening question and higher impact. Not audited at the article level. The policy contribution would have to be built by framing, and the novelty bar is likely closer to Applied Geography's (inference) |
| Journal of Environmental Management | Backup | In scope (environmental modelling; climate-resilient agriculture). Requires a novelty statement and warns against standard-method case studies. 6000–8000 words including references |
| Agricultural Water Management | Excluded | Mandatory APC |
| Ecological Indicators | Excluded | Mandatory APC; no indicator is developed |

## Why not the other verdicts

- **Not GO:** the AG version, unchanged, would likely be desk-rejected at EM&A (geographic framing, an economics section, no EM&A literature).
- **Not HOLD or NO-GO:** EM&A publishes comparable work without new field data, the APC-free route is verified, and every condition can be met with existing results.
- **Not RECOMMEND ALTERNATIVE:** LUP's advantage rests on scope text, not on an article-level audit, and its novelty bar is likely higher. The earlier recommendation of LUP is therefore superseded by this evidence. If the author values readership and impact over acceptance probability, LUP remains a legitimate choice.

## Author decision needed

Approve one of the following:
- (a) EM&A with conditions C1–C6;
- (b) EM&A plus the optional omission curve;
- (c) LUP instead.

No rewriting happens before this approval. The uncommitted LUP draft files (`modern_rice/manuscript_lup/`, `modern_rice/scripts/build_lup_manuscript.py`) are kept locally and are not part of this package.
