"""Recolor held-out O4 residuals into explicit reference-noise scenarios.

This is a finite-interval quotient construction, not observed O5/ET/CE data.
For the same degree-2 projection P, xi = W_O4 y; y_target = P.T L_target xi.
Consequently W_target y_target = xi. No samples outside the interval enter.
The order of Cholesky coordinates is fixed; non-Gaussian future noise is NOT
predicted by this arbitrary transport. Gaussian controls isolate that issue.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.linalg import cholesky, qr
from prepare_empirical_noise import polynomial_whitener
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def reference_psd(curve, frequencies, low_exponent=4):
    path=ROOT/'cache/psd'/curve['filename']
    if hashlib.sha256(path.read_bytes()).hexdigest()!=curve['sha256']:
        raise ValueError('Reference PSD custody changed')
    raw=np.loadtxt(path)
    valid=(raw[:,0]>0)&(raw[:,1]>0)&np.isfinite(raw[:,1])
    f,p=raw[valid,0],raw[valid,1]
    if curve['kind']=='ASD':p=p*p
    if f[-1]<frequencies[-1]:raise ValueError('Reference curve ends below Nyquist')
    out=np.zeros_like(frequencies)
    positive=frequencies>0
    out[positive]=np.exp(np.interp(np.log(frequencies[positive]),np.log(f),np.log(p)))
    below=positive&(frequencies<f[0])
    out[below]=p[0]*(frequencies[below]/f[0])**(-low_exponent)
    # DC is annihilated exactly by P, not interpreted as zero physical noise.
    return out*1e42,dict(lowest_tabulated_hz=float(f[0]),
        low_frequency_continuation=f'PSD(f_min)*(f/f_min)^(-{low_exponent})',
        extrapolated_bins=int(below.sum()),DC='Exactly quotiented; value zero is computational only')

def main():
    curves=json.loads((ROOT/'FISHER_INPUTS.json').read_bytes())['psds']
    meta=json.loads((ROOT/'C5_EMPIRICAL_NOISE.json').read_bytes())
    observed={}
    for row in meta['detectors']:
        path=ROOT/f"cache/empirical_noise/{row['detector']}_noise.npz"
        if hashlib.sha256(path.read_bytes()).hexdigest()!=row['cache_sha256']:
            raise ValueError('Measured-noise custody changed')
        observed[row['detector']]=np.load(path)
    reference=observed['H1'];n=reference['whitener_scaled'].shape[1]
    frequencies=reference['frequency_hz'];fs=4096
    orthogonal,_=qr(np.polynomial.legendre.legvander(np.linspace(-1,1,n),2),mode='full')
    projection=orthogonal[:,3:].T
    t=np.arange(n)/2048.
    test=np.column_stack([np.exp(-t/.004)*np.cos(2*np.pi*f*t+phase)
        for f in (150.,250.,400.,600.) for phase in (0.,np.pi/2)])
    rows=[];output=ROOT/'cache/recolored_noise';output.mkdir(exist_ok=True)
    for curve in curves:
        variants={}
        for exponent in (2,4,6):
            psd,assumption=reference_psd(curve,frequencies,exponent)
            w,cov,inverse=polynomial_whitener(psd,fs,n)
            residual=float(np.max(abs(inverse@cov@inverse.T-np.eye(len(w)))))
            if residual>1e-5:raise ValueError(f'Whitening unstable: {curve["key"]}, {exponent}: {residual}')
            wt=w@test
            variants[exponent]=dict(w=w,cov=cov,psd=psd,assumption=assumption,
                residual=residual,norm=np.linalg.norm(wt,axis=0))
        primary=variants[4];w=primary['w'];cov=primary['cov']
        chol=cholesky(cov,lower=True)
        recolored={};checks=[]
        for detector,data in observed.items():
            xi=data['held_out_strain_scaled']@data['whitener_scaled'].T
            y=xi@chol.T@projection
            error=float(np.max(abs(y@w.T-xi)))
            if error>1e-5:raise ValueError('Recoloring does not recover the original whitened residuals')
            recolored[detector]=y
            checks.append(dict(detector=detector,max_coordinate_error=error,
                N=len(xi),reduced_chisquare_mean=float(np.mean(xi*xi))))
        # Separate frequency-domain Gaussian generator, not Cholesky self-test.
        nfft=2*(len(frequencies)-1);rng=np.random.default_rng(130528+len(rows))
        coefficients=(rng.normal(size=(256,len(frequencies)))+
                      1j*rng.normal(size=(256,len(frequencies))))*np.sqrt(primary['psd']*fs*nfft/4)
        coefficients[:,0]=0
        coefficients[:,-1]=rng.normal(size=256)*np.sqrt(primary['psd'][-1]*fs*nfft/2)
        gaussian=np.fft.irfft(coefficients,n=nfft,axis=1)[:,:2*n:2]
        energy=float(np.mean((gaussian@w.T)**2))
        if abs(energy-1)>.03:raise ValueError('Independent Gaussian covariance check failed')
        sensitivity={str(k):(v['norm']/primary['norm']-1).tolist() for k,v in variants.items()}
        target=output/f"{curve['key']}_noise.npz"
        if target.exists():raise FileExistsError('Keep scenario cache immutable; inspect before rerunning')
        np.savez_compressed(target,frequency_hz=frequencies,psd_scaled=primary['psd'],
            projected_covariance_scaled=cov,whitener_scaled=w,
            H1_strain_scaled=recolored['H1'],L1_strain_scaled=recolored['L1'],
            H1_original_GPS=observed['H1']['held_out_GPS'],L1_original_GPS=observed['L1']['held_out_GPS'],
            whitener_low2=variants[2]['w'],whitener_low6=variants[6]['w'])
        row=dict(psd=curve['key'],curve=curve,cache_path=str(target.relative_to(ROOT)),
            cache_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
            assumption=primary['assumption'],whitening_residual=primary['residual'],
            recoloring_checks=checks,independent_Gaussian_energy=energy,
            filter_norm_relative_change_low_exponent=sensitivity,
            max_filter_norm_fractional_sensitivity=float(max(abs(x) for v in sensitivity.values() for x in v)))
        rows.append(row)
        print(json.dumps({k:row[k] for k in ('psd','whitening_residual','independent_Gaussian_energy','max_filter_norm_fractional_sensitivity')}),flush=True)
    atomic_json(ROOT/'C5_RECOLORED_NOISE.json',dict(status='CONDITIONAL_REFERENCE_RECOLORING_VALIDATED',
        scope='Identical target PSD in two illustrative response channels; not an ET/CE network geometry or an O5 achieved sensitivity. Measured residual coordinates are transported by an explicit convention; future non-Gaussian noise is unknown.',
        no_on_source_strain_access=True,samples_per_detector=256,degree=2,stride=2,fs_original=4096,
        low_frequency_exponent_primary=4,low_frequency_controls=[2,6],
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scenarios=rows))

if __name__=='__main__':main()
