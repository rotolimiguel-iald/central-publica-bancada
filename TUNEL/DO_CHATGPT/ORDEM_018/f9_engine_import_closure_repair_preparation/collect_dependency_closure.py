"""Read installed dependency bytes through UNC; never import or launch them."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import ast
import hashlib
import json
import os
import struct
import uuid

BASE = Path(__file__).resolve().parent
OLD = BASE.parent / 'f9_engine_assembly_integration_preparation'
UNC = r'\\wsl.localhost\Ubuntu-24.04'
SITE = '/opt/lal_env/lib/python3.12/site-packages'
PACKAGE = SITE + '/charset_normalizer'
ZIP = '/usr/lib/python312.zip'


def host(path):
    return Path(UNC + path.replace('/', '\\'))


def pin(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def fresh_json(path, value):
    assert not path.exists(), 'Collection already exists; do not silently repin'
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
    tmp = path.with_name(path.name + '.tmp_' + uuid.uuid4().hex)
    tmp.write_bytes(raw)
    assert tmp.read_bytes() == raw
    os.replace(tmp, path)
    assert path.read_bytes() == raw


def elf(raw):
    if raw[:6] != b'\x7fELF\x02\x01':
        raise ValueError('Expected little-endian 64-bit ELF')
    offset = struct.unpack_from('<Q', raw, 32)[0]
    width, count = struct.unpack_from('<HH', raw, 54)
    loads, section = [], None
    for n in range(count):
        row = struct.unpack_from('<IIQQQQQQ', raw, offset + n * width)
        if row[0] == 1:
            loads.append((row[3], row[2], row[5]))
        if row[0] == 2:
            section = (row[2], row[5])
    if section is None:
        return {'needed': [], 'soname': None, 'rpath': []}
    entries = []
    for n in range(section[0], sum(section), 16):
        key, value = struct.unpack_from('<qQ', raw, n)
        if key == 0:
            break
        entries.append((key, value))
    address = next(v for k, v in entries if k == 5)
    start = next(o + address - a for a, o, s in loads if a <= address < a+s)
    def string(v):
        pos = start + v
        return raw[pos:raw.index(b'\0', pos)].decode()
    return {'needed': [string(v) for k, v in entries if k == 1],
            'soname': next((string(v) for k, v in entries if k == 14), None),
            'rpath': [string(v) for k, v in entries if k in (15, 29)]}


def main():
    original_raw = (OLD / 'RUNTIME_INVENTORY.json').read_bytes()
    inventory = json.loads(original_raw)
    original_pins = {x['path']: x for x in inventory['pins']}
    pins = dict(original_pins)
    discovered, edges, externals, dynamic_sites = {}, [], set(), []
    todo = ['charset_normalizer']
    while todo:
        module = todo.pop()
        if module in discovered:
            continue
        suffix = module.split('.', 1)[1] if '.' in module else '__init__'
        path = PACKAGE + '/' + suffix.replace('.', '/') + '.py'
        raw = host(path).read_bytes()
        tree = ast.parse(raw, filename=path)
        discovered[module] = path
        pins[path] = {'path': path, **pin(raw)}
        lines = raw.decode('utf-8').splitlines()
        for node in ast.walk(tree):
            targets = []
            if isinstance(node, ast.Import):
                targets = [x.name for x in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    assert node.level == 1 and node.module, 'Unresolved relative import'
                    targets = ['charset_normalizer.' + node.module]
                elif node.module:
                    targets = [node.module]
            for target in targets:
                edges.append({'source': path, 'line': node.lineno, 'target': target})
                if target == 'charset_normalizer' or target.startswith('charset_normalizer.'):
                    todo.append(target)
                else:
                    externals.add(target)
            if isinstance(node, ast.Call) and (
                isinstance(node.func, ast.Attribute) and node.func.attr == 'import_module'
                or isinstance(node.func, ast.Name) and node.func.id == '__import__'
            ):
                dynamic_sites.append({'source': path, 'line': node.lineno,
                    'text': '\n'.join(lines[max(0,node.lineno-2):min(len(lines),node.end_lineno+1)])})
    cache_metadata, native = [], []
    for module, path in sorted(discovered.items()):
        src = host(path)
        cache = str(PurePosixPath(path).parent / '__pycache__' /
                    (src.stem + '.cpython-312.pyc'))
        # Preserve existing cache bytes too: -B prohibits writing, not reading.
        try:
            raw = host(cache).read_bytes()
        except FileNotFoundError:
            cache_metadata.append({'path': cache, 'exists': False})
        else:
            assert len(raw) >= 16
            pins[cache] = {'path': cache, **pin(raw)}
            flags, timestamp, size = struct.unpack_from('<III', raw, 4)
            st = src.stat()
            cache_metadata.append({'path': cache, 'exists': True,
                'magic_hex': raw[:4].hex(), 'flags': flags,
                'timestamp_header': timestamp, 'source_size_header': size,
                'source_mtime_seconds': int(st.st_mtime), 'source_bytes': st.st_size,
                'timestamp_and_size_match': None if flags & 1 else
                    timestamp == (int(st.st_mtime) & 0xffffffff) and size == st.st_size,
                'bytecode_not_loaded_or_decoded': True})
        for binary in sorted(src.parent.glob(src.stem + '.cpython-312-*.so')):
            path_so = str(PurePosixPath(path).parent / binary.name)
            raw = binary.read_bytes()
            pins[path_so] = {'path': path_so, **pin(raw)}
            native.append({'path': path_so, **elf(raw),
                'scope': 'ELF metadata only; binary was not loaded'})
    # METADATA identifies one installed distribution, not all of site-packages.
    distributions = sorted(host(SITE).glob('charset_normalizer-*.dist-info'))
    assert len(distributions) == 1, 'Ambiguous installed distribution'
    dist = distributions[0]
    metadata = (dist/'METADATA').read_text(encoding='utf-8')
    metadata_headers = metadata.split('\n\n', 1)[0].splitlines()
    requirements = [x for x in metadata_headers if x.startswith('Requires-Dist:')]
    assert not requirements, 'New distribution requirement needs explicit resolution'
    distroot = SITE + '/' + dist.name
    for path in sorted(dist.rglob('*')):
        if path.is_file():
            name = distroot + '/' + path.relative_to(dist).as_posix()
            pins[name] = {'path': name, **pin(path.read_bytes())}
    # All discovered absolute Python imports must already resolve in the pinned stdlib.
    config_path = '/usr/lib/python3.12/_sysconfigdata__x86_64-linux-gnu.py'
    config_raw = host(config_path).read_bytes()
    assert pin(config_raw) == {k: original_pins[config_path][k] for k in ('bytes','sha256')}
    config_tree = ast.parse(config_raw, filename=config_path)
    build = ast.literal_eval(next(n.value for n in config_tree.body if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == 'build_time_vars' for t in n.targets)))
    builtin_names = set(build['MODBUILT_NAMES'].split())
    inittab_path = '/usr/lib/python3.12/config-3.12-x86_64-linux-gnu/config.c'
    inittab_raw = host(inittab_path).read_bytes()
    assert pin(inittab_raw) == {k: original_pins[inittab_path][k] for k in ('bytes','sha256')}
    required_builtins, stdlib_checks = [], []
    for name in sorted(externals):
        root = name.split('.')[0]
        candidates = [p for p in original_pins if p == '/usr/lib/python3.12/'+root+'.py'
            or p.startswith('/usr/lib/python3.12/'+root+'/')
            or p.startswith('/usr/lib/python3.12/lib-dynload/'+root+'.')]
        if not candidates:
            assert root in builtin_names and ('{"'+root+'", PyInit_'+root+'}').encode() in inittab_raw, 'Unresolved external module: '+name
            required_builtins.append(root)
        stdlib_checks.append({'module': name, 'existing_pinned_candidates': candidates,
            'builtin_in_pinned_build_metadata': root in required_builtins})
    # Recursive native edges must terminate in unchanged, previously inventoried ELF.
    aliases = inventory.get('loader_alias_checks_required', []) + inventory['alias_resolution_metadata']['checks_required_in_Linux']
    native_edges, done, queue = [], set(), list(native)
    while queue:
        item = queue.pop()
        if item['path'] in done:
            continue
        done.add(item['path'])
        for name in item['needed']:
            matches = [a for a in aliases if PurePosixPath(a['alias_path']).name == name]
            direct = [p for p in original_pins if PurePosixPath(p).name == name]
            candidates = sorted(set(direct + [a['candidate_path'] for a in matches]))
            assert candidates, 'Unresolved native dependency: '+name
            identities = set()
            resolved = []
            for path in candidates:
                raw = host(path).read_bytes()
                assert pin(raw) == {k: original_pins[path][k] for k in ('bytes','sha256')}
                identities.add(pin(raw)['sha256'])
                facts = elf(raw)
                assert facts['soname'] == name, 'ELF SONAME mismatch'
                resolved.append({'path': path, **facts})
            assert len(identities) == 1, 'Ambiguous native bytes'
            native_edges.append({'from': item['path'], 'needed': name,
                'existing_candidates': candidates, 'alias_checks_retained': matches,
                'resolution_status': 'PINNED_CANDIDATE_RUNTIME_ALIAS_CHECK_STILL_REQUIRED'})
            queue.extend(resolved)
    # A missing exact ZIP pathname is a no-content probe, never permission to read it.
    try:
        host(ZIP).lstat()
    except FileNotFoundError:
        zip_state = {'path': ZIP, 'absent_now_via_UNC': True,
                     'runtime_recheck': 'LSTAT_ENOENT_ONLY_BEFORE_IMPORT_AND_EACH_OPEN'}
    else:
        raise RuntimeError('Exact ZIP probe exists; no content admitted')
    additions = [pins[p] for p in sorted(pins) if p not in original_pins]
    assert all(pins[p] == original_pins[p] for p in original_pins)
    inventory['pins'] = [pins[p] for p in sorted(pins)]
    inventory['roots'] += [PACKAGE, distroot]
    inventory['exact_absent_probe_paths'] = [ZIP]
    inventory['required_builtin_modules'] = sorted(set(required_builtins))
    inventory['created_utc'] = datetime.now(timezone.utc).isoformat()
    inventory['status'] = 'STATIC_DEPENDENCY_DELTA_NOT_DYNAMIC_QUALIFICATION'
    inventory['dependency_repair'] = {'original_inventory': pin(original_raw),
        'package': 'charset_normalizer', 'added_files': len(additions),
        'exact_absent_probe': ZIP, 'old_pins_unchanged': True,
        'candidate_imports': 0, 'Linux_processes_started': 0, 'solver_calls': 0}
    evidence = {'at_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'STATIC_SOURCE_AND_ELF_DEPENDENCY_CLOSURE',
        'old_inventory': pin(original_raw), 'python_modules': discovered,
        'import_edges': edges, 'external_stdlib_coverage': stdlib_checks,
        'dynamic_import_sites': dynamic_sites, 'cache_headers': cache_metadata,
        'builtin_metadata': {'sysconfig': {'path': config_path, **pin(config_raw)},
            'inittab': {'path': inittab_path, **pin(inittab_raw)},
            'names_required_in_runtime_builtin_module_names': sorted(set(required_builtins))},
        'ELF_objects': native, 'recursive_ELF_edges': native_edges,
        'distribution_metadata_headers': metadata_headers,
        'new_runtime_pins': additions, 'zip_state': zip_state,
        'excluded': ['charset_normalizer CLI', 'charset_normalizer __main__',
                     'other site-packages distributions', 'observed datasets'],
        'scope': 'Source graph and ELF DT_NEEDED; not complete dynamic trace or native syscall isolation',
        'candidate_imports': 0, 'solver_calls': 0, 'Linux_processes_started': 0}
    fresh_json(BASE/'DEPENDENCY_CLOSURE_EVIDENCE.json', evidence)
    fresh_json(BASE/'RUNTIME_INVENTORY.json', inventory)
    print(json.dumps({'added_files': len(additions), 'runtime_files': len(pins),
        'python_modules': len(discovered), 'ELF_objects': len(native),
        'ELF_edges': len(native_edges), 'dynamic_import_sites': dynamic_sites,
        'runtime_inventory': pin((BASE/'RUNTIME_INVENTORY.json').read_bytes()),
        'candidate_imports': 0, 'solver_calls': 0}))


if __name__ == '__main__':
    main()
