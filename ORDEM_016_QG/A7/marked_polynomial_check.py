"""Complete polarization basis with symbolic momenta; exact sparse algebra."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
from marked_polynomial_engine import *
from metric_principal_vertices import eh_cubic_16k,clear_caches
HERE=Path(__file__).resolve().parent;DEST=HERE/'marked_polynomial';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    raw=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),engine_sha256=sha(HERE/'marked_polynomial_engine.py'),
    gauge_cubic='Derived from classical action covariance, checked against direct cubic below',
    completeness='O4 invariant polynomial, p=a e0,r=b e0+c e1,10 symmetric T and4v*4w bases',
    method='Exact QQ sparse ring q0..3,a,b,c; no numerical interpolation in external momenta',
    expectation='All160 residual polynomials vanish; fail on first nonzero',
    forbidden_inference='No finite causal anomaly or curved QME conclusion'))
start,cpu=perf_counter(),process_time();checks=[];nonzero=0
def check(name,e):
    assert e==ZERO,(name,str(e));checks.append(name)
bs=[]
for i in range(4):
    for j in range(i,4):
        H=[[ONE if (x,y) in [(i,j),(j,i)] else ZERO for y in range(4)] for x in range(4)];bs.append(H)
def flat(H):return tuple(x for row in H for x in row)
# Compare derived gauge-contracted cubic to the original Gamma-Gamma cubic
# at SYMBOLIC momenta, before either enters a quantum integral.
for j,k,m in [(0,0,0),(0,4,1),(1,1,2),(2,7,3),(4,8,0),(6,9,1),(3,5,2),(7,7,3)]:
    pa=scale(q,-1);pb=add(q,scale(P,-1))
    derived=cubic_gauge(bs[j],pa,bs[k],pb,P,axes[m])
    direct=eh_cubic_16k(flat(gauge(P,axes[m])),tuple(P),flat(bs[j]),tuple(pa),flat(bs[k]),tuple(pb))
    check(f'classical_Ward_symbolic_{j}_{k}_{m}',derived-direct)
    if derived:nonzero+=1
    clear_caches()
assert nonzero
print(json.dumps(dict(classical_symbolic_checks=len(checks),nonzero=nonzero)),flush=True)
cases=[];piece_nonzero=0
for ti,T in enumerate(bs):
    for vi,v in enumerate(axes):
        for wi,w in enumerate(axes):
            res,pieces=ward(T,v,w)
            check(f'BV_tensor_{ti}_{vi}_{wi}',res)
            if any(pieces):piece_nonzero+=1
            cases.append(dict(T=ti,v=vi,w=wi,residual_terms=len(res),pieces=list(map(str,pieces))))
    print(json.dumps(dict(T=ti,checked=(ti+1)*16,elapsed=perf_counter()-start)),flush=True)
assert piece_nonzero
result=dict(statute='REAL_FULL_POLYNOMIAL_PRINCIPAL_HSTAR_CC_BASIS',
    checks_passed=len(checks),nonvacuous_polarizations=piece_nonzero,
    momenta='p=a e0,r=b e0+c e1; a,b,c algebraically independent',cases=cases,
    completeness_argument='O4 covariance plus polarization multilinearity; no epsilon tensor, all momentum pairs rotate into the plane; polynomial extends degenerate cases',
    scope='principal logarithmic h*cc BV component, using classical cubic Ward derived from action',
    full_Q2=False,gate_changed=False,wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu,
    source_sha256=sha(Path(__file__)),plan_sha256=sha(DEST/'PRE_REGISTER.json'))
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='cases'}),flush=True)
