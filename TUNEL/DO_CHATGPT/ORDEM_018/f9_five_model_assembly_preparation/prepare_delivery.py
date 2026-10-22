"""Documentary preparation only: bytes, hashes, JSON structure and AST.

Never imports, executes or compiles five_model_assembly.py. No data catalogues,
solvers or controls. Outputs are confined to this preparation directory.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REQUEST = ROOT / 'F9_FIVE_MODEL_ASSEMBLY_REQUEST.json'


def pin(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def put(path, raw):
    if isinstance(raw, str):
        raw = raw.encode('utf-8')
    if isinstance(raw, dict):
        raw = (json.dumps(raw, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if path.exists() and path.read_bytes() == raw:
        return
    old = path.read_bytes() if path.exists() else None
    if old is not None:
        backup = path.with_name(path.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temp = path.with_name(path.name + '.tmp_' + uuid.uuid4().hex)
    temp.write_bytes(raw)
    assert len(raw) > 0 and temp.read_bytes() == raw
    assert (path.read_bytes() if path.exists() else None) == old
    os.replace(temp, path)
    assert path.read_bytes() == raw


def main():
    req = json.loads(REQUEST.read_bytes())
    assert req['request_id'] == '8e017d91-f3bb-4ec6-9236-5b2c327d1b98'
    assert HERE == Path(req['output_folder'])
    verified = []
    for item in req['sources']:
        actual = pin(Path(item['path']))
        assert actual == item, actual['path']
        verified.append(actual)
    by_name = {Path(item['path']).name: item for item in verified}
    resolver = json.loads(Path(by_name['RESOLUTOR_F9.json']['path']).read_bytes())
    historical = resolver['sources']['historical_background_sources']
    actual = pin(Path(historical['path']))
    assert all(actual[k] == historical[k] for k in ('path', 'bytes', 'sha256'))
    layout_manifest_path = ROOT / 'f9_structural_layout_preparation/MANIFESTO_LAYOUT_ESTRUTURAL.json'
    lm = pin(layout_manifest_path)
    assert lm['bytes'] == 3823 and lm['sha256'] == '0eb27f110d675da5f511f4663137c79151e53188dc8090a464e8d5603b395ce2'
    layout_manifest = json.loads(layout_manifest_path.read_bytes())
    layout_members = []
    for item in layout_manifest['files']:
        actual_member = pin(Path(item['path']))
        assert actual_member == item
        layout_members.append(actual_member)
    layout_path = ROOT / 'f9_structural_layout_preparation/LAYOUT_ESTRUTURAL_3CMB_13BAO.json'
    layout_pin = pin(layout_path)
    layout = json.loads(layout_path.read_bytes())
    assert len(layout['components']) == 16 and layout['observed_values'] is None
    assert [x['observable'] for x in layout['components'][:3]] == ['R', 'l_A', 'omega_b_h2']
    assert [x['observable'] for x in layout['components'][-2:]] == ['DH_over_rdrag', 'DM_over_rdrag']
    assert layout['alpha']['symbol'] == 'ALPHA_FINE_CODATA_2018'
    dependencies = {
        'resolver': by_name['RESOLUTOR_F9.json'],
        'background_layout': layout_pin,
        'linear_design': by_name['ESPECIFICACAO_LINEAR.json'],
        'background_engine': by_name['background_controls.py'],
        'background_protocol': by_name['PROTOCOL.json'],
        'MM_contract': by_name['CONTRATO_MM_CANDIDATO.json'],
    }
    module_path = HERE / 'five_model_assembly.py'
    module_text = module_path.read_text(encoding='utf-8')
    placeholder = '__SOURCE_PINS_FROM_BYTES__'
    if placeholder in module_text:
        assert module_text.count(placeholder) == 1
        module_text = module_text.replace(placeholder, repr(dependencies))
        put(module_path, module_text)
    tree = ast.parse(module_text, filename=str(module_path))
    source_node = next(n.value for n in tree.body if isinstance(n, ast.Assign)
                       and any(isinstance(t, ast.Name) and t.id == 'SOURCE_PINS' for t in n.targets))
    assert ast.literal_eval(source_node) == dependencies
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(x.name for x in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)
    assert sorted(imports) == ['fractions', 'hashlib', 'json', 'math']
    forbidden = {'open', 'eval', 'exec', 'compile', '__import__', 'subprocess', 'Popen', 'system'}
    calls = {n.func.id if isinstance(n.func, ast.Name) else n.func.attr
             for n in ast.walk(tree) if isinstance(n, ast.Call)
             and isinstance(n.func, (ast.Name, ast.Attribute))}
    assert not (calls & forbidden)
    # No module-level imperative calls except class declarations/imports.
    assert all(isinstance(n, (ast.Expr, ast.Import, ast.ImportFrom, ast.Assign,
                              ast.ClassDef, ast.FunctionDef)) for n in tree.body)
    assert not any(isinstance(child, ast.Call) for n in tree.body if isinstance(n, (ast.Assign, ast.Expr))
                   for child in ast.walk(n))
    functions = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
    assert 'assemble_five' in functions
    design = json.loads(Path(dependencies['linear_design']['path']).read_bytes())
    rows = design['rows']
    structural = {
        'rows': len(rows), 'eta_columns': len(design['eta_columns']),
        'a_h_nonzero': sum(r['a_h'] != '0' for r in rows),
        'c_C_nonzero': sum(r['c_C'] != '0' for r in rows),
        'dex_rows_to_multiply_by_five': sum(r['family'] in ('SN_HF', 'SBF_HF', 'megamaser') for r in rows),
        'row_ids_unique': len({r['row_id'] for r in rows}) == len(rows),
        'nuisance_keys_unique': len({r['key'] for r in design['eta_columns']}) == len(design['eta_columns']),
        'rank_recomputed': False,
    }
    assert (structural['rows'], structural['eta_columns'], structural['a_h_nonzero'],
            structural['c_C_nonzero'], structural['dex_rows_to_multiply_by_five']) == (267, 63, 7, 119, 7)
    assert structural['row_ids_unique'] and structural['nuisance_keys_unique']
    protocol = json.loads(Path(dependencies['background_protocol']['path']).read_bytes())
    assert protocol['redshifts']['low_z_controls'] == [0, .1, .5, 1, 2, 3]
    assert protocol['redshifts']['z_star_law'] == 1089.95
    put(HERE / 'FONTES_PINADAS.json', {
        'request': pin(REQUEST), 'direct_sources': verified,
        'additional_documentary_source': actual, 'layout_manifest': lm, 'layout_members': layout_members,
        'embedded_sources': dependencies,
        'upstream_origin_pins_not_reopened_here': layout['sources'],
        'raw_observed_files_read': [], 'source_files_modified': [],
    })
    limits = {
        'candidate_imports': 0, 'candidate_calls': 0, 'controls': 0, 'solvers': 0,
        'observed_reads': 0, 'remote_model_calls': 0, 'downloads_or_installs': 0,
        'new_execution_request_or_claim': False, 'shared_memories_modified': False,
    }
    result = {
        'request_id': req['request_id'], 'created_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'STATIC_SOURCE_AND_DOCUMENTARY_CHECKS_PASSED_NOT_RUNTIME_TESTED',
        'source_checks': {'direct': len(verified), 'additional_documentary': 1, 'structural_layout_manifest_and_members': 4, 'all_match': True},
        'structural_metadata': structural,
        'AST': {'parsed': True, 'import_modules': imports, 'functions': functions,
                'forbidden_call_names_present': [], 'top_level_calls': False,
                'scope': 'syntactic inspection; not semantic proof, independent review or a runtime test'},
        'prepared_module': pin(module_path), 'limits': limits,
        'missing_inputs': [
            'Reviewed structural admission and effective-background configuration/runtime/receipt identity.',
            'Injected engine result at admitted layout redshifts and requested theta; no such result generated here.',
        ],
        'structural_gaps_resolved': ['Ordered 3CMB+13BAO layout received and pinned.', 'Alpha source decimal/locator received inside the same layout; no second extraction or duplicate API artifact.'],
        'next_action': 'Independent static integration review of assembly, admission and engine envelope; no execution request.',
        'scientific_outputs': {'chi2': None, 'p': None, 'sigma': None, 'lnB': None},
    }
    put(HERE / 'RECIBO_PREPARACAO_ESTATICA.json', result)
    put(HERE / 'DECISAO_IMPLEMENTACAO.json', {
        'request_id': req['request_id'], 'status': 'PREPARED_NOT_EXECUTED',
        'alternatives': [
            {'id': 'A', 'selected': True, 'method': 'Passive pure adapter with injected engine result; existing design reused.'},
            {'id': 'B', 'selected': False, 'method': 'New solver-coupled implementation.', 'reason': 'Duplicates existing execution/cosmology responsibilities.'},
            {'id': 'C', 'selected': False, 'method': 'Callback evaluator invoked from assembly.', 'reason': 'Caller can supply the resulting packet without adding external effects here.'},
        ], 'limits': limits, 'missing_inputs': result['missing_inputs'],
        'next_action': result['next_action'],
    })
    names = ['five_model_assembly.py', 'API_CONTRATO.md', 'prepare_delivery.py',
             'FONTES_PINADAS.json', 'RECIBO_PREPARACAO_ESTATICA.json', 'DECISAO_IMPLEMENTACAO.json']
    members = []
    for name in names:
        item = pin(HERE / name)
        item['path'] = name
        members.append(item)
    put(HERE / 'MANIFESTO_ENTREGA.json', {
        'request_id': req['request_id'], 'status': 'STATIC_PREPARATION_ONLY',
        'files': members, 'limits': limits,
        'excluded': ['*.bak_*', '*.tmp_*', 'RECIBOS_COORDENACAO.json'],
        'not_authorization_or_execution_receipt': True,
    })
    print(json.dumps({'manifest': pin(HERE / 'MANIFESTO_ENTREGA.json'),
                      'module': pin(module_path), 'structural_metadata': structural,
                      'source_count': len(verified) + 1 + 4, 'limits': limits}, ensure_ascii=False))


if __name__ == '__main__':
    main()
