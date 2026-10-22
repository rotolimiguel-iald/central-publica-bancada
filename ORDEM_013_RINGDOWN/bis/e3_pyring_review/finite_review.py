"""Static and synthetic Kerr review only: no strain, posterior, LAL or sampler."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[name]='1'
import ast,copy,hashlib,json,math,sys,time,types
from pathlib import Path
from datetime import datetime,timezone,timedelta
import numpy as np
from scipy.linalg import solve_triangular,toeplitz,cholesky
from scipy.interpolate import interp1d

HERE=Path(__file__).resolve().parent;S=HERE/'snapshot_001';B=HERE.parents[1]
CHECKS=[];OBS=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check(name,ok,detail=None):
    if not ok:raise RuntimeError('FAILED '+name)
    CHECKS.append(dict(name=name,passed=True,detail=detail))
def reject(name,fn,kind=(ValueError,RuntimeError)):
    try:fn()
    except kind as error:CHECKS.append(dict(name=name,passed=True,refusal=type(error).__name__))
    else:raise RuntimeError('NEGATIVE ACCEPTED '+name)
def extract(file,names,ns):
    nodes=[n for n in ast.parse((S/file).read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names]
    if {n.name for n in nodes}!=set(names):raise RuntimeError('Missing functions')
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(S/file),'exec',optimize=1),ns)
    return ns

def main():
    started=time.perf_counter();cpu=time.process_time();output=HERE/'FINITE_REVIEW_001.json'
    if output.exists():raise FileExistsError(output)
    cfg=json.loads((S/'CONFIG.json').read_text());manifest=json.loads((S/'MANIFEST.json').read_text())
    check('snapshot_source_hashes',all(sha(S/n)==h for n,h in manifest['code_sha256'].items()))
    for p in S.glob('*.py'):ast.parse(p.read_text())
    keys=('psi','Mf','af','cosiota','A2220_1','A2220_2','phi2220_1','phi2220_2')
    check('eight_exact_priors',set(cfg['priors'])==set(keys) and cfg['priors']['Mf']==[10.,500.] and cfg['priors']['af']==[0.,.99] and cfg['priors']['cosiota']==[-1.,1.])
    check('two_uniform_radii_and_phases',all(cfg['priors'][x]==[0.,50.] for x in ('A2220_1','A2220_2')) and all(cfg['priors'][x]==[0.,2*math.pi] for x in ('phi2220_1','phi2220_2')))
    check('fixed_order_and_budget',cfg['variants']==['welch','public_psd'] and sum(cfg['variant_wall_seconds'].values())==6600 and cfg['wall_envelope_seconds']==7200)
    check('819_native_samples',int(cfg['analysis_duration_s']*cfg['sample_rate_hz'])==819)
    ns=extract('kerr_model.py',['frequency_tau','polarizations','geometry','make_likelihood'],dict(np=np,PARAMETERS=keys,solve_triangular=solve_triangular))
    # Abstract dimensionless coefficients/constants only, never an astrophysical QNM evaluation.
    f,tau=ns['frequency_tau'](2.,.5,[2.,-1.,1.,1.,2.,1.],1.)
    check('frequency_tau_abstract_formula',math.isclose(f,1.5/(4*math.pi)) and math.isclose(tau,2/(math.pi*f)))
    for mass,spin in [(0.,.5),(1.,1.),(1.,-.1),(float('nan'),.5)]:reject('invalid_mass_spin_'+str((mass,spin)),lambda:ns['frequency_tau'](mass,spin,[2.,-1.,1.,1.,2.,1.],1.))
    ns['frequency_tau']=lambda *args:(1.,2.) # Synthetic oscillator, not real wave.
    tc=copy.deepcopy(cfg);tc.update(start_offset_s=.125,reference_amplitude=1.)
    x=dict(psi=.2,Mf=1.,af=.5,cosiota=.3,A2220_1=2.,A2220_2=3.,phi2220_1=.4,phi2220_2=.7)
    t=np.array([.125,.1875,.25]);u=t-.125
    def swsh(s,l,m,c):
        theta=math.acos(c);fac=math.factorial
        norm=(-1)**s*math.sqrt((2*l+1)/(4*math.pi))*math.sqrt(fac(l+m)*fac(l-m)*fac(l+s)*fac(l-s))
        return norm*sum((-1)**k*math.sin(theta/2)**(2*k+s-m)*math.cos(theta/2)**(2*l+m-s-2*k)/(fac(k)*fac(l+m-k)*fac(l-s-k)*fac(s-m+k)) for k in range(max(0,m-s),min(l+m,l-s)+1))
    for c in (-1.,-.3,0.,.7,1.):
        for m in (-2,2):
            analytic=math.sqrt(5/(64*math.pi))*(1+(1 if m==2 else -1)*c)**2
            check('SWSH_primary_sum_'+str((c,m)),math.isclose(swsh(2,2,m,c),analytic,rel_tol=1e-13,abs_tol=1e-14))
    hp,hc=ns['polarizations'](t,x,tc,1.)
    expected=np.exp(-u/2)*(swsh(2,2,2,x['cosiota'])*2*np.exp(1j*(.4+2*math.pi*u))+swsh(2,2,-2,x['cosiota'])*3*np.exp(1j*(.7-2*math.pi*u)))
    check('two_independent_branches_primary_convention',np.allclose(hp+1j*hc,expected,atol=1e-14))
    reject('negative_relative_time',lambda:ns['polarizations'](np.array([.124]),x,tc,1.))
    for c,branch in [(1.,'A2220_2'),(-1.,'A2220_1')]:
        a=dict(x,cosiota=c);p=ns['polarizations'](t,a,tc,1.);a[branch]=44.
        check('pole_suppressed_branch_'+branch,np.allclose(p,ns['polarizations'](t,a,tc,1.)))
    lal=types.ModuleType('lal');lal.G_SI=lal.MSUN_SI=lal.C_SI=1.
    seen=[]
    lal.cached_detector_by_prefix={n:types.SimpleNamespace(location=n,response=n) for n in ('H1','L1')}
    lal.LIGOTimeGPS=lambda x:x
    lal.ArrivalTimeDiff=lambda a,b,ra,dec,t:0. if a==b else .000123
    lal.GreenwichMeanSiderealTime=lambda t:seen.append(t) or t
    lal.ComputeDetAMResponse=lambda response,ra,dec,psi,gmst:response
    bilby=types.ModuleType('bilby')
    class Base:
        def __init__(self,parameters):self.parameters=parameters
    bilby.Likelihood=Base;sys.modules.update(lal=lal,bilby=bilby)
    obj,delay,gmst=ns['geometry']('L1',cfg)
    check('geometry_preserves_fractional_delay',delay==.000123 and gmst==cfg['trigger_GPS']+cfg['start_offset_s']+.000123)
    scale=.25;cov=np.array([[2.,.3,0.],[.3,1.,.2],[0.,.2,1.5]])
    physical_cov=cov*scale**2
    norm=-.5*(3*math.log(2*math.pi)+np.linalg.slogdet(physical_cov)[1])
    blocks=[dict(relative_times=t,data=np.array([1.,2.,3.]),response=(.7,-.2),gmst=0.,cholesky_scaled=cholesky(cov,lower=True),log_normalization=norm),dict(relative_times=t+.000123,data=np.array([-1.,1.,2.]),response=(-.3,.6),gmst=0.,cholesky_scaled=cholesky(cov,lower=True),log_normalization=norm)]
    tc['reference_amplitude']=scale;guard_calls=[]
    likelihood=ns['make_likelihood'](blocks,tc,lambda:guard_calls.append(1))
    # Prediction fixture returns chosen finite arrays, sharing identical parameter object.
    predictions=[]
    def pol(times,values,config,mass_time):
        predictions.append((id(values),times.copy()))
        return np.ones(3)*values['A2220_1'],np.ones(3)*values['A2220_2']
    ns['polarizations']=pol
    measured=likelihood.log_likelihood(x);independent=0.
    for b in blocks:
        resid=b['data']-b['response'][0]*x['A2220_1']-b['response'][1]*x['A2220_2']
        independent+=norm-.5*resid@np.linalg.inv(physical_cov)@resid
    check('normalized_coherent_likelihood',math.isclose(measured,independent,abs_tol=1e-12))
    check('shared_parameters_distinct_detector_times',predictions[0][0]==predictions[1][0] and not np.array_equal(predictions[0][1],predictions[1][1]))
    noise=sum(norm-.5*b['data']@np.linalg.inv(physical_cov)@b['data'] for b in blocks)
    check('noise_normalization',math.isclose(likelihood.noise_log_likelihood(),noise,abs_tol=1e-12))
    def expired():raise TimeoutError('synthetic deadline')
    timed=ns['make_likelihood'](blocks,tc,expired)
    reject('likelihood_deadline',lambda:timed.log_likelihood(x),TimeoutError)
    OBS.append(dict(name='deadline_precedes_counter_increment',observed_calls=timed.calls,scope='counts started model evaluations, excludes guard-refused entries'))
    # Mock PSD rows only; no public PSD values or strain read for this calculation.
    table=np.column_stack((np.arange(65.),np.ones(65)*2.))
    npx=types.SimpleNamespace(**{n:getattr(np,n) for n in ('isfinite','any','diff','fft')},loadtxt=lambda *a,**k:table.copy())
    psdns=extract('conditioning.py',['public_psd_acf'],dict(np=npx,interp1d=interp1d))
    pc=dict(band_hz=[20.,60.],noise_chunk_s=1.,sample_rate_hz=128.)
    acf=psdns['public_psd_acf']('SYNTHETIC',pc)
    check('one_sided_PSD_white_variance',np.isclose(acf[0],128.) and np.allclose(acf[1:],0.))
    matrix=toeplitz(acf[:9]);factor=cholesky(matrix,lower=True)
    check('Toeplitz_Cholesky_white_noise',np.allclose(factor@factor.T,np.eye(9)*128.))
    table[30,1]=-1.;reject('nonpositive_public_PSD',lambda:psdns['public_psd_acf']('SYNTHETIC',pc));table[:,1]=np.arange(65.)-19.
    table[:20,1]=1.;reject('nonpositive_extrapolation_not_clipped',lambda:psdns['public_psd_acf']('SYNTHETIC',pc));table[:,1]=2.
    # Full prepare() route uses artificial all-zero input and white covariance.
    custody=types.ModuleType('custody');custody.contained=lambda root,p:Path(p);sys.modules['custody']=custody
    npp=types.SimpleNamespace(**{n:getattr(np,n) for n in ('arange','flatnonzero','isfinite','abs','fft','log','diag','pi')},linalg=types.SimpleNamespace(cond=lambda a:1.))
    prepns=extract('conditioning.py',['prepare'],dict(np=npp,butter=lambda *a,**k:(np.array([1.]),np.array([1.])),filtfilt=lambda b,a,y:y.copy(),freqz=lambda b,a,worN,fs:(worN,np.ones(len(worN))),toeplitz=toeplitz,cholesky=cholesky,
        geometry=lambda name,c:(types.SimpleNamespace(response=name),0. if name=='H1' else .000123,0.),public_psd_acf=lambda *a:np.r_[1.,np.zeros(16383)]))
    fakecfg=copy.deepcopy(cfg);fakecfg['reference_amplitude']=1.
    helper_calls=[]
    def fake_window(*args):helper_calls.append('window');return np.zeros(32768),4096.,cfg['read_start_GPS']
    def fake_psd(*args):helper_calls.append('PSD');return np.fft.rfftfreq(16384,1/4096),np.ones(8193)/2048,dict(source='SYNTHETIC')
    for variant in ('welch','public_psd'):
        out,receipts=prepns['prepare'](fakecfg,variant,HERE,lambda:None,(fake_window,fake_psd,lambda *a:None))
        for i,b in enumerate(out):
            delay=0. if i==0 else .000123
            first=math.ceil((cfg['trigger_GPS']-cfg['read_start_GPS']+delay+cfg['start_offset_s'])*4096)
            expected_relative=(cfg['read_start_GPS']-cfg['trigger_GPS']-delay)+first/4096
            check(variant+'_native_grid_'+str(i),b['relative_times'][0]==expected_relative and len(b['data'])==819 and 0<=receipts[i]['start_grid_residual_s']<1/4096)
            check(variant+'_normalization_'+str(i),math.isclose(b['log_normalization'],-.5*819*math.log(2*math.pi),abs_tol=1e-10))
    npp.linalg.cond=lambda a:1e13
    reject('condition_number_no_jitter',lambda:prepns['prepare'](fakecfg,'welch',HERE,lambda:None,(fake_window,fake_psd,lambda *a:None)))
    # Controller execution with simulated process objects and simulated clocks only.
    scratch=HERE/'controller_mocks';scratch.mkdir()
    class Clock:
        value=1000.
        def time(self):return self.value
        def monotonic(self):return self.value-900.
        def perf_counter(self):return self.value-800.
        def sleep(self,t):self.value+=t
    def controller_case(label,returncode=0,hang=False,spawnfail=False):
        root=scratch/label;clock=Clock();children=[];cleanup_calls=[];publications={}
        cf=copy.deepcopy(cfg);cf['output_relative_to_Chatgpt']=label
        def fake_path(p):
            if str(p).startswith('/proc/'):return types.SimpleNamespace(read_text=lambda:') '+' '.join(['0']*19+['123']))
            return Path(p)
        class Child:
            pid=54321
            def __init__(self):self.returncode=None;self.polls=0
            def poll(self):
                self.polls+=1
                if not hang and self.polls>=3:self.returncode=returncode
                return self.returncode
        def popen(*a,**kw):
            if spawnfail:raise OSError('synthetic spawn failure')
            check(label+'_new_group',kw['start_new_session'] is True)
            c=Child();children.append(c);return c
        def cleanup(child):
            cleanup_calls.append(child.pid);child.returncode=child.returncode if child.returncode is not None else -15
            return dict(group_absent=True,pgid=child.pid,signals=['MOCK'])
        mod=types.ModuleType('run_controlled');mod.cleanup_group=cleanup;sys.modules['run_controlled']=mod
        class Parser:
            def add_argument(self,*a,**kw):pass
            def parse_args(self):return types.SimpleNamespace(authorization='FAKE_AUTH')
        fake_signal=types.SimpleNamespace(SIGTERM=15,SIGINT=2,signal=lambda *a:None)
        fake_os=types.SimpleNamespace(getpid=lambda:123,environ={})
        nsctrl=dict(argparse=types.SimpleNamespace(ArgumentParser=Parser),time=clock,os=fake_os,Path=fake_path,HERE=S,ROOT=scratch,
            sys=types.SimpleNamespace(executable='NO_REAL_EXECUTABLE'),subprocess=types.SimpleNamespace(Popen=popen,STDOUT=-2),signal=fake_signal,
            resource=types.SimpleNamespace(RUSAGE_CHILDREN=0,getrusage=lambda *a:types.SimpleNamespace(ru_utime=0.,ru_stime=0.)),datetime=datetime,timezone=timezone,
            verify=lambda *a:(cf,{}, {},datetime.fromtimestamp(20000,tz=timezone.utc)),contained=lambda r,p:Path(r)/p,sha=lambda *a:'MOCK',
            publish_new=lambda p,obj:publications.update({str(p.relative_to(root)):obj}))
        extract('controller.py',['main'],nsctrl)
        if spawnfail:reject(label+'_spawn_failure',nsctrl['main'],OSError)
        else:nsctrl['main']()
        cost=publications['COST.json']
        check(label+'_bounded_simulated_clock',cost['wall_seconds']<=7200)
        check(label+'_cleanup_each_owned_child',len(cleanup_calls)==len(children))
        if not spawnfail:
            check(label+'_fixed_variant_order',[a['variant'] for a in cost['runs']]==['welch','public_psd'])
            check(label+'_status',[a['status'] for a in cost['runs']]==['PARTIAL' if hang or returncode else 'COMPLETED_REQUIRES_REVIEW']*2)
        else:OBS.append(dict(name='spawn_failure_cost_has_no_explicit_failure_status',runs=cost['runs'],cleanup=cost['cleanup'],exception_propagated=True))
        return cost
    ctl={name:controller_case(name,**args) for name,args in [('completed',{}),('nonzero',dict(returncode=3)),('cutoff',dict(hang=True)),('spawn_failure',dict(spawnfail=True))]}
    # The sampled code is deliberately not an execution authorization.
    current={p.name:sha(p) for p in (B/'bis/e3_pyring_preparation').glob('*.py')}
    drift={n:dict(snapshot=h,current=current.get(n)) for n,h in manifest['code_sha256'].items() if current.get(n)!=h}
    result=dict(status='STATIC_AND_SYNTHETIC_ONLY',utc=datetime.now(timezone.utc).isoformat(),python_optimize=sys.flags.optimize,
        checks=CHECKS,observations=OBS,controller_mocks=ctl,source_sha256={p.name:sha(p) for p in S.glob('*') if p.is_file()},current_code_drift=drift,
        wall_seconds=time.perf_counter()-started,parent_cpu_seconds=time.process_time()-cpu,script_sha256=sha(__file__),
        physical_waves=0,strain_values_read=0,posterior_values_read=0,PE_runs=0,actual_process_groups_spawned=0,
        mock_scope='Arbitrary coefficients/frequency; fake LAL/Bilby; synthetic zeros/PSD; no astrophysical signal; controller clock/process simulated')
    with output.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(checks=len(CHECKS),observations=OBS,wall_seconds=result['wall_seconds'],current_code_drift=drift)))

if __name__=='__main__':main()
