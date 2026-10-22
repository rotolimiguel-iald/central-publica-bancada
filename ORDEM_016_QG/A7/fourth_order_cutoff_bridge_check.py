"""Actual polynomial covariant jets test the fourth-order cutoff completion."""
from pathlib import Path
from datetime import datetime, timezone
from functools import lru_cache
from itertools import permutations
from fractions import Fraction as F
import hashlib, json, time, uuid
import sympy as s
from curved_cutoff_descent_engine import polynomial_jet, splits
from spaceform_covariant_jet_engine import ZERO, mono, plus, times
from oneform_second_curvature_engine_v2 import loop_gauge

H = Path(__file__).resolve().parent
D = H / 'fourth_order_cutoff_bridge'
D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,obj):
    p=D/name;assert not p.exists(),p
    raw=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p)

inputs=[Path(__file__),H/'curved_cutoff_descent_engine.py',
        H/'spaceform_covariant_jet_engine.py',H/'oneform_second_curvature_engine_v2.py',
        H/'bilocal_curved_contact_primitive/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Fourth-order ordered cutoff commutator in the actual covariant polynomial recursion',
    method='Differentiate chi*h directly, independently compare all nonempty ordered subsets of covariant derivative words',
    curvature_orders=[0,1],parameters='b,c,t symbolic; no selection',
    negative_controls=['omit commutator','double half commutator'],
    sources=[dict(path=str(p),sha256=sha(p)) for p in inputs],full_Q2=False))
cpu=time.process_time();checks=[];negative=[]
b,c,t=s.symbols('b c t',real=True)
families=json.loads((H/'bilocal_curved_contact_primitive/results.json').read_bytes())['families']

def hi(indices,order):
    if order:return {}
    a,d=sorted(indices)
    return plus({ZERO:F(a+d+1)},mono((a,),a+1),mono((a,d),2),
                mono((a,(d+1)%4,(a+2)%4),-3),mono((a,a,d,d),1))

chi0=plus({ZERO:F(2)},mono((0,),3),mono((1,2),-2),
          mono((0,1,3),1),mono((2,2,3,3),4),mono((0,0,0,0),-1))
def ci(indices,order):return {} if order else chi0
h=polynomial_jet(hi,2)
chi=polynomial_jet(ci,0)
direct=polynomial_jet(lambda ix,o:times(chi0,hi(ix,o)),2)

@lru_cache(None)
def ordered_comm(word,indices,order):
    return sum((chi(u,(),k)*h(v,indices,order-k)
       for u,v in splits(word) if u for k in range(order+1)),F())

def symmetrize(jet):
    @lru_cache(None)
    def out(word,a,d,order):
        words=set(permutations(word))
        return sum((jet(w,(a,d),order) for w in words),F())/len(words)
    return out

sh,sd,sc=map(symmetrize,[h,direct,ordered_comm])
def ck(name,expr):
    assert s.expand(expr)==0,(name,expr)
    checks.append(name)

for mode in ('geodesic','coordinate'):
    flat=[s.sympify(v,locals={'b':b,'c':c,'t':t}) for v in families[mode]['flat']]
    first=[s.sympify(v,locals={'b':b,'c':c,'t':t}) for v in families[mode]['first']]
    for order in (0,1):
        nh=s.Matrix(loop_gauge(sh,flat,first,[F(),F()],order))
        nproduct=s.Matrix(loop_gauge(sd,flat,first,[F(),F()],order))
        comm=s.Matrix(loop_gauge(sc,flat,first,[F(),F()],order))
        for a in range(4):
            for d in range(4):
                ck(('ordered_comm',mode,order,a,d),nproduct[a,d]-2*nh[a,d]-comm[a,d])
                # First variation of 1/2 <chi*h, N*h> has two terms.
                varied=(2*nh[a,d]+nproduct[a,d])/2
                ck(('half',mode,order,a,d),varied-2*nh[a,d]-comm[a,d]/2)
        val=s.expand(comm[0,1])
        assert val!=0
        negative.append(dict(mode=mode,order=order,omitted_commutator=str(val/2),
                             doubled_half_error=str(val/2)))
        print('CUTOFF',mode,order,'cpu',time.process_time()-cpu,flush=True)

# Fiber-transpose identities of the parallel coefficient tensors, checked as
# polynomials in all derivative momenta. Symmetric monomial coefficients are
# unique, so this covers each completely symmetric derivative coefficient.
p=s.Matrix(s.symbols('p0:4'));p2=p.dot(p)
basis=[]
for a in range(4):
    for d in range(a,4):
        z=s.zeros(4);z[a,d]=1;z[d,a]=1;basis.append(z)
def inner(a,d):return s.trace(a*d)
def symbol(coeffs,v,order):
    if order==0:
        a1,a2,a3,a4,a5=coeffs
        return (a1*p2**2*v+a2*p2**2*s.trace(v)*s.eye(4)
          +a3*p2*(p*p.T*s.trace(v)+s.eye(4)*(p.T*v*p)[0])
          +a4*p2*(p*(v*p).T+(v*p)*p.T)/2
          +a5*p*p.T*(p.T*v*p)[0])
    a1,a2,a3,_,a4=coeffs
    return -(a1*p2*v+a2*p2*s.trace(v)*s.eye(4)
       +a3*(p*p.T*s.trace(v)+s.eye(4)*(p.T*v*p)[0])
       +a4*(p*(v*p).T+(v*p)*p.T)/2)
for mode in ('geodesic','coordinate'):
    for order,key in [(0,'flat'),(1,'first')]:
        coeffs=[s.sympify(v,locals={'b':b,'c':c,'t':t}) for v in families[mode][key]]
        images=[symbol(coeffs,v,order) for v in basis]
        for i,v in enumerate(basis):
            for j,w in enumerate(basis):
                ck(('fiber_transpose',mode,order,i,j),inner(v,images[j])-inner(images[i],w))

result=dict(at=datetime.now(timezone.utc).isoformat(),
    status='FOURTH_ORDER_COVARIANT_CUTOFF_AND_COEFFICIENT_ADJOINT_CHECKED',
    checks=len(checks),cpu_seconds=time.process_time()-cpu,
    negative_controls=negative,parameters_selected=False,
    identity='M_chi=chi*N+[N,chi]/2=(chi*N+N*chi)/2',
    degree='Actual fourth-order and first-curvature second-order covariant derivatives',
    scope='Finite covariant polynomial checks plus complete symbolic parallel-coefficient transpose; not a quantum diagram computation',
    full_Q2=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p))
    for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
