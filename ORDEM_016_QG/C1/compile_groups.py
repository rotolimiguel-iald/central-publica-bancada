"""Compile sequentially, stopping on the first real failure; no blind retry."""
from pathlib import Path
import json,subprocess,sys
D=Path(__file__).resolve().parent;ROOT=D.parent;A8=ROOT/'A8'
paths=json.loads((A8/'READONLY_IMPORT_PATHS.json').read_bytes())
plan=json.loads((D/'GROUP_AUDIT_PLAN_v3.json').read_bytes())
auditor=ROOT.parent/'TUNEL/PARA_CHATGPT/ORDEM_016_INSUMOS/A6_EQUACAO_DA_VERDADE/MEDIDAS_DO_REDATOR/auditar_axiomas.py'
for group in sys.argv[1:]:
    g=next(x for x in plan['groups'] if x['group']==group)
    label='group_'+group.lower()+'_01';receipt=D/(label+'.json')
    assert not receipt.exists(),receipt
    cmd=[sys.executable,'-X','utf8','-B',str(A8/'compile_a8_isolated_v2.py'),str(A8/'compiler_env'),g['path'],label,str(ROOT/'A1/minimal_imports'),*paths]
    result=subprocess.run(cmd,capture_output=True)
    if not receipt.exists():
        print(result.stdout.decode('utf-8',errors='replace')[-6000:]+result.stderr.decode('utf-8',errors='replace')[-6000:],flush=True);sys.exit(2)
    r=json.loads(receipt.read_bytes());print(json.dumps({'group':group,'rc':r['rc'],'cpu':r['cpu_user_seconds']+r['cpu_kernel_seconds']}),flush=True)
    if r['rc']!=0:
        print((D/(label+'.log')).read_text('utf-8')[:8000],flush=True);sys.exit(1)
    check=subprocess.run([sys.executable,'-X','utf8','-B',str(auditor),g['path'],str(D/(label+'.log'))],capture_output=True)
    out=D/(label+'_audit.json');assert not out.exists();out.write_bytes(check.stdout)
    assert check.returncode==0,check.stdout.decode('utf-8')
