"""The fixed 21-contraction ghost ansatz, reusable without running checks."""
import marked_polynomial_engine as p
def terms(H,k,l,v):
    hk,hl,hv=p.mv(H,k),p.mv(H,l),p.mv(H,v);tr=p.trace(H)
    kk,kl,ll=p.dot(k,k),p.dot(k,l),p.dot(l,l);kv,lv=p.dot(k,v),p.dot(l,v)
    return ([p.scale(v,tr*x) for x in (kk,kl,ll)]+
            [p.scale(v,x) for x in (p.dot(k,hk),p.dot(k,hl),p.dot(l,hl))]+
            [p.scale(hv,x) for x in (kk,kl,ll)]+
            [p.scale(hk,kv),p.scale(hk,lv),p.scale(hl,kv),p.scale(hl,lv)]+
            [p.scale(k,tr*kv),p.scale(k,tr*lv),p.scale(l,tr*kv),p.scale(l,tr*lv)]+
            [p.scale(k,p.dot(v,hk)),p.scale(k,p.dot(v,hl)),p.scale(l,p.dot(v,hk)),p.scale(l,p.dot(v,hl))])
