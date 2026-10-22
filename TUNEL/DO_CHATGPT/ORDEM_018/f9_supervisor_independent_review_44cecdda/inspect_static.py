"""Independent bytes/AST/diff inspection. Never imports or executes candidates."""
import ast
import datetime
import difflib
import hashlib
import json
import os
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
TARGET = BASE / 'f9_supervisor_preparation'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def pin(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    return {'path':str(path), 'bytes':len(raw), 'sha256':sha(raw)}

def read_json(path):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError('duplicate key: ' + key)
            out[key] = value
        return out
    def constant(value):
        raise ValueError('nonfinite: ' + value)
    return json.loads(Path(path).read_bytes(), object_pairs_hook=pairs,
                      parse_constant=constant)

def checked(rec, path=None):
    actual = pin(path or rec['path'])
    assert actual['bytes'] == rec['bytes'] and actual['sha256'] == rec['sha256'], actual
    return actual

def atomic_json(name, value):
    path = HERE / name
    raw = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode('utf-8')
    if path.exists():
        old = path.read_bytes()
        backup = path.with_name(path.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as stream:
            stream.write(old)
        assert backup.read_bytes() == old
    temp = path.with_name(path.name+'.tmp')
    with temp.open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    assert temp.read_bytes() == raw and raw
    os.replace(temp, path)
    assert path.read_bytes() == raw

def apply_unified(source, diff):
    """Apply exact textual hunks in memory, with no fuzz and checked line counts."""
    old = source.splitlines(keepends=True)
    lines = diff.splitlines(keepends=True)
    assert lines[0].startswith('--- ') and lines[1].startswith('+++ ')
    index = 2; cursor = 0; out = []; hunks = []
    while index < len(lines):
        match = re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@[^\n]*\n?', lines[index])
        assert match, lines[index]
        before, count_before, after, count_after = [int(x) if x is not None else 1 for x in match.groups()]
        start = before - 1 if count_before else before
        assert cursor <= start
        out.extend(old[cursor:start]); cursor = start; index += 1
        assert len(out) == (after - 1 if count_after else after)
        removed = added = 0
        while index < len(lines) and not lines[index].startswith('@@ '):
            row = lines[index]; index += 1
            assert row[:1] in (' ', '-', '+'), row
            if row[:1] in (' ', '-'):
                assert old[cursor] == row[1:], (cursor + 1, old[cursor], row)
                cursor += 1; removed += 1
            if row[:1] in (' ', '+'):
                out.append(row[1:]); added += 1
        assert (removed, added) == (count_before, count_after)
        hunks.append({'old_line':before,'old_count':count_before,'new_line':after,'new_count':count_after})
    out.extend(old[cursor:])
    return ''.join(out), hunks

def class_signatures(tree, class_name):
    cls = next(x for x in tree.body if isinstance(x, ast.ClassDef) and x.name == class_name)
    return {n.name:ast.dump(n.args, include_attributes=False) for n in cls.body
            if isinstance(n, ast.FunctionDef) and n.name in ('admit','checkpoint','process_identity','terminal_audit')}

def main():
    identity = read_json(HERE/'IDENTIDADE_REVISAO.json')
    intake = read_json(BASE/'RECIBO_ROOT_INTAKE_SUPERVISOR_F9.json')
    manifest_pin = checked(intake['manifest'])
    manifest = read_json(TARGET/'MANIFESTO_PREPARACAO.json')
    assert manifest['request_id'] == identity['candidate_request_id']
    groups = {}
    for field in ('files','backup_bytes_retained','source_pins'):
        group = []
        for rec in manifest[field]:
            path = Path(rec['path']) if 'path' in rec else TARGET/rec['name']
            if field != 'source_pins':
                assert path.resolve().parent == TARGET.resolve()
            group.append(checked(rec, path))
        groups[field] = group
    assert (len(groups['files']),len(groups['backup_bytes_retained']),len(groups['source_pins'])) == (25,8,18)
    intake_pins = [checked(rec) for rec in intake['verified']]
    copies = read_json(TARGET/'COPIAS_EXATAS.json')['copies']
    for copy in copies:
        checked(copy['source']); checked(copy['copy'])
        assert Path(copy['source']['path']).read_bytes() == Path(copy['copy']['path']).read_bytes()
    ast_records = []; trees = {}
    for rec in groups['files']:
        p = Path(rec['path'])
        if p.suffix != '.py':
            if p.suffix == '.json':
                read_json(p)
            continue
        tree = ast.parse(p.read_bytes(), filename=str(p)); trees[p.name] = tree
        imports = sorted({n.module if isinstance(n,ast.ImportFrom) else a.name
            for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))
            for a in ([None] if isinstance(n,ast.ImportFrom) else n.names)})
        assert not any(x.split('.')[0] in ('numpy','scipy','camb','ctypes') for x in imports)
        ast_records.append({'source':rec,'imports':imports,'ast_valid':True})
    assert len(ast_records) == 9
    signatures = class_signatures(trees['supervisor_port.py'],'QualifiedSupervisor')
    assert signatures == class_signatures(trees['supervisor_adapter.py'],'POSIXSupervisor39')
    assert signatures == class_signatures(trees['supervisor_port_cooperative_proposal.py'],'QualifiedSupervisor')
    derivation = read_json(TARGET/'SUCESSOR_DERIVACAO.json')
    controller = BASE/'f9_controller_preparation/controller.py'
    port = BASE/'f9_controller_preparation/supervisor_port.py'
    diff_records = []
    derived_trees = {}
    for p, name in ((controller,'CONTROLLER_COOPERATIVE_PROPOSAL.diff'),(port,'PORT_COOPERATIVE_PROPOSAL.diff')):
        # The author's text diff is LF-normalized. Original source bytes remain untouched.
        derived, hunks = apply_unified(p.read_text(encoding='utf-8'),(TARGET/name).read_text(encoding='utf-8'))
        tree = ast.parse(derived,filename='IN_MEMORY_PROPOSAL/'+p.name)
        derived_trees[p.name] = tree
        raw = derived.encode('utf-8')
        if p == controller:
            assert sha(p.read_bytes()) == derivation['base_controller_sha256']
            assert len(raw) == derivation['proposed_controller_bytes'] and sha(raw) == derivation['proposed_controller_sha256']
            before = ast.parse(p.read_bytes())
            for function in ('_grid','_verify_bindings','_preparation'):
                original = next(n for n in before.body if isinstance(n,ast.FunctionDef) and n.name == function)
                updated = next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name == function)
                assert ast.dump(original,include_attributes=False) == ast.dump(updated,include_attributes=False)
        else:
            assert sha(p.read_bytes()) == derivation['base_port_sha256']
            assert raw == (TARGET/'supervisor_port_cooperative_proposal.py').read_bytes()
        diff_records.append({'diff':pin(TARGET/name),'base':pin(p),'derived_bytes':len(raw),'derived_sha256':sha(raw),'hunks':hunks,'AST_valid':True,'applied_to_disk':False})
    backups = []
    for name in ('process_supervisor.py','qualification_child.py','native_progress.py'):
        paths = sorted(TARGET.glob(name+'.bak_*'))
        snapshots = []
        for p in paths:
            raw = p.read_bytes(); ast.parse(raw,filename=str(p))
            edits = []
            previous = raw.decode('utf-8').splitlines()
            current = (TARGET/name).read_text(encoding='utf-8').splitlines()
            for op,i,j,a,b in difflib.SequenceMatcher(a=previous,b=current).get_opcodes():
                if op != 'equal':
                    edits.append({'operation':op,'snapshot_lines':[i+1,j],'current_lines':[a+1,b]})
            snapshots.append({'pin':pin(p),'ast_valid':True,'changes_to_current':edits})
        backups.append({'current':pin(TARGET/name),'snapshots':snapshots})
    # No file from the reviewed package is written; no module under review is imported.
    for rows in groups.values():
        for rec in rows:
            checked(rec)
    checked(manifest_pin)
    receipt = {'schema':'F9_SUPERVISOR_INDEPENDENT_STATIC_CHECKS_V1',
        'request_id':identity['request_id'],'parent_request_id':identity['parent_request_id'],
        'target_preparation_request_id':identity['candidate_request_id'],
        'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status':'STATIC_BYTES_AST_DIFF_CHECKS_PASSED_NOT_RUNTIME_QUALIFICATION',
        'candidate_manifest':manifest_pin,'intake_receipt':pin(BASE/'RECIBO_ROOT_INTAKE_SUPERVISOR_F9.json'),
        'inventory':groups,'intake_verified_count':len(intake_pins),'exact_copies':copies,
        'AST':ast_records,'signatures_equal':True,'diffs':diff_records,
        'unchanged_functions':['_grid','_verify_bindings','_preparation'],
        'backup_present_and_syntax_checked':backups,
        'backup_historical_limit':'Hashes atuais e oito arquivos conferidos. A nota de recuperação não incorpora o recibo original pré-incidente; a medição anterior permanece DECLARADO nesta revisão. Não há evidência de perda dos originais nem se atesta a cronologia só por hashes atuais.',
        'execution':{'candidate_imports':0,'candidate_executions':0,'numerical_controls':0,'WSL':0,'solver':0,'observed_reads':False,'providers':0,'AUTH_CLAIM_ROOT_DECISION_created':False},
        'review_script':pin(__file__),
        'limits':['AST não prova comportamento em execução','Não mede Linux/rlimits/threads/kill/reap/FS','Inventário Linux histórico conferido como arquivo, não como runtime disponível','Não aplica propostas aos originais','Não substitui revisões I02/P3 nem qualifica F1']}
    atomic_json('VERIFICACOES_ESTATICAS.json',receipt)
    print(json.dumps({'receipt':pin(HERE/'VERIFICACOES_ESTATICAS.json'),'checked_members':25,'checked_sources':18,'checked_backups':8,'candidate_executions':0}))

if __name__ == '__main__':
    main()
