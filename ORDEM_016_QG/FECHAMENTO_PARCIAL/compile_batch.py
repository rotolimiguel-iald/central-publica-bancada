"""Serial isolated compilation of the consolidation plan; checkpoint each file."""
from pathlib import Path
from datetime import datetime,timezone
import sys,subprocess,json,time,hashlib

S=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,d):
    raw=(json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode()
    if p.exists():
        b=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'));b.write_bytes(p.read_bytes())
    t=p.with_suffix('.tmp');t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)

def main():
    start=json.loads((S/'START.json').read_bytes());deadline=datetime.fromisoformat(start['deadline']).timestamp()
    plan=json.loads((S/'SOURCE_PLAN.json').read_bytes());rows={x['module']:x for x in plan['sources']}
    order=plan['order']+['ContratoQG_v32_Proposta'];states=[]
    # Do not contend with the census/compiler already dispatched by the coordinator.
    while not (S/'logs/kernel_census_01.json').exists() and time.time()<deadline:
        time.sleep(5)
    for i,name in enumerate(order):
        receipt=S/'logs'/f'unit_{name}_01.json';source=S/'lean'/(name+'.lean')
        if time.time()>deadline-1200:
            states.append(dict(module=name,status='MEDIDA_TIMEBOX_NOT_COMPILED'));continue
        imports=rows.get(name,{}).get('imports',[])
        missing=[x for x in imports if x in rows and not (S/'lean'/(x+'.olean')).exists()]
        if missing:
            states.append(dict(module=name,status='MEDIDA_DEPENDENCY_FAILED',missing=missing));continue
        if not receipt.exists():
            completed=subprocess.run([sys.executable,'-X','utf8','-B',str(S/'run_lean.py'),str(S/'compile_config.json'),str(source),f'unit_{name}_01'],capture_output=True,text=True,encoding='utf-8')
            print(completed.stdout.strip(),flush=True)
            if completed.stderr:print(completed.stderr[-1500:],flush=True)
        if receipt.exists():
            r=json.loads(receipt.read_bytes());states.append(dict(module=name,status='COMPILED' if r['rc']==0 else 'MEDIDA_COMPILE_FAILED',receipt=str(receipt),receipt_sha256=sha(receipt),**r))
        else:states.append(dict(module=name,status='MEDIDA_RUNNER_FAILURE'))
        atomic(S/'BATCH_CHECKPOINT.json',dict(at=datetime.now(timezone.utc).isoformat(),states=states,remaining=order[i+1:]))
    atomic(S/'BATCH_RESULT.json',dict(at=datetime.now(timezone.utc).isoformat(),states=states,gate_changed=False))
    print('BATCH_COMPLETE',len(states),flush=True)
if __name__=='__main__':main()
