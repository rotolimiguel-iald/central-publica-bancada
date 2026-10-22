"""Lateral package audit: bytes, portable units, pure guards; no C6 replay."""
import ast,copy,csv,hashlib,io,json,math,subprocess,sys,types,zipfile
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
R=Path(__file__).resolve().parents[2];P=R/'C7_INDEPENDENT_v3_1'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def get(p):return json.loads(p.read_bytes())
def put(p,raw):
    need(not p.exists(),'Output exists');t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(raw)
    need(t.read_bytes()==raw,'Output bytes differ');need(not p.exists(),'Output appeared');t.rename(p)
out=R/'bis/c1_review/c7_v3_results.json';need(not out.exists(),'Output exists')
inputs=['refeito/build_independent_v3_1_013bis.py','refeito/reproduce_c6_v3.py','refeito/validate_package_v3_013bis.py','refeito/verify_delivery_v3.py','refeito/package_unit_checks_v3.py','bis/C7_V3_1_BUILD.json','bis/C7_V3_BUILD.json','cache/C7_INDEPENDENT_v3_1.zip','cache/C7_INDEPENDENT_v3.zip','C1_LEITURAS_v4.json','bis/F2_ALL_READING_TABLES_v2.json','C6_ADENDO_REALIZADO_v2.json','cache/casa/RINGDOWN_DEPHASING_V2_RESULT.json']
before={n:sha(R/n) for n in inputs};manifests={};package_digests={}
for name,receiptname in [('C7_INDEPENDENT_v3_1','bis/C7_V3_1_BUILD.json'),('C7_INDEPENDENT_v3','bis/C7_V3_BUILD.json')]:
    folder=R/name;manifest=get(folder/'MANIFEST.json');receipt=get(R/receiptname)
    need(sha(folder/'MANIFEST.json')==receipt['manifest_sha256'],'Manifest receipt mismatch')
    archive=R/receipt['archive'].replace('\\','/');need(sha(archive)==receipt['archive_sha256'],'Archive receipt mismatch')
    seen=set();digests={}
    for row in manifest['files']:
        rel=PurePosixPath(row['path']);p=folder/row['path']
        need(not rel.is_absolute() and '..' not in rel.parts and '\\' not in row['path'] and row['path'] not in seen,'Unsafe/duplicate manifest')
        need(p.resolve().is_relative_to(folder.resolve()) and not p.is_symlink(),'Escaped manifest file')
        need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Manifest content mismatch')
        digests[row['path']]=sha(p);seen.add(row['path'])
    with zipfile.ZipFile(archive) as z:
        need(len(z.namelist())==len(set(z.namelist()))==len(seen)+1,'ZIP coverage')
        need(set(z.namelist())=={name+'/'+n for n in seen|{'MANIFEST.json'}},'ZIP members differ')
        for member in z.namelist():
            file=folder/member.removeprefix(name+'/')
            need(hashlib.sha256(z.read(member)).hexdigest()==sha(file),'ZIP bytes differ')
    manifests[name]=dict(files=len(seen),manifest_sha256=sha(folder/'MANIFEST.json'),archive_sha256=sha(archive),builder_sha256=manifest['builder_sha256'])
    package_digests[name]=digests
need(manifests['C7_INDEPENDENT_v3_1']['builder_sha256']==before['refeito/build_independent_v3_1_013bis.py'],'Builder link')
need((P/'reproduce_c6.py').read_bytes()==(R/'refeito/reproduce_c6_v3.py').read_bytes(),'Wrapper copy')
for dest,source in [('verify_delivery.py','verify_delivery_v3.py'),('unit_checks.py','package_unit_checks_v3.py')]:need((P/dest).read_bytes()==(R/'refeito'/source).read_bytes(),'Helper copy')
differences=[n for n,h in package_digests['C7_INDEPENDENT_v3_1'].items() if package_digests['C7_INDEPENDENT_v3'].get(n)!=h]
for n,h in package_digests['C7_INDEPENDENT_v3_1'].items():
    if n.startswith('reproduction/'):
        need(h==package_digests['C7_INDEPENDENT_v3'][n],'Frozen reproduction changed')
        need('C6_STRAIN_' not in n and not n.endswith('/C6_RESULTS.json'),'Saved result in reproduction')
