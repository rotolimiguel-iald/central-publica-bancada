"""Two-endpoint scalar RNC check of the O(K) Euler contact, including density."""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
from itertools import product
import json,time
import sympy as s
import balanced_log_pair_engine as E
from smooth_line_compatibility_check_v2 import multiply,correction as smooth_correction
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

x=E.x;y=s.symbols('y0:4');zero=dict.fromkeys(y,0)
xx=sum(t*t for t in x);yy=sum(t*t for t in y);xy=sum(x[i]*y[i] for i in range(4))
zcart=sum((x[i]-y[i])**2 for i in range(4));la,lb=s.symbols('lambda_A lambda_B')
F=(1,0);ONE=(0,0);LG=(0,1)

def expansion(lam,order):
    if order==0:return [(s.Integer(1),F)]
    return [((xx*yy-xy**2)/3,(2,0)),(s.Rational(1,4),ONE),(-(lam+2)/4,LG)]

@lru_cache(None)
def jet(coefficient,profile,word):
    out=[]
    for mask in product((0,1),repeat=len(word)):
        c=coefficient;rad=[];sign=1
        for (side,i),on_coefficient in zip(word,mask):
            if on_coefficient:c=s.diff(c,(x if side==0 else y)[i])
            else:rad.append(i);sign*=1 if side==0 else -1
        c=s.expand(sign*c.subs(zero))
        if c:out.append((c,profile,tuple(sorted(rad))))
    return out

def pair_delta(a,ua,b,ub):
    out=0
    for ca,pa in a:
        for cb,pb in b:
            for c,p,u in jet(ca,pa,ua):
                for d,q,v in jet(cb,pb,ub):
                    if q==ONE:
                        value=0 if v else smooth_correction(p,s.Integer(1),u,())
                    elif p==ONE:
                        value=0 if u else smooth_correction(q,s.Integer(1),v,())
                    else:value=E.correction(p,q,u,v)
                    out+=multiply(c*d,value)
    return s.expand(out)

