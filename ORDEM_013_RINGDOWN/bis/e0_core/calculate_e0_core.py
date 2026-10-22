"""E0 scalar calibration from pinned existing HDF5; one process/thread, no PE."""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[key] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import time
import platform
import numpy as np
import scipy
from scipy.interpolate import CubicSpline
from scipy.stats import norm
import h5py

OUT = Path(__file__).resolve().parent
B = OUT.parents[1]
R = B.parent
A = R/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao'
START = datetime.now(timezone.utc)
WALL = time.perf_counter()
CPU = time.process_time()
SOURCES = {}
READINGS = ['R-A','R-B','R-MOD','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-RAIZ-COHERENT','R-LIN','R-GLOBAL','R-PROP']
FACTOR = float((5+norm.ppf(.9))**2/25)
Q90 = float(norm.ppf(.95))


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4*1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def read_json(path):
    raw = path.read_bytes()
    SOURCES[str(path.relative_to(R))] = {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw), 'mode':'JSON_READ'}
    return json.loads(raw)


def write_new(name, obj):
    path = OUT/name
    if path.exists():
        raise FileExistsError(path)
    raw = (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode()
    if len(raw) > 25*1024*1024:
        raise RuntimeError('Large result requires separately authorized first-level cache')
    temp = path.with_suffix(path.suffix+'.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    if temp.read_bytes() != raw:
        raise IOError('Temporary bytes mismatch')
    try:
        os.link(temp, path)
    finally:
        temp.unlink()


def stats(values):
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or len(x) < 2 or not np.all(np.isfinite(x)):
        raise ValueError('Invalid finite posterior column')
    q = np.quantile(x, [.05,.16,.5,.84,.95])
    return {'N':len(x), 'mean':float(np.mean(x)), 'median':float(q[2]),
            'std_ddof1':float(np.std(x,ddof=1)), 'quantiles_05_16_50_84_95':q.tolist(),
            'sigma_q90':float((q[4]-q[0])/(2*Q90)),
            'sigma_q68':float((q[3]-q[1])/2), 'min':float(x.min()), 'max':float(x.max())}


def predictions(mass, spin, redshift, module, interp):
    exact = complex(interp(spin))
    if not np.isfinite(exact):
        raise ValueError('Median spin outside pinned QNM grid')
    result = {}
    for reading in READINGS:
        if reading in ('R-RAIZ-COHERENT','R-PROP'):
            result[reading] = {'status':'OPEN_NO_UNIQUE_LOCAL_EXPONENTIAL_DTAU', 'delta_tau':None,
                'reason':'occupation and fitting window required' if reading=='R-RAIZ-COHERENT' else 'propagation exponent is not a local ringdown damping rate'}
            continue
        kwargs = dict(redshift=redshift, profile='CODATA2018_IAU2015', mode=(2,2,0))
        p = module.prediction(mass,spin,reading,qnm_dimensionless=exact if reading=='R-MOD' else None,**kwargs)
        q = module.prediction(mass,spin,reading,qnm_dimensionless=exact,**kwargs)
        result[reading] = {'status':'CONDITIONAL_ENSEMBLE_POINT_PREDICTION',
            'delta_tau':p['delta_tau_ensemble_exact'], 'delta_f':p['delta_f_ensemble'],
            'x':p['x'], 'Gamma_per_s':p['gamma_per_s'], 'tau_GR_s':p['tau_gr_s'],
            'qnm_method':p['qnm_method'], 'scope':p['scope'],
            'all_exact_QNM_control_delta_tau':q['delta_tau_ensemble_exact']}
    return result


def collect_event(spec, module, interp, snr):
    path = B/spec['path']
    before = sha(path)
    if before != spec['sha256']:
        raise ValueError('HDF5 pin mismatch: '+str(path))
    with h5py.File(path,'r') as handle:
        dataset_path = spec['label']+'/posterior_samples'
        if not isinstance(handle.get(spec['label'],getlink=True),h5py.HardLink) or not isinstance(handle.get(dataset_path,getlink=True),h5py.HardLink):
            raise ValueError('External/soft HDF link forbidden')
        ds = handle[dataset_path]
        names = ds.dtype.names
        spin = 'final_spin_non_evolved' if 'final_spin_non_evolved' in names else 'final_spin'
        mass = 'final_mass_non_evolved' if 'final_mass_non_evolved' in names else 'final_mass'
        selected = ['domega220','dtau220',spin,mass,'redshift']
        if not set(selected).issubset(names) or len(ds.shape)!=1:
            raise ValueError('Unexpected HDF schema')
        if any('weight' in field.lower() for field in names):
            raise ValueError('Weights require explicit interpretation before ddof1')
        draws = ds.fields(selected)[()]
    if sha(path)!=before:
        raise ValueError('Source changed during HDF read')
    ss = {key:stats(draws[field]) for key,field in [('df',selected[0]),('dtau',selected[1]),('spin',spin),('mass_detector',mass),('redshift','redshift')]}
    if ss['dtau']['N']!=spec['N']:
        raise ValueError('Posterior count changed')
    result = {'product_id':spec['release']+':'+spec['event'], 'event':spec['event'],
        'release':spec['release'], 'model':spec['model'], 'N':len(draws),
        'source_path':str(path.relative_to(R)), 'source_sha256':before, 'dataset':dataset_path,
        'field_mapping':dict(df=selected[0],dtau=selected[1],spin=spin,mass_detector=mass,redshift='redshift'),
        'stats':ss, 'stdtau':ss['dtau']['std_ddof1'], 'stddf':ss['df']['std_ddof1'],
        'mean_dtau':ss['dtau']['mean'], 'median_dtau':ss['dtau']['median'],
        'mean_df':ss['df']['mean'], 'median_df':ss['df']['median'],
        'M_detector_median':ss['mass_detector']['median'], 'spin_median':ss['spin']['median'],
        'redshift_median':ss['redshift']['median'],
        'df_dtau_correlation':float(np.corrcoef(draws['domega220'],draws['dtau220'])[0,1]),
        'snr_existing_metadata':snr.get(spec['event'],[]),
        'predictions':predictions(ss['mass_detector']['median'],ss['spin']['median'],ss['redshift']['median'],module,interp)}
    SOURCES[str(path.relative_to(R))] = {'sha256':before,'bytes':path.stat().st_size,
        'mode':'SELECTED_EXISTING_POSTERIOR_FIELDS_READ','dataset':dataset_path,'fields':selected}
    print(json.dumps({'event':spec['event'],'release':spec['release'],'N':len(draws),'stdtau':result['stdtau'],'stddf':result['stddf']}),flush=True)
    return result


def combined(rows, reading, sigma_name, prediction_key='delta_tau'):
    sig = np.array([r['stats']['dtau'][sigma_name] for r in rows])
    if np.any(sig<=0) or not np.all(np.isfinite(sig)):
        raise ValueError('Invalid sigma')
    w=1/sig**2;info=float(w.sum());n=len(rows)
    y=np.array([r['median_dtau'] for r in rows]);means=np.array([r['mean_dtau'] for r in rows])
    center=float(w@y/info);center_mean=float(w@means/info);sigma=1/math.sqrt(info)
    base={'N_events':n,'I_tau_current':info,'GW250114_equivalents_tau_reference_0p058':info*.058**2,
          'sigma_combined':sigma,'sigma_convention':sigma_name,'observed_weighted_median_center':center,
          'observed_weighted_mean_center_control':center_mean,'offset_zero_status':'PROIBIDA_COMO_TESTE_CALIBRATION_ONLY',
          'max_information_fraction':float(w.max()/info)}
    if rows[0]['predictions'][reading]['delta_tau'] is None:
        return base|{'status':'OPEN_NO_UNIQUE_LOCAL_DTAU','z_comb':None,'N50':None,'N90':None,
                     'I_tau_target90':None,'GW250114_equivalents_target90':None,'z_slope':None,
                     'N50_slope':None,'N90_slope':None,'N_spurious50_median':None}
    delta=np.array([r['predictions'][reading][prediction_key] for r in rows])
    pbar=float(w@delta/info);q=float(w@(delta**2));z=math.sqrt(q);centered=delta-pbar
    lever=float(w@(centered**2));zs=math.sqrt(lever)
    n50=25*n/q if q>0 else None;n90=n50*FACTOR if n50 is not None else None
    zobs=(center-pbar)/sigma;zobs_mean=(center_mean-pbar)/sigma
    row=base|{'status':'CONDITIONAL_GAUSSIAN_CALIBRATION' if q>0 else 'ZERO_EFFECT_NO_FINITE_POWER_TARGET',
        'delta_weighted':pbar,'delta_min':float(delta.min()),'delta_max':float(delta.max()),
        'z_comb':z,'z_common':abs(pbar)/sigma,'N50':n50,'N90':n90,'N90_factor':FACTOR,
        'I_tau_target90':n90*info/n if n90 is not None else None,
        'GW250114_equivalents_target90':n90*info/n*.058**2 if n90 is not None else None,
        'signal_information_current':q,'z_slope':zs,'N50_slope':25*n/lever if lever>0 else None,
        'N90_slope':FACTOR*25*n/lever if lever>0 else None,
        'z_observed_vs_prediction_median':zobs,'z_observed_vs_prediction_mean_control':zobs_mean,
        'N_spurious50_median':25*n/zobs**2 if zobs!=0 else None,
        'N_spurious50_mean_control':25*n/zobs_mean**2 if zobs_mean!=0 else None,
        'analytic_small_effect_below_1e12_inverse':bool(np.max(np.abs(delta))<1e-12 and q>0),
        'physical_acceptance':False}
    if lever>0:
        slope=float(np.sum(w*centered*(y-center))/lever);intercept=center-slope*pbar
        row['intercept_slope_calibration_medians']={'intercept':intercept,'slope':slope,
            'intercept_se':math.sqrt(1/info+pbar*pbar/lever),'slope_se':1/math.sqrt(lever),
            'covariance':[[1/info+pbar*pbar/lever,-pbar/lever],[-pbar/lever,1/lever]],
            'scope':'WLS diagnostic on event medians, not E1 full-posterior nuisance'}
    else:
        row['intercept_slope_calibration_medians']={'status':'NON_IDENTIFIABLE'}
    return row


def main():
    for name in ['DATASET.json','DATASET_SCHEMA.json','E0_CORE.json','COST_RECEIPT.json']:
        if (OUT/name).exists():raise FileExistsError(OUT/name)
    budget=read_json(B/'bis/PART_B_BUDGET_START.json')
    deadline=datetime.fromisoformat(budget['hard_deadline_utc'])
    if START>=deadline:raise RuntimeError('Budget deadline passed')
    codepath=B/'tgl_ringdown_prediction.py';codehash=sha(codepath)
    SOURCES[str(codepath.relative_to(R))]={'sha256':codehash,'bytes':codepath.stat().st_size,'mode':'AUTHORIZED_RUNTIME_PREDICTION_MODULE'}
    spec=importlib.util.spec_from_file_location('e0_pinned_predictions',codepath);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    if sha(codepath)!=codehash:raise ValueError('Prediction module changed')
    grid=read_json(B/'QNM_GRID.json')['modes']['220']
    interp=CubicSpline(grid['spins'],np.array(grid['real'])+1j*np.array(grid['imag']),extrapolate=False)
    registry=read_json(B/'C1_LEITURAS_v4.json')
    if set(x['reading'] for x in registry['rows'])!=set(READINGS):raise ValueError('Reading registry mismatch')
    current=read_json(B/'C4_CATALOG_SCHEMA.json')
    selection=read_json(B/'C4_CATALOG_COMBINATION.json')
    oldschema=read_json(B/'C4_GWTC3_SCHEMA.json')
    oldmap=read_json(B/'C4_GWTC3_220.json')
    oldselection=read_json(B/'C4_GWTC3_SELECTION.json')
    snr={}
    tgrpath=A/'B_catalogos/gwtc5_tgr_table2_3_parsed.json'
    for x in read_json(tgrpath):
        snr.setdefault(x['event'],[]).append({'value':x['snr'],'convention':'TGR_TABLE_NETWORK','table':x['table'],'source':str(tgrpath.relative_to(R))})
    gwoscpath=A/'E_instrumento/gwosc_catalogs_raw.json'
    for cat,values in read_json(gwoscpath).items():
        for x in values:snr.setdefault(x[0],[]).append({'value':x[2],'convention':'GWOSC_NETWORK_ARCHIVED','catalog':cat,'source':str(gwoscpath.relative_to(R))})
    specs=[]
    for x in current['rows']:
        specs.append({'release':'GWTC5','event':x['event'],'path':'cache/public/21454847/extracted/pSEOB/metafiles/'+x['filename'],
            'label':x['label'],'sha256':x['sha256'],'N':x['N'],'model':'pSEOBNRv5PHM'})
    legacy={x['member']:x for x in oldschema['rows']}
    for x in oldmap['rows']:
        source=legacy[x['legacy_member']]
        if source['sha256']!=x['source_sha256']:raise ValueError('Legacy schema/map pin mismatch')
        specs.append({'release':'GWTC3','event':x['event'],'path':source['path'].replace('\\','/'),
            'label':x['label'],'sha256':source['sha256'],'N':x['N'],'model':'pSEOBNRv4HM'})
    events=[collect_event(x,module,interp,snr) for x in specs]
    index={x['product_id']:x for x in events}
    if len(index)!=51:raise ValueError('Unexpected product count')
    sets={'GWTC5_31':['GWTC5:'+e for e in selection['selected_events']],
        'GWTC5_33':[r['product_id'] for r in events if r['release']=='GWTC5'],
        'GWTC3_18':[r['product_id'] for r in events if r['release']=='GWTC3'],
        'GWTC3_10':['GWTC3:'+e for e in oldselection['selected_events']]}
    current_ids={x['event'] for x in events if x['release']=='GWTC5'}
    sets['UNION39']=sets['GWTC5_33']+[r['product_id'] for r in events if r['release']=='GWTC3' and r['event'] not in current_ids]
    for name,expected in [('GWTC5_31',31),('GWTC5_33',33),('UNION39',39),('GWTC3_18',18),('GWTC3_10',10)]:
        if len(sets[name])!=expected or len({index[k]['event'] for k in sets[name]})!=expected:raise ValueError('Population duplicate/count failure '+name)
    data={'status':'NONBLIND_EXISTING_POSTERIOR_CALIBRATION_ONLY','created_utc':datetime.now(timezone.utc).isoformat(),
        'beta_runtime':module.beta_tgl(),'code_sha256':sha(Path(__file__)), 'prediction_module_sha256':codehash,
        'point_prediction_convention':'At separate component medians of Mdet, spin, z; C4 BCW220 except exact-grid R-MOD; all-exact-QNM control alongside. Not full-posterior likelihood or median of predicted draws.',
        'statistics_convention':'all archived selected column rows, equal empirical weights; sample std ddof=1; linear quantiles',
        'posterior_products':51,'unique_events':39,'sets':sets,'rows':events,'sources':SOURCES.copy()}
    write_new('DATASET.json',data)
    write_new('DATASET_SCHEMA.json',{'status':'DOCUMENTARY_SCHEMA','dataset':'DATASET.json','dataset_sha256':sha(OUT/'DATASET.json'),
        'row_key':'product_id = release:event; never combine both releases for an overlapping event',
        'sets':{name:len(ids) for name,ids in sets.items()},'fields':{
            'stdtau':'sample std dtau220, ddof=1','stddf':'sample std domega220, ddof=1',
            'stats':'df/dtau/spin/mass_detector/redshift: N, mean, median, std_ddof1, quantiles_05_16_50_84_95, sigma_q90, sigma_q68, min, max',
            'M_detector_median':'solar masses, detector-frame remnant field','spin_median':'dimensionless remnant spin',
            'redshift_median':'redshift','predictions':'10 readings; delta_tau null if local observable not defined; all_exact_QNM_control_delta_tau for 8 applicable readings',
            'snr_existing_metadata':'list of previously archived metadata; conventions deliberately separate, may be empty',
            'source_sha256':'raw HDF5 bytes freshly hashed before and after selected fields read'},
        'null_semantics':'OPEN/no unique observable; never zero or numerical success','large_array_exported':False})
    print('DATASET_READY '+str(OUT/'DATASET.json'),flush=True)
    combos={}
    for name,ids in sets.items():
        rows=[index[x] for x in ids]
        combos[name]={mode:{reading:combined(rows,reading,mode) for reading in READINGS} for mode in ['std_ddof1','sigma_q90']}
        combos[name]['exact_QNM_all_control']={reading:combined(rows,reading,'std_ddof1','all_exact_QNM_control_delta_tau') for reading in READINGS}
        for mode in ('std_ddof1','sigma_q90'):
            base=combos[name][mode]['R-GLOBAL']
            combos[name][mode]['GR_FALSE_FALSIFIER']={k:base[k] for k in ['N_events','sigma_combined','observed_weighted_median_center','observed_weighted_mean_center_control','z_observed_vs_prediction_median','N_spurious50_median','N_spurious50_mean_control']}
    # Inherited systematic evidence, with fresh floors and explicit missing calibration.
    cpath=A/'C_piso_sistematico/C_piso_sinais_catalogo.json';components=read_json(cpath)['d_tabela_condicao']
    c2=read_json(B/'bis/C2_TRAJECTORY_expanded_1000.json')
    currentgate=read_json(B/'PORTAO_DO_PODER_013_v2.json')
    wall=read_json(B/'bis/C5_WALL_COUNTS_013BIS.json')
    heritage=read_json(B/'bis/F2_ALL_READING_TABLES_v2.json')
    gw=index['GWTC5:GW250114_082203'];conditions=[]
    for reading in READINGS:
        delta=gw['predictions'][reading]['delta_tau'];floor=abs(delta)/5 if delta is not None else None
        items=[]
        for name,value in components.get(reading,{}).get('itens',{}).items():
            v=abs(value['valor']);items.append({'component':name,'magnitude_inherited':v,
                'source':str(cpath.relative_to(R)),'json_pointer':'/d_tabela_condicao/'+reading+'/itens/'+name+'/valor',
                'below_fresh_floor5':v<floor if floor is not None else None,
                'below_fresh_floor15':v<floor/3 if floor is not None else None,
                'scope':'historical component proxy, not calibrated residual sigma(c); old C2/window if so named'})
        conditions.append({'reading':reading,'delta_reference_fresh_GW250114':delta,'floor5_INPUT':floor,'floor15_INPUT':floor/3 if floor is not None else None,
            'components':items,'current_C2_GR_noise_bias_control':next(r['recolored'] for r in c2['rows'] if r['reading']=='R-A')['mean_dtau'],
            'current_C2_control_source':'ORDEM_013_RINGDOWN/bis/C2_TRAJECTORY_expanded_1000.json/rows[R-A]/recolored/mean_dtau',
            'sigma_c_calibrated':None,'condition_today':'FALSA_PARA_LIBERAR_TESTE_CALIBRACAO_NAO_DEMONSTRADA' if delta not in (None,0) else 'NAO_APLICAVEL_SEM_EFEITO_LOCAL_DEFINIDO_OU_NULO',
            'current_gate_inherited':currentgate['current_verdict'],'missing_components_are_success':False})
    # All scenarios below are deterministic transformations, not simulations or rate forecasts.
    fisher=read_json(B/'C5_FISHER_v3.json')
    gains={'O5_BBH_low_INPUT':1.56,'O5_BBH_high_INPUT':1.79,'O5_BNS_ceiling_DECLARADO':2.06}
    gains.update({r['psd']+'_same_source_PSD':r['snr_ratio_to_O4'] for r in fisher['same_source_R_B'] if r['psd']!='O4'})
    scenarios=[]
    for name in sets:
        for reading in READINGS:
            original=combos[name]['std_ddof1'][reading]
            for scenario,g in gains.items():
                n50=original['N50'];n90=original['N90']
                scenarios.append({'population':name,'reading':reading,'scenario':scenario,'SNR_gain_INPUT':g,
                    'z_comb':original['z_comb']*g if original['z_comb'] is not None else None,
                    'N50':n50/g**2 if n50 is not None else None,'N90':n90/g**2 if n90 is not None else None,
                    'I_tau_target90':original['I_tau_target90'],
                    'scope':'same conditional population and prediction, sigma/g; no rate/selection/years promised'})
    threeg=[]
    for reading in READINGS:
        delta=gw['predictions'][reading]['delta_tau']
        for anchor,anchor_scope in [(40.,'historical peak/postmerger SNR INPUT, not window-validated'),(2/gw['stdtau'],'Fisher-equivalent 2/sigma heuristic, not measured SNR')]:
            for rho in [50.,100.]:
                sigma=gw['stdtau']*anchor/rho
                n50=(5*sigma/abs(delta))**2 if delta not in (None,0) else None
                threeg.append({'reading':reading,'SNR_RD_target_INPUT':rho,'anchor_SNR_INPUT':anchor,'anchor_scope':anchor_scope,
                    'sigma_anchor_fresh_std':gw['stdtau'],'sigma_projected':sigma,'N50':n50,'N90':n50*FACTOR if n50 is not None else None,
                    'scope':'illustrative same-source inverse-SNR transfer; full-IMR sigma not validated for this RD window; no arrival-rate claim'})
    out={'status':'NONBLIND_E0_SCALAR_CORE_ONLY_NOT_E0_ACCEPTANCE','created_utc':datetime.now(timezone.utc).isoformat(),
        'dataset_sha256':sha(OUT/'DATASET.json'),'script_sha256':sha(Path(__file__)), 'N90_factor':FACTOR,
        'primary_prediction_convention':data['point_prediction_convention'],'combinations':combos,'systematics':conditions,
        'O5_3G_same_population_scenarios':scenarios,'threeG_GW250114_anchor_scenarios':threeg,
        'inherited_C4_rows':heritage['rows'],'inherited_C4_scope':'verdicts/lnB inherited, not recalculated; union39 only scalar calibration here',
        'delegated_not_executed':['route-IV Monte Carlo (operator)','SNR fit/GWOSC counts/Poisson exposure/chronograms (Beauvoir)','E1 nuisance and selection'],
        'limitations':['8 readings define an exponential local ensemble shift; coherent and propagation remain explicit OPEN rows in all 5 sets',
            'No likelihood or Bayes factor recalculated; scalar Gaussian calibration and ceilings only','Equal posterior empirical weights, not ESS',
            'Component medians prediction differs from median of predicted draws','Systematic components inherited, not new injection calibration'],
        'sources':SOURCES.copy()}
    write_new('E0_CORE.json',out)
    end=datetime.now(timezone.utc)
    receipt={'status':'COMPLETED_SCALAR_ONLY','started_utc':START.isoformat(),'finished_utc':end.isoformat(),
        'wall_seconds':time.perf_counter()-WALL,'process_cpu_seconds':time.process_time()-CPU,
        'processes':1,'requested_threads':1,'thread_env':{k:os.environ[k] for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')},
        'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'h5py':h5py.__version__,'platform':platform.platform(),
        'operator_budget_started_utc':budget['started_utc'],'operator_deadline_utc':budget['hard_deadline_utc'],
        'continuous_elapsed_from_operator_start_seconds':(end-datetime.fromisoformat(budget['started_utc'])).total_seconds(),
        'budget_accounting':'continuous wall-clock shared budget; own CPU/wall reported, never add overlapping worker wall times',
        'new_posteriors':False,'strain':False,'PE':False,'waveform_simulations':False,'E1_run':False,
        'raw_HDF5_sources':51,'sources':SOURCES,'script_sha256':sha(Path(__file__)),
        'outputs':{name:{'bytes':(OUT/name).stat().st_size,'sha256':sha(OUT/name)} for name in ['DATASET.json','DATASET_SCHEMA.json','E0_CORE.json']}}
    write_new('COST_RECEIPT.json',receipt)
    print(json.dumps({'status':receipt['status'],'wall_seconds':receipt['wall_seconds'],'cpu_seconds':receipt['process_cpu_seconds'],
        'GWTC5_31_RB':combos['GWTC5_31']['std_ddof1']['R-B'],'GR_spurious':combos['GWTC5_31']['std_ddof1']['GR_FALSE_FALSIFIER']}),flush=True)


if __name__=='__main__':
    main()
