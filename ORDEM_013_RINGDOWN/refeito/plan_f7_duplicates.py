"""Plan exact duplicate removal; no files are removed by this command."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os

ROOT=Path(__file__).resolve().parents[1].resolve()
CACHE=(ROOT/'cache').resolve()
errors=[]
def walk(root):
    for parent,dirs,files in os.walk(root,onerror=lambda e:errors.append(str(e)),followlinks=False):
        dirs[:]=[x for x in dirs if not (Path(parent)/x).is_symlink()]
        for name in files:
            p=Path(parent)/name
            try:
                if not p.is_symlink(): yield p,p.stat().st_size
            except OSError as e: errors.append(str(e))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while block:=f.read(4*1024*1024): h.update(block)
    return h.hexdigest()

targets=[]
for p,size in walk(ROOT):
    if size>25_000_000 and not p.resolve().is_relative_to(CACHE):
        targets.append((p,size))
sizes={size for p,size in targets}
candidates={}
for subtree in ('public','gwosc'):
    for p,size in walk(CACHE/subtree):
        if size in sizes: candidates.setdefault(size,[]).append(p)
known={}
rows=[]
for p,size in targets:
    resolved=p.resolve()
    if not resolved.is_relative_to(ROOT): raise ValueError('Target outside bench')
    rel=resolved.relative_to(ROOT)
    digest=sha(resolved)
    hits=[]
    for q in candidates.get(size,[]):
        if q not in known: known[q]=sha(q)
        if known[q]==digest:
            hits.append(q)
            break
    canonical=hits[0].resolve() if hits else None
    allowed=bool(canonical and rel.parts[0].startswith('C7_') and canonical.is_relative_to(CACHE))
    rows.append(dict(path=str(resolved),bytes=size,sha256=digest,
                     canonical_path=str(canonical) if canonical else None,
                     canonical_sha256=known[hits[0]] if hits else None,
                     exact_duplicate=bool(hits),eligible_for_authorized_removal=allowed))
result=dict(status='PLAN_ONLY_NO_DELETION',utc=datetime.now(timezone.utc).isoformat(),
            root=str(ROOT),cache_root=str(CACHE),entries=rows,access_errors=errors,
            removal_count=sum(r['eligible_for_authorized_removal'] for r in rows),
            removal_bytes=sum(r['bytes'] for r in rows if r['eligible_for_authorized_removal']))
out=ROOT/'bis/F7_DUPLICATE_REMOVAL_PLAN.json'
with out.open('x',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k!='entries'},ensure_ascii=False,indent=2))
print('plan_sha256',sha(out))
