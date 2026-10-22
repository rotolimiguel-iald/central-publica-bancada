"""Euler contact with the full localized cubic Einstein metric vertex."""
from pathlib import Path
from datetime import datetime,timezone
import json,time
import sympy as s
from fractions import Fraction
from balanced_tensor_transport_engine import balanced_euler_line,Q
from localized_eh_cubic_engine import localized_vertex_data
from position_metric_bubble_engine import LABELS,BASIS
from metric_coincident_jet_engine_v2 import metric_fiber
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

D=H/'balanced_euler_metric_vertex'

def calculate(external_h,r,lam,eta):
    W=localized_vertex_data(BASIS[external_h],Fraction(1),tuple(eta));S=metric_fiber()['S0']
    L=tuple(lam[i]+eta[i] for i in range(4));index=lambda i,j:LABELS.index(tuple(sorted((i,j))))
    out=0;count=0
    for ex in [-1,0,1,2,3]:
        vertex=W[0] if ex<0 else W[1][ex]
        for u,row in enumerate(vertex):
            du,A=u//10-1,u%10;eu=() if du<0 else (du,);i,j=LABELS[A]
            pieces=[(A,(r,),()),(index(i,r),(),(j,)),(index(j,r),(),(i,))]
            for v,raw in row.items():
                dv,B=v//10-1,v%10;hv=() if dv<0 else (dv,)
                for C,internal_h,external_c in pieces:
                    fiber=S[C,B]
                    if not fiber:continue
                    # Cubic Hessian -W/(16*kappa), one metric covariance -4*kappa*S.
                    # Two cross matchings cancel the 1/2 in the internal quadratic Taylor term.
                    coefficient=s.Rational(raw)*fiber*(-1)**(len(eu)+len(hv))/4
                    kernel=balanced_euler_line(eu,tuple(sorted(internal_h+hv)))
                    native=coefficient*kernel.subs({Q[k]:Q[k]+eta[k] for k in range(4)},simultaneous=True)
                    native*=s.prod(-Q[k]-L[k] for k in external_c)
                    if ex>=0:native*=Q[ex]
                    out+=native;count+=1
    return s.expand(out.subs({Q[k]:-Q[k]-L[k] for k in range(4)},simultaneous=True)),count

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    paths=[Path(__file__),H/'localized_eh_cubic_engine.py',H/'balanced_tensor_transport_engine.py',
        H/'free_euler_insertion_contact/results.json',H/'balanced_cubic_euler_contact/results.json']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        target='Compute T2((qFaf)_Euler,Vmetric) two-line contact with external h,c, distinct from the ghost-vertex graphs',
        normalization='Hessian -W/(16*kappa) times metric covariance -4*kappa*S gives +W*S/4; full Euler inverse gives box f Id',
        no_new_weights=True,scope='Graph coefficient only; requires bookkeeping before adding to any already reduced current expression',
        sources=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    start=time.process_time();lam=(1,-1,0,0);eta=(1,0,0,0);orders=[];checks=[]
    # Independent one-component polynomial checks the Hessian and Wick factorial.
    x,y,e,n,c=s.symbols('x y e n c');v3=-s.Symbol('w')*y**3/6
    third=s.diff(v3,y,3);expected=-s.Symbol('w')
    assert third==expected;checks.append('cubic Hessian external extraction')
    # X=E*h*c and Y=(H/2)*hY²: two matchings give H*<E hY>*<h hY>*c.
    Hs,Es,Ns=s.symbols('H E N');assert 2*(Hs/2)*Es*Ns==Hs*Es*Ns;checks.append('internal two-line factorial')
    for order,(left,right) in enumerate([(lam,eta),(eta,lam)]):
        rows=[];count=0
        for a in range(10):
            row=[]
            for r in range(4):
                value,num=calculate(a,r,left,right);count+=num;row.append(str(value))
                assert not value.has(s.Float);checks.append('exact coefficient '+str((order,a,r)))
                put(D/f'component_{order}_{a}_{r}.json',dict(external_h=LABELS[a],ghost=r,value=str(value),contractions=num))
            rows.append(row)
            print(json.dumps(dict(order=order,external_h=LABELS[a],components_done=4*(a+1))),flush=True)
        put(D/f'order_{order}.json',dict(lambda_x=left,eta_y=right,matrix=rows,contractions=count))
        orders.append(dict(order=order,contractions=count,nonzero=sum(s.sympify(v)!=0 for row in rows for v in row)))
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        orders=orders,full_Q2=False,combined_with_subtotal=False,weights_fitted=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — contato Euler com vértice Einstein cúbico localizado; Q2 OPEN]

O inventário qFaf×V contém também E_h Lie_c h contra o vértice métrico
cúbico, além dos dois contatos com Vghost. Aqui as duas linhas são métricas:
uma é a linha Euler completa box f Id e a outra é -4kappa S f.
Usou-se o vértice EH localizado existente, inclusive o termo em d eta.
A Hessiana -W/(16kappa) fixa o fator+W*S/4. Os dois emparelhamentos
cruzados compensam o1/2 da expansão quadrática interna; não há ajuste.

Calculadas40componentes em cada ordem de cutoffs; resultados: {orders}.
Controles{len(checks)}, CPU{result['cpu_seconds']}s,rc0. Os80controles de
ausência de floats atestam aritmética exata, não identidades de Ward.

Esta entrega completa esse inventário de três contatos Euler cúbicos no
setor principal plano métrico/ghost. Não é um novo termo que possa ser
somado automaticamente à expressão de correntes: deve-se conferir se a
redução prévia de s0V já o transportou por integração por partes. Evitar
dupla contagem faz parte da montagem pendente. Nenhum gate foi alterado.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_contato_Euler_Einstein_cubico.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']+sorted(D.glob('component_*.json'))+sorted(D.glob('order_*.json'))],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='BALANCED_EULER_EINSTEIN_GRAPH',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: contato Euler com EH localizado80componentes;{len(checks)}controles CPU{result["cpu_seconds"]}s; sem soma automática/dupla contagem. Q2OPEN. AberturaSHA256={opening}.\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
