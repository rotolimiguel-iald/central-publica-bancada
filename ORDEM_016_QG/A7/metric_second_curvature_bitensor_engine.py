"""Spaceform Green jets through K² using endpoint Jacobi maps.

Auxiliary local Euclidean parametrix, smooth W excluded. Strip 4k/(4pi²).
The formulas are a written derivation subject to checks in separate runners.
"""
from functools import lru_cache
import sympy as s
from curved_source_jet_engine import x,z,L,dx
from metric_coincident_jet_engine_v2 import metric_fiber

@lru_cache(None)
def data():
    f=metric_fiber();I=s.eye(10);E=f['E'];om=f['omega'];S=f['S0']
    Xom=[sum((x[j]*om[j,i] for j in range(4)),s.zeros(10)) for i in range(4)]
    quadratic=sum((X*X for X in Xom),s.zeros(10))
    V2=z*(E*E/32+E/16+f['om2']/192)-quadratic/48
    F=[I/z,I/4-f['a1']*L/4,19*z*I/480+V2*L]
    AX=[ [s.zeros(10) for _ in range(4)], [A/2 for A in Xom], [z*A/24 for A in Xom]]
    N=s.Matrix(4,4,lambda i,j:z*int(i==j)-x[i]*x[j])
    JX=[s.eye(4),N/6,7*z*N/360]
    JY=[-s.eye(4),N/3,z*N/45]
    return F,AX,JX,JY,S,V2
def derivative(M,i):return M.applyfunc(lambda t:dx(t,i))
def expanded(M):return M.applyfunc(s.expand)
@lru_cache(None)
def yjet(order,j):
    F,A,JX,JY,S,V2=data();value=s.zeros(10)
    for k in range(order+1):
        value+=A[k][j]*F[order-k]
        for m in range(4):value+=JY[k][j,m]*derivative(F[order-k],m)
    return expanded(value)
@lru_cache(None)
def green_jet(order,xi=-1,yi=-1):
    F,A,JX,JY,S,V2=data()
    if xi<0 and yi<0:return expanded(F[order]*S)
    if xi<0:return expanded(yjet(order,yi)*S)
    value=s.zeros(10)
    for k in range(order+1):
        V=F[order-k] if yi<0 else yjet(order-k,yi)
        value+=A[k][xi]*V
        for m in range(4):value+=JX[k][xi,m]*derivative(V,m)
    return expanded(value*S)
