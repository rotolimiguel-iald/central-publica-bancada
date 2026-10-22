"""Independent focal source review; verifies receipts but performs no Lean rebuild."""
from pathlib import Path
import datetime, hashlib, json, re, os
OUT=Path(__file__).resolve().parent.parent
SOURCE=OUT/'gns_coefficient_tomita'/'GENERAL_REGULAR_GENERATOR_RECEIPT_R1.json'
DEST=Path(__file__).with_name('GENERAL_REGULAR_GENERATOR_SEMANTIC_REVIEW_R1.json')
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
 if not found:raise RuntimeError('empty axiom report')
 dest=all_decl if Path(r['source']['path']).stem=='GeneralRegularGeneratorAuditR1' else prints
 for name,s in found:
  axs={a.strip() for a in s.split(',') if a.strip()}
  if axs-allowed:raise RuntimeError(name)
  dest[name]=sorted(axs)
if len(prints)!=len(j['printed_declarations']) or len(all_decl)!=j['all_local_decl_count']:raise RuntimeError('declaration mismatch')
prov=OUT/'PROVENIENCIA_V393_REUSO_V351_R1.json';v=json.loads(prov.read_text(encoding='utf8'))
if pin(Path(v['program_path']))['sha256']!=v['program_sha256']:raise RuntimeError('program changed')
if pin(Path(v['seal_path']))['sha256']!=v['seal_sha256']:raise RuntimeError('seal changed')
for item in v['sources'].values():
 if pin(Path(item['source_path']))['sha256']!=item['source_sha256']:raise RuntimeError('canonical source changed')
 if not item['normalized_source_matches_v393_embedded']:raise RuntimeError('provenance mismatch')
obj={'unit':'F1.FECHO_20261015','claim':845,'reviewer':'atrator_lean, independent of root construction','status':'PASS_WITH_STATED_SCOPE',
'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'delivery':pin(SOURCE),'source_files_read':[r['source'] for r in j['records'] if 'Audit' not in Path(r['source']['path']).name],
'additional_source_files_read':[pin(OUT/'takesaki_fock'/'RegularCovariantCoreR3.lean'),pin(OUT/'gns_coefficient_tomita'/'CoefficientBoostR1.lean')],
'pins_verified':len(seen),'printed_declarations_verified':prints,'all_local_declarations_verified':all_decl,'independent_rebuild':False,'material_findings':[],
'findings':[
'UnitaryFlow supplies actual unitary operators, strong continuity and the group law. CoefficientBoost is the measured operator field B(a), with a proved unitary inverse. No SiteProfile equivalence is assumed.',
'The positive self-adjoint generator is defined by the actual bounded spectral resolvent V sigmoid(2pi xi) V*. Both endpoint kernels vanish. Its exact graph is multiplication by exp(-2pi xi) after the same V.',
'Absorption proves V intertwines Fourier characters with the actual regular group. The imaginary powers are those of the constructed graph, then identified with that group; no modular identity is supplied as a record field.',
'Affiliation is paid by commutation with the regular generators and the existing character-multiplier calculus. The graph invariance uses the same resolvent and operator.',
'The convention C_s=exp(-is a) gives h C_s=exp(s) C_s h, equivalently Ad(C_s)h=exp(-s)h. Both graph directions and domains are proved; this is not yet a trace law.',
'The epsilon cutoff is a positive bounded member of the same core and solves (h+epsilon)y=x in both directions. Uniqueness follows from positivity, without assuming a spectral gap.',
'The three phase-balance lemmas retain endpoint damping, pairwise commutation, endpoint injectivity and phase identities explicitly. Frequency separation and CFC are used constructively; concrete GNS hypotheses remain to be consumed.'
],
'limits':['Operational baseline is v393. V351 is the historical module naming; the pinned provenance report provides the AST comparison with v393, and this review independently rechecks its source/program/seal hashes.',
'No equality with the actual dual-weight GNS modular group, semifinite trace, trace scaling, finite projection or half-splitting is concluded by this batch.',
'This is independent source/receipt/axiom verification. Existing accepted builds and their all-local audit were inspected; no additional Lean compilation was run.'],
'provenance':pin(prov),'script':pin(Path(__file__)),'production_modified':False,'gate_modified':False}
t=DEST.with_suffix('.json.tmp')
with t.open('x',encoding='utf8',newline='\n') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
json.loads(t.read_text(encoding='utf8'));os.rename(t,DEST)
print(json.dumps({'review':pin(DEST),'pins':len(seen),'prints':len(prints),'all_local':len(all_decl)},ensure_ascii=False))
