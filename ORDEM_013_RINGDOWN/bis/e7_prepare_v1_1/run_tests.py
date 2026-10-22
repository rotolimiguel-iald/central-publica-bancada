"""Run inherited regressions with explicit module origins and captured receipts."""
from pathlib import Path
import sys, unittest, argparse, json, hashlib,time,os
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--legacy',action='store_true');a=ap.parse_args()
producer=D.parent/'e7_prepare/producer' if a.legacy else D/'producer'
testdir=D/'legacy_tests' if a.legacy else D/'tests'
sys.path.insert(0,str(producer))
import tgl_ringdown_ampliacao,extrai_posteriores_pseob
assert Path(tgl_ringdown_ampliacao.__file__).resolve().parent==producer.resolve()
start=time.perf_counter();cpu=time.process_time()
suite=unittest.defaultTestLoader.discover(str(testdir),pattern='test*.py')
result=unittest.TextTestRunner(verbosity=2).run(suite)
print(json.dumps(dict(tests=result.testsRun,skipped=len(result.skipped),failures=len(result.failures),
    errors=len(result.errors),success=result.wasSuccessful(),cpu_seconds=time.process_time()-cpu,
    wall_seconds=time.perf_counter()-start,producer=str(producer))))
sys.exit(0 if result.wasSuccessful() else 1)
