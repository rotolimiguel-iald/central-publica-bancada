"""Transpose the independent endpoint jets before merging derivative words.

The first block of derivatives is symmetrized. The single opposite-endpoint
derivative retains its side of that block. Curvature commutators are computed
by the existing covariant one-form jet recursion, not set to zero.
"""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
from itertools import permutations
import sys,json,time,ast
import sympy as s
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'C6';H=ROOT/'A7'
sys.path[:0]=[str(C),str(H)]
from oneform_second_curvature_engine_v2 import oneform_second
from deliver_nonminimal_wick_and_mimo_audit import sha,put
from position_metric_bubble_engine import LABELS


def main():
    out=C/'ghost_vertices_covariant_adjoint';out.mkdir(exist_ok=False);start=time.process_time();checks=0
    q=s.symbols('Q0:4');r=s.symbols('R0:4');p=s.symbols('p0:4')
    inputs={name:json.loads((C/f'ghost_vertices_joint_symbol/{name}_SYMBOLS.json').read_bytes()) for name in ('metric','ghost')}
    rows={name:[s.zeros(10,4),s.zeros(10,4)] for name in inputs}
    terms={name:{} for name in inputs}
    for name,table in inputs.items():
        for key,values in table.items():
            terms[name][ast.literal_eval(key)]=[s.Poly(s.sympify(v),*q,*r).terms() for v in values]
    put(out/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
        scope='Right-acting covariant local jet operator for the two computed graphs; compact support or vanishing boundary, constant cutoff',
        metric_order='sym alpha then beta',ghost_order='beta then sym alpha',
        phase='Oneform jet returns covariant derivative on exp(ipx), divided by common i',
        no_early_R_equals_Q=True,full_Q2=False))
    for pol in range(4):
        jet,_,_=oneform_second(tuple(int(i==pol) for i in range(4)),p)
        @lru_cache(None)
        def ordered(name,alpha,beta,component,curvature):
            wa=tuple(i for i,n in enumerate(alpha) for _ in range(n))
            wb=tuple(i for i,n in enumerate(beta) for _ in range(n))
            words=set(permutations(wa))
            ans=sum(jet(w+wb if name=='metric' else wb+w,component,curvature) for w in words)/len(words)
            return s.expand(ans)
        for name in inputs:
            for label in range(10):
                for order in (0,1):
                    value=0
                    for component in range(4):
                        for k in range(order+1):
                            for powers,coefficient in terms[name][label,component][k]:
                                if coefficient:
                                    value+=coefficient*ordered(name,powers[:4],powers[4:],component,order-k)
                    rows[name][order][label,pol]=s.expand(value)
                old=json.loads((C/f'{name}_euler_ghost_vertex/component_{label}_{pol}.json').read_bytes())
                assert s.expand(rows[name][0][label,pol]-s.sympify(old['flat']).subs(dict(zip(q,p))))==0,(name,label,pol)
                checks+=1
        print(json.dumps(dict(polarization=pol,checks=checks,cpu_seconds=time.process_time()-start)),flush=True)
    aa,bb,cc=s.symbols('aa bb cc');p2=sum(t*t for t in p)
    basis=s.Matrix([[(1 if a==b else 2)*(aa*int(a==b)*p[u]*p2+bb*(int(a==u)*p[b]+int(b==u)*p[a])*p2+cc*p[a]*p[b]*p[u]) for u in range(4)] for a,b in LABELS])
    fits={};witnesses={}
    for name in inputs:
        equations=[]
        for v in rows[name][1]-basis:equations.extend(s.Poly(s.expand(v),*p).coeffs())
        sol=s.solve(equations,(aa,bb,cc));assert set(sol)=={aa,bb,cc},(name,sol)
        for v in rows[name][1]-basis.subs(sol):assert s.expand(v)==0;checks+=1
        fits[name]={str(k):str(v) for k,v in sol.items()}
        old=s.Matrix(json.loads((C/f'{name}_euler_ghost_vertex/MATRIX.json').read_bytes())).subs(dict(zip(q,p)))
        missing=(rows[name][1]+old).applyfunc(s.expand)
        witnesses[name]=dict(nonzero=sum(v!=0 for v in missing),sample_00_0=str(missing[0,0]),
            meaning='Difference from simply merging endpoint momenta and multiplying by the K-order Fourier sign')
        put(out/(name+'_MATRICES.json'),[[[str(v) for v in row] for row in mat.tolist()] for mat in rows[name]])
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        normalized_by='Common i on the ghost wave; curvature coefficient includes the Fourier sign',
        right_acting_K_coefficients=fits,early_momentum_merge_missing_terms=witnesses,
        scope='Two ghost-vertex graphs only; local covariant normal jets, fixed background, compact support, constant cutoff',
        EH_metric_vertex_not_included=True,full_causal_family=False,full_Q2=False,gate_changed=False)
    put(out/'results.json',result)
    paths=[Path(__file__),H/'oneform_second_curvature_engine_v2.py',H/'spaceform_covariant_jet_engine.py',C/'ghost_vertices_joint_symbol/manifest.json',out/'PRE_REGISTER.json',out/'metric_MATRICES.json',out/'ghost_MATRICES.json',out/'results.json']
    put(out/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
