"""Exact conditional identifiability checks; no physical or observed inputs."""
import datetime as dt
import json
import sys
import time
import sympy as sp
import support_r60 as s

def main():
    s.preflight('R5','ALGEBRA')
    start=dt.datetime.now(dt.timezone.utc).isoformat(); clock=time.perf_counter()
    prereg=s.pin(s.ROOT/'PREREG_R60.json')
    s.new('ALGEBRA_START.json',{'utc':start,'preregistered':prereg,'script':s.pin(__file__)})
    checks=[]
    def check(name, condition, kind='identity'):
        ok=bool(condition); checks.append({'name':name,'kind':kind,'pass':ok})
        assert ok,name
    b,g1,g2,ia,ib=sp.symbols('b g1 g2 IA IB',positive=True)
    a1=g1*ia*(1-b);a2=g2*ia*b;c1=g1*ib*b;c2=g2*ib*(1-b)
    q=sp.factor(a2*c1/(a1*c2))
    check('cross_ratio_cancels_four_nuisances',sp.simplify(q-b**2/(1-b)**2)==0)
    odds=b/(1-b)
    check('inverse_on_0_b_1',sp.simplify(odds/(1+odds)-b)==0)
    check('odds_strict_monotonicity',sp.simplify(sp.diff(odds,b)-1/(1-b)**2)==0)
    for x in (g1,g2,ia,ib):check('nuisance_derivative_'+str(x),sp.diff(q,x)==0)
    def channel(bb,ga,gb,fa,fb):return [ga*fa*(1-bb),gb*fa*bb,ga*fb*bb,gb*fb*(1-bb)]
    def inverse(v):
        if len(v)!=4 or any(x.is_real is not True or x.is_finite is not True or not x>0 for x in v):
            raise ValueError('positive finite expected means required')
        root=sp.sqrt(v[1]*v[2]/(v[0]*v[3]));return sp.simplify(root/(1+root))
    examples=[]
    for bb in [sp.Rational(1,100),sp.Rational(1,5),sp.Rational(1,2),sp.Rational(4,5),sp.Rational(99,100)]:
        v=channel(bb,sp.Rational(2,7),sp.Rational(11,5),sp.Integer(13),sp.Integer(29))
        out=inverse(v);check('cross_ratio_injection_'+str(bb),out==bb,'synthetic_exact')
        examples.append({'b_input':str(bb),'means':list(map(str,v)),'b_recovered':str(out)})
    v=channel(sp.Rational(1,5),sp.Integer(2),sp.Integer(3),sp.Integer(10),sp.Integer(20))
    check('one_direction_naive_ratio_biased',sp.simplify(v[1]/(v[0]+v[1])-sp.Rational(1,5))!=0,'negative_control')
    drift=v.copy();drift[3]*=2
    check('changing_gain_breaks_inverse',inverse(drift)!=sp.Rational(1,5),'negative_control')
    # Same four observations, another b, four configuration-dependent gains.
    alternative=sp.Rational(1,3)
    gains=[v[0]/(10*(1-alternative)),v[1]/(10*alternative),v[2]/(20*alternative),v[3]/(20*(1-alternative))]
    recreated=[gains[0]*10*(1-alternative),gains[1]*10*alternative,gains[2]*20*alternative,gains[3]*20*(1-alternative)]
    check('unknown_gain_drift_two_worlds',recreated==v,'negative_control')
    for bad in [sp.Integer(0),sp.Integer(-1),sp.oo,sp.nan]:
        vv=v.copy();vv[0]=bad
        try:inverse(vv)
        except ValueError:rejected=True
        else:rejected=False
        check('cross_ratio_refuses_'+str(bad),rejected,'guard')
    n,ea,eb=sp.symbols('n etaA etaB',positive=True)
    x=ea*n;y=eb*n;z=ea*eb*n*(n+1);delta=sp.expand(z-x*y)
    check('pair_quantum_excess',sp.simplify(delta-ea*eb*n)==0)
    check('pair_reconstruct_n',sp.simplify(x*y/delta-n)==0)
    check('pair_reconstruct_etaA',sp.simplify(delta/y-ea)==0)
    check('pair_reconstruct_etaB',sp.simplify(delta/x-eb)==0)
    jac=sp.Matrix([x,y,z]).jacobian([n,ea,eb]).det()
    check('pair_jacobian_nonzero_in_domain',sp.factor(jac)==-ea*eb*n**2)
    def pair_inverse(xx,yy,zz):
        if any(v.is_real is not True or v.is_finite is not True or not v>0 for v in [xx,yy,zz]):
            raise ValueError('positive finite moments required')
        dd=zz-xx*yy
        if not dd>0:raise ValueError('nonpositive quantum excess')
        aa=dd/yy;bb=dd/xx
        if aa>1 or bb>1:raise ValueError('efficiency outside pure-loss range')
        return tuple(map(sp.simplify,[xx*yy/dd,aa,bb]))
    pair_examples=[]
    for nn,aa,bb in [(sp.Rational(1,10),sp.Rational(1,2),sp.Rational(2,3)),(sp.Integer(2),sp.Rational(1,2),sp.Rational(1,2)),(sp.Integer(5),sp.Integer(1),sp.Rational(1,7))]:
        vals=(aa*nn,bb*nn,aa*bb*nn*(nn+1));out=pair_inverse(*vals)
        check('pair_injection_'+str(nn),out==(nn,aa,bb),'synthetic_exact')
        pair_examples.append({'input':list(map(str,[nn,aa,bb])),'moments':list(map(str,vals)),'output':list(map(str,out))})
    # A pure source n=2 behind eta=.5 and a mixed source n=1 at eta=1
    # have the same x=y=1 and |m_out|^2=3/2.
    mixed_n=sp.Integer(1);mixed_m2=sp.Rational(3,2)
    check('mixed_counterexample_physical_symplectic_eigenvalue', (mixed_n+sp.Rational(1,2))**2-mixed_m2>=sp.Rational(1,4),'negative_control')
    check('mixed_counterexample_passes_ideal_guards',pair_inverse(sp.Integer(1),sp.Integer(1),mixed_m2)==(sp.Integer(2),sp.Rational(1,2),sp.Rational(1,2)),'negative_control')
    check('mixed_counterexample_wrong_source_if_purity_assumed',pair_inverse(sp.Integer(1),sp.Integer(1),mixed_m2)[0]!=mixed_n,'negative_control')
    for label,vals in [('vacuum',[0,0,0]),('classical_excess',[1,1,1]),('negative_excess',[1,1,sp.Rational(1,2)]),('eta_gt_1',[1,1,3])]:
        try:pair_inverse(*map(sp.sympify,vals))
        except ValueError:rejected=True
        else:rejected=False
        check('pair_refuses_'+label,rejected,'guard')
    result={'status':'PASS_CONDITIONAL_IDENTIFIABILITY_WITH_COUNTEREXAMPLES','start_utc':start,
      'end_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'seconds':time.perf_counter()-clock,
      'python':sys.version,'sympy':sp.__version__,'preregistered':prereg,'script':s.pin(__file__),
      'checks':checks,'count':len(checks),'cross_ratio_examples':examples,'pair_examples':pair_examples,
      'mixed_counterexample':{'sourceA':'pure n=2 etaA=etaB=1/2 |m|^2=6','sourceB':'mixed n=1 etaA=etaB=1 |m|^2=3/2','same_observed':'x=y=1,z=3/2'},
      'unknown_drift_counterexample':{'data':list(map(str,v)),'b_true':'1/5','b_alternative':'1/3','alternative_gains':list(map(str,gains))},
      'scope':'Algebra of expected moments/means, not unbiased finite-count estimators. No observed data or empirical significance. No betaTGL inference without a physical bridge.',
      'beta_input_used':False,'R4_touched':False,'gate_changed':False}
    p=s.new('RESULT_R60.json',result);print(json.dumps({'path':str(p),'count':len(checks),'status':result['status']}))

if __name__=='__main__':main()
