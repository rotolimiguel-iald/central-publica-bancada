"""Read-only RD applicability inventory; never execute archive code or pickle."""
from pathlib import Path, PurePosixPath
from collections import Counter, defaultdict
import ast
import configparser
import hashlib
import json
import tarfile
import time
import h5py
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent

def safe_path(relative):
    relative=relative.replace('\\','/')
    p=(ROOT/relative).resolve()
    if not p.is_relative_to(ROOT.resolve()):raise ValueError(relative)
    return p

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest()

def new(path, obj):
    if path.exists():raise FileExistsError(path)
    raw=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    temp=path.with_name(path.name+'.tmp')
    with temp.open('xb') as f:f.write(raw)
    assert temp.read_bytes()==raw
    temp.replace(path)

def mode_strings(data):
    x=np.asarray(data)
    if x.dtype.kind=='S' and x.ndim==2:return [b''.join(row).decode() for row in x]
    if x.dtype.kind in ('S','O','U'):return [v.decode() if isinstance(v,bytes) else str(v) for v in x.ravel()]
    return x.tolist()

def walk_hard(group, prefix='',seen=None):
    seen=set() if seen is None else seen
    result=[];links=[]
    for key in group:
        path=prefix+key;link=group.get(key,getlink=True)
        if not isinstance(link,h5py.HardLink):
            links.append(dict(path=path,type=type(link).__name__));continue
        obj=group[key]
        if isinstance(obj,h5py.Dataset):
            result.append(dict(path=path,shape=list(obj.shape),dtype=str(obj.dtype)))
        elif isinstance(obj,h5py.Group):
            address=h5py.h5o.get_info(obj.id).addr
            if address in seen:continue
            seen.add(address)
            rows,skipped=walk_hard(obj,path+'/',seen);result.extend(rows);links.extend(skipped)
    return result,links

