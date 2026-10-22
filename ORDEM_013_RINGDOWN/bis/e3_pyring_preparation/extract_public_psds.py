"""Extract exactly two regular PSD texts; no execution, pickle or posterior read."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,tarfile,time
HERE=Path(__file__).resolve().parent;B=HERE.parents[1]


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    started=time.perf_counter()
    # Preserve the initial preparation, including exact code and manifest bytes.
    snapshot=HERE/'snapshots/pre_public_psd_001';snapshot.mkdir(parents=True,exist_ok=False)
    snapshot_pins={}
    for p in sorted(HERE.iterdir()):
        if p.is_file():
            raw=p.read_bytes()
            with (snapshot/p.name).open('xb') as f:f.write(raw)
            if (snapshot/p.name).read_bytes()!=raw:raise OSError('Snapshot mismatch')
            snapshot_pins[p.name]=hashlib.sha256(raw).hexdigest()
    with (snapshot/'SNAPSHOT_RECEIPT.json').open('x',encoding='utf-8') as f:
        json.dump(snapshot_pins,f,indent=2);f.write('\n')
    index_path=B/'cache/public/17018009/archive_index.json'
    index=json.loads(index_path.read_bytes())
    members=[m for m in index['members'] if m['name'].endswith(('_H1_psd.dat','_L1_psd.dat')) and '/bilby-NRSur7dq4_prod/pesummary/psds/' in m['name']]
    if len(members)!=2 or not all(m['regular'] and not m['link'] and m['size']<5_000_000 for m in members):raise ValueError('Ambiguous/unsafe PSD members')
    wanted={m['name']:m for m in members}
    archive_path=B/'cache/public/17018009/TGR_companion_S250114ax_results.tar.gz'
    destination=B/'cache/E3_KERR220_PSD_INPUTS';destination.mkdir(exist_ok=False)
    h=hashlib.sha256();found={}
    class HashedReader:
        def __init__(self,stream):self.stream=stream
        def read(self,size=-1):
            raw=self.stream.read(size);h.update(raw);return raw
    with archive_path.open('rb') as stream:
        reader=HashedReader(stream)
        with tarfile.open(fileobj=reader,mode='r|gz') as tar:
            for member in tar:
                if member.name not in wanted:continue
                if member.name in found or not member.isfile() or member.issym() or member.islnk() or member.size!=wanted[member.name]['size']:
                    raise ValueError('Unsafe/duplicate PSD archive entry')
                raw=tar.extractfile(member).read()
                if len(raw)!=member.size:raise OSError('Incomplete member')
                target=destination/Path(member.name).name
                if target.resolve().parent!=destination.resolve():raise ValueError('Extraction path escaped')
                with target.open('xb') as f:f.write(raw)
                # Schema only; no spectrum, posterior or strain calculation.
                lines=raw.decode('utf-8').splitlines()
                sample=[line.split() for line in lines if line.strip() and not line.startswith('#')][:3]
                schema='two_numeric_columns' if sample and all(len(row)==2 for row in sample) else 'REVIEW_REQUIRED'
                for row in sample:
                    for value in row:float(value)
                found[member.name]=dict(path=str(target),relative_to_Chatgpt=target.relative_to(B.parent).as_posix(),
                  archive_member=member.name,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),
                  header=lines[0] if lines else '',schema=schema)
                print('extracted '+target.name+' bytes='+str(len(raw)),flush=True)
        # Include archive trailer/trailing bytes in the hash, never extract them.
        while reader.read(1024*1024):pass
    if set(found)!=set(wanted) or h.hexdigest()!=index['archive_sha256']:
        raise ValueError('Archive integrity or member completeness failed; preserve extracted bytes as unapproved')
    receipt=dict(status='TWO_PUBLIC_PSD_TEXTS_EXTRACTED_AND_ARCHIVE_PIN_VERIFIED',
      created_utc=datetime.now(timezone.utc).isoformat(),archive_sha256=h.hexdigest(),
      index_sha256=sha(index_path),script_sha256=sha(Path(__file__)),files=list(found.values()),
      wall_seconds=time.perf_counter()-started,
      scope='Public bilby NRSur PSDs only; no claim of identity to pyRing INI PSDs/C00_AR; exact release source version OPEN',
      no_execution=True,no_posterior_or_strain_values_read=True,
      written_files=[str(destination/Path(m).name) for m in found]+[str(HERE/'PSD_EXTRACTION.json'),str(snapshot)])
    with (HERE/'PSD_EXTRACTION.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2);f.write('\n')
    print(json.dumps(dict(status=receipt['status'],wall_seconds=receipt['wall_seconds'],files=receipt['files']),indent=2))


if __name__=='__main__':main()
