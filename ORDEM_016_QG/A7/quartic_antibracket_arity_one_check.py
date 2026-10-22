"""Compute a1((V_chi,V_eta)) from the already fixed spaceform defect arrays."""
from pathlib import Path
from datetime import datetime, timezone
from itertools import combinations_with_replacement
import ast,json,time
import sympy as s
from metric_coincident_jet_engine_v2 import metric_fiber
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

D=H/'quartic_antibracket_arity_one'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    src=H/'antifield_quadratic_primitive_check.py'
    paths=[Path(__file__),src,H/'bv_coordinate_inventory_delivery/DICIONARIO_E_INVENTARIO.md',
        H/'nonminimal_wick_heat_ward/results.json',H/'temporal_ward_consistency_polarization/results.json']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        target='Compute the one-input anomaly of the quadratic antibracket of localized cubic vertices, retaining all cutoff terms',
        hypotheses=['Coordinate bracket B already audited','a1 has only Euler antifield/field contractions in this inventory',
            'Jh0=aTL PTL+aTr Ptr;Jc0=d Id;first coincidence jets vanish on the natural parity-even constant spaceform',
            'Antifield vertices hdag Lie_c h+cdag c.nabla c; other cubic vertices contain fields only',
            'Constant scalar background: scalar antifield vertex has one scalar derivative, whose defect first jet vanishes'],
        prescription='Same arity-one heat/Wick prescription, no new parameter or counterterm',
        exclusions=['Not full A2','No claim about all curved two-input kernels','Local normal-frame jet algebra; compact support required to remove total divergence'],
        sources=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    start=time.process_time();names={'clean','add','scale','mul','atom'}
    nodes=[n for n in ast.parse(src.read_text('utf-8')).body if isinstance(n,ast.FunctionDef) and n.name in names]
    ns={'s':s};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),ns)
    clean,add,scale,mul,atom=[ns[n] for n in ['clean','add','scale','mul','atom']]
    fiber=metric_fiber();labels=fiber['labels'];idx=lambda i,j:labels.index(tuple(sorted((i,j))))
    h=s.symbols('h0:10');dh={(m,A):s.Symbol(f'dh_{m}_{A}') for m in range(4) for A in range(10)}
    ddh={(m,n,A):s.Symbol(f'ddh_{m}_{n}_{A}') for m,n in combinations_with_replacement(range(4),2) for A in range(10)}
    oddlabels=[('c',i) for i in range(4)]+[('dc',m,i) for m in range(4) for i in range(4)]
    oddlabels += [('ddc',m,n,i) for m,n in combinations_with_replacement(range(4),2) for i in range(4)]
    O={key:k for k,key in enumerate(oddlabels)}
    c=lambda i:atom(O['c',i]);dc=lambda m,i:atom(O['dc',m,i])
    ddc=lambda m,n,i:atom(O['ddc',min(m,n),max(m,n),i])
    chi,eta,atl,atr,d=s.symbols('chi eta aTL aTr d');lam=s.symbols('lambda0:4');mu=s.symbols('mu0:4')
    l2={(m,n):s.Symbol(f'chi2_{min(m,n)}_{max(m,n)}') for m in range(4) for n in range(4)}
    m2={(m,n):s.Symbol(f'eta2_{min(m,n)}_{max(m,n)}') for m in range(4) for n in range(4)}
    def even_der(F,z):return clean({mon:s.diff(v,z) for mon,v in F.items()})
    def odd_der(F,i):
        out={}
        for mon,v in F.items():
            if i in mon:
                k=mon.index(i);out[mon[:k]+mon[k+1:]]=(-1)**k*v
        return clean(out)
    def derivative(F,m):
        out={}
        for mon,v in F.items():
            vdiff=s.diff(v,chi)*lam[m]+s.diff(v,eta)*mu[m]
            vdiff+=sum(s.diff(v,lam[n])*l2[m,n]+s.diff(v,mu[n])*m2[m,n] for n in range(4))
            vdiff+=sum(s.diff(v,h[A])*dh[m,A] for A in range(10))
            vdiff+=sum(s.diff(v,dh[n,A])*ddh[min(m,n),max(m,n),A] for n in range(4) for A in range(10))
            out=add(out,{mon:vdiff})
            for j,k in enumerate(mon):
                label=oddlabels[k]
                if label[0]=='c':image=dc(m,label[1])
                elif label[0]=='dc':image=ddc(m,label[1],label[2])
                else:raise AssertionError('third odd jet not needed')
                term={():v}
                for z in mon[:j]:term=mul(term,atom(z))
                term=mul(term,image)
                for z in mon[j+1:]:term=mul(term,atom(z))
                out=add(out,term)
        return out
    Z=[]
    for A,(i,j) in enumerate(labels):
        Z.append(add(*(scale(c(m),dh[m,A]) for m in range(4)),
            *(scale(dc(j,m),h[idx(i,m)]) for m in range(4)),
            *(scale(dc(i,m),h[idx(j,m)]) for m in range(4))))
    w=[add(*(mul(c(m),dc(m,i)) for m in range(4))) for i in range(4)]
    qh=[scale(z,chi) for z in Z];qc=[scale(z,chi) for z in w]
    qdh={(m,A):derivative(qh[A],m) for m in range(4) for A in range(10)}
    qdc={(m,i):derivative(qc[i],m) for m in range(4) for i in range(4)}
    def q(F):
        out={}
        for A in range(10):out=add(out,mul(qh[A],even_der(F,h[A])))
        for m in range(4):
            for A in range(10):out=add(out,mul(qdh[m,A],even_der(F,dh[m,A])))
        for label,k in O.items():
            if label[0]=='c':image=qc[label[1]]
            elif label[0]=='dc':image=qdc[label[1],label[2]]
            else:continue
            out=add(out,mul(image,odd_der(F,k)))
        return out
    checks=[]
    def eq(name,F,G=None):
        assert not add(F,scale(G or {},-1)),name
        checks.append(name)
    C=add(*(scale(c(m),lam[m]) for m in range(4)));divc=add(*(dc(m,m) for m in range(4)))
    lambdaw=add(*(scale(w[m],lam[m]) for m in range(4)))
    square_h=[];square_c=[]
    for A,(i,j) in enumerate(labels):
        actual=q(qh[A]);expected=scale(add(scale(mul(C,Z[A]),-1),
            *(scale(w[r],lam[i]*h[idx(j,r)]+lam[j]*h[idx(i,r)]) for r in range(4))),chi)
        eq('localized nonlinear square h '+str(A),actual,expected);square_h.append(actual)
        eq('unlocalized nonlinear square h '+str(A),clean({m:v.subs(dict.fromkeys(lam,0)) for m,v in actual.items()}))
    for i in range(4):
        actual=q(qc[i]);expected=scale(mul(C,w[i]),-chi)
        eq('localized nonlinear square c '+str(i),actual,expected);square_c.append(actual)
    # For odd I2=1/2(V,V), coordinates B give I2=-hdag*q1chi²h+cdag*q1chi²c.
    J=atl*fiber['tl']+atr*fiber['ptr'];metric={}
    for A in range(10):
        for B in range(10):
            if J[A,B]:metric=add(metric,scale(even_der(square_h[A],h[B]),-J[A,B]))
    ghost=add(*(scale(odd_der(square_c[i],O['c',i]),d) for i in range(4)))
    core=scale(add(mul(C,divc),scale(lambdaw,-1)),chi)
    mh=s.Rational(9,2)*atl+atr/2;alpha=mh+d
    eq('metric arity-one quadratic bracket',metric,scale(core,mh))
    eq('ghost arity-one quadratic bracket',ghost,scale(core,d))
    eq('same coefficient as measured cubic anomaly',add(metric,ghost),scale(core,alpha))
    # Exact divergence, including second cutoff derivatives; no discarded boundary by fiat.
    currents=[scale(mul(C,c(n)),chi) for n in range(4)]
    divergence=add(*(derivative(currents[n],n) for n in range(4)))
    eq('quadratic bracket density is a total divergence',divergence,core)
    assert core;checks.append('local density is not identically zero')
    substitute=lambda F,rule:clean({m:v.subs(rule,simultaneous=True) for m,v in F.items()})
    mixed=add(substitute(core,{chi:chi+eta,**{lam[i]:lam[i]+mu[i] for i in range(4)}}),
        scale(core,-1),scale(substitute(core,{chi:eta,**dict(zip(lam,mu))}),-1))
    mixedC=add(*(scale(c(i),eta*lam[i]+chi*mu[i]) for i in range(4)))
    mixedexpected=add(mul(mixedC,divc),scale(add(*(scale(w[i],eta*lam[i]+chi*mu[i]) for i in range(4))),-1))
    eq('polarized antibracket factor',mixed,mixedexpected)
    mixeddiv=add(*(derivative(mul(mixedC,c(n)),n) for n in range(4)))
    eq('mixed density exact divergence',mixeddiv,mixed)
    eq('equal cutoff gives twice I2',substitute(mixed,{eta:chi,**dict(zip(mu,lam))}),scale(core,2))
    # Check the entire difference is seen; dropping either contraction channel fails.
    assert metric and ghost;checks.append('neither metric nor ghost channel omitted')
    assert add(scale(core,alpha),scale(metric,-1));checks.append('missing ghost contribution detected')
    # Numeric heat coefficient follows from the already stored local result, not a fit.
    actual_alpha=s.expand(alpha.subs({atl:s.Rational(137,60),atr:s.Rational(579,20),d:s.Rational(179,20)}))
    assert actual_alpha==s.Rational(337,10);checks.append('existing heat coefficient reproduced')
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        alpha=str(alpha),normalized_auxiliary_heat_alpha=str(actual_alpha)+' K²',
        a1_I2_density='alpha chi*((c.grad chi)*div c-grad chi.(c.grad c))',
        a1_mixed_bracket_density='alpha*((c.grad(chi eta))*div c-grad(chi eta).(c.grad c))',
        divergence_current='alpha*(c.grad(chi eta))*c^nu',
        integrated_a1_antibracket_zero=True,requires_compact_support=True,local_density_zero=False,
        scope='Conditional arity-one composite contact in the declared constant-spaceform heat/Wick inventory',
        full_Q2=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — a1 do antibracket composto, no inventário/prescrição condicionados; Q2 OPEN]

