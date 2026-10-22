"""Conditional Bayes-ratio distributions with recolored held-out noise.

Two IMR families, all eight scalar-rate readings, six SNRs, a=0/1, three
recovery models. FULL_IMR is the model-mismatch test. MATCHED_RINGDOWN is a
separate numerical calibration and cannot validate the physical IMR model.
All computations hold the true remnant fixed: information is optimistic.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import hashlib
import json
import numpy as np
from fetch_public import atomic_json
from diagnose_overtones import GROUPS, control_modes, mode_basis
from tgl_ringdown_prediction import prediction, scales
from tgl_ringdown_likelihood import linear_statistics, profile_intervals

ROOT=Path(__file__).resolve().parent
READINGS=['R-A','R-B','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-LIN','R-MOD','R-GLOBAL']
FITS=['220_440','220_221_222_440','eight_modes']
SNRS=[10.,20.,40.,80.,200.,600.]
RESPONSES={'H1':(.7,.2),'L1':(-.3,.8)}
N=50

def distribution(values):
    return dict(mean=float(np.mean(values)),standard_deviation=float(np.std(values,ddof=1)),
        quantiles_05_50_95=np.quantile(values,[.05,.5,.95]).tolist(),
        fraction_gt_log100=float(np.mean(values>np.log(100))),
        fraction_lt_minus_log100=float(np.mean(values<-np.log(100))))

def main():
    meta=json.loads((ROOT/'C5_RECOLORED_NOISE.json').read_bytes())
    families=json.loads((ROOT/'C5_IMR_CONTROLS.json').read_bytes())['families']
    folder=ROOT/'cache/recolored_forecast';folder.mkdir(exist_ok=True)
    all_rows=[];receipts=[];sensitivity=[]
    for family in families:
        exact=control_modes(family);mass=family['remnant_mass_detector_solar'];spin=family['remnant_spin']
        source=ROOT/'cache/imr_controls'/f"{family['family']}.npz"
        if hashlib.sha256(source.read_bytes()).hexdigest()!=family['sha256']:raise ValueError('IMR source changed')
        waveform=np.load(source)
        for scenario in meta['scenarios']:
            path=ROOT/scenario['cache_path']
            if hashlib.sha256(path.read_bytes()).hexdigest()!=scenario['cache_sha256']:raise ValueError('Noise scenario changed')
            cache=np.load(path);w=cache['whitener_scaled'];times=np.arange(w.shape[1])/2048.
            peak_times=times+10*scales(mass,'CODATA2018_IAU2015')[0]
            components={k:np.interp(peak_times,waveform['time_from_peak_s'],waveform[k])*1e21
                for k in ('22_plus','22_cross','44_plus','44_cross','other_plus','other_cross')}
            xi={d:cache[d+'_strain_scaled'][:N]@w.T for d in RESPONSES}
            vectors=[];rows=[]
            for fit in FITS:
                modes=GROUPS[fit]
                for reading in READINGS:
                    predictions={ell:prediction(mass,spin,reading,mode=(ell,ell,0),qnm_dimensionless=exact[(ell,ell,0)]) for ell in (2,4)}
                    maxx=max(p['x'] for p in predictions.values());unresolved=maxx<1e-12
                    grid=np.array([0.,1.]) if unresolved else np.unique(np.r_[np.linspace(-.8,2.,1201)/maxx,0.,1.])
                    raw=mode_basis(times,family,reading,modes,grid,exact)
                    basis=np.einsum('kt,gti->gki',w,raw,optimize=True)
                    zero=int(np.flatnonzero(grid==0)[0]);one=int(np.flatnonzero(grid==1)[0])
                    raw_gr={d:sum(fp*components[c+'_plus']+fc*components[c+'_cross'] for c in ('22','44','other')) for d,(fp,fc) in RESPONSES.items()}
                    # Projection determines only the declared manufactured matched control.
                    amplitudes={d:np.linalg.lstsq(basis[zero],w@raw_gr[d],rcond=None)[0] for d in RESPONSES}
                    targets={d:[] for d in RESPONSES};clean={d:[] for d in RESPONSES};cells=[]
                    for content in ('FULL_IMR','MATCHED_RINGDOWN'):
                        for injected in (0.,1.):
                            signals={}
                            for d,(fp,fc) in RESPONSES.items():
                                if content=='MATCHED_RINGDOWN':
                                    signals[d]=basis[one if injected else zero]@amplitudes[d]
                                else:
                                    y=fp*components['other_plus']+fc*components['other_cross']
                                    for ell in (2,4):
                                        name=str(ell)*2
                                        y=y+(fp*components[name+'_plus']+fc*components[name+'_cross'])*np.exp(-injected*predictions[ell]['gamma_per_s']*peak_times)
                                    signals[d]=w@y
                            norm=np.sqrt(sum(np.dot(s,s) for s in signals.values()))
                            for snr in SNRS:
                                for d in RESPONSES:
                                    clean[d].append(signals[d]*snr/norm)
                                    targets[d].extend(xi[d]+signals[d][None,:]*snr/norm)
                                cells.append(dict(family=family['family'],psd=scenario['psd'],recovery=fit,
                                    reading=reading,content=content,injected_a=injected,SNR=snr,
                                    reference_SNR_at_403Mpc=float(norm),max_Gamma_tau=float(maxx)))
                    profile=None;marginal=None;clean_profile=None
                    for d in RESPONSES:
                        p,m=linear_statistics(basis,np.array(targets[d]),10.)
                        pc,_=linear_statistics(basis,np.array(clean[d]),10.)
                        if profile is None:profile=p;marginal=m;clean_profile=pc
                        else:profile+=p;marginal+=m;clean_profile+=pc
                    log_ratios=marginal[one]-marginal[zero]
                    diagnostics=None if unresolved else profile_intervals(grid,profile)
                    clean_fit=None if unresolved else profile_intervals(grid,clean_profile)
                    for index,cell in enumerate(cells):
                        lo=index*N;hi=(index+1)*N;lnb=log_ratios[lo:hi]
                        cell.update(N=N,lnB=distribution(lnb),draws_index=len(vectors))
                        if unresolved:
                            cell.update(status='UNIDENTIFIABLE_AT_NUMERICAL_AND_OBSERVATIONAL_PRECISION',
                                absolute_bias=None,coverage_90=None,boundary_hits=None,power_proxy=None)
                            data=np.column_stack([lnb,np.full((N,3),np.nan)])
                        else:
                            fits=diagnostics[lo:hi]
                            ahat=np.array([v['MLE'] for v in fits]);intervals=np.array([v['CI90'] for v in fits])
                            coverage=float(np.mean((intervals[:,0]<=cell['injected_a'])&(cell['injected_a']<=intervals[:,1])))
                            bias=float(abs(np.median(ahat)-cell['injected_a']))
                            boundaries=sum(v['boundary'] for v in fits)
                            sigma=float(np.median(intervals[:,1]-intervals[:,0])/(2*1.6448536269514722))
                            literal=bias<=.2 and .8<=coverage<=.97
                            # Do not silently change the handoff's two numeric conditions.
                            cell.update(absolute_bias=bias,coverage_90=coverage,boundary_hits=boundaries,
                                original_numeric_criteria_pass=bool(literal),
                                status='CALIBRATED_CONDITIONAL_CELL' if literal and not boundaries else 'INCONCLUSIVE_SYSTEMATICS',
                                interval_truncation_additional_caution=bool(boundaries),
                                power_proxy=1/sigma if not boundaries else None,
                                power_scope='1 / median profile sigma_a; fixed remnant; no calibrated Gaussian significance when coverage fails',
                                noiseless_a_hat=clean_fit[index]['MLE'],
                                noiseless_residual_norm_squared=float(cell['SNR']**2-2*np.max(clean_profile[:,index])))
                            data=np.column_stack([lnb,ahat,intervals])
                        vectors.append(data);rows.append(cell)
                    # Low-frequency continuation: point evidence at primary SNR40
                    # with the same standardized residuals, for both hypotheses.
                    if reading=='R-B':
                        for exponent in (2,6):
                            altw=cache[f'whitener_low{exponent}'];altbasis=np.einsum('kt,gti->gki',altw,raw[[zero,one]],optimize=True)
                            for injected in (0.,1.):
                                signal={}
                                for d,(fp,fc) in RESPONSES.items():
                                    y=fp*components['other_plus']+fc*components['other_cross']
                                    for ell in (2,4):
                                        name=str(ell)*2
                                        y=y+(fp*components[name+'_plus']+fc*components[name+'_cross'])*np.exp(-injected*predictions[ell]['gamma_per_s']*peak_times)
                                    signal[d]=altw@y
                                norm=np.sqrt(sum(s@s for s in signal.values()))
                                lm=sum(linear_statistics(altbasis,xi[d]+signal[d][None,:]*40/norm,10.)[1] for d in RESPONSES)
                                baseline=next(r for r in rows if r['recovery']==fit and r['reading']==reading and r['content']=='FULL_IMR' and r['injected_a']==injected and r['SNR']==40)
                                sensitivity.append(dict(family=family['family'],psd=scenario['psd'],recovery=fit,
                                    injected_a=injected,low_exponent=exponent,lnB=distribution(lm[1]-lm[0]),
                                    difference_in_mean=float(np.mean(lm[1]-lm[0])-baseline['lnB']['mean'])))
                    print(json.dumps(dict(family=family['family'],psd=scenario['psd'],fit=fit,reading=reading,cells=len(cells))),flush=True)
            target=folder/f"{family['family']}_{scenario['psd']}.npz"
            if target.exists():raise FileExistsError('Forecast cache already exists; preserve before resuming')
            np.savez_compressed(target,draws=np.array(vectors),columns=['lnB','a_hat','CI90_lower','CI90_upper'],
                                H1_original_GPS=cache['H1_original_GPS'][:N],L1_original_GPS=cache['L1_original_GPS'][:N])
            for row in rows:row['draws_cache']=str(target.relative_to(ROOT))
            receipts.append(dict(path=str(target.relative_to(ROOT)),sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
            all_rows.extend(rows)
            atomic_json(folder/f"{family['family']}_{scenario['psd']}.json",dict(rows=rows))
    atomic_json(ROOT/'C5_RECOLORED_FORECAST.json',dict(status='CONDITIONAL_DISTRIBUTIONS_MEASURED',
        scenarios=4,families=2,recovery_models=FITS,readings=READINGS,snrs=SNRS,
        start_tM=10.,N_per_cell=N,number_of_cells=len(all_rows),noise_independence='The same 50 paired O4 intervals are reused across all cells; not independent simulated events across cells.',
        source_clock='All 22 overtones share the effective imposed 220 Gamma; 44 overtones share 440 Gamma; other harmonics unchanged. Conditional whole-harmonic injection, not a unique TGL overtone prediction.',
        parameters_fixed='True remnant mass/spin; response factors H1=(.7,.2), L1=(-.3,.8); 0.2002 s at 2048 Hz.',
        likelihood='Independent real quadratures per mode per detector, Normal(0,1e-20 strain) prior; exact integral and determinant retained.',
        identification='Likelihood ratios compare a=1 to a=0; no conversion to sigma or physical confirmation. MATCHED_RINGDOWN is a separate manufactured calibration.',
        no_target_strain_access=True,registered_C6_unchanged=True,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        noise_manifest_sha256=hashlib.sha256((ROOT/'C5_RECOLORED_NOISE.json').read_bytes()).hexdigest(),
        draws=receipts,low_frequency_controls=sensitivity,results=all_rows))

if __name__=='__main__':main()
