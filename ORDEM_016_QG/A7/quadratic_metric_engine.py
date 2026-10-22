"""Local O(4)-covariant quadratic metric maps of derivative degree two; IO-free."""
import marked_polynomial_engine as p
def mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(4)),p.ZERO) for j in range(4)] for i in range(4)]
def transpose(A):return [list(x) for x in zip(*A)]
def raw(H,k,J,l):
    h=p.trace(H);j=p.trace(J);HJ=mm(H,J);JH=mm(J,H);hj=p.inner(H,J)
    kk,kl,ll=p.dot(k,k),p.dot(k,l),p.dot(l,l)
    hk,hl,jk,jl=p.mv(H,k),p.mv(H,l),p.mv(J,k),p.mv(J,l)
    terms=[];names=[]
    def add(name,A):names.append(name);terms.append(A)
    for name,A in [('HJ+JH',p.madd(HJ,JH)),('H trJ',p.mscale(H,j)),('J trH',p.mscale(J,h)),('I trH trJ',p.mscale(p.I,h*j)),('I trHJ',p.mscale(p.I,hj))]:
        for n,t in [('k2',kk),('kl',kl),('l2',ll)]:add(name+' '+n,p.mscale(A,t))
    for n,A in [('kk',p.outer(k,k)),('symkl',p.sym(k,l)),('ll',p.outer(l,l))]:
        for m,t in [('trH trJ',h*j),('trHJ',hj)]:add(n+' '+m,p.mscale(A,t))
    for n,t in [('kHk trJ',p.dot(k,hk)*j),('kHl trJ',p.dot(k,hl)*j),('lHl trJ',p.dot(l,hl)*j),
                ('kJk trH',p.dot(k,jk)*h),('kJl trH',p.dot(k,jl)*h),('lJl trH',p.dot(l,jl)*h)]:add('I '+n,p.mscale(p.I,t))
    for an,a in [('k',k),('l',l)]:
        for bn,b in [('k',k),('l',l)]:add('I '+an+'HJ'+bn,p.mscale(p.I,p.dot(a,p.mv(HJ,b))))
    for n,A,t in [('H kJk',H,p.dot(k,jk)),('H kJl',H,p.dot(k,jl)),('H lJl',H,p.dot(l,jl)),
                   ('J kHk',J,p.dot(k,hk)),('J kHl',J,p.dot(k,hl)),('J lHl',J,p.dot(l,hl))]:add(n,p.mscale(A,t))
    for an,a in [('Hk',hk),('Hl',hl)]:
        for bn,b in [('Jk',jk),('Jl',jl)]:add('sym '+an+' '+bn,p.sym(a,b))
    for an,a in [('k',k),('l',l)]:
        for bn,b,t in [('Hk trJ',hk,j),('Hl trJ',hl,j),('Jk trH',jk,h),('Jl trH',jl,h)]:add('sym '+an+' '+bn,p.mscale(p.sym(a,b),t))
    for an,a in [('k',k),('l',l)]:
        for bn,b in [('HJk',p.mv(HJ,k)),('HJl',p.mv(HJ,l)),('JHk',p.mv(JH,k)),('JHl',p.mv(JH,l))]:add('sym '+an+' '+bn,p.sym(a,b))
    assert len(terms)==57
    return terms,names
def terms(H,k,J,l):
    first,names=raw(H,k,J,l);second,other=raw(J,l,H,k)
    assert names==other
    return [p.mscale(p.madd(A,B),p.QQ(1,2)) for A,B in zip(first,second)],names
