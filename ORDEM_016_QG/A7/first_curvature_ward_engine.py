"""Pure ordered-symbol gauge evaluation extracted from the diagnostic."""
from oneform_radial_jet_engine import oneform

def gauge_hessian(v,p,order,flat,curved):
    c1,c2,c3,c4,c5=flat
    d1,d2,d3,_,d4=curved
    jet,j=oneform(tuple(v),tuple(p));out=[]
    for a in range(4):
        row=[]
        for b in range(4):
            value=c1*sum(j((i,i,k,k),a,b,order) for i in range(4) for k in range(4))
            if a==b:value+=c2*sum(j((i,i,k,k),m,m,order) for i in range(4) for k in range(4) for m in range(4))
            value+=c3*sum(j((a,b,i,i),m,m,order) for i in range(4) for m in range(4))
            if a==b:value+=c3*sum(j((i,k,m,m),i,k,order) for i in range(4) for k in range(4) for m in range(4))
            value+=c4/2*sum(j((a,i,k,k),i,b,order)+j((b,i,k,k),i,a,order) for i in range(4) for k in range(4))
            value+=c5*sum(j((a,b,i,k),i,k,order) for i in range(4) for k in range(4))
            if order:
                value-=d1*sum(j((i,i),a,b,0) for i in range(4))
                if a==b:value-=d2*sum(j((i,i),m,m,0) for i in range(4) for m in range(4))
                value-=d3*sum(j((a,b),m,m,0) for m in range(4))
                if a==b:value-=d3*sum(j((i,k),i,k,0) for i in range(4) for k in range(4))
                value-=d4/2*sum(j((a,i),i,b,0)+j((b,i),i,a,0) for i in range(4))
            row.append(value)
        out.append(row)
    return out
