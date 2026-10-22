"""Exact same-P geometry check; symbolic verification, not a Lean theorem or EOM."""
from pathlib import Path
import json, hashlib, datetime, time, traceback, sys
import sympy as s

ROOT = Path(__file__).resolve().parent

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def pin(p):
    p = Path(p)
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}

def new(name, value):
    with (ROOT/name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')

def simp(x):
    return s.factor(s.trigsimp(s.simplify(s.expand_trig(x))))

def main():
    freeze = json.loads((ROOT/'PREEXEC_PINS_R84.json').read_text(encoding='utf-8'))
    for item in freeze['evidence']:
        assert pin(item['path'])['sha256'] == item['sha256'], item['path']
    start, tick = now(), time.perf_counter()
    new('START_GEOMETRY_R84.json', {'started_utc':start, 'command':sys.argv,
        'python':sys.version, 'sympy':s.__version__, 'freeze':pin(ROOT/'PREEXEC_PINS_R84.json')})
    checks = []
    def check(name, expressions):
        residuals = [simp(e) for e in expressions]
        ok = all(e == 0 for e in residuals)
        checks.append({'name':name, 'passed':ok, 'residuals':[str(e) for e in residuals]})
        print(name, 'PASS' if ok else 'FAIL', flush=True)
        if not ok:
            raise AssertionError(checks[-1])
    try:
        t, th, ch, ps = coords = s.symbols('tau theta chi psi', real=True)
        a = 2*s.cos(t/2)
        phi = s.Matrix([s.cos(th)/s.sqrt(3), s.sin(th)/s.sqrt(3),
            s.sqrt(s.Rational(2,3))*s.sin(ch)*s.cos(ps),
            s.sqrt(s.Rational(2,3))*s.sin(ch)*s.sin(ps),
            s.sqrt(s.Rational(2,3))*s.cos(ch)])
        P = s.Matrix([s.sin(t/2)**2]+[s.cos(t/2)**2*f*f for f in phi])
        D = P.jacobian(coords)
        fisher = (D.T*s.diag(*[1/p for p in P])*D).applyfunc(simp)
        check('probabilities_normalized', [sum(P)-1, sum(f*f for f in phi)-1])
        check('conditional_potentials_squared', [P[j+1]/(1-P[0])-phi[j]**2 for j in range(5)])
        expected_fisher = s.diag(1,a*a/3,2*a*a/3,2*a*a*s.sin(ch)**2/3)
        check('fisher_derived_from_six_probabilities', list(fisher-expected_fisher))
        clock = s.Matrix([s.diff(P[0], x) for x in coords])
        q = simp((clock.T*fisher.inv()*clock)[0])
        g = (2*clock*clock.T/q-fisher).applyfunc(simp)
        check('selected_lorentz_metric', list(g-s.diag(1,-a*a/3,-2*a*a/3,-2*a*a*s.sin(ch)**2/3)))
        inv = g.inv().applyfunc(simp)
        # Derived from g itself, not a warped-product Ricci formula.
        Gamma = [[[simp(sum(inv[k,l]*(s.diff(g[l,j],coords[i])+
            s.diff(g[l,i],coords[j])-s.diff(g[i,j],coords[l])) for l in range(4))/2)
            for j in range(4)] for i in range(4)] for k in range(4)]
        Ric = s.zeros(4)
        for i in range(4):
            for j in range(4):
                Ric[i,j] = simp(sum(s.diff(Gamma[k][i][j],coords[k])-
                    s.diff(Gamma[k][i][k],coords[j]) + sum(
                    Gamma[k][k][l]*Gamma[l][i][j]-Gamma[k][j][l]*Gamma[l][i][k]
                    for l in range(4)) for k in range(4)))
        h = s.diag(s.Rational(1,3),s.Rational(2,3),s.Rational(2,3)*s.sin(ch)**2)
        expected_Ric = s.zeros(4)
        expected_Ric[0,0] = -3*s.diff(a,t,2)/a
        spatial = s.diag(0,1,s.sin(ch)**2)+(a*s.diff(a,t,2)+2*s.diff(a,t)**2)*h
        for i in range(3):
            for j in range(3): expected_Ric[i+1,j+1] = spatial[i,j]
        check('ricci_from_metric_derivatives', list(Ric-expected_Ric))
        waves = []
        for f in phi:
            waves.append(simp(sum(inv[i,j]*(s.diff(f,coords[i],coords[j])-
                sum(Gamma[k][i][j]*s.diff(f,coords[k]) for k in range(4)))
                for i in range(4) for j in range(4))))
        check('wave_eigen_equation_all_five_potentials', [waves[j]-3*phi[j]/a**2 for j in range(5)])
        gradients = phi.jacobian(coords)
        S = (gradients.T*gradients).applyfunc(simp)
        kinetic_trace = simp(sum(inv[i,j]*S[i,j] for i in range(4) for j in range(4)))
        # Tbar = T/c_G; c_G is fixed positive k_G/(pi cosh(k_G)^2).
        Tbar = (S-g*kinetic_trace/2).applyfunc(simp)
        divT = [simp(sum(inv[i,c]*(s.diff(Tbar[i,b],coords[c])-
            sum(Gamma[d][c][i]*Tbar[d,b]+Gamma[d][c][b]*Tbar[i,d] for d in range(4)))
            for i in range(4) for c in range(4))) for b in range(4)]
        check('stress_covariant_conservation_direct', divT)
        point = {t:s.pi/2,th:s.pi/4,ch:s.pi/4,ps:s.pi/4}
        at = lambda m: m.subs(point).applyfunc(simp)
        gp, rp, tp, pp = at(g),at(Ric),at(Tbar),at(P)
        check('point_probabilities', list(pp-s.Matrix([s.Rational(1,2)]+[s.Rational(1,12)]*4+[s.Rational(1,6)])))
        check('point_metric', list(gp-s.diag(1,-s.Rational(2,3),-s.Rational(4,3),-s.Rational(2,3))))
        check('point_ricci', list(rp-s.diag(s.Rational(3,4),s.Rational(1,6),s.Rational(4,3),s.Rational(2,3))))
        check('point_stress_from_source',list(tp-s.diag(s.Rational(3,4),-s.Rational(1,6),-s.Rational(1,3),-s.Rational(1,6))))
        vectors = [s.Matrix([1,s.sqrt(s.Rational(3,2)),0,0]),s.Matrix([1,0,s.sqrt(3)/2,0])]
        contractions = [{'g':simp((v.T*gp*v)[0]), 'Ric':simp((v.T*rp*v)[0]),
                         'T_over_cG':simp((v.T*tp*v)[0])} for v in vectors]
        check('both_vectors_null',[x['g'] for x in contractions])
        check('two_ricci_contractions',[contractions[0]['Ric']-1,contractions[1]['Ric']-s.Rational(7,4)])
        check('equal_nonzero_stress_contractions',[x['T_over_cG']-s.Rational(1,2) for x in contractions])
        requirements = [simp(x['Ric']/x['T_over_cG']) for x in contractions]
        check('incompatible_required_C_times_cG',[requirements[0]-2,requirements[1]-s.Rational(7,2)])
        assert requirements[0] != requirements[1]
        expressions = {'coordinates':[str(x) for x in coords], 'phi':[str(x) for x in phi],
            'probabilities':[str(x) for x in P], 'Fisher':str(fisher),'clock_q':str(q),
            'metric':str(g),'metric_determinant':str(simp(g.det())),
            'nonzero_christoffels':{f'{k},{i},{j}':str(Gamma[k][i][j]) for k in range(4)
                for i in range(4) for j in range(4) if Gamma[k][i][j]!=0},
            'Ricci':str(Ric),'waves':[str(x) for x in waves],
            'gradient_gram':str(S),'kinetic_trace':str(kinetic_trace),'T_over_cG':str(Tbar),
            'point_contractions':[{k:str(v) for k,v in x.items()} for x in contractions],
            'required_C_times_cG':[str(x) for x in requirements]}
        result = {'passed':True,'exit_code':0,'checks':checks,'expressions':expressions,
            'domain':'0<tau<pi; 0<theta,chi,psi<pi/2; k_G>0 constant',
            'domain_argument':'All phi_j and P_i are positive here; thus the positive square root of each conditional probability is phi_j. Fisher diagonal is strictly positive, so rank dP=4; dp0 is nonzero. These inequalities are stated domain reasoning, not an SMT sign certification.',
            'scope':'Exact symbolic same-P geometry verification; no stationary-action, full TGL-solution, physical realization or Lean proof claim.'}
    except BaseException as e:
        result = {'passed':False,'exit_code':1,'checks':checks,'error':str(e),'traceback':traceback.format_exc()}
    result.update(started_utc=start, ended_utc=now(), seconds=time.perf_counter()-tick,
                  python=sys.version,sympy=s.__version__,sources=freeze['evidence'])
    new('RESULT_GEOMETRY_R84.json',result)
    print(json.dumps({'passed':result['passed'],'checks':len(checks),'seconds':result['seconds']}),flush=True)
    return result['exit_code']

if __name__ == '__main__':
    raise SystemExit(main())
