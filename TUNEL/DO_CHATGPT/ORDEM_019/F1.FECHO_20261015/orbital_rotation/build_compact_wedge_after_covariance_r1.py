from pathlib import Path
import datetime,json,subprocess,sys,time
BASE=Path(__file__).resolve().parent
OUT=BASE/'COMPACT_WEDGE_AFTER_COVARIANCE_R1.json'
assert not OUT.exists()
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
parent=BASE/'attempts/20261016T105021_400439Z/RECEIPT.json'
print(json.dumps({'wait':str(parent)}),flush=True)
while not parent.exists():time.sleep(15)
r=json.loads(parent.read_bytes())
if r['exit_code']!=0 or not r['readonly_dependencies_unchanged']:
 code=1;status='REFUSED_FAILED_PARENT'
else:
 code=subprocess.call([sys.executable,'-B','-X','utf8',str(BASE/'build_orbital_stream_r4.py'),'PhysicalCompactWedgeComparisonR1.lean'],cwd=BASE)
 status='COMPLETED' if code==0 else 'FAILED'
result={'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parent':str(parent),'source':'PhysicalCompactWedgeComparisonR1.lean','exit':code,'status':status,'production_modified':False}
with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(result),flush=True)
raise SystemExit(code)
