"""Actual two-line Euler contacts from q(Faf) against the cubic ghost vertex."""
from pathlib import Path
from datetime import datetime,timezone
import json,time
import sympy as s
from balanced_tensor_transport_engine import balanced_euler_line,Q
from mixed_b_h_current_engine_v3 import current_terms
from position_metric_bubble_engine import LABELS
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

D=H/'balanced_cubic_euler_contact'

def calculate(lam,eta):
    L=tuple(lam[i]+eta[i] for i in range(4));metric=s.zeros(10,4);ghost=s.zeros(10,4)
    count=[0,0];index=lambda i,j:LABELS.index(tuple(sorted((i,j))))
    shift=lambda f:s.expand(f.subs({Q[i]:Q[i]+eta[i] for i in range(4)},simultaneous=True))
    adj=lambda f:s.expand(f.subs({Q[i]:-Q[i]-L[i] for i in range(4)},simultaneous=True))
    for r in range(4):
        for mu in range(4):
            unit=tuple(int(i==mu) for i in range(4))
            for (bar,A,hw,kw),zcoef in current_terms(r,unit).items():
                i,j=LABELS[A]
                # E_A Z_A at X, original ghost vertex -d(eta barc) Z at Y.
                # E_A contracts h_B with box delta_AB, including the b-h inverse.
                terms=[(A,(bar,),()),(index(i,bar),(),(j,)),(index(j,bar),(),(i,))]
                for B,external_h,internal_c in terms:
                    for bw,cutoff in [((mu,),1),((),eta[mu])]:
                        if not cutoff:continue
                        coef=-s.Rational(zcoef)*cutoff*(-1)**(len(hw)+len(bw))
                        kernel=balanced_euler_line(tuple(sorted(hw)),tuple(sorted(internal_c+bw)))
                        metric[B,r]+=coef*shift(kernel)*s.prod(-Q[k]-L[k] for k in external_h)*s.prod(Q[k] for k in kw)
                        count[0]+=1
                # -Qbarc_i c^j d_j c^i at X. Pair Qbarc_i with c^r at Y (i=r).
                # The minus vertex and barc-c covariance signs cancel.
                # Double Wick match signs are + for c^j--barc, - for d_j c^i--barc.
                cases=[(r,(bar,),(),1)]
                if r==bar:cases += [(j0,(),(j0,),-1) for j0 in range(4)]
                for u,external_c,internal_c,wick_sign in cases:
                    for bw,cutoff in [((mu,),1),((),eta[mu])]:
                        if not cutoff:continue
                        coef=-s.Rational(zcoef)*cutoff*wick_sign*(-1)**(len(kw)+len(bw))
                        kernel=balanced_euler_line(tuple(sorted(kw)),tuple(sorted(internal_c+bw)))
                        # Native order c_X B(D) h_Y; take its ordinary even/odd adjoint.
                        native=coef*shift(kernel)*s.prod(-Q[k]-L[k] for k in external_c)*s.prod(Q[k] for k in hw)
                        ghost[A,u]+=adj(native);count[1]+=1
    return metric.applyfunc(s.expand),ghost.applyfunc(s.expand),count

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    paths=[Path(__file__),H/'balanced_tensor_transport_engine.py',H/'mixed_b_h_current_engine_v3.py',
        H/'free_euler_insertion_contact/results.json',H/'bv_coordinate_inventory_delivery/DICIONARIO_E_INVENTARIO.md',
        H/'balanced_pair_normalization_v2/manifest.json']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        target='Compute actual raw two-contraction contact of (qFaf)_Euler against Vghost, external h,c',
        fixed_vertices='Faf=hdag Lie_c h+cdag c.dc; (qFaf)_Euler=E_h Lie_c h-(Qbarc)_i c^j d_j c^i',
        propagators='E_h--h=box f Id including b; barc--c=-f; c--barc=+f; no antifield propagators',
        normalization='Same balanced scalar Euler extension, all contacts divided by CE; vertex factors/temporal weights not yet combined with subtotal',
        scope='Principal flat Euclidean actual graph; not A2 or its WZ condition',
        sources=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    start=time.process_time();checks=[]
    # Independent odd-order contraction sign enumeration before tensor summation.
    def pairing_sign(pairs):
        current=list(range(5));sign=1
        for a,b in pairs:
            ia,ib=current.index(a),current.index(b)
            if ia>ib:raise AssertionError('ordered contractions required')
            sign*=(-1)**(ib-ia-1);current.remove(a);current.remove(b)
        return sign
    assert pairing_sign([(0,4),(1,3)])==1;checks.append('ghost Euler first contraction Wick sign')
    assert pairing_sign([(0,4),(2,3)])==-1;checks.append('ghost Euler second contraction Wick sign')
    assert pairing_sign([(1,3),(0,4)])==1;checks.append('even contractions commute order1')
    assert pairing_sign([(2,3),(0,4)])==-1;checks.append('even contractions commute order2')
    lam=(1,-1,0,0);eta=(1,0,0,0);data=[]
    for order,(left,right) in enumerate([(lam,eta),(eta,lam)]):
        m,g,n=calculate(left,right);L=tuple(left[i]+right[i] for i in range(4))
        for B in range(10):
            for r in range(4):
                assert not (s.expand(m[B,r]+g[B,r])).has(s.Float)
                checks.append('exact component '+str((order,B,r)))
        row=dict(order=order,lambda_x=left,eta_y=right,contractions=n,
            metric=[[str(v) for v in row] for row in m.tolist()],ghost=[[str(v) for v in row] for row in g.tolist()],
            total=[[str(v) for v in row] for row in (m+g).applyfunc(s.expand).tolist()],
            nonzero_metric=sum(v!=0 for v in m),nonzero_ghost=sum(v!=0 for v in g),nonzero_total=sum(v!=0 for v in m+g))
        put(D/f'order_{order}.json',row);data.append({k:v for k,v in row.items() if k not in ['metric','ghost','total']})
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        orders=data,weights_fitted=False,combined_with_subtotal=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — dois contatos Euler dos vértices cúbicos; Q2 OPEN]

