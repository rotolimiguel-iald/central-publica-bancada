"""One preregistered filtered-output calculation, conditional Markov-vacuum instrument."""
from pathlib import Path
import ast,datetime,hashlib,importlib.util,json,math,sys,time,traceback
BASE=Path(__file__).resolve().parent
def pin(p):
    p=Path(p);b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def write_new(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2,ensure_ascii=False,allow_nan=False)
def main():
    freeze=json.loads((BASE/'FREEZE_R64.json').read_text(encoding='utf8'))
    for row in freeze['files']:
        if pin(row['path'])['sha256']!=row['sha256']:raise ValueError('Frozen bytes changed')
    review=json.loads(Path(freeze['review_path']).read_text(encoding='utf8'))
    if not str(review.get('status',review.get('verdict',''))).startswith('PASS'):raise ValueError('Review missing PASS')
    plan=json.loads((BASE/'PLAN_OUTPUT_R64.json').read_text(encoding='utf8'))
    for row in plan['sources']:
        if pin(row['path'])['sha256']!=row['sha256']:raise ValueError('Source changed')
    start=datetime.datetime.now(datetime.timezone.utc)
    if datetime.datetime.fromisoformat(freeze['created_utc'])>=start:raise ValueError('Freeze after start')
    if (BASE/'START_R64.json').exists():raise FileExistsError('Run already started; no implicit retry')
    write_new(BASE/'START_R64.json',{'started_utc':start.isoformat(),'freeze':pin(BASE/'FREEZE_R64.json')})
    timer=time.perf_counter()
    try:
        result=calculate(plan)
        result.update({'started_utc':start.isoformat(),'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                       'seconds':time.perf_counter()-timer,'freeze':pin(BASE/'FREEZE_R64.json')})
        write_new(BASE/'RESULT_OUTPUT_R64.json',result)
        print(json.dumps({'status':result['status'],'checks':len(result['checks']),'failed':[c for c in result['checks'] if not c['passed']],
                          'seconds':result['seconds'],'result':pin(BASE/'RESULT_OUTPUT_R64.json')}))
        return 0 if result['status'].startswith('PASS') else 1
    except Exception:
        write_new(BASE/'FAILURE_R64.json',{'status':'FAILURE','traceback':traceback.format_exc(),'seconds':time.perf_counter()-timer})
        raise
def calculate(plan):
    import numpy as np
    import scipy
    from scipy.linalg import expm
    from scipy.integrate import solve_ivp
    helper=next(s['path'] for s in plan['sources'] if s['path'].endswith('finite_device_functions_r62.py'))
    spec=importlib.util.spec_from_file_location('frozen_finite_r64',helper);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    checks=[]
    def check(name,value,bound=1e-8,greater=False):
        value=float(value);checks.append({'name':name,'value':value,'bound':bound,'relation':'gt' if greater else 'le',
            'passed':bool(math.isfinite(value) and (value>bound if greater else value<=bound))})
    def cj(z):return {'re':float(complex(z).real),'im':float(complex(z).imag)}
    def M(l,theta):
        d=l.shape[0]
        return (np.exp(-1j*theta)*np.kron(np.eye(d),l)+np.exp(1j*theta)*np.kron(l.conj(),np.eye(d)))/math.sqrt(2)
    def filtered(gen,ports,thetas,rho0,filters,label,shot=True):
        d=len(rho0);d2=d*d;n=len(ports);pairs=[(j,k) for j in range(n) for k in range(j,n)]
        maps=[M(l,th) for l,th in zip(ports,thetas)];blocks=1+n+len(pairs)
        y0=np.zeros((blocks,d2),complex);y0[0]=old.vec(rho0)
        for j,(l,th) in enumerate(zip(ports,thetas)):
            direct=(np.exp(-1j*th)*l@rho0+np.exp(1j*th)*rho0@l.conj().T)/math.sqrt(2)
            check(label+'_Mvec_'+str(j),old.residual(old.unvec(maps[j]@old.vec(rho0),d)-direct),1e-12)
        def rhs(t,y):
            v=y.reshape(blocks,d2);dv=v@gen.T
            fs=[float(f(t)) for f in filters]
            for j in range(n):dv[1+j]+=fs[j]*(maps[j]@v[0])
            for z,(j,k) in enumerate(pairs):
                dv[1+n+z]+=fs[j]*(maps[j]@v[1+k])+fs[k]*(maps[k]@v[1+j])
                if shot and j==k:dv[1+n+z]+=.5*fs[j]*fs[k]*v[0]
            return dv.reshape(-1)
        sol=solve_ivp(rhs,(0.,1.),y0.reshape(-1),method='DOP853',rtol=1e-10,atol=1e-12,t_eval=[1.])
        if not sol.success or not np.isfinite(sol.y).all():raise ValueError('ODE failed: '+sol.message)
        v=sol.y[:,-1].reshape(blocks,d2);rho=old.unvec(v[0],d)
        means=np.array([np.trace(old.unvec(v[1+j],d)) for j in range(n)])
        second=np.zeros((n,n),complex)
        for z,(j,k) in enumerate(pairs):second[j,k]=second[k,j]=np.trace(old.unvec(v[1+n+z],d))
        check(label+'_rho_trace',abs(np.trace(rho)-1),1e-9)
        check(label+'_rho_hermitian',old.residual(rho-rho.conj().T),1e-9)
        check(label+'_rho_positive',max(0.,-float(np.linalg.eigvalsh((rho+rho.conj().T)/2).min())),1e-9)
        check(label+'_imaginary',max(float(np.max(np.abs(means.imag))),float(np.max(np.abs(second.imag)))),1e-9)
        cov=second.real-np.outer(means.real,means.real)
        check(label+'_classical_covariance_positive',max(0.,-float(np.linalg.eigvalsh(cov).min())),1e-9)
        return {'means':means.real.tolist(),'second':second.real.tolist(),'covariance':cov.tolist(),'nfev':sol.nfev},rho
    a=np.array([[0,1],[0,0]],complex);e=np.eye(2);ground=np.diag([1.,0.]);excited=np.diag([0.,1.])
    damping=old.liouvillian(np.zeros((2,2),complex),[(1.,a)])
    p=1-math.exp(-1);matched=lambda t:math.exp(-t/2)/math.sqrt(p)
    single,_=filtered(damping,[a],[0.],excited,[matched],'single_photon')
    vacuum,_=filtered(damping,[a],[0.],ground,[matched],'vacuum')
    missing_noise,_=filtered(damping,[a],[0.],ground,[matched],'vacuum_noise_omitted',shot=False)
    check('analytic_single_mean',abs(single['means'][0]))
    check('analytic_single_variance',abs(single['second'][0][0]-(.5+p)))
    check('analytic_vacuum_variance',abs(vacuum['second'][0][0]-.5))
    check('negative_missing_shotnoise',abs(missing_noise['second'][0][0]-.5),1e-5,True)
    s0=.2;t0=.8
    rs=old.unvec(expm(s0*damping)@old.vec(excited),2);rt=old.unvec(expm(t0*damping)@old.vec(excited),2)
    mm=M(a,0.);prop=expm((t0-s0)*damping)
    ordered=np.trace(old.unvec(mm@prop@mm@old.vec(rs),2))
    wrong=np.trace(old.unvec(mm@prop@mm@old.vec(rt),2))
    expected=math.exp(-(t0+s0)/2)
    check('ordered_QRT',abs(ordered-expected),1e-12)
    check('negative_wrong_earlier_state',abs(wrong-expected),1e-5,True)
    chi=.4;theta=.2;R=np.diag([1.,np.exp(1j*chi)])
    test=np.array([[.5,.2+.1j],[.2-.1j,.5]])
    map_lab=(np.exp(-1j*theta)*a@test+np.exp(1j*theta)*test@a.conj().T)/math.sqrt(2)
    rotated=R@test@R.conj().T
    map_rot=(np.exp(-1j*(theta+chi))*a@rotated+np.exp(1j*(theta+chi))*rotated@a.conj().T)/math.sqrt(2)
    check('LO_frame_theta_plus_chi',old.residual(R@map_lab@R.conj().T-map_rot),1e-12)
    configs=[('XX',0.,0.),('PP',math.pi/2,math.pi/2),('XP',0.,math.pi/2),('PX',math.pi/2,0.)]
    ai=np.kron(a,e);ao=np.kron(e,a)
    independent=old.liouvillian(np.zeros((4,4),complex),[(1.,ai),(1.,ao)])
    ket=np.array([1.,0.,0.,np.exp(1j*math.pi/4)])/math.sqrt(2);pair=old.projector(ket)
    pair_rows={}
    for label,ti,to in configs:
        pair_rows[label],_=filtered(independent,[ai,ao],[ti,to],pair,[matched,matched],'two_port_'+label)
    def decode(rows,key='second'):
        q={name:row[key][0][1] for name,row in rows.items()}
        return (q['XX']-q['PP']+1j*(q['XP']+q['PX']))/2,(q['XX']+q['PP']+1j*(q['XP']-q['PX']))/2
    cpair,bpair=decode(pair_rows);target=p*np.exp(1j*math.pi/4)/2
    check('two_port_emitted_pair_C',abs(cpair-target))
    check('two_port_emitted_pair_B',abs(bpair))
    check('negative_wrong_LO_sign',abs(cpair.conjugate()-target),1e-5,True)
    original_plan_path=next(row['path'] for row in plan['sources'] if row['path'].endswith('PREPARED_READOUT_PLAN_R62.json'))
    original=json.loads(Path(original_plan_path).read_text(encoding='utf8'))
    for row in original['source_pins']:
        if pin(row['path'])['sha256']!=row['sha256']:raise ValueError('Full model ancestor changed')
    alpha_file=next(row['path'] for row in original['source_pins'] if 'ALPHA_FINE_CODATA_2018' in row['role'])
    constants={}
    for node in ast.parse(Path(alpha_file).read_text(encoding='utf8')).body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id in {'ALPHA_FINE_CODATA_2018','_SEALED_ALPHA_CODATA_2018'}:
            constants[node.targets[0].id]=ast.literal_eval(node.value)
    if constants['ALPHA_FINE_CODATA_2018']!=constants['_SEALED_ALPHA_CODATA_2018']:raise ValueError('Alpha mismatch')
    beta=constants['ALPHA_FINE_CODATA_2018']*math.sqrt(math.e);gamma_Lambda=1.;lam=beta*gamma_Lambda
    m=original['model']['parameters'];dims=(2,2,2)
    ai=old.embed(a,(0,),dims);ao=old.embed(a,(1,),dims);sm=old.embed(a,(2,),dims);sp=sm.conj().T
    h=m['omega_c']*(ai.conj().T@ai+ao.conj().T@ao)+m['omega_OH']*(sp@sm)
    h+=m['g_JC']*(ai.conj().T@sm+sp@ai)+m['Omega']*(sp+sm)
    J=ao.conj().T@sm+sp@ai;Z=old.embed(np.diag([1.,-1.]),(2,),dims)
    jumps=[(m['kappa_in'],ai),(m['kappa_out'],ao),(m['gamma_OH'],sm),(m['gamma_dephasing'],Z),(lam,J)]
    gen=old.liouvillian(h,jumps)
    ports=[math.sqrt(m['kappa_in'])*ai,math.sqrt(m['kappa_out'])*ao]
    ket=np.array([1.,0.,0.,.5],complex)/math.sqrt(1.25);rho0=np.kron(old.projector(ket),e/2)
    check('full_generator_reused_direct',old.residual(old.unvec(gen@old.vec(rho0),8)-old.direct_generator(h,jumps,rho0)),1e-12)
    full={};finals=[]
    for label,ti,to in configs:
        full[label],rho=filtered(gen,ports,[ti,to],rho0,[lambda t:1.,lambda t:1.],'full_'+label);finals.append(rho)
    for i,rho in enumerate(finals):check('same_unconditional_rho_'+str(i),old.residual(rho-finals[0]),1e-9)
    cf,bf=decode(full);ccov,bcov=decode(full,'covariance')
    return {'status':'PASS_CONDITIONAL_FILTERED_OUTPUT' if all(c['passed'] for c in checks) else 'FAIL_FILTERED_OUTPUT',
      'checks':checks,'controls':{'p_emitted':p,'single':single,'vacuum':vacuum,'noise_omitted':missing_noise,
        'ordered_QRT':cj(ordered),'wrong_time_state':cj(wrong),'two_ports':pair_rows,'C_emitted':cj(cpair),'C_target':cj(target),'B_emitted':cj(bpair)},
      'full_model':{'parameters':m,'beta_runtime_input':beta,'gamma_Lambda_input':gamma_Lambda,'lambda_holo_input':lam,
        'filter':'rectangular norm1,T=1 dimensionless','phase_runs':full,'C_filtered':cj(cf),'B_filtered':cj(bf),
        'C_filtered_centered':cj(ccov),'B_filtered_centered':cj(bcov)},
      'versions':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__},
      'limits':['Conditional Markov vacuum instrument, not inferred from GKLS alone.','Filtered two-time output, not instantaneous cavity C/B.',
        'Four separate phase settings, no simultaneous incompatible X/P outcomes.','No physical calibration or beta inference.',
        'OH full state and five dissipators retained; controls are separate analytic models.']}
if __name__=='__main__':
    sys.dont_write_bytecode=True
    raise SystemExit(main())
