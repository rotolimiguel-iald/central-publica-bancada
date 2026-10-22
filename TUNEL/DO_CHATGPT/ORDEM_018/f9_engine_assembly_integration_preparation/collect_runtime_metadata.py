"""Read-only WSL filesystem inventory via UNC; no Linux process or imports.

Pins stdlib (including sysconfig), admitted installed distributions and recursive
ELF DT_NEEDED dependencies. This is not an observed import trace or OS isolation.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import posixpath
import struct
import uuid

BASE = Path(__file__).resolve().parent
UNC = '\\\\wsl.localhost\\Ubuntu-24.04'
SITE = '/opt/lal_env/lib/python3.12/site-packages'


def host(p):
    return Path(UNC + p.replace('/', '\\'))


def elf_dynamic(raw):
    if raw[:6] != b'\x7fELF\x02\x01':
        return [], []
    off = struct.unpack_from('<Q', raw, 32)[0]
    size, count = struct.unpack_from('<HH', raw, 54)
    loads, dynamic = [], None
    for i in range(count):
        row = struct.unpack_from('<IIQQQQQQ', raw, off + i * size)
        typ, _, fileoff, address, _, filesz, _, _ = row
        if typ == 1:
            loads.append((address, fileoff, filesz))
        if typ == 2:
            dynamic = (fileoff, filesz)
    if dynamic is None:
        return [], []
    entries = []
    for i in range(dynamic[0], sum(dynamic), 16):
        key, value = struct.unpack_from('<qQ', raw, i)
        if key == 0:
            break
        entries.append((key, value))
    address = next((v for k, v in entries if k == 5), None)
    if address is None:
        return [], []
    stringoff = next(o + address - a for a, o, s in loads if a <= address < a + s)
    def text(offset):
        start = stringoff + offset
        return raw[start:raw.index(b'\0', start)].decode('utf-8')
    return ([text(v) for k, v in entries if k == 1],
            [part for k, v in entries if k in (15, 29) for part in text(v).split(':')])


def main():
    roots = ['/usr/lib/python3.12']
    prefixes = ('camb', 'numpy', 'scipy')
    for p in sorted(host(SITE).iterdir()):
        if any(p.name == name or p.name == name + '.libs'
               or (p.name.startswith(name + '-') and p.name.endswith('.dist-info'))
               for name in prefixes):
            roots.append(SITE + '/' + p.name)
    for name in prefixes:
        assert SITE + '/' + name in roots, name
    paths = {'/usr/bin/python3.12', '/opt/lal_env/pyvenv.cfg'}
    for root in roots:
        for f in host(root).rglob('*'):
            if f.is_file():
                paths.add(root + '/' + f.relative_to(host(root)).as_posix())
    pins, native, missing = {}, {}, []
    queue = sorted(paths)
    search = ['/usr/lib/x86_64-linux-gnu', '/lib/x86_64-linux-gnu', '/usr/lib', '/lib']
    while queue:
        p = queue.pop()
        if p in pins:
            continue
        raw = host(p).read_bytes()
        pins[p] = {'path': p, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        needed, rpaths = elf_dynamic(raw)
        if not needed:
            continue
        dirs = [posixpath.normpath(x.replace('${ORIGIN}', posixpath.dirname(p)).replace('$ORIGIN', posixpath.dirname(p)))
                for x in rpaths] + search
        native[p] = {'needed': needed, 'search_dirs': dirs, 'resolved': {}}
        for name in needed:
            candidates = [posixpath.normpath(posixpath.join(d, name)) for d in dirs]
            found = next((q for q in candidates if host(q).is_file()), None)
            if found is None:
                missing.append({'from': p, 'needed': name, 'candidates': candidates})
            else:
                native[p]['resolved'][name] = found
                queue.append(found)
    loader_aliases = []
    # Interpreter PT_INTERP: the loader path itself, not a DT_NEEDED record.
    raw = host('/usr/bin/python3.12').read_bytes()
    off = struct.unpack_from('<Q', raw, 32)[0]; size, count = struct.unpack_from('<HH', raw, 54)
    for i in range(count):
        row = struct.unpack_from('<IIQQQQQQ', raw, off + i * size)
        if row[0] == 3:
            p = raw[row[2]:row[2]+row[5]].rstrip(b'\0').decode()
            if host(p).is_file():
                data = host(p).read_bytes()
                pins[p] = {'path': p, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
            else:
                candidate = '/usr/lib/x86_64-linux-gnu/' + posixpath.basename(p)
                data = host(candidate).read_bytes()
                pins[candidate] = {'path': candidate, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                loader_aliases.append({'alias_path': p, 'candidate_path': candidate,
                    'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                    'status': 'UNC_ALIAS_UNREADABLE_REQUIRES_LINUX_HASH_COMPARISON_BEFORE_SOLVER'})
    result = {'schema': 'F9_RUNTIME_FILESYSTEM_INVENTORY_V1',
              'created_utc': datetime.now(timezone.utc).isoformat(),
              'status': 'STATIC_PIN_INVENTORY_NOT_DYNAMIC_QUALIFICATION',
              'interpreter': '/opt/lal_env/bin/python', 'interpreter_target': '/usr/bin/python3.12',
              'site_packages': SITE, 'roots': roots, 'pins': [pins[p] for p in sorted(pins)],
              'elf_dependencies': native, 'unresolved_native_dependencies': missing,
              'loader_alias_checks_required': loader_aliases,
              'stdlib_sysconfig_included': '/usr/lib/python3.12/sysconfig.py' in pins,
              'observed_import_trace': False, 'native_OS_reads_observed': False,
              'candidate_imports': 0, 'Linux_processes_started': 0, 'solver_calls': 0,
              'scope_limit': 'Inventory is broader than future actual imports; does not prove dynamic-load closure. Missing import/file reports must name exact identities. No automatic repin/retry.'}
    target = BASE / 'RUNTIME_INVENTORY.json'
    assert not target.exists()
    data = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode()
    temp = target.with_name(target.name + '.tmp_' + uuid.uuid4().hex)
    temp.write_bytes(data); assert temp.read_bytes() == data
    os.replace(temp, target)
    print(json.dumps({'path': str(target), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                      'files': len(pins), 'sysconfig_included': result['stdlib_sysconfig_included'],
                      'unresolved_native_dependencies': missing,
                      'candidate_imports': 0, 'solver_calls': 0}))


if __name__ == '__main__':
    main()
