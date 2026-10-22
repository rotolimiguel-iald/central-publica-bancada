"""Close C7 findings using bytes, units and mocked guards; never execute C6."""
from pathlib import Path, PurePosixPath
from types import SimpleNamespace
from datetime import datetime, timezone
import ast, copy, csv, hashlib, json, math, subprocess, sys, zipfile

B=Path(__file__).resolve().parents[2]
P=B/'C7_INDEPENDENT_v3_2'
OUT=Path(__file__).with_name('c7_v3_2_closing_results.json')
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def get(p):return json.loads(p.read_bytes())
def node_code(nodes,label):return compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),label,'exec',optimize=1)

manifest=get(P/'MANIFEST.json');receipt=get(B/'bis/C7_V3_2_BUILD.json')
pins={r['path']:r['sha256'] for r in manifest['files']}
need(len(pins)==len(manifest['files']),'Duplicate manifest path')
need(sha(P/'MANIFEST.json')==receipt['manifest_sha256'],'Manifest receipt')
need(sha(B/receipt['archive'])==receipt['archive_sha256'],'ZIP receipt')
need(sha(B/'refeito/build_independent_v3_2_013bis.py')==manifest['builder_sha256'],'Builder pin')
for row in manifest['files']:
    p=P/row['path']
    need(p.resolve().is_relative_to(P.resolve()) and not p.is_symlink(),'Escaped manifest path')
    need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Manifest file mismatch')
with zipfile.ZipFile(B/receipt['archive']) as z:
    wanted={P.name+'/'+n for n in set(pins)|{'MANIFEST.json'}}
    need(set(z.namelist())==wanted and len(z.namelist())==len(wanted),'ZIP members')
    for n in set(pins)|{'MANIFEST.json'}:need(z.read(P.name+'/'+n)==(P/n).read_bytes(),'ZIP content')
old=B/'C7_INDEPENDENT_v3_1';old_manifest=get(old/'MANIFEST.json');old_receipt=get(B/'bis/C7_V3_1_BUILD.json')
need(sha(old/'MANIFEST.json')==old_receipt['manifest_sha256'] and sha(B/old_receipt['archive'])==old_receipt['archive_sha256'],'Old pins changed')
for row in old_manifest['files']:
    need(sha(old/row['path'])==row['sha256'],'Old package file changed')
    if row['path'].startswith('reproduction/'):
        need(pins[row['path']]==row['sha256'],'Frozen scientific bytes changed')
need((P/'reproduce_c6.py').read_bytes()==(B/'refeito/reproduce_c6_v3_2.py').read_bytes(),'Wrapper builder copy')
need((P/'unit_checks.py').read_bytes()==(B/'refeito/package_unit_checks_v3_2.py').read_bytes(),'Unit builder copy')
unit=subprocess.run([sys.executable,'-B','-O','unit_checks.py'],cwd=P,capture_output=True,text=True)
need(unit.returncode==0,'Unit failure '+unit.stderr)
unit_result=json.loads(unit.stdout);need(unit_result['nonfinite_and_type_controls']==48,'Not 48 shipped negative controls')

tree=ast.parse((P/'reproduce_c6.py').read_text(encoding='utf-8'))
env={'math':math,'json':json}
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'invalid_constant','load_json','compare_results','permit_status'}]
exec(node_code(functions,'pure_guards'),env)
reference=get(P/'evidence/C6_RESULTS.json');compare=env['compare_results']
need(compare(reference,copy.deepcopy(reference))==(75,0.0),'Intact reference refused')
negative_count=0
for side in ['reference','actual']:
    for i in range(len(reference['results'])):
        for key in ['start_tM','amplitude_prior_sd_strain','lnB_vs_GR']:
            for value in [float('nan'),float('inf'),float('-inf'),True,'0',None]:
                bad=copy.deepcopy(reference);bad['results'][i][key]=value
                try:compare(bad,reference) if side=='reference' else compare(reference,bad)
                except ValueError:negative_count+=1
                else:raise ValueError('Mutation accepted '+str((side,i,key,value)))
class JsonBytes:
    def __init__(self,raw):self.raw=raw
    def read_bytes(self):return self.raw
