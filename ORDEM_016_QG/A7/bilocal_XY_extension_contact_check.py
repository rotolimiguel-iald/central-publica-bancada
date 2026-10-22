"""Assemble X and Y regulator contacts of the computed singular hc pair.

Both distance completions are retained. No counterterm is selected here.
"""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
import ast,hashlib,json,time,uuid
import sympy as s
import einstein_radial_aux_engine as E
import logarithmic_contact_engine as R
H=Path(__file__).resolve().parent;D=H/'bilocal_XY_extension_contact';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p;b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
input_y=H/'bilocal_Y_regulator/results.json';input_x=H/'bilocal_X_extension_contact/results.json'
data=json.loads(input_y.read_bytes());old=json.loads(input_x.read_bytes())
bulk_script=H/'bilocal_bulk_ward_closure_check.py';contact_script=H/'bilocal_X_extension_contact_check.py'
inputs=[input_y,input_x,bulk_script,contact_script,H/'einstein_radial_aux_engine.py',Path(__file__)]
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Full sum of regulator derivative contacts for the existing singular pair+source through O(K)',
    formula='Xstage + FP_a(1-a)z^a[deltaC0-divXdeltaC1-2a x_i deltaC1_i/z+E_a deltaSource]',
    prescription='Two predeclared completions rho² and coordinate w; report both',
    poles='ell0 uses coefficient a; ell1 uses coefficient a minus coefficient a²',
    exclusions=['smooth W','other local diagrams/tadpoles','K²','higher arities','Lorentzian i0'],
    sources=[dict(path=str(p),sha256=sha(p)) for p in inputs],full_Q2=False))
cpu=time.process_time();a,L=s.symbols('a L');x=E.x;z=E.radial_z;Q=R.Q
def load_functions(p,names,ns):
    tree=ast.parse(p.read_text('utf-8'))
    defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert len(defs)==len(names),(p,names)
    exec(compile(ast.Module(body=defs,type_ignores=[]),str(p),'exec'),ns)
res_ns=dict(s=s,R=R,x=x,z=z,Q=Q,lru_cache=lru_cache,checked=set())
load_functions(contact_script,{'sphere_monomial','radial_residue','contact'},res_ns)
contact=res_ns['contact']
def parse(v):return s.sympify(v,locals={'a':a,'L':L})
sc=[[parse(v) for v in row] for row in data['source_coefficients']]
src_ns=dict(s=s,x=x,z=z,sc=sc)
load_functions(contact_script,{'de','frame','source_field'},src_ns)
source_images={}
for r in range(4):
    image=E.einstein([src_ns['source_field'](o,r) for o in (0,1)],[2*a*xx/z for xx in x])
    first=image[1]+s.Matrix(4,4,lambda i,j:sum(src_ns['frame'](i,t)*image[0][t,j]+src_ns['frame'](j,t)*image[0][i,t] for t in range(4)))
    source_images[r]=[image[0],first.applyfunc(s.expand)]
    print('SOURCE',r,'cpu',time.process_time()-cpu,flush=True)
def fp_local(f):
    pol=s.Poly(s.expand(f),a,L)
    assert pol.coeff_monomial(1)==0,'The new defect must vanish at a=0'
    assert all(pa>=1 and pl<=1 for (pa,pl),val in pol.terms() if val),pol
    effective=pol.coeff_monomial(a)+pol.coeff_monomial(a*L)-pol.coeff_monomial(a*a*L)
    return contact(s.expand(effective))
