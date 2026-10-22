from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid
H=Path(__file__).resolve().parent
src=H/'bilocal_regulator_controls_check.py'
dst=H/'bilocal_regulator_controls_check_v2.py'
text=src.read_text('utf-8').replace("D=H/'bilocal_regulator_controls'","D=H/'bilocal_regulator_controls_v2'").replace('s.simplify(f)==0','s.simplify(f.subs(B.w,B.xx))==0')
assert text!=src.read_text('utf-8')
def put(p,b):
    assert not p.exists(),p;t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
put(dst,text.encode())
put(H/'bilocal_regulator_controls_v2_generation.json',json.dumps(dict(
    at=datetime.now(timezone.utc).isoformat(),supersedes=str(src),
    predecessor_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
    predecessor_exit_code=1,predecessor_log_sha256=hashlib.sha256((H/'bilocal_regulator_controls_run.log').read_bytes()).hexdigest(),
    reason='Auxiliary radius w was compared before imposing w=sum(x²); residual 2/3*(1-X²/w) is zero on physical locus',
    modification='Only test simplification substitutes w=X²; no kernel or contact coefficient modified',
    new_sha256=hashlib.sha256(dst.read_bytes()).hexdigest()),indent=2).encode())
