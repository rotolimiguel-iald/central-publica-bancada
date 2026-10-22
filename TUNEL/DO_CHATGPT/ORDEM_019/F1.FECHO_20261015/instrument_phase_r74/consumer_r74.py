"""Finite synthetic transport of the SAME full generator and filtered instrument.
No original main is executed. Validity here does not calibrate RF/optical hardware.
"""
from pathlib import Path
import ast, hashlib, importlib.util, json, math

def calculate(plan):
    import numpy as np
    from scipy.integrate import solve_ivp
    import scipy
    sources={x['role']:Path(x['path']) for x in plan['sources']}
    spec=importlib.util.spec_from_file_location('r62_pure_reuse',sources['r62_pure'])
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    # Reuse EXACT two assignment ASTs R62, without importing its runner/main.
    tree=ast.parse(sources['r62_decoder'].read_text(encoding='utf-8'))
    found=[]
    for n in ast.walk(tree):
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['c','b']:
            if "Q['XX']" in ast.unparse(n):found.append(n)
    assert len(found)==2 and {n.targets[0].id for n in found}=={'c','b'}
    module=ast.fix_missing_locations(ast.Module(body=found,type_ignores=[]));decoder=compile(module,str(sources['r62_decoder']),'exec')
    def decode(Q):
        env={'Q':Q};exec(decoder,{'__builtins__':{}},env);return complex(env['c']),complex(env['b'])
    constants={}
    for n in ast.parse(sources['alpha'].read_text(encoding='utf-8')).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['ALPHA_FINE_CODATA_2018','_SEALED_ALPHA_CODATA_2018']:
            constants[n.targets[0].id]=ast.literal_eval(n.value)
    assert constants['ALPHA_FINE_CODATA_2018']==constants['_SEALED_ALPHA_CODATA_2018']
    beta=constants['ALPHA_FINE_CODATA_2018']*math.sqrt(math.e)
    original=json.loads(sources['r62_plan'].read_text(encoding='utf-8'))
    m=original['model']['parameters'];lam=beta*original['model']['gamma_Lambda']
    for v in [*m.values(),original['model']['gamma_Lambda'],*plan['gains']]:
        if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v<=0:raise ValueError('Invalid positive INPUT')
    checks=[]
    def norm(x):return float(np.linalg.norm(x))
    def check(name,value,bound=None,negative=False):
        v=float(value);b=plan['tolerances']['algebra'] if bound is None else bound
        checks.append({'name':name,'value':v,'bound':b,'relation':'gt' if negative else 'le','passed':bool(math.isfinite(v) and (v>b if negative else v<=b))})
    def enc(z):return {'re':float(complex(z).real),'im':float(complex(z).imag)}
    a=np.array([[0,1],[0,0]],complex);dims=(2,2,2)
    ai=old.embed(a,(0,),dims);ao=old.embed(a,(1,),dims);sm=old.embed(a,(2,),dims);sp=sm.conj().T
    ns=[ai.conj().T@ai,ao.conj().T@ao,sp@sm]
    Z=old.embed(np.diag([1.,-1.]),(2,),dims);A=ao.conj().T@sm;B=sp@ai;J=A+B
    H0=m['omega_c']*(ns[0]+ns[1])+m['omega_OH']*ns[2]+m['g_JC']*(ai.conj().T@sm+sp@ai)
    rates=[m['kappa_in'],m['kappa_out'],m['gamma_OH'],m['gamma_dephasing'],lam]
    ops=[ai,ao,sm,Z,J]
    alpha=1j*m['Omega']/math.sqrt(m['gamma_OH'])
    L3=math.sqrt(m['gamma_OH'])*sm
    pump=1j*(alpha.conjugate()*L3-alpha*L3.conj().T)
    H=H0+pump;jumps=list(zip(rates,ops));ports=[math.sqrt(rates[0])*ai,math.sqrt(rates[1])*ao]
    ket=np.array([complex(*x) for x in plan['rich_state_amplitudes']],complex);ket/=np.linalg.norm(ket)
    rho0=plan['pure_weight']*old.projector(ket)+(1-plan['pure_weight'])*np.eye(8)/8
    old.validate_density(rho0,1e-12)
    def phase(t):
        # Frozen polynomial + sinusoidal laws; zero initial phase for both frames.
        rows=plan['phase_laws']
        chi=np.array([p['linear']*t+p['quadratic']*t*t+p['sin_amplitude']*math.sin(p['sin_frequency']*t) for p in rows])
        dot=np.array([p['linear']+2*p['quadratic']*t+p['sin_amplitude']*p['sin_frequency']*math.cos(p['sin_frequency']*t) for p in rows])
        return chi,dot
    def frame(t):
        chi,dot=phase(t);diag=sum(chi[k]*np.diag(ns[k]) for k in range(3))
        R=np.diag(np.exp(1j*diag));D=sum(dot[k]*ns[k] for k in range(3));return chi,R,D
    def filt(t,j):
        p=plan['filters'][j];amp=p['amplitude_slope'];phaseval=p['phase_linear']*t+p['phase_quadratic']*t*t
        return (1+amp*t)*np.exp(1j*phaseval)/math.sqrt(1+amp+amp*amp/3)
    def transformed(t,branch):
        chi,R,D=frame(t);conj=lambda x:R@x@R.conj().T
        if branch=='lab':return H,jumps,ports,np.zeros(3)
        hp=conj(H)-D;jp=[(rate,conj(op)) for rate,op in jumps]
        pports=[conj(x) for x in ports]
        if branch=='bad_J_phase':jp[-1]=(lam,np.exp(1j*(chi[1]-chi[2]))*A+B)
        elif branch=='split_bath':jp=jp[:-1]+[(lam,conj(A)),(lam,conj(B))]
        elif branch=='bad_pump':hp=conj(H0)+pump-D
        if branch in ['base_LO','stale_LO']:pports=ports
        return hp,jp,pports,chi
    tol=plan['tolerances']
    for t in plan['point_times']:
        chi,R,D=frame(t);rho=R@rho0@R.conj().T
        hp,jp,pp,_=transformed(t,'transported')
        target=R@old.direct_generator(H,jumps,rho0)@R.conj().T+1j*(D@rho-rho@D)
        check('generator_covariance_t'+str(t),norm(old.direct_generator(hp,jp,rho)-target))
        explicit=np.exp(1j*(chi[1]-chi[2]))*A+np.exp(1j*(chi[2]-chi[0]))*B
        check('joint_jump_formula_t'+str(t),norm(jp[-1][1]-explicit))
        pump_prime=1j*(alpha.conjugate()*jp[2][1]*math.sqrt(rates[2])-alpha*(jp[2][1]*math.sqrt(rates[2])).conj().T)
        check('coherent_reservoir_pump_t'+str(t),norm(pump_prime-R@pump@R.conj().T))
    for branch in ['bad_J_phase','split_bath','bad_pump']:
        t=plan['negative_point_time'];chi,R,D=frame(t);rho=R@rho0@R.conj().T
        hp,jp,_,_=transformed(t,branch);hc,jc,_,_=transformed(t,'transported')
        check('negative_generator_'+branch,norm(old.direct_generator(hp,jp,rho)-old.direct_generator(hc,jc,rho)),tol['negative_generator'],True)
    configs=[('XX',0.,0.),('PP',math.pi/2,math.pi/2),('XP',0.,math.pi/2),('PX',math.pi/2,0.)]
    pairs=[(0,0),(0,1),(1,1)]
    def integrate(branch):
        # R64 hierarchy, extended pointwise to complex filters and time-dependent generators.
        y0=np.zeros((4,6,8,8),complex);y0[:,0]=rho0
        def rhs(t,y):
            v=y.reshape(4,6,8,8);hp,jp,pp,chi=transformed(t,branch)
            dv=old.direct_generator(hp,jp,v)
            for n,(_,ti,to) in enumerate(configs):
                coeff=[]
                for j,th in enumerate([ti,to]):
                    # Exactly one phase transport: either pp=L' or theta'=theta+chi.
                    if branch=='base_LO':th+=chi[j]
                    coeff.append(plan['gains'][j]*filt(t,j).conjugate()*np.exp(-1j*th))
                def measurement(j,x):
                    c=coeff[j];l=pp[j];return (c*(l@x)+c.conjugate()*(x@l.conj().T))/math.sqrt(2)
                for j in range(2):dv[n,1+j]+=measurement(j,v[n,0])
                for z,(j,k) in enumerate(pairs):
                    dv[n,3+z]+=measurement(j,v[n,1+k])+measurement(k,v[n,1+j])
                    if j==k:dv[n,3+z]+=.5*abs(coeff[j])**2*v[n,0]
            return dv.reshape(-1)
        sol=solve_ivp(rhs,(0.,plan['T']),y0.reshape(-1),method='DOP853',rtol=tol['rtol'],atol=tol['atol'],t_eval=[plan['T']])
        if not sol.success or not np.isfinite(sol.y).all():raise ValueError('Filtered ODE failed '+sol.message)
        v=sol.y[:,-1].reshape(4,6,8,8);rows={};Q={}
        for n,(label,_,_) in enumerate(configs):
            old.validate_density(v[n,0],tol['ode'])
            means=np.array([np.trace(v[n,1+j]) for j in range(2)])
            second=np.array([[np.trace(v[n,3]),np.trace(v[n,4])],[np.trace(v[n,4]),np.trace(v[n,5])]])
            check(branch+'_'+label+'_imag',max(norm(means.imag),norm(second.imag)),tol['ode'])
            cov=second.real-np.outer(means.real,means.real)
            check(branch+'_'+label+'_cov_psd',max(0.,-float(np.linalg.eigvalsh(cov).min())),tol['ode'])
            rows[label]={'means':means.real.tolist(),'second':second.real.tolist(),'covariance':cov.tolist()}
            Q[label]=float(second[0,1].real)/(plan['gains'][0]*plan['gains'][1])
        C,Bread=decode(Q)
        z=(rows['XX']['means'][0]+1j*rows['PP']['means'][0])/(math.sqrt(2)*plan['gains'][0])
        return {'rows':rows,'C':C,'B':Bread,'z':z,'rho':v[0,0],'nfev':sol.nfev}
    runs={branch:integrate(branch) for branch in plan['branches']}
    lab=runs['lab'];endR=frame(plan['T'])[1]
    for branch in ['transported','base_LO']:
        run=runs[branch]
        check(branch+'_final_state',norm(run['rho']-endR@lab['rho']@endR.conj().T),tol['ode'])
        for key in ['C','B','z']:check(branch+'_filtered_'+key,abs(run[key]-lab[key]),tol['ode'])
        for label,_,_ in configs:
            for key in ['means','second','covariance']:
                check(branch+'_'+label+'_'+key,norm(np.array(run['rows'][label][key])-np.array(lab['rows'][label][key])),tol['ode'])
    for branch in ['stale_LO','bad_J_phase','split_bath','bad_pump']:
        delta=max(abs(runs[branch][k]-lab[k]) for k in ['C','B','z'])
        check('negative_filtered_'+branch,delta,tol['negative_output'],True)
    # An endpoint phase cannot undo different phases at every time in the packet integral.
    ci,co,_=phase(plan['T'])[0];bad=runs['stale_LO']
    cfix=bad['C']*np.exp(-1j*(ci+co));bfix=bad['B']*np.exp(1j*(ci-co))
    check('negative_final_phase_only',max(abs(cfix-lab['C']),abs(bfix-lab['B'])),tol['negative_output'],True)
    theta=math.asin(math.sqrt(beta));G=np.array([[0,1],[-1,0]],complex)
    S=math.cos(theta)*np.eye(2)+math.sin(theta)*G;P=(np.eye(2)-1j*G)/2
    for branch in ['lab','transported','base_LO']:
        z=runs[branch]['z'];encoded=z*S;w=2*(P@encoded)[0,0]
        decoded=w*np.exp(-1j*theta)*S
        check(branch+'_R57_read_phase',abs(w-z*np.exp(1j*theta)))
        check(branch+'_R57_decoder',norm(decoded-encoded))
        check(branch+'_R57_reread',norm(P@(P@encoded)-P@encoded))
    check('rich_signal_nonzero',abs(lab['z']),tol['negative_output'],True)
    safe={}
    for name,run in runs.items():safe[name]={'rows':run['rows'],'C':enc(run['C']),'B':enc(run['B']),'z_operational':enc(run['z']),'nfev':run['nfev']}
    return {'status':'PASS_SYNTHETIC_FRAME_INSTRUMENT' if all(c['passed'] for c in checks) else 'FAIL_SYNTHETIC_FRAME_INSTRUMENT','passed':all(c['passed'] for c in checks),'checks':checks,'runs':safe,'beta_runtime_INPUT':beta,'Gamma_INPUT':original['model']['gamma_Lambda'],'lambda_INPUT':lam,'coherent_OH_input':enc(alpha),'final_phase_only':{'C':enc(cfix),'B':enc(bfix)},'versions':{'numpy':np.__version__,'scipy':scipy.__version__},'limits':['Finite cutoff (2,2,2), dimensionless INPUT; no GHz/nm calibration.','R64 Markov-vacuum monitored output ports 1/2; coherent reservoir channel3 drives H only.','Four distinct LO experiments, not simultaneous incompatible quadratures.','Operational filtered quadrature mean is encoded by R57; no equality with physical G_OH claimed.','No full-state tomography, Gamma inference, physical measurement, Lean, gate or production change.']}
