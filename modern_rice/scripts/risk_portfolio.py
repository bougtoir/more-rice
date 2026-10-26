#!/usr/bin/env python3
"""Food-supply risk model: does adding rice reduce severe shortfall?

Data: FAOSTAT QCL yields (kg/ha) 1961-present for wheat, barley, maize,
potatoes, rice per focal country. Detrend log-yields (linear trend on year);
residuals preserve real interannual dependence within country (same-year
cross-crop shocks retained by keeping rows aligned on year).

Scenarios (per country):
 A existing portfolio = observed cereal mix (wheat+barley+maize equally
   weighted by harvested-area shares, latest year).
 B partial rice substitution = replace f in {0.10,0.20} of cereal area
   with rice; rice shock from country's own series if >=15 obs else
   analog-region residual pool (documented mapping).
 C additional rice = A + rice at f of total area (no displacement).
 D non-rice comparator = substitute f with potatoes (caloric comparator).
Metrics: mean kcal/ha, sd, P5, ES5 (CVaR below P5 shortfall vs 0.8*mean
 threshold), P(portfolio<0.8*mean), P(joint shock: main cereal AND
 substitute both < -15%).
"""
import pandas as pd, numpy as np, os, csv, json

RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "modern_rice")
os.makedirs(OUT, exist_ok=True)
F = os.path.join(RAW, "Production_Crops_Livestock_E_All_Data_(Normalized).csv")

CROPS = {"wheat":"Wheat","barley":"Barley","maize":"Maize (corn)",
         "rice":"Rice","potato":"Potatoes"}
KCAL = {"Wheat":3.4,"Barley":3.5,"Maize (corn)":3.6,"Rice":3.65,"Potatoes":0.8}
COUNTRIES = ["Romania","Bulgaria","Serbia","Ukraine","Chile","Kazakhstan",
             "Uzbekistan","France","Germany","United Kingdom of Great Britain and Northern Ireland",
             "Italy","Spain","Portugal","Greece","Hungary","Croatia","Poland",
             "Japan","Bangladesh","United States of America","Argentina","Australia"]
ANALOG = {  # rice shock analog when local rice series absent/short
 "Romania":"Bulgaria","Bulgaria":"Greece","Serbia":"Hungary","Ukraine":"Italy",
 "Chile":"Argentina","Kazakhstan":"Uzbekistan","France":"Spain","Germany":"Italy",
 "United Kingdom of Great Britain and Northern Ireland":"Italy","Croatia":"Greece",
 "Poland":"Hungary"}

d = pd.read_csv(F, usecols=["Area","Item","Element","Year","Value"], low_memory=False)
d = d[d.Area.isin(COUNTRIES)&d.Item.isin(CROPS.values())]
yld = d[d.Element=="Yield"].pivot_table(index=["Area","Item","Year"], values="Value").reset_index()
area = d[d.Element=="Area harvested"]

def detrend(g):
    if len(g)<12: return None
    x=g.Year.values; y=np.log(np.clip(g.Value.values,1,None))
    b=np.polyfit(x,y,1); res=y-np.polyval(b,x)
    return pd.Series(res,index=g.Year.values)
resid = yld.groupby(["Area","Item"]).apply(detrend, include_groups=False)
# flatten to dict
R={}
for (a,i),s in resid.groupby(level=[0,1]):
    if s is not None: R[(a,i)]=s.droplevel([0,1])
latest = yld.groupby(["Area","Item"]).apply(lambda g:g.loc[g.Year==g.Year.max()].Value.iloc[0], include_groups=False)
ares = area.groupby(["Area","Item"]).apply(lambda g:g.loc[g.Year==g.Year.max()].Value.iloc[0], include_groups=False)

def rice_resid(c):
    if (c,"Rice") in R and len(R[(c,"Rice")])>=15:
        return R[(c,"Rice")], c
    a=ANALOG.get(c)
    if a and (a,"Rice") in R: return R[(a,"Rice")], "analog:"+a
    return None, None

rows_dep=[]; rows_port=[]
f=0.2
for c in COUNTRIES:
    mains=[i for i in ["Wheat","Barley","Maize (corn)"] if (c,i) in R]
    if not mains: continue
    # portfolio kcal per ha per year: equal-weighted area shares of available cereals
    shares={i:(ares.get((c,i),np.nan)) for i in mains}
    tot=sum(v for v in shares.values() if np.isfinite(v))
    shares={i:(v/tot if np.isfinite(v) else 1/len(mains)) for i,v in shares.items()}
    yrs=set.intersection(*[set(R[(c,i)].index) for i in mains])
    if not yrs: continue
    yr_yld={i:{y: latest.get((c,i),np.nan)*np.exp(R[(c,i)][y]) for y in yrs} for i in mains}
    yrs=sorted(yrs)
    def port_series(subs, sub_resid, frac, add=False):
        out=[]
        for y in yrs:
            base=sum(shares[i]*yr_yld[i][y]*KCAL[i] for i in mains)
            sh=1-frac if not add else 1.0
            v=base*sh
            ry=latest.get((c,"Rice"),np.nan)*np.exp(sub_resid[y]) if y in sub_resid.index else np.nan
            if np.isfinite(ry): v+=frac*ry*KCAL["Rice"]
            out.append(v)
        return np.array(out)
    A=np.array([sum(shares[i]*yr_yld[i][y]*KCAL[i] for i in mains) for y in yrs])
    rr,rr_src = rice_resid(c)
    if rr is None: continue
    B=port_series("Rice", rr, f)
    C_=port_series("Rice", rr, f, add=True)
    # D: potatoes comparator
    if (c,"Potatoes") in R:
        D=np.array([sum(shares[i]*yr_yld[i][y]*KCAL[i]*(1-f) for i in mains)+
                    f*latest.get((c,"Potatoes"),np.nan)*np.exp(R[(c,"Potatoes")].get(y,0))*KCAL["Potatoes"] for y in yrs])
    else: D=None
    thr=0.8*A.mean()
    def m(x):
        p5=np.percentile(x,5)
        return [round(x.mean(),0),round(x.std(),0),round(p5,0),
                round(x[x<0.8*x.mean()].mean() if (x<0.8*x.mean()).any() else np.nan,0),
                round((x<0.8*x.mean()).mean(),3)]
    for name,x in [("A_existing",A),(f"B_rice{f}",B),(f"C_addrice{f}",C_),("D_potato",D if D is not None else np.array([np.nan]))]:
        rows_port.append([c,name,rr_src or "",len(yrs)]+m(x))
    # joint failure: wheat vs rice residuals, lower-tail dependence
    w=R[(c,"Wheat")]
    yrs2=sorted(set(w.index)&set(rr.index))
    if len(yrs2)>=12:
        co=np.corrcoef(w[yrs2].values, rr[yrs2].values)[0,1]
        jt=((w[yrs2]<-0.15)&(rr[yrs2]<-0.15)).mean()
        rows_dep.append([c,rr_src or "own",len(yrs2),round(co,3),round(jt,3)])

pd.DataFrame(rows_port,columns=["country","scenario","rice_source","n_years","mean_kcalha","sd","p5","ES_below_0.8mean","P_shortfall"]).to_csv(
    os.path.join(OUT,"RICE_PORTFOLIO_SCENARIOS.csv"),index=False)
pd.DataFrame(rows_dep,columns=["country","rice_source","n_years","wheat_rice_resid_corr","P_joint_lt_-15pct"]).to_csv(
    os.path.join(OUT,"CROP_FAILURE_DEPENDENCE.csv"),index=False)
print("done", len(rows_port), len(rows_dep))
