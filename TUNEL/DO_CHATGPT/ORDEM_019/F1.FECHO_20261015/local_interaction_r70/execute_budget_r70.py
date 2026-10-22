"""Execute once after verifying the frozen synthetic plan and implementation."""
import datetime as dt
import json
import subprocess
import sys
import time
import support_r70 as s

def main():
    plan=json.loads((s.ROOT/'PRE_REGISTRO_CAUSAL_R70.json').read_text(encoding='utf-8'))
    for row in plan['pins']:
        assert s.pin(row['path']) == row
    for name in ['START_CAUSAL_R70.json','RESULT_CAUSAL_R70.json','COMMAND_CAUSAL_R70.json']:
        assert not (s.ROOT/name).exists()
    command=[sys.executable,'-B','-X','utf8',str(s.ROOT/'causal_budget_r70.py')]
    start=dt.datetime.now(dt.timezone.utc).isoformat()
    s.new('START_CAUSAL_R70.json',{'utc':start,'command':command,'plan':s.pin(s.ROOT/'PRE_REGISTRO_CAUSAL_R70.json')})
    t=time.perf_counter()
    p=subprocess.run(command,capture_output=True,encoding='utf-8')
    elapsed=time.perf_counter()-t
    end=dt.datetime.now(dt.timezone.utc).isoformat()
    s.new('STDOUT_CAUSAL_R70.txt',p.stdout)
    s.new('STDERR_CAUSAL_R70.txt',p.stderr)
    s.new('RESULT_CAUSAL_R70.json',json.loads(p.stdout))
    s.new('COMMAND_CAUSAL_R70.json',{'command':command,'start':start,'end':end,'seconds':elapsed,'exit_code':p.returncode,'result':s.pin(s.ROOT/'RESULT_CAUSAL_R70.json')})
    print(p.stdout)
    raise SystemExit(p.returncode)

if __name__=='__main__':main()
