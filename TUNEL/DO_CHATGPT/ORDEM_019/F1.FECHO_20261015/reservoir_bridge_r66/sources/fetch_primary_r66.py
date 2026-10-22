"""Public source custody only; no scientific computation or mission mutations."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, urllib.request, importlib.util

HERE=Path(__file__).resolve().parent
DEST=HERE/'literature'
DEST.mkdir(exist_ok=True)
sources=[
 ('engel_nagel.pdf','https://www.math.uni-tuebingen.de/de/forschung/agfa/members/engel-nagel_one-parameter-semigroups.pdf'),
 ('attal_pautrat_0311002v2.html','https://arxiv.org/abs/math-ph/0311002v2'),
 ('attal_pautrat_0402064v1.html','https://arxiv.org/abs/math/0402064v1'),
]
rows=[]
for name,url in sources:
 row={'url':url,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'IALD source custody/1.0'}),timeout=35) as response:
   data=response.read(15000000)
   row.update(status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type'))
  p=DEST/name
  tmp=DEST/(name+'.tmp')
  with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  assert tmp.stat().st_size==len(data)
  if p.exists():raise FileExistsError(str(p))
  os.rename(tmp,p)
  row.update(path=str(p),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
 except Exception as e:row.update(error=type(e).__name__+': '+str(e))
 rows.append(row)
p=HERE/'PRIMARY_FETCH_R66.json'
with p.open('xb') as f:f.write((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'sources':rows,'pdf_packages':{x:bool(importlib.util.find_spec(x)) for x in ['pypdf','fitz','pdfplumber']}},ensure_ascii=False))
