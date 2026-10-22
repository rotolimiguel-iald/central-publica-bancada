"""New immutable supplements: reject internal paths before any mkdir."""
from pathlib import Path
import ast, hashlib, json, subprocess, sys, zipfile
B=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f: f.write(raw)
records=[]
for base in ['C7_POSTERIOR_REPRODUCTION','C7_GWTC3_REPRODUCTION','C7_INJECTION_REPRODUCTION']:
    old=B/(base+'_v3_1');out=B/(base+'_v3_2')
    if out.exists(): raise FileExistsError(out)
    m=json.loads((old/'MANIFEST.json').read_bytes());content={}
    for r in m['shipped_files']:
        p=old/r['path']
        if sha(p)!=r['sha256']: raise ValueError('Changed source')
        content[r['path']]=p.read_bytes()
    s=content['reproduce.py'].decode('utf-8')
    before="""    workroot=args.work_root.resolve();workroot.mkdir(parents=True,exist_ok=True)
    outputroot=args.output_root.resolve();outputroot.mkdir(parents=True,exist_ok=True)
    if outputroot.is_relative_to(ROOT.resolve()) or workroot.is_relative_to(ROOT.resolve()):
        raise ValueError('Work/output directories must be outside immutable package')
"""
    after="""    workroot=args.work_root.resolve()
    outputroot=args.output_root.resolve()
    if outputroot.is_relative_to(ROOT.resolve()) or workroot.is_relative_to(ROOT.resolve()):
        raise ValueError('Work/output directories must be outside immutable package')
    workroot.mkdir(parents=True,exist_ok=True)
    outputroot.mkdir(parents=True,exist_ok=True)
"""
    if s.count(before)!=1: raise ValueError('Nonunique anchor')
    s=s.replace(before,after);ast.parse(s);content['reproduce.py']=s.encode('utf-8')
    content['README.md']+=b'\nRevision v3_2: work and output roots are resolved and rejected when internal BEFORE any mkdir. The earlier finally protection and frozen scientific assets are unchanged.\n'
    for n,raw in content.items(): new(out/n,raw)
    m['supersedes_manifest_sha256']=sha(old/'MANIFEST.json')
    m['shipped_files']=[dict(path=n,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()) for n,raw in sorted(content.items())]
    new(out/'MANIFEST.json',(json.dumps(m,indent=2)+'\n').encode())
    archive=B/'cache'/(out.name+'.zip')
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for p in out.rglob('*'):
            if p.is_file(): z.write(p,out.name+'/'+p.relative_to(out).as_posix())
    # Execute only the actual confinement block, under optimization, with mock paths.
    block=s[s.index('    workroot=args.work_root.resolve()'):s.index('    preserved=outputroot/')]
    events=[]
    class P:
        def __init__(self,inside=False): self.inside=inside
        def resolve(self): return self
        def is_relative_to(self,root): return self.inside
        def mkdir(self,**kw): events.append('mkdir')
    class Args: pass
    checks=[]
    for w,o in [(True,False),(False,True)]:
        events.clear();a=Args();a.work_root=P(w);a.output_root=P(o)
        try: exec(compile(__import__('textwrap').dedent(block),'<actual block>','exec',optimize=1),dict(args=a,ROOT=P()))
        except ValueError: pass
        else: raise ValueError('Internal path accepted')
        if events: raise ValueError('Mutation before refusal')
        checks.append(dict(work_internal=w,output_internal=o,mkdir=0))
    work=B/'cache/supplement_cleanup_v3_2';logs=B/'bis/supplement_cleanup_v3_2';work.mkdir(exist_ok=True);logs.mkdir(exist_ok=True)
    cmd=[sys.executable,'-B',str(out/'reproduce.py'),next(iter(m['stages'])),'--prepare-only','--work-root',str(work),'--output-root',str(logs),'--source-root',str(B/'cache/INTENTIONALLY_ABSENT_SOURCE')]
    p=subprocess.run(cmd,capture_output=True);new(logs/(out.name+'.log'),p.stdout+p.stderr)
    if p.returncode==0 or b'FileNotFoundError' not in p.stderr or list(work.iterdir()): raise ValueError('Missing-input cleanup failed')
    records.append(dict(package=out.name,archive=str(archive.relative_to(B)),sha256=sha(archive),manifest_sha256=sha(out/'MANIFEST.json'),internal_path_tests=checks,expected_failure_test=True,temporary_removed=True))
new(B/'bis/C7_SUPPLEMENTS_V3_2_BUILD.json',(json.dumps(dict(packages=records,builder_sha256=sha(Path(__file__))),indent=2)+'\n').encode())
# New final bundle builder, preserving the previous final bundle and verifier receipt.
src=B/'refeito/build_final_bundle_v3_final_013bis.py'
s=src.read_text(encoding='utf-8')
for base in ['POSTERIOR','GWTC3','INJECTION']: s=s.replace('C7_'+base+'_REPRODUCTION_v3_1','C7_'+base+'_REPRODUCTION_v3_2')
s=s.replace('C7_SUPPLEMENTS_V3_1_BUILD','C7_SUPPLEMENTS_V3_2_BUILD')
s=s.replace('TGL_RINGDOWN_DELIVERY_v3','TGL_RINGDOWN_DELIVERY_v3_1').replace('C7_FINAL_BUNDLE_V3_','C7_FINAL_BUNDLE_V3_1_')
s=s.replace('research delivery v3','research delivery v3_1')
ast.parse(s);new(B/'refeito/build_final_bundle_v3_1_013bis.py',s.encode('utf-8'))
print('PASS',len(records),'supplements; six no-mkdir refusals; three missing-input cleanups')
