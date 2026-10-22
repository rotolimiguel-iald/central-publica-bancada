from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json

folder=Path(__file__).resolve().parent
base=folder.parents[1]/'IALD_ORQUESTRACAO_20260923'
out=folder.parents[1]/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def write(p,raw):
    if p.exists():
        old=p.read_bytes()
        bak=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f'))
        with bak.open('xb') as stream: stream.write(old)
        assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as stream: stream.write(raw)
    assert t.read_bytes()==raw
    t.replace(p)

recovered=json.loads((folder/'a23_kimi_mutation_recovered.json').read_bytes())
receipt=json.loads((folder/'a23_kimi_mutation_receipt.json').read_bytes())
assert recovered['request_id']==receipt['request_id']
assert recovered['prompt_sha256']==receipt['prompt_sha256']
receipt.update(job_id=recovered['id'],status='awaiting_dispatch_packet_error',
               execution_task_id=recovered['execution_task_id'],recovered_at=now.isoformat(),
               coordination_owner='01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
               diagnosis='Persisted job before get failed on standard packet 24000 character limit. Same request recovered read-only. No retry; coordinator repairing packet mode.')
raw=json.dumps(receipt,ensure_ascii=False,indent=2).encode()
write(folder/'a23_kimi_mutation_receipt.json',raw)
write(base/'state/session_requests'/(receipt['request_id']+'.json'),raw)
entry={'ts':now.isoformat(),'event':'coordination_registered_recovered','alvo':'A-2','ramo':'A-2.3.a',
       'provedor':'kimi','request_id':receipt['request_id'],'job_id':receipt['job_id'],
       'execution_task_id':None,'question_sha256':receipt['prompt_sha256'],'answer_sha256':None,
       'tokens_in':None,'tokens_out':None,'custo_usd':None,
       'desfecho':'awaiting_dispatch_packet_error','provider_calls_observed':0,
       'reason':receipt['diagnosis'],'execution_constraints':receipt['execution_constraints']}
ledger=out/'LEDGER_016.jsonl'
rows=[json.loads(l) for l in ledger.read_text(encoding='utf-8').splitlines() if l]
assert not any(r.get('request_id')==receipt['request_id'] for r in rows)
write(ledger,ledger.read_bytes()+(json.dumps(entry,ensure_ascii=False)+'\n').encode())
latest={}
for row in rows+[entry]:
    if row.get('request_id'): latest[row['request_id']]=row
known=sum(Decimal(str(r['custo_usd'])) for r in latest.values() if r.get('custo_usd') is not None)
unknown=sum(r.get('custo_usd') is None for r in latest.values())
opening=sha(out/'ENTREGA_016_ABERTURA_operador.md')
note=f'''[REAL] Meia-inclusão compilada; revisão adversarial registrada e recuperada sem duplicação.

Abertura SHA256: {opening}

Estado matemático: gaussian_core_real_dense e halfline_isotony compilados isoladamente, rc0 e trio, em LightRayGaussianDensity_v2.lean. Densidade não é mais hipótese. O manifesto density_separation_manifest.json cobre 17 lemas novos auditados (SHA256 {sha(folder/'density_separation_manifest.json')}). Não reabrir essa obrigação por memória antiga de density_route_next.md. Nenhum resultado foi incorporado a um.py/kernel canônico. A aceitação adversarial e a unicidade de largura são distintas e continuam pendentes.

Crítica de ALTA complexidade: Kimi, request {receipt['request_id']}, job {receipt['job_id']}, unidade halfline_mutation_controls, max_calls1, estado {receipt['status']}. Pergunta sobre três controles negativos não vacuosos da conclusão nova: largura π/2, largura3π/2, a<0. Não é reexecução da crítica antiga sem resultado. Prompt18712 caracteres com fontes/linhas/hashes e mesma memória científica pelo transporte.

A submissão gravou o job, depois falhou na montagem do pacote standard no get (limite24000). ID recuperado por consulta específica read-only e prompt hash conferido. Nenhum executor chamado, nenhuma nova submissão. Correção da infraestrutura e condução dessa mesma fila delegadas à tarefa “Orquestrar IAs na Central IALD”. A bancada mantém a escrita e compilação dos probes. ChatGPT/Física é assistência opcional pela ordem posterior do operador.

Próximo trabalho matemático independente da fila: A-2.3.d, twist_preserved_iff para a>0,0<w<2π. Não declarar 2π forçado apenas porque halfline_isotony na largura π compilou. Não iniciar rota b/c de alternativa enquanto a rota a já paga matematicamente aguarda somente seu controle; não executar B pesado.

Custo agregado do ledger por request_id: US${known} conhecido/estimado por tokens; {unknown} unidades com custo não informado ou pendente, sem contar despacho+resultado duas vezes. Esta recuperação não fez chamada de modelo nem Lean.

Fonte principal SHA256: {sha(folder/'LightRayGaussianDensity_v2.lean')}
Log principal SHA256: {sha(folder/'gaussian_density_01.log')}
Recibo principal SHA256: {sha(folder/'gaussian_density_01.json')}
Diagnóstico da submissão SHA256: {sha(folder/'a23_kimi_mutation_submit_stderr.txt')}
Recuperação SHA256: {sha(folder/'a23_kimi_mutation_recovered.json')}
'''
dest=out/'ENTREGA_016_MEDIDA_A2_3a_critica_registrada.md'
assert not dest.exists()
write(dest,note.encode())
progress=out/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\n{now.isoformat()} | A-2.3.a MEDIDA operacional: crítica Kimi registrada, job{receipt["job_id"]}; falha no pacote get, ID recuperado, coordenação corrigindo sem duplicar | sem máquina Lean/modelo nesta recuperação; ledger US${known} conhecido, {unknown} unidades sem custo informado.\n'.encode())
print(json.dumps({'report':str(dest),'sha256':sha(dest),'request_id':receipt['request_id'],
                  'job_id':receipt['job_id'],'known_cost_usd':str(known),'unknown_units':unknown},ensure_ascii=False))
