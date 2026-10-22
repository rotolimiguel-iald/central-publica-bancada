"""Compile only the candidate, preserving command, environment, times and failed attempts."""
from support_r56 import *
import re
import time

preflight()
source=ROOT/'MiguelReadingTemporalCompositionR56.lean'
stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
out=ROOT/'builds'/stamp
out.mkdir(parents=True,exist_ok=False)
lean=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
paths=[KERNEL/'.lake/build/lib/lean']
paths += sorted((KERNEL/'.lake/packages').glob('*/.lake/build/lib/lean'))
env=dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,paths)))
version=subprocess.run([str(lean),'--version'],capture_output=True,text=True,encoding='utf-8',check=True).stdout.strip()
command=[str(lean),str(source),'-o',str(out/'MiguelReadingTemporalCompositionR56.olean')]
baseline=[pin(Path(x['original']['path'])) for x in json.loads((ROOT/'SOURCES_R56.json').read_text(encoding='utf-8'))['sources']]
started=dt.datetime.now(dt.timezone.utc).isoformat();clock=time.perf_counter()
new(out/'START.json',{'start_utc':started,'command':command,'cwd':str(ROOT),'LEAN_PATH':env['LEAN_PATH'],'toolchain':version,'source':pin(source)})
p=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8')
seconds=time.perf_counter()-clock;ended=dt.datetime.now(dt.timezone.utc).isoformat()
log=new(out/'BUILD.log',f'command={json.dumps(command)}\ncwd={ROOT}\ntoolchain={version}\nLEAN_PATH={env["LEAN_PATH"]}\nstart_utc={started}\nend_utc={ended}\nseconds={seconds}\nexit_code={p.returncode}\n\nSTDOUT\n{p.stdout}\nSTDERR\n{p.stderr}')
axioms=re.findall(r"depends on axioms: \[([^]]*)\]",p.stdout)
allowed={'propext','Classical.choice','Quot.sound'}
lists=[set(a.replace('\n',' ').replace(' ','').split(','))-{''} for a in axioms]
trio_only=len(lists)==8 and all(a<=allowed for a in lists)
unchanged=all(pin(x['path'])==x for x in baseline)
receipt={'command':command,'cwd':str(ROOT),'toolchain':version,'LEAN_PATH':env['LEAN_PATH'],
 'start_utc':started,'end_utc':ended,'seconds':seconds,'exit_code':p.returncode,
 'source':pin(source),'build_log':pin(log),'axiom_declarations':len(lists),'axioms':list(map(sorted,lists)),
 'trio_only':trio_only,'no_sorry':not re.search(r'\b(sorry|admit|axiom)\b',source.read_text(encoding='utf-8')),
 'selected_original_sources_unchanged':unchanged,
 'olean':pin(out/'MiguelReadingTemporalCompositionR56.olean') if p.returncode==0 else None}
new(out/'RESULT.json',receipt)
if p.returncode==0 and trio_only and unchanged:new('BUILD_SUCCESS_R56.json',receipt)
print(json.dumps({'build':str(out),'exit':p.returncode,'axioms':len(lists),'trio_only':trio_only,'seconds':seconds},ensure_ascii=False))
if p.returncode:print(p.stdout);print(p.stderr)
