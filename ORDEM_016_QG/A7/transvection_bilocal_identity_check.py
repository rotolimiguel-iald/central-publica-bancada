"""Independent first-curvature Killing and bilocal covariance check, off diagonal."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
import bilocal_first_curvature_engine as B
H=Path(__file__).resolve().parent;D=H/'transvection_bilocal_identity';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
    p=D/name;assert not p.exists();b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'bilocal_first_curvature_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 claim='FirstK Killing field and diagonal Lie derivative of bilocal propagators',
 k1='-(X² delta_i^a-Xa Xi)/3',
 scope='Off diagonal, firstK, no distribution extension, no Q2',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();checks=0;neg=[]
def k1(P,i,a):return -(sum(t*t for t in P)*B.d(i,a)-P[a]*P[i])/3
def simp(f):return s.cancel(s.expand(f).subs(B.w,sum(t*t for t in B.r)))
def assert_zero(f,label):
    global checks
    r=simp(f);assert r==0,(label,r);checks+=1
for i in range(4):
    for a in range(4):
        for b in range(4):
            assert_zero(s.diff(B.gX1[a,b],B.x[i])+s.diff(k1(B.x,i,b),B.x[a])+s.diff(k1(B.x,i,a),B.x[b]),('Killing',i,a,b))
for i in range(4):
    for a in range(4):
        for b in range(4):
            g0=B.ghost(0,a,b);g1=B.ghost(1,a,b)
            expr=B.derivative(g1,'X',i)+B.derivative(g1,'Y',i)
            for c in range(4):
                expr+=k1(B.x,i,c)*B.derivative(g0,'X',c)+k1(B.y,i,c)*B.derivative(g0,'Y',c)
                expr-=s.diff(k1(B.x,i,a),B.x[c])*B.ghost(0,c,b)
                expr+=s.diff(k1(B.y,i,c),B.y[b])*B.ghost(0,a,c)
            assert_zero(expr,('ghost',i,a,b))
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    ids=(a,b,c,d);g0=B.metric(0,*ids);g1=B.metric(1,*ids)
                    expr=B.derivative(g1,'X',i)+B.derivative(g1,'Y',i)
                    for e in range(4):
                        expr+=k1(B.x,i,e)*B.derivative(g0,'X',e)+k1(B.y,i,e)*B.derivative(g0,'Y',e)
                        for pos in range(4):
                            P=B.x if pos<2 else B.y
                            changed=ids[:pos]+(e,)+ids[pos+1:]
                            expr+=s.diff(k1(P,i,e),P[ids[pos]])*B.metric(0,*changed)
                    assert_zero(expr,('metric',i,*ids))
    print('generator',i,'checks',checks,'cpu',time.process_time()-cpu,flush=True)
# Independent concrete defect of naive translation; no expected result from a provider.
for kind,ids,i in [('ghost',(0,1),1),('metric',(0,0,0,1),1)]:
    f=B.ghost(1,*ids) if kind=='ghost' else B.metric(1,*ids)
    r=B.anchored(B.derivative(f,'X',i)+B.derivative(f,'Y',i))
    r=simp(r).subs(dict(zip(B.x,(1,0,0,0)))).subs(dict.fromkeys(B.y,0))
    r=s.simplify(r);assert r!=0,(kind,ids,i,r)
    neg.append(dict(kind=kind,indices=ids,generator=i,defect=str(r)))
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,
 negative_controls=neg,cpu_seconds=time.process_time()-cpu,
 status='FIRST_K_BILOCAL_KILLING_COVARIANCE_CHECKED',
 quantum_anomaly_computed=False,second_endpoint_recurrence_derived=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