def main():
    D=H/'bilocal_scalar_euler_zerojet';D.mkdir(exist_ok=False);start=time.process_time();now=datetime.now(timezone.utc)
    sources=[Path(__file__),H/'smooth_line_compatibility_check_v2.py',H/'smooth_line_compatibility_v2/results.json',
        H/'balanced_log_pair_engine.py',H/'bilocal_first_curvature_engine.py']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        model='Euclidean 4D constant curvature scalar P=Box_g+lambda*K, auxiliary Hadamard profile only',
        profile='H0=1/w;H1=(|x|²|y|²-(x.y)²)/(3w²)+1/4-(lambda+2)log(w)/4',
        task='Compare densitized Euler action at x and y before setting y=0',
        sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
    checks=[]
    def eq(name,a,b=0):
        assert s.cancel(a-b)==0,(name,a,b);checks.append(name)
    A0,B0=expansion(la,0),expansion(lb,0);A1,B1=expansion(la,1),expansion(lb,1)
    E0=E.euler_correction(F,F);coefficients={};details={}
    # The bitensor itself, differentiated before restricting the second endpoint.
    raw1=(xx*yy-xy**2)/(3*zcart**2)+s.Rational(1,4)-(la+2)*s.log(zcart)/4
    raw0=1/zcart
    for side in [0,1]:
        coords=x if side==0 else y
        profile_contact=sum(pair_delta(A1,((side,i),(side,i)),B0,())+
            pair_delta(A0,((side,i),(side,i)),B1,()) for i in range(4))
        operator_contact=0
        radius=sum(t*t for t in coords)
        for i in range(4):
            for j in range(4):
                c=((radius*s.KroneckerDelta(i,j)-coords[i]*coords[j])/3).subs(zero)
                operator_contact+=multiply(c,pair_delta(A0,((side,i),(side,j)),B0,()))
            operator_contact+=multiply((-2*coords[i]).subs(zero),pair_delta(A0,((side,i),),B0,()))
        density_contact=multiply((-radius/2).subs(zero),E0)
        mass_contact=la*pair_delta(A0,(),B0,())
        value=s.expand(profile_contact+operator_contact+density_contact+mass_contact)
        coefficients[side]=value
        details[str(side)]={k:str(s.expand(v)) for k,v in dict(profile=profile_contact,operator=operator_contact,
            density=density_contact,potential=mass_contact,total=value).items()}
        # Off-diagonal field equation, independent from local-contact calculation.
        raw_box=sum(s.diff(raw1,t,2) for t in coords)
        raw_geom=sum((radius*s.KroneckerDelta(i,j)-coords[i]*coords[j])/3*s.diff(raw0,coords[i],coords[j])
            for i in range(4) for j in range(4))-2*sum(coords[i]*s.diff(raw0,coords[i]) for i in range(4))
        eq('offdiagonal scalar equation endpoint'+str(side),(raw_box+raw_geom+la*raw0).subs(zero))
        eq('densitized contact endpoint'+str(side),value,(1+la-lb)/4)
    eq('two endpoint equality after density',coefficients[0],coefficients[1])
    eq('massless equal scalar lines',coefficients[0].subs({la:0,lb:0}),s.Rational(1,4))
    eq('equal potentials cancel from this coefficient',coefficients[0].subs(lb,la),s.Rational(1,4))
    # The pre-density difference is not zero. This is a negative control on omission.
    non_density_difference=s.expand(s.sympify(details['0']['profile'])+s.sympify(details['0']['operator'])-
        s.sympify(details['1']['profile'])-s.sympify(details['1']['operator']))
    eq('omitting density leaves3/8',non_density_difference,s.Rational(3,8))
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        endpoint_details=details,coefficient_K_over_CE=str(coefficients[0]),
        distribution='CE*(3*Box_delta/32+K*(1+lambda_A-lambda_B)*delta/4), zero added smooth W',
        scalar_massless_coefficient='1/4',full_tensor_transport=False,global_time_ordered_family=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — contato escalar bilocal de primeira curvatura, jato sem derivadas adicionais]

A verificação agora diferencia H(x,y) ANTES de fixar y=0. Inclui o termo
de distância (|x|²|y|²-(x.y)²)/(3w²), ausente no perfil radial isolado.
O operador é sqrt(g)(Box_g+lambda*K), em RNC euclidianas auxiliares4D.
Usam-se a extensão f/f e f/log declarada e a compatibilidade suave corrigida.

Resultado nas duas pontas, para a primeira linha de potencial lambda_A
e a segunda lambda_B: coeficiente CE*K*(1+lambda_A-lambda_B)/4.
Para as linhas escalares iguais do modelo087: CE*K/4.
Em x, perfil+operador dão5/8 e a densidade subtrai3/8; em y, o cálculo
bilocal já dá1/4 e a densidade vale1. As duas leituras coincidem.
Omitir a densidade deixa diferença3/8 — controle negativo não trivial.
Também foi conferida a equação fora da diagonal em ambas as pontas.

Isto paga esta parcela escalar; não paga os transportes vetorial/tensorial,
vértices curvos, jatos adicionais nem a família causal lorentziana completa.
lambda aqui é coeficiente do potencial de Laplace, NÃO a constante
cosmológica identificada. Nenhuma identificação física nova foi feita.
Referência suave adicional não escolhida; W0 contribuiria separadamente.
{len(checks)}identidades simbólicas; CPU{result['cpu_seconds']}s;rc0.
Sem chamadas/kernel/gate. AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_Euler_escalar_bilocal_curvo.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='SCALAR_BILOCAL_CURVATURE_EULER_ZEROJET',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: contato escalarEuler curvo nas duas pontas CE*K/4; diferença3/8seomitir densidade. {len(checks)}identidades CPU{result["cpu_seconds"]}s;Q2inteiraOPEN.AberturaSHA256={opening}.\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
