"""Read/hash installed pinned runtime only; no scientific imports or execution."""
from pathlib import Path
import json,hashlib,time,datetime,sys
root=Path(__file__).resolve().parent
old=root.parent/'p3_codec_002'
ini=root.parent/'p3_init_preparation'
t=time.perf_counter();cpu=time.process_time()
def info(p):
 b=Path(p).read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
manifest=old/'RUNTIME_P3_READONLY.json'
runtime=json.loads(manifest.read_bytes())
codec=json.loads((old/'CODEC_CP437_PIN.json').read_bytes())
interpreter=json.loads((old/'INTERPRETER_PIN.json').read_bytes())
asd=json.loads((ini/'DEPENDENCIA_FACTORY_PIN.json').read_bytes())
rows=runtime['files']+[codec,interpreter,dict(path=asd['runtime_path'],sha256=asd['sha256'],bytes=asd['bytes'])]
checks=[]
for row in rows:
 actual=info(row['path'])
 checks.append({'path':row['path'],'passed':actual['sha256']==row['sha256'] and actual['bytes']==row['bytes'],'actual':actual})
assert not any(n in sys.modules for n in ('numpy','bilby','lal','lalsimulation','dynesty'))
result={'status':'RUNTIME_CURRENT_READ_ONLY' if all(c['passed'] for c in checks) else 'PIN_MISMATCH_STOP',
 'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runtime_files':len(runtime['files']),
 'extra_pins':['codec','interpreter','exact_ASD'],'checks':checks,'source_manifest':info(manifest),
 'wall_s':time.perf_counter()-t,'CPU_s':time.process_time()-cpu,'scientific_imports':False,
 'waveform_calls':0,'likelihood_calls':0,'PE_jobs':0,'D_read':False}
out=root/'VERIFICACAO_RUNTIME_INIT003.json';assert not out.exists()
b=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8');tmp=out.with_name(out.name+'.tmp')
with tmp.open('xb') as f:f.write(b)
assert tmp.read_bytes()==b;tmp.replace(out)
print(json.dumps({'status':result['status'],'checks':len(checks),'passed':sum(c['passed'] for c in checks),'receipt':info(out)}))
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
