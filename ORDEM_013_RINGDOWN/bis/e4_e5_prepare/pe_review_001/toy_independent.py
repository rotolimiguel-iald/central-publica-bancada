"""Authorized finite analytic adapter audit: no LAL/GW source/strain/private seed."""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
    os.environ[key]='1'
import sys, json, hashlib, time, multiprocessing, ast
from pathlib import Path
O=Path(__file__).resolve().parent
sys.path.insert(0,str(O/'snapshot'))
import numpy as np
import bilby
from pe_runner import sampler_class, convergence

COUNTER=multiprocessing.Array('q',[0],lock=True)


class CountedToy(bilby.Likelihood):
    def __init__(self):
        super().__init__(parameters={'x':None,'y':None})
    def log_likelihood(self,parameters=None):
        with COUNTER.get_lock():COUNTER[0]+=1
        p=self.parameters if parameters is None else parameters
        return float(-.5*(p['x']**2+((p['y']-.3*p['x'])/1.2)**2))
    def noise_log_likelihood(self):return 0.


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    target=O/'toy_parallel';target.mkdir(exist_ok=False)
    started=time.perf_counter();rows=[]
    # Read the actual installed sampler code as text; no waveform imports/calls.
    import inspect
    from bilby.core.sampler.dynesty import Dynesty
    import dynesty
    primary={}
    for label,obj in [('bilby_dynesty',Dynesty),('dynesty_sampler',dynesty.NestedSampler)]:
        p=Path(inspect.getsourcefile(obj));raw=p.read_bytes()
        (target/(label+'.py.txt')).write_bytes(raw)
        primary[label]={'path':str(p),'sha256':sha(p)}
    for name,cap,expected in [('converged',12000,True),('maxcall',70,False)]:
        with COUNTER.get_lock():COUNTER[0]=0
        config={'maxcall':cap,'dlogz':.4,'minimum_effective_samples':12,'minimum_posterior_samples':12}
        bilby.core.utils.random.seed(132236);np.random.seed(132236)
        likelihood=CountedToy()
        priors=bilby.core.prior.PriorDict({k:bilby.core.prior.Uniform(-8,8,name=k) for k in ['x','y']})
        cls=sampler_class(config)
        sampler=cls(likelihood=likelihood,priors=priors,outdir=str(target/name),label=name,
                    nlive=32,maxcall=cap,dlogz=.4,seed=132236,sample='rwalk',walks=5,npool=2,
                    resume=False,check_point=False,check_point_plot=False,print_progress=False,plot=False)
        after_init=int(COUNTER[0])
        result=bilby.run_sampler(likelihood=likelihood,priors=priors,sampler=sampler,
                                outdir=str(target/name),label=name,save='hdf5',plot=False)
        state=convergence(result,config)
        if state['accepted_for_analysis'] is not expected:raise ValueError('Unexpected convergence '+str(state))
        rows.append({'case':name,'terminal':state,'actual_log_likelihood_invocations':int(COUNTER[0]),
                     'after_sampler_constructor':after_init,'actual_minus_reported':int(COUNTER[0])-state['ncall'],
                     'workers':2,'sample':'rwalk','walks':5})
    # Check Bilby parameter extraction/cache when explicit geocent_time appears in source signature.
    from bilby.gw.waveform_generator import WaveformGenerator
    fake_calls=[]
    def fake_source(frequency_array,mass_1,geocent_time=None,**kwargs):
        fake_calls.append({'mass_1':mass_1,'geocent_time':geocent_time,'analysis_time_contract':kwargs.get('analysis_time_contract')})
        return {'plus':np.ones(len(frequency_array),dtype=complex),'cross':np.zeros(len(frequency_array),dtype=complex)}
    gen=WaveformGenerator(duration=2,sampling_frequency=8,start_time=100,
          frequency_domain_source_model=fake_source,parameter_conversion=lambda p:(dict(p),[]),
          waveform_arguments={'analysis_time_contract':{'start_GPS':100,'duration_s':2,'roll_off_s':.1}})
    for t in [101.,101.,101.1]:gen.frequency_domain_strain({'mass_1':30.,'geocent_time':t})
    if [x['geocent_time'] for x in fake_calls]!=[101.,101.1]:raise ValueError('Source time extraction/cache')
    report={'status':'INDEPENDENT_FINITE_ANALYTIC_ADAPTER_ONLY','results':rows,'fake_generator_calls':fake_calls,
            'installed_primary_sources':primary,'source_snapshot_sha256':sha(O/'snapshot/pe_runner.py'),
            'script_sha256':sha(Path(__file__)),'wall_seconds':time.perf_counter()-started,
            'versions':{'bilby':bilby.__version__,'numpy':np.__version__,'dynesty':dynesty.__version__},
            'physical_waveforms':0,'physical_PE':0,'strain_reads':0,'real_blinding_seed_reads':0}
    with (target/'INDEPENDENT_TOY_RECEIPT.json').open('x') as f:json.dump(report,f,indent=2,allow_nan=False)
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
