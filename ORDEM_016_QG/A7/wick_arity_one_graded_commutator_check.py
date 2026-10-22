"""Check the arity-one Wick commutator with the existing graded algebra.

Only pure polynomial helpers are loaded from the previous checked script.
No import of that script: its top-level code writes a pre-existing artifact.
"""
from pathlib import Path
from datetime import datetime, timezone
from itertools import combinations_with_replacement
import ast, hashlib, json, time, uuid
import sympy as s

H=Path(__file__).resolve().parent
D=H/'wick_arity_one_graded_commutator'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):
    assert not p.exists(),p
    data=json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8')
    temp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    temp.write_bytes(data);assert temp.read_bytes()==data;temp.replace(p)

def main():
    D.mkdir(exist_ok=False)
    source=H/'antifield_quadratic_primitive_check.py'
    put(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
        target='[q,C_W] for a nilpotent linear free BV differential, including antifield-Euler slots',
        conventions='Left odd derivatives; C_W contracts fields only, C_W(c*barc)=wG; h1 equation m*h1',
        sources=[dict(path=str(p),sha256=sha(p)) for p in
            [Path(__file__),source,H/'shifted_antifield_check.py']],
        model='Finite coefficient/Grassmann control of formula; not a spacetime covariance or T1 construction',
        conditional_dictionary='With a fixed equivariant G representation and T1H=N_G exp(i*hbar*C_(G-H)), A1=i*hbar*[q,C_(G-H)]',
        scope='No numerical curved A1 or Q2; no choice of W; no canonical change'))
    start=time.process_time()
    names={'clean','add','scale','mul','atom'}
    nodes=[n for n in ast.parse(source.read_text('utf-8')).body
           if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes}==names
    ns={'s':s};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),ns)
    clean,add,scale,mul,atom=[ns[n] for n in ['clean','add','scale','mul','atom']]
    def even(v): return clean({():v})
    h0,h1,b,cs,bars,m,ell,t=s.symbols('h0 h1 b c_af barc_af m ell t')
    evens=[h0,h1,b,cs,bars]
    # Odd order c,barc,hstar0,hstar1,bstar.
    odds=[atom(i) for i in range(5)]
    c,barc,hs0,hs1,bs=odds
    fields=[even(v) for v in evens]+odds
    parity=[0]*5+[1]*5
    qeven=[c,{}, {}, add(scale(barc,-1),scale(hs0,-1)),c]
    qodd=[{},even(-b),even(b),even(m*h1),even(h0-ell*b-bars)]
    def de(a,v): return clean({k:s.diff(z,v) for k,z in a.items()})
    def do(a,i):
        out={}
        for mon,coef in a.items():
            if i in mon:
                j=mon.index(i);key=mon[:j]+mon[j+1:]
                out[key]=out.get(key,0)+(-1)**j*coef
        return clean(out)
    def q(a):
        out={}
        for v,qv in zip(evens,qeven):out=add(out,mul(qv,de(a,v)))
        for i,qv in enumerate(qodd):out=add(out,mul(qv,do(a,i)))
        return out
    w00,w01,w0b,w11,w1b,wbb,wg=s.symbols('w00 w01 w0b w11 w1b wbb wG')
    W=s.Matrix([[w00,w01,w0b],[w01,w11,w1b],[w0b,w1b,wbb]])
    def C(a):
        out={}
        for i in range(3):
            for j in range(3):out=add(out,scale(de(de(a,evens[j]),evens[i]),W[i,j]/2))
        return add(out,scale(do(do(a,0),1),wg))
    def R(a): return add(q(C(a)),scale(C(q(a)),-1))
    checks=[]
    def eq(name,a,expected=None):
        assert not add(a,scale(expected or {},-1)),(name,a,expected)
        checks.append(name)
    eq('odd contraction convention',C(mul(c,barc)),even(wg))
    eq('bosonic half convention',C(even(h1*h1)),even(w11))
    for i,f in enumerate(fields):eq('q squared generator '+str(i),q(q(f)))
    monomials=[]
    for degree in range(1,5):
        for inds in combinations_with_replacement(range(10),degree):
            if degree==4 and not (3 in inds or 8 in inds):continue
            a=even(1)
            for i in inds:a=mul(a,fields[i])
            if a:monomials.append((inds,a))
    for inds,a in monomials:
        eq('nilpotent '+str(inds),q(q(a)))
        eq('BCH terminates '+str(inds),add(C(R(a)),scale(R(C(a)),-1)))
        eq('linear WZ '+str(inds),add(q(R(a)),R(q(a))))
    F=mul(mul(hs1,even(h1)),c)
    eq('antifield vertex initial contraction vanishes',C(F))
    eq('Euler contraction survives',C(q(F)),scale(c,m*w11))
    eq('antifield commutator sign',R(F),scale(c,-m*w11))
    assert R(F)
    checks.append('zero initial contraction does not imply equivariance')
    def exponential(a,sign):
        out=a;term=a
        for n in range(1,5):
            term=C(term)
            if not term:break
            out=add(out,scale(term,(sign*t)**n/s.factorial(n)))
        return out
    # Direct finite exponential transport on a quartic containing an antifield.
    probe=mul(hs1,even(h1**3))
    actual=exponential(q(exponential(probe,1)),-1)
    eq('finite exponential identity',actual,add(q(probe),scale(R(probe),t)))
    assert add(actual,q(probe),scale(R(probe),-t))
    checks.append('wrong transport signs rejected')
    # A smooth shift S supported only in b-b does not commute with q; this
    # disproves treating every smooth covariance change as equivariant.
    witness=R(mul(barc,even(b)))
    eq('nonminimal smooth Ward witness',witness,even(wbb))
    def render(a):return [{'odd':list(k),'coefficient':str(v)} for k,v in a.items()]
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),
        tested_monomials=len(monomials),cpu_seconds=time.process_time()-start,
        witness_F='hstar1*h1*c',C_F=render(C(F)),C_qF=render(C(q(F))),
        commutator_F=render(R(F)),nonminimal_witness=render(witness),
        formula='exp(-t C_W) q exp(t C_W)=q+t[q,C_W]',
        state_transport='G->G+B leaves A1 unchanged only when [q,C_B]=0; not every smooth shift',
        physically_constructed_covariance=False,curved_A1_computed=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result)
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
        [Path(__file__),source,D/'PRE_REGISTER.json',D/'results.json']],full_Q2=False))
    print(json.dumps(result,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
