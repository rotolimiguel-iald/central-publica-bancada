"""Check Wick conjugation and the algebraic smooth-source companion.

No choice of state, no new diagram or claim of full Ward cancellation.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
H=Path(__file__).resolve().parent;D=H/'smooth_reference_transport_audit';D.mkdir(exist_ok=True)
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
source=BASE/'state/handoffs/47073144-af8e-4f96-9300-390d12bbaa3a_delivery.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,obj):
    p=D/name;assert not p.exists(),p
    raw=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);tmp.write_bytes(raw)
    assert tmp.read_bytes()==raw;tmp.replace(p)
packet=json.loads(source.read_bytes());response=packet['result']['text']
p=D/'KIMI_RESPONSE.md';assert not p.exists();tmp=p.with_suffix('.tmp');tmp.write_text(response,encoding='utf-8');assert tmp.read_text('utf-8')==response;tmp.replace(p)
put('RECEIPT.json',dict(at=datetime.now(timezone.utc).isoformat(),job_id=packet['job_id'],
    execution_task_id=packet['execution_task_id'],stage=packet['stage'],source_sha256=sha(source),
    response_sha256=sha(p),usage=packet['result']['usage'],model=packet['result'].get('model'),
    cost_estimate_usd=None,cost_status='SUBSCRIPTION_COST_NOT_ALLOCATED_UNKNOWN_NOT_ZERO'))
inputs=[Path(__file__),H/'smooth_source_contact_check.py',H/'smooth_source_contact/results.json',p]
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Wick transport conjugation; smooth-source factorization and its canonical BRST companion',
    limitations=['Not full W-dependent metric/ghost diagrams','No physical Hadamard state constructed',
                 'W at coincidence arbitrary algebraic tensor, not presumed bisolution'],
    sources=[dict(path=str(p),sha256=sha(p)) for p in inputs],full_Q2=False))
cpu=time.process_time();checks=[];neg=[]
def ck(name,expr):
    assert s.expand(expr)==0,(name,s.expand(expr));checks.append(name)

# A finite polynomial model exactly tests the stated exponential conjugation.
x,h,D0,W0=s.symbols('x h D W')
def alpha(f,w):
    degree=s.degree(f,x) if f else 0
    return s.expand(sum((h*w/2)**k/s.factorial(k)*s.diff(f,x,2*k)
                        for k in range(int(degree)//2+1)))
def product(f,g,d):
    degree=min(s.degree(f,x),s.degree(g,x)) if f and g else 0
    return s.expand(sum((h*d)**k/s.factorial(k)*s.diff(f,x,k)*s.diff(g,x,k)
                        for k in range(int(degree)+1)))
for m in range(5):
    for n in range(5):
        f,g=x**m,x**n
        correct=alpha(product(alpha(f,-W0),alpha(g,-W0),D0),W0)
        ck(('Wick_conjugation',m,n),correct-product(f,g,D0+W0))
bad=product(alpha(x,W0),alpha(x,W0),D0)-product(x,x,D0+W0)
assert s.expand(bad)==-h*W0
neg.append(dict(name='Kimi_input_only_alpha_not_conjugation',residual=str(bad)))

# The source coefficient for a general symmetric W_{ab|cd} at coincidence.
labels=[(a,b) for a in range(4) for b in range(a,4)]
index={v:i for i,v in enumerate(labels)}
ws=s.symbols('w0:55');wmap={};k=0
for i in range(10):
    for j in range(i,10):wmap[i,j]=ws[k];k+=1
def w(a,b,c,d):
    i,j=sorted((index[tuple(sorted((a,b)))],index[tuple(sorted((c,d)))]))
    return wmap[i,j]
S=s.Matrix(4,4,lambda a,r:sum(w(a,m,r,m) for m in range(4)))
def R(a,b,j,r):
    return -(int(j==b)*S[a,r]+int(j==a)*S[b,r]
              +w(a,j,b,r)+w(b,j,a,r)-2*w(a,b,j,r))/4
for a in range(4):
    for b in range(4):
        for j in range(4):
            for r in range(4):
                defect=-(int(j==b)*S[a,r]+int(j==a)*S[b,r]
                    -int(r==b)*S[a,j]-int(r==a)*S[b,j])/4
                ck(('antisymmetric_derivative',a,b,j,r),R(a,b,j,r)-R(a,b,r,j)-defect)

# Kernel of the defect as a linear map on a general symmetric 4x4 S.
ss=s.symbols('s0:10');sm=s.Matrix(4,4,lambda a,b:ss[index[tuple(sorted((a,b)))]])
defects=[-(int(j==b)*sm[a,r]+int(j==a)*sm[b,r]
           -int(r==b)*sm[a,j]-int(r==a)*sm[b,j])/4
         for a in range(4) for b in range(4) for j in range(4) for r in range(4)]
matrix,_=s.linear_eq_to_matrix(defects,ss);kernel=matrix.nullspace()
assert matrix.rank()==9 and len(kernel)==1
identity=s.Matrix([int(a==b) for a,b in labels])
assert matrix*identity==s.zeros(256,1)
checks.append('defect_rank9_kernel_scalar_identity')

# Concrete symmetric smooth jet W=H tensor H with H=diag(1,0,0,0).
sub={wmap[i,j]:s.Integer(labels[i]==(0,0) and labels[j]==(0,0))
     for i in range(10) for j in range(i,10)}
counter=s.expand((R(0,1,1,0)-R(0,1,0,1)).subs(sub))
assert counter==-s.Rational(1,4)
neg.append(dict(name='generic_anisotropic_W_does_not_factor_through_G',
    component='ab01, (j,r)=(1,0) minus (0,1)',residual=str(counter),
    physical_state_claim=False))

# Isotropic W: construct the actual algebraic field redefinition L_W.
wI,wT=s.symbols('wI wT')
def iso(a,b,c,d):return wI*(int(a==c)*int(b==d)+int(a==d)*int(b==c))/2+wT*int(a==b)*int(c==d)
isosub={wmap[i,j]:iso(*labels[i],*labels[j]) for i in range(10) for j in range(i,10)}
p=s.Matrix(s.symbols('p0:4'));I=s.eye(4)
la=-(wI+wT)/2;lb=-wI/8+wT/4
def L(v):return la*v+lb*I*s.trace(v)
def G(v):return p*v.T+v*p.T
def E(v):
    cv=v*p-p*s.trace(v)/2
    return -p.dot(p)*v+I*p.dot(p)*s.trace(v)/2+p*cv.T+cv*p.T-I*p.dot(cv)
examples=[]
for r in range(4):
    v=I[:,r];rv=s.Matrix(4,4,lambda a,b:sum(R(a,b,j,r).subs(isosub)*p[j] for j in range(4)))
    for a in range(4):
        for b in range(4):
            ck(('isotropic_factor',r,a,b),rv[a,b]-L(G(v))[a,b])
            ck(('Einstein_G',r,a,b),E(G(v))[a,b])
    ng=E(L(G(v)))+L(E(G(v)))
    er=E(rv)
    for a in range(4):
        for b in range(4):ck(('companion_Ward',r,a,b),ng[a,b]-er[a,b])
    if r==1:
        nonclosed=s.expand(er[0,1].subs({p[0]:1,p[1]:0,p[2]:0,p[3]:0,wI:1,wT:0}))
        # This component can vanish; use the whole tensor and record any nonzero
        # coefficient if one exists rather than infer non-exactness from N alone.
        examples.append(dict(component_01=str(nonclosed),source_s0_operator=str(er)))

result=dict(at=datetime.now(timezone.utc).isoformat(),status='WICK_CONJUGATION_AND_SMOOTH_SOURCE_FACTOR_TESTED',
    checks=len(checks),cpu_seconds=time.process_time()-cpu,negative_controls=neg,
    partial_trace_obstruction='R_ab^(jr)-R_ab^(rj)=-(delta_jb S_ar+delta_ja S_br-delta_rb S_aj-delta_ra S_bj)/4',
    factor_condition='S_ar=sum_m W_am|rm is scalar; kernel rank9 on Sym2(R4)',
    isotropic_L_coefficients=[str(la),str(lb)],
    canonical_generator='F_W=integral hdagger.L_W h, ghost number -1',
    action_companion='s0 F_W=integral (E h).L_W h - hdagger.L_W Gc; ghost number 0',
    companion_metric_hessian='N_W=E L_W+L_W E',
    scope='Constructed BRST-exact action-level pair; not a computed sum of smooth loop diagrams, not the ghost-number1 anomaly',
    source_nonzero_does_not_decide_cohomology=True,full_Q2=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p))
    for p in inputs+[D/'PRE_REGISTER.json',D/'results.json',D/'RECEIPT.json']]))
print(json.dumps(result))
