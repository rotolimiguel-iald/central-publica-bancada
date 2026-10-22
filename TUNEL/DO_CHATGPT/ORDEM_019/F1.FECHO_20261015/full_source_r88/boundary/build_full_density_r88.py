"""At most three new Lean attempts; canonical imports read-only, no junctions."""
import os,sys,subprocess,datetime,time,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parents[1]/'integrated_h3_r84'))
import support_r84 as support
support.ROOT=ROOT
new,pin,check=support.new,support.pin,support.check
kernel=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
lean=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
tag=sys.argv[1]
if tag not in ['1','2','3']:raise ValueError('At most three numbered attempts')
source=ROOT/('FullDensityR88_'+tag+'.lean')
out=ROOT/('FullDensityR88_'+tag+'.olean')
for name in [out.name,'FULL_BUILD_'+tag+'.json','FULL_BUILD_'+tag+'.log','FULL_START_'+tag+'.json']:
    if (ROOT/name).exists():raise FileExistsError(name)
check('FULL_BUILD_'+tag+'_PREFLIGHT')
paths=[ROOT,kernel/'.lake/build/lib/lean']+sorted((kernel/'.lake/packages').glob('*/.lake/build/lib/lean'))
env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(map(str,paths))
if re.search(r'\bsorry\b',source.read_text(encoding='utf-8')):raise ValueError('Forbidden placeholder')
cmd=[str(lean),'-o',str(out),str(source)]
version=subprocess.run([str(lean),'--version'],capture_output=True,text=True,encoding='utf-8',env=env)
if version.returncode or '4.31.0' not in version.stdout:raise RuntimeError('Wrong toolchain')
start=datetime.datetime.now(datetime.timezone.utc).isoformat();tick=time.perf_counter()
new('FULL_START_'+tag+'.json',{'command':cmd,'toolchain':version.stdout,'LEAN_PATH':env['LEAN_PATH'],'start_utc':start,'source':pin(source),'builder':pin(Path(__file__))})
r=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8')
finish=datetime.datetime.now(datetime.timezone.utc).isoformat();seconds=time.perf_counter()-tick
log=new('FULL_BUILD_'+tag+'.log',r.stdout+'\nSTDERR:\n'+r.stderr)
result=new('FULL_BUILD_'+tag+'.json',{'command':cmd,'cwd':str(ROOT),'toolchain':version.stdout,'LEAN_PATH':env['LEAN_PATH'],'start_utc':start,'finish_utc':finish,'seconds':seconds,'exit_code':r.returncode,'source':pin(source),'log':pin(log),'olean':pin(out) if out.exists() else None,'kernel_written':False})
print(result);print(r.stdout);sys.exit(r.returncode)
