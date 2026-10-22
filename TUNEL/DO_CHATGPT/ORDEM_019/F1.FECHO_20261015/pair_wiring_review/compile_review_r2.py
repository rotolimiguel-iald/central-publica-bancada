from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys,time
B=Path(__file__).resolve().parent
P=B.parent
TRIO={'propext','Classical.choice','Quot.sound'}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p),'bytes':Path(p).stat().st_size}
def put(p,raw):
 if isinstance(raw,str):raw=raw.encode('utf-8')
 with p.open('xb') as f:f.write(raw)
 assert p.read_bytes()==raw
name=sys.argv[1];rp=Path(sys.argv[2]);r=json.loads(rp.read_text(encoding='utf-8'))
assert r['exit_code']==0
original=Path(r['source']['path']);assert sha(original)==r['source']['sha256']
text=original.read_text(encoding='utf-8');assert not re.search(r'\b(?:sorry|admit|axiom)\b',re.sub(r'/\-.*?\-/','',text,flags=re.S))
D=B/name;D.mkdir(exist_ok=False)
source_root=D/'src';source_root.mkdir()
rel=Path('TGLExt')/original.name if name=='maxwell' else Path(original.name)
source=source_root/rel;source.parent.mkdir(parents=True,exist_ok=True);put(source,original.read_bytes())
output=D/'lib'/rel.with_suffix('.olean');output.parent.mkdir(parents=True,exist_ok=True)
paths=r['LEAN_PATH'].split(';')
upstream = {
 'assembly': [], 'assembly_r4': [], 'flow': [], 'closability': [], 'symplectic': [], 'anti': [],
 'closed': [('closability', 'PairTomitaClosabilityR2')],
 'wedgepair': [('closed','PairClosedTomitaR2'), ('closability','PairTomitaClosabilityR2')],
}[name]
paths=[str(D/'lib')]+[x for x in paths if Path(x)!=rp.parent]
for dirname,modname in upstream:
 lib=B/dirname/'lib';assert (lib/(modname+'.olean')).is_file()
 paths=[str(lib)]+[x for x in paths if not (Path(x)/(modname+'.olean')).is_file()]
if name not in {'closability','closed','symplectic'}:
 for dirname,modname in [('vectors','ExponentialVectorsR3'),('totality','ExponentialTotalityR4')]:
  lib=P/'exponential_review'/dirname/'lib';assert (lib/(modname+'.olean')).is_file()
  paths=[str(lib)]+[x for x in paths if not (Path(x)/(modname+'.olean')).is_file()]
 for dirname,modname in [('field','FieldWeylR3'),('continuity','ConcreteWeylContinuityR2'),('concrete','ConcreteWeylR1'),('covariance','WeylCovarianceR1'),('operators','WeylOperatorsGenericR2'),('coefficients','WeylCoefficientsR4')]:
  lib=P/'weyl_review'/dirname/'lib';assert (lib/(modname+'.olean')).is_file()
  paths=[str(lib)]+[x for x in paths if not (Path(x)/(modname+'.olean')).is_file()]
if name in {'wedgepair','assembly_r4'}:
 for dirname,modname in [('analytic','WedgeAnalyticR2'),('span','StandardComplexSpanR1'),('totality','RealSubspaceTotalityR5'),('cyclic','WedgeCyclicR3')]:
  lib=P/'wedge_review'/dirname/'lib';assert (lib/(modname+'.olean')).is_file()
  paths=[str(lib)]+[x for x in paths if not (Path(x)/(modname+'.olean')).is_file()]
lean_path=';'.join(paths)
deps=[rp,original]
for x in r.get('dependencies',[]):
 assert sha(x['path'])==x['sha256'];deps.append(Path(x['path']))
for imp in re.findall(r'^import\s+([^\s]+)',text,re.M):
 mod=Path(*imp.split('.')).with_suffix('.olean')
 matches=[Path(d)/mod for d in paths if (Path(d)/mod).is_file()]
 assert matches,(imp,paths)
 deps.append(matches[0])
pre=[pin(p) for p in dict.fromkeys(deps)]
exe=r['command'][0];toolchain=subprocess.check_output([exe,'--version'],text=True,encoding='utf-8').strip()
assert 'version 4.31.0,' in toolchain
cmd=[exe,'-R',str(source_root),'-o',str(output),str(source)]
start=now();tick=time.perf_counter();env=dict(os.environ,LEAN_PATH=lean_path)
res=subprocess.run(cmd,cwd=source_root,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
seconds=time.perf_counter()-tick;end=now()
put(D/'STDOUT.log',res.stdout);put(D/'STDERR.log',res.stderr)
stdout=res.stdout.decode('utf-8');stderr=res.stderr.decode('utf-8');ax={}
for line in stdout.splitlines():
 if line.startswith('LOCAL_DECL\t'):
  _,decl,a=line.split('\t');ax[decl]=[x for x in a.split(',') if x]
for decl,a in re.findall(r"'(.+?)' depends on axioms: \[([^]]*)\]",stdout):ax[decl]=[x.strip() for x in a.split(',') if x.strip()]
for decl in re.findall(r"'(.+?)' does not depend on any axioms",stdout):ax[decl]=[]
for x in pre:assert sha(x['path'])==x['sha256']
accepted_olean=r.get('olean') or next((x for x in r.get('artifacts',[]) if x['path'].endswith('.olean')),None)
if accepted_olean:assert sha(accepted_olean['path'])==accepted_olean['sha256']
passed=res.returncode==0 and bool(ax) and all(set(v)<=TRIO for v in ax.values()) and 'sorryAx' not in stdout+stderr
receipt={'unit':'F1.FECHO_20261015','claim_event':845,'start_utc':start,'end_utc':end,'seconds':seconds,'command':cmd,'cwd':str(source_root),'toolchain':toolchain,'LEAN_PATH':lean_path,'exit_code':res.returncode,'passed':passed,'source':pin(source),'source_exact_copy':source.read_bytes()==original.read_bytes(),'original_receipt':pin(rp),'script':pin(__file__),'dependencies_before_after':pre,'axioms':ax,'axiom_count':len(ax),'stdout':pin(D/'STDOUT.log'),'stderr':pin(D/'STDERR.log'),'olean':pin(output) if output.exists() else None,'olean_identical_to_accepted':bool(accepted_olean and output.exists() and sha(output)==accepted_olean['sha256']),'originals_memory_production_gate_touched':False}
log=json.dumps({k:receipt[k] for k in ['start_utc','end_utc','seconds','command','cwd','toolchain','LEAN_PATH','exit_code']},ensure_ascii=False,indent=2)+'\nSTDOUT\n'+stdout+'\nSTDERR\n'+stderr
put(D/'BUILD.log',log);receipt['log']=pin(D/'BUILD.log');put(D/'RECEIPT_R1.json',json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'name':name,'passed':passed,'exit':res.returncode,'seconds':seconds,'axiom_count':len(ax),'olean_identical':receipt['olean_identical_to_accepted'],'receipt':pin(D/'RECEIPT_R1.json')},ensure_ascii=False))
sys.exit(0 if passed else 1)
