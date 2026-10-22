"""Light F4 audit: norms, reference Fisher, scalar quadrature; no PE or injection.

Run with /opt/lal_env Python if h5py/scipy are unavailable in bundled Python.
No production module is imported. Writes only this review directory.
"""
from pathlib import Path
from datetime import datetime,timezone
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
import hashlib,json,math,sys
import numpy as np
import h5py
from scipy.integrate import quad
from scipy.special import log_ndtr

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def load(p):return json.loads((ROOT/p).read_bytes())
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(2**20),b''):h.update(chunk)
    return h.hexdigest()
def require(c,msg):
    if not c:raise RuntimeError(msg)
def relative(a,b):return abs(a-b)/abs(b) if b else abs(a-b)

def log_interval(lo,hi):
    if lo>0:lo,hi=-hi,-lo
    top=float(log_ndtr(hi));bottom=float(log_ndtr(lo))
    return top+math.log(-math.expm1(bottom-top))

def closed_log_evidence(y,x,sigma):
    # t=log(1+a*x)/sigma, da=sigma*exp(sigma*t)/x dt.
    upper=math.log1p(x)/sigma;center=y+sigma
    return math.log(sigma/x)+.5*center*center+.5*math.log(2*math.pi)+log_interval(-center,upper-center)

def moments(x,sigma,truth):
    center=math.log1p(truth*x)/sigma
    density=lambda e:math.exp(-e*e/2)/math.sqrt(2*math.pi)
    f=lambda e:closed_log_evidence(center+e,x,sigma)
    mean,err=quad(lambda e:f(e)*density(e),-12,12,epsabs=3e-11,epsrel=3e-12)
    variance,err2=quad(lambda e:(f(e)-mean)**2*density(e),-12,12,epsabs=3e-11,epsrel=3e-12)
    return dict(mean_lnB=mean,sd_lnB=math.sqrt(variance),integration_error=max(err,err2),noise_free_lnB=f(0))

def reference_information(qreal,qimag,psdfile,kind):
    # Finite five-point derivative of analytic causal cosine FT; weighted QR
    # projects nuisances, independently of production's analytic Schur formula.
    f=np.arange(20,2048.00001,.125);raw=np.loadtxt(psdfile)
    valid=(raw[:,0]>0)&(raw[:,1]>0)&np.isfinite(raw[:,1]);raw=raw[valid]
    curve=np.exp(np.interp(np.log(f),np.log(raw[:,0]),np.log(raw[:,1])))
    if kind=='ASD':curve=curve**2
    weights=.5/curve;weights[[0,-1]]*=.5
    tm=68.1*1.3271244e20/299792458**3
    fr=qreal/(2*math.pi*tm);decay=-qimag/tm
    def waveform(logamp,phase,logfr,logdecay):
        freq=fr*math.exp(logfr);d=decay*math.exp(logdecay)
        return math.exp(logamp)/2*(np.exp(1j*phase)/(d+2j*np.pi*(f-freq))+np.exp(-1j*phase)/(d+2j*np.pi*(f+freq)))
    base=waveform(0,0,0,0);norm=np.sqrt(np.sum(weights*abs(base)**2))
    step=1e-4;columns=[]
    for k in range(4):
        values=[]
        for t in (-2,-1,1,2):
            args=[0.,0.,0.,0.];args[k]=t*step;values.append(waveform(*args))
        deriv=(values[0]-8*values[1]+8*values[2]-values[3])/(12*step*norm)
        columns.append(np.concatenate([np.sqrt(weights)*deriv.real,np.sqrt(weights)*deriv.imag]))
    rows=[]
    for k in (2,3):
        Q,_=np.linalg.qr(np.column_stack(columns[:k]),mode='reduced')
        residual=columns[3]-Q@(Q.T@columns[3]);rows.append(float(residual@residual))
    return dict(fixed_information=rows[0],frequency_free_information=rows[1],raw_norm=float(norm))

