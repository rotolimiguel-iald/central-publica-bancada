"""Initial P1 functionals from filtered output effects; conditional observability, not tomography."""
from pathlib import Path
import ast,json,math

def calculate(plan):
    import numpy as np
    import scipy
    from scipy import sparse as sp
    from scipy.sparse.linalg import expm_multiply
    src={x['role']:Path(x['path']) for x in plan['sources']}
    prior=json.loads(src['r62_plan'].read_text(encoding='utf-8'));parameters=prior['model']['parameters']
    constants={}
    for n in ast.parse(src['alpha'].read_text(encoding='utf-8')).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['ALPHA_FINE_CODATA_2018','_SEALED_ALPHA_CODATA_2018']:constants[n.targets[0].id]=ast.literal_eval(n.value)
    assert constants['ALPHA_FINE_CODATA_2018']==constants['_SEALED_ALPHA_CODATA_2018']
    beta=constants['ALPHA_FINE_CODATA_2018']*math.sqrt(math.e);lam=beta*prior['model']['gamma_Lambda']
    nodes=[n for n in ast.walk(ast.parse(src['r66_helpers'].read_text(encoding='utf-8'))) if isinstance(n,ast.FunctionDef) and n.name in ['liou','model','include']]
    assert len(nodes)==3;astcode=compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),str(src['r66_helpers']),'exec')
    checks=[];tol=plan['tolerances']
    def check(name,value,bound=None,negative=False):
        value=float(value);bound=tol['algebra'] if bound is None else bound
        checks.append({'name':name,'value':value,'bound':bound,'relation':'gt' if negative else 'le','passed':bool(math.isfinite(value) and math.isfinite(bound) and (value>bound if negative else value<=bound))})
    def vec(x):return x.reshape(-1,order='F')
    def unvec(x,d):return x.reshape((d,d),order='F')
    def opnorm(x):return float(np.max(np.abs(np.linalg.eigvalsh((x+x.conj().T)/2))))
    configs=[('XX',0.,0.),('PP',math.pi/2,math.pi/2),('XP',0.,math.pi/2),('PX',math.pi/2,0.)]
    pairs=[(0,0),(0,1),(1,1)];times=plan['windows'];Tf=plan['filter_horizon'];m=plan['cut'];m0=plan['initial_max_N']
    assert len(times)==3 and all(abs(t-(j+1)*times[-1]/3)<1e-15 for j,t in enumerate(times))
    def E(k,q):
        if k<0:return math.exp(q)
        ratio=q/(k+2)
        if not ratio<1:raise ValueError('Invalid tail-majorant denominator')
        return q**(k+1)/math.factorial(k+1)/(1-ratio)
    def bounds(p,t):
        q=2*abs(p['Omega'])*t;ed=E(m-m0,q);t2=m0*ed+q*E(m-m0-1,q);t1=math.sqrt(ed*t2)
        aa=[math.sqrt(2*p[key])*plan['gains'][j]*t/math.sqrt(Tf) for j,key in enumerate(['kappa_in','kappa_out'])]
        return [2*a*t1 for a in aa]+[2*aa[j]*aa[k]*t2 for j,k in pairs]
    def build_branch(zero_ports=False):
        p=dict(parameters)
        if zero_ports:p['kappa_in']=p['kappa_out']=0.
        env={'np':np,'sp':sp,'math':math,'p':p,'lam':lam};exec(astcode,env)
        mod=env['model'](m);small=env['model'](m0);inc=env['include'](small,mod);d=len(mod['basis']);d2=d*d
        assert len(small['basis'])==4
        states={}
        for item in plan['validation_states']:
            ket=np.zeros(4,complex)
            for a in item['terms']:ket[small['index'][tuple(a['basis'])]]=complex(*a['amplitude'])
            ket/=np.linalg.norm(ket);states[item['name']]=np.outer(ket,ket.conjugate())
        ni=np.diag([b[0] for b in small['basis']]);no=np.diag([b[1] for b in small['basis']]);ne=np.diag([b[2] for b in small['basis']])
        targets={'N_b':ni+no,'N_total':ni+no+ne}
        H=[]
        for i in range(4):h=np.zeros((4,4),complex);h[i,i]=1;H.append(h)
        for i in range(4):
            for j in range(i+1,4):
                h=np.zeros((4,4),complex);h[i,j]=h[j,i]=1/math.sqrt(2);H.append(h)
                h=np.zeros((4,4),complex);h[i,j]=-1j/math.sqrt(2);h[j,i]=1j/math.sqrt(2);H.append(h)
        effects=[np.eye(4,dtype=complex)];metadata=[{'name':'trace_identity','time':0.,'R75_bound':0.,'numerical_allowance_INPUT':0.}]
        observed={name:[1.] for name in states}
        for label,ti,to in configs:
            cs=[plan['gains'][j]*np.exp(-1j*theta)/math.sqrt(Tf) for j,theta in enumerate([ti,to])]
            M=[]
            for c,l in zip(cs,mod['jumps'][:2]):
                M.append((c*sp.kron(sp.eye(d),sp.csr_matrix(l))+c.conjugate()*sp.kron(sp.csr_matrix(l.conj()),sp.eye(d)))/math.sqrt(2))
            blocks=[[None]*6 for _ in range(6)]
            for j in range(6):blocks[j][j]=mod['g']
            blocks[1][0]=M[0];blocks[2][0]=M[1]
            for z,(j,k) in enumerate(pairs):
                row=3+z
                if j==k:blocks[row][1+j]=2*M[j];blocks[row][0]=.5*abs(cs[j])**2*sp.eye(d2)
                else:blocks[row][1+k]=M[j];blocks[row][1+j]=M[k]
            K=sp.bmat(blocks,format='csr')
            W=np.zeros((6*d2,5),complex)
            for j in range(5):W[(j+1)*d2:(j+2)*d2,j]=vec(np.eye(d))
            Y=np.zeros((6*d2,len(states)),complex)
            for j,rho in enumerate(states.values()):Y[:d2,j]=vec(inc@rho@inc.conj().T)
            # Three windows from a single equally spaced exponential sequence; no adaptive windows.
            dual=expm_multiply(K.conj().T,W,start=0.,stop=times[-1],num=4,endpoint=True)
            primal=expm_multiply(K,Y,start=0.,stop=times[-1],num=4,endpoint=True)
            for it,t in enumerate(times,1):
                delta=bounds(p,t)
                for j in range(5):
                    ef=inc.conj().T@unvec(dual[it,:d2,j],d)@inc
                    check(f'{zero_ports}_{label}_{t}_{j}_effect_hermitian',np.linalg.norm(ef-ef.conj().T),tol['algebra'])
                    ef=(ef+ef.conj().T)/2;effects.append(ef)
                    metadata.append({'name':label+'_'+['mean_i','mean_o','second_ii','second_io','second_oo'][j],'time':t,'R75_bound':delta[j],'numerical_allowance_INPUT':plan['numerical_allowance_INPUT']})
                    for k,(name,rho) in enumerate(states.items()):
                        y=np.trace(unvec(primal[it,(j+1)*d2:(j+2)*d2,k],d));pred=np.trace(ef@rho)
                        check(f'{zero_ports}_{label}_{t}_{j}_{name}_adjoint_primal',abs(y-pred),tol['primal_dual'])
                        observed[name].append(float(y.real))
        A=np.array([[np.trace(h@ef).real for ef in effects] for h in H])
        U,sv,Vh=np.linalg.svd(A,full_matrices=False);threshold=plan['rcond']*sv[0];rank=int(np.count_nonzero(sv>threshold))
        inverse=np.linalg.pinv(A,rcond=plan['rcond']);answers={}
        for target_name,target in targets.items():
            av=np.array([np.trace(h@target).real for h in H]);weights=inverse@av
            reconstructed=sum(w*ef for w,ef in zip(weights,effects));eta=opnorm(target-reconstructed)
            numerical=sum(abs(w)*row['numerical_allowance_INPUT'] for w,row in zip(weights,metadata))
            tail=sum(abs(w)*row['R75_bound'] for w,row in zip(weights,metadata))
            noise_l1=float(np.sum(np.abs(weights[1:])))
            # This is a named synthetic budget, not a claim of measured statistical uncertainty.
            statistical=noise_l1*plan['statistical_uncertainty_INPUT_per_feature']
            model_budget=noise_l1*plan['model_uncertainty_INPUT_per_feature']
            Delta=eta+plan['residual_allowance_INPUT']+tail+numerical+statistical+model_budget
            rows=[]
            for name,rho in states.items():
                value=float(weights@np.array(observed[name]));truth=float(np.trace(target@rho).real)
                check(f'{zero_ports}_{target_name}_{name}_finite_residual_bound',abs(value-truth),eta+numerical+tol['primal_dual'])
                lo=value-Delta;hi=value+Delta;consistent=bool(math.isfinite(lo) and math.isfinite(hi) and lo<=hi and hi>=0. and lo<=m0)
                interval=[max(0.,lo),min(float(m0),hi)] if consistent else None
                informative=bool(consistent and interval[1]<1.)
                lower=max(0.,1-interval[1]) if consistent else None
                rows.append({'state':name,'value':value,'true_initial_expectation':truth,'conditional_continuum_interval':interval,'interval_consistent':consistent,'informative_vacuum_certificate':informative,'vacuum_probability_lower_bound':lower,'verdict':'CONDITIONAL_INFORMATIVE_BOUND' if informative else ('INCONCLUSIVE' if consistent else 'REFUSED_INCONSISTENT_INTERVAL')})
            if zero_ports:check('negative_unobserved_ports_'+target_name,eta,tol['negative_residual'],True)
            answers[target_name]={'target_in_span_at_cut':bool(eta<=tol['target_residual']),'operator_residual':eta,'weight_L1':float(np.sum(np.abs(weights))),'noise_amplification_L1':noise_l1,'weights':weights.tolist(),'residual_numerical_allowance_INPUT':plan['residual_allowance_INPUT'],'amplified_R75_tail':tail,'amplified_numerical_allowance_INPUT':numerical,'amplified_statistical_INPUT':statistical,'amplified_model_INPUT':model_budget,'total_conditional_error':Delta,'validation_states':rows,'vacuum_scope':'two selected modes only, identity on OH' if target_name=='N_b' else 'two selected modes plus OH; initial P1 support hypothesis'}
        if zero_ports:
            for ef,row in zip(effects[1:],metadata[1:]):
                expected=.5*plan['gains'][0 if row['name'].endswith('ii') else 1]**2*row['time']/Tf if row['name'].endswith(('ii','oo')) else 0.
                check('zero_ports_effect_'+row['name']+'_'+str(row['time']),opnorm(ef-expected*np.eye(4)),tol['primal_dual'])
        return {'input_basis':[list(x) for x in small['basis']],'cut_dimension':d,'features':metadata,'rank':rank,'singular_values':sv.tolist(),'rcond':plan['rcond'],'svd_threshold':threshold,'targets':answers,'effects_16_real_coefficients':A.tolist(),'known_parameters_INPUT':p,'observed_synthetic_features':observed}
    normal=build_branch(False);zero=build_branch(True)
    return {'passed':all(c['passed'] for c in checks),'status':'PASS_CONDITIONAL_FUNCTIONAL_OBSERVABILITY_CHECKS' if all(c['passed'] for c in checks) else 'FAIL_FUNCTIONAL_OBSERVABILITY_CHECKS','checks':checks,'normal':normal,'zero_ports_control':zero,'beta_runtime_INPUT':beta,'Gamma_INPUT':prior['model']['gamma_Lambda'],'lambda_INPUT':lam,'versions':{'numpy':np.__version__,'scipy':scipy.__version__},'limits':['No rank/full-state success imposed; target residual and useful bound are separate outputs.','Initial state unknown only inside P1; N_b is initial cavity excitation, not final output intensity.','N_b identifies R72 local target only under the selected mode/unitary bridge.','Known synthetic rates include Gamma; no independent physical calibration or beta measurement.','Numerical allowance is INPUT, distinct from statistical uncertainty; no rigorous floating-point enclosure claimed.','R75 supplies first/second moment tails, not global HP realization.','No Lean, provider, production, gate or observed data.']}