No mesmo espaço-forma constante e par, Jh0=aTL PTL+aTr Ptr, Jc0=d I,
e os primeiros jatos Jh1,Jc1 são zero. Mantivemos os antifields assinados B
já auditados. Escreva Z=Lie_c h,w=c.nabla c,C=c.grad chi.
O diferencial não linear localizado obedece, por cálculo graduado direto,

 q1chi²h_mn=chi[-C Z_mn+(d_m chi)h_nr w^r+(d_n chi)h_mr w^r],
 q1chi²c^i=-chi C w^i.

Isso determina a parte de antifields de I2chi=(Vchi,Vchi)/2:
 -hdag q1chi²h+cdag q1chi²c. O restante só tem campos e é morto por a1
nas hipóteses de Ward entre campos deste inventário. As contribuições
métrica e ghost usam, respectivamente, 9aTL/2+aTr/2 e d. Sua soma é
alpha=9aTL/2+aTr/2+d, o mesmo coeficiente de a1(Vchi)=alpha int chi div c.
No auxiliar normalizado anterior alpha=337K²/10, sem ajuste novo.

Antes de integrar:
 a1(I2chi)=alpha chi[(c.grad chi)div c-grad chi.w]
          =alpha div[chi(c.grad chi)c].

Polarizando os VÉRTICES, sem duplicar S0, obtém-se
 a1((Vchi,Veta))=alpha div[(c.grad(chi eta))c].

