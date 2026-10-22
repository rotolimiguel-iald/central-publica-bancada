"""Close the documented UDP audit-event gap without changing scientific code."""
from pathlib import Path
import ast, hashlib, json
HERE=Path(__file__).resolve().parent
def emit(name,text):
 ast.parse(text)
 with (HERE/name).open('x',encoding='utf-8',newline='\n') as f:f.write(text)
guard=(HERE/'sitecustomize_rite_r3.py').read_text(encoding='utf-8')
old='"socket.gethostbyaddr"}'
assert old in guard
guard=guard.replace(old,'"socket.gethostbyaddr", "socket.getnameinfo", "socket.sendto", "socket.sendmsg"}')
emit('sitecustomize_rite_r4.py',guard)
test=(HERE/'test_guard_paths_r3b.py').read_text(encoding='utf-8')
test=test.replace('guard_r3_test_b','guard_r4_test').replace('sitecustomize_rite_r3.py','sitecustomize_rite_r4.py').replace('GUARD_PATHS_R3B_RESULT','GUARD_PATHS_R4_RESULT')
marker="print(json.dumps({'checks':checks,'passed':all(x['passed'] for x in checks)}))"
extra="""# The real UDP call must be stopped by the audit event before transmission.
with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as udp:
 refused('UDP_sendto_refused_before_transmission',lambda:udp.sendto(b'guard-probe',('127.0.0.1',9)))
refused('reverse_lookup_getnameinfo_refused',lambda:socket.getnameinfo(('127.0.0.1',9),0))
import sys
refused('sendmsg_audit_event_refused',lambda:sys.audit('socket.sendmsg',None,('127.0.0.1',9)))
"""
assert marker in test
test=test.replace(marker,extra+marker)
emit('test_guard_paths_r4.py',test)
for source,target in [('launch_full_rite_r3a.py','launch_full_rite_r4.py'),('preflight_engine_r3.py','preflight_engine_r4.py')]:
 text=(HERE/source).read_text(encoding='utf-8')
 assert 'sitecustomize_rite_r3.py' in text
 emit(target,text.replace('sitecustomize_rite_r3.py','sitecustomize_rite_r4.py'))
print(json.dumps({'guard':'sitecustomize_rite_r4.py','launcher':'launch_full_rite_r4.py','source_unchanged':True}))