def main():
    out=HERE/'f4_independent_results.json';require(not out.exists(),'Output exists')
    gate=load('PORTAO_DO_PODER_013.json');fisher=load('C5_FISHER_v2.json');old=load('C5_FISHER.json')
    registry=load('REGISTRO_C6.json');normsaved=load('bis/F4_GW250114_WINDOW_POWER_NORM.json');inputs=load('FISHER_INPUTS.json')
    extra=['PORTAO_DO_PODER_013.json','refeito/measure_power_gate_013bis.py','fisher_forecast.py']+['cache/psd/'+x['filename'] for x in inputs['psds']]
    before={p:sha(ROOT/p) for p in set(gate['dependencies'])|set(extra)}
    integrity={p:before[p]==h for p,h in gate['dependencies'].items()}
    require(all(integrity.values()),'Stale gate dependency')
    require(fisher['supersedes_sha256']==sha(ROOT/'C5_FISHER.json'),'Fisher origin differs')
    norms=[]
    downloads=load('C6_DOWNLOADS.json')
    for detector in ('H1','L1'):
        receipt=next(r for r in downloads['files'] if r['detector']==detector)
        filename=receipt['path'].replace('\\','/').split('/')[-1]
        p=ROOT/'cache/gwosc/on_source'/filename
        with np.load(ROOT/f'cache/empirical_noise/{detector}_noise.npz') as data:W=data['whitener_scaled'].copy()
        with h5py.File(p,'r') as h:
            gps=float(h['meta/GPSstart'][()]);series=h['strain/Strain'];spacing=float(series.attrs['Xspacing'])
            offset=(registry['reference_peak_GPS'][detector]-gps)+10*registry['reference_tM_seconds']
            first=math.ceil(offset/spacing)
            y=np.asarray(series[first:first+2*registry['interval_samples']:2],dtype=float)*1e21
        # Independent summation over whitened coefficients.
        white=np.einsum('ij,j->i',W,y);power=math.fsum(float(v)*float(v) for v in white)
        ref=next(r for r in normsaved['detectors'] if r['detector']==detector)
        norms.append(dict(detector=detector,first_index=first,stored_first_index=ref['first_index'],dof=W.shape[0],
            measured_norm=power,stored_norm=ref['norm_squared'],relative_error=relative(power,ref['norm_squared'])))
        require(first==ref['first_index'],'GPS rounding changes the selected sample')
    excess=sum(r['measured_norm']-r['dof'] for r in norms);rho=math.sqrt(excess);dof=sum(r['dof'] for r in norms)
    rho_se=math.sqrt(2*dof+4*excess)/(2*rho)
    readings={r['reading'] for r in load('C1_LEITURAS_v4.json')['rows']}
    groups={}
    for row in gate['readings']:
        key=(row['base'],row['psd'],row['family']);groups.setdefault(key,[]).append(row['reading'])
    require(len(groups)==5 and all(len(rs)==10 and set(rs)==readings for rs in groups.values()),'Missing or duplicate gate reading')
    q=next(q for q in inputs['mode_220'] if q['spin']==.68)
    wr=1.5251-1.1568*(1-.68)**.1292;qual=.7+1.4187*(1-.68)**(-.499)
    information={}
    for curve in inputs['psds']:
        require(sha(ROOT/'cache/psd'/curve['filename'])==curve['sha256'],'PSD hash mismatch')
        for kind,real,imag in [('BCW',wr,-wr/(2*qual)),('QNM',q['omega_real'],q['omega_imag'])]:
            information[curve['key'],kind]=reference_information(real,imag,ROOT/'cache/psd'/curve['filename'],curve['kind'])
    errors=[]
    for row in fisher['records']:
        x,sigma=row['x'],row['sigma_delta_local'];z=math.log1p(x)/sigma
        info=information[row['psd'],'QNM' if row['reading']=='R-MOD' else 'BCW']
        which='fixed_information' if row['scenario']=='MASS_SPIN_FIXED_OPTIMISTIC' else 'frequency_free_information'
        independent_sigma=1/(row['snr_ringdown']*math.sqrt(info[which]))
        errors.append(dict(psd=row['psd'],reading=row['reading'],snr=row['snr_ringdown'],scenario=row['scenario'],
            independent_sigma_relative_error=relative(independent_sigma,sigma),z_error=relative(z,row['z_logdecay']),
            delta_error=relative(-x/(1+x),row['delta_exact']),point_mean_error=relative(z*z/2,row['lnB_point_mean_if_reading']),
            point_sd_error=relative(z,row['lnB_point_standard_deviation'])))
        if abs(row['delta_exact'])<1e-6:require(row['identical_independent_events_for_median_5sigma']=='SUBRESOLUTION','N threshold differs')
        else:require(row['identical_independent_events_for_median_5sigma']==math.ceil(25/z**2),'N differs')
    base_errors=[];recovery=load('C5_IMR_RECOVERY.json')['results']
    for base in gate['bases']:
        if base['name']=='REFERENCE_INJECTION_403Mpc':
            matches=[r for r in recovery if r['psd']==base['psd'] and r['injection_family']==base['family']]
            zero=[r['reference_SNR_403Mpc'] for r in matches if r['injected_a']==0]
            require(max(zero)-min(zero)<1e-12,'a=0 SNR inconsistent')
            require(relative(base['rho'],zero[0])<1e-14,'a=0 base mismatch')
            for name,value in base['rho_a1_by_reading'].items():
                ones=[r['reference_SNR_403Mpc'] for r in matches if r['injected_a']==1 and r['reading']==name]
                require(max(ones)-min(ones)<1e-12 and relative(value,ones[0])<1e-14,'a=1 reference mismatch')
        else:require(relative(base['rho'],rho)<1e-8,'Norm-derived network rho differs')
        base_errors.append(dict(base=base['name'],psd=base['psd'],family=base['family'],rho=base['rho'],
            scale_error=relative(base['scale_from_SNR40'],base['rho']/40)))
    gate_errors=[]
    for row in gate['readings']:
        if row['reading'] in ('R-PROP','R-RAIZ-COHERENT'):continue
        point=next(p for p in fisher['records'] if p['reading']==row['reading'] and p['psd']==row['psd'] and p['snr_ringdown']==40 and p['scenario']=='MASS_SPIN_FIXED_OPTIMISTIC')
        z=math.log1p(point['x'])/point['sigma_delta_local']*row['rho']/40
        err=relative(z,row['fixed_source']['z_max_local'])
        alternate=None
        if row['rho_a1_same_distance'] is not None:alternate=relative(z*row['rho_a1_same_distance']/row['rho'],row['z_at_a1_same_distance'])
        gate_errors.append(dict(reading=row['reading'],base=row['base'],psd=row['psd'],family=row['family'],z=z,relative_error=err,a1_relative_error=alternate))
        require(row['unknown_source_single_220']['z_max_local']==0 and row['unknown_source_single_220']['sigma_effective_delta_tau'] is None,'Degeneracy field differs')
    free=[]
    for row in fisher['free_parameter_scalar_gaussian']:
        record=next(p for p in fisher['records'] if p['reading']==row['reading'] and p['psd']=='O4' and p['snr_ringdown']==row['snr'] and p['scenario']=='MASS_SPIN_FIXED_OPTIMISTIC')
        computed=moments(record['x'],record['sigma_delta_local'],row['injected_a'])
        free.append(dict(reading=row['reading'],snr=row['snr'],injected_a=row['injected_a'],**computed,
            mean_absolute_error=abs(computed['mean_lnB']-row['mean_lnB']),sd_absolute_error=abs(computed['sd_lnB']-row['sd_lnB'])))
    rb40=next(p for p in fisher['records'] if p['reading']=='R-B' and p['psd']=='O4' and p['snr_ringdown']==40 and p['scenario']=='MASS_SPIN_FIXED_OPTIMISTIC')
    comparison=dict(fisher_sigma=rb40['sigma_delta_local'],using_fisher=moments(rb40['x'],rb40['sigma_delta_local'],1),
        using_sigma_0p058=moments(rb40['x'],.058,1),explanation='Order 013 section 1.4 quoted sigma near 0.058; reference Fisher sigma is near 0.04974.')
    # Single-220 identifiability: map from (log M, chi) to (log f, log tau).
    a=.68;wprime=1.1568*.1292*(1-a)**(.1292-1);Qprime=1.4187*.499*(1-a)**(-.499-1)
    J=np.array([[-1,wprime/wr],[1,Qprime/qual-wprime/wr]])
    tangent=np.array([0.,-1.]);coeff=np.linalg.solve(J,tangent)
    degeneracy=dict(jacobian=J.tolist(),determinant=float(np.linalg.det(J)),minus_Qprime_over_Q=-Qprime/qual,
        deformation_representation=coeff.tolist(),residual=float(np.linalg.norm(J@coeff-tangent)),
        scope='Local single-220 with free mass/spin/amplitude; not a full-IMR or resolved-multimode theorem')
    stale=[]
    for row in fisher['same_source_R_B']:
        point=next(p for p in fisher['records'] if p['psd']==row['psd'] and p['reading']=='R-B' and p['snr_ringdown']==40 and p['scenario']=='FREQUENCY_FREE_TAU_GR_FIXED')
        corrected=point['z_logdecay']*row['snr_ratio_to_O4']
        stale.append(dict(psd=row['psd'],stored_z=row['z_local'],corrected_log_z=corrected,
            relative_change=corrected/row['z_local']-1,stored_mean=row['lnB_mean_if_reading'],corrected_mean=corrected**2/2))
    original_builder=(ROOT/'refeito/measure_power_gate_013bis.py').read_text(encoding='utf-8')
    new_builder=(ROOT/'refeito/measure_power_gate_013bis_v2.py').read_text(encoding='utf-8')
    initial_prefix=original_builder[original_builder.index('    norms=[]'):original_builder.index('    bases=[]')]
    new_prefix=new_builder[new_builder.index('    norms=[]'):new_builder.index('    bases=[]')]
    partial_comparison=dict(norm_and_fisher_computation_source_identical=initial_prefix==new_prefix,
       writer_checks_parsed_json_equality="if json.loads(p.read_bytes())!=d:" in new_builder,
       explanation='Code verifies semantic JSON equality before reusing first-attempt norm/Fisher outputs; past execution not inferred from code alone.')
    after={p:sha(ROOT/p) for p in before};require(before==after,'Inputs changed')
    result=dict(utc=datetime.now(timezone.utc).isoformat(),status='F4_NUMERICAL_AUDIT_COMPLETE__INTERPRETATION_LIMITS_REMAIN',
        python=sys.version,script_sha256=sha(Path(__file__)),input_hashes=before,dependency_matches=integrity,inputs_unchanged=True,
        norms=norms,network_rho=rho,network_rho_se=rho_se,independent_noise_dof=dof,
        coverage=dict(bases=len(groups),gate_rows=len(gate['readings']),fisher_rows=len(fisher['records']),free_rows=len(free),all_ten_each_base=True),
        fisher_checks=errors,fisher_max_sigma_relative_error=max(x['independent_sigma_relative_error'] for x in errors),
        transport=gate_errors,bases=base_errors,max_fixed_z=max(r['fixed_source']['z_max_local'] for r in gate['readings']),
        free_quadrature=free,free_max_mean_error=max(r['mean_absolute_error'] for r in free),free_max_sd_error=max(r['sd_absolute_error'] for r in free),
        comparison_to_0p05=comparison,degeneracy=degeneracy,same_source_stale=stale,partial_output_check=partial_comparison,
        limitations=['Reference-shape SNR transport is conditional, not a rigorous upper bound for all IMR signals.',
                    'Whitened excess assumes stationary Gaussian unit covariance; SNR is not a matched-filter detection.',
                    'Free-amplitude integral is exact within the scalar Gaussian model, not a new astrophysical likelihood.',
                    'No new PE or injections; existing source-free multimode and calibration records not reexecuted.'])
    raw=(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8');tmp=out.with_name(out.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    require(tmp.read_bytes()==raw,'Write differs');require(not out.exists(),'Output appeared');tmp.rename(out)
    print(json.dumps({k:result[k] for k in ('status','network_rho','network_rho_se','coverage','fisher_max_sigma_relative_error','max_fixed_z','free_max_mean_error','free_max_sd_error','comparison_to_0p05','same_source_stale','partial_output_check','inputs_unchanged')},indent=2))
    print('SHA256',sha(out))
if __name__=='__main__':main()
