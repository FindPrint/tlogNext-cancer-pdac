import numpy as np, pandas as pd, tarfile, json
BASE="/home/hatch/workspace/runs/pdac-v6"
with tarfile.open(f"{BASE}/data/tcga_paad_rsem.tar.gz") as tf:
    m=[x for x in tf.getmembers() if x.name.endswith('.data.txt')][0]
    df=pd.read_csv(tf.extractfile(m), sep='\t', index_col=0, low_memory=False)
df.index=df.index.to_series().str.split('|').str[0]; df=df[~df.index.duplicated(keep='first')]
cols=df.columns.to_series(); tc=cols[cols.str[13:15]=='01']
logmat=np.log2(df[tc].apply(pd.to_numeric,errors='coerce').dropna()+1.0)
ACINAR=["PNLIP","CTRB2","CELA3A","CTRB1","CPA1","CELA2A","CPB1","CELA3B","CLPS","CTRC","CPA2"]
ISLET=["INS","GCG","PPY","SST"]
X=np.column_stack([np.ones(len(logmat.columns)), logmat.loc[ACINAR].median(axis=0).values, logmat.loc[ISLET].median(axis=0).values])
beta,*_=np.linalg.lstsq(X, logmat.values.T, rcond=None)
resid=pd.DataFrame(logmat.values-(X@beta).T, index=logmat.index, columns=logmat.columns)
order=list(resid.loc["KRAS"].sort_values().index)
clin=pd.read_csv(f"{BASE}/data_clinical_patient.txt", sep='\t', skiprows=[1,2], dtype=str)
clin=clin.rename(columns={'#Patient Identifier':'patient','Overall Survival Status':'os_status','Overall Survival (Months)':'os_months',
 'Disease-specific Survival status':'dss_status','Months of disease-specific survival':'dss_months',
 'Progression Free Status':'pfs_status','Progress Free Survival (Months)':'pfs_months'})
for c in ['os_months','dss_months','pfs_months']:
    clin[c]=pd.to_numeric(clin[c],errors='coerce')
clin=clin[clin['os_months'].notna()].set_index('patient')
ev=clin['os_status'].astype(str).str.startswith('1')
pats=[c[:12] for c in order if c[:12] in clin.index]
order=[c for c in order if c[:12] in clin.index]
t=clin.loc[pats,'os_months'].values.astype(float); e=ev.loc[pats].values.astype(bool)
import sys; sys.path.insert(0,'/tmp')
from scipy.stats import norm
def cox(Z,t,e):
    Z=np.asarray(Z,float); t=np.asarray(t,float); e=np.asarray(e,bool)
    n,p=Z.shape; ut=np.sort(np.unique(t[e])); b=np.zeros(p)
    for _ in range(100):
        w=np.exp(Z@b-(Z@b).max()); g=np.zeros(p); h=np.zeros((p,p))
        for tt in ut:
            r=t>=tt; d=int(np.sum((t==tt)&e)); Zr=Z[r]; wr=w[r]; S0=wr.sum()
            S1=(Zr*wr[:,None]).sum(0); S2=(Zr[:,:,None]*Zr[:,None,:]*wr[:,None,None]).sum(0)
            mu=S1/S0; g+=Z[(t==tt)&e].sum(0)-d*mu; h-=d*(S2/S0-np.outer(mu,mu))
        try: s=np.linalg.solve(h,g)
        except Exception: break
        b=b-s
        if np.max(np.abs(s))<1e-10: break
    se=np.sqrt(np.diag(np.linalg.inv(-h))); return b,se,2*(1-norm.cdf(np.abs(b/se)))
def zs(v): v=np.asarray(v,float); return (v-v.mean())/v.std(ddof=0)
GENES=["KRAS","MUC16","CEACAM5","PGC","DPCR1","CLDN18"]
print("=== (a) PIÈGE : jointure naïve du CSV de flux (ordre step) avec le clinique (ordre fichier) ===")
fl=pd.read_csv(f"{BASE}/pdac_tcga_fluxes_v4.csv", index_col=0)
print("flux CSV: n lignes =", len(fl), "| index = step 0..177 (AUCUN identifiant patient)")
# appariement naïf : ligne i du CSV <-> i-ème patient du clinique dans l'ordre du fichier
clin_order=list(clin.index)
sub=clin.loc[[p for p in clin_order if p in pats]]
print("patients cliniques dans l'ordre fichier, n =", len(sub))
# on garde les 177 patients ARN, dans l'ordre du fichier clinique
pats_file=[p for p in clin_order if p in pats]
t2=clin.loc[pats_file,'os_months'].values.astype(float); e2=ev.loc[pats_file].values.astype(bool)
for g in ["MUC16","CEACAM5","PGC","DPCR1","CLDN18"]:
    z=zs(fl[g].values[:len(pats_file)])
    b,se,p=cox(z.reshape(-1,1), t2, e2)
    print(f"  {g:10s} HR brouille={np.exp(b[0]):.2f} p={p[0]:.3f}")
print("=== (b) Cox univarie sur PFS (survie sans progression) au lieu de OS ===")
pfs_t=clin.loc[pats,'pfs_months'].values.astype(float)
pfs_e=clin.loc[pats,'pfs_status'].astype(str).str.startswith('1').values
ok=~np.isnan(pfs_t); print("PFS: n =",int(ok.sum()),"evenements =",int(pfs_e[ok].sum()))
for g in GENES:
    z=zs(np.array([resid.loc[g,c] for c in order])[ok])
    b,se,p=cox(z.reshape(-1,1), pfs_t[ok], pfs_e[ok])
    print(f"  {g:10s} HR PFS={np.exp(b[0]):.2f} p={p[0]:.4f}")
print("=== (c) Cox univarie sur DSS (survie specifique) ===")
dss_t=clin.loc[pats,'dss_months'].values.astype(float)
dss_e=clin.loc[pats,'dss_status'].astype(str).str.startswith('1').values
ok=~np.isnan(dss_t); print("DSS: n =",int(ok.sum()),"evenements =",int(dss_e[ok].sum()))
for g in GENES:
    z=zs(np.array([resid.loc[g,c] for c in order])[ok])
    b,se,p=cox(z.reshape(-1,1), dss_t[ok], dss_e[ok])
    print(f"  {g:10s} HR DSS={np.exp(b[0]):.2f} p={p[0]:.4f}")
print("=== (d) HR par UNITE log2 (non standardise) — residus ===")
for g in GENES:
    v=np.array([resid.loc[g,c] for c in order]); sd=v.std(ddof=0)
    z=zs(v); b,se,p=cox(z.reshape(-1,1), t, e)
    print(f"  {g:10s} sd={sd:.3f} coef_z={b[0]:+.3f} -> HR par unite={np.exp(b[0]/sd):.2f} (vs HR par sd={np.exp(b[0]):.2f})")
