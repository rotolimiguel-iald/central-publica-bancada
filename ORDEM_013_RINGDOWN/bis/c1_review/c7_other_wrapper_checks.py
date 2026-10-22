"""Read-only asset/receipt checks and fully mocked legacy wrapper; no C5 execution."""
from pathlib import Path, PurePosixPath
from types import SimpleNamespace
from datetime import datetime, timezone
import ast, hashlib, io, json, zipfile
B=Path(__file__).resolve().parents[2]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def get(p):return json.loads(p.read_bytes())
wrapper=B/'refeito/replay_legacy_in_temporary_v3.py'
tree=ast.parse(wrapper.read_text(encoding='utf-8'))
main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
code=compile(ast.fix_missing_locations(ast.Module(body=[main],type_ignores=[])),'generic_wrapper_mock','exec',optimize=1)
cases=[]
for case in ['verify_only','prepare','mock_run_zero','mock_run_failure','copy_failure','internal_work','internal_output','output_mkdir_failure']:
    events=[];active=set();written={}
    class FakeStream(io.BytesIO):
        def __init__(self,path):super().__init__();self.path=path
        def close(self):
            if not self.closed:written[str(self.path)]=self.getvalue()
            super().close()
    class FakePath:
        def __init__(self,value):self.v=value.v if isinstance(value,FakePath) else PurePosixPath(str(value))
        def __str__(self):return str(self.v)
        def __truediv__(self,n):return FakePath(self.v/str(n))
        def __eq__(self,o):return isinstance(o,FakePath) and self.v==o.v
        def resolve(self):return self
        def is_relative_to(self,o):return self.v.is_relative_to(o.v)
        def relative_to(self,o):return self.v.relative_to(o.v)
        def is_symlink(self):return False
        def exists(self):return str(self) in active
        @property
        def name(self):return self.v.name
        @property
        def parent(self):return FakePath(self.v.parent)
        def read_bytes(self):return json.dumps({'files':[{'path':'asset.py','sha256':'MOCK_PIN'}]}).encode()
        def mkdir(self,**kw):
            events.append(['mkdir',str(self)])
            if case=='output_mkdir_failure' and self.name.startswith('package_'):raise PermissionError('Mock output failure')
        def open(self,mode):events.append(['open',str(self),mode]);return FakeStream(self)
        def rglob(self,pattern):return []
    args=SimpleNamespace(run=case.startswith('mock_run'),prepare_only=case not in ('verify_only','mock_run_zero','mock_run_failure'),
          work_root=FakePath('/package/new' if case=='internal_work' else '/work'),
          output_root=FakePath('/package/new' if case=='internal_output' else '/output'))
    class Parser:
        def __init__(self,**kw):pass
        def add_argument(self,*a,**kw):pass
        def parse_args(self):return args
        def error(self,message):raise ValueError(message)
    def mkdtemp(prefix,dir):
        path=dir/(prefix+'fake');active.add(str(path));events.append(['mkdtemp',str(path)]);return str(path)
    def copyfile(source,target):
        events.append(['copyfile',str(source),str(target)])
        need(target.is_relative_to(FakePath('/work/legacy_replay_fake')),'Mock copy escaped temporary')
        if case=='copy_failure':raise PermissionError('Mock asset copy failure')
    def rmtree(path):
        need(str(path)=='/work/legacy_replay_fake','Mock deletion escaped child')
        events.append(['rmtree',str(path)]);active.remove(str(path))
    def run(command,**kwargs):
        need(command==['MOCK_PYTHON','-B','/work/legacy_replay_fake/reproduce_legacy.py'],'Wrong mock execution target')
        need(str(kwargs['cwd'])=='/work/legacy_replay_fake','Wrong mock working directory')
        events.append(['simulated_subprocess',command]);return SimpleNamespace(returncode=1 if case=='mock_run_failure' else 0)
    env=dict(__doc__='mock',Path=FakePath,PurePosixPath=PurePosixPath,ROOT=FakePath('/package'),json=json,
        argparse=SimpleNamespace(ArgumentParser=Parser),sha=lambda p:'MOCK_PIN',datetime=datetime,timezone=timezone,
        tempfile=SimpleNamespace(mkdtemp=mkdtemp),shutil=SimpleNamespace(copyfile=copyfile,rmtree=rmtree),
        os=SimpleNamespace(environ={}),subprocess=SimpleNamespace(run=run,STDOUT='MOCK_STDOUT'),sys=SimpleNamespace(executable='MOCK_PYTHON'),
        print=lambda *a,**kw:None)
    exec(code,env);error=None
    try:env['main']()
    except Exception as exc:error=type(exc).__name__+': '+str(exc)
    need(not active,'Mock temporary leaked')
    runs=[e for e in events if e[0]=='simulated_subprocess']
    need(len(runs)==(1 if case.startswith('mock_run') else 0),'Unexpected mock computation: '+case+' '+str(error))
    if case in ('internal_work','internal_output'):
        need(error and error.startswith('ValueError') and not events,'Internal roots mutated before refusal')
    elif case=='output_mkdir_failure':
        need(error and error.startswith('PermissionError') and not any(e[0]=='mkdtemp' for e in events),'Output failure leaked temporary')
    elif case in ('copy_failure','mock_run_failure'):
        need(error is not None and any(e[0]=='rmtree' for e in events),'Failure not cleaned/propagated')
    else:need(error is None,'Unexpected mock failure')
    reports={n:json.loads(raw) for n,raw in written.items() if n.endswith('/RECEIPT.json')}
    for report in reports.values():need(report['temporary_removed'] is True and report['scientific_calibration'] is False,'Bad mock report')
    cases.append(dict(case=case,error=error,events=events,receipts=reports))

