"""Copy installed PyYAML source and license; never access provider credentials."""
from pathlib import Path
import hashlib
import importlib.metadata
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now

BASE = Path(__file__).resolve().parent

def main():
    distribution = importlib.metadata.distribution('PyYAML')
    target = BASE / 'clients/python'
    records = []
    for entry in distribution.files:
        name = str(entry).replace('\\', '/')
        if not ((name.startswith('yaml/') and name.endswith('.py')) or
                name.endswith('.dist-info/licenses/LICENSE')):
            continue
        relative = name if name.startswith('yaml/') else 'PyYAML-LICENSE.txt'
        payload = Path(distribution.locate_file(entry)).read_bytes()
        path = target / relative
        if not path.exists() or path.read_bytes() != payload:
            replace_bytes(path, payload)
        records.append({'path': relative, 'sha256': hashlib.sha256(payload).hexdigest()})
    assert any(r['path'] == 'yaml/__init__.py' for r in records)
    assert any(r['path'] == 'PyYAML-LICENSE.txt' for r in records)
    save_json(target / 'PyYAML-manifest.json', {
        'package': 'PyYAML', 'version': distribution.version,
        'source': 'existing_local_installation', 'copied_at': utc_now(), 'files': records})
    print(f'Copied PyYAML {distribution.version}: {len(records)} source/license files.')

if __name__ == '__main__':
    main()
