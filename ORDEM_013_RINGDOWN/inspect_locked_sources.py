"""Search source distributions pinned by the release without importing them."""
from pathlib import Path
import hashlib
import json
import tarfile
from fetch_public import atomic_json
ROOT=Path(__file__).resolve().parent

def main():
    folder=ROOT/'cache/source_distributions'
    manifest=json.loads((folder/'manifest.json').read_bytes());records=[]
    for entry in manifest['packages']:
        path=folder/Path(entry['url']).name
        if hashlib.sha256(path.read_bytes()).hexdigest()!=entry['sha256']:raise ValueError('Archive changed')
        with tarfile.open(path,'r:gz') as tar:
            for member in tar:
                if not member.isfile() or not member.name.endswith(('.py','.pyx')):continue
                raw=tar.extractfile(member).read();text=raw.decode(errors='replace');lines=text.splitlines()
                terms=('TEOBResumSPM','dtau_','Jimenez','Jiménez','final_spin_non_evolved','_final_from_initial')
                hits=[(i+1,line[:300]) for i,line in enumerate(lines) if any(k in line for k in terms)]
                if not hits:continue
                dest=folder/'selected'/(hashlib.sha256(member.name.encode()).hexdigest()[:16]+Path(member.name).suffix)
                dest.parent.mkdir(exist_ok=True)
                if dest.exists() and dest.read_bytes()!=raw:raise ValueError('Cached source changed')
                if not dest.exists():
                    temp=dest.with_suffix(dest.suffix+'.tmp');temp.write_bytes(raw);temp.replace(dest)
                row=dict(package=entry['package'],member=member.name,path=str(dest),sha256=hashlib.sha256(raw).hexdigest(),hits=hits)
                records.append(row)
                print(json.dumps(dict(package=entry['package'],member=member.name,local=dest.name,hits=hits[:18])),flush=True)
    atomic_json(folder/'source_index.json',dict(sources=records,executed=False))

if __name__=='__main__':main()
