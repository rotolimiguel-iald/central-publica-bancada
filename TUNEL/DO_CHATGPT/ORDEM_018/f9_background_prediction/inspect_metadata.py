"""Read local NPZ axes or installed package metadata; never run a cosmology solver."""
from pathlib import Path
import ast, hashlib, importlib.metadata as metadata, importlib.util, json, struct, sys, zipfile
from datetime import datetime, timezone
from fractions import Fraction
HERE=Path(__file__).resolve().parent
REQUEST='f132a1d5-7477-405d-963b-b1659db63328'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
    p=HERE/name
    data=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    tmp=p.with_name(p.name+'.new')
    if p.exists(): raise FileExistsError(p)
    with tmp.open('xb') as f: f.write(data)
    if tmp.stat().st_size != len(data): raise RuntimeError('short write')
    tmp.rename(p)
def axes():
    source=HERE.parent/'reproducao_fase45_conjunta/T4_camb_lcdm_v1.npz'
    headers={}; coordinates={}
    with zipfile.ZipFile(source) as archive:
        for name in archive.namelist():
            with archive.open(name) as f:
                assert f.read(6)==b'\x93NUMPY'
                v=f.read(2); n=2 if v[0]==1 else 4
                size=struct.unpack('<H' if n==2 else '<I',f.read(n))[0]
                h=ast.literal_eval(f.read(size).decode('latin1').strip()); headers[name]=h
                if name.startswith('grade_'):
                    assert h['descr']=='<f8' and len(h['shape'])==1
                    coordinates[name[6:-4]]=list(struct.unpack('<'+'d'*h['shape'][0],f.read()))
    broad={'H0':['50','90'],'ombh2':['.015','.03'],'omch2':['.08','.18']}
    support={'H0':['60','76'],'ombh2':['.02025','.02475'],'omch2':['.102','.138']}
    volume=Fraction(1); fraction=Fraction(1)
    for name,(lo,hi) in broad.items():
        width=Fraction(hi)-Fraction(lo); volume*=width
        fraction*=(Fraction(support[name][1])-Fraction(support[name][0]))/width
        axis=coordinates[name]
        assert abs(axis[1]-float(support[name][0]))<1e-12
        assert abs(axis[-2]-float(support[name][1]))<1e-12
    save('UNIDADE.json',{'request_id':REQUEST,'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'DOCUMENTARY_BACKGROUND_PREDICTIONS_PREPARATION_ONLY','science_runs':0,'data_centers_read':False,'remote_calls':0})
    save('TABLE_METADATA.json',{'source':str(source),'bytes':source.stat().st_size,'sha256':sha(source),'headers':headers,'axes':coordinates,'prediction_array_payloads_read':False,'raw_shape':[len(coordinates[n]) for n in broad],'effective_support':support,'common_uniform_prior':broad,'coordinate_volume_exact':str(volume),'density_exact':str(1/volume),'covered_volume_fraction_exact':str(fraction),'covered_percent':float(100*fraction),'uncovered_percent':float(100*(1-fraction)),'interpretation':'prior-volume geometry, not posterior probability; no likelihood read','support_rule':'T4_reproduzir.py: coordinate position between 1 and len(axis)-2; raw exterior nodes are padding'})
    print('AXES_ONLY_COMPLETE',float(100*fraction))
def packages():
    spec=importlib.util.find_spec('camb')
    if spec is None: raise RuntimeError('CAMB missing')
    root=Path(spec.origin).parent
    pins=[]
    for p in sorted(root.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':
            pins.append({'relative_path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
    info={'request_id':REQUEST,'python':sys.version,'executable':sys.executable,'camb_root':str(root),'packages':{n:metadata.version(n) for n in ('camb','numpy','scipy')},'package_files':pins,'camb_imported':False,'solver_calls':0}
    save('RUNTIME_METADATA.json',info)
    extracts=[]
    wanted={'set_cosmology','set_accuracy','set_dark_energy','get_background','get_derived_params','hubble_parameter','comoving_radial_distance','get_Omega','set_classes'}
    for name in ['model.py','results.py','camb.py','recombination.py','bbn.py']:
        p=root/name; lines=p.read_text().splitlines(); tree=ast.parse('\n'.join(lines))
        for node in ast.walk(tree):
            if isinstance(node,(ast.FunctionDef,ast.ClassDef)) and (node.name in wanted or (name=='recombination.py' and node.name=='Recfast')):
                excerpt='\n'.join(f'{i+1}: {lines[i]}' for i in range(node.lineno-1,node.end_lineno))
                extracts.append({'source':str(p),'sha256':sha(p),'symbol':node.name,'start_line':node.lineno,'end_line':node.end_lineno,'text':excerpt})
    save('LOCAL_API_EXTRACTS.json',extracts)
    print(json.dumps({k:v for k,v in info.items() if k!='package_files'}))
    for e in extracts: print(e['source'],e['symbol'],e['text'])
if __name__=='__main__':
    {'axes':axes,'packages':packages}[sys.argv[1]]()