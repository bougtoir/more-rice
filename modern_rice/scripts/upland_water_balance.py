#!/usr/bin/env python3
"""Phase 8 Task 3: daily root-zone water balance for upland-rice feasibility.
Model: single-layer bucket (TAW 100mm, scenario class), daily P from NASA POWER,
ETc = Kc*ET0, ET0 via Hargreaves-Samani (Tmax,Tmin,lat -> extraterrestrial Ra).
Season: 120-day upland crop window starting Jun 1 (NH). Deficit counted when
soil water < 30% TAW by stage (establish 0-25d, veg 25-70, flower 70-95, fill 95-120).
"""
import os, json, math, csv
import numpy as np, pandas as pd
RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "modern_rice")
POINTS = {"Hokkaido_JP":43.2,"Morioka_JP":39.7,"LowerDanube_RO":43.9,"Balkan_Osijek":45.5,
 "SUkraine_Kherson":46.6,"Danube_HU":47.0,"Rhine_DE":50.9,"Alsace_FR":48.5,"Loire_FR":47.5,
 "Saxony_DE":51.0,"Berlin_DE":52.5,"Beauce_FR":48.4,"Kent_UK":51.2,"Denmark_Aarhus":56.2,
 "Lund_SE":55.7,"Warsaw_PL":52.2,"Vilnius_LT":54.7,"CentralAsia_Tashkent":41.3,"Vercelli_IT":45.3}
TAW, STRESS_FRAC = 100.0, 0.30
KC = {0:1.05, 25:1.10, 70:1.20, 95:1.05}  # stage-start day -> Kc
def kc(d):
    for s in sorted(KC, reverse=True):
        if d>=s: return KC[s]
def Ra(lat, doy):
    doy=np.asarray(doy,float)
    phi=math.radians(lat); dr=1+0.033*np.cos(2*np.pi*doy/365)
    dec=0.409*np.sin(2*np.pi*doy/365-1.39)
    ws=np.arccos(np.clip(-math.tan(phi)*np.tan(dec),-1,1))
    return 37.6*dr*(ws*math.sin(phi)*np.sin(dec)+math.cos(phi)*np.cos(dec)*np.sin(ws))
rows=[]
for k,lat in POINTS.items():
    fp=os.path.join(RAW,f"nasa_power_{k}.json")
    if not os.path.exists(fp): continue
    d=json.load(open(fp))["properties"]["parameter"]
    df=pd.DataFrame({"tmax":d["T2M_MAX"],"tmin":d["T2M_MIN"],"p":d["PRECTOTCORR"]})
    df.index=pd.to_datetime(df.index)
    df["doy"]=df.index.dayofyear
    df["et0"]=0.0023*Ra(lat,df.doy.values)*np.sqrt(np.clip(df.tmax-df.tmin,0,None))*(0.5*(df.tmax+df.tmin)+17.8)*0.408
    per=[]
    df["year"]=df.index.year
    for yr,gdf in df[df.doy.between(152,271)].groupby("year"):
        gdf=gdf.sort_values("doy")
        if len(gdf)<110: continue
        sw=TAW; deficits={s:0 for s in ["est","veg","flower","fill"]}
        for i,(_,r) in enumerate(gdf.iterrows()):
            etc=kc(i)*r.et0; sw=min(TAW, max(0, sw + r.p - etc))
            if sw < STRESS_FRAC*TAW:
                s="est" if i<25 else "veg" if i<70 else "flower" if i<95 else "fill"
                deficits[s]+=1
        per.append(deficits)
    if not per: continue
    P=pd.DataFrame(per)
    rows.append([k, len(P), *[round(P[s].mean(),1) for s in ["est","veg","flower","fill"]],
                 round((P.flower>10).mean()*100,1), round((P.fill>15).mean()*100,1)])
w=csv.writer(open(os.path.join(OUT,"DAILY_SOIL_WATER_BALANCE.csv"),"w"))
w.writerow(["point","n_years","deficit_days_est","deficit_days_veg","deficit_days_flower","deficit_days_fill",
            "P_flower_deficit_10d_pct","P_fill_deficit_15d_pct"])
w.writerows(rows)
print(pd.DataFrame(rows).to_string())
