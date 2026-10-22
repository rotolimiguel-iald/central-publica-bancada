"""Receive two completed independent reviews and audit against existing engines."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,time,uuid
import sympy as s
from opposite_endpoint_current_engine import external_adjoint
from metric_boundary_current_engine import boundary_current,eh_boundary_vertex_raw
from position_metric_bubble_engine import BASIS

H=Path(__file__).resolve().parent; BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,append=False):
    if p.exists():
        assert append,p
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
        assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old;b=old+b
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(b);assert b and tmp.read_bytes()==b;tmp.replace(p)
def put(p,v):write(p,json.dumps(v,indent=2,ensure_ascii=False).encode('utf-8'))

units=[('mimo','736fc1b7-9efd-4d84-b02c-51691b99c14e','mimo_opposite_endpoint_adjoint_review'),
       ('deepseek','f5fe254c-46c2-4a17-a0f2-9b280d7a3302','deepseek_localized_boundary_review')]
events=[];dirs={}
ledger=OUT/'LEDGER_016.jsonl'
seen={json.loads(l).get('execution_task_id') for l in ledger.read_text('utf-8').splitlines()}
for provider,jid,folder in units:
    D=H/folder;assert not D.exists();D.mkdir();dirs[provider]=D
    source=BASE/'state/handoffs'/f'{jid}_delivery.json'
    data=json.loads(source.read_bytes());j=data['job'];e=j['execution'];r=e['result']
    assert j['stage']=='completed' and j['id']==jid
    assert e['id'] not in seen
    write(D/'RECEIPT.json',source.read_bytes());write(D/'RESPONSE.md',r['text'].encode('utf-8'))
    put(D/'INTAKE.json',dict(at=now.isoformat(),job_id=jid,request_id=j['request_id'],
        execution_task_id=e['id'],source=str(source),receipt_sha256=sha(source),
        scientific_status='DECLARADO_PENDING_LOCAL_AUDIT'))
    accounting=r['request_cost_accounting']
    events.append(dict(at=now.isoformat(),event='INDEPENDENT_REVIEW_RECEIVED',provider=provider,
        target='A7.b',job_id=jid,request_id=j['request_id'],execution_task_id=e['id'],
        usage=r['usage'],cost_estimate_usd=accounting['accounted_usd'],cost_status=accounting['status'],
        provider_elapsed_seconds=r['elapsed_seconds'],receipt_sha256=sha(source),
        response_sha256=sha(D/'RESPONSE.md'),prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),
        remote_call_by_this_script=False))
write(ledger,(''.join(json.dumps(e)+'\n' for e in events)).encode('utf-8'),True)

start=time.process_time();checks=0
def eq(a,b):
    global checks
    assert s.expand(a-b)==0,(a,b);checks+=1
def neq(a,b):
    global checks
    assert s.expand(a-b)!=0,(a,b);checks+=1
x,y=s.symbols('x y');p=s.symbols('p0:4')
lam=(1,-1,0,0);eta=(1,0,0,0)
# Existing operator is applied to nonconstant products, not compared only as syntax.
f=x**3+2*x*y+y**2;g=x**2*y+1
words=[((0,),()),((),(0,)),((0,0),()),((0,1),()),((0,0),(1,)),((0,1),(0,))]
for hw,cw in words:
    out=s.Integer(0)
    for word,coef in external_adjoint(hw,cw,lam,eta).items():
        term=f*g
        for i in word:term=s.diff(term,[x,y][i])
        out+=coef*term
    direct=f*g
    for i in hw:direct=-s.diff(direct,[x,y][i])-lam[i]*direct
    for i in cw:direct=s.diff(direct,[x,y][i])-eta[i]*direct
    eq(out,direct)
eq(s.diff(f*g,x,2),s.diff(f,x,2)*g+2*s.diff(f,x)*s.diff(g,x)+f*s.diff(g,x,2))
neq(s.diff(f*g,x)-eta[0]*f*g,s.diff(f*g,x)+eta[0]*f*g)
neq(s.diff(f*g,x,2)+2*lam[0]*s.diff(f*g,x)+lam[0]**2*f*g,
    2*lam[0]*s.diff(f*g,x)+lam[0]**2*f*g)
mimo=dict(at=now.isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 accepted='Adjoint (-1)^|I|(d+lambda)^I(d-eta)^J and endpoint/Wick signs agree with existing engine; polynomial product controls including repeated/mixed derivatives pass',
 qualification='Equalities in response section6 must carry the adjoint symbol; original derivative is not literally its adjoint. Checkmarks in model output are not executed tests.',
 existing_evidence=str(H/'opposite_endpoint_current/results.json'),new_engine_required=False,
 scientific_scope='Formal adjunction and given propagator conventions; no full diagram or Q2 theorem',full_Q2=False,gate_changed=False)
put(dirs['mimo']/'local_audit.json',mimo)

start=time.process_time();checks=0
p0=(1,2,-1,1);q0=(2,-1,0,3);r0=(0,1,1,0);s0=(-1,0,2,1)
fields=((BASIS[0],p0),(BASIS[4],q0),(BASIS[0],r0),(BASIS[0],s0))
bc=boundary_current(*fields)
Q=tuple(sum(v[i] for _,v in fields) for i in range(4))
raw=eh_boundary_vertex_raw(*fields);qdot=sum(a*b for a,b in zip(Q,bc))
eq(F(raw,16),qdot);eq(qdot,F(-9,8));eq(raw,-18)
qzero=tuple(-p0[i]-r0[i]-s0[i] for i in range(4))
zero_fields=(fields[0],(fields[1][0],qzero),fields[2],fields[3])
eq(eh_boundary_vertex_raw(*zero_fields),0)
neq(sum(t*t for t in boundary_current(*zero_fields)),0)
# On [0,1], chi and its first derivative vanish at both ends. No surface flux.
# Moving a second derivative changes bulk jet placement while the integral survives.
t=s.Symbol('t',real=True);chi=t**2*(1-t)**2;B=t**2
before=-s.integrate(chi*s.diff(B,t),(t,0,1))
after=s.integrate(s.diff(chi,t)*B,(t,0,1))
surface=(chi*B).subs(t,1)-(chi*B).subs(t,0)
eq(surface,0);eq(before,after);eq(before,-s.Rational(1,30))
# Both Fourier i factors must be included when b denotes B with i removed.
q,b,k=s.symbols('q b k',nonzero=True)
eq(-s.I*q*(s.I*b)/(2*k),q*b/(2*k))
deep=dict(at=now.isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 accepted=['Boundary current B4 has one derivative; unintegrated divergence activates W20/W02/W11',
           'After moving divergence onto cutoff, the representative has at most first jets of W'],
 corrections=['Second jets are redistributed to cutoff derivatives by IBP, not located entirely in a nonzero physical surface term',
              'With compact support/no physical surface, Q=0 raw Fourier divergence is identically zero; the proposed boundary profile changes the domain and is not the requested rational control',
              'Quartic engine is GammaGamma only, not full EH; add boundary engine explicitly',
              'Response mixes B with i removed and full B; normalized contracted raw/16 is Q.dot(b), not raw -16 div(B) without the final normalization'],
 controls=dict(boundary_current=list(map(str,bc)),total_momentum=Q,raw=str(raw),normalized=str(qdot),
               zero_total_momentum_raw='0',compact_support_surface=str(surface),
               compact_support_integral_before=str(before),compact_support_integral_after=str(after)),
 conclusion='Derivative-order organization retained; normalization and surface interpretation corrected. Existing local boundary-jet result remains authoritative.',
 existing_evidence=str(H/'localized_tadpole_boundary_jets_v2/results.json'),full_Q2=False,gate_changed=False)
put(dirs['deepseek']/'local_audit.json',deep)
for provider,D in dirs.items():
    paths=[Path(__file__),D/'RECEIPT.json',D/'RESPONSE.md',D/'INTAKE.json',D/'local_audit.json']
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths]))
print(json.dumps(dict(mimo=mimo,deepseek=deep),ensure_ascii=False))
