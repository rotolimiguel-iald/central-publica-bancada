"""Project the same scientific review within the existing transport prompt cap."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
HERE=Path(__file__).resolve().parent;CHAT=HERE.parents[1];BASE=CHAT/'IALD_ORQUESTRACAO_20260923'
DEST=HERE/'orchestration_primitive_v4';DEST.mkdir(exist_ok=True)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def new(path,o):
    b=json.dumps(o,ensure_ascii=False,indent=2).encode()
    if path.exists():assert path.read_bytes()==b;return
    t=path.with_name(path.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert b and t.read_bytes()==b;t.replace(path)
prior=HERE/'orchestration_primitive_v3/kimi_a7_metric_primitive_submit.json';old=json.loads(prior.read_bytes())
failed=dict(at=datetime.now(timezone.utc).isoformat(),rc=1,stage='local_preview_before_any_submission',
    exception='ValueError: Informe uma tarefa de 1 a 24000 caracteres.',
    payload_sha256=sha(prior),prompt_chars=len(old['prompt']),remote_calls=0,
    next='Project exact bounded source excerpts, keeping same request ID and scientific question; no infrastructure change')
new(HERE/'orchestration_primitive_v3/LOCAL_PREVIEW_FAILURE.json',failed)
question=old['prompt'].split('\nSOURCE ',1)[0]
question=question.replace('Esta v3','Esta v4').replace('mesmo request_id/posição/restrições.','mesmo request_id/posição/restrições. A v3 excedeu o limite LOCAL de24000 caracteres\nna prévia e não foi submetida. Este pacote é projeção textual parcial rastreável;\no corpus completo não é alegado. A memória canônica comum permanece no adaptador.')
specs=[(HERE/'bv_gradient_fit/DERIVACAO_COMPLETA_PRINCIPAL.md',1,None),
       (HERE/'bv_gradient_fit/results.json',1,None),(HERE/'quadratic_metric_engine.py',1,None),
       (HERE/'ghost_primitive_engine.py',1,None),(HERE/'bv_gradient_engine.py',1,None),
       (HERE/'constant_ghost_completion/results.json',60,None),
       (HERE/'shifted_antifield/DERIVACAO_DESLOCAMENTO.md',1,None),
       (CHAT/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md',75,112)]
parts=[question];receipts=[]
for path,start,end in specs:
    lines=path.read_text('utf-8-sig').splitlines();end=len(lines) if end is None else end
    assert 1<=start<=end<=len(lines)
    h=sha(path)
    parts.append(f'\nSOURCE {path.relative_to(CHAT)}; sha256={h}; lines={start}-{end}\n'+
                 '\n'.join(f'{i}: {lines[i-1]}' for i in range(start,end+1)))
    receipts.append(dict(path=str(path),sha256=h,start=start,end=end))
prompt='\n'.join(parts);assert len(prompt)<=24000,len(prompt)
payload=dict(old);payload['prompt']=prompt;path=DEST/'kimi_a7_metric_primitive_submit.json';new(path,payload)
new(DEST/'kimi_a7_metric_primitive_receipt.json',dict(at=datetime.now(timezone.utc).isoformat(),
    request_id=old['request_id'],origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',
    status='V4_PREPARED_HELD_UNSUBMITTED',prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),
    sources=receipts,supersedes_payload=str(prior),supersedes_sha256=sha(prior)))
sys.path.insert(0,str(BASE))
from iald_orchestrator.runtime import Runtime
runtime=Runtime(recover=False);preview=runtime.preview(prompt,payload['execution_constraints'])
new(DEST/'kimi_a7_metric_primitive_preview.json',preview)
assert preview.get('selected')=='kimi',preview.get('selected')
cat=json.loads((HERE/'orchestration_primitive_v2/prepared_units.json').read_bytes())
cat[0].update(payload=str(path),payload_sha256=sha(path),prompt_chars=len(prompt),selected='kimi',
    status='V4_REPLACES_HELD_UNSUBMITTED_PAYLOAD',supersedes_payload=str(prior),supersedes_sha256=sha(prior))
new(DEST/'prepared_units.json',cat)
print(json.dumps(dict(catalog=str(DEST/'prepared_units.json'),request_id=old['request_id'],selected='kimi',
    prompt_chars=len(prompt),payload_sha256=sha(path),remote_calls=0),ensure_ascii=False))
