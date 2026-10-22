"""Explicit balanced two-line extension, preserving raw results as another prescription."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product,combinations_with_replacement
from functools import lru_cache
import json,time
import sympy as s
from full_loop_extension_engine import propagator_derivative as f,contact,Q
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append
D=H/'balanced_pair_normalization_v2'

@lru_cache(None)
def balanced(word):
    """D_bal=(D1-D2)/2 applied before identifying the two relative coordinates."""
    out=0
    for mask in product((0,1),repeat=len(word)):
        left=tuple(i for i,b in zip(word,mask) if not b)
        right=tuple(i for i,b in zip(word,mask) if b)
        out+=(-1)**len(right)*f(left)*f(right)/s.Integer(2)**len(word)
    return s.expand(out)

@lru_cache(None)
def correction(left,right):
    """(R_bal(f_left*f_right)-R_raw(f_left*f_right))/CE, CE=-4*pi^2."""
    slots=tuple((0,i) for i in left)+tuple((1,i) for i in right)
    out=0
    for mask in product((0,1),repeat=len(slots)):
        total=[];bal=[];co=s.Integer(1)
        for (side,i),is_bal in zip(slots,mask):
            if is_bal:
                bal.append(i);co*=(-1)**side
            else:
                total.append(i);co/=2
        if total:
            out-=co*contact(balanced(tuple(sorted(bal))),tuple(sorted(total)))
    return s.expand(out)

def words(n):return list(combinations_with_replacement(range(4),n))

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    sources=[Path(__file__),H/'balanced_pair_normalization_check.py',H/'balanced_pair_normalization/PRE_REGISTER.json',H/'full_loop_extension_engine.py',H/'logarithmic_contact_engine.py',
             H/'free_euler_insertion_contact/results.json',H/'euler_span_mixed_review_delivery/DERIVACAO.md']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        previous_failure='v1 rc1 at tau assertion: coeff applied before expansion; retained unchanged. v2 only fixes coefficient extraction and records custody.',
        target='Explicit local corrections for the two-line balanced differential extension up to total order4',
        prescription='D1=Dtot/2+Dbal, D2=Dtot/2-Dbal. Extend balanced primaries by existing R; commute every total derivative outside R.',
        relation_to_previous='New explicit completion R_bal, NOT identical to raw R on all differentiated products. Earlier results remain unchanged.',
        no_fit='No tau or Ward residual used to choose coefficients',
        negative_controls=['Raw insertion loses total derivative identity','A single regulator allocation tau cannot match both balanced Euler lines'],
        scope='Principal Euclidean scalar pair; no complete tensor/curvature/BRST family claimed',
        sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
    start=time.process_time();checks=[]
    def eq(label,a,b=0):
        assert s.expand(a-b)==0,(label,a,b);checks.append(label)
    table=[]
    for degree in range(5):
        for nl in range(degree+1):
            for left in words(nl):
                for right in words(degree-nl):
                    delta=correction(left,right)
                    eq('line exchange '+str((left,right)),delta,correction(right,left))
                    table.append(dict(left=left,right=right,delta_over_CE=str(delta)))
                    if degree<=3:
                        raw=s.expand(f(left)*f(right))
                        for i in range(4):
                            dleft=tuple(sorted(left+(i,)));dright=tuple(sorted(right+(i,)))
                            lhs=correction(dleft,right)+correction(left,dright)-Q[i]*delta
                            eq('total derivative identity '+str((left,right,i)),lhs,-contact(raw,(i,)))
    eq('undifferentiated pair unchanged',correction((),()))
    q2=sum(q*q for q in Q)
    first=sum(correction((i,i),()) for i in range(4))
    second=sum(correction((),(i,i)) for i in range(4))
    cross=sum(correction((i,),(i,)) for i in range(4))
    eq('Euler first line',first,3*q2/32)
    eq('Euler second line',second,3*q2/32)
    eq('crossed gradient finite correction',cross,3*q2/32)
    eq('full product Laplacian',first+second+2*cross,3*q2/8)
    tau=s.Symbol('tau')
    values1=s.solve(s.expand(tau*q2/8-first).coeff(Q[0],2),tau)
    values2=s.solve(s.expand((1-tau)*q2/8-second).coeff(Q[0],2),tau)
    assert values1==[s.Rational(3,4)] and values2==[s.Rational(1,4)]
    assert set(values1).isdisjoint(values2)
    checks.append('no single tau reproduces both balanced Euler insertions')
    assert contact(f(())**2,(0,))!=0
    checks.append('raw differentiated pair is not action-Ward-normalized')
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        pair_count=len(table),table=table,
        Euler_first_over_CE=str(first),Euler_second_over_CE=str(second),cross_correction_over_CE=str(cross),
        first_tau=str(values1[0]),second_tau=str(values2[0]),
        conclusion='Explicit balanced completion satisfies the tested total-derivative identities and is not the old scalar tau allocation family',
        previous_tensor_results_reused_without_conversion=False,
        complete_time_ordered_family=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result)
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — normalização diferencial explícita do par escalar; Q2 completa OPEN]

Correção do teste: v1 terminou rc1 porque coeff(q0,2) foi aplicado antes
da expansão algébrica, perdendo o termo tau. A v2 expande antes de extrair;
não altera a prescrição nem seus coeficientes. Original e pré-registro preservados.

Declaramos ANTES da conta uma continuação por derivadas balanceadas:
Dtot=D1+D2, Dbal=(D1-D2)/2. Os primários Dbal^v(fg) recebem a extensão
radial R anterior; as derivadas Dtot são aplicadas DEPOIS de estender.
Para derivadas individuais, expandimos D1=Dtot/2+Dbal e D2=Dtot/2-Dbal.
Cada termo Dtot^u R(Dbal^v(fg)) difere de R(Dtot^u Dbal^v(fg)) pelo
contato -CE C_u já calculável no motor existente. Nenhum resíduo Ward foi
usado para ajustar coeficientes. A tabela tem {len(table)} pares até ordem4.

Esta é R_bal, uma continuação explícita. O par SEM derivadas é o mesmo,
mas produtos de linhas derivadas recebem correções locais. Portanto os
números anteriores de R_raw não podem ser somados aos novos sem conversão.
Isso não altera os artefatos anteriores nem seleciona uma leitura física.

Para f=g=1/z, no auxiliar euclidiano, obtivemos
 R_bal((Delta f)g)/CE=3q²/32,
 R_bal(f(Delta g))/CE=3q²/32,
 R_bal(grad f.grad g)=4R(z^-3)+CE*3q²/32.
O total pela regra de Leibniz é8R(z^-3)+CE*3q²/8, como exige Delta R(z^-2).
Derivação curta: Dbal(fg)=0 e Dbal²(fg)=-2z^-3; logo
R_bal((Delta f)g)=Delta R(z^-2)/4-2R(z^-3)=CE*3q²/32.

A família de alocação anterior tinha Euler1=tau q²/8 e Euler2=(1-tau)q²/8.
Igualar o primeiro requer tau=3/4; igualar o segundo requer tau=1/4.
Não existe tau único que reproduza esta normalização simétrica. Assim,
o teste anterior de não pertencimento ao span de dois kernels Euler não
excluía todas as normalizações diferenciais: R_bal está fora daquela família.
Não se está apagando o teste anterior; seu domínio fica identificado.

A identidade verificada para todas as entradas da tabela com ordem até3 é
 DeltaR_(u+i,v)+DeltaR_(u,v+i)-q_i DeltaR_(u,v)
 =-C_i((D^u f)(D^v g)). Ela expressa derivar a inserção total antes/depois
da extensão. Testamos também troca das linhas e controles de Laplaciano.
{len(checks)} controles exatos, CPU {result['cpu_seconds']}s, rc0.

Próximo: transportar as contrações tensoriais para R_bal e conferir as
condições restantes de uma única família T2, inclusive curvatura, graus
Grassmann e inserções lineares. Só a normalização diferencial escalar foi
construída aqui; não é Q2 nem uma prova completa de causalidade/realidade.
Não adotamos tau, não movemos gate e não alteramos fonte canônica.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode('utf-8'))
    write(OUT/'ENTREGA_016_MEDIDA_normalizacao_balanceada_par.md',note.encode('utf-8'))
    put(D/'manifest.json',dict(at=now.isoformat(),artifacts=[dict(path=str(p),sha256=sha(p)) for p in
        sources+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']],full_Q2=False,opening_sha256=opening))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='BALANCED_PAIR_DIFFERENTIAL_COMPLETION',target='A7.b',
        checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')),ensure_ascii=False)+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f"\n{now.isoformat()} A7.b PROGRESS: R_bal explícita, {len(table)} pares, {len(checks)} controles CPU{result['cpu_seconds']}s. Euler simétrico3q²/32 fora da família tau anterior. Q2 completa OPEN. AberturaSHA256={opening}.\n")
    p=H/'CONTINUIDADE.json';st=json.loads(p.read_bytes())
    st.setdefault('head_history',[]).append({k:st.get(k) for k in ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration']})
    st.update(at=now.isoformat(),previous_goal_turn='PROGRESS',completed_this_turn=[
        'Explicit balanced scalar completion derived before evaluation, preserving raw artifacts',
        'Euler contacts3q²/32 on both lines; not realizable by one tau in old allocation family',
        'All differential composition and exchange checks passed through declared orders'],
        next=['Transport actual tensor contractions to R_bal with explicit local corrections; do not mix raw and balanced coefficients',
              'Verify remaining same-T2 conditions including curved kernels and composite Euler source',
              'Preserve Kimi pending units under quota; no repeat',
              'A7b deadline20:32UTC; A7c/d,A8,PartB/final remain'])
    st['balanced_pair_update']=dict(manifest=str(D/'manifest.json'),full_Q2=False)
    put(p,st,True)
    for a in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
    print(json.dumps(dict(manifest=str(D/'manifest.json'),pairs=len(table),checks=len(checks),cpu_seconds=result['cpu_seconds']),ensure_ascii=False),flush=True)

if __name__=='__main__':main()
