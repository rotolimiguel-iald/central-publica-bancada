"""Reference-PSD forecasts, not measured evidence or a single-event likelihood.

The deformation multiplies Gamma, not beta. Point hypotheses are a=0 and a=1.
For a locally Gaussian experiment their log Bayes ratio has mean +/-z^2/2
and standard deviation z. No free-parameter Occam factor is inserted.
Single-220 mass/spin/dephasing non-identifiability is checked explicitly.
"""
import json
import math
import argparse
from pathlib import Path
import numpy as np
from fetch_public import atomic_json
from tgl_ringdown_prediction import prediction, kerr_220
from tgl_ringdown_template import damped_cosine_fourier

ROOT=Path(__file__).resolve().parent

def run(empirical=False):
    inputs=json.loads((ROOT/'FISHER_INPUTS.json').read_bytes())
    qrow=next(r for r in inputs['mode_220'] if r['spin']==.68)
    qexact=complex(qrow['omega_real'],qrow['omega_imag'])
    # Deliberately a reference source, not an estimate of an observed event.
    mass,spin=68.1,.68
    fmax=1024. if empirical else 2048.
    f=np.arange(20.,fmax+.0001,.125)
    df=f[1]-f[0]
    records=[]
    source_norms={}
    if empirical:
        inputs['psds']=[dict(key='O4_MEASURED_'+d,filename=d+'_noise.npz',kind='PSD') for d in ('H1','L1')]
    for curve in inputs['psds']:
        if empirical:
            cache=np.load(ROOT/'cache/empirical_noise'/curve['filename'])
            raw=np.column_stack([cache['frequency_hz'],cache['median_psd_strain']])
        else:
            raw=np.loadtxt(ROOT/'cache/psd'/curve['filename'])
        valid=(raw[:,0]>0)&(raw[:,1]>0)&np.isfinite(raw[:,1])
        xp,yp=raw[valid,0],raw[valid,1]
        if xp.min()>f.min() or xp.max()<f.max():
            raise ValueError('PSD does not cover the forecast band')
        psd=np.exp(np.interp(np.log(f),np.log(xp),np.log(yp)))
        if curve['kind']=='ASD': psd=psd**2
        if empirical:
            # Match stride-2 sample selection: sum the mirrored upper-band noise.
            # The near-2048-Hz release rolloff is not a new low-noise detector band.
            mirrored=2048.-f
            psd+=np.exp(np.interp(np.log(mirrored),np.log(xp),np.log(yp)))
        weight=4*df/psd
        weight[0]*=.5; weight[-1]*=.5
        inner=lambda u,v: float(np.sum(weight*(u.conj()*v).real))
        for reading in ['R-A','R-B','R-MOD','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-LIN','R-GLOBAL']:
            kwargs={'qnm_dimensionless':qexact} if reading=='R-MOD' else {}
            pred=prediction(mass,spin,reading,**kwargs)
            baseq=kerr_220(mass,spin,**kwargs)
            fr,d=baseq['f_gr_hz'],1/baseq['tau_gr_s']
            rawh=damped_cosine_fourier(f,1.,fr,d)
            norm=math.sqrt(inner(rawh,rawh))
            if reading=='R-B':source_norms[curve['key']]=norm
            h=rawh/norm
            # Derivatives wrt log amplitude, phase, log frequency, log decay.
            zminus=d+2j*np.pi*(f-fr); zplus=d+2j*np.pi*(f+fr)
            dphase=.5j*(1/zminus-1/zplus)/norm
            dlogf=.5*(2j*np.pi*fr/zminus**2-2j*np.pi*fr/zplus**2)/norm
            dlogd=-.5*d*(1/zminus**2+1/zplus**2)/norm
            # Derivative wrt deformation a at a=0; factor x isolated so tiny
            # Planck-clock signals do not poison the SVD conditioning.
            direction=dlogd
            x=pred['x']
            matrix=np.array([[inner(u,v) for v in [h,dphase,dlogf,dlogd]]
                             for u in [h,dphase,dlogf,dlogd]])
            for snr in [10.,20.,40.,80.,200.,600.]:
                fixed = matrix[3,3]-matrix[3,:2]@np.linalg.solve(matrix[:2,:2],matrix[:2,3])
                freqfree=matrix[3,3]-matrix[3,:3]@np.linalg.solve(matrix[:3,:3],matrix[:3,3])
                for scenario,information in [('MASS_SPIN_FIXED_OPTIMISTIC',fixed),
                                            ('FREQUENCY_FREE_TAU_GR_FIXED',freqfree)]:
                    sigma_delta_linear=1/(snr*math.sqrt(max(information,0.)))
                    z=x/sigma_delta_linear
                    records.append(dict(psd=curve['key'],reading=reading,snr_ringdown=snr,
                      scenario=scenario,delta_exact=pred['delta_tau_ensemble_exact'],x=x,
                      sigma_delta_local=sigma_delta_linear,z_local=z,
                      lnB_point_mean_if_reading=z*z/2,lnB_point_mean_if_GR=-z*z/2,
                      lnB_point_standard_deviation=z,
                      identical_independent_events_for_median_5sigma=(math.ceil(25/z**2) if z>0 else None),
                      scope='LOCAL_LINEAR_GAUSSIAN_POINT_FORECAST__ALIASED_MEASURED_PSD__CONTINUOUS_ENSEMBLE_APPROXIMATION' if empirical else 'LOCAL_LINEAR_GAUSSIAN_POINT_FORECAST__REFERENCE_PSD__ENSEMBLE_TEMPLATE',
                      strong_shift_caution=x>.1))
            # M and spin supply the same two shape directions as f and tau.
            # A single 220 mode cannot additionally identify deformation a.
            # Verify numerically using actual Kerr parameter derivatives.
            step=1e-5
            def shape(m,a):
                if reading=='R-MOD':
                    # The rank result holds for exact Kerr as well; use an
                    # independent BCW rank witness, no exact-spin derivative claim.
                    pass
                v=kerr_220(m,a)
                return damped_cosine_fourier(f,1.,v['f_gr_hz'],1/v['tau_gr_s'])
            rankh=shape(mass,spin)
            ranknorm=math.sqrt(inner(rankh,rankh))
            dm=(shape(mass*np.exp(step),spin)-shape(mass*np.exp(-step),spin))/(2*step*ranknorm)
            da=(shape(mass,spin+step)-shape(mass,spin-step))/(2*step*ranknorm)
            qb=kerr_220(mass,spin)
            db=1/qb['tau_gr_s']; fb=qb['f_gr_hz']
            target=-.5*db*(1/(db+2j*np.pi*(f-fb))**2+1/(db+2j*np.pi*(f+fb))**2)/ranknorm
            gram=np.array([[inner(u,v) for v in [dm,da]] for u in [dm,da]])
            rhs=np.array([inner(u,target) for u in [dm,da]])
            coeff=np.linalg.solve(gram,rhs)
            residual=target-coeff[0]*dm-coeff[1]*da
            rel=math.sqrt(inner(residual,residual)/inner(target,target))
            if rel>2e-7:raise AssertionError(('Mass/spin degeneracy oracle failed',rel))
        print(json.dumps({'psd':curve['key'],'mass_spin_degeneracy_relative_residual':rel}),flush=True)
    same_source=[]
    for curve,norm in source_norms.items():
        reference_key='O4_MEASURED_H1' if empirical else 'O4'
        ratio=norm/source_norms[reference_key]
        row=next(r for r in records if r['psd']==curve and r['reading']=='R-B' and
                 r['snr_ringdown']==40 and r['scenario']=='FREQUENCY_FREE_TAU_GR_FIXED')
        zz=row['z_local']*ratio
        same_source.append(dict(psd=curve,snr_ratio_to_O4=ratio,snr_if_O4_were_40=40*ratio,
            z_local=zz,lnB_mean_if_reading=zz*zz/2,lnB_standard_deviation=zz,
            scope='Same source, same projection, individual reference PSD; no detector network or cosmological population forecast'))
    atomic_json(ROOT/('C5_FISHER_EMPIRICAL.json' if empirical else 'C5_FISHER.json'),dict(status='CONDITIONAL_MEASURED_PSD_FORECAST_COMPLETE' if empirical else 'CONDITIONAL_REFERENCE_FORECAST_COMPLETE',
        inputs_sha256=__import__('hashlib').sha256((ROOT/'FISHER_INPUTS.json').read_bytes()).hexdigest(),
        parameters=dict(mass_detector_solar=mass,spin=spin,source_status='ILLUSTRATIVE_INPUT',
                        frequency_band_hz=[20,fmax],frequency_step_hz=.125),
        records=records,same_source_R_B=same_source,same_source_reference='O4_MEASURED_H1' if empirical else 'O4',
        PSD_scope='Measured H1 and L1, each a separate single-detector forecast: original PSD plus mirrored upper-band alias, 20-1024 Hz to match retained sample rate. Continuous causal Fourier waveform approximation; empirical finite-interval C5 likelihood is the definitive calibration.' if empirical else 'Reference design curves',
        noise_artifact_sha256=__import__('hashlib').sha256((ROOT/'C5_EMPIRICAL_NOISE.json').read_bytes()).hexdigest() if empirical else None,
        mass_spin_free=dict(status='NON_IDENTIFIABLE_SINGLE_220',
          evidence='Deformation tangent lies in mass/spin tangent span',
          last_relative_residual=rel,lnB_from_ringdown_alone=None,
          remedy='Independent mass/spin information or additional resolved modes; joint prior treatment required'),
        not_in_this_local_fisher_approximation=['Full-IMR uncertainty and priors','Finite-interval empirical coverage','Single-event stochastic likelihood'],
        interpretation='Reference O5 A+ is a scenario, not a scheduled achieved sensitivity; no actual data Bayes factors'))
    for curve in [c['key'] for c in inputs['psds']]:
        print(json.dumps(next(r for r in records if r['psd']==curve and r['reading']=='R-B' and
            r['snr_ringdown']==40 and r['scenario']=='FREQUENCY_FREE_TAU_GR_FIXED')),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--empirical',action='store_true')
    run(empirical=parser.parse_args().empirical)
