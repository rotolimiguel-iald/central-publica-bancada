"""Continuous time, frequency and graviton reading in the explicit M2 model.

This source is intended to be embedded in the isolated um.py v394 candidate.
Synthetic calculations verify a specified finite model, not observed nature.
The operator's inscriptions are embedded separately with their own provenance.
"""


def _v394_finite(value, name, positive=False, nonnegative=False):
    import math
    import numbers
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        raise ValueError(name + ": finite real scalar required, not boolean")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(name + ": nonfinite scalar")
    if positive and value <= 0:
        raise ValueError(name + ": positive scalar required")
    if nonnegative and value < 0:
        raise ValueError(name + ": nonnegative scalar required")
    return value


def _v394_matrix(value, name, density=False):
    import numpy as np
    a = np.asarray(value, dtype=complex)
    if a.shape != (2, 2) or not np.isfinite(a).all():
        raise ValueError(name + ": finite 2 by 2 matrix required")
    if density:
        if np.linalg.norm(a-a.conj().T) > 1e-11 or abs(np.trace(a)-1) > 1e-11:
            raise ValueError(name + ": Hermitian trace-one state required")
        if np.linalg.eigvalsh(a).min() < -1e-11:
            raise ValueError(name + ": positive state required")
    return a


def _v394_geometry():
    import numpy as np
    i = np.eye(2, dtype=complex)
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    k = np.array([[0, 1], [-1, 0]], dtype=complex)
    ep = np.array([1, 1j], dtype=complex)
    em = np.conj(ep)
    pp, pm = np.outer(ep, ep.conj())/2, np.outer(em, em.conj())/2
    hp, hm = np.outer(ep, ep), np.outer(em, em)
    c = np.diag([1, 1j])
    original = np.array([1, 1j])/np.sqrt(2)
    state = c @ original
    return dict(I=i, X=x, Y=y, K=k, C=c, Pplus=pp, Pminus=pm,
                hplus=hp, hminus=hm, plus=ep/np.sqrt(2), minus=em/np.sqrt(2),
                rho0=np.outer(state, state.conj()))


def _v394_read(a):
    a = _v394_matrix(a, "reading input")
    g = _v394_geometry()
    return g['Pplus'] @ a @ g['Pplus'] + g['Pminus'] @ a @ g['Pminus']


def _v394_channel(a, t, omega, gamma):
    import math
    a = _v394_matrix(a, "channel input")
    t = _v394_finite(t, 'time', nonnegative=True)
    omega = _v394_finite(omega, 'angular frequency', positive=True)
    gamma = _v394_finite(gamma, 'rate', nonnegative=True)
    angle = omega*t
    exposure = gamma*t
    if not math.isfinite(angle) or not math.isfinite(exposure):
        raise ValueError('derived angle or exposure overflow')
    g = _v394_geometry()
    unitary = math.cos(angle)*g['I'] + math.sin(angle)*g['K']
    reading = _v394_read(a)
    out = unitary @ (reading + math.exp(-exposure)*(a-reading)) @ unitary.conj().T
    return _v394_matrix(out, 'channel output')


def _v394_rule(state, target, tolerance=1e-10):
    import numpy as np
    state = _v394_matrix(state, 'state', density=True)
    target = _v394_matrix(target, 'target', density=True)
    tolerance = _v394_finite(tolerance, 'rule tolerance', positive=True)
    if tolerance > 1e-6:
        raise ValueError('rule tolerance exceeds pinned ceiling')
    if np.linalg.norm(_v394_read(target)-target) > tolerance:
        raise ValueError('target is not a fixed reading')
    residual = float(np.linalg.norm(_v394_read(state)-target))
    return {'admitted': residual <= tolerance, 'residual': residual,
            'tolerance': tolerance, 'target_fixed_before_evolution': True}


def _v394_clock_modulus(c0, c1, gamma):
    import math
    import numbers
    gamma = _v394_finite(gamma, 'rate for modulus clock', positive=True)
    for z in (c0, c1):
        if isinstance(z, bool) or not isinstance(z, numbers.Complex) or not math.isfinite(z.real) or not math.isfinite(z.imag) or abs(z) == 0:
            raise ValueError('nonzero finite coherence required')
    result = -(math.log(abs(c1))-math.log(abs(c0)))/gamma
    if not math.isfinite(result) or result < -1e-10/gamma:
        raise ValueError('coherence does not represent forward decay')
    return max(0., result)


