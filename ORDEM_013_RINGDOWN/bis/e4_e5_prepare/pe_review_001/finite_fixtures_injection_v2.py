"""Independent finite mocks extracted by AST. No production main or physical data."""
import ast, copy, hashlib, json, math, os, stat, sys, time, types
from pathlib import Path
from datetime import datetime, timezone
import numpy as np

O=Path(__file__).resolve().parent
S=O/'snapshot'
records=[]


def functions(file,names,ns):
    tree=ast.parse(((O/'integration_snapshot'/file) if file=='injection_design.py' else S/file).read_text(encoding='utf-8'))
    nodes=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in names]
    if {x.name for x in nodes}!=set(names):raise ValueError('Missing functions')
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(S/file),'exec',optimize=1),ns)
    return ns


def check(name,condition,detail=None):
    if not condition:raise ValueError('Failed fixture: '+name)
    records.append({'name':name,'passed':True,'detail':detail})


def rejects(name,call,exception=Exception):
    try:call()
    except exception as e:
        records.append({'name':name,'passed':True,'error_type':type(e).__name__,'message':str(e)})
    else:raise ValueError('Expected refusal: '+name)


def main():
    started=time.perf_counter()
    target=O/'FINITE_FIXTURES_INJECTION_V2.json'
    if target.exists():raise FileExistsError(target)
    draft=json.loads((S/'E2_DESIGN_DRAFT_002.json').read_text())
    cfg=copy.deepcopy(draft['pe_jobs']['GW250114_PILOT'])
    ns={'math':math,'json':json}
    functions('registration_guard.py',['positive','integer','strict_json'],ns)
    ns['PHYSICAL']=('mass_1','mass_2','chi_1','chi_2','luminosity_distance','theta_jn','phase','ra','dec','psi','geocent_time')
    ns['DEFORMATIONS']=('dtau220','dtau440','domega220','domega440')
    functions('pe_runner.py',['validate_config','posterior_columns','terminal_state','convergence'],ns)
    ns['validate_config'](cfg);check('draft002_actual_config_passes',True)
    for key in ns['PHYSICAL']+ns['DEFORMATIONS']:
        bad=copy.deepcopy(cfg);bad['priors'][key]=.1
        rejects('fixed_'+key,lambda bad=bad:ns['validate_config'](bad),ValueError)
    class Frame(dict):
        def __len__(self):return len(next(iter(self.values())))
    frame=Frame({k:np.arange(4,dtype=float)+i/100 for i,k in enumerate(ns['PHYSICAL']+ns['DEFORMATIONS'])})
    result=ns['posterior_columns'](frame,cfg)
    check('15_columns_keep_same_row_order',set(result)==set(frame) and all(np.array_equal(result[k],frame[k]) for k in frame))
    frame['mass_1'][1]=np.nan
    rejects('nonfinite_physical_output',lambda:ns['posterior_columns'](frame,cfg),ValueError)
    sampler=types.SimpleNamespace(ncall=cfg['sampler']['maxcall'],saved_run={'logz':[0.],'logvol':[-30.]},live_logl=np.array([0.,1.]))
    state=ns['terminal_state'](sampler,cfg['sampler'])
    check('maxcall_refused_even_small_delta',state['status']=='PARTIAL_MAXCALL_NOT_ACCEPTED')
    rejects('duplicate_json',lambda:ns['strict_json']('{"x":1,"x":2}'),ValueError)
    # Private descriptor and launch identity fixtures; fake /proc, no real process.
    scratch=O/'fake_launch_injection_v2';scratch.mkdir(exist_ok=False)
    out=scratch/'owned';out.mkdir()
    (out/'PRIVATE.log').write_text('SYNTHETIC LOG ONLY')
    digest='a'*64
    launch={'registration_sha256':digest,'job':'toy','controller_pid':123,'controller_start_ticks':'444',
            'config_sha256':hashlib.sha256(json.dumps(cfg,sort_keys=True,allow_nan=False).encode()).hexdigest(),
            'stop_utc':'2099-01-01T00:00:00+00:00'}
    path=out/'LAUNCH_CONTEXT.json';path.write_text(json.dumps(launch))
    expected=(out/'PRIVATE.log').stat();fd=types.SimpleNamespace(st_mode=stat.S_IFREG,st_dev=expected.st_dev,st_ino=expected.st_ino)
    fakeos=types.SimpleNamespace(name='posix',getppid=lambda:123,getsid=lambda _:222,getpid=lambda:222,getpgrp=lambda:222,
                                isatty=lambda _:False,fstat=lambda _:fd)
    claim=[]
    nslaunch={'contained':lambda p:Path(p),'strict_json':ns['strict_json'],'output_path':lambda _:out,
              'hashlib':hashlib,'json':json,'os':fakeos,'stat':stat,'datetime':datetime,'timezone':timezone,
              'utc':lambda s:datetime.fromisoformat(s),'time_guard':lambda reg:datetime(2100,1,1,tzinfo=timezone.utc),
              'Path':lambda _:types.SimpleNamespace(read_text=lambda:') '+' '.join(['0']*19+['444'])),
              'publish_new':lambda p,x:claim.append((p,x)),'sha':lambda p:hashlib.sha256(p.read_bytes()).hexdigest()}
    functions('registration_guard.py',['validate_launch'],nslaunch)
    nslaunch['validate_launch'](path,{},digest,'toy',cfg)
    check('private_descriptor_positive',len(claim)==1)
    fd.st_ino+=1
    rejects('private_descriptor_wrong_inode',lambda:nslaunch['validate_launch'](path,{},digest,'toy',cfg),ValueError)
    fd.st_ino=expected.st_ino;fakeos.getsid=lambda _:333
    rejects('not_session_leader',lambda:nslaunch['validate_launch'](path,{},digest,'toy',cfg),ValueError)
    fakeos.getsid=lambda _:222;fakeos.isatty=lambda _:True
    rejects('tty_leak_refused',lambda:nslaunch['validate_launch'](path,{},digest,'toy',cfg),ValueError)
    # Synthetic source stub; all LAL/Bilby calls below are replaced, never imported.
    lal=types.ModuleType('lal');lal.MSUN_SI=1.;lal.CreateDict=dict
    ls=types.ModuleType('lalsimulation')
    ls.SimInspiralChirpTimeBound=lambda *a:1.
    ls.SimInspiralMergeTimeBound=lambda *a:.1
    ls.SimInspiralFinalBlackHoleSpinBound=lambda *a:.7
    ls.SimInspiralRingdownTimeBound=lambda *a:.2
    for key in ['DTau220','DTau440','DOmega220','DOmega440']:
        setattr(ls,'SimInspiralWaveformParamsInsert'+key,lambda d,x:None)
    bilby=types.ModuleType('bilby');gw=types.ModuleType('bilby.gw');src=types.ModuleType('bilby.gw.source')
    calls=[]
    def toy_wave(f,*args,**kwargs):
        calls.append(kwargs);return {'plus':np.ones(len(f),complex),'cross':np.zeros(len(f),complex)}
    src.lal_binary_black_hole=toy_wave;gw.source=src;bilby.gw=gw
    saved={k:sys.modules.get(k) for k in ['lal','lalsimulation','bilby','bilby.gw','bilby.gw.source']}
    sys.modules.update({'lal':lal,'lalsimulation':ls,'bilby':bilby,'bilby.gw':gw,'bilby.gw.source':src})
    class Counter(list):
        def get_lock(self):return self
        def __enter__(self):return self
        def __exit__(self,*args):pass
    counter=Counter([0.,0.])
    nss={'np':np,'time':time,'STOP_UTC_TIMESTAMP':None,'COST_COUNTER':counter}
    functions('pseob_source.py',['validate_polarizations','pseob_frequency_domain','parameter_conversion'],nss)
    nsi={'np':np,'pseob_frequency_domain':nss['pseob_frequency_domain'],'parameter_conversion':nss['parameter_conversion']}
    functions('injection_design.py',['aligned_gr_xphm','inject_into_ifos'],nsi)
    class FakeGenerator:
        def __init__(self,**kwargs):self.kwargs=kwargs
        def frequency_domain_strain(self,parameters):
            return self.kwargs['frequency_domain_source_model'](np.array([20.,21.]),**parameters,**self.kwargs['waveform_arguments'])
    gw.WaveformGenerator=FakeGenerator
    class FakeIfo:
        def __init__(self,name):
            self.name=name;self.strain_data=types.SimpleNamespace(start_time=100.,time_within_data=lambda t:100<=t<=108)
        def time_delay_from_geocenter(self,*args):return 0.
        def get_detector_response(self,p,params):return p['plus']
        def optimal_snr_squared(self,signal):return np.vdot(signal,signal).real
        def inject_signal(self,**kwargs):pass
    test=copy.deepcopy(cfg);test.update(segment_start_GPS=100.,event_GPS=1000.,duration_s=8)
    params={k:0. for k in ns['PHYSICAL']+ns['DEFORMATIONS']}
    params.update(mass_1=30.,mass_2=25.,luminosity_distance=1000.,geocent_time=100.3)
    test['injection']={'family':'pSEOBNRv4HM_PA','noise_kind':'REAL_OFFSOURCE','target_network_optimal_SNR':2.,'parameters':params}
    test['data']={name:{'onsource_path':'SYNTHETIC','offsource_path':'SYNTHETIC','onsource_sha256':'x','offsource_sha256':'x'} for name in ['H1','L1']}
    reg={'calibration_event_ids':[test['event']], 'event_reference_GPS':{test['event']:1000.}}
    try:
        rejects('pseob_insufficient_untapered_support',lambda:nsi['inject_into_ifos']([FakeIfo('H1'),FakeIfo('L1')],test,reg),RuntimeError)
        check('pre_waveform_guard_failure_not_in_source_counter',counter[0]==0.,{'source_entries':1,'counted_LAL_calls':counter[0]})
        bad=copy.deepcopy(test);bad['event_GPS']=1001.
        rejects('forged_real_event_GPS_refused',lambda:nsi['inject_into_ifos']([FakeIfo('H1'),FakeIfo('L1')],bad,reg),ValueError)
        bad=copy.deepcopy(test);bad['segment_start_GPS']=999.
        rejects('real_event_noise_overlap_refused',lambda:nsi['inject_into_ifos']([FakeIfo('H1'),FakeIfo('L1')],bad,reg),ValueError)
        test['injection']['family']='IMRPhenomXPHM'
        accepted=nsi['inject_into_ifos']([FakeIfo('H1'),FakeIfo('L1')],test,reg)
        check('XPHM_same_insufficient_time_support_passes_mock',accepted['status']=='INJECTION_ADDED_TO_REAL_OFFSOURCE_NOISE',
              {'finding':'No XPHM inspiral/tail support guard; arrival check alone passes. Not a physical waveform truncation measurement.'})
        test['injection']['parameters']['mass_1']=1.
        accepted=nsi['inject_into_ifos']([FakeIfo('H1'),FakeIfo('L1')],test,reg)
        check('XPHM_injection_mass_outside_recovery_prior_passes_mock',accepted['parameters']['mass_1']==1.,
              {'prior_mass1_minimum':cfg['priors']['mass_1']['minimum'],'finding':'Only rescaled distance is checked against recovery priors'})
    finally:
        for key,value in saved.items():
            if value is None:sys.modules.pop(key,None)
            else:sys.modules[key]=value
    # Interval selection uses fake arrays, fake HDF handle and fake Welch; no strain file.
    fake_h5=types.ModuleType('h5py');fake_signal=types.ModuleType('scipy.signal');fake_scipy=types.ModuleType('scipy')
    class Array:
        attrs={'Xspacing':.25}
        def __len__(self):return 240
        def __getitem__(self,key):return 0. if key==() else np.ones(240)[key]
    class Handle:
        def __enter__(self):return self
        def __exit__(self,*args):pass
        def __getitem__(self,key):return Array()
    fake_h5.File=lambda *a:Handle()
    fake_signal.welch=lambda *a,**k:(np.array([0.,1.]),np.array([1.,1.]))
    saved2={k:sys.modules.get(k) for k in ['h5py','scipy','scipy.signal']}
    sys.modules.update({'h5py':fake_h5,'scipy':fake_scipy,'scipy.signal':fake_signal})
    nspsd={'np':np,'require_pin':lambda *a:None,'quality_mask':lambda *a:np.ones(60,dtype=bool)}
    functions('strain_io.py',['offsource_psd'],nspsd)
    try:
        config=dict(psd_duration_s=8,psd_segment_s=2,offsource_exclusion_s=16,event_GPS=100,segment_start_GPS=20,
                    quality_required=['A'],injection_flags_required=['B'])
        f,p,r=nspsd['offsource_psd']('NO_REAL_FILE','MOCK',config)
        check('PSD_block_ends_before_analysis',r['GPS_start']+r['duration_s']<=config['segment_start_GPS'],r)
        config['segment_start_GPS']=4
        rejects('PSD_refuses_block_crossing_analysis',lambda:nspsd['offsource_psd']('NO_REAL_FILE','MOCK',config),ValueError)
    finally:
        for key,value in saved2.items():
            if value is None:sys.modules.pop(key,None)
            else:sys.modules[key]=value
    report={'status':'INDEPENDENT_FINITE_FIXTURES_ONLY','python_optimize':sys.flags.optimize,'checks':records,
            'wall_seconds':time.perf_counter()-started,'physical_waveforms':0,'physical_PE':0,'strain_reads':0,
            'real_seed_reads':0,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    with target.open('x',encoding='utf-8') as f:json.dump(report,f,indent=2,ensure_ascii=False,allow_nan=False)
    print(json.dumps({'status':report['status'],'checks':len(records),'seconds':report['wall_seconds']}))


if __name__=='__main__':main()
