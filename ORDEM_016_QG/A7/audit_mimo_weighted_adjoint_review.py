"""Audit a completed MiMo review without changing the existing Ward engines."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, time, uuid
import sympy as s

H = Path(__file__).resolve().parent
BASE = H.parents[1] / 'IALD_ORQUESTRACAO_20260923'
OUT = H.parents[1] / 'TUNEL/DO_CHATGPT'
D = H / 'mimo_weighted_adjoint_review'
D.mkdir(exist_ok=False)
now = datetime.now(timezone.utc)
stamp = now.strftime('%Y%m%d_%H%M%S_%f')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, data, append=False):
    if path.exists():
        assert append, path
        old = path.read_bytes()
        backup = path.with_name(path.name+'.bak_'+stamp)
        assert not backup.exists()
        backup.write_bytes(old)
        assert backup.read_bytes() == old
        data = old + data
    temp = path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    temp.write_bytes(data)
    assert data and temp.read_bytes() == data
    temp.replace(path)

def put(path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8'))

source = BASE/'state/handoffs/5286ee12-8b8c-44d2-8af3-8dcd5562fe17_delivery.json'
receipt = json.loads(source.read_bytes())
job = receipt['job']; execution = job['execution']; result = execution['result']
assert job['stage'] == 'completed' and execution['status'] == 'result_ready'
ledger = OUT/'LEDGER_016.jsonl'
assert execution['id'] not in {json.loads(line).get('execution_task_id')
                            for line in ledger.read_text('utf-8').splitlines()}
write(D/'RECEIPT.json', source.read_bytes())
write(D/'RESPONSE.md', result['text'].encode('utf-8'))
put(D/'INTAKE.json', dict(at=now.isoformat(), job_id=job['id'],
    request_id=job['request_id'], execution_task_id=execution['id'],
    source=str(source), receipt_sha256=sha(source), status='RECEIVED_FOR_AUDIT'))

start = time.process_time(); checks = 0
def eq(left, right):
    global checks
    assert s.expand(left-right) == 0, (left, right)
    checks += 1

def neq(left, right):
    global checks
    assert s.expand(left-right) != 0, (left, right)
    checks += 1

q = s.symbols('q0:4'); lam = s.symbols('l0:4'); eta = s.symbols('e0:4')
L = [lam[i]+eta[i] for i in range(4)]
# Derive the h-coordinate multiplicities directly from each variation,
# instead of reusing the candidate matrix formula.
coeffs = {(i,j,r): (i+1)*q[r]**2 + (j+1)*q[(r+1)%4] + r+1
          for i in range(4) for j in range(i,4) for r in range(4)}
direct = s.zeros(4)
for (i,j,r), a in coeffs.items():
    direct[j,r] -= (q[i]+L[i])*a
    direct[i,r] -= (q[j]+L[j])*a
candidate = s.Matrix(4,4, lambda j,r: -sum(
    (1+int(i==j))*(q[i]+L[i])*coeffs[min(i,j),max(i,j),r] for i in range(4)))
for a,b in zip(direct, candidate): eq(a,b)

# The response inserts one extra transpose in its displayed proof.
# A formally self-adjoint differential matrix need not be pointwise symmetric.
t, ell = s.symbols('t ell')
B = s.Matrix([[0,t],[-t-ell,0]])
dagger = lambda M: M.T.subs(t,-t-ell).applyfunc(s.expand)
for a,b in zip(B,dagger(B)): eq(a,b)
neq(B[0,1],dagger(B).T[0,1])
for a,b in zip(dagger(dagger(B)), B): eq(a,b)
eq((t*t).subs(t,-t-ell)-t*t, 2*ell*t+ell*ell)
neq(t, -t-ell)

# A(q) is a polynomial in delta derivatives, not Fourier momentum.
# Moving chi_X to the diagonal is q->q-lambda; then the local operator
# acts on exp((lambda+eta)x)c: q->D+L. The net shift is D+eta.
polys = [q[0], q[0]**2, q[0]*q[1], q[0]**3+q[2]**2,
         q[0]*q[1]*q[2]*q[3]]
for a in polys:
    moved = a.subs(dict(zip(q,[q[i]-lam[i] for i in range(4)])), simultaneous=True)
    local = moved.subs(dict(zip(q,[q[i]+L[i] for i in range(4)])), simultaneous=True)
    expected = a.subs(dict(zip(q,[q[i]+eta[i] for i in range(4)])), simultaneous=True)
    eq(local, expected)
neq(1+eta[0], -s.I*(1+eta[0]))

audit = dict(at=now.isoformat(), checks=checks, cpu_seconds=time.process_time()-start,
 accepted=['Diagonal factor2 and off-diagonal factor1 for sum over i<=j; agrees with existing coordinate engine',
           'Formal transpose adjoint B^T(-D-L), two independent counterexamples to dropping derivative/weight'],
 corrections=['Section3.2 transposes twice: correct Q(B)=-Q(B^dagger), not -Q((B^dagger)^T)',
              'Section4 changes q from delta-derivative symbol to Fourier momentum. Existing local shift is A(q-lambda) then q=D+L, net A(D+eta); no unconverted -i.',
              'Nonzero s0A proves failure of homogeneous closure for this representative. It does not define a non-exact cohomology class; inhomogeneous consistency must include insertions.',
              'Statement that mixed b-h and ghost currents remain uncomputed is unsupported by this task and contradicted by existing opposite_endpoint and full_current results. Do not duplicate them.'],
 scope='Finite polynomial audit of the response, not a new physical or full Ward theorem',
 new_engine=False, full_Q2=False, gate_changed=False)
put(D/'local_audit.json', audit)
put(D/'manifest.json', dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
    [Path(__file__),D/'RECEIPT.json',D/'RESPONSE.md',D/'INTAKE.json',D/'local_audit.json']],
    gate_changed=False))
accounting = result['request_cost_accounting']
event = dict(at=now.isoformat(), event='INDEPENDENT_REVIEW_RECEIVED', provider='mimo',
    target='A7.b', job_id=job['id'], request_id=job['request_id'], execution_task_id=execution['id'],
    usage=result['usage'], cost_estimate_usd=accounting['accounted_usd'],
    cost_status=accounting['status'], provider_elapsed_seconds=result['elapsed_seconds'],
    receipt_sha256=sha(source), response_sha256=sha(D/'RESPONSE.md'),
    prompt_sha256=hashlib.sha256(job['prompt'].encode()).hexdigest(),
    remote_call_by_this_script=False)
write(ledger, (json.dumps(event)+'\n').encode('utf-8'), True)
print(json.dumps(dict(audit=audit, intake=event), ensure_ascii=False))
