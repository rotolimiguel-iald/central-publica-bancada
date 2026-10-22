"""Read-only source audit; receipts are written only inside this A0 directory."""
import datetime
import hashlib
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
BASE = HERE.parents[1]
INPUT = BASE / 'TUNEL/PARA_CHATGPT/ORDEM_016_INSUMOS'
OUT = BASE / 'TUNEL/DO_CHATGPT'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read_json(path):
    return json.loads(path.read_bytes().decode('utf-8-sig'))

def save_new(name, data):
    path = HERE / name
    if path.exists():
        raise FileExistsError(path)
    raw = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    temp = path.with_suffix(path.suffix + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    temp.rename(path)
    print(name, digest(path.read_bytes()))

sources = read_json(INPUT / 'FONTES_DA_CASA.json')
rows = []
entries = [(str(i), e) for i, e in enumerate(sources['fontes_da_015_rehasheadas'])]
entries += list(sources['fontes_novas_da_016'].items())
for name, entry in entries:
    if name.startswith('GERENCIA_') or name == 'PROMPT_MISSAO_FIXO':
        rows.append({'id': name, 'status': 'EXCLUDED_BY_ORDER'})
        continue
    row = {'id': name, 'path': entry['caminho'], 'expected_sha16': entry['sha16']}
    try:
        data = pathlib.Path(entry['caminho']).read_bytes()
        sha = digest(data)
        row.update(bytes=len(data), sha256=sha,
                   status='MATCH' if sha[:16] == entry['sha16'] and len(data) == entry['bytes'] else 'DIFFERENT')
    except OSError as error:
        row.update(status='READ_ERROR', error=str(error))
    rows.append(row)
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
opening = digest((OUT / 'ENTREGA_016_ABERTURA_operador.md').read_bytes())
save_new('sources_audit.json', {'status': 'REAL', 'utc': stamp, 'opening_sha256': opening, 'rows': rows})
print('SOURCE_COUNTS', {s: sum(r['status'] == s for r in rows) for s in sorted({r['status'] for r in rows})})

expected = read_json(INPUT / 'ESTADO_QG_v370.json')
canon = pathlib.Path(sources['fontes_novas_da_016']['CORE_v370']['caminho'])
try:
    core_raw = canon.read_bytes()
    core = json.loads(core_raw)['core']
    seal_path = pathlib.Path(sources['fontes_novas_da_016']['SELO_v370']['caminho'])
    seal = read_json(seal_path)
    closure = core['qg_closure']
    actual = {k: closure[k] for k in ('gate', 'formal_flags', 'physics_flags', 'experiment_flags', 'legitimate_seals', 'closure_order')}
    actual['gate'] = {k: closure['gate'][k] for k in expected['gate']}
    actual['kernel_frontier'] = {k: closure['gate']['kernel_frontier'][k] for k in expected['kernel_frontier']}
    actual['kernel_formalization_gpf_gpi_qgf'] = {k: core['kernel_formalization'][k] for k in expected['kernel_formalization_gpf_gpi_qgf']}
    actual['selo'] = {k: seal[k] for k in expected['selo']}
    comparisons = {k: actual[k] == expected[k] for k in actual}
    save_new('core_audit.json', {'status': 'REAL', 'utc': stamp, 'opening_sha256': opening, 'source_sha256': digest(core_raw), 'comparisons': comparisons, 'actual': actual})
    print('CORE_COMPARISONS', comparisons)
except (OSError, KeyError) as error:
    save_new('core_audit_failure.json', {'status': 'OPEN', 'error': str(error), 'opening_sha256': opening})

anchors = read_json(INPUT / 'JA_EM_KERNEL.json')
kernel = pathlib.Path(anchors['kernel'])
results = []
for group in ('kernel_v370', 'mathlib_da_casa', 'pre_resolvido_pela_gerencia_nos_insumos'):
    root = kernel if group == 'kernel_v370' else kernel / '.lake/packages/mathlib/Mathlib' if group == 'mathlib_da_casa' else INPUT
    for entry in anchors[group]:
        row = dict(entry, group=group)
        try:
            raw = (root / entry['arquivo']).read_bytes()
            lines = raw.decode('utf-8-sig').splitlines()
            name = entry['nome'].split(': ')[-1].split('.')[-1]
            if group == 'mathlib_da_casa':
                name = 'StandardSubspace' if 'StandardSubspace' in entry['nome'] else 'adjoint_toContinuousLinearMap'
            matches = [i for i, line in enumerate(lines, 1) if re.search(r'(?<![\w])' + re.escape(name) + r'(?![\w])', line)]
            row.update(sha256=digest(raw), hash_matches=digest(raw)[:16] == entry['sha16_arquivo'], name_matches=matches,
                       recorded_line_text=lines[entry['linha']-1] if entry['linha'] <= len(lines) else None,
                       name_on_recorded_line=entry['linha'] in matches,
                       status='LOCATED' if matches else 'NAME_NOT_FOUND')
        except OSError as error:
            row.update(status='READ_ERROR', error=str(error))
        results.append(row)
save_new('anchors_audit.json', {'status': 'REAL', 'utc': stamp, 'opening_sha256': opening, 'method': 'Lexical location only; compilation is a separate check.', 'rows': results})
print('ANCHOR_COUNTS', {s: sum(r['status'] == s for r in results) for s in sorted({r['status'] for r in results})})
print('ANCHOR_ISSUES', [{k: r.get(k) for k in ('nome','status','hash_matches','name_on_recorded_line')} for r in results if r['status'] != 'LOCATED' or not r.get('hash_matches') or not r.get('name_on_recorded_line')])

package = INPUT / 'PACOTE_FISICA_v370'
manifest = read_json(package / 'MANIFESTO_LOCAL.json')
package_rows = []
for entry in manifest['files']:
    raw = (package / entry['name']).read_bytes()
    package_rows.append({'name': entry['name'], 'bytes': len(raw), 'sha256': digest(raw), 'matches': len(raw) == entry['bytes'] and digest(raw) == entry['sha256']})
save_new('package_audit.json', {'status': 'REAL', 'utc': stamp, 'opening_sha256': opening, 'manifest_sha256': digest((package/'MANIFESTO_LOCAL.json').read_bytes()), 'rows': package_rows})
print('PACKAGE_MATCH',sum(x['matches'] for x in package_rows),len(package_rows))
