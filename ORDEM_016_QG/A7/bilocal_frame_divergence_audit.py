"""Independent coordinate check of radial-frame X divergence reconstruction."""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
import ast,hashlib,json,time,uuid
import sympy as s
import bilocal_first_curvature_engine as B
H=Path(__file__).resolve().parent;D=H/'bilocal_frame_divergence_audit';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
source=H/'bilocal_full_external_pair_check.py'
tree=ast.parse(source.read_text('utf-8'))
defs=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in ('d','f4','omega','divergence')]
assert len(defs)==4
scope=dict(s=s,L=B.L,n=(1,0,0,0))
exec(compile(ast.Module(body=defs,type_ignores=[]),str(source),'exec'),scope)
candidate=scope['divergence'];z=B.w;x=B.x;L=B.L
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Coordinate divergence after converting three contravariant X indices, versus frame formula',
 source_sha256=sha(source),audit_sha256=sha(Path(__file__)),
 basis_count=7,tests='Individual tensor basis and log-polynomial combinations, K0/K1; three readout components'))
cpu=time.process_time();checks=[];negative=[]
def delta(a,b):return s.Integer(a==b)
def dx(f,i):return s.diff(f,x[i])+2*x[i]*(s.diff(f,z)+s.diff(f,L)/z)
def e(a,b):return (z*delta(a,b)-x[a]*x[b])/6
def gamma(c,i,a):return -(delta(c,a)*x[i]+delta(c,i)*x[a]-2*delta(i,a)*x[c])/3
def at(f):return s.expand(f.subs(dict(zip(x,(1,0,0,0)))).subs(z,1))
def expr(c,o,i,a,b,r):
    terms=[delta(i,r)*delta(a,b),delta(i,a)*delta(b,r)+delta(i,b)*delta(a,r),
      delta(a,b)*x[i]*x[r],delta(i,r)*x[a]*x[b],
      delta(i,a)*x[b]*x[r]+delta(i,b)*x[a]*x[r],
      delta(a,r)*x[i]*x[b]+delta(b,r)*x[i]*x[a],x[i]*x[a]*x[b]*x[r]]
    return sum(value*term/z**(power-o) for value,term,power in zip(c[o],terms,[4,4,5,5,5,5,6]))
def direct(c,o,a,b,r):
    @lru_cache(None)
    def co(order,i,aa,bb):
        f=expr(c,order,i,aa,bb,r)
        if order:
            f+=sum(e(i,t)*expr(c,0,t,aa,bb,r)+e(aa,t)*expr(c,0,i,t,bb,r)+e(bb,t)*expr(c,0,i,aa,t,r) for t in range(4))
        return f
    @lru_cache(None)
    def div(order,aa,bb):
        f=sum(dx(co(order,i,aa,bb),i) for i in range(4))
        if order:
            f+=sum(gamma(i,i,t)*co(0,t,aa,bb)+gamma(aa,i,t)*co(0,i,t,bb)+gamma(bb,i,t)*co(0,i,aa,t) for i in range(4) for t in range(4))
        return f
    f=div(o,a,b)
    if o:f-=sum(e(a,t)*div(0,t,b)+e(b,t)*div(0,a,t) for t in range(4))
    return at(f)
samples=[(1,1,0),(0,1,1),(0,0,0)]
for oactive in (0,1):
    for basis in range(7):
        c=[[s.Integer(0) for _ in range(7)] for _ in range(2)]
        c[oactive][basis]=1+2*L
        for o in (0,1):
            for a,b,r in samples:
                actual=direct(c,o,a,b,r);expect=candidate(c,o,a,b,r)
                assert s.expand(actual-expect)==0,(oactive,basis,o,a,b,r,actual,expect)
                checks.append((oactive,basis,o,a,b,r))
        print('basis',oactive,basis,'cpu',time.process_time()-cpu,flush=True)
# A radial test isolates the volume/connection correction. F^{i,ab}_r=x_i x_r delta_ab/z5.
c=[[s.Integer(0) for _ in range(7)] for _ in range(2)];c[0][2]=s.Integer(1)
correct=direct(c,1,1,1,0)
naive=s.Integer(0)
assert correct!=naive;negative.append(dict(name='omit_all_curved_frame_divergence_terms',residual=str(correct)))
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),negative_controls=negative,
 cpu_seconds=time.process_time()-cpu,status='FRAME_DIVERGENCE_RECONSTRUCTION_VERIFIED',
 full_Q2=False,scope='All seven O4 tensor structures, K0/K1, linear log coefficients, three separating components')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),source,D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
