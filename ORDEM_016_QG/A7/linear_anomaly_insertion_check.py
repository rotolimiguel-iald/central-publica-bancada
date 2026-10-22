"""Connected linear insertions required by the two-entry anomalous Ward identity."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,time,uuid
import sympy as s
H=Path(__file__).resolve().parent;D=H/'linear_anomaly_insertion'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):
    assert not p.exists(),p
    b=json.dumps(x,ensure_ascii=False,indent=2).encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
def main():
    D.mkdir(exist_ok=False);src=H/'antifield_quadratic_primitive_check.py'
    put(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
        target='Both A1 insertion terms of connected A2, after the measured A1 has a linear ghost representative',
        assumption='Perturbative agreement in the linear slot, Frob eq158a/b; not inferred from radial extension of two-line loops',
        conventions='Tc2=(i/hbar)(T2-S2), GD=(Gret+Gadv)/2, G_barc,c=-GQ, right derivative Vghost/barc=-chi C Lie_c h',
        source_url='https://arxiv.org/pdf/1803.10235v3',source_equations=['34-35','158a-b'],
        sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),src,
            H/'flat_wick_dictionary_delivery_v2/ADENDO.md',H/'nonminimal_wick_heat_ward/results.json']],
        exclusions=['No unannounced selection of linear-slot normalization','No full nonlocal cancellation','No Q2 completed']))
    start=time.process_time();checks=[]
    def eq(name,a,b=0):assert s.cancel(a-b)==0,(name,a,b);checks.append(name)
    ih,adv,ret,star_left,star_right,T=s.symbols('ih GA GR left right T')
    # T2(V,phi)=left+ih GA; T2(phi,V)=right+ih GR, V even.
    left=T-ih*adv;right=T-ih*ret
    connected=(T-(left+right)/2)*(-1/ih) # i/hbar=-1/(i*hbar)
    eq('connected linear slot is minus Dirac Green',connected,-(adv+ret)/2)
    # Graded right derivative and propagator signs are checked separately.
    names={'clean','add','scale','mul','atom'}
    ns={'s':s};nodes=[n for n in ast.parse(src.read_text('utf-8')).body if isinstance(n,ast.FunctionDef) and n.name in names]
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),ns)
    clean,add,scale,mul,atom=[ns[n] for n in ['clean','add','scale','mul','atom']]
    bar,c=atom(0),atom(1);chi,h=s.symbols('chi h')
    v=scale(mul(bar,c),chi*h)
    def right_odd(a,index):
        out={}
        for mon,value in a.items():
            if index in mon:
                k=mon.index(index);key=mon[:k]+mon[k+1:]
                out[key]=out.get(key,0)+(-1)**(len(mon)-1-k)*value
        return clean(out)
    assert right_odd(v,0)==scale(c,-chi*h)
    checks.append('right antighost derivative has minus sign')
    G,J,alpha,dx,dy=s.symbols('G J alpha dchi deta')
    tree=-(-G)*(-J)
    eq('ghost propagator plus right derivative leaves minus tree',tree,-G*J)
    inserted=(-ih*alpha*dx)*tree
    eq('A1 linear insertion sign',inserted,ih*alpha*dx*G*J)
    eq('two equal A1 slots',-inserted-inserted,-2*ih*alpha*dx*G*J)
    assert -inserted!=-2*inserted
    checks.append('one missing A1 slot rejected')
    # Unequal cutoffs must retain their two different kernels and coefficients.
    Gxy,Gyx,Jchi,Jeta=s.symbols('Gxy Gyx Jchi Jeta')
    polarized=-ih*alpha*(dx*Gxy*Jeta+dy*Gyx*Jchi)
    swapped=polarized.subs({dx:dy,dy:dx,Gxy:Gyx,Gyx:Gxy,Jchi:Jeta,Jeta:Jchi},simultaneous=True)
    eq('polarized cutoff exchange',polarized,swapped)
    # Controlled constant-coefficient probe: tests nonlocality of an individual
    # inverse-operator term, NOT the curved propagator or physical value of alpha.
    lam,a,b,m2=s.symbols('lambda a b m2')
    source=(a+b)*(a+2*b)/2 # C0 Lie_c h00, momenta along 0 only.
    numerator=s.expand(lam*source.subs({a:0,b:-2*lam}))
    eq('one-component external source',numerator,4*lam**3)
    quotient,remainder=s.div(numerator,lam**2+m2,lam)
    eq('rational pole remainder',remainder,-4*m2*lam)
    assert remainder!=0;checks.append('individual insertion is not a polynomial contact')
    eq('constant cutoff removes its linear anomaly insertion',inserted.subs(dx,0))
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        general_linear_slot='Tc2(V,phiK(x))=-int GD_LK(y,x) T1(dR V/dphiL(y))dy',
        ghost_linear_slot='Tc2(Vchi,c_i(x))=-int GQ_D,ji(y,x) chi(y)*(C Lie_c h)^j(y)dy',
        alpha_definition='A1(Vchi)=i*hbar*alpha*int chi div(c); alpha includes the still explicit physical covariance normalization',
        both_insertions='-i*hbar*alpha*[int dchi(x) GQ_D(y,x) eta(y) C Lie_c h(y) + int deta(x) GQ_D(y,x) chi(y) C Lie_c h(y)]',
        equal_cutoffs='-2*i*hbar*alpha*int dchi(x) GQ_D(y,x) chi(y) C Lie_c h(y)',
        interaction_channel='Only Vghost contributes to contraction with a single c; metric and antifield vertices have no barc',
        normalization_obligation='Verify linear-slot perturbative agreement for the same T2 before numerical identification with the previous pair extension',
        negative_probe='Nonzero remainder -4*m2*lambda in a constant-coefficient test; no curved numerical amplitude inferred',
        full_nonlocal_cancellation=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result);put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
        [Path(__file__),D/'PRE_REGISTER.json',D/'results.json',src]],full_Q2=False))
    print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