Portanto sua integral zera para cutoffs compactos e alpha constante.
A densidade NÃO é zero: cancelam-se após a derivação os termos simétricos
de Hessiana contra os dois ghosts antissimétricos. Não foi descartada uma
derivada isolada de cutoff. Se alpha varia, integração por partes deixa
-grad(alpha).[(c.grad(chi eta))c]; o resultado não se estende a esse caso.
O vértice antifield escalar adicional só contrai o primeiro jato escalar,
zero sob as mesmas hipóteses naturais de fundo constante; isto não retira
loops escalares de A2.

Na condição temporal conferida anteriormente, esse é UM termo agora
avaliado no inventário declarado. Permanecem os dois a2(s0V,V) compostos,
o a2(V,V) completo na mesma família e seus termos curvos. Nenhuma nulidade
de anomalia inteira é inferida. {len(checks)}controles, CPU{result['cpu_seconds']}s,
rc0; sem nova chamada remota, contratermo escolhido ou mudança do gate.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_a1_antibracket_composto.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='ARITY_ONE_QUARTIC_ANTIBRACKET',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: a1((Vchi,Veta)) calculado como divergência no inventário de espaço-forma constante; integral compacta0, densidade não0. {len(checks)}controles CPU{result["cpu_seconds"]}s. Q2OPEN. AberturaSHA256={opening}.\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
