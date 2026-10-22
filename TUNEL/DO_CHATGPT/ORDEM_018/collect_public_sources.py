"""Archive primary scientific HTML; no fit or verdict and no confidential input."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from audit_inputs import ROOT, save_json, safe_write, file_info

SOURCES = [
 ('planck_2018_v4','https://arxiv.org/abs/1807.06209v4'),
 ('cchp_2025_v3','https://arxiv.org/abs/2408.06153v3'),
 ('tdcosmo_2025_v4','https://arxiv.org/abs/2506.03023v4'),
 ('sh0es_2022','https://arxiv.org/abs/2112.04510'),
]
def fetch(item):
 name,url=item
 path=ROOT/'fontes_publicas'/(name+'.html')
 if path.exists():
  return dict(file_info(path),url=url,retrieval='EXISTING_BYTES_PRESERVED')
 try:
  with urlopen(Request(url,headers={'User-Agent':'IALD-scientific-provenance/1.0'}),timeout=25) as response:
   raw=response.read(3000000)
   assert b'<html' in raw.lower(), 'Not HTML'
   final_url=response.url
  safe_write(path,raw)
  return dict(file_info(path),url=url,final_url=final_url,retrieved_at=datetime.now(timezone.utc).isoformat(),status='ARCHIVED_PRIMARY_HTML')
 except Exception as error:
  return dict(url=url,status='FAILED_VISIBLE',error=str(error))
if __name__=='__main__':
 rows=list(ThreadPoolExecutor(max_workers=4).map(fetch,SOURCES))
 save_json(ROOT/'FONTES_PUBLICAS.json',{'sources':rows,'scope':'Primary metadata and published uncertainty; no new composite verdict.'})
 print(rows)
