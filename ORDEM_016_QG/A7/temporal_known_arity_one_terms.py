"""Assemble all already computed arity-one terms of polarized temporal consistency."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement
import ast,json,time
import sympy as s
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

D=H/'temporal_known_arity_one_terms'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    src=H/'antifield_quadratic_primitive_check.py'
    paths=[Path(__file__),src,H/'quartic_antibracket_arity_one/results.json',
        H/'temporal_ward_consistency_polarization/results.json',H/'localized_volume_consistency/results.json']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        target='Known arity-one terms of the actual polarized temporal WZ identity, with no factor1/2 on its two mixed brackets',
        assumptions=['alpha is covariantly constant','a1(Vchi)=alpha integral chi div c',
            'a1((Vchi,Veta)) has the divergence computed previously','compact test support'],
        exclusions=['The chosen comparison cochain is not asserted to equal the measured a2','No classical two-input insertion set to zero'],
        sources=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    start=time.process_time();ns={'s':s}
    nodes=[n for n in ast.parse(src.read_text('utf-8')).body if isinstance(n,ast.FunctionDef)
        and n.name in {'clean','add','scale','mul','atom'}]
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),ns)
    clean,add,scale,mul,atom=[ns[k] for k in ['clean','add','scale','mul','atom']]
    labels=[('c',i) for i in range(4)]+[('dc',m,i) for m in range(4) for i in range(4)]
    labels += [('ddc',m,n,i) for m,n in combinations_with_replacement(range(4),2) for i in range(4)]
    index={v:k for k,v in enumerate(labels)}
    c=lambda i:atom(index['c',i]);dc=lambda m,i:atom(index['dc',m,i])
    ddc=lambda m,n,i:atom(index['ddc',min(m,n),max(m,n),i])
    chi,eta,alpha=s.symbols('chi eta alpha');lx=s.symbols('chi1_0:4');ly=s.symbols('eta1_0:4')
    xx={(i,j):s.Symbol(f'chi2_{min(i,j)}_{max(i,j)}') for i in range(4) for j in range(4)}
    yy={(i,j):s.Symbol(f'eta2_{min(i,j)}_{max(i,j)}') for i in range(4) for j in range(4)}
    def derivative(F,i):
        out={}
        for mon,v in F.items():
            dv=s.diff(v,chi)*lx[i]+s.diff(v,eta)*ly[i]
            dv+=sum(s.diff(v,lx[j])*xx[i,j]+s.diff(v,ly[j])*yy[i,j] for j in range(4))
            out=add(out,{mon:dv})
            for k,idx in enumerate(mon):
                lab=labels[idx]
                image=dc(i,lab[1]) if lab[0]=='c' else ddc(i,lab[1],lab[2])
                assert lab[0]!='ddc'
                term={():v}
                for a in mon[:k]:term=mul(term,atom(a))
                term=mul(term,image)
                for a in mon[k+1:]:term=mul(term,atom(a))
                out=add(out,term)
        return out
    checks=[]
    def eq(label,a,b=None):
        assert not add(a,scale(b or {},-1)),label;checks.append(label)
    w=[add(*(mul(c(j),dc(j,i)) for j in range(4))) for i in range(4)]
    divc=add(*(dc(i,i) for i in range(4)))
    divw=add(*(derivative(w[i],i) for i in range(4)))
    div_c_divc=add(*(derivative(mul(c(i),divc),i) for i in range(4)))
    eq('graded divergence c divc equals divergence w',div_c_divc,divw)
    W=chi*eta;gradW=[eta*lx[i]+chi*ly[i] for i in range(4)]
    # q0 L for L=alpha/2 integral W div(c trh), using q0trh=2divc and odd Leibniz.
    qL=scale(div_c_divc,-alpha*W)
    mixed=scale(add(*(scale(derivative(scale(w[i],chi),i),eta) for i in range(4)),
                    *(scale(derivative(scale(w[i],eta),i),chi) for i in range(4))),alpha)
    Ww_div=scale(add(*(derivative(scale(w[i],W),i) for i in range(4))),alpha)
    eq('full two mixed brackets plus qL is a divergence',add(qL,mixed),Ww_div)
    cgradW=add(*(scale(c(i),gradW[i]) for i in range(4)))
    a1bracket=scale(add(mul(cgradW,divc),scale(add(*(scale(w[i],gradW[i]) for i in range(4))),-1)),alpha)
    a1div=scale(add(*(derivative(mul(cgradW,c(i)),i) for i in range(4))),alpha)
    eq('previous composite antibracket density reproduced',a1bracket,a1div)
    eq('all known terms reduce to explicit divergence',add(qL,mixed,scale(a1bracket,-1)),add(Ww_div,scale(a1div,-1)))
    # Integrated forms: retain derivatives of switching functions, discard only complete divergences.
    gradWw=scale(add(*(scale(w[i],gradW[i]) for i in range(4))),alpha)
    eq('qL integrated representative',add(qL,scale(gradWw,-1)),scale(Ww_div,-1))
    eq('mixed integrated representative',add(mixed,gradWw),scale(Ww_div,2))
    assert gradWw;checks.append('mixed brackets are not separately zero for variable cutoffs')
    assert add(qL,scale(mixed,s.Rational(1,2)))
    checks.append('earlier half-weighted cochain identity is a different expression')
    # Curvature term potentially separating the divergences vanishes by ghost antisymmetry.
    ric={(i,j):s.Symbol(f'Ric_{min(i,j)}_{max(i,j)}') for i in range(4) for j in range(4)}
    eq('symmetric Ricci times two ghosts vanishes',add(*(scale(mul(c(i),c(j)),ric[i,j]) for i in range(4) for j in range(4))))
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        L='alpha/2 integral chi eta div(c trh)',
        density_identity='q0 L_density + mixed_brackets_density - a1_bracket_density = alpha div[chi eta w - (c.grad(chi eta)) c]',
        integrated_reduced_consistency='q0[a2(Vchi,Veta)-L]=a2(q0Vchi,Veta)+a2(q0Veta,Vchi)',
        actual_a2_identified_with_L=False,remaining_two_input_insertions_computed=False,
        hypotheses=['Same prescribed family','Constant alpha','Compact support','Previous arity-one inventory'],full_Q2=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — todos os termos conhecidos de aridade1 na consistência temporal]

Escreva a1(Vchi)=alpha int chi div c, com alpha constante na referência
espaço-forma já calculada. O composto a1((Vchi,Veta)) é a divergência
anterior, cuja integral compacta zera. Os DOIS colchetes mistos da
identidade temporal, sem fator1/2, dão após integração por partes

 (Vchi,a1(Veta))+(Veta,a1(Vchi))=-alpha int d(chi eta).w,
 w=c.nabla c.

Reutilize a cochain de volume já existente, como expressão de comparação:
 Lchi,eta=alpha/2 int chi eta div(c trh).
 q0L=+alpha int d(chi eta).w.

O CAS verifica a identidade de DENSIDADES, mais forte que apenas descartar
uma integral: q0L+colchetes-a1(composto) é
alpha div[chi eta w-(c.grad(chi eta))c]. A passagem covariante usa
Ric_ij c^i c^j=0 por simetria; alpha deve permanecer constante.

Logo a condição temporal previamente extraída se reduz a

 q0[a2(Vchi,Veta)-Lchi,eta]
  =a2(q0Vchi,Veta)+a2(q0Veta,Vchi).

O lado direito NÃO foi anulado. A expressão L não foi identificada com
o a2 real: apenas retira, de forma explícita, a fonte já conhecida de
aridade1 da equação. As duas inserções clássicas são exatamente o cálculo
restante nesse elo. Isso não acrescenta um operador físico ou uma hipótese
de fechamento. A identidade anterior com metade dos colchetes permanece
correta para outra expressão; não é a polarização temporal usada aqui.

{len(checks)} controles exatos, CPU{result['cpu_seconds']}s,rc0.
Nenhum original/kernel/gate alterado. AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_termos_conhecidos_Ward_temporal.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='TEMPORAL_KNOWN_ARITY_ONE_TERMS',target='A7.b',
        checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: aridade1 integrada à consistência temporal; q0(a2-L)=a2(q0V,V)+a2(q0V,V)polarizado, inserções não anuladas;{len(checks)}controles CPU{result["cpu_seconds"]}s. Q2OPEN;aberturaSHA256={opening}.\n')
    state_path=H/'CONTINUIDADE.json';state=json.loads(state_path.read_bytes())
    state.setdefault('head_history',[]).append({k:state.get(k) for k in ['at','completed_this_turn','next']})
    state['at']=now.isoformat();state['completed_this_turn'].append('All known arity-one terms assembled: reduced temporal consistency q0(a2-L)=two classical insertions, without setting them to zero')
    state['next']=[t for t in state['next'] if not t.startswith('Complete the known arity1')]
    state['temporal_known_arity_one_update']=dict(manifest=str(D/'manifest.json'),results=result)
    put(state_path,state,True)
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
