# Independent spatial recompute (own code): GDD from WC 5' tavg, fractional pipeline window, Hokkaido P05, Europe masks
import numpy as np, rasterio, geopandas as gpd
from rasterio.features import rasterize
from rasterio.windows import from_bounds
from affine import Affine
W,E,S,N=-11,45,34,71.5
def rd(f,b=(W,S,E,N)):
    with rasterio.open(f) as s:
        win=from_bounds(*b,transform=s.transform).round_offsets().round_lengths(); a=s.read(1,window=win).astype(float); t=s.window_transform(win)
    a[a<-1e30]=np.nan; return a,t
WIN={4:2,5:31,6:30,7:31,8:31,9:11}
def gdd(b): return sum(np.maximum(rd(f"wc2.1_5m_tavg_{m:02d}.tif",b)[0]-10,0)*d for m,d in WIN.items())
# Hokkaido via Natural Earth admin-1 polygon if available, else box
import os
hb=(139.3,41.35,146.0,45.6); gH=gdd(hb); rH,tH=rd("spam2010V2r0_global_H_RICE_A.tif",hb); rH[rH<0]=0
try:
    a1=gpd.read_file([p for p in [ "ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp"] if os.path.exists(p)][0])
    hk=a1[a1["name"]=="Hokkaido"].geometry; mk=rasterize([(g,1) for g in hk],out_shape=rH.shape,transform=tH,fill=0)
    print("Hokkaido polygon mask used"); rH=rH*mk
except Exception as e: print("admin1 not available:",e); 
m=np.isfinite(gH)&(rH>0); o=np.argsort(gH[m]); cw=np.cumsum(rH[m][o])/rH[m].sum()
print("Hokkaido rice ha",rH.sum(),"P05",gH[m][o][np.searchsorted(cw,0.05)],"P01",gH[m][o][np.searchsorted(cw,0.01)],"P50",gH[m][o][np.searchsorted(cw,0.5)])
T=589
g=gdd((W,S,E,N)); inc=sum(np.clip(rd(f"spam2010V2r0_global_H_{c}_A.tif")[0],0,None) for c in ["WHEA","MAIZ","BARL","POTA"])
aei,_=rd("gmia_v5_aei_ha.asc") if False else (None,None)
A=np.loadtxt("gmia_v5_aei_ha.asc",skiprows=6); r0,c0=int((90-N)*12),int((W+180)*12); aei=A[r0:r0+g.shape[0],c0:c0+g.shape[1]].clip(0,None)
_,t=rd("wc2.1_5m_tavg_07.tif"); lat=t.f+(np.arange(g.shape[0])+0.5)*t.e
cell=(6371.0072**2*np.deg2rad(1/12)*np.abs(np.sin(np.deg2rad(lat-t.e/2))-np.sin(np.deg2rad(lat+t.e/2)))*100)[:,None]
sh=aei/cell
ne=gpd.read_file("ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp")
def stats(lab,mask):
    v=np.isfinite(g)&(inc>0)&mask; tot=inc[v].sum(); th=v&(g>=T); ai=th&(sh>=0.10)
    print(f"{lab}: inc {tot/1e6:.2f} Mha | thermal pass {100*inc[th].sum()/tot:.1f}% | thermal+AEI {100*inc[ai].sum()/tot:.1f}% ({inc[ai].sum()/1e6:.2f} Mha) | AEI among thermal-pass {100*inc[ai].sum()/inc[th].sum():.1f}% | nan-GDD inc {inc[~np.isfinite(g)&mask].sum()/1e6:.3f} Mha")
stats("rectangle (as in script)",np.ones_like(g,bool))
for lab,sel in [("NE CONTINENT==Europe (incl. European Russia part in window)",ne.CONTINENT=="Europe"),("Europe excl Russia/Belarus/Ukraine/Moldova",(ne.CONTINENT=="Europe")&~ne.ADMIN.isin(["Russia","Belarus","Ukraine","Moldova"])),("EU27",ne.ADMIN.isin(["Austria","Belgium","Bulgaria","Croatia","Cyprus","Czechia","Denmark","Estonia","Finland","France","Germany","Greece","Hungary","Ireland","Italy","Latvia","Lithuania","Luxembourg","Malta","Netherlands","Poland","Portugal","Romania","Slovakia","Slovenia","Spain","Sweden","Czech Republic"]))]:
    mk=rasterize([(gg,1) for gg in ne[sel].geometry],out_shape=g.shape,transform=t,fill=0).astype(bool); stats(lab,mk)
mk=rasterize([(gg,1) for gg in ne[ne.CONTINENT!="Europe"].geometry],out_shape=g.shape,transform=t,fill=0).astype(bool)
stats("NON-Europe part of rectangle",mk)
