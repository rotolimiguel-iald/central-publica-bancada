"""Verify all 10x10x4 polarizations at zero ghost momentum after fixed fitting."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
from marked_vertex_engine import marked,BASIS,AXES,gauge
HERE=Path(__file__).resolve().parent;DEST=HERE/'constant_ghost_full_basis';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,o):
    b=json.dumps(o,ensure_ascii=False,indent=2).encode();assert not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
fit=HERE/'constant_ghost_completion/results.json';data=json.loads(fit.read_bytes())
coeff=list(map(s.Rational,data['constant_Z_coefficients']))
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    fitted_sha256=sha(fit),engine_sha256=sha(HERE/'marked_vertex_engine.py'),
    target='R1(H,p;0,v)=-K_p Z_new(H,p;0,v)+(p.v)B(E_p H)',
    coverage='10 symmetric H x10 symmetric T x4 ghosts, p=e0; O4+homogeneity extends p!=0',
    no_refitting=True,full_finite_anomaly=False))
start,cpu=perf_counter(),process_time();p=AXES[0];zero=s.zeros(4,1)
cases=[];fail=[];nonzero=0
for hi,h in enumerate(BASIS):
    C=h*p-p*s.trace(h)/2
    E=p.dot(p)*(h-s.eye(4)*s.trace(h)/2)-(p*C.T+C*p.T-s.eye(4)*p.dot(C))
    for vi,v in enumerate(AXES):
        ts=[v*s.trace(h)*p.dot(p),v*p.dot(h*p),h*v*p.dot(p),h*p*p.dot(v),p*s.trace(h)*p.dot(v),p*v.dot(h*p)]
        Z=sum((a*z for a,z in zip(coeff,ts)),zero)
        bv=p.dot(v)*(-E/6-s.eye(4)*s.trace(E)/12)
        prediction=-gauge(p,Z)+bv
        for ti,T in enumerate(BASIS):
            actual,*_=marked(T,h,p,zero,v);expect=s.trace(T*prediction)
            if actual:nonzero+=1
            if actual!=expect:fail.append(dict(H=hi,v=vi,T=ti,actual=str(actual),predicted=str(expect),residue=str(actual-expect)))
            cases.append(dict(H=hi,v=vi,T=ti,actual=str(actual),predicted=str(expect)))
    print(json.dumps(dict(H_completed=hi,components=len(cases),mismatches=len(fail))),flush=True)
result=dict(statute='DERIVED_FULL_CONSTANT_GHOST_PRINCIPAL_VERTEX' if not fail else 'MEDIDA_CONSTANT_GHOST_COMPLETION_MISMATCH',
    components=len(cases),nonzero_components=nonzero,mismatches=fail,cases=cases,
    formula='R1(H,p;0,v)=-K_p Z_new+(p.v)B(E_pH)',
    arbitrary_nonzero_ghost_momentum=False,full_Q2=False,gate_changed=False,
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='cases'},ensure_ascii=False))
