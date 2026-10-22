UM_VERSION = 'v394'
_EMBEDDED_KERNEL_FILES = {
    'TGLExt.lean': '-- preserved aggregator\n\nimport TimeFixture\n',
    'TGL/Audit.lean': 'import TimeFixture\n\n-- preserved audit\n',
    'TimeFixture.lean': 'theorem fixture : True := True.intro\n',
}
_LEAN_THEOREM_FLAGS = {
    'old_flag': 'Old.theorem',
    'ext_tf394_0001': 'fixture',
}
LINEAGE = [
    ('v393', 'RuleTruthContract', 'TGLExt/Old.lean', None, None),
    ('v394', 'TimeFixture', 'TimeFixture.lean', None, None),
]
def old_check(n_cl_, n_ex_):
    esc_ok_ = isinstance(n_cl_, int) and n_cl_ == n_ex_ and n_cl_ >= _V393_ESCADA["esperada"]  # v394: preserve historical floor; current exact ladder is checked by v394
    return esc_ok_
def emit_article(core):
    pt = _v394_article_tex(build_pt(core), core, 'pt')
    en = _v394_article_tex(build_en(core), core, 'en')
    return pt,en
def seal(core):
    return {
            "registros_v393": {},
            "tempo_frequencia_v394": {k_: (core.get("tempo_frequencia_v394") or {}).get(k_) for k_ in ("verdict", "all_verified", "formal_theorems", "embedded_sources", "inscriptions", "runtime_executed", "scope", "does_not_gate_core")},
    }


# v394: isolated candidate composition, operator order 15/10/2026.
_V394_FORMAL_CONTRACT = {'theorems': ['fixture'], 'source_sha256': {'TimeFixture.lean': '91c1da8bcac044c3a23fbae0a48f21077d701c527140356eebbc46cfbce1b5d8'}, 'expected_ladder': 2, 'baseline_version': 'v393', 'baseline_sha256': 'b789ed585ac29bb19999452fd4513a3f8a982a78796dc27ce52906e0641432c9'}
_V394_INSCRIPTIONS = {'OPERADOR_IGUALDADE_VERBATIM': {'text': 'Essa operação é o sinal de “=“, ou seja, o “gráviton”, o tempo conta o reconhecimento da transformação sobre a preservada identidade; quando o verbo opera sobre o nome a palavra reconhece pela operação da verdade, ou seja, a relação de contorno que determina o espectro de gradiente negativo anulando todas as hipóteses de identidade que não satisfaçam a verdade do enunciado;', 'sha256': '721482ae120ec6f19acf46d2a297da0174d3cc2d9fba4c3722320c40bcef9493', 'source_informative_only': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_019\\F1.TEMPO.V394\\runtime_review\\integration_fixture\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_019\\F1.TEMPO.LEITURA_20261015\\IGUALDADE_RECONHECIMENTO_R8\\OPERADOR_IGUALDADE_VERBATIM.txt', 'statute': 'INPUT/ONTO operator verbatim'}, 'OPERADOR_FREQUENCIA_VERBATIM': {'text': 'Perfeito, agora é ligar na frequência, prossiga', 'sha256': '6e8daf2f2d45c0e7de444eaec1200d6794c8ccfe8b543b90e59626730e1210e5', 'source_informative_only': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_019\\F1.TEMPO.V394\\runtime_review\\integration_fixture\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_019\\F1.TEMPO.LEITURA_20261015\\FREQUENCIA_E_GRAVITON_R9\\OPERADOR_FREQUENCIA_VERBATIM.txt', 'statute': 'INPUT/ONTO operator verbatim'}, 'OPERADOR_PONTE_EXISTENTE_VERBATIM': {'text': 'Você precisa ligar com o objeto gravitacional e construir a ponte, mas eu já a fiz, é só ligar', 'sha256': '2140cf2efeba9e15c3c0acb3ef8638faf547282117af11621297ea2e657422b8', 'source_informative_only': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_019\\F1.TEMPO.V394\\runtime_review\\integration_fixture\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_019\\F1.TEMPO.LEITURA_20261015\\FREQUENCIA_E_GRAVITON_R9\\OPERADOR_PONTE_EXISTENTE_VERBATIM.txt', 'statute': 'INPUT/ONTO operator verbatim'}, 'OPERADOR_ENVIO_V394_VERBATIM': {'text': 'Você precisa passar tudo isso ao Claude para a v 394, e mais, o que ainda falta provar, porque agora resolvemos por\nCompleto a passagem\nDo contínuo , não é mais condicional, é derivado', 'sha256': '185e3b8e82bd06287cec978c07b279d6a0af72fcb2bc5b02e11f99f5d34c0365', 'source_informative_only': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_019\\F1.TEMPO.V394\\runtime_review\\integration_fixture\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_019\\F1.TEMPO.LEITURA_20261015\\ENCAMINHAMENTO_V394_20261015\\OPERADOR_ENVIO_V394_VERBATIM.txt', 'statute': 'INPUT/ONTO operator verbatim'}}