fixture=get(P/'fixtures/legacy_per_series_2.json');full=get(R/'cache/casa/RINGDOWN_DEPHASING_V2_RESULT.json')
need(fixture['value']==full['per_series'][2] and fixture['source_sha256']==before['cache/casa/RINGDOWN_DEPHASING_V2_RESULT.json'],'Legacy fixture differs')
for n,h in package_digests['C7_INDEPENDENT_v3_1'].items():
    if n.startswith('current_evidence/'):
        base=Path(n).name;candidates=[R/base,R/'bis'/base]
        need(any(p.is_file() and sha(p)==h for p in candidates),'Current evidence differs '+n)
scope=get(P/'tables/reading_scope.json');c1=get(R/'C1_LEITURAS_v4.json');c4=get(R/'bis/F2_ALL_READING_TABLES_v2.json');c6=get(R/'C6_ADENDO_REALIZADO_v2.json')
need(len(scope['rows'])==60 and len({(r['dataset'],r['reading']) for r in scope['rows']})==60,'Scope coverage')
for n,h in scope['sources'].items():need(sha(R/n)==h,'Scope source hash')
lookup={(r['dataset'],r['reading']):r for r in c4['rows']}
for row in scope['rows']:
    original=lookup[row['dataset'],row['reading']]
    need({k:row[k] for k in original}==original,'Table transport changed')
    defn=next(r for r in c1['rows'] if r['reading']==row['reading'])
    need(row['C1_scope']==defn['canonical_scope'],'C1 scope differs')
    need(json.loads(row['EXCLUDED_IF_UNIVERSAL'])=={k:v for k,v in defn.items() if k.startswith('excluded_if_universal')},'Universal flags changed')
    need(row['C6_pre_lnB']==next(r['lnB_220plus440'] for r in c6['rows'] if r['reading']==row['reading']),'C6-pre transport changed')
with (P/'tables/reading_scope.csv').open(encoding='utf-8',newline='') as f:csvrows=list(csv.DictReader(f))
need(len(csvrows)==60,'Scope CSV rows')
for row,source in zip(csvrows,scope['rows']):
    for key,value in row.items():need(value==('' if source.get(key) is None else str(source[key])),'Scope CSV differs')
readme=(P/'README.md').read_text(encoding='utf-8');need((P/'README.md').read_bytes()==(P/'OVERVIEW.md').read_bytes(),'Overview differs')
prediction_ast=ast.parse((P/'tgl_ringdown_prediction.py').read_text(encoding='utf-8'))
scope_literals=[n.value.value for n in ast.walk(prediction_ast) if isinstance(n,ast.Assign) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str) and any(isinstance(t,ast.Name) and t.id=='scope' for t in n.targets) and 'management hypothesis' in n.value.value]
need(len(scope_literals)==1,'R-MOD scope not assigned at runtime')
exact='CONJECTURE \u2014 management hypothesis, not TGL canon'
encoding=dict(expected=exact,actual_scope=scope_literals[0],exact_in_runtime=exact in scope_literals[0],exact_in_readme=exact in readme,exact_in_overview=exact in (P/'OVERVIEW.md').read_text(encoding='utf-8'),exact_in_all_six_MOD_rows=all(exact in r['reading_status'] for r in scope['rows'] if r['reading']=='R-MOD'),actual_prefix_codepoints=[f'U+{ord(c):04X}' for c in scope_literals[0][:22]])
need(all(s in scope_literals[0] for s in ['CONJECTURE','management hypothesis, not TGL canon','Kerr state','laboratory partition','OPEN']),'Semantic scope missing')
# Read-only package tests; never invoke reproduce_c6 --run or validate_package.
unit=subprocess.run([sys.executable,'-B','-O','unit_checks.py'],cwd=P,capture_output=True,text=True)
need(unit.returncode==0,'Package unit tests fail: '+unit.stderr)
unitresult=json.loads(unit.stdout.strip());need(unitresult['status']=='PASS','Unit result')
# Isolate the numeric/status guards, not main or subprocess execution.
wrapper_tree=ast.parse((P/'reproduce_c6.py').read_text(encoding='utf-8'))
permit=next(n for n in wrapper_tree.body if isinstance(n,ast.FunctionDef) and n.name=='permit_status')
env={};exec(compile(ast.fix_missing_locations(ast.Module(body=[permit],type_ignores=[])),'permit_status','exec',optimize=1),env)
status_checks={s:env['permit_status'](s) for s in ['INCONCLUSIVE_SYSTEMATICS','INCONCLUSIVE_DENSITY_SUPPORT','AWAITING_DATA','NOT_VERIFIED','INPUT_INTEGRITY_FAILED','CONFIRMED','EXCLUDED_IN_READING','PASS','']}
main=next(n for n in wrapper_tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');tr=next(n for n in main.body if isinstance(n,ast.Try))
start=next(i for i,n in enumerate(tr.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='key' for t in n.targets))
end=next(i for i,n in enumerate(tr.body) if i>start and isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='report' for t in n.targets))
guard=compile(ast.fix_missing_locations(ast.Module(body=tr.body[start:end],type_ignores=[])),'wrapper_numeric_guard','exec',optimize=1)
reference=get(P/'evidence/C6_RESULTS.json');cases=[]
for name in ['intact','downgrade','promotion','NaN_second_row','missing_row','duplicate_row','finite_mismatch']:
    actual=copy.deepcopy(reference)
    if name=='downgrade':actual['status']='NOT_VERIFIED'
    elif name=='promotion':actual['status']='CONFIRMED'
    elif name=='NaN_second_row':actual['results'][1]['lnB_vs_GR']=float('nan')
    elif name=='missing_row':actual['results'].pop()
    elif name=='duplicate_row':actual['results'].append(copy.deepcopy(actual['results'][0]))
    elif name=='finite_mismatch':actual['results'][1]['lnB_vs_GR']+=.1
    local=dict(reference=reference,actual=actual,permit_status=env['permit_status'])
    try:exec(guard,local);accepted=True;error=None
    except ValueError as exc:accepted=False;error=str(exc)
    cases.append(dict(case=name,accepted=accepted,error=error,max_error=local.get('error'),strict_JSON_report_possible=accepted and math.isfinite(local['error'])))
