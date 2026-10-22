"""Derive local Wick multiplicities before using any measured loop residual."""
from pathlib import Path
from datetime import datetime,timezone
import sympy as s
import json,hashlib,time,uuid
H=Path(__file__).resolve().parent;D=H/'wick_current_weights';D.mkdir(exist_ok=False)
def put(n,v):
    p=D/n;assert not p.exists();raw=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),script_sha256=sha(Path(__file__)),
    input='Independent symbolic vertices/covariances, no measured loop values',
    convention='Formal Euclidean expansion exp(-V/hbar), connected coefficient and mean of odd current',
    target='Factors -1/2 metric pair, +1 ghost pair; current insertion factors from Wick; source sign',
    scope='Combinatorics under specified density/derivative conventions, not complete BRST Ward proof'))
start=time.process_time();checks=0
def eq(a,b):
    global checks
    assert s.expand(a-b)==0,(a,b);checks+=1
x=s.Matrix(s.symbols('x0:2'));y=s.Matrix(s.symbols('y0:2'))
a0,a1,a2,b0,b1,b2=s.symbols('a0 a1 a2 b0 b1 b2')
A=s.Matrix([[a0,a1],[a1,a2]]);B=s.Matrix([[b0,b1],[b1,b2]])
G=s.Matrix(2,2,s.symbols('g0:4'));v=s.Matrix(s.symbols('v0:2'));mix=s.Matrix(s.symbols('m0:2'))
VX=(x.T*A*x)[0]/2;VY=(y.T*B*y)[0]/2
def gamma(poly):return sum(G[i,j]*s.diff(poly,x[i],y[j]) for i in range(2) for j in range(2))
metric=s.expand(gamma(gamma(VX*VY))/2);trace=s.trace(A*G*B*G.T)
eq(metric,trace/2);eq(-metric,-trace/2)
# Cross order in -1/2 <(VX+VY)^2> is -<VX VY>. No extra factor2 remains.
dummy=s.symbols('by')
def gamma_mixed(poly):return gamma(poly)+sum(mix[i]*s.diff(poly,x[i],dummy) for i in range(2))
mixed=s.expand(gamma_mixed(gamma_mixed(VX*dummy*(v.T*y)[0]))/2)
eq(mixed,(mix.T*A*G*v)[0])
assert s.expand(mixed)!=0;checks+=1
# Exterior algebra: left derivatives, covariance entries for i<j, Gamma=sum Gij*dj*di.
def derivative(poly,i):
    out={}
    for w,c in poly.items():
        if i in w:
            n=w.index(i);key=w[:n]+w[n+1:];out[key]=out.get(key,0)+(-1)**n*c
    return out
def odd_gamma(poly,entries):
    out={}
    for (i,j),g in entries.items():
        for w,c in derivative(derivative(poly,i),j).items():out[w]=out.get(w,0)+g*c
    return out
u,w=s.symbols('u w');entries={(0,3):-u,(1,2):w}
# barX cX barY cY: closed ghost pairing -uw, hence effective-action cross +uw.
ghost=odd_gamma(odd_gamma({(0,1,2,3):s.Integer(1)},entries),entries)[()]/2
eq(ghost,-u*w);eq(-ghost,u*w)
# hstar at left, cX,barY,cY: only cX-barY contracts, external order hstar,cY.
source=odd_gamma({(0,1,2,3):s.Integer(1)},{(1,2):w})
eq(source[(0,3)],w)
# Odd current after even V: barX cX barY cYA cYB; no overall loop sign beyond pairing.
t=s.symbols('t');e={(0,3):-u,(0,4):-t,(1,2):w}
cur=odd_gamma(odd_gamma({(0,1,2,3,4):s.Integer(1)},e),e)
eq(cur[(4,)]/2,-u*w);eq(cur[(3,)]/2,t*w)
# All coefficients of the generic symbolic formulas are exact, not fitted examples.
for expr in [metric-trace/2,mixed-(mix.T*A*G*v)[0]]:
    eq(sum(abs(c) for c in s.Poly(s.expand(expr),*sorted(expr.free_symbols,key=str)).coeffs()),0) if expr.free_symbols else eq(expr,0)
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
    effective_action_pair={'metric_trace':'-1/2','directed_ghost_trace':'+1'},
    mean_current_first_order={'symmetric_metric_current_trace':'-1/2','one_ordered_bh_kernel':'-1','complete_ghost_current_kernel':'-1'},
    metric_current_definition='Cmetric=1/2 J_AB h_A h_B c; J is the actual Hessian of the current density',
    source='Contracted hstar*cX*barY*cY has positive Wick sign; exp(-V) adds minus before propagator/vertex normalizations',
    unresolved='Mapping every existing raw density and the composite-current placement to the same full Ward equation; no overall cancellation inferred',
    full_Q2=False,raw_loop_data_used=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
