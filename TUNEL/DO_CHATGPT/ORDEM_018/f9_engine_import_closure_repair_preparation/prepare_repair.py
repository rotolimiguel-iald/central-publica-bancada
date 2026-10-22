"""Package a static import-closure delta. No candidate import or execution."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import difflib
import hashlib
import json
import os
import uuid

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
OLD = ROOT / 'f9_engine_assembly_integration_preparation'
REQUEST_FILE = ROOT / 'F9_IMPORT_CLOSURE_REPAIR_PREPARATION_REQUEST.json'
REQUEST = 'e5d214e4-972e-41f5-bd14-0dc071c00e6b'


def pin(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def put(path, value):
    if isinstance(value, dict):
        value = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
    if isinstance(value, str):
        value = value.encode('utf-8')
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_bytes() if path.exists() else None
    if value == old:
        return
    if old is not None:
        backup = path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    tmp = path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(value)
    assert tmp.read_bytes() == value and (path.read_bytes() if path.exists() else None) == old
    os.replace(tmp, path)
    assert path.read_bytes() == value


def replace_once(text, old, new):
    assert text.count(old) == 1, ('Nonunique patch anchor', old[:100])
    return text.replace(old, new, 1)


def main():
    assert not any((BASE/n).exists() for n in ('AUTORIZACAO_ROOT.json','CLAIM.json','RUN','RESULT.json'))
    request = json.loads(REQUEST_FILE.read_bytes())
    assert request['request_id'] == REQUEST
    for source in request['sources']:
        assert pin(Path(source['path'])) == {k:source[k] for k in ('bytes','sha256')}
    old_manifest = json.loads((OLD/'MANIFESTO_PREPARACAO.json').read_bytes())
    protected = [OLD/x['path'] for x in old_manifest['files']]
    for row in old_manifest['files']:
        assert pin(OLD/row['path']) == {k:row[k] for k in ('bytes','sha256')}
    protected += [OLD/'MANIFESTO_PREPARACAO.json', OLD/'AUTORIZACAO_ROOT.json',
                  OLD/'CLAIM.json', OLD/'RESULT.json']
    protected += [p for p in (OLD/'RUN').rglob('*') if p.is_file()]
    protected_before = {str(p):pin(p) for p in protected}
    diagnostic_manifest_path = Path(request['sources'][1]['path'])
    diagnostic = json.loads(diagnostic_manifest_path.read_bytes())
    for row in diagnostic['files']:
        assert pin(Path(row['path'])) == {k:row[k] for k in ('bytes','sha256')}
    identity_path = BASE/'UNIT_IDENTITY.json'
    if identity_path.exists():
        identity = json.loads(identity_path.read_bytes())
    else:
        identity = {'preparation_request_id':REQUEST, 'proposed_run_request_id':str(uuid.uuid4()),
            'created_utc':datetime.now(timezone.utc).isoformat(),
            'status':'PROPOSED_NOT_AUTHORIZED_NOT_CLAIMED',
            'predecessor_consumed_request_id':old_manifest['proposed_run_request_id']}
        put(identity_path, identity)
    new_id, old_id = identity['proposed_run_request_id'], old_manifest['proposed_run_request_id']
    assert new_id != old_id
    old_contract = json.loads((OLD/'CONTRATO_WSL.json').read_bytes())
    original_local = [r['relative_path'] for r in old_contract['local_pins']]
    replacements = {'common.py','worker.py','linux_control.py','launch_windows.py',
        'UNIT_IDENTITY.json','EFFECTIVE_CONFIGURATION.json','ASSEMBLY_ADMISSION.json','RUNTIME_INVENTORY.json'}
    for name in original_local:
        if name not in replacements:
            put(BASE/name, (OLD/name).read_bytes())
    effective = json.loads((OLD/'EFFECTIVE_CONFIGURATION.json').read_bytes())
    effective['request_id'] = new_id
    put(BASE/'EFFECTIVE_CONFIGURATION.json', effective)
    assert {k:v for k,v in effective.items() if k!='request_id'} == {
        k:v for k,v in json.loads((OLD/'EFFECTIVE_CONFIGURATION.json').read_bytes()).items() if k!='request_id'}
    admission = json.loads((OLD/'ASSEMBLY_ADMISSION.json').read_bytes())
    admission['engine_configuration_sha256'] = pin(BASE/'EFFECTIVE_CONFIGURATION.json')['sha256']
    admission['runtime_sha256'] = pin(BASE/'RUNTIME_INVENTORY.json')['sha256']
    put(BASE/'ASSEMBLY_ADMISSION.json', admission)
    old_posix = '/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/'+OLD.name
    new_posix = '/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/'+BASE.name
    for name in ('common.py','linux_control.py','launch_windows.py'):
        text = (OLD/name).read_text(encoding='utf-8')
        text = text.replace(str(OLD),str(BASE)).replace(old_posix,new_posix).replace(old_id,new_id)
        assert str(OLD) not in text and old_posix not in text and old_id not in text
        put(BASE/name, text)
    worker = (OLD/'worker.py').read_text(encoding='utf-8')
    helpers = '''def is_exactly_absent(path):
    try:
        os.lstat(path)
    except FileNotFoundError:
        return True
    except OSError:
        return False
    return False


def bounded_failure(exc):
    # Read frame metadata only: do not trigger source lookup through linecache.
    head, tail, total = [], [], 0
    tb = exc.__traceback__
    while tb is not None:
        total += 1
        code = tb.tb_frame.f_code
        row = (total, str(code.co_filename)[:384], tb.tb_lineno, str(code.co_name)[:128])
        if total <= 2:
            head.append(row)
        tail.append(row)
        if len(tail) > 8:
            tail.pop(0)
        tb = tb.tb_next
    selected = head + [row for row in tail if row[0] > len(head)]
    return {'type': type(exc).__name__[:128], 'message': str(exc)[:2000],
        'traceback': '\\n'.join(f'#{n} {file}:{line} in {name}' for n,file,line,name in selected),
        'traceback_total_frames': total, 'traceback_retained_frames': len(selected),
        'traceback_omitted_frames': total-len(selected),
        'traceback_policy': 'FIRST_2_AND_LAST_8_METADATA_ONLY_SINGLE_EXCEPTION'}


'''
    worker = replace_once(worker, 'def main():\n', helpers+'def main():\n')
    anchor = "    g.need(inventory['stdlib_sysconfig_included'], 'sysconfig inventory missing')"
    worker = replace_once(worker, anchor, anchor+'''
    g.need(set(inventory['required_builtin_modules']) <= set(sys.builtin_module_names),
           'Build metadata builtin not present in current interpreter')
    exact_absent_probes = set(inventory['exact_absent_probe_paths'])
    g.need(exact_absent_probes == {'/usr/lib/python312.zip'}, 'Exact absence probe contract')
    for probe in exact_absent_probes:
        g.need(is_exactly_absent(probe), 'Required absent probe exists or is unreadable: '+probe)
''')
    anchor = '''            elif name not in reads and name not in readonly_extra:
'''
    worker = replace_once(worker, anchor, '''            elif name in exact_absent_probes:
                if is_exactly_absent(name):
                    missing_runtime_probes.append({'path': name, 'status': 'EXACT_ABSENT_PROBE_NO_CONTENT'})
                else:
                    reason = 'EXACT_ABSENT_PROBE_PRESENT_OR_UNREADABLE'
            elif name not in reads and name not in readonly_extra:
''')
    old_error = '''        error = {'type': type(exc).__name__, 'message': str(exc)[:4000],
                 'traceback': traceback.format_exc(limit=8)[-8000:]}
'''
    worker = replace_once(worker, old_error, '        error = bounded_failure(exc)\n')
    old_outer = '''        print(json.dumps({'status': 'FAILED_PREFLIGHT_OR_RECEIPT', 'error': type(exc).__name__, 'message': str(exc)[:4000]}))'''
    worker = replace_once(worker, old_outer, '''        print(json.dumps({'status': 'FAILED_PREFLIGHT_OR_RECEIPT', 'error': bounded_failure(exc)}))''')
    put(BASE/'worker.py', worker)
    inventory = json.loads((BASE/'RUNTIME_INVENTORY.json').read_bytes())
    old_inventory = json.loads((OLD/'RUNTIME_INVENTORY.json').read_bytes())
    old_pins, new_pins = ({r['path']:r for r in d['pins']} for d in (old_inventory, inventory))
    assert all(new_pins[k]==v for k,v in old_pins.items())
    assert set(inventory['roots'])-set(old_inventory['roots']) == {
        inventory['site_packages']+'/charset_normalizer',
        inventory['site_packages']+'/charset_normalizer-3.5.1.dist-info'}
    assert len(new_pins)-len(old_pins)==27
    contract = dict(old_contract)
    contract.update(schema='F9_ENGINE_IMPORT_CLOSURE_REPAIR_PREPARATION_V1',
        preparation_request_id=REQUEST, request_id=new_id,
        status='PREPARED_AWAITING_INDEPENDENT_DELTA_REVIEW_NO_AUTHORIZATION')
    contract['local_pins'] = [{'relative_path':name,**pin(BASE/name)} for name in original_local]
    contract['dependency_delta'] = {'additional_exact_runtime_files':27,
        'exact_absent_probe':'/usr/lib/python312.zip', 'required_builtin_modules':inventory['required_builtin_modules'],
        'predecessor_is_terminal':True, 'old_authorization_not_carried':True}
    put(BASE/'CONTRATO_WSL.json', contract)
    diffs = []
    for name in original_local+['CONTRATO_WSL.json']:
        a,b=(OLD/name).read_bytes(),(BASE/name).read_bytes()
        if a!=b:
            if name == 'RUNTIME_INVENTORY.json':
                diffs.append('Runtime inventory:27 exact additions, old pins unchanged; see DEPENDENCY_CLOSURE_EVIDENCE.json\n')
            else:
                diffs.extend(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),
                    fromfile='consumed/'+name,tofile='prepared/'+name))
    put(BASE/'DELTA_REPAIR.diff',''.join(diffs))
    parsed = []
    for path in sorted(BASE.rglob('*.py')):
        ast.parse(path.read_bytes(),filename=str(path));parsed.append(path.relative_to(BASE).as_posix())
    unchanged = [n for n in original_local if (OLD/n).read_bytes()==(BASE/n).read_bytes()]
    source_records = [{'path':str(REQUEST_FILE),**pin(REQUEST_FILE)}] + request['sources'] + diagnostic['files']
    source_records += [{'path':str(p),**pin(p)} for p in protected]
    put(BASE/'SOURCE_LINEAGE.json',{'request_id':REQUEST,'sources':source_records,
        'predecessor_manifest':pin(OLD/'MANIFESTO_PREPARACAO.json'),
        'exact_unchanged_copies':unchanged,'old_runtime_pins_unchanged':len(old_pins),
        'new_runtime_files':27,'effective_configuration_change':'request_id only',
        'guard_change':'One exact absent ZIP plus runtime builtin check; existing deny latch retained',
        'traceback_change':'First2/last8 frame metadata and total count; no source lookup',
        'transport_change':'Identity/paths only; scopes/one-use/deadlines/cleanup unchanged'})
    assert protected_before == {str(p):pin(p) for p in protected}
    assert not any((BASE/n).exists() for n in ('AUTORIZACAO_ROOT.json','CLAIM.json','RUN','RESULT.json'))
    put(BASE/'STATIC_PREPARATION_RECEIPT.json',{'at_utc':datetime.now(timezone.utc).isoformat(),
        'request_id':REQUEST,'proposed_run_request_id':new_id,'status':'STATIC_DELTA_PREPARED_NOT_EXECUTED',
        'AST_parsed_only':parsed,'protected_predecessor_files_unchanged':len(protected),
        'unchanged_scientific_engine':pin(BASE/'sources/background_controls.py'),
        'unchanged_assembler':pin(BASE/'sources/five_model_assembly.py'),
        'original_runtime_pins':len(old_pins),'new_runtime_pins':len(new_pins),
        'candidate_imports':0,'WSL_processes_started':0,'solver_calls':0,'likelihood_calls':0,
        'observed_data_read':False,'authorization_created':False,'claims_created':False,
        'independent_delta_review_required':True})
    files=[]
    for p in sorted(BASE.rglob('*')):
        if p.is_file() and '.bak_' not in p.name and '.tmp_' not in p.name and p.name not in ('MANIFESTO_PREPARACAO.json','RECIBO_COORDENACAO.json'):
            files.append({'path':p.relative_to(BASE).as_posix(),**pin(p)})
    put(BASE/'MANIFESTO_PREPARACAO.json',{'preparation_request_id':REQUEST,
        'proposed_run_request_id':new_id,'status':'PREPARED_NOT_RUN_NOT_AUTHORIZED',
        'files':files,'scientific_execution':False})
    print(json.dumps({'manifest':pin(BASE/'MANIFESTO_PREPARACAO.json'),
        'members':len(files),'proposed_run_request_id':new_id,'runtime_files':len(new_pins),
        'protected_predecessor_files_unchanged':len(protected),'candidate_imports':0,'solver_calls':0}))


if __name__ == '__main__':
    main()