all_values={};coeffs={};checks=[];log_controls=[]
for mode in ['geodesic','coordinate']:
    def table(kind,key):
        raw=data['loop_coefficients'][kind]
        return [[parse(raw['geodesic'][key][o][i])-(parse(raw['geometric_increment'][key][o][i]) if mode=='coordinate' else 0)
                 for i in range(len(raw['geodesic'][key][o]))] for o in (0,1)]
    g0,g1=table('ghost','C0'),table('ghost','C1');m0,m1=table('metric','C0'),table('metric','C1')
    c0=[[g0[o][i]-m0[o][i]/2 for i in range(3)] for o in (0,1)]
    c1=[[g1[o][i]-m1[o][i]/2 for i in range(7)] for o in (0,1)]
    ns=dict(s=s,x=x,z=z,L=L,c0=c0,c1=c1,lru_cache=lru_cache)
    load_functions(bulk_script,{'delta','dx','frame','gamma','rank3','rank4','coordinate_tensor','coordinate_divergence','frame_divergence'},ns)
    values={};y_values={}
    for r in range(4):
        density=[]
        for o in (0,1):
            density.append(s.Matrix(4,4,lambda i,j:s.expand(
                ns['rank3'](o,i,j,r)-ns['frame_divergence'](o,i,j,r)
                -2*a*sum(x[k]*ns['rank4'](o,k,i,j,r) for k in range(4))/z
                +source_images[r][o][i,j])))
        weighted=[density[0],(density[1]-z*density[0]/2).applyfunc(s.expand)]
        for o in (0,1):
            for i in range(4):
                for j in range(4):
                    yy=fp_local(weighted[o][i,j]);key=str((o,i,j,r))
                    total=s.expand(yy+parse(old['values'][key]))
                    values[key]=str(total);y_values[key]=str(yy);checks.append([mode,o,i,j,r])
                    if mode=='geodesic' and (i,j,r)==(1,1,0):
                        naive=contact(s.expand(weighted[o][i,j]).coeff(a,1).subs(L,0))
                        if s.expand(yy-naive)!=0:
                            log_controls.append(dict(order=o,name='discard_logs_before_finite_part',residual_over_C=str(s.expand(yy-naive))))
        print('CONTACT',mode,r,'cpu',time.process_time()-cpu,flush=True)
    cs=[];q2=sum(q*q for q in Q)
    for o in (0,1):
        u,v,w=s.symbols('u v w');power=2-o;eqs=[]
        def pred(i,j,r):
            return u*int(i==j)*Q[r]*q2**power+v*(int(i==r)*Q[j]+int(j==r)*Q[i])*q2**power+w*Q[i]*Q[j]*Q[r]*q2**(power-1)
        for i,j,r in [(1,1,0),(0,1,1),(0,0,0)]:eqs+=s.Poly(s.expand(pred(i,j,r)-parse(values[str((o,i,j,r))])),*Q).coeffs()
        sols=s.solve(eqs,(u,v,w),dict=True);assert len(sols)==1,sols
        cs.append([str(sols[0][q]) for q in (u,v,w)])
        for i in range(4):
            for j in range(4):
                for r in range(4):
                    assert s.expand(pred(i,j,r).subs(sols[0])-parse(values[str((o,i,j,r))]))==0
                    checks.append([mode,'isotropy',o,i,j,r])
    coeffs[mode]=cs;all_values[mode]=dict(total=values,Y_addition=y_values)
    put(mode+'_values.json',all_values[mode])
diff=[[str(s.expand(parse(coeffs['geodesic'][o][j])-parse(coeffs['coordinate'][o][j]))) for j in range(3)] for o in (0,1)]
result=dict(at=datetime.now(timezone.utc).isoformat(),status='SINGULAR_PAIR_XY_EXTENSION_CONTACT_MEASURED',
    checks=len(checks),residue_monomials_checked=len(res_ns['checked']),cpu_seconds=time.process_time()-cpu,
    coefficients_over_C_E=coeffs,geodesic_minus_coordinate=diff,C_E='-4pi²',
    invariant_basis=old['invariant_basis'],log_controls=log_controls,
    includes='All Y regulator corrections represented in loop h/Dh jets and source; X divergence and Einstein commutator; volume firstK',
    full_Q2=False,smooth_W=False,tadpoles=False,nonlinear_arities=False,lorentzian_i0=False,
    prescription_changed=False,distance_completion_selected=False,
    caveat='Pair+source singular reference through O(K), not all local diagrams nor the full QME anomaly')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json',D/'geodesic_values.json',D/'coordinate_values.json']]))
print(json.dumps(result))
