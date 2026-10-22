"""Serial isolated compilation, stopping at the first failed module."""
from pathlib import Path
import json,sys,subprocess
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C3';P=D/'package'
plan=json.loads((D/'PLAN.json').read_bytes())
paths=json.loads((ROOT/'A8/READONLY_IMPORT_PATHS.json').read_bytes())
selected=sys.argv[1:]
names=[Path(x['copy']).stem for x in plan['groups']]+['IntegrationAudit']
for i,name in enumerate(names):
    if selected and name not in selected:continue
    label='module_'+str(i+1).zfill(2)+'_01'
    assert not (P/(label+'.json')).exists(),label
    command=[sys.executable,'-X','utf8','-B',str(ROOT/'A8/compile_a8_isolated_v2.py'),
        str(ROOT/'A8/compiler_env'),str(P/(name+'.lean')),label,str(P),*paths]
    print('START '+name,flush=True)
    r=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
    if r.returncode:print(r.stdout,r.stderr);sys.exit(r.returncode)
    receipt=json.loads((P/(label+'.json')).read_bytes())
    print(json.dumps(dict(module=name,rc=receipt['rc'],wall_seconds=receipt['wall_seconds'],peak_bytes=receipt['peak_process_committed_bytes'])),flush=True)
    if receipt['rc']:sys.exit(1)
