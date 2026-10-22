"""Compare closed-form coefficients supplied by MiMo to the direct vertex sums."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
import hashlib,json,time,uuid
import sympy as s
from localized_source_boundary_engine import source_coefficients,source_reduced
from full_loop_extension_engine import x,z,terms,Q
from logarithmic_contact_engine import residue
H=Path(__file__).resolve().parent;D=H/'mimo_source_preibp_review/local_audit';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
start=time.process_time();checks=0;failures=[]
delta=lambda a,b:int(a==b)
def reduce(f):return s.expand((s.expand(f)*z**6).expand().subs(z,sum(v*v for v in x)))
for eta in [(0,0,0,0),(1,0,0,0),(1,-1,2,1)]:
    ex=sum(eta[i]*x[i] for i in range(4))
    for u,v,r in product(range(4),repeat=3):
        A,B=source_coefficients(u,v,r,eta)
        closedA=-2*(x[u]*delta(r,v)+x[v]*delta(r,u))/z**4-20*delta(u,v)*x[r]/z**4+96*x[u]*x[v]*x[r]/z**5
        closedA+=-(eta[u]*delta(r,v)+eta[v]*delta(r,u))/z**3+14*(eta[u]*x[v]+eta[v]*x[u])*x[r]/z**4
        diff=reduce(A-closedA);checks+=1
        if diff!=0:failures.append(dict(kind='A',eta=eta,u=u,v=v,r=r,difference=str(s.factor(diff))))
        for j in range(4):
            B4=20*delta(u,r)*x[v]*x[j]+20*delta(v,r)*x[u]*x[j]-4*delta(u,v)*x[r]*x[j]
            B4+=-8*delta(u,j)*x[v]*x[r]-8*delta(v,j)*x[u]*x[r]+16*delta(j,r)*x[u]*x[v]
            B3=-4*delta(u,j)*delta(v,r)-4*delta(u,r)*delta(v,j)-2*delta(u,v)*delta(j,r)
            B3+=eta[j]*(5*delta(u,r)*x[v]+5*delta(v,r)*x[u]-delta(u,v)*x[r])
            B3+=x[j]*(eta[u]*delta(v,r)+eta[v]*delta(u,r)-delta(u,v)*eta[r])
            B3+=ex*(delta(u,j)*delta(v,r)+delta(u,r)*delta(v,j)-delta(u,v)*delta(j,r))
            B3+=2*x[v]*(eta[u]*delta(j,r)-delta(u,j)*eta[r])+2*x[u]*(eta[v]*delta(j,r)-delta(v,j)*eta[r])
            diff=reduce(B[j]-B3/z**3-B4/z**4);checks+=1
            if diff!=0:failures.append(dict(kind='B',eta=eta,u=u,v=v,r=r,j=j,difference=str(s.factor(diff))))

# Residue of DeltaH alone, not E acting on it and not the full P-Q.
dH=s.expand(source_reduced(1,1,0,(1,0,0,0))-source_reduced(1,1,0,(0,0,0,0)))
R=s.expand(sum(c*residue(n,p,(1,1,1,1)) for n,p,c in terms(dH)))
physical=s.expand(-4*R) # coefficient of pi^2, since C_E=-4pi^2
values=[physical.subs(dict(zip(Q,p))) for p in [(2,1,0,0),(1,2,0,0)]]
assert values==[s.Rational(11,4),s.Rational(5,2)];checks+=2
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
    coefficient_failure_count=len(failures),failures=failures,deltaH_residue_over_pi2=list(map(str,values)),
    reviewed_limits=['DeltaH residue is not the full Einstein/source contact',
      'The Einstein operator acts on uv with r spectator in the existing engine; model uncertainty does not reopen this convention',
      'No assertion that omitted one summand equals total change in P-Q',
      'Contact commutator existed in earlier source_two_cutoff work; no novelty inferred from absence in model context'],
    full_Q2=False,gate_changed=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
    [Path(__file__),H/'mimo_source_preibp_review/RESPONSE.md',H/'localized_source_boundary_engine.py',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='failures'}))
