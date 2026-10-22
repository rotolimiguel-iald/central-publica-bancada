"""F4: light norm measurement and frozen-Fisher re-expression, no new C6 PE."""
import os
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import sys,json,math,hashlib
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import numpy as np
import h5py
from scipy.special import logsumexp

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(2**20),b''):h.update(b)
    return h.hexdigest()

def new(p,d):
    if p.exists():raise FileExistsError(p)
    raw=(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise RuntimeError('Write mismatch')
    tmp.replace(p)

def free_evidence(x,sigma,true_a,n=128):
    # Exact normalized scalar Gaussian likelihood; integrate a and sampling noise.
    nodes,weights=np.polynomial.legendre.leggauss(n)
    amps=(nodes+1)/2;weights=weights/2
    eps,probs=np.polynomial.hermite.hermgauss(n)
    ys=math.log1p(true_a*x)/sigma+math.sqrt(2)*eps
    probs=probs/math.sqrt(math.pi)
    shift=np.log1p(amps*x)/sigma
    logs=logsumexp(ys[:,None]*shift-.5*shift**2+np.log(weights),axis=1)
    mean=float(probs@logs);std=math.sqrt(max(0,float(probs@(logs-mean)**2)))
    return dict(mean_lnB=mean,sd_lnB=std)

def main():
    paths=[ROOT/n for n in ['REGISTRO_C6.json','C6_DOWNLOADS.json','C6_STRAIN_10M_GRID_1.json',
        'C5_FISHER.json','C5_FISHER_EMPIRICAL.json','C5_IMR_RECOVERY.json',
        'C5_SOURCE_UNCERTAINTY_SUMMARY.json','C1_LEITURAS_v3.json','FISHER_INPUTS.json',
        'C5_EMPIRICAL_NOISE.json']]
    reg=json.loads(paths[0].read_bytes());downloads=json.loads(paths[1].read_bytes())
    frozen=json.loads(paths[2].read_bytes())
    if sha(paths[0])!=downloads['registration_sha256'] or sha(paths[0])!=frozen['registration_sha256']:
        raise ValueError('C6 registration mismatch')
    norms=[]
    for detector in ('H1','L1'):
        receipt=next(r for r in downloads['files'] if r['detector']==detector)
        # A receipt may use Windows paths even under WSL; use the observed basename only.
        basename=receipt['path'].replace('\\','/').split('/')[-1]
        p=ROOT/'cache/gwosc/on_source'/basename
        if sha(p)!=receipt['sha256']:raise ValueError('Strain hash differs')
        wpath=ROOT/f'cache/empirical_noise/{detector}_noise.npz'
        if sha(wpath)!=reg['code_and_input_hashes'][str(wpath.relative_to(ROOT))]:
            raise ValueError('Noise metric changed')
        with np.load(wpath) as z:W=z['whitener_scaled'].copy()
        with h5py.File(p,'r') as h:
            gps0=float(h['meta/GPSstart'][()]);raw=h['strain/Strain'];fs=1/float(raw.attrs['Xspacing'])
            if fs!=4096:raise ValueError('Wrong original sample rate')
            requested=reg['reference_peak_GPS'][detector]+10*reg['reference_tM_seconds']
            first=math.ceil((requested-gps0)*fs)
            y=np.asarray(raw[first:first+reg['interval_samples']*2:2])*1e21
        white=W@y;norm=float(white@white)
        if not math.isclose(norm,frozen['noise_metric_norm_squared'][detector],rel_tol=1e-12):
            raise ValueError('Frozen norm mismatch')
        norms.append(dict(detector=detector,norm_squared=norm,noise_degrees_of_freedom=W.shape[0],
            first_index=first,requested_GPS=requested,first_sample_GPS=gps0+first/fs,
            strain_sha256=sha(p),noise_metric_sha256=sha(wpath)))
        paths.extend([p,wpath])
    dof=sum(r['noise_degrees_of_freedom'] for r in norms)
    excess=sum(r['norm_squared'] for r in norms)-dof
    if excess<=0:raise ValueError('Nonpositive whitened excess: no SNR estimate')
    rho=math.sqrt(excess)
    rho_se=math.sqrt(2*dof+4*excess)/(2*rho)
    norm_result=dict(status='MEASURED_NORM_DERIVED_SNR_ESTIMATE_NOT_MATCHED_FILTER_DETECTION',
        detectors=norms,excess_norm_squared=excess,network_rho_estimate=rho,
        approximate_standard_error_if_white_gaussian=rho_se,
        assumptions='Subtract expected noise degrees of freedom; Gaussian stationary unit-variance residuals. Nonstationarity/PSD errors not included. No likelihood or strain fit rerun.',
        start_tM=10,nonblind=True)
    new(ROOT/'bis/F4_GW250114_WINDOW_POWER_NORM.json',norm_result)
    fisher=json.loads((ROOT/'C5_FISHER.json').read_bytes())
    empirical=json.loads((ROOT/'C5_FISHER_EMPIRICAL.json').read_bytes())
    recovery=json.loads((ROOT/'C5_IMR_RECOVERY.json').read_bytes())
    readings=json.loads((ROOT/'C1_LEITURAS_v3.json').read_bytes())['rows']
    updated=[];free=[]
    for old in fisher['records']:
        row=dict(old);x=row['x'];sigma=row['sigma_delta_local']
        z=math.log1p(x)/sigma
        sub=abs(row['delta_exact'])<1e-6
        row.update(hypothesis_type='POINT_FIXED_CLOCK_OR_FIXED_EFFECT',
            z_linear_historical=row['z_local'],z_logdecay=z,
            z_log_over_linear_minus_one=(math.log1p(x)/x-1 if x else 0),
            sigma_parameter='ln(decay/decay_GR), local Fisher metric',
            sigma_effective_delta_tau=(abs(row['delta_exact'])/z if z else None),
            numerical_gate_class='SUBRESOLUTION' if sub else 'FINITE_CONDITIONAL_EFFECT',
            lnB_point_mean_if_reading=z*z/2,lnB_point_mean_if_GR=-z*z/2,
            lnB_point_standard_deviation=z,
            lnB_numerical_equivalent=0.0 if sub else None,
            identical_independent_events_for_median_5sigma='SUBRESOLUTION' if sub else math.ceil(25/z**2))
        updated.append(row)
        if row['psd']=='O4' and row['scenario']=='MASS_SPIN_FIXED_OPTIMISTIC' and not sub:
            for true_a in (0.,1.):
                v=free_evidence(x,sigma,true_a,128);v64=free_evidence(x,sigma,true_a,64)
                discrepancy=max(abs(v[k]-v64[k]) for k in v)
                if discrepancy>1e-6:raise ValueError('Scalar free-prior quadrature unresolved')
                free.append(dict(reading=row['reading'],snr=row['snr_ringdown'],injected_a=true_a,
                    prior='INPUT Uniform a in [0,1]',likelihood='Gaussian scalar log-decay, exact shift log(1+a*x)',
                    tau_star_interpretation='For the quadratic fixed-partition law, uniform tau_star in [0,reference_tau_star] gives the identical integral; not a prior-free limit.',
                    quadrature_error_64_128=discrepancy,**v))
    fisher.update(supersedes='C5_FISHER.json',supersedes_sha256=sha(ROOT/'C5_FISHER.json'),
        records=updated,free_parameter_scalar_gaussian=free,
        not_done=['Full-IMR source-marginalized calibrated bias/coverage','Calibrated likelihood for one physical stochastic realization',
                  'Prior-independent free-clock evidence (not defined without prior)','ET/CE full-IMR recovery',
                  'SEOB numerical resolution at SNR >= 200'],
        completed_elsewhere=['Measured off-source PSD: C5_EMPIRICAL_NOISE.json and C5_FISHER_EMPIRICAL.json',
                             'PSD implementation controls: PSD_CONTROLS.json'],
        nonblind=True,interpretation='Reference PSD scenarios only; z_logdecay is a local Gaussian separation, not an observed significance.')
    special=[dict(reading=r['reading'],hypothesis_type='CONDITIONAL_ANALYTIC_NUMERICAL_EQUIVALENCE',
        lnB_numerical_equivalent=0.,N_5sigma='SUBRESOLUTION',physical_exact_equality=False,
        scope='Archived coherent occupation scenario only; not all occupations' if r['reading']=='R-RAIZ-COHERENT' else 'Archived Planck-scale propagation scenario only; not an added ringdown decay rate')
        for r in readings if r['reading'] in ('R-RAIZ-COHERENT','R-PROP')]
    fisher['analytic_additional_readings']=special
    new(ROOT/'C5_FISHER_v2.json',fisher)
    bases=[]
    unique={}
    for row in recovery['results']:
        key=(row['psd'],row['injection_family'])
        snr=row['reference_SNR_403Mpc']
        if key in unique and not math.isclose(unique[key],snr,rel_tol=1e-14):raise ValueError('Reference SNR inconsistent')
        unique[key]=snr
    for (psd,family),snr in sorted(unique.items()):
        bases.append(dict(name='REFERENCE_INJECTION_403Mpc',psd=psd,family=family,
            rho=snr,scale_from_SNR40=snr/40,frame='network at 10 tM; frozen illustrative response/source',
            origin='C5_IMR_RECOVERY.json reference_SNR_403Mpc'))
    bases.append(dict(name='GW250114_MEASURED_NORM_10tM',psd='O4',family=None,rho=rho,
        scale_from_SNR40=rho/40,frame='network measured norm excess, assumptions stated in norm receipt',
        origin='bis/F4_GW250114_WINDOW_POWER_NORM.json'))
    table=[]
    for base in bases:
        for r in readings:
            reading=r['reading']
            if reading in ('R-PROP','R-RAIZ-COHERENT'):
                fixed=dict(z_max_local=0.,sigma_effective_delta_tau=None,N_5sigma='SUBRESOLUTION',
                    lnB_numerical_equivalent=0.,scope=next(q['scope'] for q in special if q['reading']==reading))
                delta=None
            else:
                point=next(q for q in updated if q['psd']==base['psd'] and q['reading']==reading and
                    q['snr_ringdown']==40 and q['scenario']=='MASS_SPIN_FIXED_OPTIMISTIC')
                z=point['z_logdecay']*base['scale_from_SNR40'];delta=point['delta_exact']
                sub=abs(delta)<1e-6
                fixed=dict(z_max_local=z,sigma_effective_delta_tau=abs(delta)/z if z else None,
                    N_5sigma='SUBRESOLUTION' if sub else math.ceil(25/z**2),
                    lnB_numerical_equivalent=0. if sub else None,
                    scope='Optimistic fixed M/spin 220 reference-shape Fisher transported linearly in network SNR; not full-IMR calibration')
            table.append(dict(base=base['name'],psd=base['psd'],family=base['family'],reading=reading,
                rho=base['rho'],delta_L_reference_shape=delta,fixed_source=fixed,
                unknown_source_single_220=dict(z_max_local=0.,sigma_effective_delta_tau=None,
                    status='NON_IDENTIFIABLE_SINGLE_220',scope='Free M/spin absorb frequency/decay tangents. Null sigma field means unidentifiable, not zero error; not a claim about full IMR.'),
                power_gate='UNDERPOWERED' if fixed['z_max_local']<5 else 'POWERED_ONLY_IF_CALIBRATED',
                calibration_gate='FAILED_TWO_FAMILY_CALIBRATION',physical_verdict='INCONCLUSIVE_SYSTEMATICS'))
    q=next(r for r in json.loads((ROOT/'FISHER_INPUTS.json').read_bytes())['mode_220'] if r['spin']==.68)
    rho_decay=40*math.exp(10*q['omega_imag'])
    norm_result_path=ROOT/'bis/F4_GW250114_WINDOW_POWER_NORM.json'
    paths.extend([norm_result_path,ROOT/'C5_FISHER_v2.json',Path(__file__)])
    result=dict(status='POWER_GATE_RECORDED_AFTER_C6_PRE__NONBLIND',created_utc=datetime.now(timezone.utc).isoformat(),
        bases=bases,readings=table,all_fixed_source_below_5=all(r['fixed_source']['z_max_local']<5 for r in table),
        conventions='Power here means |delta_L|/sigma_comb separation, not detection probability. z uses log(1+x); point-evidence moments from local Gaussian model. All existing data are calibration, not blind test.',
        measured_psd_control=[dict(detector=r['psd'],reading=r['reading'],z_at_measured_rho=math.log1p(r['x'])/r['sigma_delta_local']*rho/40)
            for r in empirical['records'] if r['snr_ringdown']==40 and r['scenario']=='MASS_SPIN_FIXED_OPTIMISTIC'],
        peak_to_window_illustration=dict(assumed_peak_rho=40,rho_after_10tM=rho_decay,
            scope='Exponential 220 envelope only, not independently measured network SNR'),
        source_free_multimode_RB_diagnostic=json.loads((ROOT/'C5_SOURCE_UNCERTAINTY_SUMMARY.json').read_bytes())['primary_B'],
        C5_stop_rule='C5 closes as measured wall; old jobs are diagnostic only and cannot enter this gate. Part B has its own preregistration and stopping rule.',
        maximum_verdict_if_calibrated_but_underpowered=['NOT_FALSIFIED_UNDERPOWERED','EXCLUDED_IN_READING'],
        current_verdict='INCONCLUSIVE_SYSTEMATICS',
        dependencies={str(p.relative_to(ROOT)):sha(p) for p in paths},
        opening_sha256=sha(ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'))
    new(ROOT/'PORTAO_DO_PODER_013.json',result)
    print('rho',rho,'approx_se',rho_se,'all_below5',result['all_fixed_source_below_5'])
    print('gate_sha256',sha(ROOT/'PORTAO_DO_PODER_013.json'))
    print('free_RB_SNR40',[r for r in free if r['reading']=='R-B' and r['snr']==40])

if __name__=='__main__':main()
