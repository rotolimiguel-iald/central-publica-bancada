from pathlib import Path
import datetime,json,subprocess,sys,time
BASE=Path(__file__).resolve().parent
OUT=BASE/'COMPACT_LOCALITY_AFTER_PAIRS_R1.json'
assert not OUT.exists()
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
parent=BASE/'COMPACT_SPACELIKE_CHAIN_R4.json'
print(json.dumps({'wait':str(parent)}),flush=True)
while not parent.exists():time.sleep(15)
r=json.loads(parent.read_bytes())
if not r['rows'] or r['rows'][-1]['exit']!=0 or r['rows'][-1]['source']!='PhysicalCompactSpacelikeR7.lean':
 code=1;status='REFUSED_FAILED_PARENT'
else:
 code=subprocess.call([sys.executable,'-B','-X','utf8',str(BASE/'build_orbital_stream_r4.py'),'PhysicalCompactNetLocalityR2.lean'],cwd=BASE)
 status='COMPLETED' if code==0 else 'FAILED'
result={'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parent':str(parent),'source':'PhysicalCompactNetLocalityR2.lean','exit':code,'status':status,'production_modified':False}
with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(result),flush=True)
raise SystemExit(code)
