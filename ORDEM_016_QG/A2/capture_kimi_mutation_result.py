from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

p=Path(__file__).resolve().parent
base=p.parents[1]/'IALD_ORQUESTRACAO_20260923'
out=p.parents[1]/'TUNEL/DO_CHATGPT'
src=base/'state/handoffs/3c0f81cc-f9dc-4fab-9abd-1dfd94f60fcc_completed.json'
now=datetime.now(timezone.utc)
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,b,replace=False):
    if replace:
        old=p.read_bytes()
        write(p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f')),old)
    else:assert not p.exists(),p
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b
    t.replace(p)
d=json.loads(src.read_bytes())
ex=d['execution']; result=ex['result']; answer=result['text'].encode()
assert ex['id']=='f0e1a3b8-d8b8-47af-9cf1-79b4a5528153'
assert ex['status']=='result_ready' and answer
write(p/'a23_kimi_mutation_answer.md',answer)
usage=result.get('usage')
safe={'source':str(src),'source_sha256':sha(src.read_bytes()),'task_id':ex['id'],
      'status':ex['status'],'usage':usage,'elapsed_seconds':result.get('elapsed_seconds'),
      'answer_sha256':sha(answer),'captured_at':now.isoformat()}
write(p/'a23_kimi_mutation_result.json',(json.dumps(safe,ensure_ascii=False,indent=2)+'\n').encode())
rpath=p/'a23_kimi_mutation_receipt.json'
receipt=json.loads(rpath.read_bytes())
receipt.update(status='completed_executor_review_received',execution_task_id=ex['id'],
    completed_at=now.isoformat(),answer_sha256=sha(answer),raw_usage=usage,
    review_status='DECLARADO_NOT_COMPILED_BY_PROVIDER__BANCADA_PROBES_PENDING')
write(rpath,(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode(),True)
entry={'ts':now.isoformat(),'event':'coordination_executor_result_received',
 'request_id':receipt['request_id'],'job_id':receipt['job_id'],'execution_task_id':ex['id'],
 'alvo':'A-2','ramo':'A-2.3.a','provedor':'kimi','question_sha256':receipt['prompt_sha256'],
 'answer_sha256':sha(answer),'raw_usage':usage,'custo_usd':None,
 'desfecho':ex['status'],'provider_calls_observed':1,
 'elapsed_seconds':result.get('elapsed_seconds'),'status_mathematics':'DECLARADO_PROBES_PENDING'}
ledger=out/'LEDGER_016.jsonl'
write(ledger,ledger.read_bytes()+(json.dumps(entry,ensure_ascii=False)+'\n').encode(),True)
opening=sha((out/'ENTREGA_016_ABERTURA_operador.md').read_bytes())
report=f'''[DECLARADO — crítica externa recebida; testes formais adicionais ainda não executados]

# A-2.3.a — recibo da crítica Kimi

Data UTC: {now.isoformat()}. ABERTURA sha256: `{opening}`.
Uma única execução Kimi K3 MAX, task `{ex['id']}`, encerrada em result_ready.
Resposta preservada em `{p/'a23_kimi_mutation_answer.md'}`; sha256 `{sha(answer)}`.
Uso informado: `{json.dumps(usage,ensure_ascii=False)}`.
Tempo informado: {result.get('elapsed_seconds')} s. Custo monetário não informado.

A crítica reconhece a densidade REAL agora demonstrada e o alcance de halfline_isotony:
subespaço real padrão 1+1 para a≥0. Não apontou contradição nessa conclusão, mas não
compilou nem recebeu todos os corpos dependentes. Isso não substitui a auditoria Lean.

Propõe três controles: sinal negativo (crescimento em fatia interna), π/2 (torção de
borda falha), 3π/2 (borda e crescimento interno). A-2.3.d, compilado durante a chamada,
já prova falha da TORÇÃO nessas duas larguras e falha da CONTRAÇÃO para a<0.
Isso não basta para provar não-pertença ao subespaço padrão. O próprio crítico identifica
a dependência ainda necessária no controle de sinal: a direção inversa da ponte de
faixa de Paley–Wiener, ou uma prova direta de não-integrabilidade espectral.

Correção de alcance à resposta: integração numérica em truncamentos finitos não prova
divergência até infinito nem dispensa essa ponte para concluir não-isotonia. A afirmação
final do crítico de que os três probes já verificam a necessidade das hipóteses é,
neste estado, um roteiro analítico, não três testes executados pela bancada.
Também não se transporta a falha de elaboração de um argumento à falsidade da proposição.

Próximo: registrar controles explícitos no escopo analítico e discriminar a ponte ainda
não formalizada; seguir A-2.5 sem reabrir a prova de densidade já auditada.
Nenhuma alteração de kernel/gate. Nenhuma reexecução da unidade.
'''
write(out/'ENTREGA_016_MEDIDA_A2_3a_critica_Kimi_recebida.md',report.encode())
print(json.dumps(safe,ensure_ascii=False))
