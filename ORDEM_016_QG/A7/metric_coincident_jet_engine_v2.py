"""Coincident UV Green jets in a space form, in an orthonormal radial frame.

Auxiliary Euclidean D=-(nabla²+E). Entries are exact, with K stripped:
a1 has degree K, a2 and mixed_jets have degree K². No finite state part.
"""
import sympy as s

def metric_fiber():
    labels=[(i,j) for i in range(4) for j in range(i,4)]
    basis=[]
    for i,j in labels:
        H=s.zeros(4);H[i,j]=H[j,i]=1;basis.append(H)
    gram=s.diag(*[1 if i==j else 2 for i,j in labels])
    g=s.Matrix([int(i==j) for i,j in labels])
    ptr=g*g.T/4;tl=s.eye(10)-ptr;itr=s.eye(10)-g*g.T/2
    E=-2*tl+6*ptr
    omega={}
    for i in range(4):
        for j in range(4):
            om=s.zeros(4)
            if i!=j:om[i,j]=1;om[j,i]=-1
            images=[om*H+H*om.T for H in basis]
            omega[i,j]=s.Matrix(10,10,lambda a,b:images[b][labels[a][0],labels[a][1]])
    om2=sum((om*om for om in omega.values()),s.zeros(10))
    a1=E+2*s.eye(10)
    a2=E*E/2+2*E+s.Rational(29,15)*s.eye(10)+om2/12
    xx={};mixed={}
    for i in range(4):
        for j in range(4):
            xx[i,j]=(E/2+s.Rational(29,30)*s.eye(10))*int(i==j)
            xx[i,j]+=sum((omega[i,k]*omega[j,k]+omega[j,k]*omega[i,k]
                          for k in range(4)),s.zeros(10))/12
            xx[i,j]+=omega[i,j]*a1/2
    for i in range(4):
        for j in range(4):
            mixed[i,j]=a2*int(i==j)/2-xx[j,i]
    return dict(labels=labels,basis=basis,gram=gram,g=g,ptr=ptr,tl=tl,itr=itr,
                E=E,omega=omega,om2=om2,a1=a1,a2=a2,xx=xx,mixed=mixed,
                S0=itr*gram.inv())
