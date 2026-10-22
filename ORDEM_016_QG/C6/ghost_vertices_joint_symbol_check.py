"""Retain independent momenta at the two endpoints before covariant adjunction."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'C6';H=ROOT/'A7'
sys.path[:0]=[str(C),str(H)]
import metric_euler_ghost_vertex_parallel_v2 as Metric
import ghost_euler_ghost_vertex_parallel_v2 as Ghost
from deliver_nonminimal_wick_and_mimo_audit import sha,put


def main():
    out=C/'ghost_vertices_joint_symbol';out.mkdir(exist_ok=False);start=time.process_time();checks=0;data={}
    put(out/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
        target='Independent endpoint jets; equality R=Q is only the previously recorded amplitude, not covariant adjunction',
        metric_order='sym(Q on h) then R on c after adjunction',ghost_order='R from h before sym(Q on c) after adjunction',full_Q2=False))
    for name,G in [('metric',Metric),('ghost',Ghost)]:
        current={}
        for label in range(10):
            for r in range(4):
                old=json.loads((C/f'{name}_euler_ghost_vertex/component_{label}_{r}.json').read_bytes())
                values=[]
                for o,key in [(0,'flat'),(1,'first')]:
                    val,count=G.component(label,r,o,joint=True)
                    projected=val.subs(dict(zip(G.R,G.Q)),simultaneous=True)
                    assert s.expand(projected-s.sympify(old[key]))==0,(name,label,r,o);checks+=1
                    assert all(sum(mon)==5-2*o for mon,coef in s.Poly(val,*G.Q,*G.R).terms() if coef)
                    assert all(sum(mon[4:])<=1 for mon,coef in s.Poly(val,*G.Q,*G.R).terms() if coef)
                    checks+=2;values.append(str(val))
                current[str((label,r))]=values
            print(json.dumps(dict(graph=name,label=label,checks=checks,cpu_seconds=time.process_time()-start)),flush=True)
        data[name]=current;put(out/(name+'_SYMBOLS.json'),current)
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        graphs=2,components_per_graph=40,curvature_orders=[0,1],independent_endpoint_variables=True,
        old_projected_amplitudes_preserved=True,covariant_adjoint_pending=True,full_Q2=False,gate_changed=False)
    put(out/'results.json',result)
    paths=[Path(__file__),C/'metric_euler_ghost_vertex_parallel_v2.py',C/'ghost_euler_ghost_vertex_parallel_v2.py',C/'metric_euler_ghost_vertex/manifest.json',C/'ghost_euler_ghost_vertex/manifest.json',out/'PRE_REGISTER.json',out/'metric_SYMBOLS.json',out/'ghost_SYMBOLS.json',out/'results.json']
    put(out/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
