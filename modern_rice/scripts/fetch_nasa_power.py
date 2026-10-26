#!/usr/bin/env python3
"""Fetch NASA POWER daily agro-meteorology for candidate region points and
compute rice-relevant seasonal risk metrics (replaces ERA5 grid for pilot
scale — daily, satellite-reanalysis blend, ~0.5deg)."""
import urllib.request, json, os, csv, time
RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "modern_rice")
os.makedirs(OUT, exist_ok=True)

POINTS = {
 "LowerDanube_RO": (43.9, 25.9), "Balkan_Osijek": (45.5, 18.7),
 "SUkraine_Kherson": (46.6, 32.6), "CentralAsia_Tashkent": (41.3, 69.2),
 "CChile": (-34.5, -70.8), "Camargue_FR": (43.5, 4.5),
 "PoValley_IT": (45.3, 9.4), "Ebro_ES": (41.8, 1.0),
 "NFrance": (49.0, 2.5), "England": (52.5, 0.5), "Germany": (52.5, 10.0),
 "Hokkaido_JP": (43.2, 143.0), "SJapan": (33.6, 130.6),
 "Bangladesh": (23.8, 90.4), "California": (38.5, -121.5),
 "Spain_Andalucia": (37.4, -5.9), "DanubeDelta": (45.2, 29.5),
}
P = {k: f"nasa_power_{k}.json" for k in POINTS}

for k,(la,lo) in POINTS.items():
    fp = os.path.join(RAW, P[k])
    if not os.path.exists(fp):
        url = (f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M_MAX,T2M_MIN,PRECTOTCORR"
               f"&community=AG&longitude={lo}&latitude={la}&start=20000101&end=20241231&format=JSON")
        for att in range(3):
            try:
                urllib.request.urlretrieve(url, fp); break
            except Exception as e:
                print(k, "retry", att, e); time.sleep(5)
        time.sleep(1)
import numpy as np
rows=[]
for k in POINTS:
    d=json.load(open(os.path.join(RAW,P[k])))
    p=d["properties"]["parameter"]
    tmax=np.array([v for v in p["T2M_MAX"].values()]); tmin=np.array([v for v in p["T2M_MIN"].values()])
    prec=np.array([v for v in p["PRECTOTCORR"].values()])
    dates=sorted(p["T2M_MAX"].keys())
    doy=np.array([int(x[4:6])*30.4+int(x[6:8]) for x in dates])
    lat=POINTS[k][0]
    # growing window: months Jun-Sep NH, Dec-Mar SH
    if lat>=0: win=(doy>=150)&(doy<=285)
    else: win=(doy>=335)|(doy<=90)
    tmean=(tmax+tmin)/2
    gdd=np.maximum(tmean-10,0)
    # seasonal aggregates per calendar year
    gdd_s=[]; coldsnap=[]; heat=[]; ff=[]
    yrs=set(int(x[:4]) for x in dates)
    for y in sorted(yrs):
        idx=np.array([int(x[:4])==y for x in dates])
        gdd_s.append(gdd[idx&win].sum())
        coldsnap.append((tmin[idx&win]<12).sum())       # nights <12C in flowering window
        heat.append((tmax[idx&win]>35).sum())            # hot days in window
        yr_idx=idx.copy()
        ff.append((tmin[yr_idx]>0).sum())                # frost-free days/yr
    gdd_s=np.array(gdd_s); coldsnap=np.array(coldsnap); heat=np.array(heat); ff=np.array(ff)
    rows.append([k, round(gdd_s.mean(),0), round(np.std(gdd_s),0),
                 round(coldsnap.mean(),1), round(np.percentile(coldsnap,90),1),
                 round(heat.mean(),1), round(ff.mean(),0),
                 round(np.nanmin(gdd_s),0)])
with open(os.path.join(OUT,"DAILY_CLIMATE_POINT_METRICS.csv"),"w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["point","gdd10_season_mean","gdd10_sd","coldsnap_nights_lt12_mean","coldsnap_p90","hotdays_gt35_mean","frostfree_days","gdd10_min_year"])
    w.writerows(rows)
print("done")
