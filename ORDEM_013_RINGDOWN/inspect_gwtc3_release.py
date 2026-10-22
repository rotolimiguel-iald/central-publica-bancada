"""List and selectively extract the verified GWTC-3 ringdown ZIP.

No file from the archive is executed. No extractall, symlinks or paths outside
the selected cache are allowed. A separate --extract invocation follows review
of the index; posterior contents are not read here.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import stat
import zipfile
from collections import Counter
from fetch_public import atomic_json, digests

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract', action='store_true')
    args = parser.parse_args()
    folder = ROOT / 'cache/public/17461225'
    name = 'IGWN-GWTC3-TGR-v2-rin.zip'
    archive = folder / name
    receipt = json.loads((folder / (name + '.receipt.json')).read_bytes())
    md5, sha = digests(archive)
    if sha != receipt['sha256'] or md5 != receipt['md5'] or archive.stat().st_size != receipt['bytes']:
        raise ValueError('Archive custody mismatch')
    metadata = json.loads((folder / 'record.json').read_bytes())
    public = next(r for r in metadata['files'] if r['key'] == name)
    if public['checksum'] != 'md5:' + md5:
        raise ValueError('Published checksum mismatch')
    index_path = folder / 'ZIP_INDEX.json'
    with zipfile.ZipFile(archive) as handle:
        records = []
        names = set()
        for info in handle.infolist():
            p = PurePosixPath(info.filename)
            mode = info.external_attr >> 16
            if (p.is_absolute() or '..' in p.parts or '\\' in info.filename or ':' in info.filename
                    or stat.S_ISLNK(mode) or info.filename in names):
                raise ValueError('Unsafe/duplicate ZIP entry: ' + info.filename)
            names.add(info.filename)
            records.append(dict(member=info.filename, bytes=info.file_size,
                compressed_bytes=info.compress_size, crc32=f'{info.CRC:08x}', directory=info.is_dir()))
        value = dict(record=17461225, archive_sha256=sha, entries=records,
            total_uncompressed_bytes=sum(r['bytes'] for r in records),
            scope='ZIP structure only; posterior datasets not yet inspected')
        if not args.extract:
            if index_path.exists():
                if json.loads(index_path.read_bytes()) != value:
                    raise ValueError('Archive listing changed')
            else:
                atomic_json(index_path, value)
            print(json.dumps(dict(entries=len(records), total_uncompressed_bytes=value['total_uncompressed_bytes'],
                models=dict(Counter(r['member'].split('_', 2)[-1].removesuffix('.h5') for r in records if not r['directory'])),
                pseob_files=[r['member'] for r in records if r['member'].endswith('_pseobnrv4hm.h5')])), flush=True)
            return
        if not index_path.exists() or json.loads(index_path.read_bytes()) != value:
            raise ValueError('First list and inspect the archive with no --extract')
        files = []
        for row in records:
            member = row['member']
            # C4 compares the 220 deformation posterior. Kerr_221 products
            # deform the overtone instead; retain their index, do not relabel.
            if row['directory'] or not (member.lower().endswith(('_pseobnrv4hm.h5', '.md', '.txt', '.ini'))):
                continue
            target = (folder / 'extracted' / member).resolve()
            if not target.is_relative_to((folder / 'extracted').resolve()):
                raise ValueError('Extraction path escaped cache')
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_name(target.name + '.partial')
            if not target.exists():
                with handle.open(member) as source, temporary.open('xb') as dest:
                    while block := source.read(8*1024*1024):
                        dest.write(block)
                if temporary.stat().st_size != row['bytes']:
                    raise ValueError('Short extracted member')
                temporary.replace(target)
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            files.append(dict(member=member, path=target.relative_to(ROOT).as_posix(),
                bytes=target.stat().st_size, sha256=digest))
            print(json.dumps(dict(extracted=member, bytes=target.stat().st_size)), flush=True)
        atomic_json(folder / 'extraction_receipt.json', dict(archive_sha256=sha, files=files,
            archive_crc_checked=True, posterior_read=False))
        print(json.dumps(dict(files=len(files), bytes=sum(r['bytes'] for r in files))), flush=True)


if __name__ == '__main__':
    main()
