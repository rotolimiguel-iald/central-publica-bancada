import hashlib,json,pathlib,re,datetime
base=pathlib.Path(__file__).resolve().parent
attempt=base/'attempts/004'
source=base/'TheSingularityReadsTheAttractor.lean'
log=attempt/'BUILD.log'
receipt=json.loads((attempt/'RECEIPT.json').read_text(encoding='utf-8'))
assert receipt['exit_code']==0
src=source.read_bytes()
assert src== (attempt/source.name).read_bytes()
assert hashlib.sha256(src).hexdigest()==receipt['source_sha256']
text=log.read_text(encoding='utf-8')
printed=re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",text,re.S)
expected=re.findall(r'^#print axioms (\w+)',src.decode(),re.M)
assert len(printed)==len(expected)==14
allowed={'propext','Classical.choice','Quot.sound'}
for name,axioms in printed:
    assert {x.strip() for x in axioms.split(',')}<=allowed,(name,axioms)
assert not re.search(r'\b(sorry|admit|axiom)\b',src.decode())
assert 'sorryAx' not in text
paths=[source,base/'build_candidate.py',base/'finalize_lean_r1.py']
paths+=sorted((base/'attempts').glob('*/*'))
artifacts=[{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths if p.is_file()]
result={'unit':'F1.ATRATOR','author':'codex-gerente-tgl/atrator_lean','status':'PASSA_CANDIDATA_SANDBOX',
'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
'accepted_attempt':str(attempt),'build':receipt,
'printed_count':len(printed),'printed_declarations':[{'name':n,'axioms':[x.strip() for x in a.split(',')]} for n,a in printed],
'sorry_count_source':0,'sorryAx_in_accepted_log':False,'theorem_count_source':len(re.findall(r'^theorem ',src.decode(),re.M)),
'finite_hypothesis_witness':'EuclideanSpace Complex (Fin 2), e=single 0 1, lam=1/2; exact non-vacuity witness, not runtime beta',
'scope':['A1 general: Cesaro for operator norm <=1, not ordinary iterates','A1 faceFamily: ordinary iterates converge for norm(lam)<1','A2 two composition identities in complete Hilbert space, norm(T)<=1 for R T','A3 starProjection of fixed space, idempotence and exact normalized letter for D=I-T; ComplexLetter matches upstream universe Type','A4 strict contraction only on orthogonal complement of named nonzero fixed e; concludes fixedSpace=span(e), finrank1','Identity on Complex^2 has fixed-space dimension2 without the strict hypothesis','No angular limit, observed data, production install, kernel alteration or gate change'],
'failed_attempts_preserved':['001','002','003'],'warnings':'4 deprecation warnings for existing ContinuousLinearMap application aliases; no errors',
'artifacts':artifacts}
out=base/'FINAL_LEAN_RECEIPT_R1.json'
with out.open('x',encoding='utf-8',newline='\n') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps({'receipt':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'accepted_source':receipt['source_sha256'],'printed_count':len(printed),'theorem_count':result['theorem_count_source']},ensure_ascii=False))