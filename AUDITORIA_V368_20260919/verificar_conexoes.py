import hashlib, json, os, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
root=Path(__file__).resolve().parent
out=root/'conexoes'
out.mkdir(exist_ok=True)
cache=root.parent/'TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel'
modules=json.loads((root/'contexto/modulos.json').read_text(encoding='utf-8'))
queue=['TGLExt.TheMasterFires','TGLExt.StrongAssembly','TGLExt.TheImportedEquilibrium']
closure=set()
checks=[]
while queue:
    mod=queue.pop()
    if mod in closure or mod not in modules: continue
    closure.add(mod)
    meta=modules[mod]
    actual=cache/meta['path']
    new=root/'contexto/lean'/meta['path']
    a,b=actual.read_bytes(),new.read_bytes()
    equal=a.decode('utf-8-sig').replace('\r\n','\n').strip()==b.decode('utf-8-sig').replace('\r\n','\n').strip()
    checks.append({'module':mod,'cached_source_sha256':hashlib.sha256(a).hexdigest(),'v368_source_sha256':hashlib.sha256(b).hexdigest(),'text_equal_normalized':equal})
    queue.extend(meta['imports'])
assert all(x['text_equal_normalized'] for x in checks), [x['module'] for x in checks if not x['text_equal_normalized']]
paths=[cache/'.lake/build/lib/lean']+[p/'.lake/build/lib/lean' for p in (cache/'.lake/packages').iterdir() if p.is_dir()]
env=dict(os.environ,LEAN_PATH=';'.join(str(p) for p in paths))
lean=Path.home()/'.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe'
def run(path):
    p=subprocess.run([str(lean),str(path)],cwd=root,env=env,capture_output=True,encoding='utf-8',errors='replace',timeout=180)
    data=p.stdout+p.stderr
    (out/(path.stem+'.txt')).write_bytes(data.encode('utf-8'))
    return {'returncode':p.returncode,'output':data}
positive=run(root/'ConexoesExistentes.lean')
negative=root/'ControleContrato.lean'
negative.write_bytes(b'import TGLExt.TheImportedEquilibrium\nimport TGLExt.TriadMaster\nopen TGLExt\nnoncomputable def invalidBridge : HorizonEquilibriumData := towerEquilibriumInput 1 (by norm_num) 1\n')
control=run(negative)
result={'scope':'new adapters compiled using existing dependency cache; cached local sources compared with v368; not full kernel rebuild','dependencies_compared':len(checks),'source_checks':checks,'positive':positive,'negative':control}
target=out/'resultado.json'
temp=target.with_suffix('.tmp')
temp.write_bytes(json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8'))
temp.replace(target)
print(json.dumps({'dependencies_compared':len(checks),'positive':positive,'negative':control},ensure_ascii=False,indent=2))
