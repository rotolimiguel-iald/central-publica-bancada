"""Read-only custody verification and local working snapshots for Order 013."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
INPUT = ROOT.parent/'TUNEL/PARA_CHATGPT/ORDEM_013_INSUMOS'
sha = lambda raw: hashlib.sha256(raw).hexdigest()

def main():
    records = []
    for name, expected in json.loads((INPUT/'MANIFESTO_INSUMOS.json').read_bytes())['arquivos'].items():
        path = INPUT/name
        raw = path.read_bytes()
        records.append({'kind':'input','path':str(path.resolve()),'bytes':len(raw),'sha256':sha(raw),
                        'expected_sha16':expected['sha16'],
                        'matches':sha(raw).startswith(expected['sha16']) and len(raw)==expected['bytes']})
    for row in json.loads((INPUT/'FONTES_DA_CASA.json').read_bytes())['fontes']:
        path = Path(row['caminho'])
        raw = path.read_bytes()
        live = path.name in ('MEMORIA_DA_LINHAGEM.md','CLAUDE.md','TUNEL_PROTOCOLO.md')
        records.append({'kind':'live' if live else 'frozen','path':str(path),'bytes':len(raw),
                        'sha256':sha(raw),'expected_sha16':row['sha16'],
                        'matches':sha(raw).startswith(row['sha16']) and len(raw)==row['bytes']})
    mismatches = [r for r in records if not r['matches']]
    report = {'at':datetime.now().astimezone().isoformat(),'records':records,
              'mismatches':mismatches,'frozen_integrity_ok':not any(r['kind']!='live' for r in mismatches)}
    output = ROOT/'custody.json'
    assert not output.exists(), 'Preserve prior audit'
    temp = ROOT/'custody.tmp'
    temp.write_bytes(json.dumps(report,ensure_ascii=False,indent=2).encode())
    temp.replace(output)
    if not report['frozen_integrity_ok']:
        raise SystemExit('Frozen source mismatch: see custody.json')
    for r in records:
        if r['kind'] == 'input':
            continue
        original = Path(r['path'])
        target = ROOT/'cache/casa'/original.name
        if target.exists():
            assert sha(target.read_bytes())==r['sha256']
        else:
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(original,target)
            assert sha(target.read_bytes())==r['sha256']
        r['snapshot'] = str(target)
    index = ROOT/'snapshots.json'
    assert not index.exists()
    index.write_bytes(json.dumps(records,ensure_ascii=False,indent=2).encode())
    print(json.dumps({'files':len(records),'mismatches':mismatches,'frozen_integrity_ok':True},ensure_ascii=False))

if __name__=='__main__': main()
