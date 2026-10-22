"""One preregistered low-energy calculation, retaining failed outcomes."""
import datetime as dt
import json
import subprocess
import sys
import time
import support_r71 as s

def main():
    plan=json.loads((s.ROOT/'PRE_REGISTRO_R71.json').read_text(encoding='utf-8'))
    review=json.loads((s.ROOT/'PREEXEC_REVIEW_R71.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    assert s.pin(s.ROOT/'PRE_REGISTRO_R71.json') in review['evidence']
    for row in plan['sources']+plan['implementation']+review['evidence']:
        assert s.pin(row['path'])['sha256']==row['sha256']
    for n in ['START_VACUUM_R71.json','RESULT_VACUUM_R71.json','COMMAND_VACUUM_R71.json']:
        assert not (s.ROOT/n).exists()
    cmd=[sys.executable,'-B','-X','utf8',str(s.ROOT/'vacuum_cost_r71.py')]
    start=dt.datetime.now(dt.timezone.utc).isoformat();t=time.perf_counter()
    s.new('START_VACUUM_R71.json',{'utc':start,'command':cmd,'plan':s.pin(s.ROOT/'PRE_REGISTRO_R71.json')})
    p=subprocess.run(cmd,capture_output=True,encoding='utf-8')
    end=dt.datetime.now(dt.timezone.utc).isoformat();elapsed=time.perf_counter()-t
    s.new('STDOUT_VACUUM_R71.txt',p.stdout);s.new('STDERR_VACUUM_R71.txt',p.stderr)
    result=json.loads(p.stdout);s.new('RESULT_VACUUM_R71.json',result)
    s.new('COMMAND_VACUUM_R71.json',{'command':cmd,'start':start,'end':end,'seconds':elapsed,'exit_code':p.returncode,'result':s.pin(s.ROOT/'RESULT_VACUUM_R71.json')})
    print(json.dumps({'passed':result['passed'],'checks':result['checks'],'rows':result['rows']}))
    raise SystemExit(p.returncode)

if __name__=='__main__':main()
