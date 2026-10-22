"""Commutation with opposite-endpoint covariant differentiation, label by label."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
from functools import lru_cache
import sys,json,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'C6';H=ROOT/'A7'
sys.path[:0]=[str(C),str(H)]
import labelled_nonminimal_metric_euler as Old
import labelled_nonminimal_metric_euler_v2 as N
import labelled_covariant_xy as M
import labelled_bilocal_jet_engine as L
import tensor_euler_zerojet as T
from deliver_nonminimal_wick_and_mimo_audit import sha,put


@lru_cache(None)
def directly_differentiated(order,ind,word):
    if not word:return Old.euler(order,ind)
    j,*tail=word;tail=tuple(tail)
    terms=list(L.partial(directly_differentiated(order,ind,tail),1,j))
    if order:
        for pos,a in enumerate(tail):
            for k in range(4):
                changed=tail[:pos]+(k,)+tail[pos+1:]
                terms.extend(N.scaled(directly_differentiated(0,ind,changed),-T.gamma(T.y,k,j,a)))
        for pos in (2,3):
            for k in range(4):
                changed=ind[:pos]+(k,)+ind[pos+1:]
                terms.extend(N.scaled(directly_differentiated(0,changed,tail),-T.gamma(T.y,k,j,ind[pos])))
    return L.clean(terms)


def main():
    out=C/'nonminimal_yjets';out.mkdir(exist_ok=False);start=time.process_time();checks=0
    labels=[(a,b) for a in range(4) for b in range(a,4)]
    words=[()]+[(i,) for i in range(4)]+[(i,j) for i,j in product(range(4),repeat=2)]
    for n,((a,b),(c,d)) in enumerate(product(labels,repeat=2)):
        ind=(a,b,c,d)
        for o,word in product(range(2),words):
            left=N.euler(o,ind,word);right=directly_differentiated(o,ind,word)
            residual=L.clean(tuple(left)+tuple((-v,p,w) for v,p,w in right))
            assert not residual,(o,ind,word,residual);checks+=1
        if n%10==9:print(json.dumps(dict(components=n+1,checks=checks,cpu_seconds=time.process_time()-start)),flush=True)
    # Same zerojet coefficients as the already recorded predecessor table.
    previous=json.loads((C/'nonminimal_metric_euler_check_v2/TABLE.json').read_bytes())
    import ast
    for key,row in previous.items():
        value=N.pair_contact(ast.literal_eval(key),'metric',(0,1,0,1))
        assert s.expand(value-s.sympify(row['full']))==0,(key,value,row);checks+=1
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        components=100,ordered_Y_words=21,curvature_orders=[0,1],
        exact_labelled_identity=True,zerojet_regression=True,
        scope='Full PH_hh differentiated at Y up to two ordered covariant derivatives, through first curvature',
        full_metric_ghost_vertices=False,full_Q2=False,gate_changed=False)
    put(out/'results.json',result)
    paths=[Path(__file__),C/'labelled_nonminimal_metric_euler.py',C/'labelled_nonminimal_metric_euler_v2.py',C/'make_nonminimal_yjets_v2.py',C/'labelled_covariant_xy.py',C/'nonminimal_metric_euler_check_v2/TABLE.json',out/'results.json']
    put(out/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
