from pathlib import Path
import json,hashlib,re,datetime
U=Path(__file__).resolve().parents[1]
B=U/'gns_coefficient_tomita'
TRIO={'propext','Classical.choice','Quot.sound'}
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
pins={}
def verify_tree(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str):
   got=pin(x['path']);assert got['sha256']==x['sha256'],x['path'];pins[got['path']]=got
  for v in x.values():verify_tree(v)
 elif isinstance(x,list):
  for v in x:verify_tree(v)
a=B/'COEFFICIENT_TOMITA_RECEIPT_R1.json';d=read(a);verify_tree(d)
records=[r for r in d['records'] if Path(r['source']['path']).name!='CoefficientTomitaAuditR1.lean']
extras=['RealTomitaGraphR3','LpPairTransportR3','RealTomitaGraphDenseR1','CoefficientGraphCoreR3','ClosedGraphRegularizationR3']
for name in extras:
 source=B/(name+'.lean');sh=pin(source)['sha256'];candidates=[]
 for rpath in (B/'attempts').glob('*/RECEIPT.json'):
  if not (rpath.parent/(name+'.lean')).is_file():continue
  rr=read(rpath)
  if type(rr.get('exit_code')) is int and rr['exit_code']==0 and pin(rpath.parent/(name+'.lean'))['sha256']==sh:candidates.append((rpath,rr))
 assert candidates,name
 rp,rr=sorted(candidates,key=lambda x:str(x[0]))[-1]
 records.append({'source':pin(source),'receipt':pin(rp),'axioms':pin(rp.parent/'AXIOMS.txt'),'build':pin(rp.parent/'BUILD.log'),'olean':pin(rp.parent/(name+'.olean'))})
prints={};per_source=[]
for r in records:
 verify_tree(r);rr=read(r['receipt']['path']);assert type(rr['exit_code']) is int and rr['exit_code']==0
 assert rr['readonly_dependencies_unchanged'] is True
 verify_tree(rr)
 src=Path(r['source']['path']).read_text(encoding='utf-8');assert not re.search(r'\b(?:sorry|admit|axiom)\b',src)
 ax=Path(r['axioms']['path']).read_text(encoding='utf-8')
 parsed={n:[z.strip() for z in a.split(',') if z.strip()] for n,a in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",ax,re.S)}
 assert parsed, r['source']['path'];assert all(set(v)<=TRIO for v in parsed.values())
 for n,v in parsed.items():
  if n in prints:assert set(prints[n])==set(v)
  prints[n]=v
 per_source.append({'source':r['source'],'receipt':r['receipt'],'exit_code':rr['exit_code'],'start_utc':rr['start_utc'],'end_utc':rr['end_utc'],'seconds':rr['seconds'],'printed_declarations':list(parsed),'no_sorry':True})
claims=[
 'Fibre resolvent calculus constructs the lifted positive self-adjoint root and its square graph; the spectral flow equality is derived by CFC and dense damping.',
 'The coefficient conjugation is the concrete L2 antiunitary combining base conjugation, reflection and pointwise boost; involution uses the proved commutation with the boost.',
 'The coefficient Tomita square is obtained with the maximal adjoint and the exact graph, not just a formal adjoint relation.',
 'Pointwise root membership is an equivalence almost everywhere with both vectors in L2; no domain integrability obligation is discarded.',
 'The concrete Fock domain is coefficient_graph_ae: (f(-a),B_-a g(a)) belongs to the actual closed base Weyl-vacuum adjunction graph almost everywhere.',
 'RealTomitaGraph is a real Hilbert subspace; no antilinear graph is asserted to be complex linear.',
 'Interval density uses orthogonal projection and the actual dense base graph closure. LpPairTransport decode/encode has the required inverse identity.',
 'coefficient_mem_of_dense_intervals has explicit interval-generator hypotheses for the target closed real graph. These still must be discharged for the actual GNS graph.',
 'Bochner preservation uses real scalar kernels, strong continuity and closedness. The equality criterion additionally requires concrete regularizer range and strong convergence; involution alone is not used as a converse inclusion.'
]
out={'unit':'F1.FECHO_20261015','claim':845,'reviewer':'codex-gerente-tgl/tempo_math_review','reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'PASS_WITH_STATED_SCOPE','review_type':'independent_semantic_source_and_record_review','independent_rebuild_performed':False,'aggregate_source':pin(a),'source_count':len(records),'verified_pin_count':len(pins),'printed_declaration_count':len(prints),'printed_axioms_only_trio':True,'sources':per_source,'semantic_findings':claims,'material_defects':[],'scope_limits':['No coefficient-to-GNS surjectivity or equality of the GNS Tomita with the coefficient Tomita is assumed or discharged by this reviewed lot.','No scaled trace on the represented Fock core or complete certificate inhabitant is claimed.','Generic regularization criterion does not construct the Gaussian/CFC bridge.'],'verified_pins':list(pins.values()),'review_script':pin(__file__),'production_modified':False,'gate_modified':False}
target=U/'network_review'/'COEFFICIENT_TOMITA_SEMANTIC_REVIEW_R1.json'
with target.open('x',encoding='utf-8',newline='\n') as f:json.dump(out,f,ensure_ascii=False,indent=2)
print(json.dumps({'review':pin(target),'sources':len(records),'pins':len(pins),'prints':len(prints),'verdict':out['verdict']},ensure_ascii=False))
