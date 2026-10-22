"""Independent R1/R2/R3 finite fixtures. Never import a scientific producer main."""
import ast, copy, hashlib, importlib.util, json, math, multiprocessing, sys, time, types
from pathlib import Path
from datetime import datetime, timezone
import numpy as np

HERE=Path(__file__).resolve().parent
SNAP=HERE/'snapshot'
B=HERE.parents[2]
RECORDS=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check(name,condition,detail=None):
    if not condition:raise RuntimeError('FAILED: '+name)
    RECORDS.append(dict(name=name,passed=True,detail=detail))
def reject(name,fn,exc=(ValueError,RuntimeError,KeyError)):
    try:fn()
    except exc as error:RECORDS.append(dict(name=name,passed=True,refusal=type(error).__name__,message=str(error)))
    else:raise RuntimeError('ACCEPTED NEGATIVE: '+name)
def extract(file,names,ns):
    tree=ast.parse((SNAP/file).read_text(encoding='utf-8'))
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    if {n.name for n in nodes}!=set(names):raise RuntimeError('Missing function')
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SNAP/file),'exec',optimize=1),ns)
    return ns
def child_count(obj):
    for j in range(11):obj.log_likelihood({'x':float(j)})

def main():
    started=time.perf_counter();cpu=time.process_time()
    installed='--installed' in sys.argv
    output=HERE/('INDEPENDENT_INSTALLED_FINITE.json' if installed else 'INDEPENDENT_FINITE.json')
    if output.exists():raise FileExistsError(output)
    sources={p.name:sha(p) for p in sorted(SNAP.glob('*.py'))}
    check('fourteen_source_bytes_current_before',len(sources)==14 and all(sha(B/'bis/e2_code'/n)==h for n,h in sources.items()))
    for p in SNAP.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'))
    check('fourteen_sources_parse',True)
    a=json.loads((B/'bis/e2_review/PE_R3_RECEIPT.json').read_text())
    check('A_seven_source_pins_match',all(sources[n]==h for n,h in a['source_sha256'].items()))
    check('A_six_artifact_pins_match',all(sha(B/'bis/e2_review'/n)==h for n,h in a['files_written'].items()))
    lal=types.ModuleType('lal');lal.MSUN_SI=1.;lal.CreateDict=dict
    ls=types.ModuleType('lalsimulation');bounds=dict(inspiral=1.,merger=.1,tail=.2)
    ls.SimInspiralChirpTimeBound=lambda *a:bounds['inspiral']
    ls.SimInspiralMergeTimeBound=lambda *a:bounds['merger']
    ls.SimInspiralFinalBlackHoleSpinBound=lambda *a:.7
    ls.SimInspiralRingdownTimeBound=lambda *a:bounds['tail']
    for name in ('DTau220','DTau440','DOmega220','DOmega440'):
        setattr(ls,'SimInspiralWaveformParamsInsert'+name,lambda d,v:None)
    bilby=types.ModuleType('bilby');gw=types.ModuleType('bilby.gw');source=types.ModuleType('bilby.gw.source')
    calls=dict(generator=0,wave=0,injected=0);post_mutation={}
    def finite_wave(f,*args,**kw):
        calls['wave']+=1
        return dict(plus=np.ones(len(f),complex),cross=np.zeros(len(f),complex))
    source.lal_binary_black_hole=finite_wave;bilby.gw=gw;gw.source=source
    temporal=types.ModuleType('temporal_contract');temporal.math=math
    extract('temporal_contract.py',['validate_time_contract'],temporal.__dict__)
    sys.modules.update({'lal':lal,'lalsimulation':ls,'bilby':bilby,'bilby.gw':gw,'bilby.gw.source':source,'temporal_contract':temporal})
    nss=extract('pseob_source.py',['pseob_frequency_domain','validate_polarizations','parameter_conversion'],
        dict(np=np,time=time,STOP_UTC_TIMESTAMP=None,COST_COUNTER=None))
    nsi=extract('injection_design.py',['aligned_gr_xphm','validate_truth_support','inject_into_ifos'],
        dict(np=np,validate_time_contract=temporal.validate_time_contract,**{k:nss[k] for k in ('pseob_frequency_domain','parameter_conversion')}))
    class Generator:
        def __init__(self,**kw):self.kw=kw;calls['generator']+=1
        def frequency_domain_strain(self,params):
            pol=self.kw['frequency_domain_source_model'](np.array([20.,21.]),**params,**self.kw['waveform_arguments'])
            params.update(post_mutation)
            return pol
    gw.WaveformGenerator=Generator
    class Ifo:
        def __init__(self,name):
            self.name=name;self.strain_data=types.SimpleNamespace(start_time=100.,time_within_data=lambda t:100<=t<=108)
        def time_delay_from_geocenter(self,*args):return 0.
        def get_detector_response(self,p,params):return p['plus']
        def optimal_snr_squared(self,h):return np.vdot(h,h).real
        def inject_signal(self,**kw):calls['injected']+=1
    cfg=copy.deepcopy(json.loads((SNAP/'E2_DESIGN_DRAFT_002.json').read_text())['pe_jobs']['GW250114_PILOT'])
    cfg.update(mode='calibration',segment_start_GPS=100.,event_GPS=1000.,duration_s=8.)
    cfg['priors']['geocent_time'].update(minimum=100.25,maximum=107.75)
    truth={k:0. for k in cfg['priors'] if k!='mass_ratio'}
    truth.update(mass_1=30.,mass_2=25.,luminosity_distance=1000.,geocent_time=103.,theta_jn=1.)
    cfg['data']={n:dict(onsource_path='SYNTHETIC',offsource_path='SYNTHETIC',onsource_sha256='SYNTHETIC',offsource_sha256='SYNTHETIC') for n in ('H1','L1')}
    reg=dict(calibration_event_ids=[cfg['event']],event_reference_GPS={cfg['event']:1000.})
    def run(family,params=None,target=2.):
        calls.update(generator=0,wave=0,injected=0)
        test=copy.deepcopy(cfg);test['injection']=dict(family=family,noise_kind='REAL_OFFSOURCE',parameters=truth if params is None else params,target_network_optimal_SNR=target)
        return nsi['inject_into_ifos']([Ifo('H1'),Ifo('L1')],test,reg)
    for family in ('pSEOBNRv4HM_PA','IMRPhenomXPHM'):
        result=run(family)
        check(family+'_positive',result['optimal_network_SNR']==2. and calls==dict(generator=1,wave=1,injected=2))
        for label,t in [('left',100.3),('delay_only_left',101.31),('right',107.7)]:
            bad=dict(truth,geocent_time=t)
            reject(family+'_R1_'+label,lambda:run(family,bad),RuntimeError)
            check(family+'_R1_'+label+'_before_wave',calls==dict(generator=1,wave=0,injected=0))
        # Every recovery coordinate: two out-of-range values plus a nonfinite value.
        for key in truth:
            p=cfg['priors'][key]
            for label,value in [('below',p['minimum']-1.),('above',p['maximum']+1.),('nan',float('nan'))]:
                bad=dict(truth);bad[key]=value
                reject(family+'_R2_'+key+'_'+label,lambda:run(family,bad),ValueError)
                if calls!=dict(generator=0,wave=0,injected=0):raise RuntimeError('Late truth guard')
        for key in truth:
            bad=dict(truth);del bad[key]
            reject(family+'_missing_'+key,lambda:run(family,bad),ValueError)
        for label,patch in [('q_below',dict(mass_1=100.,mass_2=10.)),('q_above',dict(mass_1=20.,mass_2=25.)),
                            ('q_inconsistent',dict(mass_ratio=.5)),('q_nan',dict(mass_ratio=float('nan'))),('unknown',dict(extra=1.))]:
            reject(family+'_R2_'+label,lambda patch=patch:run(family,dict(truth,**patch)),ValueError)
            if calls['generator'] or calls['wave'] or calls['injected']:raise RuntimeError('Constraint too late')
        for label,target in [('distance_low',40.),('distance_high',.5)]:
            reject(family+'_rescaled_'+label,lambda:run(family,target=target),ValueError)
            check(family+'_rescaled_'+label+'_before_inject',calls==dict(generator=1,wave=1,injected=0))
        # Mutate each truth field only AFTER the finite generator returned: second validation required.
        for key in truth:
            post_mutation[key]=cfg['priors'][key]['maximum']+1.
            reject(family+'_post_generation_'+key,lambda:run(family),ValueError)
            if calls!=dict(generator=1,wave=1,injected=0):raise RuntimeError('Post-generation support not checked')
            post_mutation.clear()
    reject('pseob_scaled_tail',lambda:run('pSEOBNRv4HM_PA',dict(truth,geocent_time=107.,dtau440=4.)),RuntimeError)
    check('pseob_scaled_tail_before_wave',calls['wave']==0)
    direct=dict(mass_1=30.,mass_2=25.,chi_1=0.,chi_2=0.,minimum_frequency=20.,geocent_time=103.,timing=dict(start_GPS=100.,duration_s=8.,roll_off_s=.2))
    out=temporal.validate_time_contract(**direct)
    check('independent_margin_arithmetic',np.allclose(out['margins_s'],[1.678,4.578],rtol=0,atol=1e-12))
    for label,patch in [('missing_contract',dict(timing=None)),('missing_time',dict(geocent_time=None)),('nonfinite_time',dict(geocent_time=float('inf'))),('invalid_tail',dict(dtau220=-1.))]:
        reject(label,lambda patch=patch:temporal.validate_time_contract(**dict(direct,**patch)),ValueError)
    for key in bounds:
        for value in (-1.,float('nan'),float('inf')):
            original=bounds[key];bounds[key]=value
            reject('invalid_bound_'+key+'_'+str(value),lambda:temporal.validate_time_contract(**direct),RuntimeError)
            bounds[key]=original
    # R3 uses the current functions; installed mode extracts the actual pinned full->ratio method by AST.
    ns=extract('pe_runner.py',['counted_likelihood_class','likelihood_snapshot'],dict(time=time))
    frontier_source=json.loads((B/'bis/e2_review/LIKELIHOOD_COUNTER_FINITE.json').read_text())['pinned_base_log_likelihood_source']
    installed_evidence={}
    if installed:
        manifest_path=B/'bis/E2_SCIENTIFIC_RUNTIME_MANIFEST.json';pins=json.loads(manifest_path.read_text())['files']
        base=Path('/opt/lal_env/lib/python3.12/site-packages/bilby/gw/likelihood/base.py')
        check('installed_Bilby_bytes_pinned',sha(base)==pins[str(base)]['sha256'])
        tree=ast.parse(base.read_text());cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='GravitationalWaveTransient')
        method=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='log_likelihood')
        frontier_source=ast.unparse(method)
        installed_evidence['Bilby_base_sha256']=sha(base)
        for name in ('astropy','pandas'):
            p=Path(importlib.util.find_spec(name).origin).resolve()
            check(name+'_active_resolution_pinned',sha(p)==pins[str(p)]['sha256'])
            installed_evidence[name]=dict(path=str(p),sha256=sha(p))
    import textwrap
    local={};exec(compile(textwrap.dedent(frontier_source),'<full_likelihood_frontier>','exec'),local)
    class Base:
        log_likelihood=local['log_likelihood']
        def log_likelihood_ratio(self,parameters=None):
            if parameters.get('fail'):raise ValueError('finite refusal before generator')
            if parameters.get('interrupt'):raise KeyboardInterrupt('finite interruption')
            return -parameters['x']**2
        def noise_log_likelihood(self):return -2.
    counter=multiprocessing.Array('d',[0.,0.,0.,0.],lock=True)
    obj=ns['counted_likelihood_class'](Base,counter)()
    check('R3_ratio_preserved',obj.log_likelihood_ratio({'x':2.})==-4.)
    check('R3_full_preserved',obj.log_likelihood({'x':2.})==-6.)
    obj.noise_log_likelihood()
    check('R3_no_double_count_no_noise',list(counter)[:3]==[2.,2.,0.])
    reject('R3_failed_attempt',lambda:obj.log_likelihood({'fail':True}),ValueError)
    reject('R3_baseexception_preserved',lambda:obj.log_likelihood({'interrupt':True}),KeyboardInterrupt)
    check('R3_attempt_accounting',list(counter)[:3]==[4.,2.,2.])
    if installed:
        children=[multiprocessing.get_context('fork').Process(target=child_count,args=(obj,)) for _ in range(2)]
        for p in children:p.start()
        for p in children:
            p.join(10)
            if p.is_alive():p.kill();p.join();raise RuntimeError('Finite child timed out')
            check('R3_fork_exit_'+str(p.pid),p.exitcode==0)
        check('R3_shared_fork_aggregation',list(counter)[:3]==[26.,24.,2.])
    final_counter=ns['likelihood_snapshot'](counter)
    check('R3_nonnegative_time',final_counter['total_wall_seconds']>=0)
    check('fourteen_source_bytes_current_after',all(sha(B/'bis/e2_code'/n)==h for n,h in sources.items()))
    result=dict(status='PASS_FINITE_ONLY_R1_R2_R3',created_utc=datetime.now(timezone.utc).isoformat(),python_optimize=sys.flags.optimize,
        source_sha256=sources,script_sha256=sha(__file__),checks=RECORDS,check_count=len(RECORDS),
        negative_count=sum('refusal' in r for r in RECORDS),installed_evidence=installed_evidence,likelihood_counter=final_counter,
        wall_seconds=time.perf_counter()-started,parent_cpu_seconds=time.process_time()-cpu,
        physical_waveforms=0,PE_runs=0,strain_reads=0,producer_mains_imported=0,
        scope='Synthetic vectors and scalar bounds; exact all-free truth supports; ratio-frontier accounting. No physical support certification or sampler campaign.')
    with output.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False,allow_nan=False)
    print(json.dumps({k:result[k] for k in ('status','check_count','negative_count','wall_seconds','likelihood_counter')}))

if __name__=='__main__':main()
