"""Add per-file licence provenance without rewriting the frozen download ledger."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,urllib.request,collections
B=Path(__file__).resolve().parents[1]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(4*2**20),b''):h.update(c)
    return h.hexdigest()
def new(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
policy=B/'cache/literature/gwosc_acknowledgement_013bis.html'
if not policy.exists():
    with urllib.request.urlopen('https://gwosc.org/acknowledgement/',timeout=40) as response:raw=response.read()
    if b'Creative Commons Attribution 4.0' not in raw:raise ValueError('Licence text absent')
    new(policy,raw)
records={}
for rid in ('17018009','21454847','17461225'):
    p=B/f'cache/public/{rid}/record.json';d=json.loads(p.read_bytes())
    records[rid]=dict(id=d['metadata']['license']['id'],source_path=str(p.relative_to(B)),source_sha256=sha(p),source_url=f'https://zenodo.org/records/{rid}')
old=B/'cache/MANIFESTO_DOWNLOADS.json';d=json.loads(old.read_bytes());rows={}
for r in d['files']:
    r=dict(r);r['path']=r['path'].replace('\\','/');rows[r['path']]=r
ex=json.loads((B/'bis/F2_CONTROL_EXTRACTION.json').read_bytes())
for a in ex['archives']:
    for r in a['files']:
        item=dict(r);item['path']=item['path'].replace('\\','/');rows.setdefault(item['path'],item)
for r in json.loads((B/'bis/F2_ARCHIVE_DOWNLOADS.json').read_bytes()):
    p=Path(r['path']);relative=p.relative_to(B).as_posix()
    rows.setdefault(relative,dict(path=relative,bytes=r['bytes'],sha256=r['sha256'],origin=r['url']))
p=B/'cache/public/DCC_P2600130_v1/pSEOBNR.tar.gz'
if p.exists():rows.setdefault(p.relative_to(B).as_posix(),dict(path=p.relative_to(B).as_posix(),bytes=p.stat().st_size,sha256=sha(p)))
missing=[];changed=[]
for key,r in rows.items():
    p=B/key
    if not p.exists():missing.append(key);r['integrity_status']='ABSENT_NOW';continue
    digest=sha(p)
    if r.get('sha256') and digest!=r['sha256']:changed.append(key);r['integrity_status']='CHANGED_FROM_PRIOR_RECEIPT';r['current_sha256']=digest
    else:r['integrity_status']='HASH_VERIFIED';r['sha256']=digest
    r['bytes_current']=p.stat().st_size
    rid=next((v for v in records if f'/{v}/' in '/'+key+'/'),None)
    if rid:r['license']=records[rid]
    elif '/gwosc/' in '/'+key+'/' or 'GWOSC' in r.get('kind',''):
        r['license']=dict(id='cc-by-4.0',source_url='https://gwosc.org/acknowledgement/',source_path=str(policy.relative_to(B)),source_sha256=sha(policy),scope='GWOSC public data policy')
    elif 'DCC_P2600130_v1' in key:
        src=B/'cache/public/DCC_P2600130_v1/release.html';r['license']=dict(id='cc-by-4.0',source_path=str(src.relative_to(B)),source_sha256=sha(src),scope='Licence declared on release page')
    else:r['license']=dict(id=None,status='NOT_ASSIGNED_BY_THIS_MANIFEST',scope='Own derived artifacts, source excerpts or other software keep their separate rights; no blanket open licence inferred')
for r in rows.values():
    r.setdefault('license',dict(id=None,status='NOT_VERIFIED_ABSENT_FILE'))
out=dict(status='ADDITIVE_PER_FILE_LICENSE_LEDGER',utc=datetime.now(timezone.utc).isoformat(),supersedes=str(old.relative_to(B)),supersedes_sha256=sha(old),records=records,files=list(rows.values()),absent=missing,changed=changed,builder_sha256=sha(Path(__file__)))
target=B/'cache/MANIFESTO_DOWNLOADS_013BIS_v2.json';new(target,(json.dumps(out,indent=2,ensure_ascii=False)+'\n').encode())
print(json.dumps(dict(files=len(rows),absent=missing,changed=changed,sha256=sha(target),licences=dict(collections.Counter(str(r['license']['id']) for r in rows.values())))))
if missing or changed:raise RuntimeError('Input discrepancies retained; inspect before declaring custody')
