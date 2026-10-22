from pathlib import Path
import datetime,json,subprocess,sys,time
BASE=Path(__file__).resolve().parent
OUT=BASE/'COMPACT_SPACELIKE_CHAIN_R3.json'
assert not OUT.exists()
rows=[]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
for parent,name in [
 ('20261016T104225_594165Z','PhysicalSymplecticPairingR6.lean'),
 ('20261016T103202_691262Z','PhysicalCompactSpacelikeR6.lean')]:
 p=BASE/'attempts'/parent/'RECEIPT.json'
 print(json.dumps({'wait':str(p),'source':name}),flush=True)
 while not p.exists():time.sleep(15)
 r=json.loads(p.read_bytes())
 if r['exit_code']!=0 or not r['readonly_dependencies_unchanged']:
  rows.append({'source':name,'status':'REFUSED_FAILED_PARENT','exit':1});break
 code=subprocess.call([sys.executable,'-B','-X','utf8',str(BASE/'build_orbital_stream_r4.py'),name],cwd=BASE)
 rows.append({'source':name,'exit':code})
 if code:break
result={'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'production_modified':False}
with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(result),flush=True)
raise SystemExit(rows[-1]['exit'])
