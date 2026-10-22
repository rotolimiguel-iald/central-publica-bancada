"""Single-thread public metadata/document fetch; never follow data/posterior/strain links."""
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from urllib.error import HTTPError
import hashlib,json,sys,time
B=Path(__file__).resolve().parents[2]
CACHE=B/'cache/e0_metadata';CACHE.mkdir(parents=True,exist_ok=True)
url,name=sys.argv[1:3]
if Path(name).name!=name or any(s in url.lower() for s in ['.hdf5','.h5','.gwf','.tar.gz','.npz']):raise ValueError('Only metadata/documents')
p=CACHE/name;receipt=p.with_name(p.name+'.receipt.json')
if p.exists() or receipt.exists():raise FileExistsError(p)
started=datetime.now(timezone.utc).isoformat();tick=time.perf_counter()
req=Request(url,headers={'User-Agent':'IALD-E0-metadata-review/1.0 (read-only public metadata)','Accept':'application/json' if name.endswith('.json') else '*/*'})
try:
    response=urlopen(req,timeout=45)
except HTTPError as error:response=error
with response as r:
    raw=r.read(20_000_001)
    if len(raw)>20_000_000:raise ValueError('Document exceeds bounded fetch')
    meta=dict(requested_url=url,final_url=r.geturl(),status=r.status,content_type=r.headers.get('Content-Type'),
        etag=r.headers.get('ETag'),last_modified=r.headers.get('Last-Modified'),server_date=r.headers.get('Date'))
with p.open('xb') as f:f.write(raw)
if p.read_bytes()!=raw:raise ValueError('Archive bytes differ')
meta.update(started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),elapsed_s=time.perf_counter()-tick,
    bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),path=str(p.relative_to(B)),
    scope='Public metadata or primary documentation only; not posterior/strain data',code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
with receipt.open('xb') as f:f.write((json.dumps(meta,indent=2,ensure_ascii=False)+'\n').encode())
print(json.dumps(meta))
if meta['status']!=200:sys.exit(2)
