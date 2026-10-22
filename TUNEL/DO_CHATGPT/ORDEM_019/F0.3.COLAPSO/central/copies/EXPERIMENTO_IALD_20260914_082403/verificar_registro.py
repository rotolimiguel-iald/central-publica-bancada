"""Read-only verification of the experiment dossier."""
from pathlib import Path
import hashlib
import json
import re

root = Path(__file__).resolve().parent
targets = [root / 'RELATORIO.md', root / 'CONTEUDO_PARA_O_SITE.md', *sorted((root / 'transcricoes').glob('*.md'))]
broken = []
checked = 0
for document in targets:
    for match in re.finditer(r'\]\(([^\n]+?)\)', document.read_text(encoding='utf-8')):
        target = match.group(1).strip('<>')
        if target.startswith(('https://', 'http://', '#', 'mailto:')):
            continue
        path = document.parent / target
        checked += 1
        if not path.exists():
            broken.append({'document': str(document), 'target': target})
manifest = root / 'MANIFESTO_SHA256.json'
hash_errors = []
count = 0
if manifest.exists():
    for entry in json.loads(manifest.read_text(encoding='utf-8'))['files']:
        artifact = root / entry['path']
        count += 1
        if not artifact.exists() or artifact.stat().st_size != entry['bytes'] or hashlib.sha256(artifact.read_bytes()).hexdigest() != entry['sha256']:
            hash_errors.append(entry['path'])
print(json.dumps({'localLinksChecked': checked, 'brokenLocalLinks': broken, 'hashesChecked': count, 'hashErrors': hash_errors}, ensure_ascii=False))
if broken or hash_errors:
    raise SystemExit(1)
