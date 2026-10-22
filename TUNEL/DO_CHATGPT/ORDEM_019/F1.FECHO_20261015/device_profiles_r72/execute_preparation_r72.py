"""Execute once after preregistration and distinct pre-execution review."""
import datetime as dt,json,subprocess,sys,time
import support_r72 as s
for name in ['START_PREPARATION_R72.json','RESULT_PREPARATION_R72.json','PREPARATION_STDOUT_R72.txt','PREPARATION_STDERR_R72.txt','COMMAND_PREPARATION_R72.json']:
    assert not (s.ROOT/name).exists(), name
r=json.loads((s.ROOT/'PREEXEC_REVIEW_R72.json').read_text(encoding='utf-8'))
assert r['status'].startswith('PASS') and r['reviewer']!=s.ACTOR['id']
for p in r['evidence']:assert s.pin(p['path'])==p
for n in ['PRE_REGISTRO_PREPARATION_R72.json','PREPARATION_WITNESS_R72.md','preparation_witness_r72.py','support_r72.py']:assert s.pin(s.ROOT/n) in r['evidence']
m=s.project('EXECUTION_PROJECT')
t=next(t for t in m['projection']['active'] if t['id']=='R4')
s.call({'operation':'check','reference':s.REF,'actor':s.ACTOR,'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],'task_id':'R4','lease_id':t['lease']['id']},'EXECUTION_CHECK')
cmd=[sys.executable,'-B','-X','utf8',str(s.ROOT/'preparation_witness_r72.py')]
start=dt.datetime.now(dt.timezone.utc).isoformat();s.new('START_PREPARATION_R72.json',{'command':cmd,'start':start,'review':s.pin(s.ROOT/'PREEXEC_REVIEW_R72.json')})
a=time.monotonic();p=subprocess.run(cmd,capture_output=True,encoding='utf-8');elapsed=time.monotonic()-a
s.new('PREPARATION_STDOUT_R72.txt',p.stdout);s.new('PREPARATION_STDERR_R72.txt',p.stderr)
s.new('COMMAND_PREPARATION_R72.json',{'command':cmd,'start':start,'end':dt.datetime.now(dt.timezone.utc).isoformat(),'seconds':elapsed,'exit_code':p.returncode,'result':s.pin(s.ROOT/'RESULT_PREPARATION_R72.json') if (s.ROOT/'RESULT_PREPARATION_R72.json').exists() else None})
print(p.stdout,p.stderr);raise SystemExit(p.returncode)
