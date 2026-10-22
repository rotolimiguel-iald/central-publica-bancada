"""Extract the complete O4 external-jet bases of the endpoint regulator defects."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,time,uuid
import sympy as s
import bilocal_Y_regulator_engine as E
H=Path(__file__).resolve().parent;D=H/'bilocal_Y_regulator';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p;b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
source=H/'bilocal_full_external_pair_check.py'
tree=ast.parse(source.read_text('utf-8'));defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('d','f3','f4')]
a,L=s.symbols('a L');ns=dict(s=s,L=L,n=(1,0,0,0))
exec(compile(ast.Module(body=defs,type_ignores=[]),str(source),'exec'),ns)
inputs=[Path(__file__),H/'bilocal_Y_regulator_engine.py',source,H/'bilocal_regulator_contact/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Full O4 coefficients of the Y regulator defect before integration of external DhX',
    prescription='FP_a[(1-a)mu^(2a)(rho²)^a] AND comparison with coordinate w^a; neither chosen to impose Ward',
    regulator_jets='fYi=-2xi/z; fYiYj=2delta/z-4xixj/z² -2K/3(delta-xixj/z)',
    fields='a and a² coefficients including log L; geometric Hessian increment stored separately',
    scope='FirstK Euclidean reference; not full Q2, not its local class',
    sources=[dict(path=str(p),sha256=sha(p)) for p in inputs],full_Q2=False))
cpu=time.process_time();checks=0;output={}
def poly(rows):return s.expand(sum(a**(i+1)*sum(s.Rational(v)*L**ell for ell,v in enumerate(row)) for i,row in enumerate(rows)))
for kind,cls in [('ghost',E.BG.PointJets),('metric',E.BM.MetricPointJets)]:
    J=cls((1,0,0,0));cache={}
    def values(der,b,c):
        b,c=sorted((b,c));key=(der,b,c)
        if key not in cache:
            raw,geom,_=E.loop_defect_point(kind,J.point,E.BG.tensor(b,c),der,J)
            val=[[poly(raw[o][r]) for r in range(4)] for o in (0,1)]
            inc=[[a*sum(s.Rational(v)*L**ell for ell,v in enumerate(geom[o][r])) for r in range(4)] for o in (0,1)]
            cache[key]=(val,inc)
            put(kind+'_jet_'+str(der)+'_'+str(b)+str(c)+'.json',dict(values=[[str(t) for t in row] for row in val],
                 geometric_increment=[[str(t) for t in row] for row in inc],cpu_cumulative=time.process_time()-cpu))
            print('JET',kind,key,'cpu',time.process_time()-cpu,flush=True)
        m=1 if b==c else 2
        return [[[v/m for v in row] for row in branch] for branch in cache[key]]
    tables={}
    for branch,name in [(0,'geodesic'),(1,'geometric_increment')]:
        def v(der,b,c,r,o):return values(der,b,c)[branch][o][r]
        c0=[];c1=[]
        for o in (0,1):
            u=v(None,1,1,0,o);w=v(None,0,1,1,o);t=v(None,0,0,0,o)-u-2*w;c0.append([u,w,t])
            u=v(1,2,2,1,o);w=v(1,1,2,2,o)
            v2=v(0,1,1,0,o)-u;v3=v(1,0,0,1,o)-u
            v4=v(1,1,0,0,o)-w;v5=v(0,1,0,1,o)-w
            v6=v(0,0,0,0,o)-u-2*w-v2-v3-2*v4-2*v5
            c1.append(list(map(s.expand,[u,w,v2,v3,v4,v5,v6])))
        for (der,b,c),(val,inc) in cache.items():
            for o in (0,1):
                for r in range(4):
                    got=(val if branch==0 else inc)[o][r]/(1 if b==c else 2)
                    want=ns['f3'](c0[o],b,c,r) if der is None else ns['f4'](c1[o],der,b,c,r)
                    assert s.expand(got-want)==0,(kind,name,der,b,c,r,o,got,want);checks+=1
        tables[name]=dict(C0=[[str(s.expand(v)) for v in row] for row in c0],C1=[[str(s.expand(v)) for v in row] for row in c1])
    output[kind]=tables
    put(kind+'_basis.json',tables)
J=E.SourceYDefect((1,0,0,0));sc=[]
for o in (0,1):
    u=J.regulator_coefficient(o,1,1,0);v=J.regulator_coefficient(o,0,1,1)
    w=J.regulator_coefficient(o,0,0,0)-u-2*v
    sc.append([str(s.expand(a*t)) for t in (u,v,w)])
    print('SOURCE',o,sc[-1],'cpu',time.process_time()-cpu,flush=True)
result=dict(at=datetime.now(timezone.utc).isoformat(),status='Y_REGULATOR_EXTERNAL_JET_DEFECTS_MEASURED',
    checks=checks,cpu_seconds=time.process_time()-cpu,loop_coefficients=output,source_coefficients=sc,
    coordinate_completion='geodesic minus geometric_increment; source first derivative unchanged',
    full_Q2=False,extended_contact_not_yet_summed=True)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json',D/'ghost_basis.json',D/'metric_basis.json']]))
print(json.dumps(result))
