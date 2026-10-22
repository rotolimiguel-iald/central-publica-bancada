"""Register the authorized A-2.5.c review once; no model execution here."""
from pathlib import Path
import hashlib
import json
import uuid
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now
from iald_orchestrator.transport import Transport

base=Path(__file__).resolve().parent
root=base.parent/'ORDEM_016_QG/A2'
payload_file=root/'a25c_kimi_review_submit.json'
if payload_file.exists():
    payload=json.loads(payload_file.read_bytes())
else:
    manifest=json.loads((root/'unbounded_transform_manifest.json').read_bytes())
    parts=['''Revisão cética delimitada ORDEM_016 A-2.5.c. Pergunta única: as hipóteses de NormalizedGraphWitness realmente identificam B com D(I+D²)^(-1/2), com domínio completo e núcleo/gap corretos, e qual passagem exata ainda falta para a existência da testemunha para D densamente definido auto-adjunto arbitrário? Procure circularidade, confusão positivo/auto-adjunto e limite inferior versus gap ótimo. Se sugerir fechamento da existência, dê cadeia matemática concreta reutilizando os lemas V350 citados; não introduza hipótese equivalente à conclusão. Não anuncie solução física. Os quatro arquivos abaixo foram auditados pela bancada de origem conforme manifesto; você não executa Lean nem acessa disco. Distinguir DECLARADO, DERIVED e OPEN. Não ampliar escopo. A tentativa ClosedLinearGraphResolvent.lean está fora desta revisão.

FONTES CIENTÍFICAS DO PEDIDO:''']
    for artifact in manifest['artifacts']:
        path=root/artifact['source'];raw=path.read_bytes()
        assert path.suffix=='.lean' and hashlib.sha256(raw).hexdigest()==artifact['source_sha256']
        parts.append('\nARQUIVO '+path.name+' SHA256 '+hashlib.sha256(raw).hexdigest()+'\n'+raw.decode('utf-8')+'\nFIM DO ARQUIVO')
    parts.append('\nESTATUTO DA BANCADA: '+manifest['status']+'\nLACUNAS: '+json.dumps(manifest['pending'],ensure_ascii=False))
    prompt='\n'.join(parts)
    assert len(prompt)<=24000
    payload={'operation':'submit','request_id':str(uuid.uuid4()),'prompt':prompt,
             'execution_constraints':dict(mission_id='ORDEM_016',branch_id='A-2.5.c',lemma_id='normalized_graph_transform_scope',role='skeptic',required_provider='kimi',max_calls=1)}
    save_json(payload_file,payload)
transport=Transport()
preview=transport.coordination.runtime.preview(payload['prompt'],payload['execution_constraints'])
assert preview['selected']=='kimi',preview['status']
save_json(root/'a25c_kimi_review_preview.json',preview)
job=transport.submit(payload['prompt'],payload['request_id'],payload['execution_constraints'])
save_json(base/'state/handoffs'/f"{job['id']}_registered.json",job)
ledger=base.parent/'TUNEL/DO_CHATGPT/LEDGER_016.jsonl'
old=ledger.read_bytes()
if payload['request_id'].encode() not in old:
    entry={'ts':utc_now(),'event':'coordination_registered','alvo':'A-2','ramo':'A-2.5.c','provedor':'kimi','request_id':payload['request_id'],'job_id':job['id'],'question_sha256':hashlib.sha256(payload['prompt'].encode()).hexdigest(),'desfecho':job['stage'],'provider_calls_observed':0,'tokens_in':None,'tokens_out':None,'custo_usd':None,'execution_constraints':payload['execution_constraints']}
    replace_bytes(ledger,old+(json.dumps(entry,ensure_ascii=False)+'\n').encode())
if job['stage']=='awaiting_dispatch':
    job=transport.coordination.act(job['id'],'prepare_without_work',{'reason':'assistance_not_needed'})
print(json.dumps({'request_id':payload['request_id'],'job_id':job['id'],'stage':job['stage'],'prompt_chars':len(payload['prompt'])}))
