"""Compute the smooth Euler defect of the specified singular Hadamard jet.

Reuses the existing radial heat coefficients; this is not the full BV anomaly.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,uuid,time
import sympy as s
from metric_coincident_jet_engine_v2 import metric_fiber

H=Path(__file__).resolve().parent;D=H/'curved_parametrix_euler_defect'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):
    assert not p.exists(),p
    b=json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
def main():
    D.mkdir(exist_ok=False)
    put(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
        target='Coincident K² smooth defect of minimal metric/ghost singular parametrix',
        prescription='Auxiliary Euclidean Hsing=U0/z-U1*log(z/ell²)/4+U2*z*log(z/ell²)/16; no smooth W included; L=nabla²+K*E, D=-L',
        normalization='Leading singular scalar 1/z; physical Green normalization not included',
        scope='Constant-curvature4D local radial-frame jet through K²; not Lorentzian Q2',
        sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),
            H/'metric_coincident_jet_engine_v2.py',H/'metric_coincident_jet_v2/results.json',
            H/'spaceform_heat/results.json']]))
    start=time.process_time();x=s.symbols('x0:4');z=sum(v*v for v in x)
    f=metric_fiber();omega={}
    for i in range(4):
        for j in range(4):
            a=s.zeros(4)
            if i!=j:a[i,j]=1;a[j,i]=-1
            omega[i,j]=a
    Eghost=3*s.eye(4)
    om2=sum((a*a for a in omega.values()),s.zeros(4))
    a2ghost=Eghost*Eghost/2+2*Eghost+s.Rational(29,15)*s.eye(4)+om2/12
    cases=[('metric',f['E'],f['omega'],f['a2']),('ghost',Eghost,omega,a2ghost)]
    checks=[];outputs={}
    def eq(label,A):
        vals=list(A) if isinstance(A,s.MatrixBase) else [A]
        assert all(s.cancel(v)==0 for v in vals),(label,A)
        checks.append(label)
    for name,E,om,a2 in cases:
        I=s.eye(E.rows);a1=E+2*I
        conn=[sum((x[j]*om[j,i]/2 for j in range(4)),s.zeros(E.rows)) for i in range(4)]
        conn2=sum((a*a for a in conn),s.zeros(E.rows))
        u1second=z*a1/4-z*I/60+conn2/3
        lap=sum((u1second.diff(v,2) for v in x),s.zeros(E.rows))
        eq(name+' radial gauge',sum((x[i]*conn[i] for i in range(4)),s.zeros(E.rows)))
        eq(name+' transport recurrence',(lap+E*a1)/2-a2)
        # The logarithmic term must cancel before taking the coincidence limit.
        logarithmic=-lap/4-E*a1/4+a2/2
        eq(name+' logarithmic cancellation',logarithmic)
        # Scalar geometric terms from L(U0/z), curvature acting on log z,
        # connection squared, flat Laplacian of u1second*log z, and U2*z*log z.
        constant=s.Rational(9,20)*I+E/4+a1/2+conn2/z-3*u1second/z+3*a2/4
        eq(name+' full directional cancellation',constant-3*a2/4)
        required=(-3*a2/4).applyfunc(s.expand)
        outputs[name]=dict(rank=E.rows,
            L_Hsing_over_K2=[[str(v) for v in row] for row in (3*a2/4).tolist()],
            L_W_required_for_bisolution_over_K2=[[str(v) for v in row] for row in required.tolist()],
            trace_L_Hsing_over_K2=str(s.trace(3*a2/4)),
            log_coefficient_zero=True,direction_independent=True)
        # Leaving out the connection term must expose the angular matrix remainder.
        omitted=constant-conn2/z-3*a2/4
        assert omitted!=s.zeros(E.rows)
        assert any(s.cancel(v)!=0 for v in omitted)
        checks.append(name+' omitted connection rejected')

    # Independent scalar radial differentiation, with potential not proportional to K.
    r,K,e=s.symbols('r K E',nonzero=True)
    log=s.log(r*r)
    u0=1+K*r*r/4+s.Rational(19,480)*K*K*r**4
    u1=e+2*K+r*r*(e*K/4+s.Rational(29,60)*K*K)
    a2=e*e/2+2*K*e+s.Rational(29,15)*K*K
    param=u0/r**2-u1*log/4+a2*r*r*log/16
    result=s.expand(s.diff(param,r,2)+3*(1/r-K*r/3-K*K*r**3/45)*s.diff(param,r)+e*param)
    limit=s.limit(result,r,0,dir='+')
    eq('independent scalar radial coincidence',limit-3*a2/4)
    eq('metric trace/traceless eigenvalue',3*f['a2']/4-(-s.Rational(21,20)*f['tl']+s.Rational(479,20)*f['ptr']))
    eq('ghost eigenvalue',3*a2ghost/4-s.Rational(179,20)*s.eye(4))
    weighted=s.trace(3*f['a2']/4)/2-s.trace(3*a2ghost/4)
    eq('weighted trace',weighted+s.Rational(571,20))
    data=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),check_names=checks,
        cpu_seconds=time.process_time()-start,blocks=outputs,
        metric_L_Hsing_over_K2='-21/20 P_TL + 479/20 P_tr',
        ghost_L_Hsing_over_K2='179/20 Id_4',
        half_metric_minus_ghost_trace_over_K2=str(weighted),
        scalar_general_L_Hsing=str(limit),
        normalization='All values relative to leading1/z; L=nabla²+E, sign reverses for D=-L',
        inference='The singular local parametrix alone is not an exact bisolution at K². A smooth W must satisfy L W=-3 U2/4 at coincidence in this chosen splitting.',
        not_claimed=['No specific W/state constructed','No full nonminimal22x22 parametrix','No A1 or A2 coefficient obtained','No composite insertion normalization','No Lorentzian continuation'],
        full_Q2=False,gate_changed=False)
    put(D/'results.json',data)
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
        [Path(__file__),D/'PRE_REGISTER.json',D/'results.json',H/'metric_coincident_jet_engine_v2.py']],full_Q2=False))
    print(json.dumps({k:v for k,v in data.items() if k not in ['blocks','check_names']},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
