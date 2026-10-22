"""Estimate off-source PSDs and a causal, finite-interval noise likelihood.

Only files ending at least two seconds before GW250114 may be opened here.
The first 2048 s train the PSD; the last 2048 s supply held-out intervals.
No bandpass is applied: polynomial nuisance terms are removed *after* the
interval is truncated, with the identical linear map for data and templates.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import hashlib
import json
import numpy as np
import h5py
from scipy.linalg import cholesky, solve_triangular, toeplitz, qr
from scipy.signal import periodogram
from fetch_public import atomic_json, digests

ROOT=Path(__file__).resolve().parent
EVENT_GPS=1420878141.2
FS=4096
STRIDE=2  # Exact sample selection, no antialias filter across the cut.
INTERVAL_SAMPLES=410  # 0.2001953125 s at 2048 Hz.

def covariance_from_psd(psd, fs, n):
    """One-sided PSD, including DC/Nyquist; trapezoidal endpoint convention."""
    acf=fs/2*np.fft.irfft(psd)
    return toeplitz(acf[:n])

def polynomial_whitener(psd, fs, n, degree=2, stride=STRIDE):
    """Project the spectral factors BEFORE forming the covariance.

    This avoids subtracting enormous nearly equal low-frequency covariances.
    The orthonormal rows annihilate degree-2 polynomials on the truncated
    interval. The Fourier sum gives P C P^T directly as a positive Gram matrix.
    No samples outside the interval, PSD floor or bandpass is involved.
    """
    polynomial=np.polynomial.legendre.legvander(np.linspace(-1,1,n),degree)
    orthogonal,_=qr(polynomial,mode='full')
    projection=orthogonal[:,degree+1:].T
    nfft=2*(len(psd)-1)
    embedded=np.zeros((len(projection),stride*n))
    embedded[:,::stride]=projection
    spectral=np.fft.rfft(embedded,n=nfft,axis=1)
    spectral[:,0]=0  # Exact annihilation of constants, avoiding DC roundoff.
    weights=psd*(fs/nfft)
    weights=weights.copy();weights[[0,-1]]*=.5
    spectral*=np.sqrt(weights)[None,:]
    covariance=(spectral@spectral.conj().T).real
    chol=cholesky(covariance,lower=True)
    inverse=solve_triangular(chol,np.eye(n-degree-1),lower=True)
    return inverse@projection,covariance,inverse

def decode(values):
    return [x.decode() if isinstance(x,bytes) else str(x) for x in values]

def main():
    output=ROOT/'cache'/'empirical_noise'
    output.mkdir(exist_ok=True)
    rows=[]
    for detector in ('H1','L1'):
        paths=list((ROOT/'cache'/'gwosc'/'offsource').glob(f'*-{detector}_*.hdf5'))
        if len(paths)!=1: raise ValueError('Ambiguous off-source artifact')
        path=paths[0]
        receipt=json.loads(path.with_name(path.name+'.receipt.json').read_bytes())
        _,digest=digests(path)
        if receipt['sha256']!=digest:raise ValueError('Off-source file custody changed')
        with h5py.File(path) as handle:
            start=float(handle['meta/GPSstart'][()]); duration=float(handle['meta/Duration'][()])
            if start+duration>=EVENT_GPS-2:raise ValueError('On-source access refused')
            strain=handle['strain/Strain']
            if 1/float(strain.attrs['Xspacing'])!=FS:raise ValueError('Unexpected sample rate')
            quality=handle['quality/simple/DQmask'][:]
            injections=handle['quality/injections/Injmask'][:]
            qnames=decode(handle['quality/simple/DQShortnames'][:])
            inames=decode(handle['quality/injections/InjShortnames'][:])
            qrequired=sum(1<<qnames.index(x) for x in ('DATA','CBC_CAT1','CBC_CAT2','CBC_CAT3'))
            irequired=sum(1<<inames.index(x) for x in ('NO_CBC_HW_INJ','NO_BURST_HW_INJ','NO_DETCHAR_HW_INJ','NO_STOCH_HW_INJ'))
            good=((quality&qrequired)==qrequired)&((injections&irequired)==irequired)
            train=np.asarray(strain[:2048*FS],dtype=float)*1e21
            if not np.all(np.isfinite(train)):raise ValueError('Nonfinite training data')
            spectra=[]; rejected=[]
            for second in range(0,2048-4+1,2):
                if not np.all(good[second:second+4]):rejected.append(second);continue
                freq,p=periodogram(train[second*FS:(second+4)*FS],fs=FS,
                                   window='hann',detrend='constant',scaling='density')
                spectra.append(p)
            spectra=np.asarray(spectra)
            if len(spectra)<512:raise ValueError('Insufficient clean training intervals')
            even=2*np.arange(1,(len(spectra)-1)//2+1)
            median_bias=1+np.sum(1/(even+1)-1/even)
            median=np.median(spectra,axis=0)/median_bias
            mean=spectra.mean(axis=0)
            if np.any(median<=0):raise ValueError('Nonpositive measured PSD')
            full_acf=FS/2*np.fft.irfft(median)
            cov=toeplitz(full_acf[::STRIDE][:INTERVAL_SAMPLES])
            w,dcov,inverse=polynomial_whitener(median,FS,INTERVAL_SAMPLES)
            residual=np.max(abs(inverse@dcov@inverse.T-np.eye(len(w))))
            print(json.dumps(dict(detector=detector,diagnostic_residual=float(residual),
                projected_condition=float(np.linalg.cond(dcov)),
                raw_ASD={str(f):float(np.sqrt(median[np.argmin(abs(freq-f))])*1e-21) for f in (0,5,10,20,50,100,250,500,1000,2000)},
                largest_PSD_frequency=float(freq[np.argmax(median)]))),flush=True)
            if residual>1e-5:raise ValueError(f'Numerical whitening failed: {residual}')
            # Independent direct Fourier sum, rather than irfft convention reuse.
            df=freq[1]-freq[0]
            direct=np.array([df*(np.sum(median[1:-1]*np.cos(2*np.pi*freq[1:-1]*lag*STRIDE/FS))+
                              (median[0]+median[-1]*np.cos(np.pi*lag*STRIDE))/2) for lag in range(12)])
            acf_residual=float(np.max(abs(direct-cov[0,:12]))/cov[0,0])
            if acf_residual>1e-12:raise ValueError('PSD covariance convention failed')
            segments=[]; times=[]
            # Spacing > window and fixed before inspecting the strain samples.
            for second in range(2048,4094,8):
                if not good[second]:continue
                begin=second*FS+1536
                y=np.asarray(strain[begin:begin+INTERVAL_SAMPLES*STRIDE:STRIDE],dtype=float)*1e21
                if not np.all(np.isfinite(y)):raise ValueError('Nonfinite held-out data')
                segments.append(y);times.append(start+begin/FS)
            data=np.asarray(segments)
            whitened=data@w.T
            expected=len(w)
            chi=np.sum(whitened**2,axis=1)/expected
            # The matched-filter variance is more pertinent than total power.
            t=np.arange(INTERVAL_SAMPLES)*STRIDE/FS
            bases=np.column_stack([np.exp(-t/.004)*np.cos(2*np.pi*f*t+phase)
                      for f in (150,250,400,600) for phase in (0.,np.pi/2)])
            wb=w@bases;wb/=np.linalg.norm(wb,axis=0)
            scores=whitened@wb
            synthetic=np.random.default_rng(130527+len(rows)).normal(size=(512,expected))
            raw_json=dict(detector=detector,input_sha256=digest,input_path=str(path),
                GPSstart=start,duration_s=duration,seconds_before_event=EVENT_GPS-(start+duration),
                sample_rate_hz=FS/STRIDE,original_sample_rate_hz=FS,interval_samples=INTERVAL_SAMPLES,
                duration_used_s=INTERVAL_SAMPLES*STRIDE/FS,training_seconds=[0,2048],
                sample_selection='Every second sample, no antialias filter. Full original PSD integrated at the retained time lags, so aliased noise is included exactly. Model uses identical sample times.',
                training_windows=len(spectra),rejected_training_start_seconds=rejected,
                quality_required=['DATA','CBC_CAT1','CBC_CAT2','CBC_CAT3'],
                injections_required=[inames[i] for i in range(len(inames)) if irequired&(1<<i)],
                hardware_CW_present_seconds=int(np.count_nonzero((injections&(1<<inames.index('NO_CW_HW_INJ')))==0)),
                CW_scope='CW hardware injections are not vetoed in CBC selection; their lines remain in measured noise and covariance',
                method='4 s Hann, 50 percent overlap, per-window constant subtraction, bias-corrected median periodogram',
                median_bias=float(median_bias),no_PSD_floor=True,no_filter=True,
                nuisance='Degree-2 polynomial quotient within truncated interval; covariance formed from projected spectral factors',
                whitened_dof=expected,whitening_residual=float(residual),
                direct_fourier_acf_relative_residual=acf_residual,
                covariance_condition_number=float(np.linalg.cond(cov)),
                projected_covariance_condition_number=float(np.linalg.cond(dcov)),
                N_held_out=len(data),held_out_GPS=times,
                reduced_chisquare_05_50_95=np.quantile(chi,[.05,.5,.95]).tolist(),
                reduced_chisquare_mean=float(chi.mean()),
                matched_filter_mean=scores.mean(axis=0).tolist(),
                matched_filter_standard_deviation=scores.std(axis=0,ddof=1).tolist(),
                matched_filter_frequencies_hz=[150,150,250,250,400,400,600,600],
                median_mean_PSD_ratio_20_1000_05_50_95=np.quantile(median[(freq>=20)&(freq<=1000)]/mean[(freq>=20)&(freq<=1000)],[.05,.5,.95]).tolist(),
                synthetic_identity_reduced_chisquare=float(np.mean(synthetic**2)))
            target=output/f'{detector}_noise.npz'
            if target.exists():raise FileExistsError('Preserve measured noise artifact; inspect before rerunning')
            np.savez_compressed(target,frequency_hz=freq,median_psd_strain=median*1e-42,
                mean_psd_strain=mean*1e-42,covariance_scaled=cov,projected_covariance_scaled=dcov,whitener_scaled=w,
                held_out_strain_scaled=data,held_out_GPS=np.asarray(times))
            raw_json['cache_sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
            rows.append(raw_json)
            print(json.dumps({k:raw_json[k] for k in ('detector','N_held_out','covariance_condition_number','whitening_residual','reduced_chisquare_05_50_95','matched_filter_standard_deviation')}),flush=True)
    atomic_json(ROOT/'C5_EMPIRICAL_NOISE.json',dict(status='MEASURED_OFF_SOURCE_ONLY',
        on_source_strain_read=False,preserved_failures=['Raw covariance inversion failed numerical whitening threshold 1e-5 with residual 0.00018503155529314697', 'Third differencing also failed threshold with residual 1.763295792168096e-05', 'Full-rate spectral projection failed at 0.00012499182145366455, covariance condition 1.0949792726729224e15. Strong 5.75 Hz noise and released near-Nyquist rolloff cause the dynamic range; exact stride-2 selection includes the aliased noise and discards no pre-onset samples. All prior scripts preserved.'],
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),detectors=rows))

if __name__=='__main__':main()
