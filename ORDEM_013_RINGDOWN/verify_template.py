"""Independent quadrature, limits, phase diffusion, and energy checks."""
from pathlib import Path
import json
import math
import numpy as np
from scipy.integrate import quad
from fetch_public import atomic_json
from tgl_ringdown_template import ringdown, damped_cosine_fourier
from tgl_ringdown_prediction import prediction

ROOT=Path(__file__).resolve().parent

def main():
    mass,spin=68.1,.68
    pred=prediction(mass,spin,'R-B')
    fr,decay=pred['f_gr_hz'],1/pred['tau_gr_s']+pred['gamma_per_s']
    phase=.37
    errors=[]
    for f in [30.,100.,fr,450.,1000.]:
        integrand=lambda t: math.exp(-decay*t)*math.cos(2*math.pi*fr*t+phase)
        real=quad(lambda t:integrand(t)*math.cos(2*math.pi*f*t),0,40/decay,epsabs=1e-12,epsrel=1e-11,limit=500)[0]
        imag=quad(lambda t:-integrand(t)*math.sin(2*math.pi*f*t),0,40/decay,epsabs=1e-12,epsrel=1e-11,limit=500)[0]
        closed=complex(damped_cosine_fourier([f],1.,fr,decay,phase)[0])
        err=abs(closed-complex(real,imag))/abs(closed)
        errors.append(dict(frequency=f,relative_error=err))
        assert err<1e-7
    t=np.arange(-.001,.04,1/32768)
    p0=ringdown(t,mass,spin,'R-B',strain_amplitude=1.,deformation=0.)
    p1=ringdown(t,mass,spin,'R-B',strain_amplitude=1.)
    energy0=p0['plus']**2+p0['cross']**2
    energy1=p1['plus']**2+p1['cross']**2
    active=t>=0
    assert np.all(p0['plus'][~active]==0)
    ratio=energy1[active]/energy0[active]
    envelope_error=float(np.max(np.abs(ratio-np.exp(-2*pred['gamma_per_s']*t[active]))))
    assert envelope_error<1e-12
    realization=ringdown(t,mass,spin,'R-B',strain_amplitude=1.,observable='brownian_phase',seed=1301)
    actual=realization['plus']**2+realization['cross']**2
    energy_error=float(np.max(np.abs(actual-energy0)))
    assert energy_error<1e-12
    # Independent Monte Carlo uses Wiener endpoint law, not template code.
    rng=np.random.default_rng(213013)
    draws=200000
    tau=pred['tau_gr_s']
    diff=[]
    for elapsed in [tau,5*tau,20*tau]:
        diffusion=math.sqrt(2*pred['gamma_per_s']*elapsed)*rng.normal(size=draws)
        z=np.exp(1j*diffusion)
        expected=math.exp(-pred['gamma_per_s']*elapsed)
        # Standard errors computed separately for two Cartesian components.
        er=float(z.real.std(ddof=1)/math.sqrt(draws))
        ei=float(z.imag.std(ddof=1)/math.sqrt(draws))
        pull_real=float((z.real.mean()-expected)/er)
        pull_imag=float(z.imag.mean()/ei)
        assert max(abs(pull_real),abs(pull_imag))<5
        diff.append(dict(t_s=elapsed,expected=expected,mean_real=float(z.real.mean()),
                         mean_imag=float(z.imag.mean()),pull_real=pull_real,pull_imag=pull_imag,
                         mean_power=float(np.mean(abs(z)**2))))
    atomic_json(ROOT/'C2_TEMPLATE_CHECKS.json',dict(status='ALGEBRA_AND_NOISELESS_CONVENTIONS_PASS',
            fourier_quadrature=errors,ensemble_power_envelope_residual=envelope_error,
            single_realization_energy_residual=energy_error,diffusion_endpoints=diff,
            seed=213013,draws=draws,
            not_tested=['Fitted tau/f distribution','Detector colored-noise recovery',
                        'Full-IMR interface','Physical choice of unraveling']))
    print(json.dumps({'fourier':errors,'ensemble_power_residual':envelope_error,
                      'single_realization_energy_residual':energy_error,'diffusion':diff}),flush=True)

if __name__=='__main__': main()
