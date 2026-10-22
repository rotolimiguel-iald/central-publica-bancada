"""One bounded syntax repair and final diagnostic adjudication; no new theorem."""
from pathlib import Path
import json,time
from compile_batch import atomic
from finish_compilation import run
S=Path(__file__).resolve().parent
def main():
    while not (S/'JOINT_FINAL_RESULT.json').exists():time.sleep(5)
    previous=json.loads((S/'JOINT_FINAL_RESULT.json').read_bytes())
    supp=json.loads((S/'SUPPLEMENTAL_RESULTS.json').read_bytes())
    for x in supp:
        if x['expected_rc']==1:
            text=Path(x['receipt']).with_suffix('.log').read_text('utf-8')
            diag=x.get('expected_diagnostic','')
            x['initial_expected_outcome_observed']=x['expected_outcome_observed']
            x['expected_outcome_observed']=x['result'].get('rc')==1 and diag.casefold() in text.casefold()
            x['diagnostic_comparison']='casefold; actual compiler diagnostic preserved in immutable log'
    for row in json.loads((S/'FINAL_REPAIR_PLAN.json').read_bytes()):
        label='repair_'+row['module']+'_01';r=run(row['module'],label)
        supp.append(dict(**row,receipt=str(S/'logs'/(label+'.json')),result=r,expected_outcome_observed=r.get('rc')==row['expected_rc']))
    atomic(S/'SUPPLEMENTAL_RESULTS.json',supp)
    replacements={x['supersedes']:x['module'] for x in supp if x.get('supersedes') and x['result'].get('rc')==0}
    modules=[n for n in previous['modules'] if n not in replacements]
    modules += [x['module'] for x in supp if x['expected_rc']==0 and x['result'].get('rc')==0 and x['module'] not in modules]
    source=S/'lean/JointBundle_Reviewed.lean'
    body='import TGL\nimport TGLExt\n'+''.join('import '+n+'\n' for n in modules)+'\n#check TGLExt.ContratoQGv31.ContratoH2\n'
    if source.exists():assert source.read_text('utf-8')==body
    else:source.write_text(body,encoding='utf-8')
    result=run(source.stem,'joint_reviewed_01')
    atomic(S/'JOINT_FINAL_RESULT.json',dict(module=source.stem,modules=modules,result=result,source=str(source),receipt=str(S/'logs/joint_reviewed_01.json'),excluded_superseded=replacements,prior_aggregate=previous,gate_changed=False))
    atomic(S/'FINAL_REPAIRS_DONE.json',dict(rc=result.get('rc'),gate_changed=False))
    print('REVIEWED_JOINT_COMPLETE',result.get('rc'),flush=True)
if __name__=='__main__':main()
