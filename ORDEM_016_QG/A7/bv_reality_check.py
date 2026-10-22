"""A consistent graded reality extension for the actual BV convention069."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'bv_reality';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,o):
    assert not p.exists();b=json.dumps(o,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    bv_dictionary_sha256=sha(HERE.parents[1]/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md'),
    target='Extend h*=h,c*=c,barc*=-barc,b*=b to antifields with opposite reality sign; verify(sF)*=(-1)^|F|s(F*)',
    scope='Algebraic reality of local generators/counterterms; no claim full causal normalization'))
start,cpu=perf_counter(),process_time()
h,b,cs,bars,E0,E1,dE0,dE1,kap,H,C,K,Q,ell=s.symbols('h b c_af barc_af E0 E1 dE0 dE1 kappa H C K Q ell',real=True)
# Odd variables: c,barc,h_af,b_af,dc,u0,u1,du0,du1.
eps=[1,-1,-1,-1,1,-1,-1,-1,-1]
def clean(a):return {k:s.expand(v) for k,v in a.items() if s.expand(v)!=0}
def plus(*items):
    out={}
    for item in items:
        for k,v in item.items():out[k]=out.get(k,0)+v
    return clean(out)
def scale(a,v):return clean({k:c*v for k,c in a.items()})
def atom(i):return {(i,):s.S.One}
def even(x):return {():x} if x!=0 else {}
def mul(a,b):
    out={}
    for x,c in a.items():
        for y,d in b.items():
            t=x+y
            if len(set(t))!=len(t):continue
            sign=(-1)**sum(t[i]>t[j] for i in range(len(t)) for j in range(i+1,len(t)))
            k=tuple(sorted(t));out[k]=out.get(k,0)+sign*c*d
    return clean(out)
def star(a,wrong_haf=False):
    out={};local=list(eps)
    if wrong_haf:local[2]=1
    for mon,coef in a.items():
        v=s.conjugate(coef).subs({cs:-cs},simultaneous=True)
        sign=(-1)**(len(mon)*(len(mon)-1)//2)
        for i in mon:sign*=local[i]
        out[mon]=v*sign
    return clean(out)
checks=[];neg=[]
# Values of s0 on generators in the shifted-antifield convention.
variables=[('h',0,1,scale(atom(0),K)),('b',0,1,{}),('c',1,1,{}),
 ('barc',1,-1,even(-b)),('h_af',1,-1,even(H*h+C*b)),
 ('b_af',1,-1,even(C*h-ell*b-bars)),('c_af',0,-1,plus(scale(atom(1),-Q),scale(atom(2),-K))),
 ('barc_af',0,1,scale(atom(0),Q))]
for name,parity,reality,value in variables:
    assert star(value)==scale(value,(-1)**parity*reality),name;checks.append('s0_reality_'+name)
nonlinear_sc=mul(atom(0),atom(4));assert star(nonlinear_sc)==scale(nonlinear_sc,-1);checks.append('nonlinear_sc_reality')
ghost_action=mul(atom(1),atom(0));metric_af_action=mul(atom(2),atom(0));ghost_af_action=scale(nonlinear_sc,cs)
for name,a in [('ghost',ghost_action),('h_af',metric_af_action),('c_af',ghost_af_action),('barc_af',even(-bars*b))]:
    assert star(a)==a;checks.append('action_real_'+name)
assert star(metric_af_action,wrong_haf=True)!=metric_af_action;neg.append('incorrect_real_metric_antifield')
F_B=scale(plus(mul(mul(atom(5),atom(0)),atom(8)),mul(mul(atom(6),atom(0)),atom(7))),s.Rational(1,2))
F_D=scale(plus(mul(mul(atom(5),atom(4)),atom(6)),scale(mul(mul(atom(6),atom(4)),atom(5)),-1)),s.Rational(1,2))
F_A=scale(atom(2),h*h);F_Z=scale(atom(0),cs*h)
for name,F in [('B',F_B),('D1',F_D),('A2',F_A),('Z',F_Z)]:
    assert star(F)==scale(F,-1);checks.append('generator_antireal_'+name)
# Differential restricted to u_i,du_i with delta u_i=E_i.
vals={5:E0,6:E1,7:dE0,8:dE1}
def delta(a):
    out={}
    for mon,coef in a.items():
        for n,i in enumerate(mon):
            if i in vals:out=plus(out,{mon[:n]+mon[n+1:]:coef*(-1)**n*vals[i]})
    return out
for name,F in [('B',F_B),('D1',F_D)]:
    dF=delta(F);assert dF and star(dF)==dF;checks.append('counterterm_real_'+name)
    assert star(scale(F,s.I))==scale(F,s.I)
    assert star(scale(dF,s.I))!=scale(dF,s.I);neg.append('extra_i_makes_counterterm_nonreal_'+name)
shift=scale(plus(atom(2),scale(atom(1),C)),4*kap)
assert star(shift)==scale(shift,-1);checks.append('shifted_antifield_antireal_real_kappa')
result=dict(statute='DERIVED_BV_REALITY_EXTENSION_AND_REAL_COUNTERTERMS',
    checks=checks,negative_controls=neg,
    convention='Field phi*=epsilon_phi phi;antifield(phi_af)*=-epsilon_phi phi_af;star reverses products and is antilinear',
    identity='(sF)*=(-1)^parity(F) s(F*);odd antireal F gives real sF',
    candidate_scope='The displayed real-coefficient A2,Z,B,D1 generator monomials; no new factor i in position space',
    limitations=['Full nonlinear completed generator not constructed','Causal normalization hierarchy unproved','Fourier i must be restored with the existing conventions'],
    full_Q2=False,gate_changed=False,cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',result);print(json.dumps(result,ensure_ascii=False))
