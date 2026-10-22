"""Audit Kimi's uniqueness claim with the existing fixed extension engines."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement
import hashlib,json,time,uuid
import sympy as s
from finite_harmonic_extension_engine_v2 import represent,harmonic_split,lap
from logarithmic_contact_engine import contact,residue,Q
from curved_source_jet_engine import x,z,L,dx,average
H=Path(__file__).resolve().parent;D=H/'harmonic_reference_audit';D.mkdir(exist_ok=True)
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
receipt=BASE/'state/handoffs/d0fd9aa9-1d09-451e-867b-a9e34ed775bb_delivery.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
 p=D/n;assert not p.exists(),p;raw=json.dumps(v,ensure_ascii=False,indent=2).encode()
 tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p)
raw=json.loads(receipt.read_bytes());text=raw['result']['text']
p=D/'KIMI_RESPONSE.md';assert not p.exists();p.write_bytes(text.encode())
payload=H/'orchestration_harmonic_followup/kimi_a7_harmonic_reference_intertwining_submit.json'
request=json.loads(payload.read_bytes())
put('RECEIPT.json',dict(source=str(receipt),source_sha256=sha(receipt),job_id=raw['job_id'],
 execution_task_id=raw['execution_task_id'],request_id=request['request_id'],
 prompt_sha256=hashlib.sha256(request['prompt'].encode()).hexdigest(),response_sha256=sha(p),
 usage=raw['result']['usage'],model=raw['result']['model'],new_call=False,
 cost_estimate_usd=None,cost_status='SUBSCRIPTION_UNKNOWN_NOT_ZERO'))
inputs=[Path(__file__),H/'finite_harmonic_extension_engine_v2.py',
 H/'logarithmic_contact_engine.py',H/'curved_source_jet_engine.py',p,D/'RECEIPT.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Same extension does not imply unique local/nonlocal split; derive exact correction before Ward assembly',
 no_prescription_change=True,sources=[dict(path=str(p),sha256=sha(p)) for p in inputs]))
cpu=time.process_time();checks=[]
def ck(n,v):assert s.expand(v)==0,(n,s.expand(v));checks.append(n)
q2=sum(q*q for q in Q)

# Nonzero off-diagonal kernel, NO remainder: F=partial_i^2 U1.
# D_H=(partial_i^2-Box/4)R(U1), X_P=partial_i^2 R(U1).
# Thus D_H-X_P=-Box R(U1)/4=-C_E delta/4.
second=[]
for i in range(4):
 F=dx(dx(1/z,i),i);rows,NH=represent(F);NP=contact(1,0,(i,i))
 ck(('NH_second',i),NH);ck(('NP_second',i),NP+s.Rational(1,4))
 assert NH!=NP
 second.append(dict(i=i,N_H=str(NH),N_P=str(NP),D_H_minus_XP_over_C=str(NP-NH)))
ck('fundamental_contact',sum(contact(1,0,(i,i)) for i in range(4))+1)

# Full quartic derivative basis on U2. Compare the two references, not just
# equality off the diagonal. Fit the invariant trace map, then check all35.
records=[];abc=s.symbols('a b');equations=[]
def lapq(v):return s.expand(sum(s.diff(v,q,2) for q in Q))
for indices in combinations_with_replacement(range(4),4):
 F=1/z**2
 for i in indices:F=dx(F,i)
 rows,NH=represent(F);NP=contact(2,0,indices)
 P=s.prod(Q[i] for i in indices)
 defect=s.expand(NP-NH)
 basis=[q2*lapq(P),q2**2*lapq(lapq(P))]
 equations.extend(s.Poly(s.expand(defect-sum(a*b for a,b in zip(abc,basis))),*Q).coeffs())
 records.append(dict(indices=indices,P=P,NH=NH,NP=NP,defect=defect,basis=basis))
solutions=s.solve(equations,abc,dict=True);assert len(solutions)==1
sol=solutions[0]
for row in records:
 ck(('quartic_trace_map',row['indices']),row['defect']-sum(sol[a]*b for a,b in zip(abc,row['basis'])))

# Kimi's explicit harmonic example: the local contact is correct, but the
# full UV residue polynomial changes even though the unweighted angular mean vanishes.
n=6*x[0]**2-2*sum(t*t for t in x[1:]);nq=n.subs(dict(zip(x,Q)))
ck('harmonic_n',lap(n));ck('angular_mean_n',average(n))
ck('weighted_angular_not_zero',average(n*x[0]**2)-s.Rational(1,2))
F=n/z**4;rows,NH=represent(F)
expected=5*(q2-4*Q[0]**2)/288
ck('kimi_harmonic_contact',NH-expected)
res=sum(c*residue(4,pow,(1,1,1,1)) for pow,c in s.Poly(n,*x).terms())
ck('full_residue_changed',res+nq/96);assert res!=0
for i in range(4):
 ck(('kimi_elementary_second',i),contact(2,0,(i,i))+(q2+5*Q[i]**2)/24)

# Compare rational kernels only after enforcing z=x.x/common denominator.
vanishing=1/z**2-sum(t*t for t in x)/z**3
ck('normalize_common_denominator',s.expand(vanishing*z**3).subs(z,sum(t*t for t in x)))
assert vanishing.coeff(z,-2)!=0

result=dict(at=datetime.now(timezone.utc).isoformat(),
 status='LOCAL_NONLOCAL_SPLIT_UNIQUENESS_REFUTED_TRACE_DEFECT_MEASURED',
 checks=len(checks),cpu_seconds=time.process_time()-cpu,
 second_derivative_counterexamples=second,
 corrected_identity='D_H-X_P-D_rem=C_E*(N_P+N_rem-N_H)(partial)delta',
 quartic_trace_map={str(k):str(v) for k,v in sol.items()},
 quartic_formula='N_P-N_H=a*q2*Lap(P)+b*q2^2*Lap^2(P)',
 quartic_basis=[{k:(list(v) if k=='indices' else str(v)) for k,v in row.items() if k!='basis'} for row in records],
 harmonic_example=dict(contact=str(NH),full_UV_residue=str(res),angular_mean=0,weighted_mean='1/2'),
 review_scope='Full response read; exact audit of split, quartic trace defect, harmonic example. Curved polynomial samples and Lorentzian normalization not validated here.',
 full_Q2=False,prescription_changed=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='quartic_basis'},ensure_ascii=False))
