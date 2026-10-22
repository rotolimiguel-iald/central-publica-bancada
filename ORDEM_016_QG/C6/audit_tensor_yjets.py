"""Independent curvature-commutator and orthogonal-frame checks of tabulated jets."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
from functools import lru_cache
import sys,json,ast,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C6/tensor_yjets';H=ROOT/'A7'
sys.path.insert(0,str(H))
from deliver_nonminimal_wick_and_mimo_audit import sha,put

def main():
    start=time.process_time();Q=s.symbols('q0:4');checks=0
    meta=json.loads((D/'manifest.json').read_bytes());tables={}
    for row in meta['blocks']:
        p=Path(row['path']);assert sha(p)==row['sha256'];raw=json.loads(p.read_bytes())
        tables[(tuple(row['u']),tuple(row['v']))]={ast.literal_eval(k):tuple(map(s.sympify,vals)) for k,vals in raw['coefficients'].items()}
    def eq(a,b,label):
        nonlocal checks
        assert s.expand(a-b)==0,(label,a,b)
        checks+=1
    def d(i,j):return s.Integer(i==j)
    def S(ind):
        a,b,c,e=ind
        return (d(a,c)*d(b,e)+d(a,e)*d(b,c)-d(a,b)*d(c,e))/2
    def RY(ind,i,j):
        # [nabla_i,nabla_j] on each lower Y slot: delta_(slot,i) H_j - delta_(slot,j) H_i.
        out=0
        for pos in (2,3):
            slot=ind[pos]
            out+=d(slot,i)*S(ind[:pos]+(j,)+ind[pos+1:])-d(slot,j)*S(ind[:pos]+(i,)+ind[pos+1:])
        return out
    box=sum(q*q for q in Q);nonzero=0
    inds=list(tables[((),())])
    for i in range(4):
        for j in range(i+1,4):
            for ind in inds:
                ai,bi=tables[((i,j),())][ind];aj,bj=tables[((j,i),())][ind]
                expected=s.Rational(3,32)*box*RY(ind,i,j)
                eq(ai-aj,expected,('first commutator',ind,i,j));eq(bi-bj,0,('first unit commutator',ind,i,j))
                ai,bi=tables[((),(i,j))][ind];aj,bj=tables[((),(j,i))][ind]
                eq(ai-aj,0,('second unit commutator',ind,i,j));eq(bi-bj,expected,('second commutator',ind,i,j))
                nonzero+=int(expected!=0)
    assert nonzero>0
    commute_checks=checks
    # Adjacent transpositions generate all coordinate permutations; sign flips check reflections.
    for axis in range(3):
        p=list(range(4));p[axis],p[axis+1]=p[axis+1],p[axis]
        repl=dict(zip(Q,[Q[p[k]] for k in range(4)]))
        @lru_cache(None)
        def rename(poly):return s.expand(poly.subs(repl,simultaneous=True))
        for (u,v),table in tables.items():
            dest=tables[(tuple(p[k] for k in u),tuple(p[k] for k in v))]
            for ind,vals in table.items():
                target=tuple(sorted((p[ind[0]],p[ind[1]])))+tuple(sorted((p[ind[2]],p[ind[3]])))
                for part in (0,1):eq(rename(vals[part]),dest[target][part],('permutation',axis,u,v,ind,part))
        print(json.dumps(dict(stage='permutation',axis=axis,checks=checks,cpu_seconds=time.process_time()-start)),flush=True)
    for axis in range(4):
        @lru_cache(None)
        def reflect(poly):return s.expand(poly.subs(Q[axis],-Q[axis]))
        for (u,v),table in tables.items():
            for ind,vals in table.items():
                sign=(-1)**(ind.count(axis)+u.count(axis)+v.count(axis))
                for part in (0,1):eq(reflect(vals[part]),sign*vals[part],('reflection',axis,u,v,ind,part))
    r=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,commutator_checks=commute_checks,
        nonzero_curvature_commutators=nonzero,permutations_tested=3,reflections_tested=4,
        statement='Ordered Y commutator equals curvature acting on the two covariant Y slots times flat Euler contact; coordinate permutation/reflection covariance',
        continuous_O4_covariance_proved=False,cpu_seconds=time.process_time()-start,full_Q2=False,gate_changed=False)
    put(D/'INDEPENDENT_AUDIT.json',r);put(D/'AUDIT_MANIFEST.json',dict(sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'manifest.json',D/'INDEPENDENT_AUDIT.json']]))
    print(json.dumps(r),flush=True)
if __name__=='__main__':main()
