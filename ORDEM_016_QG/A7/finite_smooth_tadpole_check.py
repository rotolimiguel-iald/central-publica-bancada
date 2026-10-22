"""Finite constant smooth metric contraction of the existing quartic EH vertex."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,time
import sympy as s
from metric_principal_vertices import gamma2,clear_caches
from metric_quartic_vertices import second_coefficient_4,eh_quartic_32k
from position_metric_bubble_engine import BASIS,LABELS
H=Path(__file__).resolve().parent;D=H/'finite_smooth_tadpole';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):
 p=D/n;assert not p.exists(),p
 b=json.dumps(v,ensure_ascii=False,indent=2).encode();t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
inputs=[Path(__file__),H/'metric_quartic_vertices.py',H/'metric_principal_vertices.py',H/'flat_mixed_smooth_bubble/results.json']
save('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Quartic finite smooth tadpole, constant W_I/W_T; compare signs without choosing T1 normalization',
 normalization='GH=4k/(4pi²)(S0/z+W); V4=raw/(32k); tad=raw_contraction/(16*4pi²)',
 real_symbol_units='Divide by CE/(4pi²)^2, CE=-4pi²; Fourier p²->-q² cancels ratio -1',
 excluded=['Variable first/second W jets','Curvature','T1 prescription choice','Full Q2'],
 sources=[dict(path=str(p),sha256=sha(p)) for p in inputs]))
start=time.process_time();checks=0
def eq(a,b=0):
 global checks
 assert s.expand(a-b)==0,(a,b);checks+=1
def delta(i,j):return int(i==j)
def weights(sector):
 out=[]
 for a,(i,j) in enumerate(LABELS):
  for b,(k,l) in enumerate(LABELS):
   w=F(delta(i,k)*delta(j,l)+delta(i,l)*delta(j,k),2) if sector=='metric_I' else F(delta(i,j)*delta(k,l))
   if w:out.append((a,b,w))
 return out
zero=(0,0,0,0)
def tad(A,B,p,entries):
 G=gamma2(A,tuple(p));T=gamma2(B,tuple(-v for v in p))
 return sum((w*(second_coefficient_4(BASIS[a],BASIS[b],G,T)+second_coefficient_4(BASIS[a],BASIS[b],T,G)) for a,b,w in entries),F())/16
def invariants(A,B,p):
 A=s.Matrix(4,4,A);B=s.Matrix(4,4,B);p=s.Matrix(p);p2=p.dot(p)
 return [p2*s.trace(A*B),p2*s.trace(A)*s.trace(B),(p.T*A*p)[0]*s.trace(B)+(p.T*B*p)[0]*s.trace(A),(p.T*A*B*p)[0]]
records={};p0=(1,0,0,0)
for sector in ('metric_I','metric_T'):
 entries=weights(sector);rows=[];ys=[]
 for a,A in enumerate(BASIS):
  for B in BASIS[a:]:rows.append(invariants(A,B,p0));ys.append(s.Rational(tad(A,B,p0,entries)))
  clear_caches()
 sol,par=s.Matrix(rows).gauss_jordan_solve(s.Matrix(ys));assert not len(par)
 for row,y in zip(rows,ys):eq(sum(u*v for u,v in zip(row,sol)),y)
 for a,b,p in [(0,4,(1,2,-1,1)),(1,1,(2,-1,0,3)),(0,0,(1,0,0,0))]:
  A=BASIS[a];B=BASIS[b];value=tad(A,B,p,entries)
  eq(value,sum(u*v for u,v in zip(invariants(A,B,p),sol)))
  full=sum((w*eh_quartic_32k((A,p),(B,tuple(-u for u in p)),(BASIS[i],zero),(BASIS[j],zero)) for i,j,w in entries),F())/16
  eq(value,full);clear_caches()
 records[sector]=dict(coefficients_over_hbar_by_4pi2=list(map(str,sol)))
 print('TAD',sector,records[sector],time.process_time()-start,flush=True)
# A scalar comparison parameter labels inclusion; it is not adjusted to cancel Ward.
q=s.Matrix(s.symbols('q0:4'));v=s.Matrix(s.symbols('v0:4'));I=s.eye(4);q2=q.dot(q);gv=q*v.T+v*q.T
def N(coeff,h):
 a,b,c,d=map(s.Rational,coeff)
 return a*q2*h+b*q2*s.trace(h)*I+c*(q*q.T*s.trace(h)+I*(q.T*h*q)[0])+d*(q*(h*q).T+(h*q)*q.T)/2
def E(h):
 C=h*q-q*s.trace(h)/2
 return -q2*h+I*q2*s.trace(h)/2+q*C.T+C*q.T-I*q.dot(C)
old=json.loads((H/'flat_mixed_smooth_bubble/results.json').read_bytes())['sectors']
for sector,rec in records.items():
 la=-s.Rational(1,2);lb=-s.Rational(1,8) if sector=='metric_I' else s.Rational(1,4)
 with_tad=N(old[sector]['coefficients'],gv)+E(la*gv+lb*I*s.trace(gv))+N(rec['coefficients_over_hbar_by_4pi2'],gv)
 residue=[dict(a=a,b=b,value=str(s.expand(with_tad[a,b]))) for a in range(4) for b in range(a,4) if s.expand(with_tad[a,b])!=0]
 rec['same_units_Ward_with_tad_nonzero']=residue
 rec['cancels_existing_contact_residue']=not residue
 # Fit invariant Ward basis independently of component axis samples.
 aa,bb,cc=s.symbols('a b c');ans=aa*I*q2*q.dot(v)+bb*q2*gv+cc*q*q.T*q.dot(v)
 equations=[]
 for a in range(4):
  for b in range(4):equations.extend(s.Poly(s.expand(with_tad[a,b]-ans[a,b]),*q,*v).coeffs())
 fit=s.solve(equations,(aa,bb,cc),dict=True);assert len(fit)==1
 for z in equations:eq(z.subs(fit[0]))
 rec['Ward_with_tad_coefficients']=[str(fit[0][z]) for z in (aa,bb,cc)]
results=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 sectors=records,normalization_verified_algebraically=True,T1_selected=False,
 comparison='Tadpole included as an explicit optional contraction/transport contribution; no change to T1 prescription',
 full_Q2=False,gate_changed=False)
save('results.json',results);save('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(results))
