"""One-shot continuation of the existing null campaign, ending before PE."""
from pathlib import Path
from datetime import datetime,timezone
import sys,os,time,json,subprocess,hashlib
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[1];ROOT=B.parent
CODE=B/'bis/e2_code_v1_1_2';sys.path.insert(0,str(CODE))
from registration_guard import checked_registration,load_authorized_configuration,sha,publish_new

def main():
    assert os.name=='posix' and Path('/proc/self').exists(),'WSL process inspection required'
    out=D/'post_nulls_001';out.mkdir(exist_ok=False)
    started=datetime.now(timezone.utc).isoformat();mono=time.monotonic();steps=[]
    publish_new(out/'PLAN.json',dict(started_utc=started,script_sha256=sha(Path(__file__)),
        source_campaign='nulls_campaign_001',never_launches_nulls=True,never_launches_PE=True,
        wait_seconds=1200,order=['deliver_T03','register_budget_v2','verify_budget_chain','pool_fixture','qualify400']))
    try:
        while not (D/'nulls_campaign_001/RESULT.json').exists():
            if list((ROOT/'TUNEL/PARA_CHATGPT').glob('RECIBO_016_FECHAMENTO_PARCIAL*.md')):
                raise RuntimeError('Management receipt takes precedence')
            if time.monotonic()-mono>1200:raise TimeoutError('Existing null result still absent; inspect original handle, never relaunch')
            time.sleep(5)
        def run(script,*args):
            stage=script.stem
            command=[sys.executable,'-B',str(script),*args]
            at=datetime.now(timezone.utc).isoformat();before=time.monotonic()
            print(json.dumps(dict(stage=stage,status='STARTING',at=at)),flush=True)
            # Existing bounded controllers retain process ownership and ceilings.
            # This parent is one additional process: fixture topology totals28.
            with (out/(stage+'.log')).open('xb') as log:
                child=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
            row=dict(stage=stage,started_utc=at,finished_utc=datetime.now(timezone.utc).isoformat(),
                command=command,returncode=child.returncode,wall_seconds=time.monotonic()-before,
                script_sha256=sha(script),log_sha256=sha(out/(stage+'.log')))
            steps.append(row);publish_new(out/(stage+'_RECEIPT.json'),row)
            print(json.dumps(row),flush=True)
            if child.returncode:raise RuntimeError('Stage failed: '+stage)
        run(D/'deliver_nulls_campaign.py')
        from t03_terminal_guard import require_terminal
        terminal=require_terminal(D)
        publish_new(out/'T03_TERMINAL.json',terminal)
        run(D/'prepare_budget_v2_checked.py')
        reg,digest=checked_registration();view=load_authorized_configuration(reg,digest)
        assert view['_allocation_sha256']==sha(B/'ORCAMENTO_015_v2.json')
        publish_new(out/'ALLOCATION_VERIFIED.json',dict(registration_sha256=digest,
            allocation_sha256=view['_allocation_sha256'],status='CHAIN_VERIFIED'))
        run(D/'t04/process_lifecycle_fixture.py')
        fixture=json.loads((D/'t04/process_lifecycle_fixture_001/RESULT.json').read_bytes())
        assert fixture['status']=='POOL24_LIFECYCLE_OBSERVED' and fixture['cleanup_confirmed']
        run(D/'t04/supervise_t04_v3.py','qualify')
        q=json.loads((D/'t04/qualify/RESULT.json').read_bytes())
        assert q['status']=='T04_ADAPTER_400_QUALIFIED'
        result=dict(status='T04_READY_FOR_MANUAL_RECEIPT_REVIEW_BEFORE_PILOT',steps=steps,
            qualification_sha256=sha(D/'t04/qualify/RESULT.json'),pilot_launched=False,
            machine_accounting='Use T03union,fixturewall,qualificationwall;parent wait is not an additional interval',
            gate_changed=False)
    except Exception as exc:
        result=dict(status='POST_NULLS_STOPPED_INSPECT_WITHOUT_RETRY',steps=steps,
            error=dict(type=type(exc).__name__,message=str(exc)),pilot_launched=False,gate_changed=False)
    result.update(started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),wall_seconds=time.monotonic()-mono)
    publish_new(out/'RESULT.json',result);print(json.dumps(result),flush=True)
    if result['status']!='T04_READY_FOR_MANUAL_RECEIPT_REVIEW_BEFORE_PILOT':raise SystemExit(2)
if __name__=='__main__':main()
