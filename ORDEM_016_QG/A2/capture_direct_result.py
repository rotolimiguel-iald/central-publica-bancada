from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys
folder=Path(__file__).resolve().parent
name=sys.argv[1]
assert name in ('a23_kimi_direct','a23_mimo_medium','a23_gemini_low')
out=folder.parents[1]/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc)
d=json.loads((folder/(name+'_stdout.json')).read_bytes())
assert d['status'] in ('failed','result_ready','completed','cancelled','interrupted'),d['status']
r=d.get('result') or {};u=r.get('usage') or {}
entry={'ts':now.isoformat(),'event':'direct_terminal','alvo':'A-2','ramo':'A-2.3.a',
       'provedor':d['execution_constraints']['required_provider'],'role':d['execution_constraints']['role'],
       'request_id':d['request_id'],'execution_task_id':d['id'],'job_id':None,
       'question_sha256':hashlib.sha256(d['prompt'].encode()).hexdigest(),
       'answer_sha256':hashlib.sha256(r['text'].encode()).hexdigest() if r.get('text') else None,
       'tokens_in':u.get('input_tokens'), 'tokens_out':u.get('output_tokens'),
       'tokens_thinking_reported':u.get('thinking_tokens'),'tokens_total_reported':u.get('total_tokens'),
       'tokens_cache':u.get('cache_read_tokens'),'custo_usd':u.get('cost_usd'),
       'elapsed_seconds':r.get('elapsed_seconds'),'desfecho':d['status'],'error':d.get('error'),
       'raw_usage':u or None,'verification':r.get('verification'),
       'canonical_memory':{k:(r.get('canonical_memory') or {}).get(k) for k in
                           ['generation','packet_sha256','context_bytes','coverage','memory_mode']}}
ledger=out/'LEDGER_016.jsonl';old=ledger.read_bytes();rows=[json.loads(x) for x in old.splitlines() if x]
assert not any(x.get('event')=='direct_terminal' and x.get('execution_task_id')==d['id'] for x in rows)
backup=ledger.with_name(ledger.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f'))
with backup.open('xb') as f:f.write(old)
assert backup.read_bytes()==old
new=old+(json.dumps(entry,ensure_ascii=False)+'\n').encode();temp=ledger.with_name(ledger.name+'.tmp')
with temp.open('xb') as f:f.write(new)
assert temp.read_bytes()==new;temp.replace(ledger)
if r.get('text'):
    p=folder/(name+'_answer.md');assert not p.exists()
    raw=('[DECLARADO — resposta do provedor; conferir com artefatos/compilador]\n\n'+r['text']).encode()
    t=p.with_name(p.name+'.tmp');t.write_bytes(raw);assert t.read_bytes()==raw;t.rename(p)
print(json.dumps(entry,ensure_ascii=False))
