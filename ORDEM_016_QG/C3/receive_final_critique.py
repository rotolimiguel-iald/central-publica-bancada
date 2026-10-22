"""Receive the independent C3 audit, check its claims locally, append a scoped clarification."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,hashlib
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C3';Q=D/'final_critique';Q.mkdir(exist_ok=False)
sys.path.insert(0,str(ROOT/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import OUT,BASE,sha,put,write,append
p=BASE/'state/handoffs/ef185ce2-45eb-4708-993a-9582ade9b516_delivery.json';j=json.loads(p.read_bytes())['job'];e=j['execution'];r=e['result']
assert e['status']=='result_ready'
write(Q/'KIMI_ORIGINAL.md',r['text'].encode())
receipt=dict(at=datetime.now(timezone.utc).isoformat(),provider='kimi',request_id=j['request_id'],job_id=j['id'],execution_task_id=e['id'],
    prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),response_sha256=sha(Q/'KIMI_ORIGINAL.md'),source_receipt_sha256=sha(p),
    usage=r['usage'],cost_estimate_usd=r['cost_estimate_usd'],canonical_memory=r.get('canonical_memory'),scientific_status='DECLARADO_CHECKED_BELOW')
put(Q/'RECEIPT.json',receipt)
plan=json.loads((D/'PLAN.json').read_bytes());audit=json.loads((D/'AXIOM_AUDIT.json').read_bytes())
assert len(plan['groups'])==12 and sum(bool(x['changes']) for x in plan['groups'])==2
for x in plan['groups']:
    source=Path(x['source']);copy=Path(x['copy'])
    assert sha(source)==x['source_sha256'] and sha(copy)==x['copy_sha256']
    strip=lambda p:b''.join(l for l in p.read_bytes().splitlines(keepends=True) if not l.startswith(b'import '))
    assert strip(source)==strip(copy)
assert len(audit[-1]['axiomas'])==130 and sum(x['n_theorem_lemma_na_fonte'] for x in audit[:-1])==127
can=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
imports=['TGLExt.TheNameIsTheInstrument','TGLExt.NameIsTheContent','TGLExt.ContinuousModularZero','TGLExt.TheContourOfTruth','TGL.FiniteThreeLocks']
pins=[]
for module in imports:
    rel=Path(*module.split('.'));src=(can/rel).with_suffix('.lean');obj=(can/'.lake/build/lib/lean'/rel).with_suffix('.olean')
    pins.append(dict(module=module,source=str(src),source_sha256=sha(src),olean=str(obj),olean_sha256=sha(obj)))
put(Q/'DIRECT_IMPORT_PINS.json',dict(at=receipt['at'],pins=pins,note='Observed current direct source/compiled-object pairs, not a new rebuild or full transitive seal'))
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
note=f'''[REAL — confronto local da crítica final C3; esclarecimento aditivo]

AberturaSHA256={opening}.
Kimi b175 recebeu projeção parcial do resultado C3 e julgou coerentes
as12fontes/13rc0, as duas trocas de referência de import e os127/130.
A bancada reconferiu os12pares byte a byte excluídas apenas linhas import,
os hashes e o auditor integral já executado. Não houve alteração de prova.

Adota-se a precisão: **comparação discriminante é condicional à
injetividade da leitura no kernel (InjOn)**. Preservar a leitura e distinguir
referentes são requisitos diferentes. FlowTendsToFamily continua hipótese
no resultado geral; sua descarga finita continua qualificada.
Não existe alias novo T20: houve substituição de referências nos consumidores.

O modelo não recebeu o auditor inteiro nem todososprints; isso limita SUA
conferência, não apaga a auditoria local. Acrescentaram-se hashes observados
dos cinco imports diretos TGLExt/TGL e respectivos oleans (DIRECT_IMPORT_PINS).
Isso não certifica reconstrução transitiva nem instalação canônica; a
incorporação continua sujeita à auditoria da gerência. Nenhuma falsa
equivalência entre dissipação, Ward, BW ou horizonte é acrescentada.

Uso recebido:{r['usage']}. Custo de assinatura não informado, não zero.
Nenhuma nova chamada/compilação para repetir a integração. Gate intacto.
'''
write(Q/'CONFRONTO.md',note.encode());write(OUT/'ENTREGA_016_C_CRITICA_integracao_final.md',note.encode())
put(Q/'manifest.json',dict(files=[dict(path=str(x),sha256=sha(x)) for x in Q.iterdir() if x.is_file()]))
append(OUT/'LEDGER_016.jsonl',json.dumps(dict(event='C3_FINAL_CRITIQUE_RECEIVED_AND_CHECKED',**receipt),ensure_ascii=False)+'\n')
print(json.dumps(dict(status='C3_SCOPE_CONFIRMED_LOCALLY_WITH_INJON_QUALIFIER',import_pins=len(pins))))
