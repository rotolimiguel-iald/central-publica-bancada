"""Audit the second actual ghost-vertex graph; retain distinct Wick matchings."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'C6';H=ROOT/'A7'
sys.path[:0]=[str(C),str(H)]
import ghost_euler_ghost_vertex_parallel as G
from deliver_nonminimal_wick_and_mimo_audit import sha,put


def main():
    out=C/'ghost_euler_ghost_vertex';out.mkdir(exist_ok=False);start=time.process_time();checks=0;rows=[]
    put(out/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),scope='Actual -Qbarc.c.dc x Vghost, constant cutoff, K order1, X parallel vector/Y metric jets',
        unknown_coefficients=True,full_Q2=False,temporal_weight_assigned=False,metric_Euler_graph_not_included=True))
    for label in range(10):
        row=[]
        for r in range(4):
            flat,n0=G.component(label,r,0);ref=G.flat_reference(label,r)
            assert s.expand(flat-ref)==0,('flat',label,r,flat,ref);checks+=1
            val,n1=G.component(label,r,1)
            assert not val.free_symbols.difference(G.Q)
            assert all(sum(p)==3 for p,c in s.Poly(val,*G.Q).terms() if c),(label,r,val)
            checks+=2;row.append(val)
            put(out/f'component_{label}_{r}.json',dict(label=G.LABELS[label],ghost=r,flat=str(flat),first=str(val),terms_flat=n0,terms_first=n1))
            print(json.dumps(dict(label=G.LABELS[label],ghost=r,checks=checks,cpu_seconds=time.process_time()-start)),flush=True)
        rows.append(row)
    aa,bb,cc=s.symbols('aa bb cc');q=G.Q;q2=sum(t*t for t in q)
    target=s.Matrix([[(1 if a==b else 2)*(aa*int(a==b)*q[r]*q2+bb*(int(a==r)*q[b]+int(b==r)*q[a])*q2+cc*q[a]*q[b]*q[r]) for r in range(4)] for a,b in G.LABELS])
    equations=[]
    for v in s.Matrix(rows)-target:equations.extend(s.Poly(s.expand(v),*q).coeffs())
    sol=s.solve(equations,(aa,bb,cc));assert set(sol)=={aa,bb,cc},sol
    for v in s.Matrix(rows)-target.subs(sol):assert s.expand(v)==0;checks+=1
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        first_curvature_coefficients={str(k):str(v) for k,v in sol.items()},
        scope='Ghost Euler graph only; X parallel vector normal jets, Y metric first jets, no temporal weight',
        full_metric_ghost_sum=False,full_Q2=False,gate_changed=False)
    put(out/'MATRIX.json',[[str(v) for v in row] for row in rows]);put(out/'results.json',result)
    paths=[Path(__file__),C/'ghost_euler_ghost_vertex_parallel.py',C/'labelled_ghost_dual.py',C/'labelled_covariant_xy.py',H/'mixed_b_h_current_engine_v3.py',out/'PRE_REGISTER.json',out/'results.json',out/'MATRIX.json']+sorted(out.glob('component_*.json'))
    put(out/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
