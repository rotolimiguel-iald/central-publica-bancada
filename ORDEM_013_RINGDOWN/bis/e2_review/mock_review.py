"""Finite AST-extracted tests; no production imports, PE, waveforms or strain."""
import ast
import contextlib
import datetime
import hashlib
import io
import json
import math
from pathlib import Path
import signal
import sys
import types
from unittest.mock import patch
import numpy as np

HERE = Path(__file__).resolve().parent
SNAPSHOT = HERE / 'snapshot_001'
results = []


def function(filename, name, namespace):
    tree = ast.parse((SNAPSHOT/filename).read_text())
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(SNAPSHOT/filename), 'exec'), namespace)
    return namespace[name]


def record(name, demonstrated, detail):
    if not demonstrated:
        raise RuntimeError('Mock did not reproduce claimed finding: ' + name)
    results.append(dict(name=name, reproduced=True, detail=detail))


def source_tests():
    dictionaries = []
    lal = types.ModuleType('lal')
    def create_dict():
        item = {}; dictionaries.append(item); return item
    lal.CreateDict = create_dict
    ls = types.ModuleType('lalsimulation')
    for name in ('DTau220', 'DTau440', 'DOmega220', 'DOmega440'):
        setattr(ls, 'SimInspiralWaveformParamsInsert'+name, lambda d, v, key=name: d.update({key:v}))
    target = types.ModuleType('bilby.gw.source')
    source = function('pseob_source.py', 'pseob_frequency_domain', {'np': np})
    args = (np.array([0., 10., 20.]), 40., 30., 100., .2, -.3, .4, .5, .1, .2)
    with patch.dict(sys.modules, {'lal':lal, 'lalsimulation':ls, 'bilby.gw.source':target}):
        zero = {'plus':np.zeros(3), 'cross':np.zeros(3)}
        target.lal_binary_black_hole = lambda *a, **k: zero
        record('ZERO_WAVEFORM_ACCEPTED', source(*args) is zero,
               'Both fake polarizations zero pass wrapper without rejection')
        nonfinite = {'plus':np.array([0., np.nan, 0.]), 'cross':np.zeros(3)}
        target.lal_binary_black_hole = lambda *a, **k: nonfinite
        record('NONFINITE_WAVEFORM_ACCEPTED', source(*args) is nonfinite,
               'Fake nonfinite polarization passes wrapper unchanged')
        target.lal_binary_black_hole = lambda *a, **k: None
        record('NONE_PROPAGATED_EXPECTED', source(*args) is None,
               'None propagation is valid Bilby likelihood behavior, not a bug')
        record('FRESH_DICTIONARY_OK', len({id(x) for x in dictionaries}) == 3,
               'Three calls created distinct dictionaries; four deformation setters used')


def strain_tests():
    class Raw:
        attrs = {'Xspacing': .25}
        def __len__(self): return 8
        def __getitem__(self, key): return np.arange(8, dtype=float)[key]
    class Value:
        def __getitem__(self, key): return 100.
    class Handle(dict):
        def __enter__(self): return self
        def __exit__(self, *args): return False
    fake_h5 = types.ModuleType('h5py')
    fake_h5.File = lambda *a: Handle({'strain/Strain':Raw(), 'meta/GPSstart':Value()})
    window = function('strain_io.py', 'window', {'np':np, 'require_pin':lambda *a:None,
        'quality_mask':lambda *a:np.array([True, True])})
    with patch.dict(sys.modules, {'h5py':fake_h5}):
        _, _, actual = window('MOCK', 'MOCK', 100.1, .5, ['GOOD'], ['NO_INJ'])
    record('FRACTIONAL_START_SILENTLY_ROUNDED', actual != 100.1,
           dict(requested_start=100.1, returned_start=actual, sample_rate=4))
    class Dataset:
        def __init__(self, values): self.values = values
        def __getitem__(self, item): return self.values
    quality = function('strain_io.py', 'quality_mask', {})
    handle = {group+'/'+field:Dataset(value) for group, field, value in [
        ('quality/simple','DQShortnames',[b'GOOD']),
        ('quality/simple','DQmask',np.zeros(2,dtype=int)),
        ('quality/injections','InjShortnames',[b'NO_INJ']),
        ('quality/injections','Injmask',np.zeros(2,dtype=int))]}
    record('EMPTY_DQ_REQUIREMENTS_PASS_BAD_FLAGS', bool(quality(handle, [], []).all()),
           'No flags requested causes all bad flags to pass; registration must forbid empty lists')


