from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys,time
B=Path(__file__).resolve().parent
K=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def put(p,b):
 if isinstance(b,str):b=b.encode('utf-8')
 with p.open('xb') as f:f.write(b)
src=B/sys.argv[1];raw=src.read_bytes();assert src.parent==B
assert not re.search(r'\b(?:sorry|admit|axiom)\b',re.sub(r'/\-.*?\-/','',raw.decode('utf-8'),flags=re.S))
D=B/'attempts'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ');D.mkdir(parents=True,exist_ok=False)
copy=D/src.name;put(copy,raw);out=copy.with_suffix('.olean')
base=json.loads((B.parent/'gamma_unbounded/attempts/20261015T194946_301445Z/RECEIPT.json').read_text(encoding='utf-8'))
extra=json.loads((B.parent/'weyl_net_wiring/attempts/20261015T202537_872158Z/RECEIPT.json').read_text())
roots=[D]+[Path(x) for x in base['LEAN_PATH'].split(';')]+[Path(x) for x in extra['LEAN_PATH'].split(';')]
for q in sorted((B/'attempts').glob('*/RECEIPT.json')):
 r=json.loads(q.read_text(encoding='utf-8'))
 if r.get('passed'):roots.insert(1,q.parent)
lp=';'.join(map(str,roots));cmd=[str(LEAN),'-R',str(D),'-o',str(out),str(copy)]
ver=subprocess.check_output([str(LEAN),'--version'],text=True).strip();start=now();t=time.perf_counter()
p=subprocess.run(cmd,cwd=D,env=dict(os.environ,LEAN_PATH=lp),capture_output=True);sec=time.perf_counter()-t;end=now()
put(D/'STDOUT.log',p.stdout);put(D/'STDERR.log',p.stderr)
s=p.stdout.decode('utf-8');ax={n:[v.strip() for v in vs.split(',') if v.strip()] for n,vs in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",s,re.S)}
for n in re.findall(r"'([^']+)' does not depend on any axioms",s):ax[n]=[]
for line in s.splitlines():
 if line.startswith('LOCAL_DECL\t'):
  _,n,values=line.split('\t');ax[n]=[v for v in values.split(',') if v]
passed=p.returncode==0 and bool(ax) and all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in ax.values()) and 'sorryAx' not in s
assert src.read_bytes()==raw
r={'unit':'F1.FECHO_20261015','claim':845,'start_utc':start,'end_utc':end,'seconds':sec,'command':cmd,'toolchain':ver,'LEAN_PATH':lp,'exit_code':p.returncode,'passed':passed,'source':pin(src),'compiled_source':pin(copy),'olean':pin(out) if out.exists() else None,'axioms':ax,'stdout':pin(D/'STDOUT.log'),'stderr':pin(D/'STDERR.log'),'script':pin(__file__),'canonical_modified':False}
put(D/'BUILD.log',json.dumps({k:r[k] for k in ['start_utc','end_utc','seconds','command','toolchain','LEAN_PATH','exit_code']},ensure_ascii=False,indent=2)+'\nSTDOUT\n'+s+'\nSTDERR\n'+p.stderr.decode('utf-8'))
r['build_log']=pin(D/'BUILD.log');put(D/'RECEIPT.json',json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':passed,'exit':p.returncode,'seconds':sec,'receipt':pin(D/'RECEIPT.json'),'stdout':s if not passed else list(ax)},ensure_ascii=False))
sys.exit(0 if passed else 1)
