"""Archive public primary HTML; no upstream execution, fits or model calls."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import json
import urllib.request

ROOT = Path(__file__).resolve().parent
SOURCES = {
    'h0dn': 'https://arxiv.org/html/2510.23823v1',
    'jagb_cchp': 'https://arxiv.org/html/2408.03474v2',
    'jagb_sh0es': 'https://arxiv.org/html/2502.05259v2',
    'method_comparison': 'https://arxiv.org/html/2408.11770v2',
    'cchp_overview': 'https://arxiv.org/html/2408.06153v3',
}

class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.skip += 1
        if tag in ('p', 'tr', 'h1', 'h2', 'h3', 'h4', 'h5'): self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip -= 1
        if tag in ('p', 'tr', 'h1', 'h2', 'h3', 'h4', 'h5'): self.parts.append('\n')
        elif tag == 'td': self.parts.append(' | ')
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)

def write_new(path, data):
    if path.exists():
        if path.read_bytes() != data: raise RuntimeError('Existing artifact differs: '+str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix+'.tmp')
    with temp.open('xb') as out: out.write(data)
    if temp.stat().st_size != len(data): raise RuntimeError('Short write')
    temp.replace(path)

def fetch(item):
    name, url = item
    path = ROOT/'sources'/(name+'.html')
    if path.exists(): raw = path.read_bytes()
    else:
        req = urllib.request.Request(url, headers={'User-Agent': 'IALD-documentary-review/1.0'})
        with urllib.request.urlopen(req, timeout=45) as r: raw = r.read()
        if len(raw) < 10000: raise RuntimeError('Incomplete HTML: '+url)
        write_new(path, raw)
    parser = Text(); parser.feed(raw.decode('utf-8'))
    lines = [' '.join(s.split()) for s in ''.join(parser.parts).splitlines()]
    text = ('\n'.join(s for s in lines if s)+'\n').encode('utf-8')
    derived = path.with_suffix('.txt'); write_new(derived, text)
    return {'id': name, 'url': url, 'path': str(path), 'bytes': len(raw),
            'sha256': sha256(raw).hexdigest(), 'text_path': str(derived),
            'text_sha256': sha256(text).hexdigest(),
            'note': 'Full public HTML cached. TXT is a derived locator, not the original; equations may have duplicate accessibility text.'}

def main():
    with ThreadPoolExecutor(max_workers=3) as pool: entries = list(pool.map(fetch, SOURCES.items()))
    manifest = ROOT/'PRIMARY_SOURCES.json'
    if not manifest.exists():
        write_new(manifest, (json.dumps({'retrieved_utc': datetime.now(timezone.utc).isoformat(),
            'request_id': '54feb986-d927-4ff9-aa69-3c07680ee78b', 'files': entries},
            indent=2, ensure_ascii=False)+'\n').encode())
    else:
        assert json.loads(manifest.read_text(encoding='utf-8'))['files'] == entries
    print(json.dumps([{'id': e['id'], 'bytes': e['bytes']} for e in entries]))

if __name__ == '__main__': main()
