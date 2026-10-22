"""Exclude explicitly superseded modules before the final aggregate import."""
from pathlib import Path
import json,time
from compile_batch import atomic
from finish_compilation import run
S=Path(__file__).resolve().parent
def main():
    while not (S/'JOINT_RESULT.json').exists():time.sleep(5)
    old=json.loads((S/'JOINT_RESULT.json').read_bytes())
    supplements=json.loads((S/'SUPPLEMENTAL_RESULTS.json').read_bytes())
    replaced={x['supersedes']:x['module'] for x in supplements if x.get('supersedes') and x['result'].get('rc')==0}
    modules=[m for m in old['modules'] if m not in replaced]
    source=S/'lean/JointBundle_Final.lean'
    body='import TGL\nimport TGLExt\n'+''.join('import '+n+'\n' for n in modules)+'\n#check TGLExt.ContratoQGv31.ContratoH2\n'
    if source.exists():assert source.read_text('utf-8')==body
    else:source.write_text(body,encoding='utf-8')
    result=run(source.stem,'joint_final_01')
    atomic(S/'JOINT_FINAL_RESULT.json',dict(module=source.stem,modules=modules,result=result,source=str(source),receipt=str(S/'logs/joint_final_01.json'),
        excluded_superseded=replaced,prior_aggregate=old,gate_changed=False))
    print('FINAL_JOINT_COMPLETE',result.get('rc'),flush=True)
if __name__=='__main__':main()