def main():
    started=time.monotonic()
    receipt=ROOT/'bis/F2_CONTROL_EXTRACTION.json'
    data=json.loads(receipt.read_bytes());rd=next(a for a in data['archives'] if a['kind']=='RD')
    archive=safe_path(rd['archive']);archive_hash=sha(archive)
    assert archive_hash==rd['archive_sha256']
    members=[]
    with tarfile.open(archive,'r:gz') as tf:
        for m in tf:
            members.append(dict(name=m.name,bytes=m.size,regular=m.isfile(),type=m.type.decode('ascii',errors='replace')))
    recorded={r['member'] for r in rd['files']}
    omitted=[m for m in members if m['regular'] and m['name'] not in recorded]
    files=[];families=defaultdict(lambda:dict(configs=[],results=[],models={},schemas=[]))
    mismatches=[];errors=[]
    for index,record in enumerate(rd['files']):
        path=safe_path(record['path']);digest=sha(path)
        if digest!=record['sha256'] or path.stat().st_size!=record['bytes']:mismatches.append(record['path'])
        entry=dict(path=str(path.relative_to(ROOT)),member=record['member'],bytes=path.stat().st_size,sha256=digest)
        rel=record['member'];family=rel.split('/engine/')[0] if '/engine/' in rel else str(PurePosixPath(rel).parent)
        if path.suffix=='.ini':
            text=path.read_text(encoding='utf-8-sig');parser=configparser.ConfigParser(interpolation=None)
            parser.read_string(text);sections={s:dict(parser[s]) for s in parser.sections()}
            entry.update(type='config',sections=sections,lines=[dict(line=i,text=l) for i,l in enumerate(text.splitlines(),1)])
            families[family]['configs'].append(entry['path'])
            model=sections.get('model',{})
            families[family]['models'][json.dumps(model,sort_keys=True)]=model
        elif path.suffix=='.md':
            entry.update(type='readme',text=path.read_text(encoding='utf-8-sig'))
        elif path.suffix=='.nc':
            try:
                with h5py.File(path,'r') as h:
                    config=h.attrs.get('config','{}')
                    if isinstance(config,bytes):config=config.decode()
                    config=json.loads(config)
                    datasets,links=walk_hard(h)
                    posterior_names=[r['path'] for r in datasets if r['path'].startswith('posterior/')]
                    modes=mode_strings(h['posterior/mode'][()]) if 'posterior/mode' in posterior_names else None
                    deviation_stats={}
                    for name in posterior_names:
                        base=name.split('/')[-1]
                        if base in ('df','dg','dtau','domega','df220','dg220','dtau220','domega220') or base.startswith(('df_','dg_','dtau_','domega_')):
                            obj=h[name]
                            if obj.dtype.kind not in 'fiu':continue
                            values=obj[()]
                            flattened=values.reshape(-1,values.shape[-1]) if values.ndim==3 else values.reshape(-1,1)
                            deviation_stats[name]=dict(shape=list(values.shape),finite=bool(np.isfinite(values).all()),
                                min_by_last_axis=np.min(flattened,axis=0).tolist(),max_by_last_axis=np.max(flattened,axis=0).tolist(),
                                nonzero_by_last_axis=np.count_nonzero(flattened,axis=0).tolist())
                    schema_text=json.dumps(datasets,sort_keys=True)
                    schema_hash=hashlib.sha256(schema_text.encode()).hexdigest()
                    embedded_model=config.get('model',{})
                    side_config=path.with_name('config.ini')
                    parser=configparser.ConfigParser(interpolation=None);parser.read_string(side_config.read_text(encoding='utf-8-sig'))
                    side_model=dict(parser['model'])
                    mismatch={k:[side_model.get(k),embedded_model.get(k)] for k in set(side_model)|set(embedded_model) if side_model.get(k)!=embedded_model.get(k)}
                    entry.update(type='netcdf',datasets=datasets,nonhard_links_not_followed=links,
                        config=config,mode_labels=modes,posterior_names=posterior_names,deviations=deviation_stats,
                        ringdown_version=str(h.attrs.get('ringdown_version','')),schema_sha256=schema_hash,
                        embedded_vs_sidecar_model_differences=mismatch)
                    families[family]['results'].append(entry['path']);families[family]['schemas'].append(schema_hash)
                    families[family]['models'][json.dumps(embedded_model,sort_keys=True)]=embedded_model
            except Exception as e:
                entry.update(type='netcdf',error=type(e).__name__+': '+str(e));errors.append(entry['path'])
        else:raise ValueError('Unexpected extracted payload '+str(path))
        files.append(entry)
        if (index+1)%100==0:print('inspected',index+1,'of',len(rd['files']),flush=True)
    family_rows=[]
    for name,f in sorted(families.items()):
        if not f['results'] and not f['configs']:continue
        f['models']=list(f['models'].values());f['schemas']=dict(Counter(f['schemas']))
        family_rows.append(dict(family=name,**f))
    base=ROOT/'cache/public/21454847/controls_extracted'
    disk_files={str(p.relative_to(ROOT)).replace('\\','/') for p in base.rglob('*') if p.is_file()}
    receipt_files={r['path'].replace('\\','/') for r in rd['files']}
    result=dict(scope='All RD configs and all NetCDF schemas; numerical reads limited to mode coordinates and deviation fields; no strain values or archive code executed',
        extraction_receipt=dict(path=str(receipt.relative_to(ROOT)),sha256=sha(receipt)),
        earlier_six_schemas=dict(path='bis/F2_CONTROL_SCHEMAS.json',sha256=sha(ROOT/'bis/F2_CONTROL_SCHEMAS.json')),
        archive=dict(path=str(archive.relative_to(ROOT)),bytes=archive.stat().st_size,sha256=archive_hash,members=members),
        counts=dict(files=len(files),extensions=dict(Counter(Path(r['path']).suffix for r in rd['files'])),families=len(family_rows)),
        omitted_regular_members=omitted,missing_on_disk=sorted(receipt_files-disk_files),extra_on_disk=sorted(disk_files-receipt_files),
        hash_mismatches=mismatches,read_errors=errors,files=files,families=family_rows,
        h5py_version=h5py.__version__,numpy_version=np.__version__,elapsed_seconds=time.monotonic()-started)
    new(OUT/'rd_inventory.json',result)
    print(json.dumps({k:result[k] for k in ['counts','hash_mismatches','read_errors','missing_on_disk','extra_on_disk','elapsed_seconds']},indent=2))
    print('OMITTED',json.dumps(dict(Counter(PurePosixPath(m['name']).suffix for m in omitted))))
    for f in family_rows:
        print(json.dumps(dict(family=f['family'],nc=len(f['results']),ini=len(f['configs']),models=f['models']),ensure_ascii=False))
    for f in files:
        if f.get('deviations'):
            print('DEVIATION_EXAMPLE',json.dumps({k:f[k] for k in ['path','mode_labels','deviations']},ensure_ascii=False));break

if __name__=='__main__':main()
