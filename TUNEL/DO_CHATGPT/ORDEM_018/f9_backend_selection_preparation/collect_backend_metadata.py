"""Read installed metadata/source bytes only; never import candidate backends."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import subprocess
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
RID = 'bf2a5692-1aff-423e-9345-7bfa256d5072'
request_path = ROOT / 'F9_BACKEND_SELECTION_REQUEST.json'
raw = request_path.read_bytes()
assert len(raw) == 2574
assert hashlib.sha256(raw).hexdigest() == '3302abdbb730ffed057d1f46bde8f92a00e4e58cdfe8e45d63fa6e69500bc914'
request = json.loads(raw)
assert request['request_id'] == RID
assert Path(request['output_folder']).resolve() == BASE
assert all(v == 0 for v in request['limits'].values())
pins = []


def record(path, expected=None, size=None, role='source'):
    path = Path(path)
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if expected is not None:
        assert digest == expected, str(path)
    if size is not None:
        assert len(data) == size, str(path)
    if not any(x['path'] == str(path) for x in pins):
        pins.append({'path': str(path), 'bytes': len(data), 'sha256': digest, 'role': role})
    return data


record(request_path, role='official_request')
objects = {}
for source in request['source_pins']:
    data = record(source['path'], source['sha256'], source['bytes'], 'request_pin')
    objects[Path(source['path']).name] = json.loads(data)
manifest = objects['MANIFESTO_ENTREGA.json']
for source in manifest['files']:
    record(ROOT / 'f9_numerical_certification_preparation' / source['path'], source['sha256'], source['bytes'], 'accepted_interface_member')
review = objects['MANIFESTO_REVISAO_CERTIFICACAO_NUMERICA_F9.json']
for source in review['files']:
    record(source['path'], source['sha256'], source['bytes'], 'independent_review_member')
tail = objects['RECIBO_ROOT_CONTROLES_TAIL_V2_PASS.json']
for source in tail['inputs_revalidated']:
    if Path(source['path']).name in ['tail_envelope.py', 'PROPOSTA_ENVELOPE_F9.md', 'RUNTIME_PINS.json']:
        record(source['path'], source['sha256'], source['bytes'], 'consumed_tail_dependency_read_only')

stdlib = [Path(r'C:\Python314\python.exe'), Path(r'C:\Python314\python314.dll'),
    Path(r'C:\Python314\Lib\fractions.py'), Path(r'C:\Python314\Lib\decimal.py'),
    Path(r'C:\Python314\Lib\_pydecimal.py')]
stdlib.extend(sorted(Path(r'C:\Python314\DLLs').glob('_decimal*.pyd')))
for path in stdlib:
    record(path, role='installed_stdlib_or_runtime_bytes_not_imported')

pattern = re.compile(r'^(python.?flint|flint|gmpy2|mpmath|sympy|numpy|scipy|mpfi|interval|pyinterval|mpfr|arb|portion|camb)[-_.]', re.I)
roots = [Path(r'C:\Python314\Lib\site-packages'), Path(r'C:\Users\rotol\AppData\Roaming\Python\Python314\site-packages')]
windows = []
for root in roots:
    found = []
    for path in sorted(root.glob('*.dist-info')):
        if pattern.match(path.name):
            metadata = path / 'METADATA'
            data = record(metadata, role='installed_distribution_metadata')
            header = [line for line in data.decode('utf-8', errors='replace').splitlines() if line.startswith(('Name:', 'Version:', 'Requires-Python:'))]
            found.append({'path': str(metadata), 'header': header})
    windows.append({'root': str(root), 'exists': root.is_dir(), 'matching_metadata': found})

user_site = roots[1]
for relative in ['mpmath/ctx_iv.py', 'mpmath/libmp/libmpi.py', 'mpmath/function_docs.py']:
    record(user_site / relative, role='installed_mpmath_source_not_imported')

linux_code = r'''
from pathlib import Path
import sys,json,re,hashlib
base=Path('/opt/lal_env/lib/python3.12/site-packages')
found=[]
for p in sorted(base.glob('*.dist-info')):
    if re.match(r'^(python.?flint|flint|gmpy2|mpmath|sympy|numpy|scipy|mpfi|interval|pyinterval|mpfr|arb|portion|camb)[-_\.]',p.name,re.I):
        m=p/'METADATA';b=m.read_bytes()
        headers=[l for l in b.decode('utf-8',errors='replace').splitlines() if l.startswith(('Name:','Version:','Requires-Python:'))]
        found.append({'path':str(m),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'header':headers})
print(json.dumps({'root':str(base),'exists':base.is_dir(),'python':sys.version,'executable':sys.executable,'matching_metadata':found,'candidate_imports':0}))
'''
command = ['wsl.exe', '-d', 'Ubuntu-24.04', '--', '/opt/lal_env/bin/python', '-I', '-S', '-B', '-c', linux_code]
proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=False)
assert proc.returncode == 0, 'WSL_METADATA_READ_FAILED'
assert len(proc.stdout) < 32768 and len(proc.stderr) < 32768
linux = json.loads(proc.stdout.decode('utf-8'))
assert linux['candidate_imports'] == 0 and linux['exists'] is True

excerpts = []
spans = [
    (user_site/'mpmath-1.3.0.dist-info/METADATA',207,224),
    (user_site/'mpmath/libmp/libmpi.py',278,297),
    (Path(r'C:\Python314\Lib\fractions.py'),182,203),
    (Path(r'C:\Python314\Lib\fractions.py'),790,858),
    (Path(r'C:\Python314\Lib\_pydecimal.py'),3052,3071),
    (Path(r'C:\Python314\Lib\_pydecimal.py'),3196,3202),
    (ROOT/'f9_tail_envelope_implementation_v2/tail_envelope.py',119,149),
    (ROOT/'f9_tail_envelope_proposal_v2/PROPOSTA_ENVELOPE_F9.md',55,66),
]
for path, first, last in spans:
    b=path.read_bytes();lines=b.decode('utf-8').splitlines()
    text='\n'.join(lines[first-1:last])
    excerpts.append({'path':str(path),'source_sha256':hashlib.sha256(b).hexdigest(),'line_start':first,'line_end':last,'text':text,'excerpt_sha256_utf8':hashlib.sha256(text.encode('utf-8')).hexdigest()})

result={'request_id':RID,'created_utc':datetime.now(timezone.utc).isoformat(),
    'status':'LOCAL_METADATA_AND_STATIC_SOURCE_ONLY_NOT_BACKEND_QUALIFICATION',
    'windows_runtime':{'python':sys.version,'executable':sys.executable,'isolated':sys.flags.isolated,'no_site':sys.flags.no_site},
    'windows_inventory':windows,'wsl_inventory':linux,'wsl_stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),
    'local_pins':pins,'local_source_excerpts':excerpts,
    'inventory_scope':'Only the two listed Windows roots and the listed WSL venv; absence in this list is not absence on whole machine',
    'access_note':'Initial sandbox enumeration denied user-site and WSL. Approved read-only metadata elevation then succeeded. No candidate import or package install.',
    'candidate_imports':0,'control_or_solver_runs':0,'observed_data_access':False,'remote_model_calls':0,'downloads':0,'installations':0,
    'scanning_scripts_are_metadata_not_scientific_controls':True}
dest=BASE/'METADADOS_BACKENDS_LOCAIS.json';assert not dest.exists()
data=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
tmp=dest.with_suffix('.json.tmp')
with tmp.open('xb') as stream:
    stream.write(data);stream.flush();os.fsync(stream.fileno())
assert tmp.read_bytes()==data
os.replace(tmp,dest);assert dest.read_bytes()==data
print(json.dumps({'file':str(dest),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'local_pins':len(pins),'wsl_metadata':len(linux['matching_metadata']),'candidate_imports':0}))
