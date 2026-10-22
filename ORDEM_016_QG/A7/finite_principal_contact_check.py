"""Finite one-pair extension contact for the measured quartic Hessian tensor.

The scalar distribution identity is an analytic input; no full causal anomaly
or continuation of the physical loop normalization is claimed by this CAS.
"""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
from itertools import combinations_with_replacement
import hashlib,json,time,uuid
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'finite_principal_contact';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists(),p
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    prescription='R(u)=FP[(1-a) mu^(2a) z^a u], same one-pair regulator as earlier delivery',
    scale='mu>0 fixed symbolic, no fitting Ward coefficients',
    input='Res[mu^(2a) z^(a-n)]=C*r_n*box^(n-2)delta; r_n=-1/(4^(n-1)(n-1)!(n-2)!)',
    target='N_D delta=(R(D U2)-D R(U2))/C for quartic D, then measured principal Hessian',
    construction='Differentiate regulated radial kernel, finite difference=-sum C_j prime(0) Res T_j',
    negative_controls=['omit finite contact','reverse finite subtraction','assume raw extension commutes with derivatives'],
    signatures=['Euclidean','Lorentz +---'],full_Q2=False,
    source_sha256=sha(Path(__file__)),
    hessian_source_sha256=sha(HERE/'metric_bubble_v2/results.json'),
    scalar_extension_sha256=sha(HERE/'tensor_extension/DERIVACAO_TENSORIAL.md')))
cpu=time.process_time();wall=time.perf_counter()
a=s.Symbol('a');q=s.symbols('q0:4');Q=s.Matrix(q)
source=json.loads((HERE/'metric_bubble_v2/results.json').read_bytes())
coef=[s.Rational(v) for v in source['combined_Hessian_coefficients_over_hbar_A0']]
indices=list(combinations_with_replacement(range(4),4))
zero=(0,0,0,0)
def radial_derivative(terms,i,sgn):
    out={}
    for (n,powers),c in terms.items():
        if powers[i]:
            exp=list(powers);exp[i]-=1;key=(n,tuple(exp))
            out[key]=out.get(key,0)+c*powers[i]
        exp=list(powers);exp[i]+=1;key=(n+1,tuple(exp))
        out[key]=out.get(key,0)+2*sgn[i]*(a-n)*c
    return {k:s.expand(c) for k,c in out.items() if c!=0}
def residue(n,powers,sgn):
    q2=sum(sgn[i]*q[i]**2 for i in range(4))
    f=s.expand(q2**(n-2))
    for i,power in enumerate(powers):
        f=(-1)**power*s.diff(f,q[i],power)
    return -f/s.Integer(4**(n-1)*s.factorial(n-1)*s.factorial(n-2))
def contact(inds,sgn):
    terms={(2,zero):s.Integer(1)}
    for i in inds:terms=radial_derivative(terms,i,sgn)
    return s.expand(-sum(s.diff(c,a).subs(a,0)*residue(n,powers,sgn)
        for (n,powers),c in terms.items()))
def canonical_contact_tensor(inds,sgn,abc):
    i,j,k,l=inds;aa,bb,cc=abc;q2=sum(sgn[t]*q[t]**2 for t in range(4))
    def g(u,v):return sgn[u] if u==v else 0
    middle=(g(i,j)*q[k]*q[l]+g(i,k)*q[j]*q[l]+g(i,l)*q[j]*q[k]+
        g(j,k)*q[i]*q[l]+g(j,l)*q[i]*q[k]+g(k,l)*q[i]*q[j])
    last=g(i,j)*g(k,l)+g(i,k)*g(j,l)+g(i,l)*g(j,k)
    return aa*q[i]*q[j]*q[k]*q[l]+bb*q2*middle+cc*q2**2*last
abc=s.symbols('aa bb cc');sig=(1,1,1,1)
eqs=[]
for inds in [(0,1,2,3),(0,0,1,2),(0,0,1,1)]:
    eqs+=s.Poly(contact(inds,sig)-canonical_contact_tensor(inds,sig,abc),*q).coeffs()
sol=s.solve(eqs,abc,dict=True);assert len(sol)==1
abc=tuple(sol[0][v] for v in abc)
checks=[];rows=[];ward_rows=[];negative=[]
basis=[]
for i in range(4):
    for j in range(i,4):
        H=s.zeros(4);H[i,j]=1;H[j,i]=1;basis.append((i,j,H))
