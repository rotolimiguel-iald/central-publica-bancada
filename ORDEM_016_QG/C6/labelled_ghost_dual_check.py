"""Independent recursive dual-connection check, plus finite contact control."""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
from itertools import product
import json,sys,time
import sympy as s

ROOT=Path(__file__).resolve().parents[1];C=ROOT/'C6';H=ROOT/'A7'
sys.path[:0]=[str(C),str(H)]
import labelled_ghost_dual as D
import labelled_covariant_xy as M
import labelled_bilocal_jet_engine as L
import tensor_euler_zerojet as T
from deliver_nonminimal_wick_and_mimo_audit import sha,put


@lru_cache(None)
def direct(order,ind,xword=(),yword=()):
    # Independently apply covector X / vector Y connections to the undifferentiated dual.
    if not xword and not yword:return D.cov(order,ind)
    side=0 if xword else 1
    word=xword if side==0 else yword
    i,*tail=word;tail=tuple(tail)
    xrest=tail if side==0 else xword
    yrest=tail if side==1 else yword
    terms=list(L.partial(direct(order,ind,xrest,yrest),side,i))
    if order:
        coords=T.x if side==0 else T.y
        for pos,j in enumerate(tail):
            changed=tail[:pos]+(0,)+tail[pos+1:]
            for k in range(4):
                changed=tail[:pos]+(k,)+tail[pos+1:]
                lower=direct(0,ind,changed if side==0 else xrest,changed if side==1 else yrest)
                gam=-T.gamma(coords,k,i,j)
                terms.extend((gam*v,p,w) for v,p,w in lower)
        for k in range(4):
            a,b=ind
            ids=(k,b) if side==0 else (a,k)
            gam=-T.gamma(coords,k,i,a) if side==0 else T.gamma(coords,b,i,k)
            terms.extend((gam*v,p,w) for v,p,w in direct(0,ids,xrest,yrest))
    return L.clean(terms)


def main():
    output=C/'ghost_dual_check';output.mkdir(exist_ok=False)
    now=datetime.now(timezone.utc);start=time.process_time();checks=0
    def eq(a,b,label):
        nonlocal checks
        assert s.cancel(s.expand(a-b))==0,(label,a,b);checks+=1
    def same(a,b,label):
        nonlocal checks
        # Stronger than equality off diagonal: exact same base profile and derivative labels.
        residual=L.clean(tuple(a)+tuple((-c,p,w) for c,p,w in b))
        assert not residual,(label,residual);checks+=1
    words=[((),())]
    words += [((i,),()) for i in range(4)]+[((),(j,)) for j in range(4)]
    words += [((i,),(j,)) for i,j in product(range(4),repeat=2)]
    words += [((i,j),()) for i,j in product(range(4),repeat=2)]
    words += [((),(i,j)) for i,j in product(range(4),repeat=2)]
    for a,b in product(range(4),repeat=2):
        for order,(xw,yw) in product(range(2),words):
            same(D.cov(order,(a,b),xw,yw),direct(order,(a,b),xw,yw),(order,a,b,xw,yw))
    print(json.dumps(dict(stage='derivatives',checks=checks,cpu_seconds=time.process_time()-start)),flush=True)
    # Contract the independent second covariant derivative, including density and +3K.
    for a,b in product(range(4),repeat=2):
        ind=(a,b)
        for order in range(2):
            terms=[]
            for i in range(4):terms.extend(direct(order,ind,(i,i),()))
            if order:
                for i,j in product(range(4),repeat=2):
                    g=(T.xx*T.delta(i,j)-T.x[i]*T.x[j])/3
                    terms.extend((g*v,p,w) for v,p,w in direct(0,ind,(i,j),()))
                terms.extend((3*v,p,w) for v,p,w in direct(0,ind))
                for i in range(4):
                    terms.extend((-T.xx*v/2,p,w) for v,p,w in direct(0,ind,(i,i),()))
            same(D.euler(order,ind),L.clean(terms),('Euler',order,ind))
    # Record differences; matching flat indices does not license reuse at first curvature.
    witnesses=[];table={}
    for a,b,c,d in product(range(4),repeat=4):
        ind=(a,b);other=(c,d)
        old0=M.pair_contact('ghost',ind,'ghost',other,order=0)
        new0=D.pair_contact(ind,'ghost',other,order=0)
        eq(new0,old0,('flat',ind,other))
        old=M.pair_contact('ghost',ind,'ghost',other)
        new=s.expand(D.pair_contact(ind,'ghost',other))
        difference=s.expand(new-old)
        table[str((a,b,c,d))]=str(new)
        if difference!=0:witnesses.append(dict(first=ind,second=other,dual=str(new),original=str(old),difference=str(difference)))
    result=dict(at=now.isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        derivative_words=len(words),label_identity_checked=True,
        contacts=256,nonzero_dualization_changes=len(witnesses),witnesses=witnesses[:8],
        scope='First curvature; ghost covector X/vector Y; same partial labelled extension, zerojet spectator contacts',
        Grassmann_sign_assigned=False,full_metric_ghost_assembly=False,full_Q2=False,gate_changed=False)
    put(output/'results.json',result);put(output/'TABLE.json',table)
    paths=[Path(__file__),C/'labelled_ghost_dual.py',C/'labelled_covariant_xy.py',C/'labelled_bilocal_jet_engine.py',output/'results.json',output/'TABLE.json']
    put(output/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    print(json.dumps(result,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
