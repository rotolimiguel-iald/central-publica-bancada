"""Pin public H0DN source for static review; never import or run upstream code."""
from pathlib import Path
import concurrent.futures
import datetime
import hashlib
import json
import urllib.request

ROOT = Path(__file__).resolve().parent
BASE = 'https://api.github.com/repos/StefCas789/H0DN'
COMMIT = 'cc0a4b9f36e65470d514f254a3c5cffa463fbd94'

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'TGL-documentary-review'})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read()

def write_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise RuntimeError(f'Existing file differs: {path}')
        return
    temp = path.with_name(path.name + '.tmp')
    temp.write_bytes(data)
    assert temp.stat().st_size == len(data) > 0
    temp.replace(path)

def main():
    raw = fetch(BASE + '/git/trees/' + COMMIT + '?recursive=1')
    tree = json.loads(raw)
    assert not tree['truncated']
    write_new(ROOT / 'UPSTREAM_TREE.json', raw)
    selected = [r for r in tree['tree'] if r['type'] == 'blob' and (
        r['path'].startswith('h0_constrainer/')
        or r['path'] in ['README.md', 'data/README.md', 'idlcode/mpinv.pro',
            'idlcode/org_v3p9.pro', 'data/anchors.dat', 'data/groups.dat',
            'data/host_data.dat', 'data/sn1a_covar_pp.dat'])]

    def download(entry):
        relative = entry['path']
        url = 'https://raw.githubusercontent.com/StefCas789/H0DN/' + COMMIT + '/' + relative
        data = fetch(url)
        git_sha = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert git_sha == entry['sha'], relative
        write_new(ROOT / 'upstream' / relative, data)
        return dict(path=relative, url=url, bytes=len(data), git_blob_sha1=git_sha,
                    sha256=hashlib.sha256(data).hexdigest())

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(download, selected))
    manifest = dict(commit=COMMIT, repository='https://github.com/StefCas789/H0DN',
        retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        scope='STATIC_DOCUMENTARY_REVIEW_ONLY_NO_UPSTREAM_EXECUTION_NO_FIT', files=records)
    target = ROOT / 'UPSTREAM_MANIFEST.json'
    if not target.exists():
        write_new(target, (json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode())
    print(json.dumps({'files':len(records), 'bytes':sum(r['bytes'] for r in records),
                      'manifest':str(target), 'commit':COMMIT}))

if __name__ == '__main__':
    main()