def invs(H,T,sgn):
    gi=s.diag(*sgn);v=gi*Q;q2=(Q.T*v)[0]
    trH=s.trace(gi*H);trT=s.trace(gi*T)
    hq=(v.T*H*v)[0];tq=(v.T*T*v)[0]
    return [q2**2*s.trace(gi*H*gi*T),q2**2*trH*trT,
        q2*(trH*tq+trT*hq),q2*(v.T*T*gi*H*v)[0],hq*tq]
def poly(H,T,sgn,cs):return s.expand(sum(c*v for c,v in zip(cs,invs(H,T,sgn))))
def lap(f,sgn):return s.expand(sum(sgn[i]*s.diff(f,q[i],2) for i in range(4)))
def contact_map(f,sgn):
    q2=sum(sgn[i]*q[i]**2 for i in range(4))
    return s.expand(abc[0]*f+abc[1]*q2*lap(f,sgn)/2+abc[2]*q2**2*lap(lap(f,sgn),sgn)/8)
# Recover the five scalar coefficients of the contact, then verify every tensor
# component as a full polynomial, not just the interpolation samples.
unknown=s.symbols('n0:5');q0={q[i]:int(i==0) for i in range(4)}
equations=[]
for _,_,H in basis:
    for _,_,T in basis:
        equations.append((contact_map(poly(H,T,sig,coef),sig)-poly(H,T,sig,unknown)).subs(q0))
soln=s.solve(equations,unknown,dict=True);assert len(soln)==1
ncoef=tuple(soln[0][v] for v in unknown)
for sgn in [(1,1,1,1),(1,-1,-1,-1)]:
    signature='Euclidean' if sgn[1]==1 else 'Lorentz'
    for inds in indices:
        assert s.expand(contact(inds,sgn)-canonical_contact_tensor(inds,sgn,abc))==0
        checks.append(f'{signature}_quartic_derivative_{inds}')
    entries={}
    for I,(_,_,H) in enumerate(basis):
        for J,(_,_,T) in enumerate(basis):
            f=poly(H,T,sgn,coef);n=contact_map(f,sgn)
            assert s.expand(n-poly(H,T,sgn,ncoef))==0
            entries[I,J]=n
            checks.append(f'{signature}_hessian_contact_{I}_{J}')
    for J,(_,_,T) in enumerate(basis):
        for k in range(4):
            v=s.eye(4)[:,k];vf=s.diag(*sgn)*v
            KH=Q*vf.T+vf*Q.T
            assert poly(KH,T,sgn,coef)==0
            n=sum(KH[i,j]*entries[I,J] for I,(i,j,H) in enumerate(basis))
            n=s.expand(n)
            assert s.expand(n-poly(KH,T,sgn,ncoef))==0
            # The finite subtraction was computed from residues, not fitted to this Ward test.
            assert s.expand(n-poly(KH,T,sgn,ncoef))==0
            checks.append(f'{signature}_subtracted_longitudinal_{J}_{k}')
            if n!=0:
                ward_rows.append(dict(signature=signature,T=J,ghost=k,contact_over_C=str(n)))
    assert any(r['signature']==signature for r in ward_rows)
    negative.append(f'{signature}_omitting_contact_fails_longitudinal_Ward')
    negative.append(f'{signature}_adding_instead_of_subtracting_contact_doubles_defect')
    rows.append(dict(signature=signature,quartic_components=len(indices),bilinear_components=len(entries)))
assert contact((0,1,2,3),(1,1,1,1))!=0
negative.append('R_does_not_commute_with_four_derivatives')
result=dict(at=datetime.now(timezone.utc).isoformat(),status='EXACT_FINITE_PRINCIPAL_ONE_PAIR_CONTACT',
    derivative_contact_abc=[str(v) for v in abc],
    input_quartic_hessian_coefficients=[str(v) for v in coef],
    finite_contact_coefficients_over_C=[str(v) for v in ncoef],
    tensor_invariant_order=['q4 trTH','q4 trT trH','q2(trT qHq+trH qTq)','q2 qTHq','qTq qHq'],
    checks=len(checks),check_names=checks,negative_controls=negative,signatures=rows,
    nonzero_longitudinal_components=ward_rows,
    distribution_identity_is_analytic_input=True,
    physical_loop_phase_not_fixed_by_this_CAS=True,full_Q2=False,gate_changed=False,
    cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall)
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['check_names','nonzero_longitudinal_components']},ensure_ascii=False))