Calculados os contatos de duas linhas entre (qFaf)_Euler e Vghost,
com saída h,c. Eles diferem do descendente E_h[G,chi]w anteriormente
medido, cuja saída tem dois ghosts. Não são uma repetição desse diagrama.

 (qFaf)_Euler=E_A(Lie_c h)_A-(Qbarc)_i c^j d_j c^i.

No primeiro termo, E_A--h_B=box f delta_AB usa o inverso completo h,b.
A segunda contração é c--barc. No segundo termo há duas linhas ghosts;
o menos do vértice cancela o menos de barc--c, e os dois emparelhamentos
restantes têm sinais+ e-. Esses sinais foram conferidos por enumeração
independente da ordem dos cinco fatores ímpares, antes da soma tensorial.

Usamos a R_bal já declarada, mantendo todas as derivadas em cada linha,
os dois cutoffs e a adjunção que põe h à esquerda de c no resultado.
Foram computadas40componentes em cada ordem; dados: {data}.

São valores de grafos crus divididos por CE, sem selecionar um peso para
zerar o subtotal. A tradução para os prefatores de Tc2/A2 ainda deve
acompanhar a fonte composta inteira. Não somamos silenciosamente esses
valores à matriz anterior. {len(checks)}controles (incluem80verificações de
aritmética exata; não80identidades de Ward), CPU{result['cpu_seconds']}s,rc0.
Termos curvos e família completa continuam OPEN; nenhum gate alterado.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_contatos_Euler_vertices_cubicos.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths+[D/'PRE_REGISTER.json',D/'results.json',D/'order_0.json',D/'order_1.json',D/'DERIVACAO.md']],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='BALANCED_CUBIC_EULER_GRAPHS',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: contatos Euler de qFaf×Vghost com saída h,c calculados nas2ordens, sem peso ajustado nem soma prematura;{len(checks)}controles CPU{result["cpu_seconds"]}s. Q2OPEN. AberturaSHA256={opening}.\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
