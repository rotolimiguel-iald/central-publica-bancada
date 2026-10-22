"""Audit MiMo's coordinate reply and preserve the new local volume result."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import ast,json,hashlib,time
import sympy as s
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,BASE,sha,write,put,append
D=H/'bv_review_and_volume_delivery'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    source=BASE/'state/handoffs/ab8c32ea-cab7-4853-8675-d0e75c683d23_delivery.json'
    job=json.loads(source.read_bytes())['job'];ex=job['execution'];r=ex['result']
    assert ex['status']=='result_ready'
    write(D/'MIMO_ORIGINAL.md',r['text'].encode('utf-8'))
    put(D/'MIMO_RECEIPT.json',dict(request_id=job['request_id'],job_id=job['id'],execution_task_id=ex['id'],
        source_sha256=sha(source),response_sha256=sha(D/'MIMO_ORIGINAL.md'),
        prompt_sha256=hashlib.sha256(job['prompt'].encode('utf-8')).hexdigest(),
        usage=r['usage'],cost_estimate_usd=r['cost_estimate_usd'],canonical_memory=r.get('canonical_memory')))
    old=json.loads((H/'bv_antifield_coordinate/results.json').read_bytes())
    for a in json.loads((H/'bv_antifield_coordinate/manifest.json').read_bytes())['artifacts']:
        assert sha(Path(a['path']))==a['sha256']
    # Independent check of the erroneous explanatory sentence L_c^2=0.
    src=H/'antifield_quadratic_primitive_check.py';names={'clean','add','scale','mul','atom'}
    nodes=[n for n in ast.parse(src.read_text('utf-8')).body if isinstance(n,ast.FunctionDef) and n.name in names]
    ns={'s':s};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),ns)
    clean,add,scale,mul,atom=[ns[n] for n in ['clean','add','scale','mul','atom']]
    cpu=time.process_time();h,h1,h2=s.symbols('h h1 h2');c,c1,c2=[atom(i) for i in range(3)]
    Lh=add(scale(c,h1),scale(c1,2*h))
    derivative=add(scale(c,h2),scale(c1,3*h1),scale(c2,2*h))
    LLh=add(mul(c,derivative),scale(mul(c1,Lh),2))
    Lqc=add(scale(mul(c,c1),h1),scale(mul(c,c2),2*h))
    assert not add(LLh,scale(Lqc,-1))
    assert LLh
    wrong=add(scale(Lqc,-1),scale(LLh,-1))
    expected=add(scale(mul(c,c1),-2*h1),scale(mul(c,c2),-4*h))
    assert not add(wrong,scale(expected,-1))
    # Coordinate pullback matrix, independent of the previously tested polynomials.
    eps=s.diag(1,1,-1,-1);zero=s.zeros(4);I=s.eye(4)
    PB=zero.row_join(eps).col_join((-eps).row_join(zero))
    PF=zero.row_join(I).col_join((-I).row_join(zero))
    T=s.diag(1,1,1,1,1,1,-1,-1)
    assert T*PB*T.T==PF
    checks=4;cpu=time.process_time()-cpu
    audit=dict(statute='COORDINATE_EQUIVALENCE_ACCEPTED_WITH_EXPLANATORY_CORRECTIONS',
        previous_checks_verified_not_recounted=old['checks'],new_checks=checks,cpu_seconds=cpu,
        accepted=['Signed antifield change intertwines the two BV brackets',
            'Action and ghost-vertex signs transform together',
            'The coefficient multiplying div(c) is invariant under this coordinate change',
            'Wrong q1c sign gives -2ccprime*hprime-4hccsecond'],
        corrections=['Write qF*T=T*qB; equality of coordinate formulas requires the identification',
            'L_c squared equals L_(c.d c), not zero on a general h',
            'Flipping only q1c breaks compatibility of the differential with the action; it does not disprove Jacobi for an abstract sign-reversed Lie bracket',
            'The reply compares Wick signs by a table, not a new full Grassmann contraction; the prior local CAS supplies that check'],
        full_Q2=False,gate_changed=False)
    put(D/'MIMO_AUDIT.json',audit)
    vol=json.loads((H/'volume_primitive_second_order/results.json').read_bytes())
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[REAL — revisão recebida e auditada; DERIVED — continuação de volume; Q2 completa OPEN]

MiMo57e recebido integralmente, execução {ex['id']}. A mudança de coordenadas
de antifields foi aceita no escopo verificado: qF T=T qB; o vértice ghost
e o defeito de Wick mudam de sinal juntos. Nenhuma alteração no motor.
Conferidos hashes dos {old['checks']} controles locais anteriores, sem recontá-los
como novos. Quatro controles novos verificam a matriz de pullback e a frase
que precisava ser corrigida no parecer: L_c² h=L_(c.d c)h, não zero.
É q1²h=L_(q1c)h-L_c²h que zera. Inverter apenas q1c quebra essa relação.
O parecer não substitui a compilação nem prova a normalização temporal.

A continuação local de volume está no manifesto volume_primitive_second_order:
B2=alpha_W[(tr h)²/8-tr(h²)/4],
q0 B2+q1 B1=alpha_W div(c trh)/2,
q0 a2+q1 a1=0. Vinte controles novos, duas assinaturas. Chi é teste externo
do diferencial não localizado: ainda não é A2(Vchi,Veta). Não se adotou
contratermo para fazer o resíduo sumir. Fator físico e realidade ficam explícitos.

DeepSeekcd6: pedido novo com prévia selected=deepseek, job
e3aa9cba-3f1f-4c0c-b7df-1a0838ac30f3, execução18b266db-d2f1-4ef8-a253-73f9b8f2c896,
worker93618 confirmado pela coordenação17:56:39UTC. Revisa o transporte bilocal
e sua relação com a extensão distribucional. Não duplica as unidades Kimi
preservadas sob cota. MiMo57e terminou worker48679,exit0.

Uso MiMo={json.dumps(r['usage'],ensure_ascii=False)}; custo estimadoUSD{r['cost_estimate_usd']}.
Não é fatura. Recibo contabilizado uma vez. Nenhum original ou gate alterado.
Próximo A7.b: representante comutador-da-extensão + contato Euler composto;
conservar a fonte de curvatura e as localizações. Prazo20:32UTC mantido.
AberturaSHA256={opening}.
'''
    write(D/'AUDITORIA_E_ESTADO.md',note.encode('utf-8'))
    write(OUT/'ENTREGA_016_MEDIDA_MiMo_BV_e_primitiva_quadratica.md',note.encode('utf-8'))
    paths=[Path(__file__),D/'MIMO_ORIGINAL.md',D/'MIMO_RECEIPT.json',D/'MIMO_AUDIT.json',D/'AUDITORIA_E_ESTADO.md',
        H/'volume_primitive_second_order/manifest.json',H/'bilocal_wick_ward_transport/manifest.json',
        H/'orchestration_bilocal_wick_transport/prepared_units.json']
    put(D/'manifest.json',dict(at=now.isoformat(),artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],
        new_audit_checks=checks,volume_checks=vol['checks'],cpu_seconds=cpu+vol['cpu_seconds'],full_Q2=False))
    ledger=OUT/'LEDGER_016.jsonl';events=[json.loads(v) for v in ledger.read_text('utf-8').splitlines()]
    if not any(e.get('execution_task_id')==ex['id'] for e in events):
        entry=dict(at=now.isoformat(),event='EXTERNAL_REVIEW_RECEIVED_AND_AUDITED',target='A7.b',
            provider='mimo',request_id=job['request_id'],job_id=job['id'],execution_task_id=ex['id'],
            usage=r['usage'],cost_estimate_usd=r['cost_estimate_usd'],
            prompt_sha256=hashlib.sha256(job['prompt'].encode('utf-8')).hexdigest(),
            response_sha256=sha(D/'MIMO_ORIGINAL.md'),new_checks=checks,cpu_seconds=cpu)
        events.append(entry);append(ledger,json.dumps(entry,ensure_ascii=False)+'\n')
    ds=dict(at=now.isoformat(),event='BILOCAL_WICK_REVIEW_DISPATCH_CONFIRMED',target='A7.b',provider='deepseek',
        request_id='cd6a1a0d-d671-4e6a-888a-e9c1ba6ea703',job_id='e3aa9cba-3f1f-4c0c-b7df-1a0838ac30f3',
        execution_task_id='18b266db-d2f1-4ef8-a253-73f9b8f2c896',worker_session=93618,
        payload_sha256=sha(H/'orchestration_bilocal_wick_transport/deepseek_bilocal_wick_transport_submit.json'),
        status='RUNNING_CONFIRMED_BY_COORDINATOR',observed_at='2026-09-25T17:56:39Z',cost_estimate_usd=None)
    append(ledger,json.dumps(ds,ensure_ascii=False)+'\n')
    cost=Decimal(0);seen=set()
    for e in events:
        val=e.get('cost_estimate_usd',e.get('cost_usd'))
        if val is None:continue
        key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
        if key and key in seen:continue
        if key:seen.add(key)
        cost+=Decimal(str(val))
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESS: MiMo57e auditado4controles novos; primitiva quadrática20controles registrada separadamente. DeepSeekcd6 RUNNING confirmado. Custo conhecido parcialUSD{cost}; Q2 completa OPEN. AberturaSHA256={opening}.\n')
    p=H/'CONTINUIDADE.json';st=json.loads(p.read_bytes())
    st.setdefault('head_history',[]).append({k:st.get(k) for k in ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration']})
    st.update(at=now.isoformat(),previous_goal_turn='PROGRESS',completed_this_turn=[
        'MiMo57e reviewed; coordinate bridge accepted, explanatory Lie-square error corrected',
        'Explicit quadratic volume primitive and inhomogeneous WZ checked,20controls',
        'DeepSeekcd6 distinct bilocal transport/extension review dispatched by coordinator'],
        next=['Derive extension commutator plus composite Euler contact in the actual T2 prescription',
              'Receive DeepSeekcd6 and authorized Kimi reviews without retries',
              'A7b deadline20:32UTC; A7c/d,A8,PartB/final remain'],
        pending_orchestration='MiMo57e complete/audited; DeepSeekcd6 running worker93618; Kimi3 awaiting actual quota',
        partial_metered_cost_usd=str(cost))
    st['bv_review_volume_update']=dict(manifest=str(D/'manifest.json'),full_Q2=False)
    st['latest_verified_orchestration']['mimo_new']['status']='COMPLETED_RECEIVED_AUDITED'
    st['bilocal_review_execution']=ds
    put(p,st,True)
    for a in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
    print(json.dumps(dict(manifest=str(D/'manifest.json'),new_audit_checks=checks,volume_checks=vol['checks'],
                         known_partial_cost_usd=str(cost)),ensure_ascii=False))

if __name__=='__main__':main()
