"""Capture old diagnostic jobs without interrupting or promoting them."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parents[1]
stamp=datetime.now(timezone.utc)
tag=stamp.strftime('%Y%m%dT%H%M%SZ')
out=ROOT/'bis'/('F0_SNAPSHOT_'+tag+'.json')
command=['wsl.exe','-e','sh','-c',
         'pgrep -af "[r]un_real_phase_importance|[r]un_continuous_source_curves"; free -b']
run=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
if run.returncode:
    raise RuntimeError(repr(run.stderr)+repr(run.stdout))
source=ROOT/'cache/source_evidence'
records=[]
for folder in [source/'phase_real_refined/IMRPhenomXPHM_seed130972_N32768',
               source/'continuous_source_curves/IMRPhenomXPHM_seed130972_N32768',
               source/'continuous_source_curves/SEOBNRv4HM_seed130942_N16384',
               source/'phase_native_repeat/SEOBNRv4HM_seed130942_N16384']:
    for name in ('START.json','PROGRESS.json','RESULT.json','AUDIT_RATE.json','EVALUATIONS_COMPLETE.json'):
        path=folder/name
        if path.exists():
            data=path.read_bytes()
            records.append(dict(path=str(path),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),
                                mtime_utc=datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat(),
                                content=json.loads(data)))
opening=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'
result=dict(status='DIAGNOSTIC_JOBS_RUNNING__F0_NOT_CLOSED',utc=stamp.isoformat(),
            statement='nenhum produto destes processos entra em veredito nem no portão',
            compute_budget_hours_charged=0,command=command,
            process_and_memory_snapshot=run.stdout.decode('utf-8'),records=records,
            opening_sha256=hashlib.sha256(opening.read_bytes()).hexdigest(),
            not_done=['Final checksum inventory of completed chunks at end or termination',
                      'Proof of empty process list before E3.1', 'RAM snapshot after old jobs end'])
with out.open('x',encoding='utf-8') as stream:
    json.dump(result,stream,ensure_ascii=False,indent=2)
    stream.write('\n')
print(out)
print('sha256',hashlib.sha256(out.read_bytes()).hexdigest())
for row in records:
    v=row['content']
    if Path(row['path']).name in ('PROGRESS.json','AUDIT_RATE.json'):
        print(row['path'],{key:v[key] for key in ('done','completed','valid_draws','status','passed_precision','date_utc') if key in v})
