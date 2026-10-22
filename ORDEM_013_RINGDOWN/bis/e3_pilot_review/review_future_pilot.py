"""Read-only future NONBLIND pilot review. Default mode opens no result files."""
import argparse,hashlib,json,math,time
from pathlib import Path
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;B=HERE.parents[1]
def require(ok,message):
    if not ok:raise ValueError(message)
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def load(p):
    def pairs(items):
        d={}
        for k,v in items:
            require(k not in d,'Duplicate JSON key');d[k]=v
        return d
    def number(s):
        v=float(s);require(math.isfinite(v),'Nonfinite JSON float');return v
    def bad(s):raise ValueError('Nonfinite JSON constant')
    return json.loads(Path(p).read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,parse_constant=bad,parse_float=number)
def finite(x):return type(x) in (int,float) and math.isfinite(x)
def count(x):return type(x) is int and x>=0
def gates(controller,conv,settings,failure_present=False,analyst_status=None):
    """Pure metadata decision. Never rescue a partial using an incidental raw file."""
    if failure_present:return ['FAILURE_PRESENT']
    if analyst_status and analyst_status.get('accepted') is not True:return ['ANALYST_PARTIAL_OR_REFUSAL']
    if controller.get('status')!='CHILD_COMPLETED_REQUIRES_REVIEW' or controller.get('returncode')!=0:return ['CONTROLLER_PARTIAL_OR_FAILURE']
    if controller.get('cleanup',{}).get('group_absent') is not True:return ['CLEANUP_NOT_CONFIRMED']
    if not conv:return ['MISSING_CONVERGENCE']
    errors=[]
    def test(ok,label):
        if not ok:errors.append(label)
    test(conv.get('accepted_for_analysis') is True,'NOT_ACCEPTED_BY_PRODUCER')
    test(conv.get('status')=='CONVERGENCE_CRITERIA_MET_REQUIRES_INDEPENDENT_REVIEW','BAD_CONVERGENCE_STATUS')
    test(conv.get('before_add_live') is True,'PRE_LIVE_CAPTURE_MISSING')
    d=conv.get('delta_logz');test(finite(d) and 0<=d<settings['dlogz'],'DLOGZ_NOT_REACHED')
    test(conv.get('threshold')==settings['dlogz'],'DLOGZ_THRESHOLD_DIFFERS')
    n=conv.get('ncall');test(count(n) and n<settings['maxcall'],'MAXCALL_OR_INVALID_CALLS')
    test(n==conv.get('ncall_reported'),'SAMPLER_COUNTS_DIFFER')
    ess=conv.get('ess');test(finite(ess) and ess>=settings['minimum_effective_samples'],'LOW_OR_INVALID_ESS')
    N=conv.get('posterior_samples');test(count(N) and N>=settings['minimum_posterior_samples'],'LOW_OR_INVALID_N')
    test(finite(conv.get('log_evidence')) and finite(conv.get('log_evidence_err')) and conv['log_evidence_err']>=0,'INVALID_EVIDENCE_METADATA')
    return errors
