"""Controlled first/second filtered moments in TOTAL bosonic cuts; no new HP claim."""
from pathlib import Path
import ast,importlib.util,json,math

def calculate(plan):
    import numpy as np
    import scipy
    from scipy import sparse as sp
    from scipy.integrate import solve_ivp
    src={x['role']:Path(x['path']) for x in plan['sources']}
    original=json.loads(src['r62_plan'].read_text(encoding='utf-8'));p=original['model']['parameters']
    constants={}
    for n in ast.parse(src['alpha'].read_text(encoding='utf-8')).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['ALPHA_FINE_CODATA_2018','_SEALED_ALPHA_CODATA_2018']:constants[n.targets[0].id]=ast.literal_eval(n.value)
    assert constants['ALPHA_FINE_CODATA_2018']==constants['_SEALED_ALPHA_CODATA_2018']
    beta=constants['ALPHA_FINE_CODATA_2018']*math.sqrt(math.e);lam=beta*original['model']['gamma_Lambda']
    # EXACT R66 local functions, no imports/main/global assignments from the ancestor.
    tree=ast.parse(src['r66_helpers'].read_text(encoding='utf-8'))
    nodes=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name in ['liou','model','include']]
    assert len(nodes)==3
    env={'np':np,'sp':sp,'math':math,'p':p,'lam':lam}
    exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),str(src['r66_helpers']),'exec'),env)
    models={m:env['model'](m) for m in plan['cuts']}
    decnodes=[n for n in ast.walk(ast.parse(src['r62_decoder'].read_text(encoding='utf-8'))) if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['c','b'] and "Q['XX']" in ast.unparse(n)]
    assert len(decnodes)==2;decoder=compile(ast.fix_missing_locations(ast.Module(body=decnodes,type_ignores=[])),str(src['r62_decoder']),'exec')
    def decode(Q):
        e={'Q':Q};exec(decoder,{'__builtins__':{}},e);return complex(e['c']),complex(e['b'])
    checks=[];tol=plan['tolerances']
    def check(name,value,bound=None,negative=False):
        value=float(value);bound=tol['algebra'] if bound is None else float(bound)
        checks.append({'name':name,'value':value,'bound':bound,'relation':'gt' if negative else 'le','passed':bool(math.isfinite(value) and math.isfinite(bound) and (value>bound if negative else value<=bound))})
    def norm(x):return float(np.linalg.norm(x.toarray() if sp.issparse(x) else x))
    def enc(z):return {'re':float(complex(z).real),'im':float(complex(z).imag)}
    def vec(x):return x.reshape(-1,order='F')
    def unvec(x,d):return x.reshape((d,d),order='F')
    T=plan['T'];m0=plan['initial_max_N'];gains=plan['gains']
    prior74=json.loads(src['r74_plan'].read_text(encoding='utf-8'))
    def phase(t):
        rows=prior74['phase_laws']
        chi=np.array([z['linear']*t+z['quadratic']*t*t+z['sin_amplitude']*math.sin(z['sin_frequency']*t) for z in rows])
        dot=np.array([z['linear']+2*z['quadratic']*t+z['sin_amplitude']*z['sin_frequency']*math.cos(z['sin_frequency']*t) for z in rows]);return chi,dot
    def rotation(mod,t):
        chi,dot=phase(t);bas=np.array(mod['basis']);rdiag=np.exp(1j*(bas@chi));dd=bas@dot
        sd=vec(np.outer(rdiag,rdiag.conjugate()));deriv=vec(1j*(dd[:,None]-dd[None,:]))
        return rdiag,sd,deriv,dd
    def filt(t,j):
        f=plan['filters'][j];a=f['amplitude_slope'];phaseval=f['phase_linear']*t+f['phase_quadratic']*t*t
        return (1+a*t/T)*np.exp(1j*phaseval)/math.sqrt(T*(1+a+a*a/3))
    for m,mod in models.items():check('dimension_'+str(m),abs(len(mod['basis'])-(m+1)**2),0)
    # Pointwise independent explicit generator check for the one rotating-frame run.
    mod=models[plan['frame_cut']];d=len(mod['basis'])
    for t in plan['frame_check_times']:
        rd,sd,deriv,dd=rotation(mod,t);R=np.diag(rd)
        hp=R@(mod['h0']+mod['drive'])@R.conj().T-np.diag(dd)
        lp=[R@l@R.conj().T for l in mod['jumps']]
        explicit=env['liou'](hp,lp)
        transported=sp.diags(sd)@mod['g']@sp.diags(sd.conjugate())+sp.diags(deriv)
        check('explicit_rotating_generator_t'+str(t),norm(explicit-transported))
    configs=[('XX',0.,0.),('PP',math.pi/2,math.pi/2),('XP',0.,math.pi/2),('PX',math.pi/2,0.)]
    pairs=[(0,0),(0,1),(1,1)]
    def integrate(m,rotating=False):
        mod=models[m];d=len(mod['basis']);d2=d*d
        ket=np.zeros(d,complex)
        for z in plan['initial_amplitudes']:
            assert sum(z['basis'])<=m0
            ket[mod['index'][tuple(z['basis'])]]=complex(*z['amplitude'])
        ket/=np.linalg.norm(ket);rho=np.outer(ket,ket.conjugate())
        v0=np.zeros((4,6,d2),complex);v0[:,0]=vec(rho)
        left=[sp.kron(sp.eye(d,format='csr'),sp.csr_matrix(l),format='csr') for l in mod['jumps'][:2]]
        right=[sp.kron(sp.csr_matrix(l.conj()),sp.eye(d,format='csr'),format='csr') for l in mod['jumps'][:2]]
        def rhs(t,y):
            v=y.reshape(4,6,d2)
            if rotating:
                _,sd,deriv,_=rotation(mod,t);w=v*sd.conjugate()
                dv=(mod['g']@w.reshape(24,d2).T).T.reshape(4,6,d2)*sd+v*deriv
            else:w=v;dv=(mod['g']@v.reshape(24,d2).T).T.reshape(4,6,d2)
            for k,(_,ti,to) in enumerate(configs):
                cs=[gains[j]*filt(t,j).conjugate()*np.exp(-1j*th) for j,th in enumerate([ti,to])]
                def M(j,x):
                    out=(cs[j]*(left[j]@x)+cs[j].conjugate()*(right[j]@x))/math.sqrt(2)
                    return out*sd if rotating else out
                for j in range(2):dv[k,1+j]+=M(j,w[k,0])
                for z,(j,l) in enumerate(pairs):
                    dv[k,3+z]+=M(j,w[k,1+l])+M(l,w[k,1+j])
                    if j==l:dv[k,3+z]+=.5*abs(cs[j])**2*v[k,0]
            return dv.reshape(-1)
        sol=solve_ivp(rhs,(0.,T),v0.reshape(-1),method='DOP853',rtol=tol['rtol'],atol=tol['atol'],t_eval=[T])
        if not sol.success or not np.isfinite(sol.y).all():raise ValueError('ODE failed '+sol.message)
        v=sol.y[:,-1].reshape(4,6,d2);rows={};Q={};Qcov={};rhoout=unvec(v[0,0],d)
        tag=str(m)+('_rot' if rotating else '_lab')
        check(tag+'_trace',abs(np.trace(rhoout)-1),tol['ode'])
        check(tag+'_hermitian',norm(rhoout-rhoout.conj().T),tol['ode'])
        check(tag+'_positive',max(0.,-float(np.linalg.eigvalsh((rhoout+rhoout.conj().T)/2).min())),tol['ode'])
        for k,(label,_,_) in enumerate(configs):
            means=np.array([np.trace(unvec(v[k,1+j],d)) for j in range(2)])
            second=np.array([[np.trace(unvec(v[k,3],d)),np.trace(unvec(v[k,4],d))],[np.trace(unvec(v[k,4],d)),np.trace(unvec(v[k,5],d))]])
            check(tag+'_'+label+'_imag',max(norm(means.imag),norm(second.imag)),tol['ode'])
            cov=second.real-np.outer(means.real,means.real)
            check(tag+'_'+label+'_cov_psd',max(0.,-float(np.linalg.eigvalsh(cov).min())),tol['ode'])
            rows[label]={'means':means.real.tolist(),'second':second.real.tolist(),'covariance':cov.tolist()}
            Q[label]=float(second[0,1].real)/(gains[0]*gains[1]);Qcov[label]=float(cov[0,1])/(gains[0]*gains[1])
        C,B=decode(Q);Cc,Bc=decode(Qcov)
        return {'rows':rows,'C':C,'B':B,'C_centered':Cc,'B_centered':Bc,'rho':rhoout,'nfev':sol.nfev}
    runs={m:integrate(m) for m in plan['cuts']};rot=integrate(plan['frame_cut'],True)
    ref=runs[plan['frame_cut']];rd,_,_,_=rotation(models[plan['frame_cut']],T)
    check('rotating_final_state',norm(rot['rho']-rd[:,None]*ref['rho']*rd.conjugate()[None,:]),tol['ode'])
    for label,_,_ in configs:
        for key in ['means','second','covariance']:
            check('rotating_'+label+'_'+key,norm(np.array(rot['rows'][label][key])-np.array(ref['rows'][label][key])),tol['ode'])
    for key in ['C','B','C_centered','B_centered']:check('rotating_'+key,abs(rot[key]-ref[key]),tol['ode'])
    # Conservative positive tail majorants: no subtractive cancellation or infinite exact-reference cut.
    q=2*abs(p['Omega'])*T
    def E(k):
        if k<0:return math.exp(q)
        first=k+1
        ratio=q/(first+1)
        if not ratio<1:raise ValueError('Tail majorant domain violated')
        return q**first/math.factorial(first)/(1-ratio)
    A=[]
    for j,f in enumerate(plan['filters']):
        a=f['amplitude_slope'];integral=gains[j]*math.sqrt(T)*(1+a/2)/math.sqrt(1+a+a*a/3)
        A.append(math.sqrt(2*p[['kappa_in','kappa_out'][j]])*integral)
    S1=math.exp(q)*math.sqrt(m0+q);comparisons=[];certificates=[]
    for m in plan['cuts']:
        tail=E(m-m0);T2=m0*tail+q*E(m-m0-1);T1=math.sqrt(tail*T2)
        epsmean=[2*a*T1 for a in A]
        epssecond=[[2*a*b*T2 for b in A] for a in A]
        epscov=[[2*a*b*T2+4*a*b*S1*T1 for b in A] for a in A]
        epsdecode=4*A[0]*A[1]*T2/(gains[0]*gains[1]);epsdecodecov=2*epscov[0][1]/(gains[0]*gains[1])
        certificates.append({'cut':m,'reference':'analytical_infinite_first_two_moments_only','q':q,'E_majorant':tail,'T1_majorant':T1,'T2_majorant':T2,'mean_error_bound':epsmean,'raw_second_error_bound':epssecond,'covariance_error_bound':epscov,'C_B_error_bound':epsdecode,'centered_C_B_error_bound':epsdecodecov})
        for n in plan['cuts']:
            if n<=m:continue
            row={'lower':m,'upper':n,'upper_is_exact_infinite':False,'max_mean_difference':0.,'max_raw_second_difference':0.}
            for label,_,_ in configs:
                lo=runs[m]['rows'][label];hi=runs[n]['rows'][label]
                for j in range(2):
                    delta=abs(hi['means'][j]-lo['means'][j]);check(f'cut_{m}_{n}_{label}_mean{j}',delta,epsmean[j]+tol['ode']);row['max_mean_difference']=max(row['max_mean_difference'],delta)
                    for k in range(j,2):
                        ds=abs(hi['second'][j][k]-lo['second'][j][k]);dc=abs(hi['covariance'][j][k]-lo['covariance'][j][k])
                        check(f'cut_{m}_{n}_{label}_second{j}{k}',ds,epssecond[j][k]+tol['ode']);check(f'cut_{m}_{n}_{label}_cov{j}{k}',dc,epscov[j][k]+tol['ode']);row['max_raw_second_difference']=max(row['max_raw_second_difference'],ds)
            for key in ['C','B']:check(f'cut_{m}_{n}_{key}',abs(runs[n][key]-runs[m][key]),epsdecode+tol['ode'])
            for key in ['C_centered','B_centered']:check(f'cut_{m}_{n}_{key}',abs(runs[n][key]-runs[m][key]),epsdecodecov+tol['ode'])
            comparisons.append(row)
    # Algebraic negative controls; no extra trajectory/campaign.
    low=models[2];high=models[3];inc=env['include'](low,high)
    amp=low['ai'][low['index'][(1,0,0)],low['index'][(2,0,0)]]
    check('sqrt_two_correct',abs(amp-math.sqrt(2)))
    check('negative_Pauli_unit_coefficient',abs(amp-1),tol['negative'],True)
    Xhigh=(high['ai']+high['ai'].conj().T)/math.sqrt(2)
    Xlow=(low['ai']+low['ai'].conj().T)/math.sqrt(2)
    top=low['index'][(2,0,0)]
    projected_second=(inc.conj().T@Xhigh@Xhigh@inc)[top,top]
    squared_projection=(Xlow@Xlow)[top,top]
    check('projected_second_on_n2',abs(projected_second-2.5))
    check('negative_square_after_projection',abs(projected_second-squared_projection),tol['negative'],True)
    shot=[.5*g*g for g in gains]
    for j,x in enumerate(shot):check('negative_omitted_shot_'+str(j),x,tol['negative'],True)
    def safe(run):return {'rows':run['rows'],**{k:enc(run[k]) for k in ['C','B','C_centered','B_centered']},'nfev':run['nfev']}
    return {'passed':all(x['passed'] for x in checks),'status':'PASS_CONTROLLED_BOSONIC_FILTERED_MOMENTS' if all(x['passed'] for x in checks) else 'FAIL_CONTROLLED_BOSONIC_FILTERED_MOMENTS','checks':checks,'runs':{str(m):safe(v) for m,v in runs.items()},'rotating_run':safe(rot),'analytical_error_certificates':certificates,'cut_comparisons':comparisons,'controls':{'lowering_n2':enc(amp),'projected_second':enc(projected_second),'square_of_projection':enc(squared_projection),'shot_variances':shot},'beta_runtime_INPUT':beta,'Gamma_INPUT':original['model']['gamma_Lambda'],'lambda_INPUT':lam,'versions':{'numpy':np.__version__,'scipy':scipy.__version__},'limits':['Total bosonic excitation cuts, not independent Pauli cuts.','First and second filtered moments plus derived covariances only; no infinite HP unitary/process existence claimed.','Upper cut is not an exact infinite solution; each cut has an analytical error bound.','Four separate LO settings with R64 Markov-vacuum monitored instrument; coherent OH pump retained.','All parameters dimensionless INPUT; no independent Gamma calibration, observed data, Lean, production or gate.']}