build=get(B/'bis/C7_OTHER_V3_BUILD.json');need(build['builder_sha256']==sha(B/'refeito/build_other_packages_v3_013bis.py'),'Other builder pin')
rows=[]
for r in build['packages']:
    root=B/r['package'];old=B/r['package'].removesuffix('_v3');m=get(root/'MANIFEST.json');om=get(old/'MANIFEST.json')
    need(sha(root/'MANIFEST.json')==r['manifest_sha256'] and sha(B/r['archive'])==r['archive_sha256'],'Build receipt mismatch')
    need(m['supersedes_manifest_sha256']==sha(old/'MANIFEST.json'),'Old manifest link')
    names=set()
    for row in m['files']:
        p=root/row['path'];need(row['path'] not in names and p.resolve().is_relative_to(root.resolve()),'Invalid file path')
        need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Manifest mismatch');names.add(row['path'])
    unchanged=0
    for row in om['files']:
        need(sha(old/row['path'])==row['sha256'],'Old asset changed')
        target={'reproduce.py':'reproduce_legacy.py','README.md':'historical_README.md'}.get(row['path'],row['path'])
        need((root/target).read_bytes()==(old/row['path']).read_bytes(),'Legacy bytes changed');unchanged+=1
    need((root/'reproduce.py').read_bytes()==wrapper.read_bytes(),'Generic wrapper differs')
    with zipfile.ZipFile(B/r['archive']) as z:
        want={root.name+'/'+n for n in names|{'MANIFEST.json'}}
        need(set(z.namelist())==want and len(z.namelist())==len(want),'New ZIP members')
        for n in names|{'MANIFEST.json'}:need(z.read(root.name+'/'+n)==(root/n).read_bytes(),'New ZIP bytes')
    old_zip=B/'cache'/(old.name+'_v1.zip')
    with zipfile.ZipFile(old_zip) as z:
        prefix=old.name+'/' if old.name+'/MANIFEST.json' in z.namelist() else ''
        for row in om['files']:need(z.read(prefix+row['path'])==(old/row['path']).read_bytes(),'Old ZIP file differs')
        need(z.read(prefix+'MANIFEST.json')==(old/'MANIFEST.json').read_bytes(),'Old ZIP manifest differs')
    preparation=r['preparation'];temp=Path(preparation['temporary']).resolve();cache=(B/'cache').resolve()
    need(preparation['status']=='PREPARATION_VERIFIED_NO_COMPUTATION' and preparation['scientific_calibration'] is False,'Unexpected preparation claim')
    need(preparation['temporary_removed'] is True and not temp.exists() and temp.is_relative_to(cache) and temp!=cache,'Preparation cleanup mismatch')
    receipts=list((B/'bis/legacy_prepare_v3').glob(root.name+'_*/RECEIPT.json'))
    need(len(receipts)==1 and get(receipts[0])==preparation,'Actual preparation receipt mismatch')
    rows.append(dict(package=root.name,manifest_files=len(names),old_files_preserved=unchanged,manifest_sha256=sha(root/'MANIFEST.json'),
        archive_sha256=sha(B/r['archive']),old_archive_sha256=sha(old_zip),wrapper_sha256=sha(root/'reproduce.py'),
        legacy_script_sha256=sha(root/'reproduce_legacy.py'),receipt_sha256=sha(receipts[0]),temporary_absent=True))
result=dict(status='PASS_SCOPED_EXECUTION_AND_CLEANUP_DESIGN_CHECKS',utc=datetime.now(timezone.utc).isoformat(),
    scope='Fully mocked main plus read-only byte/receipt checks; no actual wrapper subprocess or scientific run',
    wrapper_sha256=sha(wrapper),builder_sha256=build['builder_sha256'],build_receipt_sha256=sha(B/'bis/C7_OTHER_V3_BUILD.json'),
    script_sha256=sha(Path(__file__)),packages=rows,mock_cases=cases)
out=Path(__file__).with_name('c7_other_wrapper_results.json');raw=(json.dumps(result,indent=2,ensure_ascii=False)+'\n').encode()
with out.open('xb') as f:f.write(raw)
need(out.read_bytes()==raw,'Output mismatch')
print(json.dumps(dict(status=result['status'],packages=[dict(package=r['package'],manifest_files=r['manifest_files']) for r in rows],mock_cases=len(cases))))
