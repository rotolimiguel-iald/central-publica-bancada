"""Independent review build: source copy and exact scope probes, no canonical writes."""
from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,time
BASE=Path(__file__).resolve().parent
DELIVERY=BASE.parent/'quadratic_rule/DELIVERY_R1.json'
LEAN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
D=json.loads(DELIVERY.read_text(encoding='utf-8'))
RECEIPT=json.loads(Path(D['build']['path']).read_text(encoding='utf-8'))
OUT=BASE/'build_r1';OUT.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p),'bytes':Path(p).stat().st_size}
def put(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
 assert p.read_bytes()==b

def putj(p,o):put(p,(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
pins=[D['build']]+D['dependencies']+D['artifacts']
for p in pins:assert sha(p['path'])==p['sha256'],p['path']
source=BASE.parent/'quadratic_rule/RuleQuadraticResidual.lean'
local=OUT/'src/TGLExt/RuleQuadraticResidual.lean'
put(local,source.read_bytes())
assert local.read_bytes()==Path(RECEIPT['source']['path']).read_bytes()
assert not re.search(r'\bsorry\b|\badmit\b|^\s*axiom\s',local.read_text(encoding='utf-8'),re.M)
probe='import TGLExt.RuleQuadraticResidual\nopen Matrix Complex\nopen TGLExt TGLExt.TimeGravitonMatrix TGLExt.TimeGravitonFlow\nopen TGLExt.RuleQuadraticResidual\nnamespace QuadraticIndependentReview\nnoncomputable section\n\ntheorem impossible_hypothesis_is_inhabited : ∃ A : M2, Eg A ≠ A := by\n  refine ⟨rootPlus, ?_⟩\n  rw [Eg_rootPlus]\n  exact Ne.symm concrete_nonzero_modes.1\n\ntheorem impossible_control (X : M2) : 0 < residual rootPlus X := by\n  apply impossible_anchor_positive\n  rw [Eg_rootPlus]\n  exact Ne.symm concrete_nonzero_modes.1\n\ntheorem accepted_does_not_identify_raw_state :\n    residual anchor transportedRho = 0 ∧ transportedRho ≠ anchor :=\n  ⟨transported_accepted, transported_is_not_anchor⟩\n\ntheorem pinching_differs_from_one_polarization :\n    Eg (1 : M2) ≠ projPlus * (1 : M2) * projPlus := by\n  intro h\n  have hc := congrArg (fun X : M2 => X 0 0) h\n  norm_num [Eg, projPlus, projMinus, genK, Matrix.mul_apply, Fin.sum_univ_two,\n    Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, Matrix.one_apply] at hc\n\n#print axioms impossible_hypothesis_is_inhabited\n#print axioms impossible_control\n#print axioms accepted_does_not_identify_raw_state\n#print axioms pinching_differs_from_one_polarization\nend\nend QuadraticIndependentReview\n'
probepath=OUT/'src/QuadraticIndependentReview.lean';put(probepath,probe.encode('utf-8'))
lib=OUT/'lib';lib.mkdir()
lean_path=str(lib)+';'+RECEIPT['LEAN_PATH']
assert all(Path(s).is_dir() for s in lean_path.split(';'))
env=dict(os.environ,LEAN_PATH=lean_path)
version=subprocess.check_output([str(LEAN),'--version'],text=True).strip();assert '4.31.0' in version
results=[]
for src,target in [(local,lib/'TGLExt/RuleQuadraticResidual.olean'),(probepath,lib/'QuadraticIndependentReview.olean')]:
 target.parent.mkdir(exist_ok=True,parents=True)
 cmd=[str(LEAN),'-R',str(OUT/'src'),'-o',str(target),str(src)]
 start=now();t=time.perf_counter();run=subprocess.run(cmd,cwd=OUT/'src',env=env,capture_output=True)
 sec=time.perf_counter()-t;end=now();text=(run.stdout+run.stderr).decode('utf-8','replace')
 log=OUT/(src.stem+'_BUILD.log')
 header={'command':cmd,'toolchain':version,'LEAN_PATH':lean_path,'start_utc':start,'end_utc':end,'seconds':sec,'exit_code':run.returncode}
 put(log,json.dumps(header,ensure_ascii=False,indent=2).encode()+b'\nSTDOUT\n'+run.stdout+b'\nSTDERR\n'+run.stderr)
 axioms={name:[x.strip() for x in axi.split(',') if x.strip()] for name,axi in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",text)}
 expected=re.findall(r'^#print axioms (\S+)',src.read_text(encoding='utf-8'),re.M)
 passed=run.returncode==0 and len(axioms)==len(expected) and all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in axioms.values()) and 'sorryAx' not in text
 rec={**header,'source':pin(src),'log':pin(log),'olean':pin(target) if target.exists() else None,'axioms':axioms,'axiom_count':len(axioms),'passed':passed}
 if src==local:
  rec['olean_byte_identical_to_original']=target.exists() and target.read_bytes()==Path(RECEIPT['olean']['path']).read_bytes()
 putj(OUT/(src.stem+'_RECEIPT.json'),rec);results.append(rec)
 print(json.dumps({'source':src.name,'exit':run.returncode,'seconds':sec,'axioms':len(axioms),'passed':passed}),flush=True)
 if not passed:print(text);break
for p in pins:assert sha(p['path'])==p['sha256']
putj(BASE/'BUILD_REVIEW_R1.json',{'created_utc':now(),'status':'PASSA' if len(results)==2 and all(x['passed'] for x in results) else 'FALHA_BUILD','script':pin(__file__),'delivery':pin(DELIVERY),'checked_pins':pins,'source_unchanged':sha(source)==sha(local),'builds':results})
