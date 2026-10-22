"""Finish metadata after backup-name collision; never rerun scientific tests."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
H=Path(__file__).resolve().parent; O=H.parents[1]/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replace(p,b):
 old=p.read_bytes(); tag=now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex
 bak=p.with_name(p.name+'.bak_'+tag);bak.write_bytes(old);assert bak.read_bytes()==old
 tmp=p.with_name(p.name+'.tmp_'+tag);tmp.write_bytes(b);assert tmp.read_bytes()==b and b;tmp.replace(p)
def append(p,s):replace(p,p.read_bytes()+s.encode())
m=H/'harmonic_reference_delivery/manifest.json';d=json.loads(m.read_bytes())
for r in d['artifacts']:assert sha(Path(r['path']))==r['sha256']
ledger=O/'LEDGER_016.jsonl'; rows=[json.loads(s) for s in ledger.read_text('utf-8-sig').splitlines() if s.strip()]
assert any(r.get('execution_task_id')=='023b86dd-dab0-4f17-8f78-f989d9d676fc' for r in rows)
event='A7_HARMONIC_REFERENCE_TRANSFER'
assert not any(r.get('event')==event for r in rows)
append(ledger,json.dumps(dict(at=now.isoformat(),event=event,target='A7.b',checks=d['checks'],cpu_seconds=d['cpu_seconds'],remote_call=False,manifest_sha256=sha(m),full_Q2=False))+'\n')
seen=set();cost=Decimal(0)
for r in rows:
 v=r.get('cost_estimate_usd')
 if v is None:v=r.get('cost_usd')
 if v is None:continue
 k=r.get('execution_task_id') or r.get('job_id') or r.get('request_id')
 if k and k in seen:continue
 if k:seen.add(k)
 cost+=Decimal(str(v))
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS: transferência harmônica corrigida, defeito local aplicado ao P4; {d["checks"]}checks CPU{d["cpu_seconds"]}s; custo parcial US${cost}; Q2 OPEN.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes())
c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',harmonic_reference_manifest=str(m),
 completed_this_turn=['Harmonic reference correction delivered:394 exact checks; same prescription preserved'],
 next=['Audit Fourier reply6c210ea9 and DeepSeek7df6c82e','Assemble Ward contributions before2026-09-25T20:32Z','A7c/d,A8,PartB,final still pending'],
 partial_metered_cost_usd=str(cost),own_live_processes=[],
 orchestration_update='MiMo c76366aa admitted, dispatch awaiting real-worker fingerprint; Kimi3ceb40a7 running; DeepSeek7df6c82e completed, unread locally')
replace(p,json.dumps(c,ensure_ascii=False,indent=2).encode())
note=dict(at=now.isoformat(),status='REGISTRATION_RECOVERED',
 first_failure='v1 compared full result to deliberately abridged log; no artifact written',
 second_failure='v2 reused backup suffix for second ledger append; first append and delivery succeeded',
 recovery='Only remaining metadata appended; unique byte-backup suffix; scientific artifacts untouched',
 manifest_sha256=sha(m),checks=d['checks'],cpu_seconds=d['cpu_seconds'],partial_cost=str(cost))
q=H/'harmonic_reference_delivery/registration_recovery.json';assert not q.exists()
t=q.with_suffix('.tmp');t.write_bytes(json.dumps(note,ensure_ascii=False,indent=2).encode());assert t.stat().st_size;t.replace(q)
print(json.dumps(note))
