"""Read-only integrity audit; writes only new bench evidence."""
import hashlib
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt')
INPUTS = ROOT / 'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS'
BENCH = ROOT / 'ORDEM_013_RINGDOWN'
OUT = BENCH / 'bis'

def audit(path, expected):
    row = {'path': str(path), 'expected': expected}
    try:
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        row.update(bytes=len(data), sha256=digest,
                   matches=(digest[:16] == expected['sha16'] and len(data) == expected['bytes']))
    except OSError as exc:
        row.update(matches=False, error=str(exc))
    return row

def main():
    manifest_path = INPUTS / 'MANIFESTO_INSUMOS.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    rows = [audit(INPUTS / name, exp) for name, exp in manifest['arquivos'].items()]
    manifest_digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    manifest_ok = manifest_digest[:16] == '296acf7758ec06b2'
    sources, previous = [], []
    if manifest_ok and all(row['matches'] for row in rows):
        sources = [audit(Path(row['caminho']), row) for row in
                   json.loads((INPUTS/'FONTES_DA_CASA.json').read_text(encoding='utf-8-sig'))['fontes']]
        previous = [audit(BENCH / row['arquivo'], row) for row in
                    json.loads((INPUTS/'ESTADO_AUDITADO.json').read_text(encoding='utf-8-sig'))['artefatos']]
    opening = ROOT/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'
    result = dict(utc=datetime.now(timezone.utc).isoformat(),
                  opening_sha256=hashlib.sha256(opening.read_bytes()).hexdigest(),
                  manifest_sha256=manifest_digest, manifest_matches=manifest_ok,
                  inputs=rows, sources=sources, audited_state=previous,
                  all_frozen_match=manifest_ok and all(x['matches'] for x in rows+sources))
    OUT.mkdir(exist_ok=True)
    target = OUT/('INPUT_INTEGRITY_013BIS' + ('_retry' if '--retry' in sys.argv else '') + '.json')
    if target.exists():
        raise FileExistsError(target)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('inputs','sources','audited_state')}, indent=2))
    for category in ('inputs','sources','audited_state'):
        items = result[category]
        print(category, len(items), 'matched', sum(row['matches'] for row in items))
        for row in items:
            if not row['matches']:
                print(json.dumps(row, ensure_ascii=False))
    print('report_sha256', hashlib.sha256(target.read_bytes()).hexdigest())
    if not result['all_frozen_match']:
        raise SystemExit(2)

if __name__ == '__main__':
    main()
