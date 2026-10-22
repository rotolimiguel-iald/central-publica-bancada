"""Capture only explicitly allowed textual documentation; never follow data links."""
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import urllib.request

BASE = Path(__file__).resolve().parent
DROOT = BASE.parent
ROOT = DROOT.parent.parent
OLD = Path(r'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis')
URLS = {
    'o4_details': 'https://gwosc.org/O4/o4_details/',
    'o4a': 'https://gwosc.org/O4/O4a/',
    'o4b': 'https://gwosc.org/O4/O4b/',
    'o4b_alternate': 'https://gwosc.org/O4/o4b_alternate/',
    'o4_inj': 'https://gwosc.org/O4/o4_inj/',
    'data_flag': 'https://gwosc.org/datadef/',
    'o4a_bits': 'https://gwosc.org/archive/dataset/O4a_16KHZ_R1/json/',
    'o4b_bits': 'https://gwosc.org/archive/dataset/O4b_16KHZ_R1/json/',
    'calibration_dcc': 'https://dcc.ligo-wa.caltech.edu/LIGO-T2500288/public',
    'calibration_readme': 'https://dcc.ligo-wa.caltech.edu/public/0202/T2500288/005/README.txt',
}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def atomic_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() == data:
            return
        raise FileExistsError(f'Refusing replacement: {path}')
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('xb') as f:
        f.write(data)
    if tmp.stat().st_size != len(data):
        raise RuntimeError('Incomplete write')
    os.replace(tmp, path)

class RestrictedRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Even redirects must stay within the explicit documentary whitelist.
        if newurl not in set(URLS.values()):
            raise RuntimeError('Redirect outside documentary whitelist: ' + newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def fetch(item):
    name, url = item
    row = {'id': name, 'url': url, 'retrieved_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
           'scope': 'PUBLIC_TEXT_DOCUMENTATION_ONLY', 'data_links_followed': False}
    try:
        opener = urllib.request.build_opener(RestrictedRedirect)
        req = urllib.request.Request(url, headers={'User-Agent': 'IALD-documentary-audit/1.0'})
        with opener.open(req, timeout=25) as res:
            content_type = res.headers.get_content_type()
            if content_type not in ('text/html', 'text/plain', 'application/json'):
                raise RuntimeError('Unexpected content type: ' + content_type)
            data = res.read(2_000_001)
            if len(data) > 2_000_000:
                raise RuntimeError('Documentary size limit exceeded')
            row.update(final_url=res.url, content_type=content_type)
        suffix = '.json' if content_type == 'application/json' else '.txt' if content_type == 'text/plain' else '.html'
        dest = BASE / 'sources_public' / (name + suffix)
        atomic_new(dest, data)
        row.update(status='CAPTURED_RAW_HTTP_BODY', path=str(dest), bytes=len(data), sha256=digest(data))
    except Exception as exc:
        row.update(status='FETCH_FAILED_VISIBLE', error=f'{type(exc).__name__}: {exc}')
    return row

def main():
    request_path = ROOT / 'D_METADATA_SEMANTICS_REQUEST.json'
    request = json.loads(request_path.read_bytes())
    contract_dir = DROOT / 'd_psd_dq_contract'
    sources = [request_path,
        contract_dir / 'CONTRATO_PSD_DQ_SELECAO_D_PROPOSTA.json',
        contract_dir / 'NOTA_PSD_DQ_SELECAO_D.md',
        contract_dir / 'FONTES_E_LACUNAS.json',
        contract_dir / 'GWOSC_METADATA_EXCERPT.json',
        OLD / 'e2_code_v1_1_2' / 'strain_io.py',
        *[OLD / '015' / 't08' / f'ZENODO_{r}_METADATA.json' for r in (17602505, 20348005, 20348006)]]
    expected = {x['path']: x for x in (request['source_contract'], request['source_note'])}
    old_pins = json.loads((contract_dir / 'FONTES_E_LACUNAS.json').read_bytes())['source_pins']
    expected.update({x['path']: x for x in old_pins})
    pins = []
    for source in sources:
        if source.suffix.lower() not in {'.json', '.md', '.py'}:
            raise RuntimeError('Non-documentary local source refused')
        data = source.read_bytes()
        row = {'source': str(source), 'bytes': len(data), 'sha256': digest(data)}
        if str(source) in expected:
            pin = expected[str(source)]
            if (len(data), digest(data)) != (pin['bytes'], pin['sha256']):
                raise RuntimeError('Source pin mismatch: ' + str(source))
            row['previous_pin_matches'] = True
        dest = BASE / 'sources_local' / source.name
        atomic_new(dest, data)
        row['snapshot'] = str(dest)
        pins.append(row)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        public = list(pool.map(fetch, URLS.items()))
    receipt = {'request_id': request['request_id'], 'created_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'local': pins, 'public': public, 'scientific_containers_opened': False,
        'science_executed': False, 'remote_model_calls': 0}
    atomic_new(BASE / 'SOURCE_CAPTURE.json', (json.dumps(receipt, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    print(json.dumps({'local_sources': len(pins), 'public': [{k: r.get(k) for k in ('id', 'status', 'bytes', 'error')} for r in public]}, ensure_ascii=False))

if __name__ == '__main__':
    main()
