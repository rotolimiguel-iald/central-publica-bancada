"""Independent integrated counterexample to dropping cutoff commutators."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time
import sympy as s
H=Path(__file__).resolve().parent;D=H/'deepseek_cutoff_audit';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):
 p=D/n;assert not p.exists(),p
 b=v.encode() if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2).encode()
 t=p.with_suffix('.tmp');t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
src=H.parents[1]/'IALD_ORQUESTRACAO_20260923/state/handoffs/7df6c82e-f427-4c85-865e-68259cc829f8_delivery.json'
save('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(src),
 tests=['Direct integrated first variation vs Hessian with and without cutoff commutator',
        'Same-vector skew-adjoint cancellation versus mixed variation',
        'Verify existing phase and cutoff manifests without rerunning their tests'],new_remote_call=False))
start=time.process_time();checks=0
def eq(a,b):
 global checks
 assert s.expand(a-b)==0,(a,b);checks+=1
x,e=s.symbols('x epsilon',real=True)
h=(1-x*x)**6;v=x*x*h;chi=(1-x*x)**6
def integ(p):return s.integrate(s.expand(p),(x,-1,1))
def N(p):return s.diff(p,x,4)
comm=s.expand(N(chi*h)-chi*N(h))
eq(comm,4*s.diff(chi,x)*s.diff(h,x,3)+6*s.diff(chi,x,2)*s.diff(h,x,2)+4*s.diff(chi,x,3)*s.diff(h,x)+s.diff(chi,x,4)*h)
B=-integ(chi*(h+e*v)*N(h+e*v))/2
direct=s.diff(B,e).subs(e,0)
correct=-integ(v*(chi*N(h)+comm/2));wrong=-integ(chi*v*N(h))
eq(direct,correct);assert direct!=wrong;checks+=1
eq(integ(h*comm),0)
eq(direct-wrong,-integ(v*comm)/2)
# Piecewise polynomial extensions by zero have sufficient C5 endpoint regularity.
for f in (h,v,chi):
 for order in range(6):
  for endpoint in (-1,1):eq(s.diff(f,x,order).subs(x,endpoint),0)
verified=[]
for name in ('fourier_phase_convention','pair_fourier_phase','fourth_order_cutoff_bridge'):
 m=H/name/'manifest.json'
 for row in json.loads(m.read_bytes())['artifacts']:
  assert sha(Path(row['path']))==row['sha256']
 result=json.loads((H/name/'results.json').read_bytes())
 verified.append(dict(name=name,manifest_sha256=sha(m),previous_checks=result['checks'],rerun=False))
d=json.loads(src.read_bytes());save('DEEPSEEK_RESPONSE.md',d['result']['text'])
payload=H/'orchestration_contact_bridge_v2/deepseek_fourth_order_primitive_adjoint_cutoff_submit.json'
pj=json.loads(payload.read_bytes())
receipt=dict(at=datetime.now(timezone.utc).isoformat(),provider='deepseek',target='A7.b',
 event='RECEIVED_CUTOFF_REVIEW_AUDITED',request_id=pj['request_id'],job_id=d['job_id'],execution_task_id=d['execution_task_id'],
 prompt_sha256=hashlib.sha256(pj['prompt'].encode()).hexdigest(),response_sha256=sha(D/'DEEPSEEK_RESPONSE.md'),
 source=str(src),source_sha256=sha(src),usage=d['result']['usage'],model=d['result']['model'],
 cost_estimate_usd=d['result']['cost_estimate_usd'],cost_status=d['result']['cost_status'],new_call=False)
save('RECEIPT.json',receipt)
r=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 direct_variation_over_C=str(direct),corrected_variation_over_C=str(correct),claimed_variation_over_C=str(wrong),
 omitted_term_over_C=str(direct-wrong),same_vector_commutator_integral=0,
 identity='Hessian=(chi*N+N*chi)/2; skew-adjointness does not remove mixed term',
 previous_artifacts_verified=verified,phase_status='Already resolved by previous plus-plane audit; no engine change needed',
 full_Q2=False,gate_changed=False)
save('results.json',r)
save('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),src,payload]+list(D.iterdir()) if p.is_file()]))
print(json.dumps(r))
