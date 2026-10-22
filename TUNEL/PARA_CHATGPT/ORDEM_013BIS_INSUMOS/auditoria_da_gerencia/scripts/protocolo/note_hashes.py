import os, re, glob, hashlib, json
D = r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT"
R = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
BS = chr(92)
notes = sorted([f for f in glob.glob(os.path.join(D, "ENTREGA_013_*.md")) if "ESPONTANEA" not in f], key=os.path.getmtime)
cache = {}


def sha(p):
    if p in cache:
        return cache[p]
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for ch in iter(lambda: f.read(8 << 20), b''):
            h.update(ch)
    cache[p] = h.hexdigest()
    return cache[p]


def resolve(tok):
    t = tok.strip('`* ').replace('/mnt/c/', 'C:/').replace(BS, '/')
    cands = []
    if re.match(r'^[A-Za-z]:/', t):
        cands.append(t)
    else:
        cands.append(os.path.join(R, t))
        cands.append(os.path.join(R, 'cache', t))
    for c in cands:
        c = os.path.normpath(c)
        if os.path.isfile(c):
            return c
    return None


pair_re = re.compile(r'`?([^`\s|]+\.(?:json|md|py|zip|npz|h5|csv|txt|hdf5|tar\.gz|svg|png|lean|sh))`?[^0-9a-f\n]{0,40}?`?([0-9a-f]{64})`?')
summary = []
for n in notes:
    t = open(n, encoding='utf-8', errors='replace').read()
    ok = diff = unres = 0
    diffs = []
    for m in pair_re.finditer(t):
        p = resolve(m.group(1))
        if not p:
            unres += 1
            continue
        s = sha(p)
        if s == m.group(2):
            ok += 1
        else:
            diff += 1
            diffs.append((os.path.relpath(p, R) if p.startswith(R) else p, m.group(2)[:16], s[:16]))
    summary.append((os.path.basename(n), ok, diff, unres, diffs))
for s in summary:
    print(f"{s[0][:66]:66s} ok={s[1]:3d} diff={s[2]:3d} unresolved={s[3]:3d}")
    for d in s[4][:8]:
        print("      DIFF", d)
json.dump(summary, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'note_hashes.json'), 'w'), indent=1)
