"""Exact graded Wick and differentiated-kernel checks for the ghost current."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from ghost_current_insertion_engine import GhostCurrentInsertion,contraction_terms
from position_metric_bubble_engine import BASIS,LABELS
from full_loop_extension_engine import x,z,Q,dx

H=Path(__file__).resolve().parent;D=H/'ghost_current_insertion';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();raw=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(raw)
    assert t.read_bytes()==raw;t.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'ghost_current_insertion_engine.py',H/'localized_ghost_boundary_engine.py']],
    target='Graded Wick signs, both choices of external ghost, complete local vertex, derivative extension',
    global_Ward_weight=False,full_Q2=False))
start=time.process_time();checks=0
def eq(a,b=0):
    global checks
    assert s.cancel(a-b)==0,(a,b,s.cancel(a-b));checks+=1

# Independent exterior-algebra contraction, not the signs hardcoded in the engine.
# Left derivative d_i removes i with (-1)^position; d_j d_i gives contraction of ordered i,j.
def derivative(poly,i):
    out={}
    for word,v in poly.items():
        if i in word:
            k=word.index(i);key=word[:k]+word[k+1:]
            out[key]=out.get(key,0)+(-1)**k*v
    return out
def gamma(poly,entries):
    out={}
    for (i,j),c in entries.items():
        for word,v in derivative(derivative(poly,i),j).items():out[word]=out.get(word,0)+c*v
    return out
# Field order barX,cX,barY,cYA,cYB; entry signs follow the graded covariance.
u,v,w=s.symbols('u v w');poly={(0,1,2,3,4):s.Integer(1)}
entries={(0,3):-u,(0,4):-v,(1,2):w}
second={key:s.expand(value/2) for key,value in gamma(gamma(poly,entries),entries).items()}
eq(second[(4,)],-u*w);eq(second[(3,)],v*w)
for e,expected in [({(0,3):-u,(1,2):w},-u*w),({(0,4):-v,(1,2):w},v*w)]:
    out=gamma(gamma(poly,e),e)
    eq(sum(out.values())/2,expected)
bad={(0,3):u,(0,4):v,(1,2):w};badresult=gamma(gamma(poly,bad),bad)
eq(badresult[(4,)]/2,u*w);eq(badresult[(3,)]/2,-v*w)

point=(1,2,-1,1);probe=(2,1,0,0);T=BASIS[LABELS.index((1,1))];rows=[]
def ev(f):return f.subs(dict(zip(x,point))).subs(z,sum(t*t for t in point))
for lam,et in [((0,0,0,0),(0,0,0,0)),((0,0,0,0),(1,0,0,0)),((1,-1,0,0),(1,0,0,0))]:
    a=GhostCurrentInsertion(T,0,lam,et);b=GhostCurrentInsertion(T,0,lam,et,point)
    for kw in sorted({key[-1] for key in a.terms}):
        for ex in [-1,0,1,2,3]:
            f=a.raw(ex,kw)
            for word in [(),(0,),(1,)]:
                sf=f
                for i in word:sf=dx(sf,i)
                eq(ev(sf),b.raw(ex,kw,word))
    kernel=a.off_diagonal();eq(ev(kernel),b.off_diagonal())
    extension=a.extension_contact()
    # The two separately enumerated contraction branches add to the full result.
    left=GhostCurrentInsertion(T,0,lam,et,point,omit=1).off_diagonal()
    right=GhostCurrentInsertion(T,0,lam,et,point,omit=0).off_diagonal()
    eq(left+right,b.off_diagonal())
    if not any(et):eq(kernel,0);eq(extension,0)
    else:assert left!=0 and right!=0 and left!=b.off_diagonal() and right!=b.off_diagonal();checks+=1
    rows.append(dict(lambda_x=lam,eta_y=et,kernel=str(kernel),at_point=str(ev(kernel)),
        contact=str(extension),contact_at_probe=str(extension.subs(dict(zip(Q,probe)))),
        first_contraction_at_point=str(left),second_contraction_at_point=str(right)))
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
    wick_signs=['- for contracted first cY, external second cY','+ for contracted second cY, external first cY'],
    point=point,contact_probe=probe,contact_unit='CE=-4pi²',rows=rows,full_Q2=False,
    global_Ward_weights='Not inserted; sum of both internal ghost assignments only',
    scope='Flat localized h/c diagram, no curvature or smooth state data')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'ghost_current_insertion_engine.py',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=checks,cpu_seconds=result['cpu_seconds'],rows=[{k:v for k,v in row.items() if k not in ['kernel','contact']} for row in rows])))
