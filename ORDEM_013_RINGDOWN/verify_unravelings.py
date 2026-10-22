"""Independent finite-density, probability and actual Bilby API controls."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np
from scipy.special import gammaln
from scipy.stats import poisson
import bilby
from tgl_ringdown_unravelings import phase_factor,poisson_support,coherent_root_factor,conditional_ringdown
from tgl_ringdown_prediction import beta_tgl
from tgl_ringdown_template import ringdown
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def main():
    rows=[];omega=1500.;times=np.array([0.,.001,.01,.1])
    for occupation in (4.,64.,256.,4096.):
        n,weights,meta=poisson_support(occupation)
        ref=poisson.pmf(n,occupation)
        residual=float(np.max(abs(weights-ref)))
        omitted=float(poisson.cdf(n[0]-1,occupation)+poisson.sf(n[-1],occupation))
        if residual>5e-12 or omitted>meta['analytic_omitted_mass_bound']:
            raise ValueError('Poisson support/recurrence independent oracle failed')
        row=dict(independent_pmf_max_error=residual,actual_tail=omitted,**meta)
        if occupation<=256:
            size=int(poisson.ppf(1-1e-14,occupation))+3;levels=np.arange(size)
            state=np.exp((levels*np.log(occupation)-occupation-gammaln(levels+1))/2)
            rho=np.outer(state,state)
            jump=np.diag(np.sqrt(beta_tgl()*omega*levels))
            jump2=jump@jump
            lindblad=jump@rho@jump-.5*(jump2@rho+rho@jump2)
            annihilator=np.diag(np.sqrt(np.arange(1,size)),1)
            initial_slope=-float(np.trace(annihilator@lindblad))/math.sqrt(occupation)
            api,info=coherent_root_factor(times,omega,occupation)
            oracle=[]
            values=np.diag(jump)
            for t in times:
                evolved=rho*np.exp(-.5*t*(values[:,None]-values[None,:])**2)
                oracle.append(float(np.trace(annihilator@evolved))/math.sqrt(occupation))
            error=float(np.max(abs(api-np.array(oracle))))
            if error>1e-11 or abs(initial_slope-info['initial_rate_per_s'])>1e-9:
                raise ValueError('Root field does not match finite density evolution')
            row.update(finite_density_error=error,initial_slope_error=abs(initial_slope-info['initial_rate_per_s']))
        rows.append(row)
    # Distinguish generators by their second harmonics, not only equal <exp(i phi)>.
    rng=np.random.default_rng(130529);number=200000;gammat=.3
    phases={'brownian':np.sqrt(2*gammat)*rng.normal(size=number),
            'cauchy':gammat*rng.standard_cauchy(size=number)}
    harmonics=[]
    for name,angles in phases.items():
        for k in (1,2):
            expected=np.exp(-gammat*(k*k if name=='brownian' else abs(k)))
            measured=np.exp(1j*k*angles).mean();error=float(abs(measured-expected))
            if error>6/np.sqrt(number):raise ValueError('Stochastic characteristic function failed')
            harmonics.append(dict(process=name,harmonic=k,expected=float(expected),
                empirical=[float(measured.real),float(measured.imag)],error=error))
        z=phase_factor(times,3.,process=name,seed=13)
        if np.max(abs(abs(z)-1))>1e-14:raise ValueError('Pure phase trajectory lost modulus')
        if not np.array_equal(z,phase_factor(times,3.,process=name,seed=13)):raise ValueError('Seed not reproducible')
    # Existing interface remains delegated exactly, including the Brownian seed.
    params=dict(mass_detector_solar=68.1,spin=.68,reading='R-B',strain_amplitude=1e-21,
        t_start=.001,phase=.3,inclination=.6,deformation=1.,redshift=.1)
    t=np.arange(512)/4096
    for observable in ('ensemble','brownian_phase'):
        old=ringdown(t,**params,observable=observable,seed=42)
        new=conditional_ringdown(t,**params,observable=observable,seed=42)
        if any(not np.array_equal(old[k],new[k]) for k in old):raise ValueError('Existing template changed')
    consumer=[]
    for reading,observable,occupation in [('R-LIN','cauchy_phase',None),
              ('R-RAIZ-COHERENT','ensemble',64.),('R-RAIZ-COHERENT','quantum_wiener',64.)]:
        arguments=dict(observable=observable,seed=42,occupation=occupation)
        model=dict(params,reading=reading)
        generator=bilby.gw.WaveformGenerator(duration=.125,sampling_frequency=4096,
            time_domain_source_model=conditional_ringdown,parameter_conversion=lambda p:(dict(p),[]),
            waveform_arguments=arguments)
        computed=generator.time_domain_strain(model)
        direct=conditional_ringdown(generator.time_array,**model,**arguments)
        error=max(float(np.max(abs(computed[k]-direct[k]))) for k in direct)
        if error:raise ValueError('Bilby result differs from direct source')
        if any(np.any(v[generator.time_array<params['t_start']]) for v in computed.values()):raise ValueError('Pre-onset waveform leaked')
        consumer.append(dict(reading=reading,observable=observable,occupation=occupation,max_error=error))
    refusals=[]
    for label,call in [
        ('missing_Cauchy_seed',lambda:phase_factor(times,1.,process='cauchy')),
        ('negative_rate',lambda:phase_factor(times,-1.,process='ensemble')),
        ('macroscopic_N_not_silent_exact',lambda:coherent_root_factor(times,omega,1e78)),
        ('zero_occupation_normalized_field_undefined',lambda:coherent_root_factor(times,omega,0.)),
        ('wrong_Cauchy_reading',lambda:conditional_ringdown(t,**params,observable='cauchy_phase',seed=2))]:
        try:call()
        except ValueError:refusals.append(label)
        else:raise ValueError('Invalid request accepted: '+label)
    atomic_json(ROOT/'C3_UNRAVELING_API.json',dict(status='PASS',finite_occupation_controls=rows,
        characteristic_functions=harmonics,consumer=consumer,refused=refusals,
        bilby_version=bilby.__version__,existing_template_delegation_exact=True,
        physical_scope='Conditional effective readouts, not a selected physical unraveling, nor the registered C6 model.',
        source_sha256=hashlib.sha256((ROOT/'tgl_ringdown_unravelings.py').read_bytes()).hexdigest(),
        verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
    print(json.dumps(dict(status='PASS',finite_occupations=len(rows),bilby_consumers=len(consumer),refusals=len(refusals))))

if __name__=='__main__':main()
