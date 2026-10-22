"""Archive located primary metadata and list the small pSEOB package, no execution."""
from pathlib import Path
from datetime import datetime,timezone
import urllib.request,hashlib,json,tarfile
ROOT=Path(__file__).resolve().parents[1];target=ROOT/'cache/public/DCC_P2600130_v1';target.mkdir(exist_ok=True)
urls=[('release.html','https://dcc.ligo.org/LIGO-P2600130/public'),('gwtc4_gwosc.html','https://gwosc.org/GWTC-4.0/'),('zenodo_paperII.html','https://zenodo.org/records/21403342'),('pSEOBNR.tar.gz','https://dcc.ligo.org/public/0206/P2600130/001/pSEOBNR.tar.gz')]
rows=[]
for name,url in urls:
    p=target/name
    if p.exists():raise FileExistsError(p)
    req=urllib.request.Request(url,headers={'User-Agent':'TGL-research-reproducibility/013bis'})
    with urllib.request.urlopen(req,timeout=120) as r:
        headers=dict(r.headers);raw=r.read();final=r.url
    if name.endswith('.tar.gz') and (not raw.startswith(b'\x1f\x8b') or len(raw)>30_000_000):raise ValueError('Unexpected archive')
    tmp=p.with_suffix('.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise ValueError('Write mismatch')
    tmp.replace(p)
    row=dict(url=url,final_url=final,path=str(p.relative_to(ROOT)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),headers=headers)
    if name.endswith('.tar.gz'):
        with tarfile.open(p,'r:gz') as tf:
            row['members']=[dict(name=m.name,bytes=m.size,regular=m.isfile(),mtime_utc=datetime.fromtimestamp(m.mtime,timezone.utc).isoformat()) for m in tf]
        row['license']='CC-BY-4.0, unless otherwise specified; release.html primary statement'
        row['content_read']='Archive directory only; no posterior values read'
    rows.append(row);print(name,len(raw),row['sha256'],flush=True)
out=dict(utc=datetime.now(timezone.utc).isoformat(),status='GWTC4_TGR_III_RELEASE_LOCATED__CORRECTION_TO_SEARCH_NOT_FOUND',rows=rows,
 limitations=['HTTP Last-Modified and archive mtime are not independently certified publication dates','No new posterior values inspected in this receipt','Paper II Zenodo release is a different dataset'])
p=ROOT/'bis/F2_GWTC4_RELEASE_SEARCH.json'
with p.open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2)
print('members',[(r['name'],r['bytes']) for r in rows[-1]['members'][:20]])