def review(contract):
    for name,pin in contract['source_pins'].items():require(sha(B/name)==pin,'Prepared source/config changed: '+name)
    cfg=contract['job_config'];settings=cfg['sampler'];digest=contract['registration_sha256']
    require(cfg['mode']=='calibration' and cfg['event']=='GW250114_082203','Nonblind pilot only')
    root=(B/'cache'/cfg['output_directory_name']).resolve()
    require(root.is_relative_to((B/'cache').resolve()),'Escaping result path')
    base=dict(job=contract['job'],registration_sha256=digest,posterior_summary=None,comparison=None,
        same_event_not_independent=True,scientific_acceptance=False,read_files={},issues=[])
    if not (root/'CONTROLLER.json').is_file():return dict(base,status='AWAITING_COMPLETED_CONTROLLER_NO_POSTERIOR_READ')
    def tracked(name):
        p=root/name;h=sha(p);v=load(p);require(sha(p)==h,'File changed during read');base['read_files'][name]=h;return v
    ctrl=tracked('CONTROLLER.json');ctx=tracked('LAUNCH_CONTEXT.json')
    for obj in (ctrl,ctx):require(obj['registration_sha256']==digest and obj['job']==contract['job'],'Wrong registration/job')
    require(ctrl.get('blind') is False,'Blind result not permitted')
    expected_cfg=hashlib.sha256(json.dumps(cfg,sort_keys=True,allow_nan=False).encode()).hexdigest()
    require(ctx['config_sha256']==expected_cfg,'Job configuration differs')
    require(ctrl['controller_code_sha256']==contract['source_pins']['bis/e2_code/run_controlled.py'],'Controller source differs')
    conv=tracked('PRIVATE_CONVERGENCE.json') if (root/'PRIVATE_CONVERGENCE.json').is_file() else None
    partial=tracked('ANALYST_STATUS.json') if (root/'ANALYST_STATUS.json').is_file() else None
    failure=tracked('FAILURE.json') if (root/'FAILURE.json').is_file() else None
    for obj in (conv,partial,failure):
        if obj is not None:require(obj['registration_sha256']==digest,'Foreign metadata receipt')
    base['controller_cost']={k:ctrl.get(k) for k in ('wall_seconds','children_user_cpu_seconds','children_system_cpu_seconds','status','returncode','cleanup')}
    base['producer_cost']=conv.get('cost') if conv else failure
    errors=gates(ctrl,conv,settings,failure is not None,partial)
    if errors:return dict(base,status='PARTIAL_OR_REFUSED_NO_POSTERIOR_REVIEW',issues=errors)
    cost=conv['cost'];counter=cost['likelihood_counter']
    require(all(count(counter[k]) for k in ('calls','completed','raised')),'Invalid R3 count')
    require(counter['calls']==counter['completed']+counter['raised']==cost['likelihood_calls'],'R3 counter not reconciled')
    phases=cost['likelihood_phase_snapshots'];previous=-1
    for phase in ('before_sampler_constructor','after_sampler_constructor','after_run_sampler'):
        c=phases[phase];require(count(c['calls']) and c['calls']>=previous and c['calls']==c['completed']+c['raised'],'Invalid phase snapshot');previous=c['calls']
    require(phases['after_run_sampler']==counter,'Final R3 snapshot differs')
    require(cost['sampler_ncall']==conv['ncall'] and cost['maxcall_nominal']==settings['maxcall'],'Sampler cost differs')
    require(count(cost['source_calls']),'Invalid source count')
    for obj,names in [(cost,('wall_seconds','parent_cpu_seconds','source_total_wall_seconds')),(counter,('total_wall_seconds',)),(ctrl,('wall_seconds','children_user_cpu_seconds','children_system_cpu_seconds'))]:
        require(all(finite(obj[k]) and obj[k]>=0 for k in names),'Invalid timing metadata')
    if cost['source_calls']:
        require(math.isclose(cost['source_seconds_per_call'],cost['source_total_wall_seconds']/cost['source_calls'],rel_tol=1e-10),'Source denominator mismatch')
    else:require(cost['source_seconds_per_call'] is None,'Zero source calls must have null rate')
    require(cost['workers']==settings['workers'] and cost['thread_caps_requested']==1,'Worker/thread metadata differs')
    require((root/'ANALYST_OUTPUT.json').is_file(),'Missing complete analyst output')
    # Scientific arrays opened only after all preceding metadata gates.
    analyst=tracked('ANALYST_OUTPUT.json')
    require(analyst['registration_sha256']==digest and analyst['job']==contract['job'],'Wrong analyst job')
    require(analyst['status']=='NONBLIND_CALIBRATION_POSTERIOR_REQUIRES_REVIEW','Wrong analyst output scope')
    require(analyst['convergence_status']==conv['status'],'Analyst convergence differs')
    final_cost=analyst['cost']
    for k in ('likelihood_counter','likelihood_calls','source_calls','source_total_wall_seconds','sampler_ncall'):
        require(final_cost[k]==cost[k],'Final cost unexpectedly changed: '+k)
    require(final_cost['wall_seconds']>=cost['wall_seconds'] and final_cost['parent_cpu_seconds']>=cost['parent_cpu_seconds'],'Final cost predates remnant conversion')
    if ctrl['wall_seconds']>cfg['wall_budget_seconds']:base['issues'].append('CONTROLLER_WALL_EXCEEDS_REGISTERED_JOB_CAP')
    import numpy as np
    import h5py
    names=contract['fields']['PHYSICAL']+contract['fields']['DEFORMATIONS'];derived=contract['fields']['DERIVED_PHYSICAL']
    require(set(analyst['columns'])==set(names+derived),'Exact 18 paired columns required')
    arrays={n:np.asarray(analyst['columns'][n],dtype=float) for n in names+derived};N=conv['posterior_samples']
    require(all(v.shape==(N,) and np.isfinite(v).all() for v in arrays.values()),'Nonfinite/unpaired analyst samples')
    require(analyst['injection_receipt'] is None,'Pilot must be real nonblind event, not injected calibration')
    for name in names:
        prior=cfg['priors'][name];require(np.all((arrays[name]>=prior['minimum'])&(arrays[name]<=prior['maximum'])),'Posterior outside prior: '+name)
    q=arrays['mass_2']/arrays['mass_1'];qp=cfg['priors']['mass_ratio'];require(np.all((q>=qp['minimum'])&(q<=qp['maximum'])),'Mass-ratio support violated')
    rem=tracked('PRIVATE_REMNANT_CONVERSION.json')
    require(rem==analyst['remnant_conversion_receipt'] and rem['N']==N and rem['same_order_no_thinning'] is True,'Remnant pairing receipt differs')
    require(np.all((arrays['final_mass_detector']>0)&(arrays['final_mass_detector']<=arrays['mass_1']+arrays['mass_2'])) and np.all(np.abs(arrays['final_spin'])<1) and np.all(arrays['redshift']>=0),'Invalid derived domain')
    raw=analyst['raw_result_files'];h5names=[n for n in raw if n.endswith(('.hdf5','.h5'))]
    require(len(h5names)==1,'Need exactly one pinned native HDF5 result; no pickle fallback loading')
    filename=h5names[0];require(Path(filename).name==filename,'Raw path must be basename')
    path=root/filename;require(path.resolve().parent==root and sha(path)==raw[filename],'Raw result hash/path differs')
    with h5py.File(path,'r') as h:
        def node(name):
            parts=name.split('/');group=h
            for part in parts:
                require(isinstance(group.get(part,getlink=True),h5py.HardLink),'External/soft HDF5 link refused');group=group[part]
            require(isinstance(group,h5py.Dataset) and not group.is_virtual,'Nonlocal HDF5 dataset refused');return group
        weights=np.asarray(node('nested_samples/weights')[()],dtype=float)
        require(weights.ndim==1 and len(weights)>0 and np.isfinite(weights).all() and np.all(weights>=0) and weights.sum()>0,'Invalid nested weights')
        ess=float(weights.sum()**2/np.dot(weights,weights));require(math.isclose(ess,conv['ess'],rel_tol=1e-9),'ESS mismatch')
        for name in names:require(np.array_equal(node('posterior/'+name)[()],arrays[name]),'HDF5/JSON paired rows differ: '+name)
        for name in ('ncall','delta_logz','threshold','before_add_live'):
            value=node('meta_data/e2_terminal/'+name)[()].item()
            require(value==conv[name],'HDF5 terminal differs: '+name)
        require(int(node('num_likelihood_evaluations')[()])==conv['ncall'],'HDF5 ncall differs')
        registered=node('meta_data/registration_sha256')[()]
        if isinstance(registered,bytes):registered=registered.decode()
        require(registered==digest,'HDF5 registration differs')
    require(sha(path)==raw[filename],'HDF5 changed while reading');base['read_files'][filename]=raw[filename]
    for name,pin in base['read_files'].items():require(sha(root/name)==pin,'Input changed before receipt')
    summaries={n:dict(q05=float(np.quantile(arrays[n],.05)),median=float(np.median(arrays[n])),q95=float(np.quantile(arrays[n],.95)),std_ddof1=float(np.std(arrays[n],ddof=1))) for n in ['dtau220','final_mass_detector','final_spin']}
    reference=contract['published_dtau220_documentary_target'];tau=summaries['dtau220']
    comp=dict(dtau220=dict(reference=reference,median_difference=tau['median']-reference['median'],interval_90_overlap=max(tau['q05'],reference['q05'])<=min(tau['q95'],reference['q95'])),
        remnant='OPEN: require matched published pSEOBv5PHM detector-frame Mf/spin summaries with provenance; do not substitute Kerr reference',
        scope='Aligned pSEOBNRv4HM_PA vs precessing pSEOBNRv5PHM, broad INPUT priors; same data, descriptive only',z_calibrated=None,lnB=None)
    ref=load(HERE/'REFERENCE_CONTRACT.json');rp=(B/ref['relative_to_B']).resolve()
    require(rp.is_relative_to((B/'cache/public').resolve()) and sha(rp)==ref['h5_sha256'],'Published reference path/hash differs')
    with h5py.File(rp,'r') as h:
        group=h
        for part in ref['dataset'].split('/'):
            require(isinstance(group.get(part,getlink=True),h5py.HardLink),'Published external link refused');group=group[part]
        require(isinstance(group,h5py.Dataset) and not group.is_virtual,'Published dataset must be local')
        fields=ref['fields'];require(set(fields)<=set(group.dtype.names or []),'Published fields differ')
        data=group.fields(fields)[()]
        require(len(data)>=2 and all(np.isfinite(data[n]).all() for n in fields),'Invalid published samples')
        frame_ok=np.allclose(data['final_mass_non_evolved'],data['final_mass_source_non_evolved']*(1+data['redshift']),rtol=1e-6,atol=1e-8)
        compared={}
        for own,published in [('dtau220','dtau220'),('final_mass_detector','final_mass_non_evolved'),('final_spin','final_spin_non_evolved')]:
            if own=='final_mass_detector' and not frame_ok:
                compared[own]=dict(status='OPEN_MASS_FRAME_IDENTITY_FAILED');continue
            vals=data[published];quant=np.quantile(vals,[.05,.5,.95]);ours=summaries[own]
            compared[own]=dict(published_05_50_95=quant.tolist(),published_std_ddof1=float(np.std(vals,ddof=1)),
                median_difference=ours['median']-float(quant[1]),interval_90_overlap=bool(max(ours['q05'],quant[0])<=min(ours['q95'],quant[2])))
    require(sha(rp)==ref['h5_sha256'],'Published reference changed')
    comp.update(published_sample_comparison=compared,published_source_sha256=ref['h5_sha256'],published_N=len(data),
        mass_frame_pair_identity=bool(frame_ok),remnant='GR fit conditional on component posterior in each family; not independent remnant measurements',
        reference_weighting='Existing released equal-weight samples; merging provenance remains a limitation')
    return dict(base,status='NUMERICAL_CONSISTENCY_CHECKED_REQUIRES_SCIENTIFIC_REVIEW',posterior_summary=summaries,comparison=comp,
        recomputed_ESS=ess,N=N,final_cost=analyst['cost'],systematic_gate=analyst['systematic_gate'],
        limitations=['Pre-live chronology corroborated by pinned adapter and terminal receipt, not reconstructed from final HDF5','No coverage or multimodality guarantee','GR remnant fit and external Planck18 INPUT, not independent remnant measurement','CPU and summed invocation wall must not be added to job wall'])
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--activate-existing-result-review',action='store_true');parser.add_argument('--output-name');args=parser.parse_args()
    if not args.activate_existing_result_review:
        print(json.dumps(dict(status='PREPARED_INACTIVE_NO_RESULT_FILES_OPENED')));return
    require(args.output_name is not None and Path(args.output_name).name==args.output_name and args.output_name.endswith('.json'),'New local JSON output name required')
    out=HERE/args.output_name;require(not out.exists(),'Do not overwrite review')
    started=time.perf_counter()
    try:result=review(load(HERE/'CONTRACT.json'))
    except Exception as error:result=dict(status='REVIEW_REFUSED_OR_SCHEMA_OPEN',error_type=type(error).__name__,message=str(error),posterior_summary=None,comparison=None,scientific_acceptance=False)
    result.update(created_utc=datetime.now(timezone.utc).isoformat(),wall_seconds=time.perf_counter()-started,review_script_sha256=sha(__file__),contract_sha256=sha(HERE/'CONTRACT.json'))
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False,allow_nan=False)
    print(json.dumps(dict(status=result['status'],output=str(out))))
if __name__=='__main__':main()
