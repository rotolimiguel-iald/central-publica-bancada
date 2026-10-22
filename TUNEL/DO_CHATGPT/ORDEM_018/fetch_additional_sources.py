from pathlib import Path
import sys,json,time,urllib.request,hashlib
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from audit_inputs import safe_write,save_json,file_info
base='https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/'
jobs=[('pantheon_readme',base+'README',None),('pantheon_table',base+'Pantheon%2BSH0ES.dat','Pantheon+SH0ES.dat'),('pantheon_cov',base+'Pantheon%2BSH0ES_STAT%2BSYS.cov','pantheon_covariance.dat'),('siren_o4b','https://arxiv.org/abs/2605.27227',None),('siren_hosts','https://arxiv.org/abs/2609.04991',None)]
def fetch(job):
 name,url,local=job;t=time.perf_counter();req=urllib.request.Request(url,headers={'User-Agent':'IALD-scientific-source-audit/1.0'})
 try:
  with urllib.request.urlopen(req,timeout=45) as response: raw=response.read(); final=response.url
  dst=ROOT/'fontes_publicas'/(name+('.txt' if name.startswith('pantheon') else '.html'))
  safe_write(dst,raw);info=file_info(dst);info.update(url=url,final_url=final,retrieved_at=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.perf_counter()-t)
  if local:
   prior=ROOT/'reproducao_fase5'/local;info['local_copy']=file_info(prior);info['bytes_match_local']=prior.read_bytes()==raw
  return info
 except Exception as e:return {'name':name,'url':url,'error':str(e),'elapsed_seconds':time.perf_counter()-t}
with ThreadPoolExecutor(max_workers=5) as pool:results=list(pool.map(fetch,jobs))
save_json(ROOT/'FONTES_PUBLICAS_ADICIONAIS.json',results)
print(json.dumps(results,ensure_ascii=False))
