"""Check endpoint recurrence derived from simultaneous Killing covariance."""
from pathlib import Path
from functools import lru_cache
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
import bilocal_first_curvature_engine as B
import bilocal_covariant_jet_engine as E
H=Path(__file__).resolve().parent;D=H/'transvection_endpoint_recurrence';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
def dx(f,i):return s.expand(s.diff(f,B.x[i])+2*B.x[i]*(s.diff(f,B.w)+s.diff(f,B.L)/B.w))
def k1(i,a):return -(B.xx*B.d(i,a)-B.x[a]*B.x[i])/3
@lru_cache(None)
def lie(kind,order,ids,word):
    if not word:return B.anchored(E.raw(kind,order,ids))
    i,*rest=word;rest=tuple(rest)
    f=dx(lie(kind,order,ids,rest),i)
    if order:
        for c in range(4):
            f+=k1(i,c)*dx(lie(kind,0,ids,rest),c)
            if kind=='ghost':
                f-=s.diff(k1(i,ids[0]),B.x[c])*lie(kind,0,(c,ids[1]),rest)
            else:
                for pos in (0,1):
                    changed=ids[:pos]+(c,)+ids[pos+1:]
                    f+=s.diff(k1(i,c),B.x[ids[pos]])*lie(kind,0,changed,rest)
    return s.expand(f)
sources=[Path(__file__),H/'bilocal_first_curvature_engine.py',H/'bilocal_covariant_jet_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='First and second covariant Y derivatives from X Lie derivatives',
 first='DY_i G|0=-LX_i G|0',
 second='DY_j DY_i G|0=LX_i LX_j G|0+K sum_Yslots(delta_jb G[b->i]-delta_ib G[b->j])',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources],full_Q2=False))
cpu=time.process_time();checks=0;negative=[]
def zero(f,label):
    global checks
    r=s.cancel(s.expand(f).subs(B.w,B.xx));assert r==0,(label,r);checks+=1
cases=[('ghost',(0,1)),('ghost',(2,2)),('metric',(0,1,2,3)),
       ('metric',(0,0,1,1)),('metric',(0,1,0,1))]
for kind,ids in cases:
    for o in (0,1):
        for i in range(4):
            target=B.anchored(E.yjet(kind,o,ids,(i,)))
            zero(target+lie(kind,o,ids,(i,)),('first',kind,o,ids,i))
            for j in range(4):
                correction=0
                for pos in ((1,) if kind=='ghost' else (2,3)):
                    b=ids[pos]
                    for new,weight in [(i,B.d(j,b)),(j,-B.d(i,b))]:
                        changed=ids[:pos]+(new,)+ids[pos+1:]
                        correction+=weight*lie(kind,0,changed,())
                actual=B.anchored(E.yjet(kind,o,ids,(j,i)))
                zero(actual-lie(kind,o,ids,(i,j))-(correction if o else 0),
                     ('second',kind,o,ids,j,i))
                if o and len(negative)<4:
                    value=s.cancel(correction.subs(B.w,B.xx)).subs(dict(zip(B.x,(1,2,0,0))))
                    if value!=0:negative.append(dict(kind=kind,indices=ids,i=i,j=j,omitted_curvature=str(value)))
    print(kind,ids,'checks',checks,'cpu',time.process_time()-cpu,flush=True)
assert negative
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,negative_controls=negative,
 cpu_seconds=time.process_time()-cpu,status='ENDPOINT_RECURRENCE_COMPONENTS_EXACT',
 scope='Five tensor components, all derivative directions, symbolic X, K0/K1; general derivation separate',
 full_Q2=False,distribution_extension=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
