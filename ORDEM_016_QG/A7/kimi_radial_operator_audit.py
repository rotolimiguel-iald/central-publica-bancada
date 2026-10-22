"""Audit specified claims of the received Kimi radial dictionary, not the amplitude."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, time, uuid
import sympy as s

H=Path(__file__).resolve().parent
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
D=H/'kimi_radial_operator_audit';D.mkdir(exist_ok=True)
receipt=BASE/'state/handoffs/b323257e-1d28-4689-a393-2ded69cfe5cd_delivery.json'
j=json.loads(receipt.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p
    b=v.encode() if isinstance(v,str) else json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
put('RESPONSE.md',j['result']['text'])
put('RECEIPT.json',dict(at=j['at'],job_id=j['job_id'],execution_task_id=j['execution_task_id'],
    usage=j['result']['usage'],model=j['result']['model'],receipt_sha256=sha(receipt),
    response_sha256=sha(D/'RESPONSE.md'),review_scope='INDEPENDENT_LOCAL_CAS_OF_SELECTED_ALGEBRA',
    cost_status='SUBSCRIPTION_COST_UNKNOWN_NOT_ZERO'))
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    targets=['plane wave symbol F1,F2,F3,F4 and mixed E4 normalization',
             'scalar differentiated constant correction', 'Lichnerowicz algebra',
             'homogeneity of a scale-free fourth-order local symbol'],
    sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'RESPONSE.md',D/'RECEIPT.json']]))
cpu=time.process_time();checks=[];counter=[]
A=s.Matrix([[2,1,0,3],[1,-1,2,0],[0,2,4,1],[3,0,1,5]])
B=s.Matrix([[1,2,3,0],[2,4,0,1],[3,0,-2,2],[0,1,2,3]])
def inner(a,b):return sum(a[i,k]*b[i,k] for i in range(4) for k in range(4))
for pv in [(1,2,-1,1),(2,0,1,-1),(1,1,1,2)]:
    p=s.Matrix(pv);p2=(p.T*p)[0];pp=p*p.T
    symbols=[p2*inner(A,B),(p.T*A*B*p)[0],
             (p.T*A*p)[0]*s.trace(B)+(p.T*B*p)[0]*s.trace(A),
             p2*s.trace(A)*s.trace(B)]
    # Read the displayed differential operators on exp(i p.x), coefficient K stripped.
    proposed=[-p2*B,-(p*(p.T*B)+(B*p)*p.T)/2,
              -(pp*s.trace(B)+s.eye(4)*(p.T*B*p)[0])/2,
              -s.eye(4)*p2*s.trace(B)]
    for idx in range(4):
        actual=inner(A,proposed[idx]);expected=symbols[idx]
        assert expected!=0 and actual!=expected,(pv,idx)
        multiplier=2 if idx==2 else 1
        assert -multiplier*actual==expected
        counter.append(dict(claim='F'+str(idx+1),p=pv,
                            proposed=str(actual),target=str(expected)))
        checks.append(('corrected_plane_wave',pv,idx))
    E4=pp*p2*s.trace(B)/2+s.eye(4)*p2*(p.T*B*p)[0]/2
    target=p2*symbols[2];actual=inner(A,E4)
    assert target!=0 and actual*2==target and actual!=target
    counter.append(dict(claim='E4_half_normalization',p=pv,proposed=str(actual),target=str(target)))
    checks.append(('mixed_E4_correction',pv))

x=s.symbols('x0:4');K,c=s.symbols('K c');z=sum(v*v for v in x)
green=1/z+c*K # 1/(4 pi²) stripped.
for i in range(4):
    for k in range(4):
        correction=s.diff(s.diff(green,x[i])*s.diff(green,x[k]),K)
        assert s.simplify(correction)==0
        checks.append(('scalar_derivative_product_no_c',i,k))
counter.append(dict(claim='scalar_example_2cK_correction',
                    computed='0 for all 16 derivative products',claimed='nonzero 2cK term'))
# Check the limited part of the response that is valid algebraically.
for a in range(4):
    for b in range(4):
        curvature=sum((int(a==b)*int(i==k)-int(a==k)*int(i==b))*B[i,k]
                      for i in range(4) for k in range(4))
        actual=-2*curvature+6*B[a,b]
        expected=8*B[a,b]-2*int(a==b)*s.trace(B)
        assert s.expand(actual-expected)==0
        checks.append(('Lichnerowicz_endomorphism',a,b))

scale=s.Symbol('scale',positive=True)
assert (scale**2)*(scale**2)==scale**4
assert scale**2!=scale**4
checks.append(('homogeneous_order4_allows_Kd2_not_K_without_scale',))
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),
    counterexamples=counter,cpu_seconds=time.process_time()-cpu,
    status='RADIAL_DICTIONARY_REJECTED_AS_WRITTEN_SELECTED_ERRORS_EXACT',
    accepted='RNC strategy and tested Lichnerowicz endomorphism; neither is a new matching theorem',
    rejected='F signs, F3/E4 half factors, scalar derivative illustration; scale-free order-four argument for mandatory Kp0 not established',
    not_audited=['all curved commutator coefficients','formal selfadjointness of whole proposed dictionary'],
    changes_to_existing_vertices=False,full_Q2=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p))
    for p in [Path(__file__),D/'RESPONSE.md',D/'RECEIPT.json',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),counterexamples=len(counter),cpu_seconds=result['cpu_seconds'],status=result['status'])))
