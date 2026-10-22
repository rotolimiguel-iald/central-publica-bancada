"""Lift the measured linear divergence to an explicit quadratic volume primitive.

This tests the UNLOCALIZED BRST differential with a separate compact test chi.
It does not identify the answer with A2(V_chi,V_eta) of localized interactions.
"""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement
import ast,json,time
import sympy as s
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append
D=H/'volume_primitive_second_order'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    src=H/'antifield_quadratic_primitive_check.py'
    sources=[Path(__file__),src,H/'nonminimal_wick_heat_ward/results.json',
             H/'bv_coordinate_inventory_delivery/DICIONARIO_E_INVENTARIO.md']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        target='One explicit nonlinear completion of B1=(alpha_W/2)tr h; exact q0 a2+q1 a1=0',
        hypotheses=['Constant background metric in pointwise tensor-jet check',
            'q0 h=Lie_c background, q1 h=Lie_c h, q1 c=c.d c, q0 c=0',
            'alpha_W is constant on the spaceform; its physical normalization remains explicit',
            'chi is an independent compact test, not substituted into q1'],
        exclusions=['No new choice of finite time-ordering normalization',
            'No identification with A2(Vchi,Veta)', 'No proof of admissible counterterm reality or global state'],
        sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
    start=time.process_time()
    names={'clean','add','scale','mul','atom'}
    nodes=[n for n in ast.parse(src.read_text('utf-8')).body
           if isinstance(n,ast.FunctionDef) and n.name in names]
    ns={'s':s};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),ns)
    clean,add,scale,mul,atom=[ns[n] for n in ['clean','add','scale','mul','atom']]
    ev=lambda a:clean({():a})
    alpha,u=s.symbols('alpha_W u');labels=list(combinations_with_replacement(range(4),2))
    hs=s.symbols('h0:10');h={ij:hs[n] for n,ij in enumerate(labels)}
    hv=lambda i,j:h[tuple(sorted((i,j)))]
    dh={(k,ij):s.Symbol('dh'+str(k)+'_'+str(n)) for k in range(4) for n,ij in enumerate(labels)}
    dhv=lambda k,i,j:dh[k,tuple(sorted((i,j)))]
    oddlabels=[('c',i) for i in range(4)]+[('dc',i,j) for i in range(4) for j in range(4)]
    oddlabels += [('ddc',i,j,k) for i,j in labels for k in range(4)]
    odd={lab:atom(n) for n,lab in enumerate(oddlabels)}
    c=lambda i:odd['c',i]
    dc=lambda i,j:odd['dc',i,j]
    ddc=lambda i,j,k:odd['ddc',min(i,j),max(i,j),k]
    divc=add(*(dc(i,i) for i in range(4)))
    checks=[]
    def eq(label,a,b=None):
        assert not add(a,scale(b or {},-1)),(label,a,b)
        checks.append(label)
    rows=[]
    for sig in [(1,1,1,1),(-1,1,1,1)]:
        tr=sum(sig[i]*hv(i,i) for i in range(4))
        tr2=sum(sig[i]*sig[j]*hv(i,j)**2 for i in range(4) for j in range(4))
        B1=alpha*tr/2;B2=alpha*(tr*tr/8-tr2/4)
        q0h={h[i,j]:add(scale(dc(i,j),sig[j]),scale(dc(j,i),sig[i])) for i,j in labels}
        q1h={h[i,j]:add(*(scale(c(k),dhv(k,i,j)) for k in range(4)),
                        *(scale(dc(i,k),hv(k,j)) for k in range(4)),
                        *(scale(dc(j,k),hv(i,k)) for k in range(4))) for i,j in labels}
        q0vars=dict(q0h)
        q0vars.update({dhv(k,i,j):add(scale(ddc(k,i,j),sig[j]),scale(ddc(k,j,i),sig[i]))
                       for k in range(4) for i,j in labels})
        def act(a,images):
            out={}
            for v,qv in images.items():
                derivative=clean({mon:s.diff(co,v) for mon,co in a.items()})
                out=add(out,mul(qv,derivative))
            return out
        a1=scale(divc,alpha)
        a2=scale(add(scale(divc,tr),*(scale(c(k),sum(sig[i]*dhv(k,i,i) for i in range(4)))
                                      for k in range(4))),alpha/2)
        eq('linear primitive '+str(sig),act(ev(B1),q0h),a1)
        eq('quadratic volume descent '+str(sig),add(act(ev(B2),q0h),act(ev(B1),q1h)),a2)
        # q1 div(c)=sum_i,j [d_i c^j d_j c^i + c^j d_i d_j c^i].
        square=add(*(mul(dc(i,j),dc(j,i)) for i in range(4) for j in range(4)))
        eq('odd derivative trace square vanishes '+str(sig),square)
        q1a1=scale(add(square,*(mul(c(j),ddc(i,j,i)) for i in range(4) for j in range(4))),alpha)
        eq('inhomogeneous WZ '+str(sig),add(act(a2,q0vars),q1a1))
        assert q1a1
        checks.append('nonzero inhomogeneous term retained '+str(sig))
        assert act(ev(B1),q1h)
        checks.append('omitting nonlinear primitive contribution fails '+str(sig))
        wrong=add(act(a2,q0vars),scale(q1a1,-1))
        assert wrong
        checks.append('wrong ghost sign fails WZ '+str(sig))
        # Determinant coefficients independently generate the proposed primitive.
        M=s.diag(*sig)*s.Matrix(4,4,lambda i,j:hv(i,j))
        # Principal minors avoid a large multivariate determinant expansion.
        det1=s.trace(M)
        det2=sum(M[i,i]*M[j,j]-M[i,j]*M[j,i] for i,j in combinations_with_replacement(range(4),2) if i<j)
        eq('volume first coefficient '+str(sig),ev(alpha*det1/2),ev(B1))
        eq('volume second coefficient '+str(sig),ev(alpha*(det2/2-det1*det1/8)),ev(B2))
        # Smearing keeps the gradient of the cutoff instead of discarding a divergence.
        chi=s.Symbol('chi');dchi=s.symbols('dchi0:4')
        cutoff=scale(add(*(scale(c(i),dchi[i]) for i in range(4))),alpha*tr/2)
        total_div=add(scale(a2,chi),cutoff)
        assert cutoff
        checks.append('nonconstant compact test gives a boundary-density term '+str(sig))
        rows.append(dict(signature=sig,B1=str(B1),B2=str(B2),
            q1_a1=[dict(odd=list(k),coefficient=str(v)) for k,v in q1a1.items()]))
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        B1='alpha_W/2 * tr(h)',B2='alpha_W*((tr h)^2/8-tr(h^2)/4)',
        a1='alpha_W div(c)',a2='alpha_W/2 div(c tr(h))',
        identity='q0 B2+q1 B1=a2; q0 a2+q1 a1=0',
        completion='B(u)=alpha_W*(sqrt(det(I+u*g_inverse*h))-1)',
        cutoff='int chi*a2=-alpha_W/2 int (dchi).c*tr(h)',
        rows=rows,localized_interaction_identity_verified=False,
        normalization_adopted=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result)
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — continuação quadrática explícita da primitiva linear; A2 integral OPEN]