for token in [b'NaN',b'Infinity',b'-Infinity']:
    try:env['load_json'](JsonBytes(b'{"value":'+token+b'}'))
    except ValueError:pass
    else:raise ValueError('Strict load accepted '+str(token))
other=[]
for case in ['missing','duplicate','finite_mismatch','empty','bad_reading','overflow_difference']:
    actual=copy.deepcopy(reference);ref=copy.deepcopy(reference)
    if case=='missing':actual['results'].pop()
    elif case=='duplicate':actual['results'].append(copy.deepcopy(actual['results'][0]))
    elif case=='finite_mismatch':actual['results'][1]['lnB_vs_GR']+=.1
    elif case=='empty':actual['results']=[]
    elif case=='bad_reading':actual['results'][1]['reading']=False
    elif case=='overflow_difference':actual['results'][1]['lnB_vs_GR']=1e308;ref['results'][1]['lnB_vs_GR']=-1e308
    try:compare(ref,actual)
    except ValueError:other.append(case)
    else:raise ValueError('Bad structural case accepted '+case)
need(env['permit_status']('NOT_VERIFIED') and env['permit_status']('INCONCLUSIVE_SYSTEMATICS') and not env['permit_status']('CONFIRMED'),'Status policy')

# Mock actual preflight and cleanup; no directories or scientific assets are accessed.
events=[];active=set();existing=False
class FakePath:
    def __init__(self,v):self.v=v.v if isinstance(v,FakePath) else PurePosixPath(str(v))
    def __truediv__(self,n):return FakePath(self.v/str(n))
    def __str__(self):return str(self.v)
    def __eq__(self,o):return isinstance(o,FakePath) and self.v==o.v
    def resolve(self):return self
    def is_relative_to(self,o):return self.v.is_relative_to(o.v)
    def exists(self):return str(self) in active or (existing and self.name in ['C7_V3_2_CLEAN_VALIDATION.json','result.json'])
    @property
    def parent(self):return FakePath(self.v.parent)
    @property
    def name(self):return self.v.name
    def mkdir(self,**kw):events.append(['mkdir',str(self)])
def mkdtemp(prefix,dir):
    p=dir/(prefix+'mock');events.append(['mkdtemp',str(p)]);active.add(str(p));return str(p)
def rmtree(p):
    need(p.is_relative_to(FakePath('/work')) and p!=FakePath('/work'),'Unsafe mock cleanup')
    events.append(['rmtree',str(p)]);active.remove(str(p))
def chmod(p,mode):events.append(['chmod',str(p)]);raise PermissionError('Injected chmod failure')
vm=next(n for n in ast.parse((B/'refeito/validate_package_v3_2_013bis.py').read_text(encoding='utf-8')).body if isinstance(n,ast.FunctionDef) and n.name=='main')
ve=dict(B=FakePath('/base'),Path=FakePath,tempfile=SimpleNamespace(mkdtemp=mkdtemp))
exec(node_code([vm],'validator_preflight'),ve);existing=True
try:ve['main']()
except FileExistsError:pass
else:raise ValueError('Existing receipt accepted')
need(not events and not active,'Validator created temporary before existing receipt refusal')
validator_events=list(events)
wm=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
start=next(i for i,n in enumerate(wm.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='workroot' for t in n.targets))
stop=next(i for i in range(start,len(wm.body)) if isinstance(wm.body[i],ast.Try))
wt=wm.body[stop]
need(isinstance(wt.body[1],ast.Expr) and ast.unparse(wt.body[1]).startswith('os.chmod'),'Unexpected lifecycle ordering')
mock_try=ast.Try(body=wt.body[:2],handlers=wt.handlers,orelse=[],finalbody=wt.finalbody)
code=node_code(wm.body[start:stop]+[mock_try],'wrapper_preflight_and_chmod_only')
base=dict(Path=FakePath,ROOT=FakePath('/package'),args=SimpleNamespace(work_root=FakePath('/work'),output=FakePath('/results/result.json')),
          tempfile=SimpleNamespace(mkdtemp=mkdtemp),os=SimpleNamespace(chmod=chmod),shutil=SimpleNamespace(rmtree=rmtree),
          datetime=datetime,timezone=timezone,new=lambda p,d:events.append(['write_mock_report',d['status'],d['temporary_removed']]))
