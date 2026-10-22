from pathlib import Path
import sys,json,urllib.request,time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from audit_inputs import safe_write,save_json,file_info
jobs=[('act_dr6_v2','https://arxiv.org/html/2503.14454v2'),('h0dn','https://arxiv.org/html/2510.23823'),('cmb_s4_status','https://cmb-s4.org/')]
def fetch(job):
 name,url=job;t=time.perf_counter()
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'IALD-scientific-source-audit/1.0'}),timeout=40) as r:raw=r.read();final=r.url
  dst=ROOT/'fontes_publicas'/(name+'.html');safe_write(dst,raw)
  return dict(file_info(dst),url=url,final_url=final,retrieved_at=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.perf_counter()-t)
 except Exception as e:return dict(name=name,url=url,error=str(e),elapsed_seconds=time.perf_counter()-t)
with ThreadPoolExecutor(max_workers=3) as pool:out=list(pool.map(fetch,jobs))
save_json(ROOT/'FONTES_ATUALIZACAO_F0.json',out)
print(json.dumps(out,ensure_ascii=False))
