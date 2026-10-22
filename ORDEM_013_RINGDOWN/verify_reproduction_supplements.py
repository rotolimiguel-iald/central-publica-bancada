"""Audit fresh-run receipts and make compact additive reproduction archives."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import shutil
import tempfile
import zipfile
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    destination=ROOT/'C7_SUPPLEMENTS_VALIDATION.json'
    if destination.exists():
        raise FileExistsError('Preserve the delivered verification')
    records=[]
    stages={'C7_POSTERIOR_REPRODUCTION':['primary','joint','free_clock','catalog'],
            'C7_INJECTION_REPRODUCTION':['full']}
    for name,required in stages.items():
        package=ROOT/name
        manifest=json.loads((package/'MANIFEST.json').read_bytes())
        for row in manifest['shipped_files']:
            path=package/row['path']
            if sha(path)!=row['sha256'] or path.stat().st_size!=row['bytes']:
                raise ValueError('Shipped input changed: '+str(path))
        results=[]
        for stage in required:
            candidates=sorted((package/'cache').glob('run_'+stage+'_*/RESULT.json'))
            if len(candidates)!=1:
                raise ValueError('Expected exactly one documented fresh replay for '+stage)
            receipt=json.loads(candidates[0].read_bytes())
            if receipt['status']!='PASS' or receipt['reference_results_copied_as_inputs']:
                raise ValueError('Fresh replay did not pass')
            if receipt['manifest_sha256']!=sha(package/'MANIFEST.json'):
                raise ValueError('Receipt belongs to another package')
            # Read computed outputs, not only the summary status.
            run=candidates[0].parent/'ORDEM_013_RINGDOWN'
            for check in receipt['comparisons']:
                if sha(run/check['output'])!=check['output_sha256']:
                    raise ValueError('Recomputed output differs from replay receipt')
                if check['numerical_leaves']<=0:
                    raise ValueError('Empty numerical comparison')
            results.append(dict(stage=stage,path=candidates[0].relative_to(ROOT).as_posix(),
                sha256=sha(candidates[0]),comparisons=receipt['comparisons']))
        spec=importlib.util.spec_from_file_location('reviewed_driver',package/'reproduce.py')
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        temporary=Path(tempfile.mkdtemp(prefix='supplement_guard_',dir=ROOT/'cache'))
        sample=manifest['shipped_files'][0]
        original=package/sample['path'];copy=temporary/'sample'
        shutil.copyfile(original,copy)
        module.verify(copy,sample)
        data=bytearray(copy.read_bytes());data[len(data)//2]^=1;copy.write_bytes(data)
        try:
            module.verify(copy,sample)
        except ValueError:
            refused=True
        else:
            raise ValueError('Mutated file was accepted')
        path_refusals=[]
        for unsafe in ('../escape','/absolute','bad\\path'):
            try:
                module.checked(temporary,unsafe)
            except ValueError:
                path_refusals.append(unsafe)
            else:
                raise ValueError('Path escape was accepted')
        archive=ROOT/'cache'/(name+'_v1.zip')
        if archive.exists():
            raise FileExistsError('Preserve earlier supplementary archive')
        with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as handle:
            for row in manifest['shipped_files']:
                handle.write(package/row['path'],name+'/'+row['path'])
            handle.write(package/'MANIFEST.json',name+'/MANIFEST.json')
            for result in results:
                handle.write(ROOT/result['path'],name+'/replay_receipts/'+result['stage']+'.json')
        with zipfile.ZipFile(archive) as handle:
            if handle.testzip() is not None:
                raise ValueError('Supplement archive CRC failure')
            # Verify exact shipped byte hashes directly from the archive.
            for row in manifest['shipped_files']:
                if hashlib.sha256(handle.read(name+'/'+row['path'])).hexdigest()!=row['sha256']:
                    raise ValueError('Archive member changed')
        record=dict(package=name,status='PASS',archive=archive.relative_to(ROOT).as_posix(),
            bytes=archive.stat().st_size,sha256=sha(archive),manifest_sha256=sha(package/'MANIFEST.json'),
            shipped_files=len(manifest['shipped_files']),replays=results,
            adversarial=dict(mutated_file_refused=refused,path_escapes_refused=path_refusals))
        records.append(record)
        print(json.dumps({k:v for k,v in record.items() if k!='replays'}),flush=True)
    atomic_json(destination,dict(status='PASS',date_utc=datetime.now(timezone.utc).isoformat(),packages=records,
        scope='Fresh local scientific-environment replays and tamper/path controls; public download path not re-fetched, original LVK samplers not rerun',
        v1_independent_package_unchanged=True))


if __name__=='__main__':
    main()
