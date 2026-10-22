from pathlib import Path
import json,subprocess,sys,time
B=Path(__file__).resolve().parent
rp=B/'nonabelian/RECEIPT_R1.json';deadline=time.monotonic()+900
while not rp.exists():
 if time.monotonic()>deadline:raise TimeoutError('No accepted Nonabelian review receipt')
 time.sleep(1)
r=json.loads(rp.read_text(encoding='utf-8'));assert r['passed']
for script in ['audit_all_local_r1.py','assemble_reviews_r1.py']:
 r=subprocess.run([sys.executable,'-B','-X','utf8',str(B/script)])
 if r.returncode:raise SystemExit(r.returncode)
