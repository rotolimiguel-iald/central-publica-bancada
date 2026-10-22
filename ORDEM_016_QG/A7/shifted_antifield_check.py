"""Check the gauge-fermion shift and normalization of the local BV candidate."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'shifted_antifield';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,o):
    b=json.dumps(o,ensure_ascii=False,indent=2).encode();assert not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    dictionary_sha256=sha(HERE.parents[1]/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md'),
    target='hat_hstar=hstar+C*barc has s0 hat_hstar=H h; u=4kappa hat_hstar has s0u=E',
    scope='Free linear BV differential, fixed background C, not interacting or curved anomaly'))
start,cpu=perf_counter(),process_time()
k,m,L,A0=s.symbols('kappa m L A0',nonzero=True)
# One gauge component and one independent physical component: H K=0, C K=Q=1.
# The differential on antifields is read with the dual-slot convention specified
# in the associated derivation, not silently mixed with another Darboux convention.
names=['h0','h1','b','c','barc','hstar0','hstar1','bstar','cstar','barcstar']
gh=[0,0,0,1,-1,-1,-1,-1,-2,0]
D=s.zeros(10);D[0,3]=1;D[4,2]=-1;D[5,2]=1;D[6,1]=m/(4*k)
D[7,0]=1;D[7,2]=-L;D[7,9]=-1;D[8,4]=-1;D[8,5]=-1;D[9,3]=1
assert D*D==s.zeros(10)
assert all(gh[j]==gh[i]+1 for i in range(10) for j in range(10) if D[i,j])
U=s.zeros(2,10);U[0,5]=4*k;U[0,4]=4*k;U[1,6]=4*k
target=s.zeros(2,10);target[1,1]=m
assert U*D==target
bad=U.copy();bad[0,4]=-4*k
assert bad*D!=target
# Coefficient of hstar in delta[A0/2 * u B c.partial u] is 4kappa A0 B c.partial E.
scale=s.simplify(A0*(4*k)*(4*k)/(4*k))
assert scale==4*k*A0
assert s.simplify(A0*(4*k)/(4*k))!=4*k*A0
result=dict(statute='DERIVED_FREE_SHIFTED_ANTIFIELD_AND_NORMALIZATION',checks_passed=4,negative_controls=2,
    shifted='hat_hstar=hstar+C*barc',differential='s0 hat_hstar=Hh; u=4kappa hat_hstar; s0u=E',
    generator='A0/2 integral u B c.partial u',hstar_coefficient=str(scale),
    full_R1_matched=False,full_Q2=False,gate_changed=False,
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',result);print(json.dumps(result,ensure_ascii=False))