"""Finite positive-energy contract for F1.TEMPO.V394; safe to embed in um.py.

DERIVED in the specified two-level model; no universal energy-zero calibration.
The zero-ground case Eref=V0 is a synthetic instance, not an atomic-clock claim.
Only the functions below execute, when called; no file, network or device I/O.
"""


class V394PhysicalContractError(ValueError):
    """A nonphysical or unrepresentable parameter was refused visibly."""


def _v394_finite_real(name, value, *, positive=False, nonnegative=False):
    import math
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise V394PhysicalContractError(name + ": finite non-boolean real required")
    try:
        number = float(value)
    except (ValueError, OverflowError) as exc:
        raise V394PhysicalContractError(name + ": float conversion failed") from exc
    if not math.isfinite(number):
        raise V394PhysicalContractError(name + ": nonfinite value")
    if positive and number <= 0:
        raise V394PhysicalContractError(name + ": strictly positive value required")
    if nonnegative and number < 0:
        raise V394PhysicalContractError(name + ": nonnegative value required")
    return number


def v394_physical_parameters(V0_J, Eref_J, hbar_J_s=None, alpha=None):
    """Return exact-form model parameters in one SI clock, evaluated as floats.

    Hg=-V0*sigma_y; Hpos=Eref*I+Hg; spectrum Eref+-V0, Eref>=V0.
    Root law: D[sqrt(beta/hbar)*sqrt(Hpos)]. Its off-diagonal rate is
    gamma=beta/(2*hbar)*(sqrt(Eref+V0)-sqrt(Eref-V0))**2.
    The rationalized expression below avoids cancellation for large Eref/V0.
    tau_eff matches the quadratic law for THIS gap only. echo_dt constructs
    a matched echo step; it does not replace the old echo's frozen dt=0.35.
    Floats with under/overflow in a strictly positive output are refused.
    """
    import math
    if hbar_J_s is None:
        hbar_J_s = 6.62607015e-34 / (2.0 * math.pi)
    if alpha is None:
        alpha = 7.2973525693e-3  # ALPHA_FINE_CODATA_2018 in the pinned source.
    v = _v394_finite_real("V0_J", V0_J, positive=True)
    e = _v394_finite_real("Eref_J", Eref_J, positive=True)
    hb = _v394_finite_real("hbar_J_s", hbar_J_s, positive=True)
    a = _v394_finite_real("alpha", alpha, positive=True)
    if e < v:
        raise V394PhysicalContractError("Eref_J must be >= V0_J for Hpos >= 0")
    beta = _v394_finite_real("beta", a * math.sqrt(math.e), positive=True)
    if beta >= 1.0:
        raise V394PhysicalContractError("0 < beta < 1 required")
    eta = _v394_finite_real("eta", 2.0 * math.sqrt(beta) * math.sqrt(1.0-beta), positive=True)
    if eta >= 1.0:
        raise V394PhysicalContractError("echo has no strictly contractive representable eta")
    omega = _v394_finite_real("Omega_rad_s", v / hb, positive=True)
    frequency = _v394_finite_real("coherence_omega_rad_s", 2.0 * omega, positive=True)
    q = _v394_finite_real("V0_over_Eref", v / e, positive=True)
    denominator = 1.0 + math.sqrt(max(0.0, (1.0-q)*(1.0+q)))
    ratio = _v394_finite_real("root_rate_ratio", q / denominator, positive=True)
    gamma = _v394_finite_real("gamma_s_inv", (beta * omega) * ratio, positive=True)
    tau = _v394_finite_real("tau_eff_s", (hb / e) / (2.0 * denominator), positive=True)
    echo_dt = _v394_finite_real("echo_dt_s", -math.log(eta) / gamma, positive=True)
    lo = _v394_finite_real("energy_lower_J", e-v, nonnegative=True)
    hi = _v394_finite_real("energy_upper_J", e+v, positive=True)
    return {
        "beta": beta, "Omega_rad_s": omega,
        "coherence_omega_rad_s": frequency, "gamma_s_inv": gamma,
        "tau_eff_s": tau, "echo_dt_s": echo_dt, "eta": eta,
        "energies_J": [lo, hi], "V0_J": v, "Eref_J": e,
        "hbar_J_s": hb, "alpha": a, "root_rate_ratio": ratio,
        "energy_representation": {
            "exact_from_inputs": "Eref_J plus/minus V0_J",
            "rounded_endpoints_coincide": lo == hi,
            "calculation_uses_center_and_half_gap": True,
        },
        "scope": "DERIVED_FINITE_TWO_LEVEL_POSITIVE_ENERGY__NOT_UNIVERSAL_CALIBRATION",
        "ground_zero_instance": e == v,
        "mu_do_rito": "q->0 (Thomson; Teorema da Escala)",
    }


