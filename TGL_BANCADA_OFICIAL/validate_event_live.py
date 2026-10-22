"""End-to-end event receipt on the deployed resident bench, no scientific inference."""
import hashlib,json,statistics,time,urllib.request
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent
URL='http://127.0.0.1:18765/api/universe/'
def call(route,data=None):
 req=urllib.request.Request(URL+route, data=None if data is None else json.dumps(data).encode(),
  headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=65) as f:return json.load(f)
def run():
 last=-1
 while True:
  status=call('status')
  if status['status']!='LOADING':break
  if status['loaded_files']!=last:
   print(json.dumps({'state':status['status'],'loaded':status['loaded_files'],'total':status['total_files']}),flush=True)
   last=status['loaded_files']
  time.sleep(10)
 if status['status']!='READY':raise ValueError(status['errors'])
 meta=call('event');payload={'reading':'R-B','start_tm':10,
  'mass_source_solar':meta['reference_mass_detector_solar']/(1+meta['redshift']),
  'spin':.7,'redshift':meta['redshift'],
  'detectors':{'H1':{'amplitude':1e-21,'phase':0},'L1':{'amplitude':1e-21,'phase':0}}}
 queries=[];first=None
 for start in meta['starts_tm']:
  before=time.perf_counter();res=call('event_view',{**payload,'start_tm':start});elapsed=(time.perf_counter()-before)*1000
  assert res['load_id']==status['load_id'] and res['data_reads_since_load']==0
  assert all(c['quality']['passed'] and len(c['strain'])==410 for c in res['channels'])
  queries.append({'start_tm':start,'http_ms':elapsed,'worker_ms':res['elapsed_ms']})
  if start==10:first=res
 gr=call('event_view',{**payload,'reading':'R-GLOBAL'})
 assert all(c['gr']==c['tgl'] for c in gr['channels'])
 changed=call('event_view',{**payload,'mass_source_solar':80,'spin':.85,'redshift':.2})
 for a,b in zip(first['channels'],changed['channels']):
  assert a['strain']==b['strain'] and a['time_s']==b['time_s'] and a['gr']!=b['gr']
 final=call('status')
 receipt={'status':'DEPLOYED_EVENT_UI_BACKEND_VALIDATED_NOT_INFERENCE','utc':datetime.now(timezone.utc).isoformat(),
  'load_id':status['load_id'],'event':meta['event'],'resident':{k:final[k] for k in ['status','loaded_files','total_files','resident_bytes','worker_rss_bytes','worker_swap_bytes']},
  'queries':queries,'r_global_matches_gr':True,'parameters_change_model_not_data':True,
  'physical_gate':first['physical_gate'],'example':first,'metadata':meta,
  'ui_checked_separately':True,
  'implementation_hashes':{str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'app.py',HERE/'resident_bridge.py',HERE/'event_sources.py',HERE/'adapters/event_runtime.py',HERE/'adapters/resident_worker.py',HERE/'static/universe.js',HERE/'static/universe.html',HERE/'static/universe.css']}}
 p=HERE/'state'/('validation_event_live_'+status['load_id']+'.json');raw=json.dumps(receipt,ensure_ascii=False,allow_nan=False,indent=2).encode()
 t=p.with_suffix('.new');t.write_bytes(raw);assert t.stat().st_size==len(raw);t.replace(p)
 print(json.dumps({'receipt':str(p),'resident':receipt['resident'],'queries':queries,'controls':'passed'},ensure_ascii=False),flush=True)
if __name__=='__main__':run()
