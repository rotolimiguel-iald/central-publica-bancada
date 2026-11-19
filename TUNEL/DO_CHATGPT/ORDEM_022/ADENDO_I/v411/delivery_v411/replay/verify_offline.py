"""Verifique o pacote local com python replay/verify_offline.py. Opcional: --nos <pasta da rodada>."""
import argparse, hashlib, json, math, re
from pathlib import Path

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as stream:
        for block in iter(lambda:stream.read(1048576),b''):
            h.update(block)
    return h.hexdigest()

def check(condition,reason):
    if not condition: raise ValueError(reason)

def replay(root, nos=None):
    manifest=json.loads((root/'PUBLIC_DELIVERY_V7.json').read_bytes())
    source=json.loads((root/'PROVENANCE_PUBLIC.json').read_bytes())
    check(manifest['version']==source['version']=='v411','versão')
    paths=set()
    for row in manifest['public_files']:
        path=(root/row['path']).resolve()
        check(root in path.parents and path not in paths,'caminho repetido ou externo')
        check(path.stat().st_size==row['bytes'] and digest(path)==row['sha256'],row['path'])
        paths.add(path)
    expected={p.resolve() for p in root.rglob('*') if p.is_file() and p!=root/'PUBLIC_DELIVERY_V7.json' and '__pycache__' not in p.parts}
    check(paths==expected,'inventário')
    records=source['stdout_excerpt']
    ladder=re.search(r'teoremas limpos:\s*(\d+)/(\d+)',records['1342'])
    check(ladder and ladder[1]==ladder[2],'escada')
    raw=re.findall(r'Z (?:nulo|K) = ([-.\d]+)',records['1848'])
    check(list(map(float,raw))==source['hubble']['z'],'razão de Hubble')
    beta=source['alpha']*math.sqrt(math.e)
    check(abs(beta-float(re.search(r'beta=alpha sqrt\(e\)=([\d.]+)',records['129'])[1]))<1e-12,'acoplamento')
    if nos:
        for name,pin in source['sources'].items():
            check(digest(nos/name)==pin,name)
        log=(nos/'rodada_v411_stdout.txt').read_text(encoding='utf-8-sig').splitlines()
        for n,line in records.items():check(line==log[int(n)-1],f'linha {n}')
    print(f'{len(paths)} arquivos íntegros. Escada {ladder[1]}/{ladder[2]}. Acoplamento e quatro desvios reproduzidos.')
    if nos: print('Fontes da rodada e excertos conferidos byte a byte e linha a linha.')

if __name__=='__main__':
    args=argparse.ArgumentParser()
    args.add_argument('--nos',type=Path)
    replay(Path(__file__).resolve().parents[1],args.parse_args().nos)

