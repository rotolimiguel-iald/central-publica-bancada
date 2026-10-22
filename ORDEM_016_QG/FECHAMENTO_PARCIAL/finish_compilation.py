"""Run packaging controls after the existing serial batch, never a second batch."""
from pathlib import Path
import json,subprocess,sys,time
from compile_batch import atomic
S=Path(__file__).resolve().parent

def run(name,label):
    receipt=S/'logs'/(label+'.json')
    if not receipt.exists():
        p=subprocess.run([sys.executable,'-X','utf8','-B',str(S/'run_lean.py'),str(S/'compile_config.json'),str(S/'lean'/(name+'.lean')),label],capture_output=True,text=True,encoding='utf-8')
        print(p.stdout.strip(),flush=True)
        if p.stderr: print(p.stderr[-1000:],flush=True)
    return json.loads(receipt.read_bytes()) if receipt.exists() else {'rc':None}

def main():
    while not (S/'BATCH_RESULT.json').exists():time.sleep(5)
    results=[]
    for row in json.loads((S/'SUPPLEMENTAL_PLAN.json').read_bytes()):
        r=run(row['module'],'supp_'+row['module']+'_01')
        log=S/'logs'/('supp_'+row['module']+'_01.log')
        diagnostic=row.get('expected_diagnostic')
        results.append(dict(**row,receipt=str(log.with_suffix('.json')),result=r,
            expected_outcome_observed=r.get('rc')==row['expected_rc'] and (not diagnostic or diagnostic in log.read_text('utf-8'))))
        atomic(S/'SUPPLEMENTAL_RESULTS.json',results)
    batch=json.loads((S/'BATCH_RESULT.json').read_bytes())
    modules=[x['module'] for x in batch['states'] if x.get('rc')==0]
    modules += [x['module'] for x in results if x['expected_rc']==0 and x['result'].get('rc')==0]
    # An aggregate import is a genuine coexistence check, not a sum of rc values.
    source=S/'lean/JointBundle.lean'
    body='import TGL\nimport TGLExt\n'+''.join('import '+n+'\n' for n in modules)+'\n#check TGLExt.ContratoQGv31.ContratoH2\n'
    if source.exists():assert source.read_text('utf-8')==body
    else:source.write_text(body,encoding='utf-8')
    r=run('JointBundle','joint_bundle_01')
    atomic(S/'JOINT_RESULT.json',dict(modules=modules,result=r,source=str(source),
        scope='All successful final modules imported together over the pinned v371 copy',gate_changed=False))
    print('FOLLOWUP_COMPLETE',r.get('rc'),flush=True)
if __name__=='__main__':main()
