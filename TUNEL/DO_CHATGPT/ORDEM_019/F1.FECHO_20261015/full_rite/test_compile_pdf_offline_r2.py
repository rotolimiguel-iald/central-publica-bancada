"""Exercise only the replacement function against local MiKTeX in fresh fixtures."""
from pathlib import Path
import ast, datetime, hashlib, json, os, shutil, subprocess, time, types
HERE=Path(__file__).resolve().parent
UNIT=HERE.parent
OUT=HERE/'pdf_patch_r2'
OUT.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size)
def save(p,obj):
    raw=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
base=UNIT/'candidate_r3/um.py'
patch=HERE/'compile_pdf_offline_r2.py'
manual=Path(r'C:\Users\rotol\AppData\Local\Programs\MiKTeX\doc\miktex\manual\miktex-pdftex.html')
binary=Path(r'C:\Users\rotol\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe')
original=base.read_text(encoding='utf-8')
node=next(n for n in ast.parse(original).body if isinstance(n,ast.FunctionDef) and n.name=='compile_pdf')
oldfun=ast.get_source_segment(original,node)
with (OUT/'compile_pdf_baseline.py').open('x',encoding='utf-8') as f:f.write(oldfun+'\n')
sourcepins=[pin(p) for p in (base,patch,manual,binary)]
envdata=json.loads(Path(r'C:\IALD\Central de Patentes\work\rite394_20261015\r3\ENVIRONMENT_PREFLIGHT_R4.json').read_bytes())
overrides=envdata['overrides']
env=dict(os.environ)
for k in envdata['unset']:env.pop(k,None)
env.update(overrides)
os.environ['TGL_NO_NETWORK']='1'
commands=[]
def run(cmd,**kw):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.perf_counter()
    kw['env']=env
    # Preserve the actual function's interfaces while custoding real engine logs.
    capture=kw.get('capture_output',False)
    if not capture:
        kw.pop('stdout',None);kw.pop('stderr',None);kw['capture_output']=True
    r=subprocess.run(cmd,**kw)
    stdout=r.stdout.encode() if isinstance(r.stdout,str) else r.stdout
    stderr=r.stderr.encode() if isinstance(r.stderr,str) else r.stderr
    ix=len(commands)
    for name,raw in [('stdout',stdout),('stderr',stderr)]:
        with (OUT/f'engine_{ix}_{name}.log').open('xb') as f:f.write(raw or b'')
    commands.append(dict(command=cmd,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
       seconds=time.perf_counter()-t,exit_code=r.returncode,cwd=str(kw.get('cwd')),logs=[pin(OUT/f'engine_{ix}_{z}.log') for z in ['stdout','stderr']]))
    return r
namespace=dict(os=os,shutil=types.SimpleNamespace(which=lambda name:str(binary)),
    subprocess=types.SimpleNamespace(run=run,DEVNULL=subprocess.DEVNULL))
exec(compile(patch.read_text(encoding='utf-8'),str(patch),'exec'),namespace)
checks=[]
for name,tex,expected in [
 ('local_ok',r'\documentclass{article}\begin{document}Offline fixture.\immediate\write18{cmd /c echo unexpected>write18_marker.txt}\end{document}',True),
 ('stale_pdf_then_failure',r'\documentclass{article}\usepackage{iald_unavailable_package_negative_control_20261015}\begin{document}Failure must override stale PDF.\end{document}',False),
 ('missing_package',r'\documentclass{article}\usepackage{iald_unavailable_package_negative_control_20261015}\begin{document}Never downloaded.\end{document}',False),
]:
    dest=OUT/name;dest.mkdir()
    with (dest/'fixture.tex').open('x',encoding='utf-8') as f:f.write(tex+'\n')
    if name=='stale_pdf_then_failure':
        with (dest/'fixture.pdf').open('xb') as f:f.write((OUT/'local_ok/fixture.pdf').read_bytes())
    namespace['OUT']=str(dest)
    actual=namespace['compile_pdf']('fixture')
    checks.append(dict(name=name,actual=actual,expected=expected,passed=actual is expected))
    checks.append(dict(name=name+'_write18_absent',passed=not(dest/'write18_marker.txt').exists()))
for rec in commands:
    if '--version' not in rec['command']:
        checks.append(dict(name='explicit_offline_options_'+str(len(checks)),
            passed=all(flag in rec['command'] for flag in ['--disable-installer','--disable-write18'])))
checks.append(dict(name='source_pins_unchanged',passed=all(sha(Path(p['path']))==p['sha256'] for p in sourcepins)))
baseline_ast=ast.dump(node,include_attributes=False)
result=dict(scope='isolated actual replacement function, no um.py import or scientific rite',
    baseline_source=sourcepins[0],baseline_function_lines=[node.lineno,node.end_lineno],
    baseline_function_ast_sha256=hashlib.sha256(baseline_ast.encode()).hexdigest(),
    replacement=sourcepins[1],source_pins=sourcepins,
    manual_lines=dict(disable_installer=[49,52],disable_write18=[52,53]),
    manual_semantics='--disable-installer overrides configuration data store; --disable-write18 forbids command execution',
    environment=overrides,commands=commands,checks=checks,passed=all(c['passed'] for c in checks),
    os_sandbox_claimed=False,whole_rite_run=False,
    limitations=['Native process confinement is not provided by the Python audit hook.',
      'Both engine exit codes must be zero; a stale PDF cannot override failure.',
      'Other TeX engines retain existing options; only the actually identified MiKTeX branch is hardened here.'])
save(OUT/'PDF_PATCH_RECEIPT_R2.json',result)
print(json.dumps(dict(passed=result['passed'],checks=len(checks),receipt=str(OUT/'PDF_PATCH_RECEIPT_R2.json'),sha256=sha(OUT/'PDF_PATCH_RECEIPT_R2.json'))))
raise SystemExit(0 if result['passed'] else 1)
