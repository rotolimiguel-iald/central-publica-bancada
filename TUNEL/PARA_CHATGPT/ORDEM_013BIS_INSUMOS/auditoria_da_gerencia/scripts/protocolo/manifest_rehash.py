import json, os, hashlib
root = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
m = json.load(open(os.path.join(root, 'cache', 'MANIFESTO_DOWNLOADS.json'), encoding='utf-8'))
BS = chr(92)


def norm(p):
    p = p.replace('/mnt/c/', 'C:/').replace(BS, '/')
    if not os.path.isabs(p):
        p = os.path.join(root, p)
    return os.path.normcase(os.path.normpath(p))


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for ch in iter(lambda: f.read(8 << 20), b''):
            h.update(ch)
    return h.hexdigest()


res = {'ok': 0, 'bad': [], 'missing': [], 'total_bytes_listed': 0}
listed = set()
for x in m['files']:
    p = norm(x['path'])
    listed.add(p)
    if not os.path.exists(p):
        res['missing'].append(x['path'])
        continue
    s = sha(p)
    size = os.path.getsize(p)
    res['total_bytes_listed'] += size
    if s == x['sha256'] and size == x.get('bytes', size):
        res['ok'] += 1
    else:
        res['bad'].append((x['path'], s, x['sha256'], size, x.get('bytes')))

big_outside = []
unlisted_big = []
tot = 0
denied = []
count = 0
for dp, ds, fs in os.walk(root, onerror=lambda e: denied.append(str(e))):
    for f in fs:
        p = os.path.join(dp, f)
        try:
            s = os.path.getsize(p)
        except Exception:
            denied.append(p)
            continue
        tot += s
        count += 1
        rel = os.path.relpath(p, root)
        if s > 25 * 1024 * 1024 and not rel.lower().startswith('cache' + os.sep):
            big_outside.append((rel, s))
        if s > 25 * 1024 * 1024 and os.path.normcase(os.path.normpath(p)) not in listed:
            unlisted_big.append((rel, s))
res.update(big_outside_cache=big_outside, unlisted_big_files=unlisted_big,
           tree_total_bytes=tot, tree_file_count=count, walk_denied=denied)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'manifest_rehash_result.json')
json.dump(res, open(out, 'w'), indent=1)
print(json.dumps({k: (v if not isinstance(v, list) else v[:40]) for k, v in res.items()}, indent=1))