try:exec(code,dict(base))
except FileExistsError:pass
else:raise ValueError('Existing output accepted')
need(not active and not any(e[0]=='mkdtemp' for e in events),'Wrapper precondition created temporary')
preflight_events=list(events);events.clear();existing=False
try:exec(code,dict(base))
except PermissionError:pass
else:raise ValueError('Injected chmod failure did not propagate')
need(not active and any(e[0]=='rmtree' for e in events),'Chmod failure left temporary')
chmod_events=list(events)

marker='CONJECTURE \u2014 management hypothesis, not TGL canon'
scope=get(P/'tables/reading_scope.json')
need(len(scope['rows'])==60,'Scope table length changed')
modrows=[r for r in scope['rows'] if r['reading']=='R-MOD']
need(len(modrows)==6 and all(marker in r['reading_status'] for r in modrows),'MOD rows')
for name in ['README.md','OVERVIEW.md','tables/reading_scope.csv','tables/reading_scope.json']:
    text=(P/name).read_text(encoding='utf-8');need(marker in text,'Marker '+name)
    need('\u00e2\u20ac' not in text,'Known encoding corruption remains '+name)
need('5\u201395%' in (P/'README.md').read_text(encoding='utf-8'),'Interval encoding')

ledger=get(P/'provenance/DOWNLOAD_LICENSE_LEDGER.json')
need(sha(P/'provenance/DOWNLOAD_LICENSE_LEDGER.json')==sha(B/'cache/MANIFESTO_DOWNLOADS_013BIS_v2.json'),'Ledger source copy')
for rid,row in ledger['records'].items():
    shipped=P/('provenance/zenodo_'+rid+'_record.json')
    need(sha(shipped)==row['source_sha256']==sha(B/row['source_path']),'Licence record pin')
    need(get(shipped)['metadata']['license']['id']==row['id'],'Licence record declaration')
need(sha(P/'provenance/GWOSC_acknowledgement.html')==sha(B/'cache/literature/gwosc_acknowledgement_013bis.html'),'GWOSC source copy')
attributions=get(P/'provenance/SHIPPED_ATTRIBUTIONS.json')
need(attributions['ledger_sha256']==sha(P/'provenance/DOWNLOAD_LICENSE_LEDGER.json'),'Attribution ledger pin')
attrs={r['path']:r for r in attributions['files']}
need(len(attrs)==len(attributions['files']) and set(attrs)==set(pins)-{'provenance/SHIPPED_ATTRIBUTIONS.json'},'Per-file attribution coverage')
mismatches=[]
for n,row in attrs.items():
    need((P/row['provenance']).is_file(),'Attribution source missing')
    if sha(P/n)!=row['sha256']:mismatches.append(dict(path=n,declared_sha256=row['sha256'],actual_sha256=sha(P/n)))
need(set(r['path'] for r in mismatches)=={'README.md','OVERVIEW.md'},'Unexpected attribution mismatch set')
for n,h in pins.items():need(sha(P/n)==h,'Package changed during review')
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='R1_R2_R3_CLOSED_R4_PARTIAL_STALE_ATTRIBUTION_HASHES',
            no_C6_replay=True,manifest_sha256=sha(P/'MANIFEST.json'),archive_sha256=sha(B/receipt['archive']),files=len(pins),
            builder_sha256=manifest['builder_sha256'],wrapper_sha256=sha(P/'reproduce_c6.py'),
            validator_sha256=sha(B/'refeito/validate_package_v3_2_013bis.py'),unit_result=unit_result,
            independent_numeric_type_mutations_refused=negative_count,strict_JSON_tokens_refused=3,
            other_refusals=other,existing_validator_receipt_events=validator_events,
            existing_wrapper_output_events=preflight_events,chmod_failure_events=chmod_events,
            MOD_exact_marker_pass=True,ledger_records_verified=len(ledger['records']),
            attribution_files=len(attrs),attribution_hash_mismatches=mismatches,
            original_v3_1_preserved=True,frozen_reproduction_unchanged=True,script_sha256=sha(Path(__file__)))
raw=(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
with OUT.open('xb') as f:f.write(raw)
need(OUT.read_bytes()==raw,'Control result write mismatch')
print(json.dumps(result,ensure_ascii=False,indent=2))