need(next(c for c in cases if c['case']=='NaN_second_row')['accepted'],'NaN probe no longer reproduces')
# Mock only the validator preflight path; no real directory creation/deletion.
vt=ast.parse((R/'refeito/validate_package_v3_013bis.py').read_text(encoding='utf-8'));vm=next(n for n in vt.body if isinstance(n,ast.FunctionDef) and n.name=='main')
created=[];removed=[]
class FakePath:
    def __init__(self,value):self.value=str(value)
    def __truediv__(self,name):return FakePath(self.value+'/'+str(name))
    def resolve(self):return self
    def is_relative_to(self,other):return self.value.startswith(other.value+'/')
    def exists(self):return self.value.endswith('/bis/C7_V3_1_CLEAN_VALIDATION.json')
    def __eq__(self,other):return isinstance(other,FakePath) and self.value==other.value
    def __str__(self):return self.value
def mkdtemp(prefix,dir):
    result=str(dir)+'/'+prefix+'simulated';created.append(result);return result
fake=dict(B=FakePath('/workspace'),Path=FakePath,tempfile=types.SimpleNamespace(mkdtemp=mkdtemp),shutil=types.SimpleNamespace(rmtree=lambda p:removed.append(str(p))))
exec(compile(ast.fix_missing_locations(ast.Module(body=[vm],type_ignores=[])),'validator_main_fake_preflight','exec',optimize=1),fake)
try:fake['main']();failure=None
except FileExistsError as exc:failure=type(exc).__name__
cleanup_probe=dict(case='Existing validation receipt before try',failure=failure,created=created,removed=removed,leaked_simulated_directory=bool(created) and not removed)
need(cleanup_probe['leaked_simulated_directory'],'Cleanup probe no longer reproduces')
need(before=={n:sha(R/n) for n in before},'Audited inputs changed')
for name,entries in package_digests.items():need(entries=={n:sha(R/name/n) for n in entries},'Package changed during audit')
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='C7_LATERAL_REVIEW_WITH_FINDINGS__NO_C6_REPLAY',input_hashes=before,script_sha256=sha(Path(__file__)),manifests=manifests,v3_to_v3_1_changed_files=differences,table_rows=60,fixture_verified=True,unit_result=unitresult,MOD_encoding=encoding,status_controls=status_checks,numeric_guard_probes=cases,cleanup_probe=cleanup_probe,no_C6_replay=True,inputs_unchanged=True)
put(out,(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
print(json.dumps({k:result[k] for k in ['status','manifests','v3_to_v3_1_changed_files','unit_result','MOD_encoding','numeric_guard_probes','cleanup_probe']},indent=2,ensure_ascii=False))
