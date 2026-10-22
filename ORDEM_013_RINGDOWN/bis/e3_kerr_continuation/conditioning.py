"""Future-only GWOSC conditioning. No file opened until prepare() is called."""
import numpy as np
from scipy.signal import butter,filtfilt,freqz
from scipy.interpolate import interp1d
from scipy.linalg import toeplitz,cholesky
from kerr_model import geometry


def public_psd_acf(path,config):
    """Reproduce the 2.7.0 external-PSD interpolation prescription explicitly.

    A public NRSur PSD is a robustness INPUT, never asserted identical to the
    unavailable H1_PSD.txt/L1_PSD.txt used by the released pyRing run.
    """
    table=np.loadtxt(path,comments='#')
    if table.ndim!=2 or table.shape[1]!=2 or not np.isfinite(table).all():raise ValueError('Expected two numeric PSD columns')
    f,p=table.T
    if np.any(np.diff(f)<=0) or np.any(p<=0):raise ValueError('Invalid public PSD')
    mask=(f>max(config['band_hz'][0],20.))&(f<min(config['band_hz'][1],2038.))
    if mask.sum()<2:raise ValueError('Insufficient PSD support')
    n=int(config['noise_chunk_s']*config['sample_rate_hz'])
    grid=np.fft.rfftfreq(n,1/config['sample_rate_hz'])
    density=interp1d(f[mask],p[mask],fill_value='extrapolate',bounds_error=False)(grid)
    if not np.isfinite(density).all() or np.any(density<=0):
        raise ValueError('Legacy PSD extrapolation nonpositive: no clipping or replacement')
    return .5*config['sample_rate_hz']*np.fft.irfft(density,n=n)


def prepare(config,variant,root,guard,helpers):
    """Pinned E2 readers reused read-only; their exact hashes are dependencies."""
    window,offsource_psd,require_pin=helpers
    from custody import contained
    fs=config['sample_rate_hz'];n=int(fs*config['analysis_duration_s'])
    if n!=819 or fs!=4096:raise ValueError('Unreviewed sampling/window contract')
    ba=butter(4,[v/(fs*.5) for v in config['band_hz']],btype='band')
    blocks=[];receipts=[]
    for name in config['detectors']:
        guard();data=config['data'][name]
        onpath=contained(root,data['onsource_path'])
        offpath=contained(root,data['offsource_path'])
        y,rate,epoch=window(onpath,data['onsource_sha256'],config['read_start_GPS'],config['read_duration_s'],config['quality_required'],config['injection_flags_required'])
        if rate!=fs or epoch!=config['read_start_GPS']:raise ValueError('No implicit resampling or epoch shift')
        conditioned=filtfilt(*ba,y)
        if not np.isfinite(conditioned).all():raise ValueError('Bandpass produced nonfinite strain')
        obj,delay,gmst=geometry(name,config)
        # Preserve fractional delay analytically; only membership on native grid
        # is discretized, exactly the >=t0 truncation in pyRing likelihood.pyx.
        relative=(epoch-config['trigger_GPS']-delay)+np.arange(len(y))/fs
        selection=np.flatnonzero(relative>=config['start_offset_s'])[:n]
        if len(selection)!=n:raise ValueError('Incomplete analysis segment')
        if selection[0]<fs or selection[-1]>len(y)-fs:raise ValueError('Filter padding less than one second')
        if variant=='welch':
            psdcfg=dict(psd_duration_s=config['psd_duration_s'],psd_segment_s=config['noise_chunk_s'],
              offsource_exclusion_s=config['offsource_exclusion_s'],event_GPS=config['trigger_GPS'],
              segment_start_GPS=config['read_start_GPS'],quality_required=config['quality_required'],
              injection_flags_required=config['injection_flags_required'])
            freq,p,psdreceipt=offsource_psd(offpath,data['offsource_sha256'],psdcfg)
            _,transfer=freqz(*ba,worN=freq,fs=fs)
            # filtfilt has |H|^2 amplitude, hence |H|^4 power.
            filtered=p*np.abs(transfer)**4
            acf=.5*fs*np.fft.irfft(filtered,n=2*(len(freq)-1))
            psdreceipt['transfer']='raw Welch PSD times |Butterworth response|^4'
        elif variant=='public_psd':
            spec=config['public_psd'][name]
            path=contained(root,spec['relative_to_Chatgpt']);require_pin(path,spec['sha256'])
            acf=public_psd_acf(path,config)
            psdreceipt=dict(source_sha256=spec['sha256'],member=spec['archive_member'],
              method='pyRing 2.7.0 external PSD interpolation/extrapolation',same_as_release_psd='UNKNOWN')
        else:raise ValueError('Unknown PSD branch')
        guard()
        covariance=toeplitz(acf[:n])/config['reference_amplitude']**2
        if not np.isfinite(covariance).all():raise ValueError('Nonfinite covariance')
        condition=float(np.linalg.cond(covariance))
        if not np.isfinite(condition) or condition>1e12:raise ValueError('Covariance fails registered conditioning threshold; no jitter')
        factor=cholesky(covariance,lower=True,check_finite=True)
        logdet=2*np.log(np.diag(factor)).sum()+2*n*np.log(config['reference_amplitude'])
        lognormal=-.5*(n*np.log(2*np.pi)+logdet)
        selected=conditioned[selection]
        blocks.append(dict(data=selected,relative_times=relative[selection],response=obj.response,gmst=gmst,
          cholesky_scaled=factor,log_normalization=float(lognormal)))
        receipts.append(dict(detector=name,onsource_sha256=data['onsource_sha256'],psd=psdreceipt,
          delay_relative_to_H1_s=delay,first_relative_time_s=float(relative[selection[0]]),
          start_grid_residual_s=float(relative[selection[0]]-config['start_offset_s']),
          sample_count=n,nominal_duration_s=config['analysis_duration_s'],sample_count_over_fs=n/fs,
          window='No onsource taper; native-grid crop',covariance_condition_number=condition,
          conditioning='4th order Butterworth + filtfilt on padded segment; model unfiltered as pyRing 2.7.0',
          independent_between_detectors=True))
    return blocks,receipts
