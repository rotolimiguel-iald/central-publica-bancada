"""Finite mocked Bilby frontier, including fork aggregation; no PE or waveform."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import sys,multiprocessing,json,hashlib,inspect,ast,time
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;B=HERE.parents[1];CODE=B/'bis/e2_code'
sys.path.insert(0,str(CODE))
from pe_runner import counted_likelihood_class,likelihood_snapshot
from registration_guard import publish_new
from bilby.gw.likelihood import GravitationalWaveTransient as G
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
started=time.perf_counter()
source=inspect.getsource(G.log_likelihood)
if source.count('self.log_likelihood_ratio(')!=1:raise RuntimeError('Changed Bilby frontier')
original_ratio=G.log_likelihood_ratio;original_noise=G.noise_log_likelihood
counter=multiprocessing.get_context('fork').Array('d',[0.,0.,0.,0.],lock=True)
def analytic(self,parameters=None):
    if parameters.get('fail'):raise ValueError('Mock pre-generator refusal')
    return -float(parameters['x'])**2
def noise(self):return -2.
def child(obj,count):
    for j in range(count):obj.log_likelihood({'x':j})
checks=[]
try:
    G.log_likelihood_ratio=analytic;G.noise_log_likelihood=noise
    cls=counted_likelihood_class(G,counter)
    obj=object.__new__(cls)  # Deliberately bypass physical G.__init__.
    if obj.log_likelihood_ratio({'x':2.})!=-4:raise RuntimeError('Ratio value changed')
    if obj.log_likelihood({'x':2.})!=-6:raise RuntimeError('Full likelihood value changed')
    obj.noise_log_likelihood()
    if likelihood_snapshot(counter)['calls']!=2:raise RuntimeError('Nested full/ratio double count or noise counted')
    checks.append('direct_ratio_and_full_once_each_noise_excluded')
    try:obj.log_likelihood({'fail':True})
    except ValueError:pass
    else:raise RuntimeError('Exception swallowed')
    s=likelihood_snapshot(counter)
    if (s['calls'],s['completed'],s['raised'])!=(3,2,1):raise RuntimeError('Failed attempt missing')
    checks.append('pre_generator_exception_counted_and_preserved')
    children=[multiprocessing.get_context('fork').Process(target=child,args=(obj,7)) for _ in range(2)]
    for p in children:p.start()
    for p in children:
        p.join(10)
        if p.is_alive():p.kill();p.join();raise RuntimeError('Finite child timeout')
        if p.exitcode!=0:raise RuntimeError('Finite child failed')
    s=likelihood_snapshot(counter)
    if (s['calls'],s['completed'],s['raised'])!=(17,16,1):raise RuntimeError('Shared counter aggregation failed')
    checks.append('two_fork_workers_14_evaluations_aggregated')
finally:G.log_likelihood_ratio=original_ratio;G.noise_log_likelihood=original_noise
manifest=B/'bis/E2_SCIENTIFIC_RUNTIME_MANIFEST.json'
pins=json.loads(manifest.read_text())['files']
origins={}
for name in ('astropy','pandas'):
    module=__import__(name);path=Path(module.__file__).resolve()
    if not str(path).startswith('/opt/lal_env/') or pins[str(path)]['sha256']!=sha(path):raise RuntimeError('Active origin not pinned')
    origins[name]={'path':str(path),'sha256':sha(path)}
checks.append('astropy_and_pandas_active_origins_match_existing_runtime_pins')
for p in (CODE/'pe_runner.py',CODE/'registration_guard.py'):ast.parse(p.read_text())
receipt=dict(status='FINITE_MOCK_ONLY_NOT_PE',created_utc=datetime.now(timezone.utc).isoformat(),
  checks=checks,counter=s,active_origins=origins,wall_seconds=time.perf_counter()-started,
  pinned_base_log_likelihood_source=source,base_source_path=inspect.getsourcefile(G),
  sources={str(p):sha(p) for p in (Path(__file__),CODE/'pe_runner.py',CODE/'registration_guard.py',Path(inspect.getsourcefile(G)),manifest)},
  limits='Physical likelihood body mocked; real inherited full->ratio wrapper and actual fork shared counter exercised; no sampler or physical data run')
publish_new(HERE/'LIKELIHOOD_COUNTER_FINITE.json',receipt)
print(json.dumps(receipt,indent=2))
