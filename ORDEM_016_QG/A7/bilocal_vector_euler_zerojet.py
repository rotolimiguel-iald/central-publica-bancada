"""First-curvature vector pair Euler contacts before tensor contractions into vertices."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
import json,time
import sympy as s
import balanced_log_pair_engine as E
from bilocal_scalar_euler_zerojet import x,y,xx,yy,xy,zero,F,ONE,LG,pair_delta
from smooth_line_compatibility_check_v2 import multiply
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

def delta(a,b):return s.Integer(a==b)
def gamma(coords,a,i,b):return -(delta(a,b)*coords[i]+delta(a,i)*coords[b]-2*delta(i,b)*coords[a])/3
def prop(order,a,b):
    if order==0:return [(delta(a,b),F)]
    P=((xx-yy)*delta(a,b)-x[a]*x[b]+y[a]*y[b])/6+(x[a]*y[b]-y[a]*x[b])/2
    return [(P,F),((xx*yy-xy**2)*delta(a,b)/3,(2,0)),
        (delta(a,b)/4,ONE),(-5*delta(a,b)/4,LG)]

def raw(order,a,b):
    z=sum((x[i]-y[i])**2 for i in range(4));out=0
    for coef,(n,l) in prop(order,a,b):out+=coef*z**(-n)*s.log(z)**l
    return out

def main():
    D=H/'bilocal_vector_euler_zerojet';D.mkdir(exist_ok=False);now=datetime.now(timezone.utc);start=time.process_time()
    sources=[Path(__file__),H/'bilocal_scalar_euler_zerojet.py',H/'bilocal_first_curvature_engine.py',
        H/'bilocal_covariant_jet_engine.py',H/'smooth_line_compatibility_check_v2.py']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        task='Ordered vector pair local Euler contacts O(K), at both endpoints in one RNC chart',
        operator='sqrt(g)*(rough Laplacian+3K), X vector index contravariant and Y index covariant',
        scope='Pair distribution components, not a completed loop amplitude; ghost Wick signs and interaction vertices still separate',
        sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
    checks=[];matrix={};differences=[]
    def eq(name,a,b=0):
        assert s.cancel(a-b)==0,(name,a,b);checks.append(name)
    # Check the individual parametrix independently, before any pairing or extension.
    for side,a,b in product(range(2),range(4),range(4)):
        coords=x if side==0 else y;rad=sum(t*t for t in coords)
        h0=raw(0,a,b);h1=raw(1,a,b)
        val=sum(s.diff(h1,t,2) for t in coords)
        val+=sum((rad*delta(i,j)-coords[i]*coords[j])/3*s.diff(h0,coords[i],coords[j]) for i,j in product(range(4),repeat=2))
        val-=2*sum(coords[i]*s.diff(h0,coords[i]) for i in range(4))
        for i,c in product(range(4),repeat=2):
            g=gamma(coords,a,i,c) if side==0 else -gamma(coords,c,i,b)
            h=raw(0,c,b) if side==0 else raw(0,a,c)
            val+=2*g*s.diff(h,coords[i])+s.diff(g,coords[i])*h
        val+=3*h0
        eq('offdiagonal vector parametrix'+str((side,a,b)),val.subs(zero))
    for a,b,c,d in product(range(4),repeat=4):
        A0,A1=prop(0,a,b),prop(1,a,b);B0,B1=prop(0,c,d),prop(1,c,d);values=[]
        for side in range(2):
            coords=x if side==0 else y;rad=sum(t*t for t in coords)
            value=sum(pair_delta(A1,((side,i),(side,i)),B0,())+
                pair_delta(A0,((side,i),(side,i)),B1,()) for i in range(4))
            for i,j in product(range(4),repeat=2):
                coef=((rad*delta(i,j)-coords[i]*coords[j])/3).subs(zero)
                value+=multiply(coef,pair_delta(A0,((side,i),(side,j)),B0,()))
            for i in range(4):
                value+=multiply((-2*coords[i]).subs(zero),pair_delta(A0,((side,i),),B0,()))
                for r in range(4):
                    g=gamma(coords,a,i,r) if side==0 else -gamma(coords,r,i,b)
                    A=prop(0,r,b) if side==0 else prop(0,a,r)
                    value+=multiply((2*g).subs(zero),pair_delta(A,((side,i),),B0,()))
                    value+=multiply(s.diff(g,coords[i]).subs(zero),pair_delta(A,(),B0,()))
            value+=3*pair_delta(A0,(),B0,())
            e0=sum(pair_delta(A0,((side,i),(side,i)),B0,()) for i in range(4))
            value+=multiply((-rad/2).subs(zero),e0)
            values.append(s.expand(value))
        matrix[str((a,b,c,d))]=list(map(str,values))
        diff=s.expand(values[0]-values[1])
        if diff: differences.append(dict(indices=[a,b,c,d],difference=str(diff)))
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        components=len(matrix),endpoint_differences=len(differences),difference_entries=differences,
        local_pole_only=True,additional_derivative_jets=False,ghost_wick_signs_applied=False,
        loop_anomaly=False,full_Q2=False,gate_changed=False)
    put(D/'TABLE.json',matrix);put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — pares vetoriais de primeira curvatura, antes dos vértices]

Calculados256componentes do contato de Euler para Hq(a,b)Hq(c,d)
nas duas pontas. O operador inclui sqrt(g), Laplaciano covariante e3K.
O transporte usa a mesma P1 bilocal já custodiada; conexões têm sinal
positivo no índice contravarianteX e negativo no índice covarianteY.
As32equações de parametrix fora da diagonal passaram simbolicamente.

Comparação das pontas: {len(differences)}componentes diferentes de256.
As diferenças, se presentes, são medidas no TABLE/results; não se
declara anomalia ou inadmissibilidade só por esse número, pois os
operadores nas pontas e índices precisam do transporte distributivo.
Este é um bloco de montagem da mesma prescrição parcial, não o laço
completo. Faltam sinais de Wick, vértices, jatos e família causal completa.

CPU{result['cpu_seconds']}s;rc0; {len(checks)}controles do parametrix.
Sem chamada externa/kernel/gate. AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_Euler_vetorial_bilocal_curvo.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'TABLE.json',D/'results.json',D/'DERIVACAO.md']],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='VECTOR_BILOCAL_EULER_ZEROJET',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b:256contatosvetoriais curvos,32equaçõesparametrix; diferençaentre pontas{len(differences)}/256;CPU{result["cpu_seconds"]}s, Q2OPEN. AberturaSHA256={opening}.\n')
    print(json.dumps({k:v for k,v in result.items() if k!='difference_entries'}),flush=True)

if __name__=='__main__':main()
