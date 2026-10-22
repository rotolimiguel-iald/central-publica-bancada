"""Independent focal source review; verifies receipts but performs no Lean rebuild."""
from pathlib import Path
import datetime, hashlib, json, re, os
OUT=Path(__file__).resolve().parent.parent
SOURCE=OUT/'gns_coefficient_tomita'/'GENERAL_CUTOFF_FORMS_RECEIPT_R1.json'
DEST=Path(__file__).with_name('GENERAL_CUTOFF_FORMS_SEMANTIC_REVIEW_R1.json')
if DEST.exists(): raise RuntimeError('immutable review already exists')
def pin(p):
 b=p.read_bytes(); return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
seen={}
def check(v):
 if isinstance(v,dict):
  if 'path' in v and 'sha256' in v:
   p=Path(v['path']); actual=pin(p)
   if actual['sha256']!=v['sha256']: raise RuntimeError('changed '+str(p))
   if 'bytes' in v and actual['bytes']!=v['bytes']: raise RuntimeError('size '+str(p))
   seen[str(p)]=actual
  for w in v.values(): check(w)
 elif isinstance(v,list):
  for w in v:check(w)
j=json.loads(SOURCE.read_text(encoding='utf8'));check(j)
allowed={'propext','Classical.choice','Quot.sound'}
prints={};all_decl={}
for r in j['records']:
 if r['exit_code']!=0:raise RuntimeError('failed record')
 b=Path(r['source']['path']).read_text(encoding='utf8')
 code=re.sub(r'/\-.*?\-/','',b,flags=re.S);code=re.sub(r'--[^\n]*','',code)
 if re.search(r'\b(sorry|admit|axiom)\b',code):raise RuntimeError('unproved source token')
 rr=json.loads(Path(r['receipt']['path']).read_text(encoding='utf8'));check(rr)
 if rr['exit_code']!=0 or not rr.get('readonly_dependencies_unchanged',True):raise RuntimeError('receipt')
 if not all(k in rr for k in ['start_utc','end_utc','seconds','LEAN_PATH','toolchain','command']):raise RuntimeError('build metadata')
 ax=Path(r['axioms']['path']).read_text(encoding='utf8')
 found=re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",ax)
 if 'Audit' in Path(r['source']['path']).stem:
  found=re.findall(r'^LOCAL_DECL\t([^\t]+)\t([^\n]*)$',ax,re.M)
 if not found:raise RuntimeError('empty axiom report')
 dest=all_decl if 'Audit' in Path(r['source']['path']).stem else prints
 for name,s in found:
  axs={a.strip() for a in s.split(',') if a.strip()}
  if axs-allowed:raise RuntimeError(name)
  dest[name]=sorted(axs)
if len(prints)!=len(j['printed_declarations']) or len(all_decl)!=j['all_local_decl_count']:raise RuntimeError('declaration mismatch')
prov=OUT/'gns_coefficient_tomita'/'GENERAL_CUTOFF_FORMS_REUSE_R1.json';v=json.loads(prov.read_text(encoding='utf8'));check(v)
obj={'unit':'F1.FECHO_20261015','claim':845,'reviewer':'atrator_lean, independent of root construction','status':'PASS_WITH_STATED_SCOPE',
'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'delivery':pin(SOURCE),'source_files_read':[r['source'] for r in j['records'] if 'Audit' not in Path(r['source']['path']).name],
'additional_source_files_read':[],
'pins_verified':len(seen),'printed_declarations_verified':prints,'all_local_declarations_verified':all_decl,'independent_rebuild':False,'material_findings':[],
"findings":[
"The cutoff CFC is transported by the actual coefficient unitary; its equality with the constructed inverse uses the exact graph and uniqueness, with no new inverse supplied as a hypothesis.",
"Positive cutoff resolvents commute and satisfy the resolvent identity. Antitonicity in epsilon uses positivity of the commuting product, not an invalid order rule for unrelated sandwiches.",
"Domain cuts q_delta=1-delta B_delta are positive contractions and converge strongly to identity using dense range of 1-R and its zero kernel. No spectral gap or operator-norm convergence is asserted.",
"Quadratic-form balance retains actual graph equations and commutation assumptions. The double-cut supremum proof uses positive contractions, strong convergence, and ENNReal suprema; it does not assume finiteness or identify unbounded products.",
"Closed-star-subalgebra CFC is transported through the actual star representation. The algebraic multiplication lemma proves an equality after the common factor; it does not cancel that factor without injectivity.",
"GNS vector injectivity follows from pointwise unitary conjugation of an injective regular operator and equality almost everywhere. It is not inferred merely from faithfulness of a representation.",
"The Fatou lemma uses only strong convergence of A_n: the relevant integrand is the squared norm of the conjugated A_n applied to a vector. Adjoint strong convergence is not assumed. The common bound may be infinite."
],
"limits":[
"The operational source is v393; V351 is historical naming of sources still embedded in that version. The six source and current-program byte hashes in the reuse report were rechecked without executing um.py.",
"These are generic required consumers, not a constructed semifinite trace or a proof of its cyclicity, scaling, or identification of the actual GNS modular group.",
"Independent focal source review plus receipt/hash/axiom verification; no new Lean reconstruction was run."
],
'provenance':pin(prov),'script':pin(Path(__file__)),'production_modified':False,'gate_modified':False}
t=DEST.with_suffix('.json.tmp')
with t.open('x',encoding='utf8',newline='\n') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
json.loads(t.read_text(encoding='utf8'));os.rename(t,DEST)
print(json.dumps({'review':pin(DEST),'pins':len(seen),'prints':len(prints),'all_local':len(all_decl)},ensure_ascii=False))
