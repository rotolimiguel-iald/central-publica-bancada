from pathlib import Path
import sympy as S
import json,hashlib,datetime
root=Path(__file__).resolve().parent
plan=json.loads((root/'EXACT_RANK_PLAN_R85.json').read_text(encoding='utf-8'))
assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==plan['script_sha256']
assert not (root/'EXACT_RANK_RESULT_R85.json').exists()
x=S.symbols('x0:4',real=True); z=dict.fromkeys(x,S.Integer(0)); pairs=[(a,b) for a in range(4) for b in range(a,4)]
qs=[x[a]**2/2 if a==b else x[a]*x[b] for a,b in pairs]
v=S.Matrix([1,*x,*qs]); eta=v/S.sqrt((v.T*v)[0]);s=1+x[0];r=S.sqrt(4-s*s)
psi=S.Matrix([s,*list(r*eta)])
d=[psi.diff(t).subs(z).applyfunc(S.simplify) for t in x]
F=S.Matrix(4,4,lambda a,b:S.simplify(d[a].dot(d[b])))
c=S.Matrix([S.Rational(1,2),0,0,0]);q=(c.T*F.inv()*c)[0];u=F.inv()*c
g=2*c*c.T/q-F
II=S.Matrix(10,10,lambda row,col:S.simplify(S.diff(psi[6+col],x[pairs[row][0]],x[pairs[row][1]]).subs(z)/S.sqrt(3)))
L=S.zeros(10,10)
for col,(a,b) in enumerate(pairs):
 H=S.zeros(4);H[a,b]=-2;H[b,a]=-2
 D=-H+2*c*c.T*(u.T*H*u)[0]/q**2
 for row,(i,j) in enumerate(pairs):L[row,col]=S.simplify(D[i,j])
assert F==S.diag(S.Rational(13,3),3,3,3)
assert g==S.diag(S.Rational(13,3),-3,-3,-3)
assert II==S.eye(10)
assert L==S.diag(-2,*([2]*9)) and L.det()==-1024 and L.rank()==10
assert (L/2)**2==S.eye(10)
p=[S.Rational(1,4)]+[S.Rational(1,20)]*15
assert sum(p)==1 and min(p)>0
out={'status':'PASS_EXACT_RANK','method':'SymPy exact derivatives at x=0; normal-frame fields and compact lifting proved in accompanying text, not numerically inferred','sympy':S.__version__,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script_sha256':plan['script_sha256'],'variables':list(map(str,x)),'pair_order':pairs,'probabilities_at_zero':list(map(str,p)),'F_at_zero':str(F),'g_at_zero':str(g),'clock_q':str(q),'II_matrix':str(II),'normal_to_metric_matrix':str(L),'rank':int(L.rank()),'determinant':str(L.det()),'checks':['positive_normalized_P16','independent_differential_rank4','ten_independent_normal_second_forms','normal_to_metric_rank10','fixed_clock_metric_derivative_involution'],'limits':['No numerical data, beta fitting, Lean or independent stationarity conclusion.','Rotation to positive coordinates preserves all Gram/curvature expressions; Householder proof is analytic.']}
with (root/'EXACT_RANK_RESULT_R85.json').open('xb') as f:f.write((json.dumps(out,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps(out,ensure_ascii=False))