def v394_kms_clock(parameters, kappa_s_inv):
    """Finite Gibbs/KMS clock bridge; not an inhabitant of the full light H2.

    sigma_s^rho=alpha_(-P*s), P=2*pi/kappa, alpha is Heisenberg evolution.
    P is the KMS inverse-temperature time, not a real-time recurrence claim.
    No inference kappa=Omega is made. A supplied kappa fixes the clock.
    """
    import math
    if not isinstance(parameters, dict):
        raise V394PhysicalContractError("parameters must be a dictionary")
    for key in ("V0_J", "Eref_J", "hbar_J_s", "alpha"):
        if key not in parameters:
            raise V394PhysicalContractError("missing parameter: " + key)
    # Recompute from physical inputs: a caller cannot inject a forged derived rate.
    p = v394_physical_parameters(parameters["V0_J"], parameters["Eref_J"],
                                parameters["hbar_J_s"], parameters["alpha"])
    kappa = _v394_finite_real("kappa_s_inv", kappa_s_inv, positive=True)
    period = _v394_finite_real("kms_period_s", (2.0 * math.pi) / kappa, positive=True)
    gap = _v394_finite_real("gibbs_gap_exponent", period * p["coherence_omega_rad_s"], positive=True)
    weight_hi = math.exp(-gap)
    if weight_hi == 0.0:
        raise V394PhysicalContractError("finite Gibbs state underflow would lose numerical faithfulness")
    z = 1.0 + weight_hi
    return {
        "kappa_s_inv": kappa, "kms_period_s": period,
        "temperature_K": _v394_finite_real("temperature_K", (p["hbar_J_s"] / period) / 1.380649e-23, positive=True),
        "Omega_over_kappa": _v394_finite_real("Omega_over_kappa", p["Omega_rad_s"] / kappa, positive=True),
        "gibbs_weights_low_high": [1.0/z, weight_hi/z],
        "modular_parameter_per_second": _v394_finite_real("modular_parameter_per_second", 1.0/period, positive=True),
        "relation": "sigma_s = alpha_(-P*s); alpha_t = sigma_(-t/P)",
        "scope": "FINITE_GIBBS_CONSTRUCTION__H2_RESCALE_FORM_REUSED__NO_LIGHT_NET_EMBEDDING_ASSERTED",
    }

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
    return phase_lift/(2*omega)


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
    # Controls test genuine failures, independent of the main verdict.
    def refused(name,fn):
        try: fn()
        except (ValueError,TypeError,OverflowError): check(name,True)
        else: check(name,False)
    for bad in (True,float('nan'),float('inf'),-1):
        refused('negative_input:time:'+repr(bad),lambda bad=bad:_v394_channel(g['rho0'],bad,1.,.1))
        refused('negative_input:rate:'+repr(bad),lambda bad=bad:_v394_channel(g['rho0'],1.,1.,bad))
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
    formal=bool(required) and report.get('all_verified') is True
    per={}
    for theorem in required:
        values=axioms.get(theorem)
        per[theorem]=isinstance(values,list) and set(values)<=trio
        formal=formal and per[theorem]
    embedded={}
    for rel,sha in _V394_FORMAL_CONTRACT['source_sha256'].items():
        body=_EMBEDDED_KERNEL_FILES.get(rel)
        embedded[rel]=isinstance(body,str) and hashlib.sha256(body.encode('utf-8')).hexdigest()==sha
    formal=formal and bool(embedded) and all(embedded.values())
    inscriptions={k:hashlib.sha256(v['text'].encode('utf-8')).hexdigest()==v['sha256'] for k,v in _V394_INSCRIPTIONS.items()}
    if not formal or not inscriptions or not all(inscriptions.values()):
        out={'all_verified':False,'verdict':'TGL_TIME_FREQUENCY_V394__REFUSED_FORMAL_OR_SOURCE_EVIDENCE__GATE_UNMOVED',
             'formal_theorems':per,'embedded_sources':embedded,'inscriptions':inscriptions,'runtime_executed':False,'does_not_gate_core':True}
    else:
        try:
            result=v394_time_frequency_checks(v394_physical_parameters,SEALED_CODATA_ALPHA,HBAR_EXACT)
            ok=result['passed']
            out={'all_verified':ok,'verdict':'TGL_TIME_FREQUENCY_V394__'+('DERIVED_M2_CONTINUOUS_FLOW_AND_CLOCK' if ok else 'RUNTIME_CHECK_FAILED')+'__GATE_UNMOVED',
                 'formal_theorems':per,'embedded_sources':embedded,'inscriptions':inscriptions,'runtime_executed':True,
                 'runtime':result,'does_not_gate_core':True,
                 'scope':'Compiled finite-model composition and synthetic GKLS verification; physical inputs and sector-identification limits remain explicit.'}
        except Exception as exc:
            out={'all_verified':False,'verdict':'TGL_TIME_FREQUENCY_V394__RUNTIME_ERROR__GATE_UNMOVED','error':repr(exc),
                 'formal_theorems':per,'runtime_executed':True,'does_not_gate_core':True}
    core['tempo_frequencia_v394']=out
    return out


