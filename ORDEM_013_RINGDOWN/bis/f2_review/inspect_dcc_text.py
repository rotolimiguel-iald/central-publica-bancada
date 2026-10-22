"""Inspect only release text and notebook source cells, never pickle or code."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import tarfile

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent

def write_new(path,raw):
    if path.exists():raise FileExistsError(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+'.tmp')
    with temporary.open('xb') as f:f.write(raw)
    assert temporary.read_bytes()==raw
    temporary.replace(path)

def main():
    receipt=ROOT/'bis/F2_GWTC4_RELEASE_SEARCH.json'
    d=json.loads(receipt.read_bytes())
    record=next(r for r in d['rows'] if r['path'].endswith('pSEOBNR.tar.gz'))
    archive=ROOT/record['path'].replace('\\','/')
    actual=hashlib.sha256(archive.read_bytes()).hexdigest()
    assert actual==record['sha256']
    entries=[];extracted=[]
    with tarfile.open(archive,'r:gz') as tf:
        for m in tf:
            p=PurePosixPath(m.name)
            assert not p.is_absolute() and '..' not in p.parts and not m.issym() and not m.islnk(),m.name
            entries.append(dict(name=m.name,bytes=m.size,regular=m.isfile()))
            if not m.isfile() or p.suffix not in ('.md','.ipynb','.py','.json'):continue
            assert m.size<2_000_000
            raw=tf.extractfile(m).read();text=raw.decode('utf-8-sig')
            target=(OUT/'dcc_text'/p).resolve()
            assert target.is_relative_to((OUT/'dcc_text').resolve())
            write_new(target,raw)
            item=dict(member=m.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
                path=str(target.relative_to(ROOT)))
            if p.suffix=='.ipynb':
                nb=json.loads(text);lines=[];cells=[]
                for i,cell in enumerate(nb['cells']):
                    source=cell.get('source',[]);source=''.join(source) if isinstance(source,list) else source
                    lines.append(f'CELL {i} [{cell["cell_type"]}]')
                    start=len('\n'.join(lines).split('\n'))+1
                    lines.append(source);lines.append('')
                    cells.append(dict(index=i,type=cell['cell_type'],source=source))
                readable=target.with_name(target.stem+'.cells.txt')
                write_new(readable,('\n'.join(lines)+'\n').encode())
                item.update(cells=cells,source_only_path=str(readable.relative_to(ROOT)),
                    source_only_sha256=hashlib.sha256(readable.read_bytes()).hexdigest(),
                    notebook_outputs_executed=False,notebook_outputs_interpreted=False)
            extracted.append(item)
    expected=[dict(name=m['name'],bytes=m['bytes'],regular=m['regular']) for m in record['members']]
    assert entries==expected
    result=dict(status='PRIMARY_TEXT_INSPECTED_NO_BINARY_POSTERIOR_DESERIALIZATION',
        receipt=dict(path=str(receipt.relative_to(ROOT)),sha256=hashlib.sha256(receipt.read_bytes()).hexdigest()),
        archive=dict(path=str(archive.relative_to(ROOT)),bytes=archive.stat().st_size,sha256=actual,
            url=record['url'],last_modified_header=record['headers'].get('Last-Modified')),
        members=entries,text_sources=extracted,
        not_read=['Pickles','NPZ contents','DAT.GZ posterior values','Notebook outputs as scientific evidence'],
        no_code_executed=True)
    write_new(OUT/'dcc_text_inventory.json',(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps(dict(members=len(entries),text_sources=[{k:v for k,v in r.items() if k!='cells'} for r in extracted]),indent=2))

if __name__=='__main__':main()
