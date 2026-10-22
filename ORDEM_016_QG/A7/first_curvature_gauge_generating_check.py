"""Check the closed generating function against ordered words and prior jets."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
from math import factorial
import hashlib,json,random,time,uuid
from first_curvature_gauge_generating_engine import AXES,dot,word_value,gauge_generator
from oneform_second_curvature_engine_v2 import oneform_second
from position_metric_bubble_engine import LABELS

H=Path(__file__).resolve().parent;D=H/'first_curvature_gauge_generating';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,value):
    p=D/name;assert not p.exists(),p
    data=json.dumps(value,indent=2,ensure_ascii=False).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(data);assert t.read_bytes()==data;t.replace(p)
sources=[Path(__file__),H/'first_curvature_gauge_generating_engine.py',H/'oneform_second_curvature_engine_v2.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Resum firstK ordered covariant Taylor jets exactly; preserve anchored outer derivative',
 seed=164701,orders=[0,1],derivative_lengths_prior=[1,3,5],directional_lengths=[0,1,2,3,4,5,6,7,8],
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources],full_Q2=False))
cpu=time.process_time();rng=random.Random(164701);count=0
for seed in range(2):
    p=tuple(rng.randint(-2,3) for _ in range(4));v=tuple(rng.randint(-2,3) for _ in range(4))
    jet,_,_=oneform_second(v,p)
    for n in (1,3,5):
        for sample in range(24):
            word=tuple(rng.randrange(4) for _ in range(n));a=rng.randrange(4)
            for order in (0,1):
                raw=word_value(tuple(AXES[i] for i in word),AXES[a],p,v,order)
                if n<2*order+1:expected=F()
                else:expected=(-1)**((n-2*order-1)//2)*raw
                assert expected==jet(word,a,order),(word,a,order,expected,jet(word,a,order))
                count+=1
    x=tuple(rng.randint(-2,2) for _ in range(4))
    for xi,yj in [(-1,-1),(0,-1),(-1,2),(1,3)]:
        prefix=(AXES[yj],) if yj>=0 else ()
        suffix=(AXES[xi],) if xi>=0 else ()
        for order in (0,1):
            poly=gauge_generator(p,v,x,xi,yj,order)
            for n in range(9):
                for label,(a,b) in enumerate(LABELS):
                    word=prefix+(x,)*n+suffix
                    actual=word_value(word+(AXES[a],),AXES[b],p,v,order)
                    actual+=word_value(word+(AXES[b],),AXES[a],p,v,order)
                    expected=sum((F(factorial(n),factorial(n-j))*dot(p,x)**(n-j)*poly[j][label]
                                  for j in range(min(n,2)+1)),F())
                    assert actual==expected,(seed,xi,yj,order,n,label,actual,expected)
                    count+=1
result=dict(at=datetime.now(timezone.utc).isoformat(),status='FIRST_K_COVARIANT_TAYLOR_GENERATOR_MATCHED',
 checks=count,cpu_seconds=time.process_time()-cpu,full_Q2=False,
 formula='sum D_y D_x^n D_i G(v)/n! = exp(p.x)*(P0+P1+P2), through K1',
 derivation='Select two or three ordered slots; k radial choices give binomial(n,k), then 1/k! after exponential sum; all-radial triple Gamma vanishes',
 scope='Real formal momenta; restore Fourier phases per homogeneous degree; not yet the integrated curved amplitude')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
