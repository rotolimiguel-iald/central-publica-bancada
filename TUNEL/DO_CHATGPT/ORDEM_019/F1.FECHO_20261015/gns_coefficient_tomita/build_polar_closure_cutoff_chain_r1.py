from pathlib import Path
import datetime,json,subprocess,sys
BASE=Path(__file__).resolve().parent
OUT=BASE/'POLAR_CLOSURE_CUTOFF_CHAIN_R1.json'
assert not OUT.exists()
rows=[]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
parent=BASE/'attempts/20261016T104658_597906Z/RECEIPT.json'
r=json.loads(parent.read_bytes())
assert r['exit_code']==0 and r['readonly_dependencies_unchanged']
for name in ['CanonicalFockPolarRightClosureR10.lean','CanonicalFockPolarRightCutoffOrderR10.lean']:
 code=subprocess.call([sys.executable,'-B','-X','utf8',str(BASE/'build_coefficient_stream_r4.py'),name],cwd=BASE)
 rows.append({'source':name,'exit':code})
 if code:break
result={'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'production_modified':False}
with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(result),flush=True)
raise SystemExit(rows[-1]['exit'])
