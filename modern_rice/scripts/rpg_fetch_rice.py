#!/usr/bin/env python3
"""Fetch RPG rice parcels (code_cultu='RIZ') for France via IGN Géoplateforme WFS; raw pages saved under modern_rice/data/raw/rpg (gitignored)."""
import os, sys, json, hashlib, datetime, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "..", "data", "raw", "rpg"); os.makedirs(RAW, exist_ok=True)
YEARS = [int(y) for y in sys.argv[1:]] or [2015, 2020, 2024]
for y in YEARS:
    start, n = 0, 0
    while True:
        q = dict(SERVICE="WFS", REQUEST="GetFeature", VERSION="2.0.0", TYPENAMES=f"RPG.{y}:parcelles_graphiques", OUTPUTFORMAT="application/json", SRSNAME="EPSG:4326",
                 COUNT="5000", STARTINDEX=str(start), CQL_FILTER="code_cultu='RIZ'", SORTBY="id_parcel")
        u = "https://data.geopf.fr/wfs?" + urllib.parse.urlencode(q)
        b = urllib.request.urlopen(u, timeout=300).read(); fn = f"rpg{y}_riz_p{start//5000:03d}.geojson"; open(os.path.join(RAW, fn), "wb").write(b)
        k = len(json.loads(b)["features"]); n += k
        open(os.path.join(RAW, "LEDGER.txt"), "a").write(f"{fn} {datetime.datetime.utcnow().isoformat()}Z {len(b)} {hashlib.sha256(b).hexdigest()} {u}\n")
        print(y, start, k, flush=True)
        if k < 5000: break
        start += 5000
    print("year", y, "features", n, flush=True)
