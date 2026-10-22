"""Consume the existing modular-identification attempt exactly once, then build two fixed consumers.
No retries, no provider calls, no production writes. An unsuccessful parent stops the chain.
"""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time
BASE=Path(__file__).resolve().parent
PARENT=BASE/'attempts/20261016T102125_186958Z/RECEIPT.json'
OUT=BASE/'FRAME_WEDGE_CHAIN_R3.json'
assert not OUT.exists()
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
print(json.dumps({'phase':'waiting_for_existing_physical_opposite_wedge_attempt','receipt':str(PARENT),'start_utc':start}),flush=True)
while not PARENT.exists(): time.sleep(15)
r=json.loads(PARENT.read_bytes())
assert r['exit_code']==0 and r['readonly_dependencies_unchanged'], 'Parent failed; chain refused'
parent_source=BASE/'PhysicalOppositeWedgeR4.lean'
assert hashlib.sha256(parent_source.read_bytes()).hexdigest()==r['source']['sha256']
rows=[]
for name in ['PhysicalFrameWedgeLocalityR2.lean']:
    print(json.dumps({'phase':'compiling','source':name}),flush=True)
    code=subprocess.call([sys.executable,'-B','-X','utf8',str(BASE/'build_orbital_stream_r4.py'),name],cwd=BASE)
    rows.append({'source':name,'builder_exit':code})
    if code: break
result={'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'parent_receipt':str(PARENT),'rows':rows,'production_modified':False,'new_provider_calls':0}
with OUT.open('x',encoding='utf-8',newline='\n') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(result,ensure_ascii=False),flush=True)
raise SystemExit(rows[-1]['builder_exit'])
