# 03 — Diffusion Ontology and Coding Rules

Work Package B. A staged (non-sequential) ontology for what could cross medieval borders, with coding rules
that separate evidence *types* (positive / negative / missing / contested) from diffusion *stages*.

## Stages (not a strict sequence)

| Code | Stage | Operational test |
|------|-------|------------------|
| D0 | No accessible evidence | Sources searched do not address the item for this cell. **Not** a claim of historical absence. |
| D1 | Commodity circulating | Edible rice attested in trade, diet, cookbooks, medicine, taxation of the commodity |
| D2 | Plant-level awareness | Rice known as a cultivated plant (not only as grain) — travel accounts, botany, agronomy texts |
| D3 | Actionable cultivation knowledge | Instructions/knowledge sufficient to attempt cultivation (manuals, resident cultivators, inherited practice) |
| D4 | Input availability | Seed stock, tools, experienced cultivators, irrigation specialists present |
| D5 | Documented attempt | A trial/introduction event recorded |
| D6 | Sustained cultivation | Continued production (tax entries, repeated registers, archaeobotanical series) |
| D7 | Institutional/policy transfer | Legal water rules, administrative templates, or explicit crop policy adopted elsewhere |

Stages may co-occur and skip: tacit knowledge can arrive with a Mudéjar cultivator (D3/D4) leaving no
written trace; an institution (D7) can travel without the crop; D1 can precede or follow D6.

## Evidence types per cell

- **POS** — positive attestation (dated source passage cited verbatim)
- **NEG** — a searched source *of the right kind* is silent (e.g., a crop-by-crop register listing named crops
  that omits rice) — weaker than POS
- **MIS** — no source of a type able to record the item survives/accessible → D0
- **CON** — sources conflict (e.g., Vella forgeries vs genuine documents)

## Coding rules

1. Every POS cell cites exact passage/date. NEG cells cite the source *and* why it would record the item if
   present (document purpose, vocabulary, completeness). MIS cells name the missing source class.
2. Dynastic marriage, diplomatic contact, commodity trade, and translation absence are **not proxies** for
   cultivation-technology transfer (spec guardrail 2). Each edge codes the *item*, not the relationship.
3. Non-textual channels — Mudéjar cultivators, migrants, merchants, estate managers, oral instruction,
   inherited practice — are coded as channel `personnel/tacit` with evidence type assigned by what survives
   (usually NEG or MIS at D3–D5).
4. Post-1300 evidence is coded in separate cells flagged `post_period` and can only support *continuity of
   practice* claims, never contemporaneous motives.
5. Corrections to Phase 1–2 cells are appended, not overwritten.

## Item codes used in 04_MULTILAYER_TRANSMISSION_EDGES.csv

`grain` (edible rice commodity), `knowledge` (cultivation knowledge), `seed`, `irrig_tech` (irrigation
technique), `personnel` (cultivators/specialists), `water_inst` (water governance/legal institutions),
`admin` (administrative/legal templates), `policy` (crop-specific policy).
