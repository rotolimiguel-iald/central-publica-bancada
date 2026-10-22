"""One reviewed R75 scientific launch; receipts and no implicit retry."""
import datetime as dt, json, os, subprocess, sys
import support_r75 as s

def main():
    for name in ['LAUNCH_INTENT_R75.json','START_R75.json','RESULT_R75.json','FREEZE_R75.json']:
        assert not (s.ROOT/name).exists(),name
    m=s.project('EXEC_PROJECT')
    for tid in ['R4','R5']:
        task=next(x for x in m['projection']['active'] if x['id']==tid)
        s.call({'operation':'check','reference':s.REF,'actor':s.ACTOR,'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],'task_id':tid,'lease_id':task['lease']['id']},'EXEC_CHECK_'+tid)
    cmd=[sys.executable,'-B','-X','utf8',str(s.ROOT/'run_bosonic_readout_r75.py')]
    env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    s.new('LAUNCH_INTENT_R75.json',{'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'command':cmd,'environment_overrides':{'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'},'execution_count':1})
    f=subprocess.run([sys.executable,'-B','-X','utf8',str(s.ROOT/'freeze_r75.py')],capture_output=True,encoding='utf-8')
    s.new('FREEZE_COMMAND_R75.json',{'exit_code':f.returncode,'stdout':f.stdout,'stderr':f.stderr})
    assert f.returncode==0,f.stderr
    p=subprocess.run(cmd,capture_output=True,encoding='utf-8',env=env)
    s.new('LAUNCH_RESULT_R75.json',{'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'ended_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    print(p.stdout,p.stderr)
    return p.returncode
if __name__=='__main__':raise SystemExit(main())