def controller_test():
    calls = []
    class DummyFile:
        def __enter__(self): return io.StringIO()
        def __exit__(self, *args): return False
    class DummyPath:
        def exists(self): return False
        def open(self, *a, **kw): return DummyFile()
        def stat(self): return types.SimpleNamespace(st_size=0)
    class Child:
        pid = 12345; returncode = None
        def poll(self): return self.returncode
        def wait(self, timeout=None): self.returncode=0; return 0
    child = Child()
    # SIGTERM makes the leader exit; mocked worker remains alive indefinitely.
    def killpg(pid, sig): calls.append((pid, sig)); child.returncode=0
    fake_os = types.SimpleNamespace(name='posix', environ={}, killpg=killpg)
    times = iter([0., 2., 3., 4.])
    fake_time = types.SimpleNamespace(time=lambda:next(times), sleep=lambda n:None)
    cfg={'sampler':{'workers':1}, 'output_directory_name':'mock', 'wall_budget_seconds':1,
         'mode':'blind_test'}
    fake_resource=types.SimpleNamespace(RUSAGE_CHILDREN=1,
        getrusage=lambda _:types.SimpleNamespace(ru_utime=0.,ru_stime=0.))
    import argparse
    namespace=dict(argparse=argparse, os=fake_os, time=fake_time, signal=signal,
        subprocess=types.SimpleNamespace(Popen=lambda *a,**kw:child, TimeoutExpired=TimeoutError, STDOUT=-2),
        resource=fake_resource, sys=sys, Path=Path, __file__=str(SNAPSHOT/'run_controlled.py'),
        checked_registration=lambda:({'pe_jobs':{'mock':cfg}}, 'MOCK_NOT_REAL_HASH'),
        time_guard=lambda _:types.SimpleNamespace(timestamp=lambda:100.),
        output_path=lambda _:DummyPath(), sha=lambda _:'MOCK_NOT_REAL_HASH',
        datetime=datetime.datetime, timezone=datetime.timezone, json=json)
    main=function('run_controlled.py','main',namespace)
    with patch.object(sys,'argv',['mock','--job','mock']), contextlib.redirect_stdout(io.StringIO()):
        main()
    record('LEADER_EXIT_LEAVES_WORKER_UNCHECKED', calls==[(12345,signal.SIGTERM)],
           'No group-existence probe or SIGKILL after leader returns; no real process launched')


def finite_guard_tests():
    fn=function('blinding.py','unblinding_allowed',{'np':np})
    receipt={'status':'REGISTERED_UNBLINDING_GATE_MET','independent_review_passed':True}
    reg={'blinding':{'minimum_information_to_unblind':float('nan')}}
    record('NAN_INFORMATION_THRESHOLD_ACCEPTED', fn(reg,1.,True,receipt) is True,
           'Registered threshold not checked finite; no seed accessed')
    fn=function('synthetic_null.py','simulate_projection',{'np':np})
    ticks=[]
    def stop():
        ticks.append(1)
        if len(ticks)==3: raise RuntimeError('MOCK_LOOP_BOUNDED')
    try: fn({'noise_variance_fraction':1.,'nuisance_variance_fraction':0.},1,7,'gaussian',stop,chunk=0)
    except RuntimeError as error:
        record('ZERO_CHUNK_NO_PROGRESS', str(error)=='MOCK_LOOP_BOUNDED',
               'Three zero-length chunks with no progress; finite mock cutoff, no MC campaign')
    else: raise RuntimeError('Expected zero-chunk failure')


if __name__ == '__main__':
    source_tests();strain_tests();controller_test();finite_guard_tests()
    report=dict(status='FINITE_MOCK_REPRODUCTIONS_NOT_PE_VALIDATION',
        utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), tests=results,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        snapshots={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in SNAPSHOT.glob('*.py')},
        real_waveform_calls=0, real_strain_files_opened=0, pe_calls=0, secret_bytes_read=0,
        real_processes_spawned=0, numpy_version=np.__version__)
    with (HERE/'MOCK_RESULTS_001.json').open('x',encoding='utf-8') as f:
        json.dump(report,f,indent=2,allow_nan=False)
    print(json.dumps(report,indent=2))
