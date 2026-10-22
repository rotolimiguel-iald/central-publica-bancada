"""C6: rank-two pair Euler contact at first curvature, using existing partial prescription.

All tensor indices covariant. No vertices, Ward amplitude or quantum class is inferred.
The second line is a spectator to the Euler operator. Differentiate before anchoring.
"""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
from functools import lru_cache
import json,sys,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'A7';D=ROOT/'C6/tensor_zerojet'
sys.path.insert(0,str(H))
from bilocal_scalar_euler_zerojet import x,y,xx,yy,xy,zero,F,ONE,LG,pair_delta
from smooth_line_compatibility_check_v2 import multiply
import bilocal_first_curvature_engine as B
from deliver_nonminimal_wick_and_mimo_audit import OUT,sha,put,write,append

def delta(a,b):return s.Integer(a==b)
def gamma(coords,a,i,b):return -(delta(a,b)*coords[i]+delta(a,i)*coords[b]-2*delta(i,b)*coords[a])/3
def S(ind):
    a,b,c,d=ind
    return (delta(a,c)*delta(b,d)+delta(a,d)*delta(b,c)-delta(a,b)*delta(c,d))/2

@lru_cache(None)
def prop(order,ind):
    a,b,c,d=ind;ss=S(ind)
    if order==0:return ((ss,F),) if ss else ()
    t=(B.lower1[a,c]*delta(b,d)+delta(a,c)*B.lower1[b,d]+B.lower1[a,d]*delta(b,c)+delta(a,d)*B.lower1[b,c]
       -B.gX1[a,b]*delta(c,d)-delta(a,b)*B.gY1[c,d])/2
    terms=[(s.expand(t),F),(s.expand((xx*yy-xy**2)*ss/3),(2,0)),(ss/4,ONE),(delta(a,b)*delta(c,d)/2,LG)]
    return tuple((a,b) for a,b in terms if a!=0)

@lru_cache(None)
def raw(order,ind):
    z=sum((x[i]-y[i])**2 for i in range(4))
    return sum(coef*z**(-n)*s.log(z)**ell for coef,(n,ell) in prop(order,ind))

PD=lru_cache(None)(pair_delta)
U=((s.S.One,F),)

def potential_lines(ind,side):
    a,b,c,d=ind
    yield -2,ind
    g=delta(a,b) if side==0 else delta(c,d)
    if g:
        for r in range(4):yield 2*g,((r,r,c,d) if side==0 else (a,b,r,r))

def connection_lines(ind,side,i):
    coords=x if side==0 else y
    for pos in ((0,1) if side==0 else (2,3)):
        a=ind[pos]
        for r in range(4):
            g=-gamma(coords,r,i,a)
            if g:yield g,ind[:pos]+(r,)+ind[pos+1:]

@lru_cache(None)
def first_coefficient(ind,side):
    A0,A1=prop(0,ind),prop(1,ind);coords=x if side==0 else y;rad=sum(t*t for t in coords)
    val=sum(PD(A1,((side,i),(side,i)),U,()) for i in range(4))
    for i,j in product(range(4),repeat=2):
        coef=((rad*delta(i,j)-coords[i]*coords[j])/3).subs(zero)
        if coef:val+=multiply(coef,PD(A0,((side,i),(side,j)),U,()))
    for i in range(4):
        val+=multiply((-2*coords[i]).subs(zero),PD(A0,((side,i),),U,()))
        for g,replaced in connection_lines(ind,side,i):
            A=prop(0,replaced)
            val+=multiply((2*g).subs(zero),PD(A,((side,i),),U,()))
            val+=multiply(s.diff(g,coords[i]).subs(zero),PD(A,(),U,()))
    for coef,replaced in potential_lines(ind,side):val+=coef*PD(prop(0,replaced),(),U,())
    val+=multiply((-rad/2).subs(zero),sum(PD(A0,((side,i),(side,i)),U,()) for i in range(4)))
    return s.expand(val)

