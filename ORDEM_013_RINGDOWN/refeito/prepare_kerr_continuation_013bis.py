"""Preserve failed Kerr attempts; prepare a computation-only continuation copy."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,os
B=Path(__file__).resolve().parents[1];R=B.parent
SOURCE=B/'bis/e3_pyring_preparation';OUT=B/'bis/e3_kerr_continuation'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def create(p,v):
    raw=v if isinstance(v,bytes) else (json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
def main():
    if OUT.exists():raise FileExistsError('Continuation preparation already exists')
    oldmanifest=SOURCE/'MANIFEST_v3.json';manifest=json.loads(oldmanifest.read_bytes())
    oldconfig=SOURCE/'CONFIG.json';cfg=json.loads(oldconfig.read_bytes())
    previous=B/'cache/E3_KERR220_CALIBRATION_V1';state=json.loads((previous/'public_psd/CONVERGENCE.json').read_bytes())
    cost=json.loads((previous/'COST.json').read_bytes());envelope=json.loads((previous/'ENVELOPE.json').read_bytes())
    if state['status']!='PARTIAL_MAXCALL_NOT_ACCEPTED' or state['accepted_for_analysis'] is not False or state['before_add_live'] is not True:
        raise ValueError('Only the recorded insufficient-computation case permits this continuation')
    if len(cost['runs'])!=2 or any(r['cleanup']['group_absent'] is not True for r in cost['runs']):raise ValueError('Prior workers not closed')
    if datetime.now(timezone.utc)>=datetime.fromisoformat(envelope['stop_utc']):raise TimeoutError('Original Kerr envelope expired')
    OUT.mkdir()
    names=['conditioning.py','controller.py','custody.py','kerr_model.py','runner.py']
    for name in names:
        raw=(SOURCE/name).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=manifest['code_sha256'][name]:raise ValueError('Original source changed')
        create(OUT/name,raw)
    cfg['sampler']['maxcall']=3_000_000;cfg['variants']=['public_psd']
    cfg['output_relative_to_Chatgpt']='ORDEM_013_RINGDOWN/cache/E3_KERR220_CALIBRATION_V2'
    create(OUT/'CONFIG.json',cfg)
    inputs=dict(manifest['source_and_config_pins'])
    for p in [OUT/'CONFIG.json',oldmanifest,oldconfig,previous/'COST.json',previous/'ENVELOPE.json',
              previous/'public_psd/CONVERGENCE.json',previous/'public_psd/CONTROLLER.json',
              previous/'welch/FAILURE.json',B/'bis/e3_kerr_failure_diagnostic/DIAGNOSTIC.json']:
        inputs[p.relative_to(R).as_posix()]=sha(p)
    continuation={'status':'PREPARED_NOT_EXECUTED_CALIBRATION_ONLY','created_utc':datetime.now(timezone.utc).isoformat(),
      'code_sha256':{n:sha(OUT/n) for n in names},'source_and_config_pins':inputs,
      'parent_manifest_sha256':sha(oldmanifest),'original_envelope_stop_utc':envelope['stop_utc'],
      'changes':{'sampler.maxcall':[1_000_000,3_000_000],'variants':[['welch','public_psd'],['public_psd']],
        'output_relative_to_Chatgpt':['ORDEM_013_RINGDOWN/cache/E3_KERR220_CALIBRATION_V1',cfg['output_relative_to_Chatgpt']]},
      'unchanged':'All waveform/data/PSD/prior/seed/convergence settings and runtime source bytes; failed Welch branch retained without changing threshold',
      'reason':'Insufficient iterations on known calibration event. Restart with same seed and larger cap, not acceptance of partial posterior or new physical hypothesis.',
      'wall_contract':'Authorization must expire at original envelope stop; new controller7200 ceiling cannot extend that earlier deadline. Public branch1800s unchanged.',
      'cost_projection_INPUT':{'source_partial_wall_seconds':state['cost']['wall_seconds'],
        'source_sampler_ncall':state['ncall'],'linear_3million_call_projection_seconds':state['cost']['wall_seconds']*3_000_000/state['ncall'],
        'limitation':'Computation forecast only; no assurance of convergence or equal cost throughout parameter space'},
      'script_sha256':sha(Path(__file__))}
    create(OUT/'MANIFEST.json',continuation)
    print(json.dumps({'status':continuation['status'],'manifest_sha256':sha(OUT/'MANIFEST.json'),
      'original_envelope_stop_utc':envelope['stop_utc'],'projected_seconds':continuation['cost_projection_INPUT']['linear_3million_call_projection_seconds']}))
if __name__=='__main__':main()
