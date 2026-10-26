# Gate 1 — Irrigation & Water-Stress Audit

Data: FAO GMIA v5 AEI% (5-arcmin ASCII, SHA in data/ACQUISITION_LEDGER.csv) aggregated to 10-min + World Bank SDG 6.4.2 freshwater-withdrawal stress (wb_waterstress_642.csv).

Findings (see IRRIGATION_GMIA_CANDIDATES.csv):
- Po Valley (AEI ~47% in feasible cells) and Bangladesh (28%) — established irrigation systems; paddy infrastructure already present.
- Ebro (21%), Camargue (13%), Lower Danube (11%) — moderate existing irrigation; paddy conversion would need additional water allocation.
- Central Asia / Tashkent (AEI 8%) — thermally best candidate but Amu/Syr Darya basins are among the world's most water-stressed; expansion requires demonstrated sustainable allocation → conditional, not unconditional GO.
- Kazakhstan N (AEI ~0%), Balkans/Osijek (2%), S. Ukraine (9%) — paddy would be new water demand in cereal belts; classified "potentially irrigable — allocation unproven".
- England/N. France/Germany — no feasible cells; irrigation cannot fix a thermal constraint.

Water-stress join: Central Asian candidate sits in countries with high SDG 6.4.2 stress → flagged UNACCEPTABLE unless allocation demonstrated. Danube/Ukraine/Kazakhstan → CAUTION tier.

Classes used: feasible / existing-irrigated / potentially-irrigable / water-stress-unacceptable, per spec. No assumption that climatically suitable = irrigable.
