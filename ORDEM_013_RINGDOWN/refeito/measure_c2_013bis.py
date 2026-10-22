"""Conditional C2 trajectories; single worker, no PE or on-source data access."""
import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np
from scipy.interpolate import CubicSpline
from trajectory_recovery import fit
from prepare_empirical_noise import polynomial_whitener
from tgl_ringdown_prediction import prediction, beta_tgl
from tgl_ringdown_unravelings import poisson_support

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write_new(p, obj):
    if p.exists():
        raise FileExistsError(p)
    raw = (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode()
    tmp = p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:
        f.write(raw)
    assert tmp.read_bytes() == raw
    tmp.replace(p)

def summarize(fits, groups=None):
    x = np.array([r['df'] for r in fits])
    y = np.array([r['dtau'] for r in fits])
    n = len(x)
    sd = x.std(ddof=1)
    # Influence-function uncertainty, with finite-group correction when noise windows repeat.
    def se(influence):
        if groups is None:
            return float(np.std(influence, ddof=1)/np.sqrt(n))
        unique = np.unique(groups)
        sums = np.array([influence[groups == g].sum() for g in unique])
        return float(np.sqrt(len(unique)/(len(unique)-1)*np.sum(sums**2))/n)
    scatter_influence = ((x-x.mean())**2-np.mean((x-x.mean())**2))/(2*sd) if sd else np.zeros(n)
    return dict(N=n, mean_dtau=float(y.mean()), mean_dtau_standard_error=se(y-y.mean()),
        mean_df=float(x.mean()), df_standard_deviation=float(sd),
        df_standard_deviation_standard_error=se(scatter_influence),
        df_05_50_95=np.quantile(x,[.05,.5,.95]).tolist(),
        dtau_05_50_95=np.quantile(y,[.05,.5,.95]).tolist(),
        uncertainty_method='IID influence-function SE' if groups is None else 'Cluster influence-function SE by original off-source window; finite empirical support, not 1000 independent noise windows',
        distinct_noise_windows=None if groups is None else len(np.unique(groups)),
        boundary_count=sum(r['boundary'] for r in fits),
        optimizer_failures=sum(not r['optimizer_success'] for r in fits), fits=fits)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n',type=int,required=True)
    ap.add_argument('--tag',required=True)
    ap.add_argument('--reading')
    args = ap.parse_args()
    if args.n < 4:
        raise ValueError('At least four trajectories required')
    if not args.tag.replace('_','').isalnum():
        raise ValueError('Alphanumeric output tag required')
    out = ROOT/'bis'/('C2_TRAJECTORY_'+args.tag+'.json')
    if out.exists():
        raise FileExistsError(out)
    start = time.monotonic()
    meta_path = ROOT/'C5_RECOLORED_NOISE.json'
    meta = json.loads(meta_path.read_bytes())
    scenario = next(r for r in meta['scenarios'] if r['psd']=='O4')
    noise_path = ROOT/scenario['cache_path']
    assert sha(noise_path) == scenario['cache_sha256']
    with np.load(noise_path) as archive:
        psd = archive['psd_scaled'].copy()
        noise = archive['H1_strain_scaled'][:,:128].copy()
        gps = archive['H1_original_GPS'].copy()
    whitener, cov, inverse = polynomial_whitener(psd,4096,128)
    error = float(np.max(np.abs(inverse@cov@inverse.T-np.eye(len(inverse)))))
    assert error < 1e-5, error
    times = np.arange(128)/2048.
    dt = np.diff(np.r_[0.,times])
    rng = np.random.default_rng(13051301)
    wiener = np.cumsum(rng.normal(size=(args.n,128))*np.sqrt(dt),axis=1)
    cauchy = np.cumsum(rng.standard_cauchy(size=(args.n,128))*dt,axis=1)
    noise_index = rng.integers(0,len(noise),size=args.n)
    grid = json.loads((ROOT/'QNM_GRID.json').read_bytes())['modes']['220']
    exact = complex(CubicSpline(grid['spins'],np.array(grid['real'])+1j*np.array(grid['imag']))(.68))
    readings = ['R-A','R-B','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-LIN','R-MOD','R-GLOBAL']
    cases = [dict(reading=r) for r in readings]
    cases += [dict(reading='R-RAIZ-COHERENT',occupation=k) for k in (4,64,256)]
    if args.reading:
        cases = [r for r in cases if r['reading']==args.reading]
        if not cases:
            raise ValueError('Unknown reading')
    rows=[]
    for case in cases:
        p = prediction(68.1,.68,'R-B' if case.get('occupation') else case['reading'],
            qnm_dimensionless=exact if case['reading']=='R-MOD' else None)
        omega,tau = p['omega_rad_s'],p['tau_gr_s']
        carrier = np.exp(-times/tau+1j*(omega*times+.37))
        amp = 20/np.linalg.norm(whitener@carrier.real)
        if case.get('occupation'):
            support,weights,poisson_meta = poisson_support(case['occupation'])
            gaps = np.sqrt(beta_tgl()*omega)/(np.sqrt(support+1)+np.sqrt(support))
            ensemble = np.exp(-.5*times[:,None]*gaps**2)@weights
            process = 'COHERENT_POISSON_SHARED_WIENER__CONDITIONAL_QUANTUM_MEAN'
        else:
            gamma=p['gamma_per_s']
            ensemble=np.exp(-gamma*times)
            process='CAUCHY_PHASE' if case['reading']=='R-LIN' else 'WIENER_SINGLE_COHERENCE'
            poisson_meta=None
        expected=fit(times,amp*(carrier*ensemble).real,whitener,omega,tau)
        if not case.get('occupation'):
            assert abs(expected['dtau']+gamma*tau/(1+gamma*tau))<1e-6
            assert abs(expected['df'])<1e-6
        gr_basis=whitener@np.column_stack([np.exp(-times/tau)*np.cos(omega*times),
                                         np.exp(-times/tau)*np.sin(omega*times)])
        gr_basis=np.linalg.qr(gr_basis)[0]
        fits=[[],[]]; losses=[]
        for i in range(args.n):
            if case.get('occupation'):
                factor=np.exp(1j*wiener[i,:,None]*gaps)@weights
            else:
                angle=gamma*cauchy[i] if process=='CAUCHY_PHASE' else np.sqrt(2*gamma)*wiener[i]
                factor=np.exp(1j*angle)
                assert np.max(abs(abs(factor)**2-1))<1e-12
            clean=amp*(carrier*factor).real
            white=whitener@clean
            losses.append(float(1-np.linalg.norm(gr_basis.T@white)/np.linalg.norm(white)))
            fits[0].append(fit(times,clean,whitener,omega,tau))
            fits[1].append(fit(times,clean+noise[noise_index[i]],whitener,omega,tau))
        row=dict(**case,unraveling=process,poisson_meta=poisson_meta,ensemble_fit=expected,
            gr_matched_filter_snr_fractional_loss=dict(mean=float(np.mean(losses)),
                quantiles_05_50_95=np.quantile(losses,[.05,.5,.95]).tolist(),
                definition='1 minus phase-maximized fixed-GR-template projection norm / optimal clean-signal norm; not energy loss'),
            noise_free=summarize(fits[0]),recolored=summarize(fits[1],noise_index))
        rows.append(row)
        print(json.dumps(dict(reading=case['reading'],occupation=case.get('occupation'),N=args.n,
            dtau_clean=row['noise_free']['mean_dtau'],dtau_noisy=row['recolored']['mean_dtau'],
            seconds=time.monotonic()-start)),flush=True)
    result=dict(status='CONDITIONAL_ESTIMATOR_CONTROL_NOT_PHYSICAL_UNRAVELING_OR_PE',
        created_utc=datetime.now(timezone.utc).isoformat(),N_per_cell=args.n,
        seed=13051301,reference=dict(mass_detector_solar=68.1,spin=.68,GR_reference_SNR=20),
        sample_hz=2048,sample_count=128,window_seconds=128/2048,
        changed_from_v1='Same sample count, twice the time span (v1 used 4096 Hz); explicit PSD polynomial quotient replaces synthetic OU covariance.',
        noise_scope='One H1 response channel. Reused off-source residuals transported to O4 reference PSD by the frozen C5 convention. This is not a new measured O4 PSD or an independent 1000-window dataset.',
        physical_scope='Detector records one realization; physical unraveling remains OPEN. Earlier C4/C6 tested ensemble. These chosen readouts calibrate estimator distributions only.',
        cauchy_scope='No phase variance exists; df scatter is for the bounded fitted estimator.',
        coherent_scope='Conditional quantum <a>, not a unique classical strain; occupation values illustrative, no distance-to-occupation law.',
        estimator='Original trajectory_recovery.fit, three-start variable projection, df [-0.5,0.5], log(tau/tau_GR) [-2,2]; failed and boundary fits retained.',
        whitening_residual=error,original_noise_windows=len(noise),noise_indices=noise_index.tolist(),
        original_noise_GPS=gps.tolist(),wall_seconds=time.monotonic()-start,
        beta_runtime=beta_tgl(),rows=rows,
        sources={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'trajectory_recovery.py',ROOT/'tgl_ringdown_prediction.py',ROOT/'tgl_ringdown_unravelings.py',ROOT/'prepare_empirical_noise.py',ROOT/'QNM_GRID.json',meta_path,noise_path]})
    write_new(out,result)
    print(str(out),sha(out),flush=True)

if __name__=='__main__':
    main()
