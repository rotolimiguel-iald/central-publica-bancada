"""Constant-cutoff limit of the three computed actual Euler graphs."""
from pathlib import Path
from datetime import datetime,timezone
import time,json
import sympy as s
from balanced_cubic_euler_contact_check import calculate as ghost_graphs
from balanced_euler_metric_vertex_check import calculate as metric_graph
from euler_ghost_descendant_contact_engine import weighted_defect
from position_metric_bubble_engine import LABELS
from full_loop_extension_engine import Q
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,put,write,append

D=H/'balanced_euler_constant_cutoff'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc);zero=(0,0,0,0)
    paths=[Path(__file__),H/'balanced_cubic_euler_contact_check.py',H/'balanced_euler_metric_vertex_check.py',
        H/'euler_subtotal_placement_audit/results.json',H/'temporal_ward_consistency_polarization/results.json']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        question='For vanishing cutoff jets, is the principal flat Euler sum free-BRST closed?',
        hypothesis='Local coefficient test with constant coupling in a neighborhood; not a globally compact constant switching function.',
        expectation='If this sum represents the one-loop flat A2 and qV vanishes modulo divergences, qA2 must vanish because a1 at K=0 vanishes.',
        stop_on_nonzero=False,no_fit=True,full_Q2=False,
        sources=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    start=time.process_time();m,g,counts=ghost_graphs(zero,zero);eh=s.zeros(10,4);checks=[];num=0
    for a,(i,j) in enumerate(LABELS):
        for r in range(4):
            value,n=metric_graph(a,r,zero,zero);eh[a,r]=value;num+=n
            assert not value.has(s.Float);checks.append('exact EH graph '+str((a,r)))
            put(D/f'component_{a}_{r}.json',dict(h=[i,j],c=r,metric_ghost=str(m[a,r]),
                ghost_ghost=str(g[a,r]),einstein=str(value),sum=str(s.expand(m[a,r]+g[a,r]+value))))
        print(json.dumps(dict(components=4*(a+1),cpu_seconds=time.process_time()-start)),flush=True)
    total=(m+g+eh).applyfunc(s.expand); B=s.zeros(4)
    # Already right-acting: variation of h and integration by parts at zero cutoff jets.
    for a,(i,j) in enumerate(LABELS):
        for r in range(4):
            B[j,r]-=Q[i]*total[a,r];B[i,r]-=Q[j]*total[a,r]
    defect=weighted_defect(B,zero)
    q2=sum(v*v for v in Q)
    # Extract the three parity-even O(4)-covariant rank-three basis coefficients,
    # then test all 40 polynomial components. This is not a Ward-canceling fit.
    a,b,c=s.symbols('a b c'); unknown=[a,b,c]
    basis=lambda i,j,r:(a*int(i==j)*Q[r]+b*(int(i==r)*Q[j]+int(j==r)*Q[i]))*q2**2+c*Q[i]*Q[j]*Q[r]*q2
    candidates=[]
    for A,(i,j) in enumerate(LABELS):
        for r in range(4):
            weight=1 if i==j else 2
            candidates.extend(s.Poly(s.expand(total[A,r]-weight*basis(i,j,r)),*Q).coeffs())
    sol=s.solve(candidates,unknown,dict=True)
    if len(sol)==1:
        for A,(i,j) in enumerate(LABELS):
            for r in range(4):
                assert s.expand(total[A,r]-(1 if i==j else 2)*basis(i,j,r).subs(sol[0]))==0
                checks.append('O4 decomposition '+str((A,r)))
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        contractions=dict(ghost_vertex=counts,einstein=num),
        total=[[str(v) for v in row] for row in total.tolist()],
        free_bv_square=[[str(v) for v in row] for row in defect.tolist()],
        nonzero_total=sum(v!=0 for v in total),nonzero_square=sum(v!=0 for v in defect),
        O4_decomposition=[{str(k):str(v) for k,v in row.items()} for row in sol],
        quantum_anomaly_computed=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — limite de jatos de cutoff constantes, setor principal plano]

Recomputados os três grafos Euler anteriores com lambda=eta=0, sem
apagar nenhum grafo e sem alterar a extensão balanceada. Trata-se de
uma região de cutoff constante; não se postula uma função globalmente
constante e simultaneamente compacta.

O resultado tem{result['nonzero_total']} componentes não nulas em40;
o quadrado BV livre graduado tem{result['nonzero_square']} em16.
Decomposição tensorial O(4) em

 A delta_ij q_r(q²)²+B(delta_ir q_j+delta_jr q_i)(q²)²
 +C q_i q_j q_r q²:
 {result['O4_decomposition']}.

Quando a decomposição existe, seus coeficientes descrevem os valores já
calculados e foram conferidos em todas40 componentes; não são contratermos
ajustados para remover o resultado. Fechamento BV neste limite é uma
condição necessária, não a condição completa com cutoffs variáveis,
curvatura, escalares e aridade1. A passagem ao par físico não é inferida.
{len(checks)} controles, CPU{result['cpu_seconds']}s,rc0.
Nenhum original/gate alterado. AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_Euler_cutoff_constante.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths+
        [D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']+sorted(D.glob('component_*.json'))]))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='EULER_CONSTANT_CUTOFF_LIMIT',target='A7.b',
        checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: limite cutoff constante, Euler componentes{result["nonzero_total"]}/40 e quadradoBV{result["nonzero_square"]}/16;{len(checks)}controles CPU{result["cpu_seconds"]}s. Q2OPEN;aberturaSHA256={opening}.\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['total','free_bv_square']}),flush=True)

if __name__=='__main__':main()
