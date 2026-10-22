"""Exact local Euler residual of the R85 P16; no physical parameter fitting."""
from pathlib import Path
import datetime, hashlib, json, time
import sympy as S

ROOT = Path(__file__).resolve().parent
PLAN = json.loads((ROOT / 'P16_PLAN_R86.json').read_text(encoding='utf-8'))
assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest() == PLAN['script_sha256']
assert not (ROOT / 'P16_RESULT_R86.json').exists()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
t0 = time.monotonic()
x = S.symbols('x0:4', real=True)
zero = dict.fromkeys(x, S.Integer(0))
pairs = [(a,b) for a in range(4) for b in range(a,4)]
v = S.Matrix([1,*x,*[x[a]**2/2 if a==b else x[a]*x[b] for a,b in pairs]])
norm2 = v.dot(v)
z = 1+x[0]
r2 = 4-z*z
# h_eta = d(v/|v|).d(v/|v|); O is constant orthogonal and cancels.
heta = S.Matrix(4,4,lambda a,b: v.diff(x[a]).dot(v.diff(x[b]))/norm2
               - v.dot(v.diff(x[a]))*v.dot(v.diff(x[b]))/norm2**2)
F = r2*heta
F[0,0] += 4/r2
ev = lambda e: S.simplify(e.subs(zero))
F0 = F.applyfunc(ev)
dF = [F.diff(t).applyfunc(ev) for t in x]
ddF = [[F.diff(t).diff(u).applyfunc(ev) for u in x] for t in x]
assert F0 == S.diag(S.Rational(13,3),3,3,3)
# Schur complement: g00=F00-2*b^T*D^-1*b, g0i=-F0i, gij=-Fij.
# At zero b=0; only first derivatives of b enter its second derivative.
g = -F0; g[0,0] = F0[0,0]
dg = [-a for a in dF]
ddg = [[-a for a in row] for row in ddF]
for a in range(4):
    dg[a][0,0] = dF[a][0,0]
    for b in range(4):
        ddg[a][b][0,0] = ddF[a][b][0,0] - S.Rational(4,3)*sum(dF[a][0,i]*dF[b][i,0] for i in range(1,4))
gi = g.inv()
dgi = [-gi*d*gi for d in dg]
Gamma = [[[S.simplify(sum(gi[a,l]*(dg[i][l,j]+dg[j][l,i]-dg[l][i,j])/2 for l in range(4))) for j in range(4)] for a in range(4)] for i in range(4)]
dGamma = [[[[S.simplify(sum((dgi[k][a,l]*(dg[i][l,j]+dg[j][l,i]-dg[l][i,j])
              +gi[a,l]*(ddg[k][i][l,j]+ddg[k][j][l,i]-ddg[k][l][i,j]))/2 for l in range(4)))
              for j in range(4)] for a in range(4)] for i in range(4)] for k in range(4)]
# Kernel convention R_ij=partial_i Gamma_j-partial_j Gamma_i+[Gamma_i,Gamma_j].
Ric = S.Matrix(4,4,lambda b,j: S.simplify(sum(dGamma[a][j][a][b]-dGamma[j][a][a][b]
      +sum(Gamma[a][a][l]*Gamma[j][l][b]-Gamma[j][a][l]*Gamma[a][l][b] for l in range(4)) for a in range(4))))
assert Ric == Ric.T
R = S.simplify(sum(gi[a,b]*Ric[a,b] for a in range(4) for b in range(4)))
Ein = Ric-R*g/2
s = z*z/4
sv = ev(s); c = S.Matrix([ev(S.diff(s,t)) for t in x])
Hess = S.Matrix(4,4,lambda a,b: ev(S.diff(s,x[a],x[b]))-sum(Gamma[a][l][b]*c[l] for l in range(4)))
q = (c.T*gi*c)[0]
boxs = S.simplify(sum(gi[a,b]*Hess[a,b] for a in range(4) for b in range(4)))
y = S.symbols('s', positive=True)
cg, Fc = S.symbols('c_G F_c', positive=True)
A = cg/(4*(1-y)); B = cg/(8*y*(1-y)**2)
E_s = S.simplify((S.diff(A,y)-S.diff(B,y)*q-2*B*boxs).subs(y,sv))
L = S.simplify((A+B*q).subs(y,sv))
Teff = S.simplify(L)*g-2*B.subs(y,sv)*c*c.T
metric_residual = S.simplify(Fc*Ein-Teff/2)
k = S.Matrix([1,S.sqrt(13)/3,0,0])
assert S.simplify((k.T*g*k)[0]) == 0
Rnull = S.simplify((k.T*Ric*k)[0])
Tnull = S.simplify((k.T*Teff*k)[0])
assert Tnull == -4*cg/9
# Compare Hessian volume formula against connection divergence for scalar s.
volume_log_derivative = [S.trace(gi*dg[a])/2 for a in range(4)]
box_divergence = S.simplify(sum(volume_log_derivative[a]*gi[a,b]*c[b]+dgi[a][a,b]*c[b]
                  +gi[a,b]*ev(S.diff(s,x[a],x[b])) for a in range(4) for b in range(4)))
assert box_divergence == boxs
out = {'status':'EXACT_EULER_RESIDUAL_RECORDED','started_utc':started,
 'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-t0,
 'script_sha256':PLAN['script_sha256'],'sympy':S.__version__, 'curvature_convention':'coordinateRicci b j = sum_a (partial_a Gamma_j-partial_j Gamma_a+[Gamma_a,Gamma_j])^a_b',
 'g':str(g),'Ricci':str(Ric),'scalar_curvature':str(R),'Einstein':str(Ein),
 's':str(sv),'q':str(q),'box_s':str(boxs),'scalar_Euler':str(E_s),
 'scalar_stationary_for_positive_cG':bool(E_s==0), 'T_eff':str(Teff),
 'metric_Euler_residual':str(metric_residual),'Ricci_null':str(Rnull),'T_eff_null':str(Tnull),
 'metric_null_residual':str(S.simplify(Fc*Rnull-Tnull/2)),
 'checks':['R85_F_at_origin','Ricci_symmetry','g_null_test','R85_effective_null_source','scalar_box_two_forms'],
 'limits':['Exact local calculation in the specified EH-sigma reduced sector; not full TGL action.',
           'No observed data, beta values or parameter fitting; P16 was chosen for free variations, not stationarity.',
           'The general compact first-variation argument is analytic and must be reviewed independently.']}
with (ROOT/'P16_RESULT_R86.json').open('x',encoding='utf-8') as f: json.dump(out,f,ensure_ascii=False,indent=2)
print(json.dumps(out,ensure_ascii=False))
