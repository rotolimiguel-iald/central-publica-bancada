"""Construct, but do not adopt, a primitive for the measured mixed contact shift."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time,uuid
import sympy as s
H=Path(__file__).resolve().parent;D=H/'flat_mixed_smooth_primitive';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();raw=json.dumps(v,indent=2).encode()
    q=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);q.write_bytes(raw)
    assert q.read_bytes()==raw;q.replace(p)
source=H/'flat_mixed_smooth_bubble/results.json';data=json.loads(source.read_bytes())
inputs=[Path(__file__),source,H/'smooth_reference_transport_audit/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Measured N G+E R residual of flat mixed constant-W contact shift; local primitive with gauge-invariant ambiguity retained',
    method='N_eff=N_bubble+E L+L E; compare against all stored residual components, then fiber transpose',
    no_new_prescription=True,full_Q2=False,sources=[dict(path=str(p),sha256=sha(p)) for p in inputs]))
cpu=time.process_time();p=s.Matrix(s.symbols('p0:4'));p2=p.dot(p);I=s.eye(4);eta=s.Symbol('eta',real=True)
def G(v):return p*v.T+v*p.T
def N(co,h):
    a,b,c,d=co
    return a*p2*h+b*p2*s.trace(h)*I+c*(p*p.T*s.trace(h)+I*(p.T*h*p)[0])+d*(p*(h*p).T+(h*p)*p.T)/2
eb=[-1,1,-1,2];checks=[];records={}
def ck(n,v):assert s.expand(v)==0,(n,s.expand(v));checks.append(n)
for sector in ['metric_I','metric_T']:
    old=list(map(s.Rational,data['sectors'][sector]['coefficients']))
    la=-s.Rational(1,2);lb=-s.Rational(1,8) if sector=='metric_I' else s.Rational(1,4)
    companion=[-2*la,2*la+4*lb,-2*la-2*lb,4*la]
    effective=[s.expand(a+b) for a,b in zip(old,companion)]
    family=[a+eta*b for a,b in zip(effective,eb)]
    previous={(v['r'],v['i'],v['j']):s.sympify(v['value'])
              for v in data['sectors'][sector]['Ward_NG_plus_ER_nonzero_components']}
    for r in range(4):
        actual=N(family,G(I[:,r]))
        for a in range(4):
            for b in range(4):ck((sector,'residual',r,a,b),actual[a,b]-previous.get((r,a,b),0))
    basis=[]
    for a in range(4):
        for b in range(a,4):
            v=s.zeros(4);v[a,b]=v[b,a]=1;basis.append(v)
    images=[N(family,v) for v in basis]
    for a,v in enumerate(basis):
        for b,w in enumerate(basis):ck((sector,'adjoint',a,b),s.trace(v*images[b]-images[a]*w))
    aa,bb,cc,dd=effective
    records[sector]=dict(effective_coefficients=list(map(str,effective)),
        free_family=list(map(str,family)),
        Ward_basis_g_p2pv_p2G_pppv=list(map(str,[2*(bb+cc),aa+dd/2,2*cc+dd])))
result=dict(at=datetime.now(timezone.utc).isoformat(),
    status='LOCAL_PRIMITIVE_FOR_MEASURED_FLAT_MIXED_CONTACT_SHIFT',
    checks=len(checks),cpu_seconds=time.process_time()-cpu,sectors=records,
    primitive='B=-C_E/2 integral h.N_eff h; adding eta*E does not change s0B because E G=0',
    representative_selected=False,prescription_changed=False,full_Q2=False,
    limitation='Only the measured constant-W flat contact shift relative to the derivative-defined reference; not all local Q2 terms')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p))
    for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
