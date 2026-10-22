"""Conditional QNM predictions. No default physical reading is selected.

[DERIVED] Gamma damps ensemble amplitude (and a density-matrix coherence),
not energy: delta_tau = -Gamma*tau_GR/(1+Gamma*tau_GR).
[INPUT] Single damped oscillator is an effective model, not QNM quantization.
[OPEN] A GKSL generator alone does not determine a classical single event.
Legacy profile reproduces the V346 detector-clock convention exactly.
"""
import math
import numpy as np

ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
C = 299792458.0
HBAR_SI = 6.62607015e-34/(2*math.pi)
G_CODATA_2018 = 6.67430e-11
GM_SUN_IAU_2015 = 1.3271244e20

def beta_tgl():
    return ALPHA_FINE_CODATA_2018*math.sqrt(math.e)

def scales(mass_detector_solar, profile):
    if not math.isfinite(mass_detector_solar) or mass_detector_solar <= 0:
        raise ValueError('Positive finite detector-frame remnant mass required')
    if profile == 'LEGACY_V346':
        gravity, hbar, gm_sun = 6.674e-11, 1.054571817e-34, 6.674e-11*1.98892e30
    elif profile == 'CODATA2018_IAU2015':
        gravity, hbar, gm_sun = G_CODATA_2018, HBAR_SI, GM_SUN_IAU_2015
    else:
        raise ValueError('Unknown constants profile')
    return mass_detector_solar*gm_sun/C**3, math.sqrt(hbar*gravity/C**5), hbar

def kerr_mode(mass_detector_solar, spin, *, profile='CODATA2018_IAU2015', qnm_dimensionless=None,
              mode=(2,2,0)):
    if len(mode)!=3 or any(not isinstance(v,(int,np.integer)) for v in mode):
        raise ValueError('Mode must be the integer tuple (ell,m,n)')
    ell,azimuthal_m,overtone=mode
    if ell<2 or abs(azimuthal_m)>ell or overtone<0:
        raise ValueError('Invalid gravitational mode labels')
    if tuple(mode)!=(2,2,0) and qnm_dimensionless is None:
        raise ValueError('Only 220 has a built-in BCW fit; every other mode requires a supplied exact QNM')
    if not math.isfinite(spin) or not -1 < spin < 1:
        raise ValueError('Signed dimensionless spin must lie strictly between -1 and 1')
    if spin < 0 and qnm_dimensionless is None:
        raise ValueError('Negative spin requires an exact mode consistent with the selected azimuthal axis; BCW fit is not extrapolated')
    tm, tp, hbar = scales(mass_detector_solar, profile)
    if qnm_dimensionless is None:
        wr = 1.5251 - 1.1568*(1-spin)**0.1292
        quality = 0.7000 + 1.4187*(1-spin)**(-0.4990)
        damping = wr/(2*quality)
        method = 'BERTI_CARDOSO_WILL_FIT_2006'
    else:
        wr, damping = float(complex(qnm_dimensionless).real), -float(complex(qnm_dimensionless).imag)
        if not (math.isfinite(wr) and math.isfinite(damping) and wr>0 and damping>0):
            raise ValueError('QNM convention is omega_R - i/tau')
        quality = wr/(2*damping)
        method = 'EXTERNALLY_SUPPLIED_QNM__PROVENANCE_REQUIRED'
    return dict(t_mass_s=tm,t_planck_s=tp,hbar_J_s=hbar,omega_rad_s=wr/tm,
                tau_gr_s=tm/damping,f_gr_hz=wr/(2*math.pi*tm),quality=quality,
                omega_mass=wr,qnm_method=method,mode=tuple(mode))

# Historical public name; the default is still exactly the registered 220.
kerr_220 = kerr_mode

