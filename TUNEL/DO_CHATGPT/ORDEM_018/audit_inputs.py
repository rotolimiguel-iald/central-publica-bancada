"""Verify supplied bytes, preserve evidence, and avoid executing scientific inputs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parent
INPUT = ROOT.parents[1] / 'PARA_CHATGPT' / 'ORDEM_018_INSUMOS'

def safe_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        data = data.encode('utf-8')
    if path.exists():
        old = path.read_bytes()
        if old == data:
            return
        stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        backup = path.with_name(path.name + '.bak_' + stamp)
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    tmp = path.with_name(path.name + '.tmp_' + str(os.getpid()))
    tmp.write_bytes(data)
    assert tmp.read_bytes() == data and len(data) > 0
    os.replace(tmp, path)
    assert path.read_bytes() == data

def save_json(path, obj):
    safe_write(path, json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def file_info(path):
    path = Path(path)
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def main():
    manifest_path = INPUT / 'MANIFESTO_INSUMOS.json'
    manifest = json.loads(manifest_path.read_bytes())
    results = []
    for name, expected in manifest['arquivos'].items():
        actual = file_info(INPUT / name)
        actual['matches_manifest'] = all(actual[k] == expected[k] for k in ('bytes', 'sha256'))
        results.append(actual)
    order = file_info(INPUT.parent / 'ORDEM_018_o_discriminante.md')
    order['matches_manifest'] = (order['sha256'] == manifest['ordem_sha256'] and order['bytes'] == manifest['ordem_bytes'])
    report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'manifest': file_info(manifest_path),
              'order': order, 'files': results, 'all_match': all(r['matches_manifest'] for r in results) and order['matches_manifest'],
              'scope': 'Byte integrity only; not scientific validation or authorization to open data for verdict.'}
    save_json(ROOT / 'AUDITORIA_INSUMOS.json', report)
    print(json.dumps({'files': len(results), 'all_match': report['all_match'], 'order_sha256': order['sha256']}))
    assert report['all_match']

if __name__ == '__main__':
    main()
