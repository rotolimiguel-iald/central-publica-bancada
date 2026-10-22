"""Replica verify_delivery/verify_manifest com prefixo de caminho longo do Windows."""
import json, hashlib, os, sys
base = sys.argv[1]
root = '\\\\?\\' + os.path.abspath(base)
man = json.loads(open(os.path.join(root, 'MANIFEST.json'), 'rb').read())
ok = bad = 0; problems = []
for row in man['files']:
    p = os.path.join(root, *row['path'].split('/'))
    try:
        raw = open(p, 'rb').read()
    except Exception as e:
        bad += 1; problems.append((row['path'], 'AUSENTE', str(e)[:80])); continue
    if len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']:
        ok += 1
    else:
        bad += 1; problems.append((row['path'], 'DIVERGE'))
print(json.dumps(dict(base=base[-60:], files=len(man['files']), ok=ok, bad=bad, problems=problems[:10])))
