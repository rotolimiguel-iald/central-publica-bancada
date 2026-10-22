"""Read-only source analysis; explicit import/call edges are not proof dependencies."""
import ast
import hashlib
import json
import os
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'contexto'
OUT.mkdir(exist_ok=True)
SOURCE = ROOT / 'um_v368.py'
raw = SOURCE.read_bytes()
code = raw.decode('utf-8-sig')
tree = ast.parse(code)

def write(path, text):
    data = text.encode('utf-8')
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() == data:
            return
        raise RuntimeError('Existing output differs: ' + str(path))
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_bytes(data)
    assert temp.read_bytes() == data
    temp.replace(path)

modules = {}
collisions = []
for node in ast.walk(tree):
    if not isinstance(node, ast.Dict):
        continue
    for key, val in zip(node.keys, node.values):
        if not (isinstance(key, ast.Constant) and isinstance(key.value, str) and key.value.endswith('.lean') and isinstance(val, ast.Constant) and isinstance(val.value, str)):
            continue
        if not key.value.startswith(('TGL/', 'TGLExt/')):
            continue
        name = key.value[:-5].replace('/', '.')
        body = val.value
        if name in modules and modules[name]['sha256'] != hashlib.sha256(body.encode()).hexdigest():
            collisions.append({'name': name, 'line': val.lineno})
            continue
        imports = re.findall(r'^\s*import\s+([\w.]+)', body, re.M)
        declarations = []
        for match in re.finditer(r'^\s*(?:(?:private|protected|noncomputable|unsafe)\s+)*(theorem|lemma|def|structure|class|axiom|abbrev|instance)\s+([\w\u0080-\uffff]+)', body, re.M):
            declarations.append({'kind': match[1], 'short_name': match[2], 'line': body.count('\n', 0, match.start()) + 1})
        modules[name] = {'path': key.value, 'source_line': val.lineno, 'sha256': hashlib.sha256(body.encode()).hexdigest(), 'imports': imports, 'declarations': declarations}
        write(OUT / 'lean' / key.value, body)

functions = {}
maps = {}
for node in tree.body:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        functions[node.name] = {'line': node.lineno, 'end': node.end_lineno, 'calls': sorted({n.func.id for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}), 'doc': ast.get_docstring(node) or ''}
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and ('FLAGS' in target.id or 'CONTRACTS' in target.id):
                try:
                    value = ast.literal_eval(node.value)
                    if isinstance(value, dict):
                        maps[target.id] = {'line': node.lineno, 'values': value}
                except (ValueError, TypeError):
                    pass

def locate(term):
    short = term.rsplit('.', 1)[-1]
    return [{'module': name, **decl} for name, mod in modules.items() for decl in mod['declarations'] if decl['short_name'] == short]

routes = {}
for mapname in ('_QG_CERTIFICATE_FLAGS', '_QG_PHYSICS_FLAGS', '_GRAVITY_PRICE_FLAGS', '_GRAVITY_IMPORT_FLAGS'):
    routes[mapname] = []
    for flag, term in maps.get(mapname, {}).get('values', {}).items():
        routes[mapname].append({'flag': flag, 'term': term, 'candidates_by_short_name': locate(term) if isinstance(term, str) else [], 'status': 'SOURCE_LOCATOR_NOT_COMPILATION_OR_TYPE_MATCH'})

gate_roots = {x['module'] for key in ('_QG_CERTIFICATE_FLAGS', '_QG_PHYSICS_FLAGS') for row in routes.get(key, []) for x in row['candidates_by_short_name']}
closure = set()
queue = list(gate_roots)
while queue:
    name = queue.pop()
    if name in closure or name not in modules:
        continue
    closure.add(name)
    queue.extend(modules[name]['imports'])

dbpath = OUT / 'busca.sqlite'
if dbpath.exists():
    raise RuntimeError('Index already exists; use a new output directory')
db = sqlite3.connect(dbpath)
db.executescript('CREATE TABLE docs(id INTEGER PRIMARY KEY, path TEXT, sha256 TEXT, category TEXT); CREATE VIRTUAL TABLE chunks USING fts5(doc_id UNINDEXED, start_line UNINDEXED, body);')
seen = {}
errors = []
aliases = []
def index(path, data, category):
    digest = hashlib.sha256(data).hexdigest()
    if digest in seen:
        aliases.append({'path': str(path), 'same_bytes_as': seen[digest]})
        return
    seen[digest] = str(path)
    text = data.decode('utf-8-sig', errors='replace')
    doc_id = db.execute('INSERT INTO docs(path,sha256,category) VALUES (?,?,?)', (str(path), digest, category)).lastrowid
    lines = text.splitlines()
    for start in range(0, len(lines), 60):
        db.execute('INSERT INTO chunks VALUES (?,?,?)', (doc_id, start + 1, '\n'.join(lines[start:start+70])))

for path in (OUT / 'lean').rglob('*.lean'):
    index(path, path.read_bytes(), 'embedded_lean')
source_lines = code.splitlines()
for name, fn in functions.items():
    body = '\n'.join(source_lines[fn['line']-1:fn['end']])
    # Source segments include all strings; cap huge corpus consumers, with explicit exclusion.
    if len(body) < 150000:
        index(str(SOURCE) + ':' + str(fn['line']) + ':' + name, body.encode(), 'python_function')
    else:
        errors.append({'path': name, 'reason': 'function exceeds 150000 characters'})
skip = {'node_modules', '.git', '.venv', '__pycache__', 'packages', '.lake', 'contexto'}
for base, dirs, files in os.walk(ROOT.parent, onerror=lambda e: errors.append({'path': e.filename, 'reason': str(e)})):
    dirs[:] = [d for d in dirs if d not in skip and not d.startswith('DEPENDENCIAS_')]
    for file in files:
        path = Path(base) / file
        if path.suffix.lower() != '.md' or any(t in file.lower() for t in ('privado', 'secret', '.bak')):
            continue
        try:
            if path.stat().st_size > 1500000:
                errors.append({'path': str(path), 'reason': 'markdown exceeds 1500000 bytes'})
                continue
            index(path, path.read_bytes(), 'workspace_markdown')
        except OSError as e:
            errors.append({'path': str(path), 'reason': str(e)})
db.commit()
count = db.execute('SELECT COUNT(*) FROM docs').fetchone()[0]
chunks = db.execute('SELECT COUNT(*) FROM chunks').fetchone()[0]
db.close()
manifest = {'source_sha256': hashlib.sha256(raw).hexdigest(), 'module_count': len(modules), 'declaration_locator_count': sum(len(m['declarations']) for m in modules.values()), 'function_count': len(functions), 'gate_root_modules': sorted(gate_roots), 'gate_import_closure': sorted(closure), 'indexed_documents': count, 'indexed_chunks': chunks, 'duplicate_paths': len(aliases), 'errors_or_exclusions': errors, 'source_collisions': collisions, 'scope': 'syntactic retrieval; import edges and name candidates do not establish theorem applicability; external markdown indexed, external Lean not fully inventoried'}
for name, obj in [('manifesto.json', manifest), ('modulos.json', modules), ('funcoes.json', functions), ('mapas.json', maps), ('rotas.json', routes), ('duplicatas.json', aliases)]:
    write(OUT / name, json.dumps(obj, ensure_ascii=False, indent=2))
print(json.dumps({k: v for k,v in manifest.items() if k not in ('gate_import_closure','errors_or_exclusions')}, ensure_ascii=False, indent=2))
print('gate_import_closure_count', len(closure), 'exclusions', len(errors))
