"""Execute the reviewed R2 plan once, with current mission preflight."""
import subprocess,sys,os,datetime as dt
import support_r79 as s

def main():
    assert not (s.ROOT/'LAUNCH_R79_INTENT.json').exists()
    ready=s.check('EXECUTION_PREFLIGHT')
    assert ready['ready']
    s.new('LAUNCH_R79_INTENT.json',{'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'plan':s.pin(s.ROOT/'PLAN_R79.json'),'environment':{'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}})
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    for name in ['freeze_r79.py','run_optical_drive_r79.py']:
        cmd=[sys.executable,'-B','-X','utf8',str(s.ROOT/name)]
        r=subprocess.run(cmd,capture_output=True,encoding='utf-8',env=env)
        s.new('LAUNCH_'+name.replace('.py','')+'.json',{'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'ended_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
        print(r.stdout)
        if r.returncode:raise RuntimeError(name+' failed; no automatic retry')
if __name__=='__main__':main()
