"""Record inaccessible sources without aborting directory diagnostics; no content on seeds."""
from pathlib import Path
import hashlib,json,ast,subprocess,time
from datetime import datetime,timezone
B=Path(__file__).resolve().parents[2];D=B/'bis/015/t13'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,obj):
    raw=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    with p.open('xb') as f:f.write(raw)
def main():
    src=B/'refeito/final_integrity_015_v2.py';dst=B/'refeito/final_integrity_015_v3.py'
    s=src.read_text('utf-8').replace('def main():', '''read_errors = []
def audited_read(p):
    try: return sha(p),p.stat().st_size
    except OSError as exc:
        read_errors.append(dict(path=str(p),error=str(exc),type=type(exc).__name__))
        return None,None

def main():''')
    s=s.replace('digest = sha(p)','digest, size = audited_read(p)').replace('bytes=p.stat().st_size','bytes=size')
    s=s.replace('directory_enumeration_errors=scan_errors,','directory_enumeration_errors=scan_errors, frozen_read_errors=read_errors,')
    s=s.replace("'bis/015/t13/FINAL_INTEGRITY_015_'","'bis/015/t13/FINAL_INTEGRITY_015_v3_'")
    s=s.replace('lstat_bytes=p.lstat().st_size','lstat_bytes=None')
    ast.parse(s)
    with dst.open('xb') as f:f.write(s.encode())
    start=time.perf_counter();p=subprocess.run(['C:\\Python314\\python.exe','-X','utf8','-B',str(dst)],capture_output=True)
    for suffix,raw in [('stdout',p.stdout),('stderr',p.stderr)]:
        with (D/('INTEGRITY_V3.'+suffix+'.log')).open('xb') as f:f.write(raw)
    r=dict(at=datetime.now(timezone.utc).isoformat(),rc=p.returncode,wall_seconds=time.perf_counter()-start,script_sha256=sha(dst),predecessor_sha256=sha(src),prior_default_attempt='V2 PermissionError hashing canonical um.py; no receipt, shell displayed exit0 due to trailing Get-Item. No PASS claimed.')
    if p.returncode==0:
        o=json.loads(p.stdout);r.update(receipt=o['receipt'],status=o['status'],directory_errors=o['directory_enumeration_errors'],read_errors=o['frozen_read_errors'])
    put(D/'INTEGRITY_V3_RUN.json',r)
    print(json.dumps(r,ensure_ascii=False))
if __name__=='__main__':main()
