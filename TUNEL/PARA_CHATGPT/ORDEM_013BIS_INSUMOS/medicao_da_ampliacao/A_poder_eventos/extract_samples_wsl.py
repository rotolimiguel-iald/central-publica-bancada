"""Frente A - extracao SO-LEITURA das amostras posteriores por evento (WSL, h5py).
Le: GWTC-5.0 pSEOB metafiles (33) + GWTC-3 rin h5 (6 so-antigos). Escreve npz+json no scratch.
Nada e escrito na pasta da bancada."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'; os.environ['OMP_NUM_THREADS']='1'
import json, hashlib, sys, time
import numpy as np, h5py
SRC='/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN'
OUT='/mnt/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/ordem013/bis/medir/A_poder_eventos'
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<22),b''): h.update(b)
    return h.hexdigest()
rng=np.random.default_rng(20260922)
THIN=4000
def summarize(ev,cat,path,label,s,spin_name,mass_name):
    df=np.asarray(s['domega220'],float); dt=np.asarray(s['dtau220'],float)
    spin=np.asarray(s[spin_name],float); mass=np.asarray(s[mass_name],float); z=np.asarray(s['redshift'],float)
    n=len(dt)
    q=lambda a:[float(x) for x in np.quantile(a,[.05,.16,.5,.84,.95])]
    idx=rng.choice(n,min(THIN,n),replace=False)
    return dict(event=ev,catalog=cat,file=os.path.relpath(path,SRC),file_sha256=sha(path),label=label,N=int(n),
        spin_field=spin_name,mass_field=mass_name,
        dtau220=dict(mean=float(dt.mean()),std=float(dt.std(ddof=1)),q05_16_50_84_95=q(dt)),
        df220=dict(mean=float(df.mean()),std=float(df.std(ddof=1)),q05_16_50_84_95=q(df)),
        corr_df_dtau=float(np.corrcoef(df,dt)[0,1]),
        spin=dict(median=float(np.median(spin)),std=float(spin.std(ddof=1)),q05_16_50_84_95=q(spin)),
        mass_detector=dict(median=float(np.median(mass)),std=float(mass.std(ddof=1)),q05_16_50_84_95=q(mass)),
        redshift=dict(median=float(np.median(z)),q05_16_50_84_95=q(z)),
        dtau440_std=float(np.std(s['dtau440'])) if 'dtau440' in s.dtype.names else None
        ), dict(df=df[idx],dt=dt[idx],spin=spin[idx],mass=mass[idx],z=z[idx])
rows=[]; thin={}
schema=json.load(open(f'{SRC}/C4_CATALOG_SCHEMA.json'))
for r in schema['rows']:
    p=f'{SRC}/cache/public/21454847/extracted/pSEOB/metafiles/{r["filename"]}'
    with h5py.File(p,'r') as h:
        s=h[r['label']]['posterior_samples'][()]
    row,th=summarize(r['event'],'GWTC5.0',p,r['label'],s,'final_spin_non_evolved','final_mass_non_evolved')
    if row['file_sha256']!=r['sha256']: row['SHA_MISMATCH_VS_SCHEMA']=True
    rows.append(row); thin[r['event']]=th; print(row['event'],row['N'],round(row['dtau220']['std'],4),flush=True)
g3=json.load(open(f'{SRC}/C4_GWTC3_220.json'))
older=set(g3['duplicate_reconciliation']['older_only'])
for r in g3['rows']:
    if r['event'] not in older: continue
    p=f'{SRC}/cache/public/17461225/extracted/{r["legacy_member"]}'
    with h5py.File(p,'r') as h:
        s=h[r['label']+'/posterior_samples'][()]
    sn='final_spin_non_evolved' if 'final_spin_non_evolved' in s.dtype.names else 'final_spin'
    mn='final_mass_non_evolved' if 'final_mass_non_evolved' in s.dtype.names else 'final_mass'
    row,th=summarize(r['event'],'GWTC3_only',p,r['label'],s,sn,mn)
    rows.append(row); thin[r['event']]=th; print(row['event'],row['N'],round(row['dtau220']['std'],4),flush=True)
json.dump(dict(generated=time.strftime('%Y-%m-%dT%H:%M:%S'),thin_per_event=THIN,rows=rows),open(f'{OUT}/samples_summary.json','w'),indent=1)
np.savez_compressed(f'{OUT}/samples_thin.npz',**{f'{k}__{f}':v for k,d in thin.items() for f,v in d.items()})
print('DONE',len(rows))
