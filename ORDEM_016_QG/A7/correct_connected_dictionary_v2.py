"""Keep the ordered remainder distinct from the algebraic connected product."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,uuid
H=Path(__file__).resolve().parent;OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
D=H/'flat_wick_dictionary_delivery_v2';D.mkdir(exist_ok=False)
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,replace=False):
    assert b
    if p.exists():
        assert replace,p
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
        assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
def put(p,v,replace=False):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'),replace)
def append(p,t):write(p,p.read_bytes()+t.encode('utf-8'),True)
old=H/'flat_wick_dictionary_delivery/DERIVACAO.md'
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
note=f'''[DERIVED — correção de nomenclatura e normalização; sem novo cálculo de Q2]

Correção ao lado de {old.name}, SHA256={sha(old)}.
O resto ORDENADO U2=T2(F,G)-T1(F)star T1(G) tem o cancelamento Ward escrito
na entrega anterior, mas não é o produto conectado algébrico da fonte.
Usar o adjetivo conectado para U2 sem essa precisão foi inadequado.

Para entradas homogêneas, defina
 S2(F,G)=[T1(F)star T1(G)+(-1)^(epsF epsG)T1(G)star T1(F)]/2,
 U2sym=T2-S2, e Tc2=(i/hbar)U2sym.

Essa é a convenção conectada algébrica de Fröb, equações34–35, p9:
https://arxiv.org/pdf/1803.10235v3 . Ela não coincide automaticamente com
conectados definidos por um estado, nem com a ação efetiva1PI.

Para F,G pares, ponha B1=s0+A1. A derivação de S2 é
 shat0 S2(F,G)=S2(B1F,G)+S2(F,B1G).
Logo, na mesma prescrição,
 T1(A2(F,G))=shat0 Tc2(F,G)-Tc2(B1F,G)-Tc2(F,B1G)-T1((F,G)).

O fator i/hbar está agora incluído em Tc2. Ambos os termos A1 continuam
presentes. A fórmula T2 da entrega anterior permanece válida; apenas sua
tradução para conectado exige esta simetrização e esta normalização.
As14 verificações de matriz livre permanecem inalteradas. Nada demonstra
o Wick localmente covariante curvo: na construção geral, a referência é
parametrix geométrico, não um estado particular arbitrariamente escolhido.

Recibo adicional: Kimi bd879 falhou HTTP403 da janela5h, confirmado pelo
coordenador; sem resposta aceita ou nova tentativa. Mantidos prompts e
IDs pendentes. MiMo e DeepSeek têm tarefas distintas, não substituições.
Nenhum original, kernel ou gate alterado. AberturaSHA256={opening}.
'''
write(D/'ADENDO.md',note.encode('utf-8'))
write(OUT/'ENTREGA_016_MEDIDA_Wick_plano_dicionario_aridade2_v2.md',note.encode('utf-8'))
receipt=BASE/'state/handoffs/06e3c2b3-89da-47c3-87ba-c8aed1be7ba1_delivery.json'
j=json.loads(receipt.read_bytes())['job'];e=j['execution']
assert j['request_id']=='bd8796b3-0bac-43fb-bb0b-51581037b965'
assert e['status']=='failed' and e['result'] is None
f=dict(at=now.isoformat(),provider='kimi',target='A7.b',event='EXTERNAL_UNIT_FAILED_NO_ACCEPTED_RESPONSE',
    request_id=j['request_id'],job_id=j['id'],execution_task_id=e['id'],status=e['status'],
    prompt_sha256=hashlib.sha256(j['prompt'].encode('utf-8')).hexdigest(),response_sha256=None,
    receipt_sha256=sha(receipt),tokens=None,cost_usd=None,error=e['error'],
    official_diagnosis='HTTP403 five-hour usage window; reset time not specified in message',
    unknown_usage_is_not_zero=True,repeated=False)
put(D/'KIMI_BD879_FAILED.json',f)
put(D/'manifest.json',dict(at=now.isoformat(),supersedes=dict(path=str(old),sha256=sha(old),
    scope='Only ordered-versus-connected identification; free covariance results retained'),
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'ADENDO.md',D/'KIMI_BD879_FAILED.json']],
    new_cas_checks=0,full_Q2=False,gate_changed=False))
ledger=OUT/'LEDGER_016.jsonl';entries=[json.loads(v) for v in ledger.read_text('utf-8').splitlines()]
rows=[]
if not any(v.get('execution_task_id')==e['id'] for v in entries):rows.append(f)
rows.append(dict(at=now.isoformat(),event='CONNECTED_DICTIONARY_SYMMETRIZATION_CORRECTION',target='A7.b',
    new_cas_checks=0,remote_call=False,manifest_sha256=sha(D/'manifest.json')))
append(ledger,''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in rows))
p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
state['flat_wick_dictionary_update']['connected_dictionary_correction']=str(D/'manifest.json')
state['pending_orchestration']='Kimi5e1 and bd879 FAILED,no retries; bd879 HTTP403 window5h. MiMoa46 running; DeepSeek6309 promotion requested for distinct audit, no provider substitution.'
state['at']=now.isoformat();put(p,state,True)
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b:correção de U2ordenado para Tc2=(i/hbar)(T2-S2simétrico),sem novo CAS. Kimi bd879403janela5h preservado;uso desconhecido. AberturaSHA256={opening}.\n')
print(json.dumps(dict(manifest=str(D/'manifest.json'),failure_recorded=e['id'],new_cas_checks=0)))
