"""Extract only data/config controls from already listed, verified public archives."""
from pathlib import Path,PurePosixPath
import tarfile,hashlib,json
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(2**20),b''):h.update(b)
    return h.hexdigest()
def new(p,d):
    if p.exists():raise FileExistsError(p)
    raw=(json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode();tmp=p.with_suffix('.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise RuntimeError('Write mismatch')
    tmp.replace(p)
def main():
    downloads=json.loads((ROOT/'bis/F2_ARCHIVE_DOWNLOADS.json').read_bytes())
    rd=next(x for x in downloads if x['key']=='RD.tar.gz')
    oldidx=json.loads((ROOT/'cache/public/17018009/archive_index.json').read_bytes())
    record=json.loads((ROOT/'cache/public/17018009/record.json').read_bytes())
    archive=next(ROOT/'cache/public/17018009'/x['key'] for x in record['files'] if x['key'].endswith('.tar.gz'))
    jobs=[(ROOT/'cache/public/21454847/RD.tar.gz',rd['sha256'],
           {r['name']:r['bytes'] for r in rd['members'] if r['type']=='0'},
           ROOT/'cache/public/21454847/controls_extracted','cc-by-4.0','RD'),
          (archive,oldidx['archive_sha256'],
           {r['name']:r['size'] for r in oldidx['members'] if r['regular']},
           ROOT/'cache/public/17018009/controls_extracted',record['metadata']['license']['id'],'LVK_INJECTION')]
    report=[]
    for archive,digest,listed,target,license_name,kind in jobs:
        if sha(archive)!=digest:raise ValueError('Archive changed')
        target.mkdir(parents=True,exist_ok=True)
        destroot=target.resolve();files=[]
        with tarfile.open(archive,'r|gz') as tf:
            for member in tf:
                pp=PurePosixPath(member.name)
                selected=(kind=='RD' and pp.suffix in ('.nc','.ini','.txt','.md','.json','.dat')) or (kind=='LVK_INJECTION' and 'pseobnr_injection' in member.name and pp.suffix in ('.h5','.dat','.ini','.json','.txt'))
                if not selected:continue
                if not member.isfile() or member.issym() or member.islnk():raise ValueError('Nonregular selected member')
                if pp.is_absolute() or '..' in pp.parts or ':' in member.name or '\\' in member.name:raise ValueError('Unsafe archive path')
                if listed.get(member.name)!=member.size:raise ValueError('Member differs from pre-extraction index')
                dest=target.joinpath(*pp.parts)
                if not dest.resolve().is_relative_to(destroot):raise ValueError('Destination escapes cache')
                if dest.exists():raise FileExistsError(dest)
                dest.parent.mkdir(parents=True,exist_ok=True)
                h=hashlib.sha256();n=0;tmp=dest.with_name(dest.name+'.tmp')
                with tf.extractfile(member) as src,tmp.open('xb') as out:
                    for block in iter(lambda:src.read(2**20),b''):
                        n+=len(block);h.update(block);out.write(block)
                if n!=member.size or sha(tmp)!=h.hexdigest():raise ValueError('Incomplete extraction')
                tmp.replace(dest)
                files.append(dict(member=member.name,path=str(dest.relative_to(ROOT)),bytes=n,
                    sha256=h.hexdigest(),license=license_name))
        if not files:raise ValueError('No selected files extracted')
        report.append(dict(kind=kind,archive=str(archive.relative_to(ROOT)),archive_sha256=digest,
            files=files,count=len(files),bytes=sum(r['bytes'] for r in files),
            nonblind=True,scope='Calibration/robustness only; not independent event evidence'))
        print(kind,len(files),sum(r['bytes'] for r in files),flush=True)
    new(ROOT/'bis/F2_CONTROL_EXTRACTION.json',dict(status='DATA_ONLY_EXTRACTED_WITH_PATH_AND_HASH_GUARDS',
        utc=datetime.now(timezone.utc).isoformat(),archives=report))

if __name__=='__main__':main()
