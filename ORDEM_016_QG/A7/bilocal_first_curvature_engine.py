"""Two-endpoint parametrices to first K in a single fixed RNC chart.

The independent auxiliary w=(x-y)^2 is imposed only after differentiation.
Keeping y before differentiating avoids treating a change of anchor as -d_x.
"""
from functools import lru_cache
import sympy as s
x=s.symbols('x0:4');y=s.symbols('y0:4');w,L=s.symbols('w L')
X=s.Matrix(x);Y=s.Matrix(y);r=X-Y;I=s.eye(4)
xx=X.dot(X);yy=Y.dot(Y);xy=X.dot(Y)
gX1=-(xx*I-X*X.T)/3;gY1=-(yy*I-Y*Y.T)/3
distance1=-(xx*yy-xy**2)/3
P1=((xx-yy)*I-X*X.T+Y*Y.T)/6+(X*Y.T-Y*X.T)/2
lower1=gX1+P1
def d(a,b):return s.Integer(a==b)
def derivative(f,side,j):
    variables=x if side=='X' else y;sign=1 if side=='X' else -1
    return s.expand(s.diff(f,variables[j])+sign*2*r[j]*(s.diff(f,w)+s.diff(f,L)/w))
@lru_cache(None)
def ghost(o,a,b):
    if o==0:return d(a,b)/w
    return s.expand(P1[a,b]/w-distance1*d(a,b)/w**2+d(a,b)/4-5*d(a,b)*L/4)
@lru_cache(None)
def metric(o,a,b,c,e):
    S=(d(a,c)*d(b,e)+d(a,e)*d(b,c)-d(a,b)*d(c,e))/2
    if o==0:return S/w
    S1=(lower1[a,c]*d(b,e)+d(a,c)*lower1[b,e]+lower1[a,e]*d(b,c)+d(a,e)*lower1[b,c]-gX1[a,b]*d(c,e)-d(a,b)*gY1[c,e])/2
    return s.expand(S1/w-distance1*S/w**2+S/4+d(a,b)*d(c,e)*L/2)
def anchored(f):return s.expand(f.subs(dict.fromkeys(y,0)))
