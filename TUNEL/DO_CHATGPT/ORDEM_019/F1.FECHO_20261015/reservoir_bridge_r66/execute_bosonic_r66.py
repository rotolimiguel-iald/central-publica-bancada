"""Capture command, times, stdout, stderr and exit once for the bosonic check."""
import datetime as dt,sys,subprocess,time
import support_r66 as s
cmd=[sys.executable,'-B','-X','utf8',str(s.ROOT/'run_bosonic_r66.py')]
s.new('BOSONIC_COMMAND_INTENT_R66.json',{'command':cmd,'started_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
t=time.perf_counter();cp=subprocess.run(cmd,capture_output=True,encoding='utf-8')
s.new('BOSONIC_STDOUT_R66.log',cp.stdout);s.new('BOSONIC_STDERR_R66.log',cp.stderr)
s.new('BOSONIC_COMMAND_RESULT_R66.json',{'command':cmd,'exit_code':cp.returncode,'seconds':time.perf_counter()-t,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'stdout':s.pin(s.ROOT/'BOSONIC_STDOUT_R66.log'),'stderr':s.pin(s.ROOT/'BOSONIC_STDERR_R66.log')})
print(cp.stdout);print(cp.stderr);raise SystemExit(cp.returncode)
