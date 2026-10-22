"""Audit Kimi709 with Laurent coefficients and alternative Leibniz extensions."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement
import hashlib,json,time
import sympy as s
from logarithmic_contact_engine import A,Q,contact,differentiated,residue,direct_laurent_contact
from balanced_pair_normalization_check_v2 import correction
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,BASE,sha,write,put,append

D=H/'kimi_composite_normalization_audit';tau=s.Symbol('tau');SIG=(1,1,1,1)

def split_delta(u,v):
    value=0
    for (n,xs),c in differentiated(1,tuple(u),SIG).items():
        for (m,ys),d in differentiated(1,tuple(v),SIG).items():
            coeff=c.subs(A,tau*A)*d.subs(A,(1-tau)*A)
            value+=s.diff(coeff,A).subs(A,0)*residue(n+m,tuple(x+y for x,y in zip(xs,ys)),SIG)
    return s.expand(value)

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    source=BASE/'state/handoffs/8639533b-6775-4a5c-8d7f-988659d58c2d_delivery.json'
    j=json.loads(source.read_bytes())['job'];e=j['execution'];r=e['result'];assert e['status']=='result_ready'
    write(D/'KIMI_ORIGINAL.md',r['text'].encode())
    put(D/'RECEIPT.json',dict(request_id=j['request_id'],job_id=j['id'],execution_task_id=e['id'],
        source_sha256=sha(source),prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),
        response_sha256=sha(D/'KIMI_ORIGINAL.md'),usage=r['usage'],model=r['model'],
        cost_estimate_usd=r.get('cost_estimate_usd'),elapsed_seconds=r.get('elapsed_seconds'),
        cost_status='SUBSCRIPTION_COST_NOT_REPORTED_NOT_ZERO'))
    paths=[Path(__file__),H/'logarithmic_contact_engine.py',H/'balanced_pair_normalization_check_v2.py',
        H/'balanced_pair_tensor/results.json',D/'KIMI_ORIGINAL.md',D/'RECEIPT.json']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        claims=['T1 contact=0','T3 contact=+q2/4','First literal-R conflict order2',
            'Euler split residue tau*q2/8','Uniqueness of proposed normalization'],
        controls='Direct Laurent polynomial derivative; formal two-line split compared with previously fixed balanced extension; no changes to graph family',
        sources=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    start=time.process_time();checks=[]
    def eq(name,x,y):
        assert s.expand(x-y)==0,(name,x,y);checks.append(name)
    q2=sum(z*z for z in Q)
    c1=s.expand(sum(contact(1,0,(i,i)) for i in range(4)))
    c2=s.expand(sum(contact(2,0,(i,i)) for i in range(4)))
    eq('literal R Box f minus Box R f',c1,-1)
    eq('literal R Box f2 minus Box R f2',c2,-3*q2/8)
    # Independent meromorphic identity Box z^(a-n)=4(a-n)(a-n+1) z^(a-n-1).
    for n,expected in [(1,c1),(2,c2)]:
        coeff=4*(A-n)*(A-n+1)
        eq('direct meromorphic radial contact '+str(n),-s.diff(coeff,A).subs(A,0)*residue(n+1,(0,0,0,0),SIG),expected)
    eq('first conflict already order1',contact(2,0,(0,)),-Q[0]/8)
    assert c1!=0 and c2!=q2/4;checks.append('Kimi numerical contact claims rejected')
    # Correct single Euler and double Euler Laurent coefficients.
    e1=s.expand((-4*tau)*residue(3,(0,0,0,0),SIG))
    eq('split Euler line1',e1,tau*q2/8)
    eq('split Euler symmetric average',s.expand((e1+e1.subs(tau,1-tau))/2),q2/16)
    double_coeff=16*tau*(1-tau)*A*A*(tau*A-1)*((1-tau)*A-1)
    eq('double Euler finite part zero',s.diff(double_coeff,A).subs(A,0),0)
    # Both assignments have the SAME undifferentiated pair but different balanced-primary contacts.
    ebal=sum(correction((i,i),()) for i in range(4))
    eq('existing balanced Euler',ebal,3*q2/32)
    assert s.expand(ebal-q2/16)!=0;checks.append('uniqueness rejected by two admissible differential assignments')
    # Verify the proposed split extension by all total-order<=3 Leibniz controls.
    # Include order4 coefficients in the derivative side. This does not adopt it as our graph scheme.
    words=[tuple(w) for n in range(5) for w in combinations_with_replacement(range(4),n)]
    table=[]
    for u in words:
        for v in words:
            if len(u)+len(v)>3:continue
            d=split_delta(u,v)
            eq('exchange covariance',d,split_delta(v,u).subs(tau,1-tau))
            sym=s.expand((d+d.subs(tau,1-tau))/2)
            eq('symmetric split tau independent',s.diff(sym,tau),0)
            # Rraw differentiated as a product is linear; its contact is computable directly.
            for i in range(4):
                lhs=split_delta(tuple(sorted(u+(i,))),v)+split_delta(u,tuple(sorted(v+(i,))))-Q[i]*d
                raw_contact=0
                for (n,xs),cu in differentiated(1,u,SIG).items():
                    for (m,ys),cv in differentiated(1,v,SIG).items():
                        xp=tuple(x+y for x,y in zip(xs,ys))
                        # [R,di] on x^xp z^-(n+m) = x^xp Cdi(z^-N);
                        # multiplication by x is -d/dq for delta derivatives.
                        local=contact(n+m,0,(i,))
                        for axis,power in enumerate(xp):local=(-1)**power*s.diff(local,Q[axis],power)
                        raw_contact+=cu.subs(A,0)*cv.subs(A,0)*local
                eq('split Leibniz',lhs,-raw_contact)
            if len(u)+len(v)<=2:table.append(dict(u=u,v=v,split_delta=str(d),symmetric_delta=str(sym)))
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        raw_contacts=dict(Box_f=str(c1),Box_f2=str(c2),first_order_f2=str(contact(2,0,(0,)))),
        split_euler=str(e1),symmetric_split_euler=str(q2/16),balanced_euler=str(ebal),
        family_adopted=False,full_Q2=False,gate_changed=False,
        verdict='SPLIT_LAURENT_RESIDUES_ACCEPTED_LITERAL_R_CONTACTS_AND_UNIQUENESS_REJECTED',table=table)
    put(D/'AUDIT.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — auditoria Kimi709; resposta parcialmente aproveitada]

Aceitos: resíduo radial, contato unilateral tau*q²/8, média q²/16 e
duplo Euler zero na família split especificada. A divisão por CE na
definição do remanescente precisa ser mantida; a resposta inclui CE
novamente numa passagem, misturando contato normalizado e absoluto.

Corrigidos: no R LITERAL da pergunta, [R,Box](f)/CE=-1 e
[R,Box](f²)/CE=-3q²/8, não0 e+q²/4. Derivar a família z^(a-1)
antes de tirar a parte finita NÃO é aplicar R ao Box f que vale0
fora da origem. São mapas diferentes. A identidade meromorfa com
4(a-n)(a-n+1) confirma os dois valores independentemente do motor.
O primeiro conflito com Leibniz já aparece em ordem1:
[R,d_i](f²)/CE=-q_i/8. Na soma A_ii+B_ii falta ainda o fator1/2.

A atribuição split simetrizada é uma extensão diferencial possível
no setor formal considerado, não uma escolha única imposta pela lógica.
Foi verificada por Leibniz até derivadas totais4 e troca de linhas.
Ela dá Euler q²/16; a família balanceada já usada nos grafos dá3q²/32.
Ambas preservam o par sem derivadas e diferem por normalizações locais
dos primários balanceados. Portanto a afirmação de unicidade não procede.
Nenhuma foi escolhida depois de observar o resíduo: os grafos permanecem
na R_bal anterior. Preservar TODO produto derivado de Rliteral e exigir
Leibniz simultaneamente já falha no primeiro contato acima.

Não adotamos a dispensa geral de T1/referência suave nem a nulidade do
produto normal-ordenado Euler fora da casca: a conta numérica de duas
linhas não demonstra essas afirmações sobre a família temporal inteira.
{len(checks)} controles;CPU{result['cpu_seconds']}s,rc0. Recibo e resposta
preservados; consumo deduplicado por execução, assinatura sem custo
unitário informado. Nenhuma nova chamada;Q2curvaOPEN;gate intacto.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO_E_CORRECOES.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_Kimi_normalizacao_composta.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths+[D/'PRE_REGISTER.json',D/'AUDIT.json',D/'DERIVACAO_E_CORRECOES.md']],full_Q2=False))
    ledger=OUT/'LEDGER_016.jsonl';entries=[json.loads(v) for v in ledger.read_text('utf8').splitlines() if v.strip()];events=[]
    if not any(v.get('execution_task_id')==e['id'] for v in entries):
        events.append(dict(at=now.isoformat(),event='EXTERNAL_REVIEW_RECEIVED_AND_AUDITED',target='A7.b',provider='kimi',
            request_id=j['request_id'],job_id=j['id'],execution_task_id=e['id'],usage=r['usage'],cost_estimate_usd=r.get('cost_estimate_usd'),
            prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),response_sha256=sha(D/'KIMI_ORIGINAL.md'),verdict=result['verdict']))
    events.append(dict(at=now.isoformat(),event='KIMI_COMPOSITE_NORMALIZATION_AUDIT',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],manifest_sha256=sha(D/'manifest.json'),remote_call=False))
    append(ledger,''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in events))
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: Kimi709auditado;splitEuleraceito,contatosRliteral/uniquidadecorrigidos;{len(checks)}controles CPU{result["cpu_seconds"]}s.Sem troca de família;Q2OPEN.AberturaSHA256={opening}.\n')
    print(json.dumps({k:v for k,v in result.items() if k!='table'}),flush=True)

if __name__=='__main__':main()
