"""Audit the received quartic proposal against independent existing vertices."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import permutations
import ast,hashlib,importlib.util,json,random,re,time,uuid
import metric_principal_vertices as P
import metric_quartic_vertices as Q
H=Path(__file__).resolve().parent;D=H/'kimi_quartic_local_audit';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v,text=False):
    p=D/n;assert not p.exists(),p
    b=(v if text else json.dumps(v,indent=2,ensure_ascii=False)).encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
source=H/'bilocal_point_delivery/KIMI_QUARTIC_RESPONSE.md'
blocks=re.findall(r'```python\s*\n(.*?)\n```',source.read_text('utf-8'),re.S)
assert len(blocks)==1
code=blocks[0];ast.parse(code)
# The whole block was read before this extraction: only local mathematical code.
put('KIMI_CODE_UNCHANGED.py',code,True)
sources=[Path(__file__),source,D/'KIMI_CODE_UNCHANGED.py',H/'metric_principal_vertices.py',H/'metric_quartic_vertices.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 aim='Independent equivalence and diagnosis of proposal self-tests, no vertex modification',
 plans=['original selftests individually','noncommuting dense quartic crosscheck',
        'nonzero ghost momentum Ward','wrong Lie-momentum control','determinant origin control'],
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources],full_Q2=False))
spec=importlib.util.spec_from_file_location('kimi_quartic_received',D/'KIMI_CODE_UNCHANGED.py')
K=importlib.util.module_from_spec(spec);spec.loader.exec_module(K)
assert K._ANNEX and K.eh_cubic_16k is P.eh_cubic_16k
cpu=time.process_time();selftests=[];checks=[];neg=[]
for name in ['test_bose','test_gg_contraction','test_ward','test_conformal','test_sqrt_det','test_negative_control','test_zero_field']:
    try:getattr(K,name)();row=dict(name=name,status='PASSED')
    except AssertionError as e:row=dict(name=name,status='FAILED',error=str(e))
    selftests.append(row);print('ORIGINAL_SELFTEST',json.dumps(row),flush=True)
def check(name,lhs,rhs=0):
    assert lhs==rhs,(name,lhs,rhs);checks.append(name)
def add(p,q):return tuple(a+b for a,b in zip(p,q))
noncommuting=0;ward_nonzero=0
for seed in range(12):
    rng=random.Random(916010+seed)
    fs=[K.rand_field(rng) for _ in range(4)]
    ps=K.rand_momenta(rng,4,conserved=False)
    if K.mmul(fs[0],fs[1])!=K.mmul(fs[1],fs[0]):noncommuting+=1
    lhs=K.eh_quartic_32k(*[x for f,p in zip(fs,ps) for x in (f,p)])
    check('quartic_crosscheck_'+str(seed),lhs,Q.eh_quartic_32k(*zip(fs,ps)))
    # Three unconstrained metric momenta, and the fourth (ghost) balances them.
    A,B,C=fs[:3];p,q,r=ps[:3];k=tuple(-sum(t[j] for t in (p,q,r)) for j in range(4))
    assert k!=(0,0,0,0)
    v=tuple(rng.randint(-2,2) for _ in range(4));g=P.gauge_matrix(k,v)
    lhs=K.eh_quartic_32k(A,p,B,q,C,r,g,k)
    rhs=0;bad=0
    legs=[(A,p),(B,q),(C,r)]
    for i,(field,momentum) in enumerate(legs):
        rest=[leg for j,leg in enumerate(legs) if j!=i]
        correct=P.lie_matrix(field,momentum,k,v)
        wrong=P.lie_matrix(field,momentum,add(momentum,k),v)
        rhs+=P.eh_cubic_16k(correct,add(momentum,k),*rest[0],*rest[1])
        bad+=P.eh_cubic_16k(wrong,add(momentum,k),*rest[0],*rest[1])
    check('nonzero_ghost_Ward_'+str(seed),lhs+2*rhs)
    if lhs:ward_nonzero+=1
    if lhs+2*bad:neg.append(dict(name='wrong_Lie_momentum',seed=seed,residual=lhs+2*bad))
    P.clear_caches()
    print('CROSSCHECK',seed,'cpu',time.process_time()-cpu,flush=True)
assert noncommuting==12 and ward_nonzero>0 and neg
# A deterministic zero-perturbation diagnostic catches the determinant typing error.
zero=tuple(0 for _ in range(16))
check('series_zero_perturbation',sum(K.sqrt_det_series(zero)),1)
misapplied=sum(K.sqrt_det_series(P.I))-1
assert misapplied!=0
neg.append(dict(name='total_metric_used_as_perturbation_at_h0',residual=str(misapplied)))
ghost_momenta=[]
for seed in range(10):
    rng=random.Random(3000+seed)
    for _ in range(3):K.rand_field(rng)
    ps=K.rand_momenta(rng,3)
    k=tuple(-sum(p[i] for p in ps) for i in range(4))
    check('original_zero_ghost_'+str(seed),k,(0,0,0,0));ghost_momenta.append(k)
result=dict(at=datetime.now(timezone.utc).isoformat(),
 status='QUARTIC_AGREES_EXISTING_VERTEX_SELFTEST_ERRORS_MEASURED',
 original_selftests=selftests,independent_checks=len(checks),check_names=checks,
 negative_controls=neg,noncommuting_examples=noncommuting,nonzero_ward_examples=ward_nonzero,
 original_ghost_momenta=ghost_momenta,cpu_seconds=time.process_time()-cpu,
 vertex_modified=False,existing_tadpole_changed=False,full_Q2=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
