"""Record the actual linear-slot progress and the limited independent review."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json
import sympy as s
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,BASE,sha,write,put,append
D=H/'linear_insertion_review_delivery'
def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    source=BASE/'state/handoffs/f1a5534b-6c8d-47aa-8f86-b86e29384836_delivery.json'
    job=json.loads(source.read_bytes())['job'];ex=job['execution'];r=ex['result']
    assert ex['status']=='result_ready'
    write(D/'DEEPSEEK_ORIGINAL.md',r['text'].encode('utf-8'))
    put(D/'DEEPSEEK_RECEIPT.json',dict(request_id=job['request_id'],job_id=job['id'],execution_task_id=ex['id'],
        source_sha256=sha(source),response_sha256=sha(D/'DEEPSEEK_ORIGINAL.md'),
        usage=r['usage'],cost_estimate_usd=r['cost_estimate_usd'],
        prompt_sha256=__import__('hashlib').sha256(job['prompt'].encode('utf-8')).hexdigest(),
        canonical_memory=r.get('canonical_memory')))
    calc=json.loads((H/'nonminimal_wick_heat_ward/results.json').read_bytes())
    one=json.loads((H/'linear_anomaly_insertion/results.json').read_bytes())
    bridge=json.loads((H/'linear_slot_ward_bridge/results.json').read_bytes())
    ah=s.Rational(9,2)*s.Rational(137,60)+s.Rational(579,40)
    assert ah==s.Rational(99,4)
    assert ah+s.Rational(179,20)==s.Rational(337,10)
    assert s.Rational(81,5)-s.Rational(35,2)==-s.Rational(13,10)
    put(D/'DEEPSEEK_AUDIT.json',dict(statute='PARTIAL_ARITHMETIC_AND_CSTAR_RECONSTRUCTION_ACCEPTED',
        arithmetic_controls=3,accepted=['99/4 metric plus179/20 ghost=337/10',
            'Cstar S from the supplied first jet','Opposite mixed sign would give-13/10'],
        not_independently_verified_by_reply=['Full heat Ward intertwiner and transport uniqueness',
            'Global G or Lorentzian continuation','Admissible time-ordered normalization'],
        corrections=['Heat mixed derivative and logarithmic Green mixed derivative are different objects, not freely interchangeable conventions',
            'Formal heat intertwining does not require a constructed global state; the G representation is a separate assumption',
            'The trace weights were independently measured by the bench before this review, not merely named'],
        normalization_changed=False,full_Q2=False,gate_changed=False))
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED — inserções lineares identificadas e identidade auxiliar fechada; Q2 completa OPEN]

# Duas inserções de A1 entram na identidade de aridade2

Mantemos Tc2=(i/hbar)(T2-S2), com S2 simetrizado graduadamente. A condição
de concordância perturbativa para uma entrada linear, escrita nas equações
158a/b de Fröb1803.10235v3, fornece os produtos com Green avançado/retardado.
Usá-la é uma condição explícita de normalização, não consequência automática
do finite part radial aplicado aos grafos com duas linhas internas.
Fonte primária consultada: https://arxiv.org/pdf/1803.10235v3, p37.

Mediando as duas ordens e usando GD=(Gret+Gadv)/2, derivamos

 Tc2(V,phiK(x))=-int GD_LK(y,x) T1(dR V/dphiL(y))dy.

No único canal que contrai com c, Vghost=chi barc C Lie_c h. A derivada
DIREITA em barc vale -chi C Lie_c h, e G_barc,c=-GQ. Assim

 Tc2(Vchi,c_i(x))=-int GQ_D,ji(y,x) chi(y)(C Lie_c h)^j(y)dy.

As parcelas métrica e antifield de V1 não têm barc e não contribuem a essa
contração linear. O produto restante h*c não tem contração interna permitida.
Escrevendo A1(Vchi)=i hbar alpha int chi div(c), com alpha contendo a
normalização física ainda explícita, o par de termos subtraídos em A2 é

 -i hbar alpha [int dchi(x) GQ_D(y,x) eta(y) C Lie_c h(y)
              +int deta(x) GQ_D(y,x) chi(y) C Lie_c h(y)].

Para chi=eta há fator2. Omitir uma das duas entradas perde esse fator.
Essas parcelas tomadas sozinhas contêm Green e são não locais. Devem ser
combinadas com os outros termos da Ward para obter a quebra local; não
podem ser renomeadas como contato já calculado. Um controle de coeficientes
constantes deixa resto -4m²lambda ao dividir4lambda³ por lambda²+m².
Esse controle detecta a não localidade do inverso, sem pretender calcular
o propagador curvo. São{one['checks']}controles, CPU{one['cpu_seconds']}s,rc0.

# A identidade linear fecha com o termo de Euler presente

Ponha w=c.nabla c. A nilpotência clássica polarizada dá
C Lie_c Kg c=Qw. A derivada direita do vértice s0Vchi em barc tem DUAS
parcelas: chi Qw, vinda do vértice ghost, e -Q(chi w), vinda do termo
qcdag=-Qbarc-Kg*hdag. Portanto

 dR(s0 Vchi)/dbarc=chi Qw-Q(chi w)=-[Q,chi]w,
 [Q,chi]w=2nabla chi.nabla w+(box chi)w.

A identidade com uma entrada c torna-se exatamente

 s0 Tc2(Vchi,c)-Tc2(s0Vchi,c)-(Vchi,c)
 =GD chi Qw-GD(chi Q-Qchi)w-chi w=0.

Usa-se GD Q=I no domínio dos testes declarado. Tc2(A1(Vchi),c)=0 por
ausência de contração c*c. Se omitirmos -Q(chi w), a mesma expressão dá
-chi w, não zero. São{bridge['checks']}controles exatos, CPU{bridge['cpu_seconds']}s,
com matrizes finitas que testam a ordem dos operadores e a regra de produto
diferencial nas assinaturas euclidiana/lorentziana. Os controles não constroem
um Green global. O resultado é A2(Vchi,c)=0 sob o contrato; não é
A2(Vchi,Veta)=0.

# Auditoria da revisão DeepSeek6945

Resposta original e recibo preservados. O revisor reconstruiu a aritmética
99/4+179/20=337/10 e C*S a partir do primeiro jato fornecido. Essa parte
confere com o CAS da bancada. Não forneceu reconstrução independente de
toda a identidade de transporte do calor: sua aprovação é condicional.
Corrigimos sua nomenclatura: jato misto do calor e jato logarítmico de Green
são OBJETOS diferentes, não convenções intercambiáveis. Estado global e
entrelaçamento formal local também são obrigações diferentes.

Próximo passo: verificar a normalização da entrada linear na MESMA família
T2 e reunir as duas parcelas acima ao subtotal de duas inserções já medido,
conservando a parte de curvatura e os termos de cutoff. O coeficiente337/10
é auxiliar euclidiano; realidade/continuação não foram inferidas do voto do
revisor. MiMo57e está executando a revisão de coordenadas BV; Kimi mantém
três pedidos aguardando recuperação efetiva da quota. Nenhuma nova chamada
nesta entrega. Originais e gate intactos. AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO_E_REVISAO.md',note.encode('utf-8'))
    write(OUT/'ENTREGA_016_MEDIDA_insercoes_lineares_A1_e_Ward.md',note.encode('utf-8'))
    paths=[Path(__file__),D/'DEEPSEEK_ORIGINAL.md',D/'DEEPSEEK_RECEIPT.json',D/'DEEPSEEK_AUDIT.json',
        D/'DERIVACAO_E_REVISAO.md']
    for folder in ['linear_anomaly_insertion','linear_slot_ward_bridge']:
        paths.extend([H/folder/'results.json',H/folder/'manifest.json'])
    checks=one['checks']+bridge['checks'];cpu=one['cpu_seconds']+bridge['cpu_seconds']
    put(D/'manifest.json',dict(at=now.isoformat(),artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],
        checks=checks,review_arithmetic_controls=3,cpu_seconds=cpu,full_Q2=False,gate_changed=False))
    ledger=OUT/'LEDGER_016.jsonl';entries=[json.loads(v) for v in ledger.read_text('utf-8').splitlines()];events=[]
    if not any(v.get('execution_task_id')==ex['id'] for v in entries):
        events.append(dict(at=now.isoformat(),event='EXTERNAL_REVIEW_RECEIVED_AND_AUDITED',target='A7.b',
            provider='deepseek',request_id=job['request_id'],job_id=job['id'],execution_task_id=ex['id'],usage=r['usage'],
            cost_estimate_usd=r['cost_estimate_usd'],response_sha256=sha(D/'DEEPSEEK_ORIGINAL.md'),
            accepted='CONDITIONAL_ARITHMETIC_AND_CSTAR_ONLY'))
    events.append(dict(at=now.isoformat(),event='LINEAR_A1_INSERTIONS_AND_WARD_BRIDGE',target='A7.b',
        checks=checks,review_arithmetic_controls=3,cpu_seconds=cpu,manifest_sha256=sha(D/'manifest.json'),remote_call=False))
    append(ledger,''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events))
    cost=Decimal(0);seen=set()
    for event in entries+events:
        val=event.get('cost_estimate_usd',event.get('cost_usd'))
        if val is None:continue
        key=event.get('execution_task_id') or event.get('job_id') or event.get('request_id')
        if key and key in seen:continue
        if key:seen.add(key)
        cost+=Decimal(str(val))
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESS: duas inserções lineares A1 explicitadas; A2(Vchi,c)=0 sob concordância perturbativa, com controle negativo -chi w. {checks}controles CPU{cpu}s; revisão DeepSeek6945 aceita no escopo aritmético condicional. Custo conhecido parcialUSD{cost}. Q2(V,V)OPEN. AberturaSHA256={opening}.\n')
    p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
    state.setdefault('head_history',[]).append({k:state.get(k) for k in ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration']})
    state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',completed_this_turn=[
        'Both A1 linear insertions in connected A2 explicitly derived with their ghost signs',
        'Linear-slot Ward identity cancels only with the antifield Euler source retained',
        'DeepSeek6945 received and audited within its conditional arithmetic scope'],
        next=['Verify linear-slot normalization in the same T2 family as the radial pair extension',
            'Assemble both A1 insertion terms with the already measured two-entry subtotal; no omitted cutoff/curvature terms',
            'Receive MiMo57e BV-coordinate review; preserve Kimi requests under actual quota',
            'A7b deadline20:32UTC; A7c/d,A8,PartB/final remain'],
        pending_orchestration='DeepSeek6945 complete/audited; MiMo57e running worker48679; Kimi3 awaiting actual quota recovery',
        partial_metered_cost_usd=str(cost))
    state['linear_insertion_update']=dict(manifest=str(D/'manifest.json'),full_Q2=False,own_processes=[])
    state['latest_verified_orchestration']['deepseek_next']['status']='COMPLETED_RECEIVED_AUDITED_CONDITIONAL'
    state['latest_verified_orchestration']['mimo_new'].update(status='RUNNING_CONFIRMED_BY_COORDINATOR',
        execution_task_id='b6d6658a-0dfe-41e3-aa05-1d413874b348',worker_session=48679,observed_at='2026-09-25T17:32:09Z')
    put(p,state,True)
    for artifact in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(artifact['path']))==artifact['sha256']
    print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=checks,cpu_seconds=cpu,known_partial_cost_usd=str(cost)),ensure_ascii=False))
if __name__=='__main__':main()
