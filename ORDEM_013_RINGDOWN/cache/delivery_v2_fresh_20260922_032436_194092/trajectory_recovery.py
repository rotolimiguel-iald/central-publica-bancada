"""C2: fitted single-realization distributions, with/without synthetic colored noise.

These are explicitly chosen unravelings, not a claim that a GKSL generator
selects classical strain. Cauchy increments implement the linear-gap channel;
root-coherent traces use one shared Wiener process and the Poisson sum.
This is not C5's off-source strain calibration or two-IMR-family injection test.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import hashlib
import json
import math
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.linalg import cholesky, solve_triangular
from scipy.optimize import least_squares
from scipy.stats import poisson
from fetch_public import atomic_json
from tgl_ringdown_prediction import prediction, beta_tgl

ROOT=Path(__file__).resolve().parent

def fit(time, y, whitener, omega, tau):
    target=whitener@y
    def residual(p):
        angle=omega*(1+p[0])*time
        env=np.exp(-time/(tau*np.exp(p[1])))
        basis=whitener@np.column_stack([env*np.cos(angle),env*np.sin(angle)])
        amplitudes=np.linalg.lstsq(basis,target,rcond=None)[0]
        return target-basis@amplitudes
    candidates=[least_squares(residual,[start,0.],bounds=([-.5,-2.],[.5,2.]),
                 ftol=1e-10,xtol=1e-10,gtol=1e-10,max_nfev=100) for start in (0.,-.03,.03)]
    best=min(candidates,key=lambda r:r.cost)
    return dict(df=float(best.x[0]),dtau=float(np.expm1(best.x[1])),
                optimizer_success=bool(best.success),cost=float(best.cost),
                boundary=bool(abs(best.x[0])>.499 or abs(best.x[1])>1.999))

def main():
    mass,spin=68.1,.68 # illustrative frozen reference, not a fitted source posterior
    base=prediction(mass,spin,'R-B')
    omega,tau=base['omega_rad_s'],base['tau_gr_s']
    times=np.arange(128)/4096.
    increments=np.diff(np.r_[0.,times])
    covariance=.4*np.eye(len(times))+.6*np.exp(-abs(times[:,None]-times[None,:])/.001)
    chol=cholesky(covariance,lower=True)
    whiten=solve_triangular(chol,np.eye(len(times)),lower=True)
    phase=.37
    carrier=np.exp(-times/tau)*np.exp(1j*(omega*times+phase))
    snr=20.
    amplitude=snr/np.linalg.norm(whiten@carrier.real)
    grid=json.loads((ROOT/'QNM_GRID.json').read_bytes())['modes']['220']
    exact=CubicSpline(grid['spins'],np.array(grid['real'])+1j*np.array(grid['imag']))(spin)
    readings=['R-A','R-B','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-LIN','R-MOD','R-GLOBAL']
    cases=[]
    for reading in readings:
        p=prediction(mass,spin,reading,qnm_dimensionless=complex(exact) if reading=='R-MOD' else None)
        cases.append(dict(reading=reading,gamma=p['gamma_per_s'],
                          omega_rad_s=p['omega_rad_s'],tau_gr_s=p['tau_gr_s'],
                          unraveling='CAUCHY_PHASE' if reading=='R-LIN' else 'WIENER_SINGLE_COHERENCE'))
    cases.extend(dict(reading='R-RAIZ-COHERENT',occupation=n,unraveling='COHERENT_POISSON_WIENER') for n in (4,64,256))
    rng=np.random.default_rng(13042600)
    number=50
    rows=[]
    # Same instrument and standard-normal samples across cases isolate generator changes.
    wiener=np.cumsum(rng.normal(size=(number,len(times)))*np.sqrt(increments),axis=1)
    cauchy=np.cumsum(rng.standard_cauchy(size=(number,len(times)))*increments,axis=1)
    detector_noise=rng.normal(size=(number,len(times)))@chol.T
    oracle_residual=float(np.max(abs(whiten@covariance@whiten.T-np.eye(len(times)))))
    if oracle_residual>1e-12:raise ValueError('Colored-noise whitening failed')
    for case in cases:
        omega=case.get('omega_rad_s',base['omega_rad_s'])
        tau=case.get('tau_gr_s',base['tau_gr_s'])
        carrier=np.exp(-times/tau)*np.exp(1j*(omega*times+phase))
        amplitude=snr/np.linalg.norm(whiten@carrier.real)
        if case['reading']=='R-RAIZ-COHERENT':
            n=case['occupation'];k=np.arange(int(poisson.ppf(1-1e-14,n))+1)
            weights=poisson.pmf(k,n)
            tail=1-float(weights.sum())
            if abs(tail)>1e-12:raise ValueError('Poisson truncation unresolved')
            gaps=np.sqrt(beta_tgl()*omega)/(np.sqrt(k+1)+np.sqrt(k))
            factors=np.exp(1j*wiener[:,:,None]*gaps)@weights
            ensemble=np.exp(-.5*times[:,None]*gaps**2)@weights
            energy_claim='Oscillator number conserved by number-diagonal unitary; |<a>| squared is not oscillator energy'
        else:
            gamma=case['gamma'];tail=None
            angle=(gamma*cauchy if case['unraveling']=='CAUCHY_PHASE' else np.sqrt(2*gamma)*wiener)
            factors=np.exp(1j*angle)
            ensemble=np.exp(-gamma*times)
            energy_claim='Each complex phase realization has the GR envelope; ensemble coherent power decays at 2*Gamma'
            if np.max(abs(abs(factors)**2-1.))>1e-12:raise ValueError('Unitary phase realization lost envelope energy')
        expected_fit=fit(times,amplitude*(carrier*ensemble).real,whiten,omega,tau)
        if case['reading']!='R-RAIZ-COHERENT':
            predicted=-case['gamma']*tau/(1+case['gamma']*tau)
            if abs(expected_fit['df'])>1e-6 or abs(expected_fit['dtau']-predicted)>1e-6:
                raise ValueError('Noiseless ensemble fit does not recover additive damping')
        clean=amplitude*(carrier[None,:]*factors).real
        norms=np.linalg.norm(clean@whiten.T,axis=1)
        reference=whiten@(amplitude*carrier.real)
        overlaps=(clean@whiten.T)@reference/(norms*np.linalg.norm(reference))
        comparisons=[]
        for noisy in (False,True):
            fits=[fit(times,y,whiten,omega,tau) for y in (clean+detector_noise if noisy else clean)]
            columns={name:np.array([r[name] for r in fits]) for name in ('df','dtau')}
            comparisons.append(dict(detector_noise='SYNTHETIC_COLORED_OU_PLUS_WHITE' if noisy else 'NONE',
                N=number,df_05_50_95=np.quantile(columns['df'],[.05,.5,.95]).tolist(),
                dtau_05_50_95=np.quantile(columns['dtau'],[.05,.5,.95]).tolist(),
                mean_df=float(columns['df'].mean()),mean_dtau=float(columns['dtau'].mean()),
                standard_deviation_of_fitted_df=float(columns['df'].std(ddof=1)),
                boundary_count=sum(r['boundary'] for r in fits),
                optimizer_failures=sum(not r['optimizer_success'] for r in fits),fits=fits))
        result=dict(**case,poisson_tail=tail,energy_scope=energy_claim,
            ensemble_fit=expected_fit,single_trajectory_overlap_05_50_95=np.quantile(overlaps,[.05,.5,.95]).tolist(),
            ensemble_mean_endpoint=float(ensemble[-1]),
            empirical_mean_endpoint=[float(factors[:,-1].real.mean()),float(factors[:,-1].imag.mean())],
            comparisons=comparisons)
        rows.append(result)
        print(json.dumps(dict(reading=case['reading'],occupation=case.get('occupation'),
                ensemble_dtau=expected_fit['dtau'],
                noise_free_dtau=comparisons[0]['dtau_05_50_95'],
                colored_dtau=comparisons[1]['dtau_05_50_95'],
                boundaries=[c['boundary_count'] for c in comparisons])),flush=True)
    output=dict(status='C2_CONDITIONAL_ESTIMATOR_DISTRIBUTIONS_MEASURED',seed=13042600,
        beta_runtime=beta_tgl(),N_per_cell=number,reference=dict(mass_detector=mass,spin=spin),
        sampling_hz=4096,sample_count=len(times),GR_reference_SNR=snr,
        estimator='Whitened time-domain variable projection; free real sine/cosine amplitudes, df in [-.5,.5], log(tau/tauGR) in [-2,2]; three initial points; failures and boundary hits retained',
        covariance='0.4 I + 0.6 exp(-|dt|/0.001 s)',whitening_residual=oracle_residual,
        physical_scope='Explicit effective oscillator/readout hypotheses; generator alone does not select a classical realization. Root coherent uses conditional quantum <a>, not a unique classical strain process.',
        Cauchy_warning='Phase increments have no variance; reported scatter belongs only to the bounded fitted estimator, not to a phase variance',
        source_clock_note='R-MOD uses the same exact QNM for its carrier, damping time, and corotation rate; other 220 references use the registered BCW convention',
        preserved_control='Earlier common-carrier control is retained in backup. Current R-MOD carrier and reference tau are exact and consistent with its gamma.',
        rows=rows,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        not_C5='Synthetic OU noise is not off-source GWOSC strain; no two-IMR-family validation or inference coverage claim',
        remaining=['Physical choice of classical unraveling','Empirical off-source noise and IMR model-mismatch matrix','C6 registered on-source strain execution'])
    atomic_json(ROOT/'C2_TRAJECTORY_RECOVERY.json',output)

if __name__=='__main__':main()
