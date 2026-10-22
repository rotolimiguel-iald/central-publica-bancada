"""Signed antifield coordinates versus the canonical right/left BV bracket."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement
import ast,hashlib,json,time,uuid
import sympy as s
H=Path(__file__).resolve().parent;D=H/'bv_antifield_coordinate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):
    assert not p.exists(),p
    b=json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
def main():
    D.mkdir(exist_ok=False);src=H/'antifield_quadratic_primitive_check.py'
    put(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
        target='Coordinate equivalence fdag_A=(-1)^eps_A bdag_A, not an extra theorem or renormalization',
        primary='Frob arXiv1803.10235v3 eq98 and eq104 read at turn273/274, 2026-09-25',
        sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),src]],
        finite_model='One gauge component with H0=0,C=K=Q=1; scalar tests do not prove spacetime Ward',
        exclusions=['No redefinition of qhat','No alteration of parametrix','No Q2 conclusion']))
    start=time.process_time();names={'clean','add','scale','mul','atom'}
    nodes=[n for n in ast.parse(src.read_text('utf-8')).body if isinstance(n,ast.FunctionDef) and n.name in names]
    ns={'s':s};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),ns)
    clean,add,scale,mul,atom=[ns[n] for n in ['clean','add','scale','mul','atom']]
    even=lambda v:clean({():v})
    h,b,cs,bars,ell,w=s.symbols('h b cdag barcdag ell w')
    evens=[h,b,cs,bars];c,barc,hs,bs,dc=[atom(i) for i in range(5)]
    fields=[even(h),even(b),c,barc];anti=[hs,bs,even(cs),even(bars)]
    # Variable coordinates (even symbol, odd index); negative index means even.
    fv=[(h,-1),(b,-1),(None,0),(None,1)]
    av=[(None,2),(None,3),(cs,-1),(bars,-1)]
    def deriv(a,var,right=False):
        symbol,i=var
        if i<0:return clean({mon:s.diff(v,symbol) for mon,v in a.items()})
        out={}
        for mon,v in a.items():
            if i in mon:
                k=mon.index(i);key=mon[:k]+mon[k+1:]
                sign=(-1)**k
                if right:sign*=(-1)**(len(mon)+1)
                out[key]=out.get(key,0)+sign*v
        return clean(out)
    def bracket(F,G,signed):
        out={}
        for i,(v,a) in enumerate(zip(fv,av)):
            eps=1 if not signed or i<2 else -1
            term=add(mul(deriv(F,v,True),deriv(G,a)),scale(mul(deriv(F,a,True),deriv(G,v)),-1))
            out=add(out,scale(term,eps))
        return out
    def T(F):return clean({m:v.subs({cs:-cs,bars:-bars},simultaneous=True) for m,v in F.items()})
    SB=add(even(b*h-ell*b*b/2-bars*b),mul(barc,c),mul(hs,c))
    SF=T(SB);qB=lambda F:bracket(SB,F,True);qF=lambda F:bracket(SF,F,False)
    checks=[]
    def eq(name,A,B=None):
        assert not add(A,scale(B or {},-1)),(name,A,B);checks.append(name)
    expected=[c,{}, {},even(-b),even(b),even(h-ell*b-bars),add(scale(barc,-1),scale(hs,-1)),c]
    generators=fields+anti
    for i,(g,target) in enumerate(zip(generators,expected)):
        eq('B generator '+str(i),qB(g),target)
        eq('nilpotent B generator '+str(i),qB(qB(g)))
        eq('coordinate differential intertwiner '+str(i),qF(T(g)),T(qB(g)))
    eq('CME B',bracket(SB,SB,True));eq('CME F',bracket(SF,SF,False))
    mons=[]
    for degree in (1,2,3):
        for inds in combinations_with_replacement(range(8),degree):
            z=even(1)
            for i in inds:z=mul(z,generators[i])
            if z:mons.append(z)
    for i,z in enumerate(mons):
        eq('polynomial intertwiner '+str(i),qF(T(z)),T(qB(z)))
        # A generator basis suffices to detect a mismatch of biderivations.
        for k,g in enumerate(generators):eq('bracket pullback '+str((i,k)),T(bracket(z,g,True)),bracket(T(z),T(g),False))
    def CW(F):return scale(deriv(deriv(F,(None,0)),(None,1)),w)
    Faf=mul(mul(even(cs),c),dc)
    RB=add(qB(CW(Faf)),scale(CW(qB(Faf)),-1))
    RF=add(qF(CW(T(Faf))),scale(CW(qF(T(Faf))),-1))
    eq('ghost Wick correction coordinate invariant',RF,T(RB))
    eq('ghost Wick correction sign',RB,scale(dc,-w))
    eq('W=G-H Euler slot flips the W sign',clean({m:v.subs(w,-s.Symbol('d')) for m,v in RB.items()}),scale(dc,s.Symbol('d')))
    # A genuine odd-sign negative control: q1 Lie_c h, one-dimensional jet algebra.
    h0,h1,h2=s.symbols('h0 h1 h2');c0,c1,c2=atom(0),atom(1),atom(2)
    qh0=add(scale(c0,h1),scale(c1,2*h0))
    qh1=add(scale(c0,h2),scale(c1,3*h1),scale(c2,2*h0))
    def q1(F,ghost_sign):
        out=add(mul(qh0,deriv(F,(h0,-1))),mul(qh1,deriv(F,(h1,-1))))
        for k,target in enumerate([mul(c0,c1),mul(c0,c2)]):
            out=add(out,scale(mul(target,deriv(F,(None,k))),ghost_sign))
        return out
    eq('nonlinear Lie nilpotency with positive sc',q1(qh0,1))
    wrong=q1(qh0,-1)
    eq('wrong ghost sign residual',wrong,add(scale(mul(c0,c1),-2*h1),scale(mul(c0,c2),-4*h0)))
    assert wrong;checks.append('flipping only ghost sign rejected')
    # Field Ward is algebraic for arbitrary hh and the mixed/ghost blocks of Hfull.
    hh,hq,kg=s.symbols('Hh HQ Kg')
    N=s.Matrix([[hh,kg*hq,0,0],[hq*kg,0,0,0],[0,0,0,hq],[0,0,-hq,0]])
    Q=s.Matrix([[0,0,kg,0],[0,0,0,0],[0,0,0,0],[0,-1,0,0]])
    assert Q*N+s.diag(1,1,-1,-1)*N*Q.T==s.zeros(4)
    checks.append('field Ward arbitrary hh and HQ with matched mixed blocks')
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        coordinate_change='fdag_A=(-1)^eps_A bdag_A',
        free_action_F='Sfree+hdagF Kg c+barcdagF b',
        interaction_F='int chi(hdagF Lie_c h-cdagF c.nabla c)',
        ghost_Euler_B='-Qbarc-Kg*hdagB',ghost_Euler_F='+Qbarc+Kg*hdagF',
        ghost_A1_coefficient_preserved=True,nonminimal_337_over_10_changed=False,
        normalization_changed=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result);put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
        [Path(__file__),src,D/'PRE_REGISTER.json',D/'results.json']],full_Q2=False))
    print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
