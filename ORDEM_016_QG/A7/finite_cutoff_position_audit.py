"""Independent position-space integrations; no imports from the momentum audit."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,time,uuid
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'finite_cutoff_position';DEST.mkdir(exist_ok=True)
def new(name,obj):
    p=DEST/name;assert not p.exists();b=json.dumps(obj,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
new('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    method='Exact position polynomial integrations on [-1,1]; chi and first five derivatives vanish at endpoints',
    scope='Univariate test of genuine cutoff terms, Euclidean principal sector',
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
cpu=time.process_time();x=s.Symbol('x');p=s.eye(4)[:,0];chi=(1-x*x)**6
ns=list(map(s.Rational,json.loads((HERE/'finite_principal_contact/results.json').read_bytes())['finite_contact_coefficients_over_C']))
rs=list(map(s.Rational,json.loads((HERE/'finite_antifield_contact_v3/results.json').read_bytes())['source_contact_coefficients']))
def dot(H,T):return s.trace(H*T)
def derivative(M,n=1):return M.applyfunc(lambda y:s.diff(y,x,n))
def K(v):
    dv=derivative(v);return p*dv.T+dv*p.T
def Kstar(H):return -2*derivative(H*p)
def N(H):
    F=derivative(H,4);hp=F*p;tr=s.trace(F);ph=F[0,0]
    return ns[0]*F+ns[1]*s.eye(4)*tr+ns[2]*(tr*p*p.T+ph*s.eye(4))+ns[3]*(hp*p.T+p*hp.T)/2+ns[4]*ph*p*p.T
def Itr(H):return H-s.eye(4)*s.trace(H)/2
def E(H):
    cp=derivative(H*p-p*s.trace(H)/2)
    return derivative(Itr(H),2)-Itr(K(cp))
def R(v):
    w=derivative(v,3)
    return rs[0]*(p*w.T+w*p.T)+rs[1]*p*p.T*w[0]+rs[2]*s.eye(4)*w[0]
def Rstar(H):
    F=derivative(H,3)
    return -2*rs[0]*F*p-(rs[1]*F[0,0]+rs[2]*s.trace(F))*p
def integrate(y):
    poly=s.Poly(s.expand(y),x)
    return sum(c*s.Rational(2,n[0]+1) for n,c in poly.terms() if n[0]%2==0)
checks=0;records=[]
for i in range(6):
    assert s.diff(chi,x,i).subs(x,1)==s.diff(chi,x,i).subs(x,-1)==0;checks+=1
for power in [4,5,6]:
    H=s.diag(x**power, x*x+x**power,1+x, x**3)
    H[0,1]=H[1,0]=x**3+x**5
    v=s.Matrix([x**3+x**5,x*x,1+x**3,x**4])
    metric=integrate(chi*(dot(K(v),N(H))+dot(H,N(K(v))))/2)
    bulk=integrate(chi*(v.T*Kstar(N(H)))[0])
    completion=(Kstar(chi*N(H))-chi*Kstar(N(H)))+Kstar(N(chi*H)-chi*N(H))/2
    corrected=integrate((v.T*(chi*Kstar(N(H))+completion))[0])
    assert metric==corrected;checks+=1
    source=integrate(chi*dot(E(H),R(v)))
    source_bulk=integrate(chi*(v.T*Rstar(E(H)))[0])
    source_corrected=integrate((v.T*Rstar(chi*E(H)))[0])
    assert source==source_corrected;checks+=1
    records.append(dict(power=power,metric=str(metric),metric_omitted_boundary=str(metric-bulk),
        source=str(source),source_omitted_boundary=str(source-source_bulk)))
assert any(s.Rational(r['metric_omitted_boundary'])!=0 for r in records)
assert any(s.Rational(r['source_omitted_boundary'])!=0 for r in records)
new('results.json',dict(checks=checks,negative_controls=2,records=records,
    cpu_seconds=time.process_time()-cpu,full_curved_causal_Q2=False))
print(json.dumps(dict(checks=checks,negative_controls=2,records=records,cpu_seconds=time.process_time()-cpu)))
