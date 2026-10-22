"""Examples: consultar_contexto.py search '"H2"' --limit 8; ... route H2."""
import argparse
import json
import sqlite3
import sys
from pathlib import Path

root = Path(__file__).resolve().parent / 'contexto'
sys.stdout.reconfigure(encoding='utf-8')
p = argparse.ArgumentParser()
p.add_argument('mode', choices=['search', 'route', 'module'])
p.add_argument('query')
p.add_argument('--limit', type=int, default=8)
a = p.parse_args()
if a.mode == 'search':
    db = sqlite3.connect('file:' + (root / 'busca.sqlite').as_posix() + '?mode=ro', uri=True)
    rows = db.execute('SELECT docs.path, chunks.start_line, snippet(chunks,2,"[", "]", " ... ",40) FROM chunks JOIN docs ON docs.id=chunks.doc_id WHERE chunks MATCH ? ORDER BY bm25(chunks) LIMIT ?', (a.query,a.limit)).fetchall()
    print(json.dumps(rows, ensure_ascii=False, indent=2))
elif a.mode == 'route':
    data = json.loads((root / 'rotas.json').read_text(encoding='utf-8'))
    print(json.dumps({k: [v for v in vals if a.query.lower() in json.dumps(v).lower()] for k,vals in data.items()}, ensure_ascii=False, indent=2))
else:
    data = json.loads((root / 'modulos.json').read_text(encoding='utf-8'))
    print(json.dumps({k:v for k,v in data.items() if a.query.lower() in k.lower()}, ensure_ascii=False, indent=2))
