"""T05: nonblind archived diagnostics, no registered producer edits or PE."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,time
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.stats import norm
import prediction_reference as scalar
import e7_prediction_reference as vector
D=Path(__file__).resolve().parent;B=D.parents[2];ROOT=B.parent
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for v in iter(lambda:f.read(1024*1024),b''):h.update(v)
    return h.hexdigest()
def load(p):return json.loads(p.read_bytes())
def put(p,x):
    raw=(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode();tmp=p.with_name(p.name+'.pending')
    assert not p.exists()
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;os.link(tmp,p);tmp.unlink()
def quant(x):return np.quantile(x,[.05,.5,.95]).tolist()
def main():
    wall=time.perf_counter();cpu=time.process_time();out=D/'RESULT.json';assert not out.exists()
    reg=load(B/'RINGDOWN_5SIGMA_V1_1.json');sources={};checks=[]
    def source(p,expected=None):
        h=sha(p)
        if expected is not None:assert h==expected,str(p)
        sources[str(p.relative_to(ROOT))]=h;return load(p)
    for name,v in load(D/'COPIES.json').items():assert sha(D/name)==v['sha256']
    grid=source(B/'QNM_GRID.json',reg['input_pins_relative_to_Chatgpt']['ORDEM_013_RINGDOWN/QNM_GRID.json'])
    diag=source(B/'bis/e4_e5_prepare/runs/authorized_001/DETERMINISTIC_DIAGNOSTICS.json')
    plan=source(B/'bis/e4_e5_prepare/PLAN.json',diag['plan_sha256']);cfg=plan['E4']['fisher'];ref=cfg['reference_source']
    qnms={m:CubicSpline(grid['modes'][m]['spins'],np.asarray(grid['modes'][m]['real'])+1j*np.asarray(grid['modes'][m]['imag']),extrapolate=False) for m in ['220','440']}
    bounds={m:(min(grid['modes'][m]['spins']),max(grid['modes'][m]['spins'])) for m in qnms}
    f=np.arange(cfg['f_min_Hz'],cfg['f_max_Hz']+cfg['df_Hz']/2,cfg['df_Hz'])
    psds=source(B/'FISHER_INPUTS.json')['psds'];gram_data={}
    for mode in ['220','440']:
        q=scalar.kerr_mode(ref['mass_detector_Msun'],ref['spin'],mode=(int(mode[0]),int(mode[1]),0),qnm_dimensionless=complex(qnms[mode](ref['spin'])))
        decay=1/q['tau_gr_s'];fr=q['f_gr_hz'];zm=decay+2j*np.pi*(f-fr);zp=decay+2j*np.pi*(f+fr)
        h=.5*(1/zm+1/zp);deriv=[h,.5j*(1/zm-1/zp),.5*(2j*np.pi*fr/zm**2-2j*np.pi*fr/zp**2),.5*decay*(1/zm**2+1/zp**2)]
        for spec in psds:
            p=B/'cache/psd'/spec['filename'];sources[str(p.relative_to(ROOT))]=sha(p);raw=np.loadtxt(p);raw=raw[(raw[:,0]>0)&(raw[:,1]>0)]
            assert raw[0,0]<=f[0] and raw[-1,0]>=f[-1] and np.isfinite(raw[:,:2]).all()
            sn=raw[:,1]**(2 if spec['kind']=='ASD' else 1);curve=np.exp(np.interp(np.log(f),np.log(raw[:,0]),np.log(sn)))
            inner=lambda a,b:float(4*np.trapezoid((a*b.conj()).real/curve,f))
            magnitude=math.sqrt(inner(h,h));der=[v/magnitude for v in deriv];G=np.array([[inner(a,b) for b in der] for a in der])
            for profile,ix in [('FIXED_SOURCE_FREQUENCY',[0,1]),('FREE_FREQUENCY_FIXED_TAU_GR',[0,1,2])]:
                info=float(G[3,3]-G[3,ix]@np.linalg.solve(G[np.ix_(ix,ix)],G[ix,3]));assert info>0
                gram_data[mode,spec['key'],profile]=(info,magnitude)
    max_error=0.
    for row in diag['E4_fisher']:
        if row['snr_route']=='ISOLATED_440_GRID' and row['rho_440_used']==10:
            sig=1/(10*math.sqrt(gram_data['440',row['psd'],row['profile']][0]));err=abs(sig/row['sigma_delta_tau_local_GR']-1);max_error=max(max_error,err)
    assert max_error<1e-12;checks.append(dict(name='440_Fisher_reproduces_archived',passed=True,max_relative_error=max_error))
    anchors={};profile_anchor='FREE_FREQUENCY_FIXED_TAU_GR'
    for mode in ['220','440']:
        prior=next(x for x in diag['E4_archived_marginals']['prior_boundary_diagnostics'][mode] if x['field']=='dtau'+mode)
        lo,mid,hi=prior['quantiles_05_50_95'];sigma=(hi-lo)/(2*norm.ppf(.95))
        sig10=1/(10*math.sqrt(gram_data[mode,'O4',profile_anchor][0]));rho=10*sig10/sigma
        anchors[mode]=dict(rho_effective_H1L1_INPUT=rho,sigma_equivalent=sigma,sigma_Fisher_rho10=sig10,asymmetry=(hi-mid)/(mid-lo),prior_diagnostics=prior,profile=profile_anchor,
            interpretation='OPTIMISTIC_GAUSSIAN_PROXY_FROM_NETWORK_POSTERIOR; single-reference PSD gains transported as INPUT, not actual network mode SNR',N_physical=None)
    rows=[];power=(5+norm.ppf(.9))**2
    for mode in ['220','440']:
        for spec in psds:
            for profile in ['FIXED_SOURCE_FREQUENCY','FREE_FREQUENCY_FIXED_TAU_GR']:
                info,mag=gram_data[mode,spec['key'],profile];gain=mag/gram_data[mode,'O4',profile][1];rho=anchors[mode]['rho_effective_H1L1_INPUT']*gain;sigma=1/(rho*math.sqrt(info))
                for reading in plan['readings']:
                    if reading in ['R-PROP','R-RAIZ-COHERENT']:delta=None
                    else:delta=scalar.prediction(ref['mass_detector_Msun'],ref['spin'],reading,redshift=ref['redshift'],mode=(int(mode[0]),int(mode[1]),0),qnm_dimensionless=complex(qnms[mode](ref['spin'])))['delta_tau']
                    for variant in (['BOTH_220_440_DEFORMED','ONLY_220_DEFORMED'] if mode=='440' else ['BOTH_220_440_DEFORMED']):
                        value=(0. if variant=='ONLY_220_DEFORMED' and delta is not None else delta);z=None if value is None else abs(value)/sigma;resolved=value is not None and abs(value)>=cfg['operational_delta_min'] and z>0
                        rows.append(dict(mode=mode,detector_scenario=spec['key'],profile=profile,reading=reading,variant=variant,rho_proxy_INPUT=rho,sigma_delta_tau=sigma,delta_tau=value,z_expected_proxy=z,N50=25/z**2 if resolved else None,N90=power/z**2 if resolved else None,N_physical=None,
                            status='DERIVED_CONDITIONAL_GAUSSIAN' if resolved else 'OPEN_ZERO_SUBRESOLUTION_OR_NO_EXPONENTIAL',statute=vector.READING_STATUTES[reading],significance=None))
    receipt=source(B/'bis/E7_FINAL_EXECUTION_V1.json');p=B/'cache/POSTERIORES_PSEOB_GWTC5_33_013BIS_V1.json';payload=source(p,receipt['products'][p.name]['sha256']);vector.validate_events(payload['events'])
    paired=[];samples=0
    for e in payload['events']:
        s=e['samples'];spin=np.asarray(s['af']);mask=(spin>=bounds['220'][0])&(spin<=bounds['220'][1]);samples+=len(spin)
        if not mask.all():paired.append(dict(event=e['event_id'],mode='220',status='OPEN_SPIN_OUTSIDE_GRID',uncovered=int((~mask).sum()),N=len(spin)));continue
        q=qnms['220'](spin);assert np.isfinite(q).all()
        for reading in plan['readings']:
            r=vector.prediction_draws(s['Mfdet'],s['af'],s['z'],reading,qnm_dimensionless=q)
            paired.append(dict(event=e['event_id'],mode='220',reading=reading,N=len(spin),spin_range=[float(spin.min()),float(spin.max())],status=r['status'],delta_tau_05_50_95=None if r['delta_tau'] is None else quant(r['delta_tau']),statute=r['statute'],E7_status_changed=False))
        # Independent scalar implementation for three paired rows, all resolved readings.
        for i in [0,len(spin)//2,len(spin)-1]:
            for reading in ['R-A','R-B','R-MOD','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-LIN','R-GLOBAL']:
                a=vector.prediction_draws(s['Mfdet'],s['af'],s['z'],reading,qnm_dimensionless=q)['delta_tau'][i]
                b=scalar.prediction(s['Mfdet'][i],s['af'][i],reading,redshift=s['z'][i],qnm_dimensionless=q[i])['delta_tau'];assert np.isclose(a,b,rtol=2e-12,atol=1e-300),(reading,a,b)
    checks.append(dict(name='paired220_scalar_vector_agree_33events_3rows_8readings',passed=True))
    # 440 uses the archived public calibration posterior only, without modifying E7.
    import h5py
    h5=B/'cache/public/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr/posterior_samples.h5';schema=source(B/'C4_SCHEMA.json');assert sha(h5)==schema['h5_sha256'];sources[str(h5.relative_to(ROOT))]=sha(h5)
    with h5py.File(h5,'r') as h:s=h['pSEOBNRv5PHM/posterior_samples'][()]
    spin=s['final_spin_non_evolved'];q=qnms['440'](spin);covered=np.isfinite(q)
    if not covered.all():paired.append(dict(event='GW250114',mode='440',status='OPEN_SPIN_OUTSIDE_GRID',uncovered=int((~covered).sum()),N=len(spin)))
    else:
        for reading in plan['readings']:
            if reading in ['R-PROP','R-RAIZ-COHERENT']:values=None
            else:values=np.array([scalar.prediction(float(m),float(a),reading,redshift=float(z),mode=(4,4,0),qnm_dimensionless=qq)['delta_tau'] for m,a,z,qq in zip(s['final_mass_non_evolved'],spin,s['redshift'],q)])
            paired.append(dict(event='GW250114',mode='440',reading=reading,N=len(spin),status='OPEN_NO_UNIQUE_EXPONENTIAL' if values is None else 'CONDITIONAL_PAIRED_ENSEMBLE_PREDICTION',delta_tau_05_50_95=None if values is None else quant(values),statute=vector.READING_STATUTES[reading],E7_status_changed=False))
    assert not np.isfinite(qnms['220'](bounds['220'][1]+.01));checks.append(dict(name='outside_grid_not_extrapolated',passed=True))
    joint=source(B/'C4_JOINT_MODES.json',reg['input_pins_relative_to_Chatgpt']['ORDEM_013_RINGDOWN/C4_JOINT_MODES.json'])
    r=dict(status='T05_NONBLIND_DIAGNOSTICS_COMPLETE',at=datetime.now(timezone.utc).isoformat(),anchors=anchors,forecast_rows=rows,paired_predictions=paired,checks=checks,power_numerator=power,total_paired220_draws=samples,
        joint_control=dict(corr_dtau220_dtau440=joint['posterior_correlation_matrix'][1][3],R_B_joint_minus_marginals=next(x['joint_minus_marginal_product'] for x in joint['rows'] if x['reading']=='R-B'),scope='DIAGNOSTIC_ONLY_NOT_FIXED_VS_FREE440_RECOVERY'),
        sources_sha256=sources,script_sha256=sha(Path(__file__)),cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall,heavy_machine_hours=0,
        reading_selected=False,physical_N=None,physical_sigma=None,E7_status_changed=False,registered_producer_changed=False,
        assumptions='Identical independent reference sources, no systematic floor, known unit-variance Gaussian proxy. H1L1 effective anchor transported through single-PSD gains as INPUT; not physical network forecast.')
    put(out,r);print(json.dumps(dict(status=r['status'],anchors={m:a['rho_effective_H1L1_INPUT'] for m,a in anchors.items()},forecast_rows=len(rows),paired_rows=len(paired),paired_draws=samples,cpu_seconds=r['cpu_seconds'],wall_seconds=r['wall_seconds'])))
if __name__=='__main__':main()
