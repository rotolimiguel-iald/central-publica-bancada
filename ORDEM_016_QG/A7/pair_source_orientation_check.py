"""Check moving-frame derivatives, then evaluate pairs in source orientation."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import json,hashlib,time,uuid
import sympy as s
from pair_source_orientation_engine import oriented_pair_node,x_components,y_components
from einstein_test_field_engine import x,Z,I,gradient_tensor,parallel_tensor,gauge
from position_metric_bubble_engine import BASIS,LABELS
H=Path(__file__).resolve().parent;D=H/'pair_source_orientation';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'pair_source_orientation_engine.py',H/'einstein_test_field_engine.py',H/'einstein_source_adjoint/results.json',
 H/'angular_cubature_degree12/results.json',H/'flat_reference_ward/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Raw pairs with metric test at X and gauge ghost at Y, same orientation as source(E test,c)',
 controls='Full moving-frame derivative polynomial identity and origin ghost jets; flat reference; firstK nonaxis',
 no_ward_zero_target=True,exclusions=['tadpole','W','cutoff hierarchy','higher arities','full Q2'],
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();checks=[]
T=s.Matrix([[1,2,0,-1],[2,3,1,0],[0,1,-2,1],[-1,0,1,4]]);p=s.Matrix([1,2,-1,1]);v=s.Matrix([2,-1,1,3]);X=s.Matrix(x)
coord=gradient_tensor(parallel_tensor(T),-s.I*p);frame=(Z*I-X*X.T)/6;tx=T*X;px=p.dot(X)
for i in range(4):
    for a in range(4):
        for b in range(4):
            literal=coord[1][i][a,b]+sum(frame[i,j]*coord[0][j][a,b]+frame[a,j]*coord[0][i][j,b]+frame[b,j]*coord[0][i][a,j] for j in range(4))
            formula=(x[a]*T[i,b]+x[b]*T[a,i]-int(i==a)*tx[b]-int(i==b)*tx[a])/2-s.I*(Z*p[i]-x[i]*px)*T[a,b]/6
            assert s.expand(literal-formula)==0,(i,a,b)
            checks.append('moving_frame_'+str((i,a,b)))
V=[v,(-(Z*I-X*X.T)*v/6).applyfunc(s.expand)];DG=gradient_tensor(gauge(V,s.I*p),s.I*p)
for j in range(4):
    yy=y_components(tuple(p),tuple(v),1,j)
    for o,phase,vec in yy:
        for k,(a,b) in enumerate(LABELS):
            literal=DG[o][j][a,b].subs(dict.fromkeys(x,0))
            assert s.expand(literal-s.I**phase*s.Rational(vec[k]))==0
            checks.append('ghost_origin_'+str((j,o,a,b)))
put('field_checks.json',dict(checks=len(checks),cpu_seconds=time.process_time()-cpu))
nodes=json.loads((H/'angular_cubature_degree12/results.json').read_bytes())['nodes'];data=[]
contact=json.loads((H/'finite_pair_ward/results.json').read_bytes());reference=json.loads((H/'flat_reference_ward/results.json').read_bytes())
def run(ti,p,v,order):
    out=[[F() for _ in range(3)] for _ in range(2)]
    for ni,node in enumerate(nodes):
        got=oriented_pair_node(BASIS[ti],p,v,tuple(node['vector']),order);w=F(node['weight'])
        for a in range(2):
            for j in range(3):out[a][j]+=w*got[a][j]
        if ni%100==0:print(json.dumps(dict(order=order,T=ti,node=ni,cpu=time.process_time()-cpu)),flush=True)
    comb=[-out[0][j]/2+out[1][j] for j in range(3)]
    row=dict(order=order,T=ti,p=p,v=v,metric=list(map(str,out[0])),ghost=list(map(str,out[1])),combination=list(map(str,comb)))
    data.append(row);print(json.dumps(row),flush=True)
    return out,comb
fixtures=[(1,(0,1,0,0)),(4,(1,0,0,0)),(0,(1,0,0,0))];p=(1,0,0,0)
for ti,v in fixtures:
    out,_=run(ti,p,v,0);old=next(r for r in contact['values'] if r['order']==0 and r['T']==ti);ref=next(r for r in reference['values'] if r['T']==ti and r['p']==list(p))
    for j,key in enumerate(('metric','ghost')):
        expected=sum(map(F,old[key+'_pieces']))+F(ref[key])
        assert out[j][0]==expected,(ti,key,out[j],expected)
        checks.append('flat_calibration_'+str((ti,key)))
def basis(ti,p,v):
    T=s.Matrix(4,4,BASIS[ti]);p=s.Matrix(p);v=s.Matrix(v)
    return [p.dot(p)*(p.T*T*v)[0],(p.T*T*p)[0]*p.dot(v),p.dot(p)*s.trace(T)*p.dot(v)]
fit=s.Matrix([basis(ti,p,v) for ti,v in fixtures]).inv()*s.Matrix([list(map(s.Rational,run(ti,p,v,1)[1])) for ti,v in fixtures])
p=(1,2,-1,1);v=(2,-1,1,3);_,got=run(4,p,v,1);pred=s.Matrix([basis(4,p,v)])*fit
for j in range(3):assert s.Rational(got[j])==pred[j],(j,got[j],pred[j]);checks.append('nonaxis_'+str(j))
result=dict(at=datetime.now(timezone.utc).isoformat(),status='PAIRS_IN_SOURCE_ORIENTATION_MEASURED',checks=len(checks),
 values=data,coefficients=[[str(fit[i,j]) for j in range(3)] for i in range(3)],cpu_seconds=time.process_time()-cpu,full_Q2=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'field_checks.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='values'}))