@lru_cache(None)
def second_coefficient(ind,side):
    return s.expand(sum(PD(U,((side,i),(side,i)),prop(1,ind),()) for i in range(4)))

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc);t0=time.process_time()
    sources=[Path(__file__),H/'bilocal_first_curvature_engine.py',H/'bilocal_covariant_jet_engine.py',
             H/'bilocal_scalar_euler_zerojet.py',H/'balanced_log_pair_engine.py',H/'smooth_line_compatibility_check_v2.py']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),operator='sqrt(g)[roughBox-2K Id+2K g tr] on first metric line, all four tensor slots covariant',
        reduction='Bilinearity gives pair(i,j)=S(j)*first(i)+S(i)*second(j); no coefficient fitting',
        expected_value=None,sources=[dict(path=str(p),sha256=sha(p)) for p in sources],full_Q2=False))
    inds=[(a,b,c,d) for a in range(4) for b in range(a,4) for c in range(4) for d in range(c,4)]
    checks=[]
    def eq(name,value):
        assert s.cancel(value)==0,(name,s.cancel(value));checks.append(name)
    # All independent components of the two endpoint equations outside the diagonal.
    for k,ind in enumerate(inds):
        for side in (0,1):
            coords=x if side==0 else y;rad=sum(t*t for t in coords);f0=raw(0,ind);f1=raw(1,ind)
            val=sum(s.diff(f1,t,2) for t in coords)
            val+=sum((rad*delta(i,j)-coords[i]*coords[j])/3*s.diff(f0,coords[i],coords[j]) for i,j in product(range(4),repeat=2))
            val-=2*sum(coords[i]*s.diff(f0,coords[i]) for i in range(4))
            for i in range(4):
                for g,replaced in connection_lines(ind,side,i):
                    val+=2*g*s.diff(raw(0,replaced),coords[i])+s.diff(g,coords[i])*raw(0,replaced)
            val+=sum(coef*raw(0,replaced) for coef,replaced in potential_lines(ind,side))
            eq('parametrix_'+str((side,ind)),val.subs(zero))
        if k%10==0:print(json.dumps(dict(stage='parametrix',completed=k+1,cpu=time.process_time()-t0)),flush=True)
    coeff={}
    for k,ind in enumerate(inds):
        coeff[ind]=[(first_coefficient(ind,side),second_coefficient(ind,side)) for side in (0,1)]
        if k%10==0:print(json.dumps(dict(stage='contacts',completed=k+1,cpu=time.process_time()-t0)),flush=True)
    table=[];differences=[]
    for i,j in product(inds,repeat=2):
        vals=[s.expand(S(j)*coeff[i][side][0]+S(i)*coeff[j][side][1]) for side in (0,1)]
        assert all(not v.free_symbols for v in vals),(i,j,vals)
        if vals[0]!=vals[1]:differences.append(dict(first=i,second=j,values=list(map(str,vals))))
        if any(vals):table.append(dict(first=i,second=j,values=list(map(str,vals))))
    put(D/'COEFFICIENTS.json',{str(i):[[str(a),str(b)] for a,b in row] for i,row in coeff.items()})
    put(D/'TABLE_NONZERO.json',table)
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),independent_line_components=len(inds),pair_components=len(inds)**2,
        nonzero_pairs=len(table),endpoint_differences=len(differences),differences=differences,cpu_seconds=time.process_time()-t0,
        measured_jet='CE*K*delta only, no extra derivative slots',all_parametrix_equations_passed=True,
        prescription='same partial R_bal f/f f/log with smooth-line completion, no new adjustment',
        loop_anomaly=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result)
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'COEFFICIENTS.json',D/'TABLE_NONZERO.json',D/'results.json']]))
    print(json.dumps({k:v for k,v in result.items() if k!='differences'}),flush=True)
if __name__=='__main__':main()