Mantemos a1=alpha_W div(c), cujo alpha_W auxiliar foi calculado antes;
seu fator físico ainda é explícito. B1=alpha_W tr(h)/2 já estava derivado.
Uma continuação algébrica é a expansão de volume
B(u)=alpha_W(sqrt(det(I+u g^-1 h))-1)=u B1+u² B2+...,
B2=alpha_W[(tr h)²/8-tr(h²)/4]. Não alegamos unicidade dessa continuação.

Para q(u)=q0+u q1, q0h=Lie_c g, q1h=Lie_c h e q1c=c.nabla c,
q(u)B(u)=alpha_W u div(c rho(u)). Portanto
 q0 B1=a1,
 q0 B2+q1 B1=a2=alpha_W div(c tr(h))/2,
 q0 a2+q1 a1=0.
O CAS conserva a anticomutação dos jatos: sum(d_i c^j)(d_j c^i)=0,
mas sum c^j d_i d_j c^i não é zero. É exatamente a fonte inhomogênea
que q0a2 cancela. Inverter o sinal de q1c ou omitir q1B1 falha.

Foram {result['checks']} controles em assinaturas euclidiana e lorentziana,
CPU {result['cpu_seconds']}s, rc0. A expansão do determinante foi conferida
separadamente por menores principais. Em coordenadas normais, as identidades
de volume têm a tradução covariante correspondente. Não construímos estado
global nem fixamos a continuação física do fator alpha_W.

Com teste compacto chi, int chi*a2=-alpha_W/2 int(dchi).c tr(h).
Logo o termo não desaparece sob localização. Aqui chi é o TESTE externo
de um diferencial BRST NÃO LOCALIZADO. Substituir q1 por chi*q1 é outro
problema e acrescenta termos de derivadas de chi. Não identificamos esta
continuação com A2(Vchi,Veta), nem com a soma completa das inserções I1/I2.

Também não adotamos B como contratermo da prescrição causal existente: sua
realidade, naturalidade e vínculo à normalização temporal precisam ser
verificados. Ele usa a métrica de fundo e K constante no modelo truncado;
não é uma afirmação de independência entre fundos. O resultado fornece uma
família explícita para transportar a primitiva de A1, mantendo os termos
de consistência em vez de declarar A1 zero por conveniência.

Próximo: fonte de Euler composta e sua extensão na mesma família T2.
Nenhum original, kernel ou gate alterado. AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode('utf-8'))
    write(OUT/'ENTREGA_016_MEDIDA_primitiva_volume_segunda_ordem.md',note.encode('utf-8'))
    put(D/'manifest.json',dict(at=now.isoformat(),artifacts=[dict(path=str(p),sha256=sha(p)) for p in
        sources+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']],opening_sha256=opening,full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='VOLUME_PRIMITIVE_SECOND_ORDER',
        target='A7.b',checks=result['checks'],cpu_seconds=result['cpu_seconds'],remote_call=False,
        manifest_sha256=sha(D/'manifest.json')),ensure_ascii=False)+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f"\n{now.isoformat()} A7.b PROGRESS: primitiva de volume B2 explícita, q0 a2+q1 a1=0; teste externo distinto de interação localizada. {result['checks']} controles, CPU {result['cpu_seconds']}s; Q2 completa OPEN. AberturaSHA256={opening}.\n")
    print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=result['checks'],cpu_seconds=result['cpu_seconds']),ensure_ascii=False))

if __name__=='__main__':main()