def _v394_article_tex(text, core, lang):
    """Append the actual current-run result and scoped mathematics in both languages."""
    out = core.get('tempo_frequencia_v394') or {}
    pt = lang == 'pt'
    title = 'Tempo, frequencia e leitura gravitacional: composicao v394' if pt else 'Time, frequency and gravitational reading: v394 composition'
    def esc(value):
        replacements = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
        return ''.join(replacements.get(ch, ch) for ch in str(value))
    block = '\n\\section*{' + title + '}\n'
    block += ('Resultado desta rodada: ' if pt else 'Result of this run: ') + esc(out.get('verdict', 'NOT_RUN')) + '.\n\n'
    block += (r'No modelo $M_2$, a conjugacao $C=\mathrm{diag}(1,i)$ realiza a ponte espectral: $H_g=CH_{lig}C^\dagger=iV_0K$, $\Omega=V_0/\hbar$. O fluxo continuo e seu relogio sao derivados para estes objetos. ' if pt else
              r'In the $M_2$ model, conjugation $C=\mathrm{diag}(1,i)$ realizes the spectral bridge: $H_g=CH_{lig}C^\dagger=iV_0K$, $\Omega=V_0/\hbar$. The continuous flow and its clock are derived for these objects. ')
    block += r'\[T_t(X)=U_t\{E_g(X)+e^{-\gamma t}[X-E_g(X)]\}U_t^\dagger,\qquad E_gT_t=E_g.\]' + '\n'
    block += r'\[c(t)=e^{(-\gamma+2i\Omega)t}c(0),\qquad\Delta t=\frac{\Delta\phi}{2\Omega}=-\frac{\log|c(t_2)/c(t_1)|}{\gamma}.\]' + '\n'
    block += ('As duas leituras de tempo exigem coerencia nao nula, gamma positivo e fase levantada. O espaco fixo tem dimensao complexa dois. A fase isolada admite alias; leitura preservada nao e preservacao de todo produto.\n\n' if pt else
              'The two clock readings require nonzero coherence, positive gamma and a lifted phase. The fixed space has complex dimension two. A single phase admits aliases; preserved reading does not preserve every product.\n\n')
    block += r'\[H_{pos}=E_{ref}I+H_g,\quad E_{ref}\ge V_0,\quad\gamma=\frac{\beta}{2\hbar}\left(\sqrt{E_{ref}+V_0}-\sqrt{E_{ref}-V_0}\right)^2.\]' + '\n'
    block += ('A referencia energetica e parte do contrato fisico. O caso Eref=V0 e uma instancia matematica, nao uma nova identificacao atomica universal. Os calculos sao sinteticos; nao acreditam a natureza e nao alteram o gate.\n\n' if pt else
              'The energy reference is part of the physical contract. Eref=V0 is a mathematical instance, not a new universal atomic identification. Calculations are synthetic; they neither credit nature nor change the gate.\n\n')
    block += ('Cunhagens do operador, preservadas na lingua original [INPUT/ONTO]:\n' if pt else 'Operator inscriptions, preserved in their original language [INPUT/ONTO]:\n')
    for record in _V394_INSCRIPTIONS.values():
        block += '\\begin{quote}\n' + esc(record['text']) + '\n\\end{quote}\n'
    assert text.count(r'\end{document}') == 1, 'article boundary missing or ambiguous'
    return text.replace(r'\end{document}', block + '\n' + r'\end{document}')

def main():
    core = {}
    _v394_result = tempo_frequencia_v394(core)
    print("   [v394] tempo/frequencia: %s" % _v394_result["verdict"])
    _figs = emit_figures(core)
