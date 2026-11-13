# RPG crop-code verification

Source: official codebook layer `RPG.LATEST:codes_cultures` (144 codes), saved as `rpg_latest_codes_cultures.csv`.

## Codes in crop group 14

| FID | code_culture | libelle_culture | code_groupe_culture | libelle_groupe_culture |
|---|---|---|---|---|
| codes_cultures.99 | RIZ | Riz | 14 | Riz |

## Codes whose label contains 'riz'

| FID | code_culture | libelle_culture | code_groupe_culture | libelle_groupe_culture |
|---|---|---|---|---|
| codes_cultures.99 | RIZ | Riz | 14 | Riz |

Group 14 contains exactly 1 crop code, so `RIZ` is rice-specific and is not a broad group (verdict: **RICE-SPECIFIC**). The 2010 îlot layer uses the older numeric group code `14`, whose label in the retrieved features is `RIZ`; in 2010 a feature is an agricultural block (îlot) and `surf_cultu` gives the area of the rice group within it, which the analysis uses as the area weight.

## Values in the retrieved features

- 2010: {"code_cultu": {"14": 893}, "nom_cultu": {"RIZ": 893}, "culture_d1 (secondary/catch crop, non-empty)": {}}
- 2015: {"code_cultu": {"RIZ": 1459}, "code_group": {"14": 1459}, "culture_d1 (secondary/catch crop, non-empty)": {}}
- 2020: {"code_cultu": {"RIZ": 1706}, "code_group": {"14": 1706}, "culture_d1 (secondary/catch crop, non-empty)": {"DTR": 1}}
- 2024: {"code_cultu": {"RIZ": 1616}, "code_group": {"14": 1616}, "culture_d1 (secondary/catch crop, non-empty)": {"DFV": 2, "DTR": 1}}

The main-crop code is RIZ (or 14 in 2010) for every retrieved feature. A few 2020/2024 parcels also report a secondary (catch) crop in `culture_d1`; the main crop remains rice and these parcels are retained. Rice is irrigated paddy rice in the Camargue context, but the code does not distinguish cultivars or water management; no claim depends on that distinction.
