"""Authorized deterministic analytic plumbing toy; no physical PE or waveform."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
import sys,json,hashlib,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'e2_code'))
import bilby
import numpy as np
from pe_runner import sampler_class,convergence


class ToyLikelihood(bilby.Likelihood):
    def __init__(self):super().__init__(parameters={'x':None})
    def log_likelihood(self,parameters=None):
        parameters=self.parameters if parameters is None else parameters
        return float(-.5*parameters['x']**2)
    def noise_log_likelihood(self):return 0.


def main():
    root=HERE/'toy_adaptor_002';root.mkdir(exist_ok=False)
    started=time.perf_counter();results=[]
    for label,cap,expected in [('converged',6000,True),('maxcall',50,False)]:
        settings=dict(maxcall=cap,dlogz=.3,minimum_effective_samples=10,minimum_posterior_samples=10)
        priors=bilby.core.prior.PriorDict(dict(x=bilby.core.prior.Uniform(-10,10,name='x')))
        likelihood=ToyLikelihood();bilby.core.utils.random.seed(20260922);np.random.seed(20260922)
        cls=sampler_class(settings)
        sampler=cls(likelihood=likelihood,priors=priors,outdir=str(root/label),label=label,
          nlive=32,maxcall=cap,dlogz=.3,seed=20260922,sample='unif',npool=1,
          resume=False,check_point=False,check_point_plot=False,print_progress=False,plot=False)
        result=bilby.run_sampler(likelihood=likelihood,priors=priors,sampler=sampler,
          outdir=str(root/label),label=label,plot=False,save='hdf5')
        state=convergence(result,settings)
        if state['accepted_for_analysis']!=expected:raise RuntimeError('Unexpected toy verdict '+str(state))
        if not state.get('before_add_live'):raise RuntimeError('No pre-live capture')
        if not expected and state['status']!='PARTIAL_MAXCALL_NOT_ACCEPTED':raise RuntimeError('Maxcall not distinguished')
        results.append(dict(case=label,terminal=state))
    report=dict(status='ANALYTIC_TOY_PLUMBING_NOT_PHYSICAL_PE',results=results,wall_seconds=time.perf_counter()-started,
      source_sha256=hashlib.sha256((HERE.parent/'e2_code/pe_runner.py').read_bytes()).hexdigest(),
      script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),bilby_version=bilby.__version__,
      physical_waveforms=0,physical_strain_reads=0,real_blinding_seeds=0)
    with (root/'TOY_RECEIPT.json').open('x') as f:json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
