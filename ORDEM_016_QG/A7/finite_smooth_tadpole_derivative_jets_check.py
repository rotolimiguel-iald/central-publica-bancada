"""Derivative-jet tadpole grouped by internal derivatives and quartic Ward test."""
from pathlib import Path
from datetime import datetime, timezone
from itertools import combinations
from fractions import Fraction as F
import hashlib
import json
import time
from metric_principal_vertices import gamma2, gauge_matrix, lie_matrix, eh_cubic_16k, clear_caches
from metric_quartic_vertices import second_coefficient_4, eh_quartic_32k
from position_metric_bubble_engine import BASIS

H=Path(__file__).resolve().parent
D=H/'finite_smooth_tadpole_derivative_jets'
D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
    p=D/name;assert not p.exists()
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode('utf-8')
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
inputs=[Path(__file__),H/'metric_principal_vertices.py',H/'metric_quartic_vertices.py',
        H/'finite_smooth_tadpole/DERIVACAO.md']
save('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Compute finite W derivative-jet terms and test differentiated EH Noether identity',
    method='Full quartic versus independent cubic Ward identity; group by internal derivative count',
    momentum='p+k+r+s=0, exp(+ipx); G and Lie strip one common factor i',
    reference='W(X,Y)=(U exp(irX) tensor V exp(isY)+V exp(isX) tensor U exp(irY))/2',
    normalization='T=V4raw/16, cubic transport=V3raw/8; no extra4!',
    scope='Flat K=Lambda=0, constant cutoff modulo divergence, formal smooth reference not physical state',
    negative_control='Dropping the groups with internal derivatives must leave a nonzero Ward residual in a recorded fixture',
    excluded=['Physical bisolution/state existence','T1 choice','Full Q2','Curved derivative jets','Nonconstant cutoff'],
    sources=[dict(path=str(p),sha256=sha(p)) for p in inputs]))
cpu=time.process_time();checks=0
def eq(a,b=0):
    global checks
    assert a==b,(a,b);checks+=1
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def negative_sum(*ps):return tuple(-sum(v) for v in zip(*ps))
def grouped(*fields):
    gs=[gamma2(A,tuple(p)) for A,p in fields]
    result=[F(),F(),F()]
    for i,j in combinations(range(4),2):
        k,l=[a for a in range(4) if a not in (i,j)]
        n=int(k>=2)+int(l>=2)
        A,B=fields[i][0],fields[j][0]
        result[n]+=F(second_coefficient_4(A,B,gs[k],gs[l])+
                     second_coefficient_4(A,B,gs[l],gs[k]),16)
    return result
zero=(0,0,0,0)
fixtures=[(BASIS[0],(1,2,-1,1),(0,1,0,0),(1,0,-1,0),(2,-1,1,3)),
          (BASIS[1],(2,-1,0,3),(1,0,0,0),(0,1,1,0),(1,2,0,-1)),
          ((2,1,-1,3,1,0,2,-2,-1,2,1,0,3,-2,0,-1),
           (1,-1,2,3),(1,0,1,0),(-1,1,0,1),(0,2,-1,1))]
records=[];nonzero=[0,0,0];negative_count=0
for a,U in enumerate(BASIS):
    for b in range(a,len(BASIS)):
        V=BASIS[b]
        for f,(A,p,r,s,v) in enumerate(fixtures):
            k=negative_sum(p,r,s);G=gauge_matrix(k,v)
            fields=((A,p),(G,k),(U,r),(V,s))
            terms=grouped(*fields);total=sum(terms)
            eq(total,F(eh_quartic_32k(*fields),16))
            external=F(eh_cubic_16k(lie_matrix(A,p,k,v),add(p,k),U,r,V,s),8)
            internal1=F(eh_cubic_16k(A,p,lie_matrix(U,r,k,v),add(r,k),V,s),8)
            internal2=F(eh_cubic_16k(A,p,U,r,lie_matrix(V,s,k,v),add(s,k)),8)
            eq(total+external+internal1+internal2)
            eq(terms,grouped((A,p),(G,k),(V,s),(U,r)))
            eq(terms,grouped((G,k),(A,p),(U,r),(V,s)))
            bad=terms[0]+external+internal1+internal2
            if bad:negative_count+=1
            for j,value in enumerate(terms):nonzero[j]+=bool(value)
            if (bad or total) and len(records)<12:
                records.append(dict(fiber=[a,b],fixture=f,p=p,k=k,r=r,s=s,v=v,
                    groups=list(map(str,terms)),tadpole_Ward=str(total),
                    cubic_external=str(external),cubic_internal=[str(internal1),str(internal2)],
                    omitted_internal_derivatives_residual=str(bad)))
        # Constant-reference limit, including anisotropic fibers, at the same external data.
        A,p,_,_,v=fixtures[0];k=negative_sum(p)
        terms=grouped((A,p),(gauge_matrix(k,v),k),(U,zero),(V,zero))
        eq(terms,[F(),F(),F()])
    clear_caches()
assert negative_count>0 and nonzero[1]>0 and nonzero[2]>0
checks+=1
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,
    cpu_seconds=time.process_time()-cpu,fibers=55,fixtures_per_fiber=3,
    nonzero_group_counts=nonzero,negative_controls_nonzero=negative_count,controls=records,
    identity='T_W(A,Gc)+V3raw(Lie_c A,U,V)/8+V3raw(A,Lie_c U,V)/8+V3raw(A,U,Lie_c V)/8=0',
    normalization='Fourier plus convention; every Ward term carries the same extra i',
    full_Q2=False,T1_selected=False,reference_selected=False,gate_changed=False)
save('results.json',result)
save('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
