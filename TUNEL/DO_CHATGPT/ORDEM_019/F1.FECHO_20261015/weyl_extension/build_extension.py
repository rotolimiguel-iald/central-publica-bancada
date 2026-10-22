from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys,time
B=Path(__file__).resolve().parent
K=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
EXE=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p),'bytes':Path(p).stat().st_size}
def put(p,s):
 if isinstance(s,str):s=s.encode('utf-8')
 with p.open('xb') as f:f.write(s)
source=B/sys.argv[1];raw=source.read_bytes();srcpin=pin(source)
D=B/'attempts'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ');D.mkdir(parents=True)
src=D/source.name;put(src,raw);olean=src.with_suffix('.olean')
paths=[str(p/'.lake/build/lib/lean') for p in (K/'.lake/packages').iterdir() if (p/'.lake/build/lib/lean').is_dir()]
lean_path=';'.join(paths);deps=[]
for imp in re.findall(r'^import\s+([^\s]+)',raw.decode('utf-8'),re.M):
 rel=Path(*imp.split('.')).with_suffix('.olean');resolved=next(Path(p)/rel for p in paths if (Path(p)/rel).is_file());deps.append(pin(resolved))
cmd=[str(EXE),'-o',str(olean),str(src)];version=subprocess.check_output([str(EXE),'--version'],text=True,encoding='utf-8').strip()
start=now();tick=time.perf_counter();res=subprocess.run(cmd,cwd=D,env=dict(os.environ,LEAN_PATH=lean_path),stdout=subprocess.PIPE,stderr=subprocess.PIPE);sec=time.perf_counter()-tick;end=now()
put(D/'STDOUT.log',res.stdout);put(D/'STDERR.log',res.stderr);out=res.stdout.decode('utf-8');err=res.stderr.decode('utf-8')
ax={n:[a.strip() for a in v.split(',') if a.strip()] for n,v in re.findall(r"'(.+?)' depends on axioms: \[([^]]*)\]",out)}
for n in re.findall(r"'(.+?)' does not depend on any axioms",out):ax[n]=[]
assert sha(source)==srcpin['sha256'];assert all(sha(x['path'])==x['sha256'] for x in deps)
r={'unit':'F1.FECHO_20261015','claim_event':845,'command':cmd,'cwd':str(D),'toolchain':version,'LEAN_PATH':lean_path,'start_utc':start,'end_utc':end,'seconds':sec,'exit_code':res.returncode,'source':pin(src),'original':srcpin,'script':pin(__file__),'dependencies_readonly':deps,'axioms':ax,'passed':res.returncode==0 and bool(ax) and all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in ax.values()) and 'sorryAx' not in out+err,'stdout':pin(D/'STDOUT.log'),'stderr':pin(D/'STDERR.log'),'olean':pin(olean) if olean.exists() else None,'originals_memory_production_gate_touched':False}
put(D/'BUILD.log',json.dumps({k:r[k] for k in ['command','cwd','toolchain','LEAN_PATH','start_utc','end_utc','seconds','exit_code']},ensure_ascii=False,indent=2)+'\nSTDOUT\n'+out+'\nSTDERR\n'+err);r['log']=pin(D/'BUILD.log');put(D/'RECEIPT.json',json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'exit':res.returncode,'passed':r['passed'],'seconds':sec,'axioms':len(ax),'receipt':str(D/'RECEIPT.json'),'errors':out[:12000] if res.returncode else None},ensure_ascii=False));sys.exit(res.returncode)
