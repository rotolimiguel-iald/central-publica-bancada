"""Run the native helper ONLY after rebasing a verified copy to an explicit fixture."""
from pathlib import Path
import importlib.util,sys,json,hashlib
D=Path(__file__).resolve().parent/'t13'
FIXTURE=D/'ACL_CLEANUP_TEST_001'
if len(sys.argv)!=2 or Path(sys.argv[1]).resolve()!=FIXTURE.resolve():raise ValueError('Exact fixture required')
FIXTURE.resolve().relative_to(D.resolve())
p=D/'sources/e2_private_directory_native.py'
m=json.loads((D/'FIXTURE_SOURCE_MANIFEST.json').read_bytes())
if hashlib.sha256(p.read_bytes()).hexdigest()!=m['helper_copy_sha256']:raise ValueError('Copy changed')
s=importlib.util.spec_from_file_location('fixture_helper_015',p);helper=importlib.util.module_from_spec(s);s.loader.exec_module(helper)
helper.B=FIXTURE
(FIXTURE/'cache').mkdir(parents=True)
print(json.dumps(helper.operate('Prepare')))
print(json.dumps(helper.operate('Verify')))
raise RuntimeError('T13_INJECTED_FAILURE_AFTER_NATIVE_ACL_CREATION')
