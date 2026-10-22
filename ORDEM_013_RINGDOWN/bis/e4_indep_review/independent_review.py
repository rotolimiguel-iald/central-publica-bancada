"""Prepared independent E4/E5 numerical review. Nothing scientific at import.

Run only with a separately supplied, hashed principal activation after E2 and
the E4/E5 producer result. No MC, PE, waveform generator, network or test data.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import os
import re
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
PRODUCER = BASE / 'bis/e4_e5_prepare'
PACKAGE = ('independent_review.py', 'REVIEW_PLAN.json', 'SOURCE_PINS.json')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()


def load(path):
    def pairs(items):
        out = {}
        for key, value in items:
            require(key not in out, 'Duplicate JSON key')
            out[key] = value
        return out
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def publish(path, value):
    raw = (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n').encode()
    require(len(raw) <= 25*1024*1024, 'Review result unexpectedly large')
    fd, name = tempfile.mkstemp(prefix='.review-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
        require(Path(name).stat().st_size == len(raw), 'Short write')
        os.link(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def gate(args):
    require(args.execute and args.authorization and args.authorization_sha256,
            'AWAITING_PRINCIPAL_ACTIVATION_NO_SCIENCE')
    require(sha(args.authorization) == args.authorization_sha256, 'Activation pin')
    auth = load(args.authorization)
    require(auth.get('status') == 'AUTHORIZED_BY_PRINCIPAL_AFTER_E2', 'Activation status')
    require(auth.get('allowed_task') == 'E4_E5_INDEPENDENT_REVIEW_ONLY', 'Activation scope')
    require(auth.get('new_test_data_allowed') is False, 'No test data permitted')
    require(auth.get('review_package_sha256') == {n:sha(HERE/n) for n in PACKAGE}, 'Review package changed')
    registration = BASE/'RINGDOWN_5SIGMA_V1.json'
    digest = sha(registration)
    require(digest == auth['E2_registration_sha256'], 'E2 pin')
    reg = load(registration)
    gp = BASE/'bis/e2_code/registration_guard.py'
    require(sha(gp) == reg['own_code_tree_sha256']['registration_guard.py'], 'Registered guard pin')
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('_independent_e4_guard', gp)
    guard = importlib.util.module_from_spec(spec); spec.loader.exec_module(guard)
    checked, actual = guard.checked_registration()
    require(actual == digest and checked == reg, 'Complete registered context differs')
    require(guard.utc(auth['registered_utc']) >= guard.utc(reg['registered_utc']), 'Activation predates E2')
    pins = load(HERE/'SOURCE_PINS.json')
    for relative, value in pins['files'].items():
        p = (BASE/relative).resolve()
        require(p.is_relative_to(BASE.resolve()) and sha(p) == value['sha256'], 'Review source changed: '+relative)
    package = {n:sha(PRODUCER/n) for n in ('PLAN.json','INPUT_MANIFEST.json','SCHEMA.json','deterministic_e4_e5.py')}
    require(reg['e4_e5_preparation_pins'] == package, 'Producer package not registered')
    result_path = Path(auth['producer_result_path']).resolve()
    receipt_path = Path(auth['producer_receipt_path']).resolve()
    require(result_path.is_relative_to((PRODUCER/'runs').resolve()) and receipt_path.parent == result_path.parent,
            'Producer result outside own runs')
    require(sha(result_path) == auth['producer_result_sha256'] and sha(receipt_path) == auth['producer_receipt_sha256'],
            'Producer result/receipt pin')
    receipt = load(receipt_path); result = load(result_path)
    require(receipt['status'] == 'COMPLETED_DETERMINISTIC_ARCHIVED_DIAGNOSTICS' and
            receipt['result_sha256'] == sha(result_path) and receipt['executor_sha256'] == package['deterministic_e4_e5.py'],
            'Producer completion receipt differs')
    require(result['status'] == 'NONBLIND_CONDITIONAL_DETERMINISTIC_DIAGNOSTICS' and
            result['E2_registration_sha256'] == digest and result['plan_sha256'] == package['PLAN.json'] and
            result['input_manifest_sha256'] == package['INPUT_MANIFEST.json'], 'Result identity')
    manifest = load(PRODUCER/'INPUT_MANIFEST.json')
    for item in manifest['files']:
        p = (BASE/item['path']).resolve()
        require(p.is_relative_to(BASE.parent.resolve()) and p.stat().st_size == item['bytes'] and sha(p) == item['sha256'],
                'Producer input pin: '+item['path'])
    require(re.fullmatch('[a-z][a-z0-9_]{0,47}', auth['run_id']) is not None, 'Run id')
    target = HERE/'runs'/auth['run_id']
    require(target.resolve().is_relative_to(HERE.resolve()) and not target.exists(), 'Output already exists/escapes')
    return auth, guard, reg, load(PRODUCER/'PLAN.json'), manifest, result, target


def predictions(mass, spin, z, q, reading, mode):
    """Independent dimensionless x=Gamma*tau algebra; no source prediction call."""
    import numpy as np
    t = np.asarray(mass)*1.3271244e20/299792458.**3
    tp = math.sqrt((6.62607015e-34/(2*math.pi))*6.67430e-11/299792458.**5)
    b = 7.2973525693e-3*math.sqrt(math.e)
    u, v = np.real(q), -np.imag(q)
    require(np.all(u>0) and np.all(v>0), 'Damped QNM domain')
    if reading == 'R-GLOBAL': return np.zeros_like(t)
    if reading == 'R-A': x=b*(1+np.asarray(z))*tp*u*u/(2*t*v)
    elif reading == 'R-B': x=b*u*u/(2*v)
    elif reading == 'R-RAIZ-0': x=b*u/(2*v)
    elif reading == 'R-LIN': x=b*u/v
    elif reading == 'R-MOD':
        r=np.sqrt(1-np.asarray(spin)**2); gap=u-mode*np.asarray(spin)/(2*(1+r))
        require(np.all(gap>0), 'Positive restricted corotating gap')
        x=2*math.pi*b*(1+r)*gap*gap/(r*v)
    elif reading in ('R-RAIZ-EP4','R-RAIZ-REST'):
        w=u/t
        w0=1/(4*tp*(1+np.asarray(z))) if reading=='R-RAIZ-EP4' else t/(tp**2*(1+np.asarray(z))**2)
        x=b*w*w*t/(2*v*(np.sqrt(w0+w)+np.sqrt(w0))**2)
    else: raise ValueError('Reading needs OPEN, not a scalar exponential')
    return -x/(1+x)


def fisher_review(plan, result, qnms, add, check):
    import numpy as np
    cfg=plan['E4']['fisher']; ref=cfg['reference_source']
    q=complex(qnms['440'](ref['spin'])); t=ref['mass_detector_Msun']*1.3271244e20/299792458.**3
    fr=q.real/(2*math.pi*t); tau=t/(-q.imag)
    f=np.arange(cfg['f_min_Hz'],cfg['f_max_Hz']+cfg['df_Hz']/2,cfg['df_Hz'])
    def transfer(theta):
        amp,phase,df,dt=theta; decay=1/(tau*(1+dt)); freq=fr*(1+df)
        return np.exp(amp)/2*(np.exp(1j*phase)/(decay+2j*math.pi*(f-freq))+
                             np.exp(-1j*phase)/(decay+2j*math.pi*(f+freq)))
    h=transfer(np.zeros(4)); d=1/tau
    zm=d+2j*math.pi*(f-fr);zp=d+2j*math.pi*(f+fr)
    analytic=[h,.5j*(1/zm-1/zp),1j*math.pi*fr*(1/zm**2-1/zp**2),.5*d*(1/zm**2+1/zp**2)]
    for axis in range(4):
        steps=[]
        for eps in (3e-5,1e-5):
            theta=np.zeros(4);theta[axis]=eps
            fd=(transfer(theta)-transfer(-theta))/(2*eps)
            steps.append(float(np.linalg.norm(fd-analytic[axis])/np.linalg.norm(analytic[axis])))
        check('derivative_finite_difference_'+str(axis),max(steps)<1e-5,dict(relative_errors=steps))
    # Weighted real/imaginary least squares is independent of the Schur code.
    trap=np.empty(len(f));trap[0]=(f[1]-f[0])/2;trap[-1]=(f[-1]-f[-2])/2;trap[1:-1]=(f[2:]-f[:-2])/2
    configs={}
    for psd in load(BASE/'FISHER_INPUTS.json')['psds']:
        raw=np.loadtxt(BASE/'cache/psd'/psd['filename']);raw=raw[(raw[:,0]>0)&(raw[:,1]>0)]
        require(np.all(np.diff(raw[:,0])>0) and raw[0,0]<=f[0] and raw[-1,0]>=f[-1], 'PSD support')
        require(psd['kind'] in ('ASD','PSD'),'PSD kind')
        sn=raw[:,1]**(2 if psd['kind']=='ASD' else 1)
        curve=np.exp(np.interp(np.log(f),np.log(raw[:,0]),np.log(sn)))
        weights=4*trap/curve;norm=float(np.sqrt(np.sum(weights*abs(h)**2)))
        vectors=np.column_stack([a/norm for a in analytic])*np.sqrt(weights[:,None])
        design=np.vstack((vectors.real,vectors.imag));gram=design.T@design
        information={}
        for profile,count in (('FIXED_SOURCE_FREQUENCY',2),('FREE_FREQUENCY_FIXED_TAU_GR',3)):
            nuisance=design[:,:count];target=design[:,3]
            residual=target-nuisance@np.linalg.lstsq(nuisance,target,rcond=None)[0]
            info=float(residual@residual)
            schur=float(gram[3,3]-gram[3,:count]@np.linalg.solve(gram[:count,:count],gram[:count,3]))
            add('projection_vs_Schur_'+psd['key']+'_'+profile,info,schur)
            information[profile]=info
        configs[psd['key']]=(norm,information)
    expected=set(itertools.product(plan['readings'],plan['variants'],configs,
        cfg['profiles'],cfg['snr_routes'],cfg['isolated_440_snr_grid']))
    observed=[];errors=[]
    for row in result['E4_fisher']:
        route=row['snr_route'];anchor=row['rho_440_O4_anchor_INPUT'] if route=='AMPLITUDE_FIXA_INPUT' else row['rho_440_equal_per_PSD_INPUT']
        key=(row['reading'],row['variant'],row['psd'],row['profile'],route,anchor);observed.append(key)
        require(key in expected,'Unexpected forecast row')
        norm,infos=configs[row['psd']];gain=norm/configs['O4'][0];rho=anchor*(gain if route=='AMPLITUDE_FIXA_INPUT' else 1)
        sigma=1/(rho*math.sqrt(infos[row['profile']]))
        values={'reference_mode_norm':norm,'rho_gain_at_fixed_amplitude_vs_O4':gain,'rho_440_used':rho,
                'sigma_delta_tau_local_GR':sigma}
        if route=='AMPLITUDE_FIXA_INPUT':values['common_Fourier_amplitude_INPUT']=anchor/configs['O4'][0]
        if row['reading'] in ('R-PROP','R-RAIZ-COHERENT'):
            require(row['delta_tau_440'] is None and row['N90_conditional'] is None,'OPEN prediction promoted')
        else:
            delta=0. if row['variant']=='ONLY_220_DEFORMED' else float(predictions(ref['mass_detector_Msun'],ref['spin'],ref['redshift'],q,row['reading'],4))
            z=abs(delta)/sigma;values.update(delta_tau_440=delta,expected_local_z=z,log_coordinate_z_sensitivity_only=abs(math.log1p(delta))/sigma)
            resolved=abs(delta)>=cfg['operational_delta_min'] and z>0
            if resolved:values.update(N_expected_local_z5_proxy=25/z**2,N90_conditional=(5+cfg['normal_90_quantile'])**2/z**2)
            else:require(row['N90_conditional'] is None and row['N_expected_local_z5_proxy'] is None,'Unresolved count promoted')
        for field,want in values.items():
            if not np.isclose(row[field],want,rtol=2e-8,atol=0):errors.append(dict(key=key,field=field,actual=row[field],expected=want))
        require(row['calibrated_significance'] is None,'Physical significance promoted')
    check('forecast_unique_complete_cartesian_matrix',len(observed)==len(expected) and set(observed)==expected,
          dict(actual=len(observed),expected=len(expected)))
    check('forecast_formulas_PSD_gain_N50_N90',not errors,dict(mismatches=errors[:12],total=len(errors)))


def gaussian_zero(data):
    import numpy as np
    mean=data.mean(axis=1);centered=data-mean[:,None];cov=centered@centered.T/(data.shape[1]-1)
    sign,ld=np.linalg.slogdet(cov);require(sign>0,'Gaussian covariance')
    return float(-len(mean)*math.log(2*math.pi)/2-ld/2-mean@np.linalg.solve(cov,mean)/2)


def direct_kde_zero(data,multiplier):
    """Direct full mixture, no scipy.stats.gaussian_kde call or bandwidth fit."""
    import numpy as np
    n=data.shape[1];mean=data.mean(axis=1);centered=data-mean[:,None]
    cov=(centered@centered.T)/(n-1)*(n**(-1/(data.shape[0]+4))*multiplier)**2
    sign,ld=np.linalg.slogdet(cov);require(sign>0,'KDE covariance')
    exponents=-.5*np.sum(data*np.linalg.solve(cov,data),axis=0)
    top=float(exponents.max());weight=np.exp(exponents-top)
    value=top+math.log(float(weight.mean()))-data.shape[0]*math.log(2*math.pi)/2-ld/2
    return value,float(weight.sum()**2/(weight@weight))


def density_review(plan,result,qnms,add,check):
    import numpy as np
    import h5py
    cfg=plan['E4']['posterior'];path=BASE/cfg['path']
    require(sha(path)==cfg['sha256'],'Archived source hash')
    fields=['domega220','dtau220','domega440','dtau440','final_mass_non_evolved','final_spin_non_evolved','redshift']
    with h5py.File(path,'r') as h:
        name=cfg['label']+'/posterior_samples';prefix=''
        for part in name.split('/'):
            prefix+='/'+part;require(isinstance(h.get(prefix,getlink=True),h5py.HardLink),'External posterior link')
        ds=h[name];require(isinstance(ds,h5py.Dataset) and not ds.is_virtual and not ds.external,'Unpinned storage')
        samples=ds.fields(fields)[()]
    require(len(samples)==cfg['N'] and all(np.isfinite(samples[k]).all() for k in fields),'Full paired samples')
    spin=samples['final_spin_non_evolved'];require(np.all((spin>=0)&(spin<.98)),'QNM domain')
    rows=result['E4_archived_marginals']['rows'];keys=[(r['mode'],r['reading']) for r in rows]
    check('archived_20_rows_unique_complete',len(keys)==20 and set(keys)==set(itertools.product(('220','440'),plan['readings'])),len(keys))
    check('archived_no_joint_BF',result['E4_archived_marginals']['joint_220_440_lnB'] is None and all(r['lnB'] is None for r in rows),'No product of marginal densities')
    bykey=dict(zip(keys,rows));comparisons=0
    for mode,reading in itertools.product(('220','440'),('R-B','R-MOD','R-RAIZ-0','R-LIN')):
        data=np.vstack((samples['domega'+mode],samples['dtau'+mode]))
        shift=predictions(samples['final_mass_non_evolved'],spin,samples['redshift'],qnms[mode](spin),reading,int(mode[1]))
        residual=data.copy();residual[1]-=shift;row=bykey[(mode,reading)]
        estimators=row['estimators'];scores=[]
        for mult in cfg['bandwidth_multipliers']:
            zero,ess0=direct_kde_zero(data,mult);curve,ess1=direct_kde_zero(residual,mult);score=curve-zero;scores.append(score)
            item=next(e for e in estimators if e.get('bandwidth_multiplier')==mult)
            label=mode+'_'+reading+'_'+str(mult)
            add('KDE_direct_'+label,item['log_density_ratio_diagnostic'],score)
            add('KDE_null_ESS_'+label,item['null_support']['kernel_effective_samples'],ess0)
            add('KDE_curve_ESS_'+label,item['curve_support']['kernel_effective_samples'],ess1)
        score=gaussian_zero(residual)-gaussian_zero(data);scores.append(score)
        item=next(e for e in estimators if e['method']=='INDEPENDENT_FULL_MOMENT_GAUSSIAN2D_NO_KDE_BANDWIDTH')
        add('Gaussian_full_moments_'+mode+'_'+reading,item['log_density_ratio_diagnostic'],score)
        add('Estimator_range_'+mode+'_'+reading,row['estimator_range'],[min(scores),max(scores)])
        add('Paired_shift_quantiles_'+mode+'_'+reading,row['predicted_shift_quantiles_05_50_95'],np.quantile(shift,[.05,.5,.95]))
        comparisons+=1
    check('eight_predefined_density_comparisons',comparisons==8,comparisons)
    require(sha(path)==cfg['sha256'],'Archived source changed while reading')


def information_review(plan,result,add,check):
    source=load(BASE/'bis/e0_core/DATASET.json');byid={r['product_id']:r for r in source['rows']}
    anchor=byid['GWTC5:GW250114_082203']['stats']['df']['std_ddof1'];reference=.5/anchor**4
    rows=result['E5_information'];check('IV_population_coverage',len(rows)==4 and {r['population'] for r in rows}==set(plan['E5']['archived_information_populations']),len(rows))
    for row in rows:
        ids=source['sets'][row['population']];got=row['rows']
        check('IV_no_width_selection_'+row['population'],[r['product_id'] for r in got]==ids and len(ids)==len(set(ids)),len(ids))
        raw=[.5/byid[k]['stats']['df']['std_ddof1']**4 for k in ids];total=sum(raw)
        add('IV_equivalent_'+row['population'],row['N_GW250114_equivalent'],total/reference)
        for r,info in zip(got,raw):
            add('IV_relative_'+r['product_id'],r['relative_information_to_GW250114'],info/reference)
            add('IV_fraction_'+r['product_id'],r['information_fraction'],info/total)
        check('IV_unpaid_systematics_'+row['population'],row['sigma_sys'] is None and row['jitter_transfer'] is None,'Gaussian sigma_sys=0 weight proxy only')


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--execute',action='store_true')
    ap.add_argument('--authorization',type=Path);ap.add_argument('--authorization-sha256')
    args=ap.parse_args();start=time.perf_counter()
    auth,guard,reg,plan,manifest,result,target=gate(args)
    # Scientific imports and all numerical work stay below the activation gate.
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
    import numpy as np
    from scipy.interpolate import CubicSpline
    checks=[]
    def check(name,passed,detail):checks.append(dict(name=name,passed=bool(passed),detail=detail))
    def add(name,got,want):
        a,b=np.asarray(got,float),np.asarray(want,float)
        check(name,a.shape==b.shape and np.allclose(a,b,rtol=2e-8,atol=2e-10),
              dict(actual=a.tolist(),expected=b.tolist()))
    grid=load(BASE/'QNM_GRID.json');qnms={m:CubicSpline(grid['spins'],np.asarray(grid['modes'][m]['real'])+1j*np.asarray(grid['modes'][m]['imag']),extrapolate=False) for m in ('220','440')}
    for label,fn in (('fisher',fisher_review),('density',density_review),('information',information_review)):
        guard.time_guard(reg)
        try:
            if label=='information':fn(plan,result,add,check)
            else:fn(plan,result,qnms,add,check)
        except Exception as exc:check(label+'_exception',False,dict(type=type(exc).__name__,message=str(exc)))
    for item in manifest['files']:require(sha(BASE/item['path'])==item['sha256'],'Input changed during review')
    guard.time_guard(reg)
    require(sha(auth['producer_result_path'])==auth['producer_result_sha256'],'Producer result changed')
    target.mkdir(parents=True,exist_ok=False)
    value=dict(status='PASS_CONDITIONAL_ARITHMETIC_ONLY' if all(c['passed'] for c in checks) else 'REQUEST_CHANGES',
        producer_result_sha256=auth['producer_result_sha256'],authorization_sha256=sha(args.authorization),
        review_sha256=sha(Path(__file__)),checks=checks,passed=sum(c['passed'] for c in checks),
        failed=sum(not c['passed'] for c in checks),wall_seconds=time.perf_counter()-start,
        lnB=None,z_physical=None,new_PE=False,new_MC=False,new_waveforms=False,new_test_data=False,
        limitations=['Conditional arithmetic, not physical calibration','Shared pinned QNM interpolant and reference PSDs',
                    'Eight predeclared density pairs, no estimator selection','No nuisance normalization/selection or sigma_jit transfer'])
    publish(target/'INDEPENDENT_REVIEW.json',value)
    print(json.dumps(dict(path=str(target),sha256=sha(target/'INDEPENDENT_REVIEW.json'),status=value['status'])))


if __name__=='__main__':main()