def _v394_clock_phase(phase_lift, omega):
    # phase_lift is an explicitly unwrapped phase difference, not principal Arg.
    phase_lift = _v394_finite(phase_lift, 'unwrapped phase difference')
    omega = _v394_finite(omega, 'angular frequency', positive=True)
    if phase_lift < 0:
        raise ValueError('positive-helicity forward phase lift required')
    result = (phase_lift/omega)*0.5 if phase_lift <= omega else (phase_lift*0.5)/omega
    import math
    if not math.isfinite(result) or (phase_lift > 0 and result <= 0):
        raise ValueError('phase clock overflow or underflow')
    return result


def _v394_independent_liouvillian(energies_j, v0_j, hbar_js, beta):
    import numpy as np
    lo, hi = energies_j
    g = _v394_geometry()
    h = lo*g['Pplus'] + hi*g['Pminus']
    jump = (beta/hbar_js)**.5 * (lo**.5*g['Pplus'] + hi**.5*g['Pminus'])
    gram = jump.conj().T @ jump
    eye = g['I']
    return (-1j/hbar_js*(np.kron(eye, h)-np.kron(h.T, eye))
            + np.kron(jump.conj(), jump)
            - .5*np.kron(eye, gram)-.5*np.kron(gram.T, eye))


def v394_time_frequency_checks(parameter_function, alpha, hbar):
    """Numerically cross-check matrix law against independently exponentiated GKLS.

    The caller supplies the independently typed physical-parameter constructor.
    Values are synthetic reference energies, never fitted to observed data.
    """
    import math
    import numpy as np
    from scipy.linalg import expm
    g = _v394_geometry()
    checks = []
    maxima = {}
    def check(name, condition, residual=None, tolerance=None):
        ok = bool(condition)
        if residual is not None:
            ok = ok and math.isfinite(float(residual))
        checks.append(dict(name=name, ok=ok, residual=residual, tolerance=tolerance))
    def close(name, a, b, tol=2e-10):
        r = float(np.linalg.norm(a-b))
        check(name, r <= tol, r, tol)
        maxima[name.split(':')[0]] = max(r, maxima.get(name.split(':')[0], 0.))
    close('matrix:C_X_Cstar',g['C']@g['X']@g['C'].conj().T,g['Y'])
    close('matrix:C_Px_Cstar',g['C']@((g['I']+g['X'])/2)@g['C'].conj().T,g['Pplus'])
    close('matrix:graviton_factor',g['hplus']@g['hminus']/4,g['Pplus'])
    close('matrix:tensor_square_is_not_matrix_square',g['hplus']@g['hplus'],np.zeros((2,2)))
    close('matrix:state_transport',g['rho0'],(g['I']-g['X'])/2)
    close('matrix:fixed_target',_v394_read(g['rho0']),g['I']/2)
    target = g['I']/2  # Pinned independently of outputs.
    rng=np.random.default_rng(20261015)
    states=[g['rho0'],g['Pplus'],g['Pminus'],target]
    for _ in range(8):
        z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)); rho=z@z.conj().T
        states.append(rho/np.trace(rho))
    summaries=[]
    for omega_ref in (.25,1.,3.,10.):
        for offset in (1.,2.,100.):
            p=parameter_function(omega_ref*hbar,offset*omega_ref*hbar,hbar,alpha)
            omega=p['Omega_rad_s']; gamma=p['gamma_s_inv']; beta=p['beta']
            label=f'{omega_ref}:{offset}'
            check('physical:beta_runtime:'+label,abs(beta-alpha*math.sqrt(math.e))<1e-16)
            # Fixed reference time t=1/Omega, not a fitted energy/time datum.
            v0=omega_ref*hbar
            hg=1j*v0*g['K']
            close('hamiltonian:transport:'+label,g['C']@(-v0*g['X'])@g['C'].conj().T/hbar,hg/hbar)
            liouv=_v394_independent_liouvillian(p['energies_J'],v0,hbar,beta)
            check('physical:rate_bound:'+label,0<gamma/(2*omega)<=beta/2+1e-14)
            if offset==1: close('physical:ground_rate:'+label,gamma, beta*omega)
            tgrid=[0.,.2/omega,1/omega,2*math.pi/omega,10/omega,40/omega]
            max_ind=0.
            for j,t in enumerate(tgrid):
                for i,rho in enumerate(states):
                    y=_v394_channel(rho,t,omega,gamma)
                    independent=(expm(t*liouv)@rho.reshape(-1,order='F')).reshape((2,2),order='F')
                    max_ind=max(max_ind,float(np.linalg.norm(y-independent)))
                    close('gkls:'+label+f':{j}:{i}',y,independent)
                    close('reading:'+label+f':{j}:{i}',_v394_read(y),_v394_read(rho))
                    close('semigroup:'+label+f':{j}:{i}',_v394_channel(_v394_channel(rho,t*.37,omega,gamma),t*.63,omega,gamma),y)
                    close('trace:'+label+f':{j}:{i}',np.trace(y),1.)
                    check('positivity:'+label+f':{j}:{i}',float(np.linalg.eigvalsh(y).min())>=-1e-10)
                    close('energy:'+label+f':{j}:{i}',np.trace((hg/v0)@y),np.trace((hg/v0)@rho))
                c0=g['plus'].conj()@g['rho0']@g['minus']
                c1=g['plus'].conj()@_v394_channel(g['rho0'],t,omega,gamma)@g['minus']
                expected=np.exp((-gamma+2j*omega)*t)*c0
                close('coherence:'+label+f':{j}',c1,expected)
                close('clock_modulus:'+label+f':{j}',_v394_clock_modulus(c0,c1,gamma)*omega,t*omega,tol=1e-8)
                close('clock_phase:'+label+f':{j}',_v394_clock_phase(2*omega*t,omega)*omega,t*omega,tol=1e-11)
                check('rule:admit:'+label+f':{j}',_v394_rule(_v394_channel(g['rho0'],t,omega,gamma),target)['admitted'])
                check('rule:reject:'+label+f':{j}',not _v394_rule(_v394_channel(g['rho0'],t,omega,gamma),g['Pplus'])['admitted'])
            echo_dt=p['echo_dt_s'];eta=p['eta']
            close('echo:continuous_coherence_factor:'+label,math.exp(-gamma*echo_dt),eta,tol=1e-12)
            raw=np.array([[.2,.3+.4j],[-.7+.5j,1.2]],dtype=complex)
            for mode,sign in ((g['hplus'],1),(g['hminus'],-1)):
                got=(liouv@mode.reshape(-1,order='F')).reshape((2,2),order='F')
                close('generator:mode:'+label+':'+str(sign),got/omega,((-gamma+sign*2j*omega)*mode)/omega)
            t=1/omega
            choi=np.zeros((4,4),dtype=complex)
            for a in range(2):
                for b in range(2):
                    e=np.zeros((2,2),dtype=complex);e[a,b]=1
                    choi+=np.kron(e,_v394_channel(e,t,omega,gamma))
            check('choi:'+label,float(np.linalg.eigvalsh(choi).min())>=-1e-10)
            close('nonmultiplicative:correct_factor:'+label,
                  _v394_channel(g['hplus'],t,omega,gamma)@_v394_channel(g['hminus'],t,omega,gamma)/4,
                  math.exp(-2*gamma*t)*g['Pplus'])
            check('nonmultiplicative:counterexample:'+label,
                  np.linalg.norm(_v394_channel(g['hplus'],t,omega,gamma)@_v394_channel(g['hminus'],t,omega,gamma)/4-g['Pplus'])>1e-8)
            check('fixed_space:dimension2:'+label,int(np.count_nonzero(np.linalg.svd(liouv/omega,compute_uv=False)<1e-10))==2)
            long_t=12/gamma
            close('decay:asymptotic_norm:'+label,
                  np.linalg.norm(_v394_channel(g['rho0'],long_t,omega,gamma)-target),
                  math.exp(-12)*np.linalg.norm(g['rho0']-target),tol=1e-12)
            pp=parameter_function(2*v0,2*offset*v0,hbar,alpha)
            close('clock:rescaling:'+label,_v394_channel(raw,t,omega,gamma),
                  _v394_channel(raw,t/2,pp['Omega_rad_s'],pp['gamma_s_inv']))
            summaries.append(dict(omega_rad_s=omega,offset_ratio=offset,gamma_s_inv=gamma,
                                  echo_dt_s=echo_dt,gamma_over_relative_frequency=gamma/(2*omega),max_gkls_residual=max_ind))
    close('clock_phase:overflow_avoided',_v394_clock_phase(1e308,1e308),.5)
    # Controls test genuine failures, independent of the main verdict.
    def refused(name,fn):
        try: fn()
        except (ValueError,TypeError,OverflowError): check(name,True)
        else: check(name,False)
    for bad in (True,float('nan'),float('inf'),-1):
        refused('negative_input:time:'+repr(bad),lambda bad=bad:_v394_channel(g['rho0'],bad,1.,.1))
        refused('negative_input:rate:'+repr(bad),lambda bad=bad:_v394_channel(g['rho0'],1.,1.,bad))
    refused('clock_phase:unrepresentable',lambda:_v394_clock_phase(1.,5e-324))
    refused('clock_phase:underflow',lambda:_v394_clock_phase(5e-324,1e308))
    refused('negative_input:zero_coherence',lambda:_v394_clock_modulus(0j,.2j,.1))
    refused('negative_input:zero_rate_clock',lambda:_v394_clock_modulus(.3j,.2j,0))
    refused('negative_input:increasing_coherence',lambda:_v394_clock_modulus(.1j,.2j,.1))
    refused('negative_input:nonfixed_target',lambda:_v394_rule(g['rho0'],g['rho0']))
    close('zero_rate:no_convergence',np.linalg.norm(_v394_channel(g['rho0'],7.,1.,0.)-target),np.linalg.norm(g['rho0']-target))
    # Same samples, different intermediate phases: a negative uniqueness control.
    tstep=.7;omega=1.;alias=omega+math.pi/tstep
    close('alias:sample_agrees',_v394_channel(g['rho0'],tstep,omega,.1),_v394_channel(g['rho0'],tstep,alias,.1))
    check('alias:between_samples_differs',np.linalg.norm(_v394_channel(g['rho0'],tstep/2,omega,.1)-_v394_channel(g['rho0'],tstep/2,alias,.1))>.1)
    return {'passed':all(c['ok'] for c in checks),'checks':checks,'check_count':len(checks),
            'failed':[c for c in checks if not c['ok']],'maxima':maxima,'parameter_cases':summaries,
            'scope':'Synthetic M2 calculation with explicit positive energy reference. No observed data, no universal atomic identification.',
            'gate_changed':False}


