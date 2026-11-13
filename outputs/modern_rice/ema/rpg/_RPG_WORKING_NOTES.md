# RPG working notes (facts verified 2026-11-13)
- Source: IGN Géoplateforme WFS https://data.geopf.fr/wfs ; dataset page https://cartes.gouv.fr/rechercher-une-donnee/dataset/IGNF_RPG ; licence etalab-2 (Licence Ouverte 2.0).
- Layers: RPG.2015..2024:parcelles_graphiques (fields id_parcel, surf_parc [ha], code_cultu, code_group, culture_d1, culture_d2); RPG.2010-2014 rpg_20xx (îlots).
- Codebook RPG.LATEST:codes_cultures: RIZ = "Riz", groupe 14 "Riz" (rice-specific code).
- Raw (gitignored): modern_rice/data/raw/rpg/rpg{2015,2020,2024}_riz_p000.geojson; LEDGER.txt has URL/UTC/bytes/SHA-256.
- France-wide RIZ parcels: 2015 1,459 (15,928.9 ha); 2020 1,706 (14,525.5 ha); 2024 1,616 (13,665.1 ha). Fetch script: modern_rice/scripts/rpg_fetch_rice.py.
- RPG = anonymised CAP aid declarations (administrative, farmer-declared, controlled), independent of MapSPAM/WorldClim.
- Next: rpg_validation.py — overlay with ema_layers_5m.npz g5 (WorldClim 5', window 29Apr-11Sep); area-weighted intersection + centroid sensitivity; unique climate cells; thresholds 589/900/1100 + sweep; compare with MapSPAM rice in same French region cells (SPAM 2010 France rice 21,961 ha, MapSPAM irrigated share 0 for France).