def prediction(mass_detector_solar, spin, reading, *, observable='ensemble', redshift=0.0,
               profile='CODATA2018_IAU2015', qnm_dimensionless=None, occupation=None,mode=(2,2,0)):
    if observable not in ('ensemble','realization'):
        raise ValueError('Specify ensemble or realization')
    if not math.isfinite(redshift) or redshift < 0:
        raise ValueError('Redshift must be finite and nonnegative')
    q = kerr_mode(mass_detector_solar,spin,profile=profile,qnm_dimensionless=qnm_dimensionless,mode=mode)
    w, tm, tp, hb, b = q['omega_rad_s'],q['t_mass_s'],q['t_planck_s'],q['hbar_J_s'],beta_tgl()
    z1 = 1+redshift
    # Source-frame universal clock transforms as tau_star,det=(1+z)*tau_star,source.
    if reading=='R-A':
        star = tp if profile=='LEGACY_V346' else z1*tp
        gamma = b*star*w*w/2
        scope = 'INPUT_PLANCK_CLOCK__SOURCE_TO_DETECTOR_REDSHIFT_EXPLICIT'
    elif reading=='R-B':
        star = tm
        gamma = b*star*w*w/2
        scope = 'INPUT_SOURCE_MASS_CLOCK__NO_DERIVATION_OF_TAU_STAR'
    elif reading=='R-RAIZ-0':
        star = None
        gamma = b*w/2
        scope = 'CONDITIONAL_VACUUM_TO_ONE_QUANTUM_COHERENCE__NOT_MACROSCOPIC_FIELD'
    elif reading=='R-RAIZ-EP4':
        star = None
        w0 = 1/(4*tp*z1)
        gamma = b*w*w/(2*(math.sqrt(w0+w)+math.sqrt(w0))**2)
        scope = 'INPUT_BASE_ENERGY_EP_OVER_4__UNILATERAL_POSITIVE_GENERATOR'
    elif reading=='R-RAIZ-REST':
        star = None
        gravity = 6.674e-11 if profile=='LEGACY_V346' else G_CODATA_2018
        mass_source_kg = (tm/z1)*C**3/gravity
        w0 = mass_source_kg*C*C/(hb*z1)
        gamma = b*w*w/(2*(math.sqrt(w0+w)+math.sqrt(w0))**2)
        scope = 'CONJECTURE_REMNANT_REST_ENERGY_OFFSET__NOT_SHIFT_INVARIANT'
    elif reading=='R-RAIZ-COHERENT':
        if occupation is None or not math.isfinite(occupation) or occupation < 1e6:
            raise ValueError('Asymptotic coherent reading requires explicit N >= 1e6')
        star = None
        gamma = b*w/(8*occupation)
        scope = 'CONJECTURE_EFFECTIVE_OSCILLATOR__LARGE_N_INITIAL_SLOPE_NOT_EXACT_EXPONENTIAL'
    elif reading=='R-LIN':
        star = None
        gamma = b*w
        scope = 'CONJECTURE_CLOCK_BRIDGE_FOR_KERNEL_LINEAR_GAP_COMMENT__COEFFICIENT_1'
    elif reading=='R-MOD':
        if qnm_dimensionless is None:
            raise ValueError('Corotation reading requires exact QNM, not BCW fit')
        root = math.sqrt(1-spin*spin)
        horizon_omega = spin/(2*tm*(1+root))
        kappa = root/(2*tm*(1+root))
        effective = w-mode[1]*horizon_omega
        if effective <= 0:
            raise ValueError('Chosen restricted positive corotating mode is not admissible')
        star = 2*math.pi/kappa
        gamma = b*star*effective*effective/2
        scope = 'CONJECTURE_RESTRICTED_KMS_AND_MODULAR_CLOCK__NO_GLOBAL_KERR_HARTLE_HAWKING'
    elif reading=='R-GLOBAL':
        star, gamma = None, 0.0
        scope = 'CONDITIONAL_COMMON_TIME_NOISE_ON_SYSTEM_AND_REFERENCE__RELATIONAL_OBSERVABLE'
    else:
        raise ValueError('Unknown reading; propagation uses propagation_exponent separately')
    x = gamma*q['tau_gr_s']
    output = {**q,'reading':reading,'observable':observable,'profile':profile,'redshift':redshift,
              'beta_runtime':b,'tau_star_detector_s':star,'gamma_per_s':gamma,'x':x,
              'gamma_over_omega':gamma/w,'delta_tau_linear':-x,'delta_tau_ensemble_exact':-x/(1+x),
              'delta_f_ensemble':0.0,'scope':scope}
    if observable=='realization':
        output.update(delta_tau=None,delta_f=None,frequency_scatter=None,
                      requires='Specify unraveling, estimator, time window and detector noise; no universal fitted value')
    else:
        output.update(delta_tau=-x/(1+x),delta_f=0.0)
    if reading=='R-RAIZ-COHERENT':
        # A Poisson mixture has an initial slope, not one exact decay time.
        output.update(gamma_initial_per_s=gamma,x_initial_slope=x,x=None,
                      delta_tau_linear=None,delta_tau_ensemble_exact=None,delta_tau=None,
                      requires='Use the coherent Poisson sum and an explicit fitting window; no universal delta_tau')
    return output

def propagation_exponent(omega_observed, tau_star_source, redshift_grid, hubble_per_s):
    """[CONJECTURE] Independent local time noise in FLRW. Affects spectral coherence.

Xi=beta*tau_star*omega_obs^2/2 * integral_0^z (1+z)/H(z) dz.
Not an extra ringdown damping rate: no source-to-detector affine time substitution.
"""
    z,h = np.asarray(redshift_grid,dtype=float),np.asarray(hubble_per_s,dtype=float)
    if z.ndim!=1 or z.size<2 or z.shape!=h.shape or z[0]!=0 or not np.all(np.diff(z)>0):
        raise ValueError('Increasing cosmological redshift grid beginning at zero required')
    if not np.all(np.isfinite(z)) or not np.all(np.isfinite(h)) or np.any(h<=0):
        raise ValueError('Positive finite H(z) required')
    if not math.isfinite(omega_observed) or not math.isfinite(tau_star_source) or min(omega_observed,tau_star_source)<0:
        raise ValueError('Nonnegative finite frequency and clock required')
    integral = np.trapezoid((1+z)/h,z)
    return float(beta_tgl()*tau_star_source*omega_observed**2*integral/2)
