"""Compile a new sandbox artifact without writing into the canonical kernel."""
import os, sys, subprocess, datetime, time
from pathlib import Path
from support_r81 import ROOT,new,pin,check
kernel=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
lean=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
tag=sys.argv[1]
out=ROOT/('RecoveryAreaCoefficient_'+tag+'.olean')
for name in [out.name,'BUILD_'+tag+'.json','BUILD_'+tag+'.log']:
    if (ROOT/name).exists():raise FileExistsError(name)
check('BUILD_'+tag+'_PREFLIGHT')
paths=[kernel/'.lake/build/lib/lean']+sorted((kernel/'.lake/packages').glob('*/.lake/build/lib/lean'))
env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(map(str,paths))
source=ROOT/'RecoveryAreaCoefficient.lean'
assert 'sorry' not in source.read_text(encoding='utf-8')
cmd=[str(lean),'-o',str(out),str(source)]
version=subprocess.run([str(lean),'--version'],capture_output=True,text=True,encoding='utf-8',env=env)
start=datetime.datetime.now(datetime.timezone.utc).isoformat();tick=time.perf_counter()
r=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8')
finish=datetime.datetime.now(datetime.timezone.utc).isoformat();seconds=time.perf_counter()-tick
log=new('BUILD_'+tag+'.log',r.stdout+'\nSTDERR:\n'+r.stderr)
result=new('BUILD_'+tag+'.json',{'command':cmd,'cwd':str(ROOT),'toolchain':version.stdout,'LEAN_PATH':env['LEAN_PATH'],'start_utc':start,'finish_utc':finish,'seconds':seconds,'exit_code':r.returncode,'source':pin(source),'log':pin(log),'olean':pin(out) if out.exists() else None,'kernel_written':False})
print(result);print(r.stdout);sys.exit(r.returncode)
