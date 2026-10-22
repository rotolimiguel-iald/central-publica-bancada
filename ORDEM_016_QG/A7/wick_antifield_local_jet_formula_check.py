"""Check the finite-jet antifield formula with explicit graded contractions."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,time,uuid
import sympy as s
H=Path(__file__).resolve().parent;D=H/'wick_antifield_local_jet_formula'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):
    assert not p.exists(),p
    b=json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
def main():
    D.mkdir(exist_ok=False)
    source=H/'antifield_quadratic_primitive_check.py'
    put(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
        target='Antifield-Euler part of A1(F_af) in terms of four coincidence arrays',
        basis='h_A independent symmetric coordinates; hdagger_A their dual coordinates',
        conventions='W=G-H, N_H=N_G exp(i*hbar C_W), fixed equivariant G representation',
        excluded='No full PH matrix, numerical curved A1, Lorentzian i0 or Q2',
        sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),source]]))
    start=time.process_time();names={'clean','add','scale','mul','atom'}
    ns={'s':s};nodes=[n for n in ast.parse(source.read_text('utf-8')).body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes}==names
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),ns)
    clean,add,scale,mul,atom=[ns[n] for n in ['clean','add','scale','mul','atom']]
    def even(v):return clean({():v})
    def do(a,i):
        out={}
        for mon,v in a.items():
            if i in mon:
                j=mon.index(i);key=mon[:j]+mon[j+1:]
                out[key]=out.get(key,0)+(-1)**j*v
        return clean(out)
    checks=[]
    def eq(name,a,b=None):
        assert not add(a,scale(b or {},-1)),(name,a,b)
        checks.append(name)
    # Ghost jet controls: independent generators c,barc,d_c.
    c,barc,dc=atom(0),atom(1),atom(2)
    cs,Q,w0,w1=s.symbols('c_af Q w0 w1')
    def Cg(a):return add(scale(do(do(a,0),1),w0),scale(do(do(a,2),1),w1))
    def qg(a):return mul(scale(barc,-Q),clean({mon:s.diff(v,cs) for mon,v in a.items()}))
    F=scale(mul(c,dc),cs)
    eq('C(c barc)',Cg(mul(c,barc)),even(w0))
    eq('C(dc barc)',Cg(mul(dc,barc)),even(w1))
    eq('source has no initial ghost contraction',Cg(F))
    eq('source differential nilpotent',qg(qg(F)))
    R=add(qg(Cg(F)),scale(Cg(qg(F)),-1))
    eq('ghost two endpoint signs',R,add(scale(dc,-Q*w0),scale(c,Q*w1)))
    assert add(R,scale(dc,Q*w0),scale(c,Q*w1))
    checks.append('wrong second ghost contraction sign rejected')
    assert add(R,scale(dc,Q*w0))
    checks.append('omitting derivative covariance rejected')
    # Metric control: u odd antifield, c/dc ghosts; q u=E even.
    h,dh,E,v0,v1,M=s.symbols('h dh E v0 v1 M')
    u=atom(3)
    def qm(a):return scale(do(a,3),E)
    def Cm(a):
        return clean({mon:v0*s.diff(v,E,h)+v1*s.diff(v,E,dh) for mon,v in a.items()})
    Fm=mul(u,add(scale(c,dh),scale(dc,M*h)))
    eq('metric initial contraction',Cm(Fm))
    Rm=add(qm(Cm(Fm)),scale(Cm(qm(Fm)),-1))
    eq('metric derivative and representation slots',Rm,add(scale(c,-v1),scale(dc,-M*v0)))
    assert Rm
    checks.append('metric PH cannot be discarded by initial normal ordering')
    # W=G-H and extended Ward defect of G vanishes: D_W=-D_H.
    jh0,jh1,jc0,jc1=s.symbols('Jh0 Jh1 Jc0 Jc1')
    converted=clean({mon:v.subs({v0:-jh0,v1:-jh1}) for mon,v in Rm.items()})
    converted=add(converted,clean({mon:v.subs({w0:-jc0/Q,w1:-jc1/Q}) for mon,v in R.items()}))
    eq('H parametrix sign conversion',converted,add(scale(c,jh1-jc1),scale(dc,M*jh0+jc0)))
    r=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        formula='A1(Faf)/(i*hbar)=int chi [c^k Jh1[k,A,A]+M_A^B(nabla c) Jh0[A,B]+Jc0[i,j] nabla_j c^i-Jc1[j,i,i] c^j]',
        definitions={'Jh0':'[D_H(hdagger_A,h_B)]','Jh1':'[nabla_y,k D_H(hdagger_A,h_B)]',
                     'Jc0':'[D_H(cdagger_i,c^j)]','Jc1':'[nabla_y,k D_H(cdagger_i,c^j)]'},
        D_H='Extended free Ward defect including antifield->Euler equation, no contractions with antifields themselves',
        metric_slot='M_A^B(nabla c) is the tensor representation part of Lie_c h; sum in dual independent coordinates',
        highest_covariance_derivative_order=3,actual_J_arrays_measured=False,
        full_nonminimal_parametrix_constructed=False,curved_A1_computed=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',r)
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
        [Path(__file__),source,D/'PRE_REGISTER.json',D/'results.json']],full_Q2=False))
    print(json.dumps(r,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
