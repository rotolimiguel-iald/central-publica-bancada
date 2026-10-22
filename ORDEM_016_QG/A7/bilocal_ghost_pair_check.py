"""Insert the existing ghost vertices into the full Y-divergence at one point."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from fractions import Fraction as F
import bilocal_ghost_pair_engine as E
import ghost_direct_position_engine as G
H=Path(__file__).resolve().parent;D=H/'bilocal_ghost_pair';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'bilocal_ghost_pair_engine.py',H/'bilocal_covariant_jet_engine.py',
 H/'bilocal_first_curvature_engine.py',H/'ghost_direct_position_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Actual ghost loop B0/B1 inserted in endpoint Ward reduction',
 point=[1,0,0,0],external_h='e11 in local orthonormal frame',external_Dh=0,
 scope='Pointwise off diagonal, only hX jet; no R extension/Fourier or other loops',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();checks=[];point=(1,0,0,0);J=E.PointJets(point)
G0,G1,GL,d0,d1=G.green(point)
for order in (0,1):
    actual=J.matrix(order)
    refs=(G0,[{} for _ in range(20)]) if order==0 else (G1,GL)
    den=d0 if order==0 else d1
    for ell in (0,1):
        for i in range(20):
            for j in range(20):
                value=actual[ell][i].get(j,F())-F(refs[ell][i].get(j,0),den)
                assert value==0,(order,ell,i,j,value)
                checks.append((order,ell,i,j))
    print('ANCHORED_GREEN_MATCH',order,len(checks),'cpu',time.process_time()-cpu,flush=True)

# Flat endpoint derivative independently from translation of the scalar kernel.
x=s.symbols('x0:4');z=sum(q*q for q in x);xm=dict(zip(x,point))
for word in [(0,),(1,),(0,0),(0,1),(1,1)]:
    actual=J.matrix(0,word)[0]
    for ix in range(5):
        for iy in range(5):
            f=1/z
            if ix:f=s.diff(f,x[ix-1])
            if iy:f=-s.diff(f,x[iy-1])
            for j in word:f=-s.diff(f,x[j])
            expected=F(f.subs(xm))
            value=actual[4*ix][0+4*iy] .__class__ if False else actual[4*ix].get(4*iy,F())
            assert value==expected,(word,ix,iy,value,expected)
            checks.append(('flat_translation',word,ix,iy))
    print('FLAT_TRANSLATION_MATCH',word,'cpu',time.process_time()-cpu,flush=True)
T=E.tensor(1,1)
def progress(o,b,row):print(json.dumps(dict(order=o,b=b,value=list(map(str,row)),cpu=time.process_time()-cpu)),flush=True)
values,J=E.ghost_ward_point(point,T,progress,jets=J)
for order in (0,1):
    for b in (1,2,3):
        assert values[order][b]==(0,0),(order,b,values[order][b])
        checks.append(('axial_parity',order,b))
result=dict(at=datetime.now(timezone.utc).isoformat(),status='GHOST_LOOP_Y_DIVERGENCE_POINT_MEASURED',
 checks=len(checks),cpu_seconds=time.process_time()-cpu,
 values=[[[str(t) for t in row] for row in rows] for rows in values],
 log_basis=['1','log(mu²x²)'],point=point,external_tensor='e11',external_Dh=0,
 full_Q2=False,metric_loop=False,source=False,tadpole=False,distribution_extension=False,
 scope='Actual existing ghost vertices, complete pointwise Y endpoint IBP for the hX jet only')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
