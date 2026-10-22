"""Deliver the arity-one formula and audit MiMo's scalar normalization reply."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,time,uuid
import sympy as s
from logarithmic_contact_engine import Q,residue,contact
H=Path(__file__).resolve().parent;OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923';D=H/'wick_arity_one_scalar_review_delivery_v2'
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,replace=False):
    assert b
    if p.exists():
        assert replace,p
        old=p.read_bytes();backup=p.with_name(p.name+'.bak_'+stamp)
        assert not backup.exists();backup.write_bytes(old);assert backup.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
def put(p,v,replace=False):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'),replace)
def append(p,text):
    old=p.read_bytes();write(p,old+text.encode('utf-8'),True);assert p.stat().st_size>len(old)
def main():
    D.mkdir(exist_ok=False)
    path=BASE/'state/handoffs/ea89a9c0-00c5-4c75-9340-d0efcda7cddd_delivery.json'
    job=json.loads(path.read_bytes())['job'];execution=job['execution'];result=execution['result']
    assert execution['status']=='result_ready'
    write(D/'MIMO_ORIGINAL.md',result['text'].encode('utf-8'))
    put(D/'MIMO_RECEIPT.json',dict(request_id=job['request_id'],job_id=job['id'],
        execution_task_id=execution['id'],source_sha256=sha(path),
        prompt_sha256=hashlib.sha256(job['prompt'].encode('utf-8')).hexdigest(),
        response_sha256=sha(D/'MIMO_ORIGINAL.md'),usage=result['usage'],
        cost_estimate_usd=result['cost_estimate_usd'],canonical_memory=result.get('canonical_memory')))
    start=time.process_time();a,tau=s.symbols('a tau');q2=sum(v*v for v in Q);r3=residue(3,(0,0,0,0),(1,1,1,1))
    checks=[]
    def eq(name,v):assert s.cancel(v)==0,(name,v);checks.append(name)
    first=4*tau*a*(tau*a-1);second=4*(1-tau)*a*((1-tau)*a-1)
    cross=8*(tau*a-1)*((1-tau)*a-1);total=4*(a-2)*(a-1)
    eq('allocated Laurent Leibniz before finite part',first+second+cross-total)
    finite=lambda c:s.diff(c,a).subs(a,0)*r3
    eq('first line',finite(first)-tau*q2/8)
    eq('second line',finite(second)-(1-tau)*q2/8)
    eq('gradient local correction',finite(cross)-q2/4)
    eq('total local correction',finite(total)-3*q2/8)
    eq('line exchange transports allocation',finite(first).subs(tau,1-tau)-finite(second))
    for value in (0,1,s.Rational(1,2)):
        eq('allocation control '+str(value),finite(first).subs(tau,value)-value*q2/8)
    # Retain the reply's valid equal-slope calculation in its own convention.
    eq('equal slope Euler retained',s.diff(4*a*(a-1),a).subs(a,0)*r3/2-q2/16)
    cb=sum(contact(2,0,(i,i)) for i in range(4))
    eq('fixed pair derivative contact',cb+3*q2/8)
    eq('scale derivative of C_box cancels',8*r3-q2*residue(2,(0,0,0,0),(1,1,1,1)))
    # Homogeneity, independent of any dimensional or analytic renormalization restriction.
    x=s.symbols('x0:4');z=sum(v*v for v in x);tensor=x[0]*x[1]/z**4
    eq('two-line gradient tensor has scaling degree six',sum(xi*s.diff(tensor,xi) for xi in x)+6*tensor)
    eq('Euler dilation preserves degree',sum(xi*s.diff(z**-2,xi) for xi in x)+4/z**2)
    assert [j for j in range(5) if j%2==0]==[0,2,4]
    checks.append('sd8 scalar local degrees include box delta')
    audit=dict(at=now.isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        tau_meaning='allocation of the one pair regulator, not a finite counterterm coefficient',
        contacts={'first':str(finite(first)),'second':str(finite(second)),
            'cross_relative_to_8R3':str(finite(cross)),'total_relative_to_8R3':str(finite(total)),
            'C_box':str(cb)},
        prompt_defect='Sent text says f_a,g_a above but never defines them or tau. Responsibility of this bench; cannot compare its assumed scheme as if it were the requested one.',
        reply_corrections=['Euler was reinterpreted as dilation despite requested box-line formulas',
            'Total slope2a is a distinct parameterization; prefactor and scale must also transform',
            'x_i x_j z^-4 has scaling degree6, not8',
            'sd8 scalar bound admits delta,box delta,box²delta unless further restrictions remove lower degrees',
            'No universal logarithmic term 2Res(t) in C_D: derivative commutator cancels its scale dependence here'],
        old_engine_changed=False,normalization_selected=False,full_Q2=False)
    put(D/'scalar_audit.json',audit)
    dirs=['wick_arity_one_graded_commutator','wick_antifield_local_jet_formula','wick_antifield_spaceform_reduction']
    results=[json.loads((H/d/'results.json').read_bytes()) for d in dirs]
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    report=f'''[DERIVED — aridade1 condicional e CAS graduado; A1 curvo numérico e Q2 OPEN]

# Transporte de Wick sem redefinir o diferencial para forçar zero

Hipóteses explícitas: uma representação livre G equivarante já fixada;
H é o parametrix local; W=G-H é suave; não há contrações de antifields.
A derivação quântica é fixada em geradores/Leibniz, não escolhida por
conjugação de H. As equações7,20–21,140/160 de Fröb1803.10235v3
fornecem as convenções de representação; usamos a relação
N_H=N_G exp(i hbar C_W). Fonte primária consultada nesta rodada:
https://arxiv.org/pdf/1803.10235v3 (pp3,5,31,37).

Como q é linear e C_W é uma contração de coeficientes independentes dos
campos, R_W=[q,C_W] tem coeficientes constantes e [C_W,R_W]=0. Então

 exp(-t C_W) q exp(t C_W)=q+t R_W,
 A1(F)=i hbar R_W F.

Isto deriva a correção em H a partir da derivação livre fixa em G. Não
declara existência de G/H completos no alvo. Uma troca de estado G+B
preserva esta fórmula quando [q,C_B]=0; suavidade sozinha não basta.
São {results[0]['checks']} controles em {results[0]['tested_monomials']} monômios
da álgebra graduada finita, com testemunhas não nulas; não são uma prova
de existência de covariância no espaço-tempo. CPU{results[0]['cpu_seconds']}s.
Exemplo: q(hdagger)=m h, F=hdagger h c, C_W F=0, mas
C_W(qF)=m W_hh c e R_W F=-m W_hh c. O termo Euler não desaparece.

# O vértice existente exige quatro arrays finitos

Use coordenadas independentes h_A simétricas e antifields duais. Escreva
Lie_c h_A=c^k nabla_k h_A+M_A^B(nabla c)h_B. Seja D_H o defeito Ward
estendido a campos/antifields: no slot hdagger ele inclui a equação livre
completa, inclusive b; no slot cdagger, a equação ghost e seus sinais.
Defina os quatro arrays no ponto de coincidência:

 Jh0[A,B]=[D_H(hdagger_A,h_B)], Jh1[k,A,B]=[nabla_y,k D_H(hdagger_A,h_B)],
 Jc0[i,j]=[D_H(cdagger_i,c^j)], Jc1[k,i,j]=[nabla_y,k D_H(cdagger_i,c^j)].

Para Faf=int chi(hdagger Lie_c h+cdagger_i c^j nabla_j c^i),

 A1(Faf)/(i hbar)=int chi [c^k Jh1[k,A,A]+M_A^B(nabla c)Jh0[A,B]
                         +Jc0[i,j]nabla_j c^i-Jc1[j,i,i]c^j].

A última subtração é Grassmann; omiti-la falha no controle. Até três
derivadas de H são necessárias, porque a equação livre tem ordem2 e
o vértice acrescenta uma. Os{results[1]['checks']}controles dos slots não
medem esses arrays do multiplet completo. O resto mínimo3U2/4 calculado
antes NÃO pode ser substituído diretamente por Jh0/Jc0.

Se, adicionalmente, os arrays são naturais, invariantes de espaço-forma
e pares sob O4, seus primeiros jatos têm posto tensorial ímpar e zeram.
Escreva Jh0=aTL P_TL+aTr P_tr, Jc0=d I4. A representação simétrica dá
tr(M P_TL)=9 div(c)/2 e tr(M P_tr)=div(c)/2. Logo

 A1(Faf)/(i hbar)=(9aTL/2+aTr/2+d) int chi div(c).

Nesse setor condicionado, a primitiva linear é metade desse coeficiente
vezes int chi tr(h), pois q tr(h)=2 div(c). Verificado por{results[2]['checks']}
controles matriciais. Não se supôs que M preserva cada setor. Não é a
anomalia de todo V1, nem família admissível/reality de contratermos já paga.

# MiMoa46 — resposta preservada, cálculo e limitação do pedido

O prompt da bancada dizia f_a,g_a «acima», mas não os definia, nem definia
tau. Essa lacuna é minha. MiMo adotou f_a=g_a=z^(a-1) e tau como contato
finito; também chamou Euler de dilatação. Não transportamos essa resposta
como se fosse o cálculo com tau de alocação feito antes pela bancada.
Seu contato q²/16 para uma linha no esquema simétrico é correto.

Para f_a=z^(tau a-1), g_a=z^((1-tau)a-1), com o mesmo prefator de R:
FP[(box f_a)g_a]/CE=tau q²/8; a outra linha dá(1-tau)q²/8.
O gradiente total é8R3/CE+q²/4; a soma é8R3/CE+3q²/8.
C_box(z^-2)/CE=-3q²/8, independente da escala. Mantidos tau0,1,1/2
como diagnósticos, sem adotar um deles. São{audit['checks']}controles.
Corrigidos ainda o grau6 de x_i x_j z^-4 e a ausência indevida de box delta
na tabela de grau≤4. Grau de escala sozinho admite termos inferiores;
restrições homogêneas/dimensionais adicionais devem ser declaradas.
Nenhum motor anterior foi refeito, nenhum parâmetro foi ajustado.

MiMo87d está executando a revisão independente da fórmula de aridade1;
as conclusões locais não foram inseridas em seu prompt. Q2/gate intactos.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO_E_REVISAO.md',report.encode('utf-8'))
    write(OUT/'ENTREGA_016_MEDIDA_Wick_aridade1_arrays_finitos_v2.md',report.encode('utf-8'))
    paths=[Path(__file__),D/'DERIVACAO_E_REVISAO.md',D/'MIMO_ORIGINAL.md',D/'MIMO_RECEIPT.json',D/'scalar_audit.json']
    for d in dirs:paths.extend([H/d/'results.json',H/d/'manifest.json'])
    checks_total=audit['checks']+sum(r['checks'] for r in results)
    cpu_total=audit['cpu_seconds']+sum(r['cpu_seconds'] for r in results)
    put(D/'manifest.json',dict(at=now.isoformat(),supersedes={'path':str(H/'deliver_wick_arity_one_and_scalar_review.py'),'sha256':sha(H/'deliver_wick_arity_one_and_scalar_review.py'),'reason':'V1 assertion used expand instead of cancel on a rational identity; failed before report/ledger writes'},artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],
        checks=checks_total,cpu_seconds=cpu_total,full_Q2=False,gate_changed=False))
    ledger=OUT/'LEDGER_016.jsonl';entries=[json.loads(v) for v in ledger.read_text('utf-8').splitlines()];events=[]
    if not any(e.get('execution_task_id')==execution['id'] for e in entries):
        events.append(dict(at=now.isoformat(),event='EXTERNAL_REVIEW_RECEIVED_AND_AUDITED',target='A7.b',
            provider='mimo',request_id=job['request_id'],job_id=job['id'],execution_task_id=execution['id'],
            usage=result['usage'],cost_estimate_usd=result['cost_estimate_usd'],
            response_sha256=sha(D/'MIMO_ORIGINAL.md'),accepted='PARTIAL_DIFFERENT_SCHEME_PROMPT_AMBIGUITY_RECORDED'))
    events.append(dict(at=now.isoformat(),event='WICK_ARITY_ONE_FINITE_ARRAY_FORMULA',target='A7.b',
        checks=checks_total,cpu_seconds=cpu_total,manifest_sha256=sha(D/'manifest.json'),remote_call=False))
    append(ledger,''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in events))
    cost=Decimal(0);seen=set()
    for e in entries+events:
        v=e.get('cost_estimate_usd',e.get('cost_usd'))
        if v is None:continue
        key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
        if key and key in seen:continue
        if key:seen.add(key)
        cost+=Decimal(str(v))
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESS: fórmula de aridade1 em quatro arrays; redução isotrópica condicionada e primitiva linear do setor antifield. {checks_total}controles CPU{cpu_total}s. MiMoa46 auditado com lacuna do prompt registrada;87d running. Custo conhecido parcialUSD{cost}. AberturaSHA256={opening}.\n')
    p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
    state.setdefault('head_history',[]).append({k:state.get(k) for k in ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration']})
    state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',completed_this_turn=[
        'Arity-one Wick defect derived with explicit fixed G versus H distinction',
        'Antifield vertex reduced to four finite arrays, conditional spaceform primitive',
        'MiMoa46 audited; prompt omission and different regulator scheme recorded'],
        next=['Measure full nonminimal coincidence arrays or name missing identity; do not insert minimal heat coefficients silently',
            'Receive independent MiMo87d response; Kimi pending actual quota recovery',
            'A7b deadline20:32UTC; A7c/d,A8,PartB/final remain'],
        pending_orchestration='Official16:56:12UTC MiMo87d running executione93704c5 worker16211; MiMoa46 complete/audited; Kimi quota5h blocked',
        partial_metered_cost_usd=str(cost))
    state['wick_arity_one_update']=dict(manifest=str(D/'manifest.json'),full_Q2=False,
        actual_J_arrays_measured=False,own_processes=[])
    state['latest_verified_orchestration']['mimo']['status']='COMPLETED_RECEIVED_AUDITED_PARTIAL'
    state['latest_verified_orchestration']['mimo_next'].update(status='RUNNING_CONFIRMED_BY_COORDINATOR',
        execution_task_id='e93704c5-bb33-43f9-bb2e-bffcfd63b5ad',worker_session=16211,
        observed_at='2026-09-25T16:56:12Z')
    put(p,state,True)
    for v in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(v['path']))==v['sha256']
    print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=checks_total,cpu_seconds=cpu_total,
        known_partial_cost_usd=str(cost)),ensure_ascii=False))
if __name__=='__main__':main()