def tempo_frequencia_v394(core):
    """Actual v394 consumer: formal evidence and runtime jointly determine verdict."""
    import hashlib
    report=core.get('kernel_formalization') or {}
    axioms=report.get('axiom_report') or {}
    trio={'propext','Classical.choice','Quot.sound'}
    required=_V394_FORMAL_CONTRACT['theorems']
    expected=_V394_FORMAL_CONTRACT['expected_ladder']
    clean=report.get('n_theorems_clean'); counted=report.get('n_theorems_expected')
    exact_ladder=(type(expected) is int and type(clean) is int and type(counted) is int
                  and clean == counted == expected)
    formal=bool(required) and report.get('all_verified') is True and exact_ladder
    per={}
    for theorem in required:
        values=axioms.get(theorem)
        per[theorem]=isinstance(values,list) and all(isinstance(x,str) for x in values) and set(values)<=trio
        formal=formal and per[theorem]
    embedded={}
    for rel,sha in _V394_FORMAL_CONTRACT['source_sha256'].items():
        body=_EMBEDDED_KERNEL_FILES.get(rel)
        embedded[rel]=isinstance(body,str) and hashlib.sha256(body.encode('utf-8')).hexdigest()==sha
    formal=formal and bool(embedded) and all(embedded.values())
    inscriptions={k:hashlib.sha256(v['text'].encode('utf-8')).hexdigest()==v['sha256'] for k,v in _V394_INSCRIPTIONS.items()}
    if not formal or not inscriptions or not all(inscriptions.values()):
        out={'all_verified':False,'verdict':'TGL_TIME_FREQUENCY_V394__REFUSED_FORMAL_OR_SOURCE_EVIDENCE__GATE_UNMOVED',
             'exact_ladder':exact_ladder,'formal_theorems':per,'embedded_sources':embedded,'inscriptions':inscriptions,'runtime_executed':False,'does_not_gate_core':True}
    else:
        try:
            result=v394_time_frequency_checks(v394_physical_parameters,SEALED_CODATA_ALPHA,HBAR_EXACT)
            ok=result['passed']
            out={'all_verified':ok,'verdict':'TGL_TIME_FREQUENCY_V394__'+('DERIVED_M2_CONTINUOUS_FLOW_AND_CLOCK' if ok else 'RUNTIME_CHECK_FAILED')+'__GATE_UNMOVED',
                 'exact_ladder':exact_ladder,'formal_theorems':per,'embedded_sources':embedded,'inscriptions':inscriptions,'runtime_executed':True,
                 'runtime':result,'does_not_gate_core':True,
                 'scope':'Compiled finite-model composition and synthetic GKLS verification; physical inputs and sector-identification limits remain explicit.'}
        except Exception as exc:
            out={'all_verified':False,'verdict':'TGL_TIME_FREQUENCY_V394__RUNTIME_ERROR__GATE_UNMOVED','error':repr(exc),
                 'exact_ladder':exact_ladder,'formal_theorems':per,'runtime_executed':True,'does_not_gate_core':True}
    core['tempo_frequencia_v394']=out
    return out
