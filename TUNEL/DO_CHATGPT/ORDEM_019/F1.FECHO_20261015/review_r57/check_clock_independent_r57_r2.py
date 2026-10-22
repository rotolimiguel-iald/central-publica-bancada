"""Independent finite-matrix checks from Schrodinger evolution; no mission mutation."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import xml.etree.ElementTree as ET
import zipfile
import sympy as s

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent
def pin(path):
    p=Path(path); b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
pins=[]
def verify(p):
    q=pin(p['path']); assert all(q[k]==v for k,v in p.items()),p
    if q not in pins:pins.append(q)
scope=read(OUT/'device_clock_r57/SCOPE_R57.json')
for p in scope['source_pins']+[scope['runner']]:verify(p)
start=read(OUT/'device_clock_r57/RUN_START_R57.json')
end=read(OUT/'device_clock_r57/RUN_END_R57.json')
for p in [start['script'],start['scope'],end['script'],end['result']]:verify(p)
assert end['exit_code']==0
source=read(OUT/'device_clock_r57/SYMBOLIC_RESULT_R57.json')
assert len(source['checks'])==34 and all(x['passed'] for x in source['checks'])
custody=read(OUT/'continuity_r57/SOURCE_JAN09_CUSTODY_R57.json')
for key in ['source','copy','extraction']:verify(custody[key])
assert Path(custody['source']['path']).read_bytes()==Path(custody['copy']['path']).read_bytes()
with zipfile.ZipFile(custody['copy']['path']) as archive:
    document=ET.fromstring(archive.read('word/document.xml'))
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    m='{http://schemas.openxmlformats.org/officeDocument/2006/math}'
    paras=[''.join(x.text or '' for x in p.iter() if x.tag in (w+'t',m+'t'))
           for p in document.find(w+'body').findall(w+'p')]
    extracted='\n'.join(f'[{i}] {p}' for i,p in enumerate(paras,1) if p)+'\n'
    assert extracted.encode()==Path(custody['extraction']['path']).read_bytes()
    metadata=archive.read('docProps/core.xml').decode('utf-8')
    assert '2026-01-09T15:33:00Z' in metadata

checks=[]
def eq(name,left,right):
    d=left-right
    entries=list(d) if isinstance(d,s.MatrixBase) else [d]
    assert all(s.simplify(x)==0 for x in entries),name
    checks.append({'name':name,'passed':True})
I=s.eye(2); down=s.Matrix([[0,1],[0,0]])
embed=lambda op,k:s.kronecker_product(*[op if j==k else I for j in range(3)])
ai,ao,sm=[embed(down,k) for k in range(3)]
sp=sm.H; Z=embed(s.diag(1,-1),2)
ni,no,ne=ai.H*ai,ao.H*ao,sp*sm
wc,w,g,om,ki,ko,ga,gp,la,a=s.symbols('omega_c omega_OH g_JC Omega_Rabi kappa_in kappa_out gamma_OH gamma_phi lambda_holo a',positive=True)
h=wc*(ni+no)+w*ne+g*(ai.H*sm+sp*ai)+om*(sp+sm)
J=ao.H*sm+sp*ai
jumps=[(ki,ai),(ko,ao),(ga,sm),(gp,Z),(la,J)]
def evolve(r):
    v=-s.I*(h*r-r*h)
    for rate,c in jumps:
        q=c.H*c;v+=rate*(c*r*c.H-(q*r+r*q)/2)
    return v.applyfunc(s.expand)
def signal(r):return s.expand(2*s.trace(r*sp))
rhs=(s.I*w-ga/2-2*gp)*sp+s.I*g*ai.H*Z+s.I*om*Z+la*(ai.H*ao.H*sm-(ni+ao*ao.H)*sp/2)
# Adjoint recovered via trace duality on all 64 matrix units, not a copied dual routine.
adjoint=s.zeros(8)
for i in range(8):
    for j in range(8):
        unit=s.zeros(8);unit[j,i]=1
        adjoint[i,j]=s.trace(evolve(unit)*sp)
eq('64_matrix_unit_trace_duality',adjoint,rhs)
eq('pump_obstruction',adjoint[0,0],s.I*om)
vac=s.diag(1,0);rho=s.kronecker_product(vac,vac,s.Matrix([[1,a],[a,1]])/2)
eq('trace_one',s.trace(rho),1)
Gamma=ga/2+2*gp+la/2
d1=signal(evolve(rho));d2=signal(evolve(evolve(rho)))
eq('Schrodinger_z0',signal(rho),a)
eq('Schrodinger_zprime',d1,a*(s.I*w-Gamma))
eq('Schrodinger_zsecond',d2,a*(s.I*w-Gamma)**2-a*g**2+2*s.I*om*(ga+la))
eq('phase_velocity',s.im(d1/a).expand(complex=True),w)
phase2=s.simplify(s.im(s.expand(d2/a-(d1/a)**2)))
eq('phase_acceleration',phase2,2*om*(ga+la)/a)
local={str(x):x for x in [wc,w,g,om,ki,ko,ga,gp,la,a]}
eq('published_second_derivative',d2,s.sympify(source['state_counterexample']['second_derivative'],locals=local))
eq('published_phi_second',phase2,s.sympify(source['state_counterexample']['phase_acceleration_at_zero'],locals=local))
rs=s.Matrix([[3,1],[1,1]])/4;plus=s.ones(2)/2
rdiff=s.kronecker_product(plus-vac,vac,rs)
eq('equal_initial_OH_signal',signal(rdiff),0)
eq('different_initial_derivative',signal(evolve(rdiff)),s.I*g/2-la/8)
x,y,theta=s.symbols('x y theta',real=True);z=x+s.I*y
K=s.Matrix([[0,1],[-1,0]]);P=(I-s.I*K)/2;S=s.cos(theta)*I+s.sin(theta)*K
readout=2*(P*(z*S))[0,0];carrier=s.cos(theta)+s.I*s.sin(theta)
eq('fixed_boundary_reading',readout,z*carrier)
eq('fixed_boundary_decode',s.conjugate(carrier)*readout*S,z*S)
eq('fixed_boundary_reflected_weight',s.conjugate((z*S)[1,0])*(z*S)[1,0],(x*x+y*y)*s.sin(theta)**2)
eq('fixed_boundary_transmitted_weight',s.conjugate((z*S)[0,0])*(z*S)[0,0],(x*x+y*y)*s.cos(theta)**2)
t,wd=s.symbols('t omega_drive',real=True);N=ni+no+ne
R=s.diag(*[s.exp(s.I*wd*t*N[k,k]) for k in range(8)])
h0=h-om*(sp+sm)
hlab=h0+om*(s.exp(-s.I*wd*t)*sp+s.exp(s.I*wd*t)*sm)
hrot=(wc-wd)*(ni+no)+(w-wd)*ne+g*(ai.H*sm+sp*ai)+om*(sp+sm)
eq('lab_to_rot_H_sign',R*hlab*R.H+s.I*R.diff(t)*R.H,hrot)
eq('lab_signal_positive_carrier',R*sp*R.H,s.exp(s.I*wd*t)*sp)
eq('holo_rotation',R*J*R.H,J)
for name,c in [('in',ai),('out',ao),('OH',sm)]:
    eq('loss_rotation_'+name,R*c*R.H,s.exp(-s.I*wd*t)*c)
eq('dephasing_rotation',R*Z*R.H,Z)
result={'status':'PASS','reviewer':'codex-mission-memory-review',
 'time_utc':dt.datetime.now(dt.timezone.utc).isoformat(), 'script':pin(__file__),
 'source_run_checks':34,'independent_checks':len(checks),'checks':checks,
 'pins':pins,'phi_second':str(phase2),'docx_paragraphs':len(paras),
 'extraction_exact':True,'date_scope':'OOXML creation/modification metadata says Jan09; no legal deposit or independent historical timestamp verified.',
 'execution_scope':'Independent exact symbolic matrix checks only; original runner not reexecuted, no provider or numerical evolution.',
 'requirement_satisfied':False}
path=ROOT/'INDEPENDENT_CLOCK_CHECKS_R57.json'
with path.open('xb') as f:f.write((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'result':pin(path),'checks':len(checks),'phi_second':str(phase2)},ensure_ascii=False))
