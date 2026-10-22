"""Actual metric/ghost two-line normalization change and its free-BRST descent."""
from pathlib import Path
from datetime import datetime,timezone
import json,time,gc
import sympy as s
from balanced_tensor_transport_engine import FormalPairLoop,loop_ward_delta,realize
from full_loop_extension_engine import SymbolicRawLoop,Q
from position_metric_bubble_engine import BASIS,LABELS
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append
D=H/'balanced_pair_tensor'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    sources=[Path(__file__),H/'balanced_tensor_transport_engine.py',H/'full_loop_extension_engine.py',
        H/'balanced_pair_normalization_v2/manifest.json',H/'localized_eh_cubic_engine.py',
        H/'localized_ghost_boundary_engine.py']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),target='Two cutoff orderings, all40 h/c components of Y-Ward variation of R_bal-R_raw in metric/ghost h-h bubbles',
        method='Preserve separate formal derivative words through tensor contraction, then use declared balanced correction; external adjunction after extension.',
        fixed_weights='ghost - metric/2, scalar metric normalization /16 remains in engine',
        scope='Local finite normalization of ordinary pairs, NOT complete A2; source/current/curved terms not included',
        check='Polarized free-BRST square of a symmetric even bilinear counterterm should vanish; record failures, never fit.',
        sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
    start=time.process_time();checks=[];matrices=[];allrows=[]
    for order,(lam,eta) in enumerate([((1,-1,0,0),(1,0,0,0)),((1,0,0,0),(1,-1,0,0))]):
        A={};L=tuple(a+b for a,b in zip(lam,eta))
        for a,(i,j) in enumerate(LABELS):
            metric=FormalPairLoop('metric',BASIS[a],lam,eta);ghost=FormalPairLoop('ghost',BASIS[a],lam,eta)
            for engine in [metric,ghost]:
                ordinary=SymbolicRawLoop(engine.kind,BASIS[a],lam,eta)
                for ex,yidx,b,r in [(-1,-1,0,0),(0,1,1,2)]:
                    assert s.expand(realize(engine.raw_expression(ex,yidx,b,r))-ordinary.raw_expression(ex,yidx,b,r))==0
                    checks.append((order,a,engine.kind,ex,yidx,b,r))
            for r in range(4):
                m,nm=loop_ward_delta(metric,r);g,ng=loop_ward_delta(ghost,r)
                value=s.expand(g-m/2);A[a,r]=value
                row=dict(order=order,a=a,h=[i,j],c=r,lambda_x=lam,eta_y=eta,
                    metric_delta=str(m),ghost_delta=str(g),weighted_delta=str(value),
                    nonzero_raw_blocks=[nm,ng],cpu_seconds=time.process_time()-start)
                put(D/f'component_{order}_{a}_{r}.json',row);allrows.append(row)
                print(json.dumps(dict(order=order,h=[i,j],c=r,cpu_seconds=row['cpu_seconds'])),flush=True)
            # Old engine methods cache by instance; release completed instances explicitly.
            metric.raw_expression.cache_clear();metric.paired.cache_clear();metric.matrix.cache_clear();metric.scalar.cache_clear()
            ordinary.raw_expression.cache_clear();ordinary.paired.cache_clear();ordinary.matrix.cache_clear()
            gc.collect()
        B=s.zeros(4)
        for a,(i,j) in enumerate(LABELS):
            for r in range(4):
                f=A[a,r].subs({Q[k]:Q[k]+L[k] for k in range(4)},simultaneous=True)
                B[j,r]-=(Q[i]+L[i])*f;B[i,r]-=(Q[j]+L[j])*f
        matrices.append(B.applyfunc(s.expand))
    L=(2,-1,0,0)
    adj=lambda M:M.T.applyfunc(lambda f:s.expand(f.subs({Q[k]:-Q[k]-L[k] for k in range(4)},simultaneous=True)))
    polarized=(matrices[0]+matrices[1])/2
    square=(polarized-adj(polarized)).applyfunc(s.expand)
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        rows=len(allrows),nonzero_pair_changes=sum(s.sympify(r['weighted_delta'])!=0 for r in allrows),
        polarized_free_bv_square=[[str(v) for v in row] for row in square.tolist()],
        nonzero_square_components=sum(v!=0 for v in square),full_Q2=False,gate_changed=False,
        interpretation='Square of the normalization change tests self-consistency of this ordinary pair only; zero is not full Ward closure. Nonzero remains a diagnostic.')
    put(D/'results.json',result)
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — transporte tensorial da mudança de prescrição nas bolhas ordinárias; Q2 completa OPEN]

Os vértices métricos e ghost localizados foram reutilizados sem alteração.
Cada propagador conserva sua palavra de derivadas até a contração. Só então
se aplica (R_bal-R_raw)/CE da prescrição já declarada, seguido da adjunção
dos campos externos e dos cutoffs. O peso é ghost-métrica/2, com /16 métrico
preservado no motor. Não há ajuste de tau, resíduo ou constante física.

80 componentes h_A c_r, incluindo as duas ordens dos cutoffs; mudanças não
nulas: {result['nonzero_pair_changes']}. {len(checks)} conferências exatas da
realização dos símbolos contra os kernels originais; CPU{result['cpu_seconds']}s.
Quadrado BV livre da mudança polarizada: {result['nonzero_square_components']}
componentes não nulos em16. Resultado integral preservado no JSON, sem ajuste.

O que foi calculado é a variação Ward da mudança local dos pares h-h,
não o valor novo de A2. As inserções de corrente, fonte, contatos Euler,
normalização de aridade1 e curvatura têm de pertencer à mesma família antes
da soma final. Quadrado nulo desta mudança não prova anomalia completa nula.
AberturaSHA256={opening}. Nenhum original ou gate alterado.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_bolhas_tensor_balanceado.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']+sorted(D.glob('component_*.json'))],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='BALANCED_PAIR_TENSOR_TRANSPORT',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f"\n{now.isoformat()} A7.b: bolhas ordinárias balanceadas80componentes, controles{len(checks)}, quadradoBVnãozero{result['nonzero_square_components']}; CPU{result['cpu_seconds']}s. Q2OPEN. AberturaSHA256={opening}.\n")
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
