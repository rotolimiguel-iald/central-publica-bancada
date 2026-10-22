"""Pin the accepted finite-Weyl KMS construction; refuse incomplete evidence."""
from pathlib import Path
import datetime, hashlib, json, re
BASE=Path(__file__).resolve().parent
NAMES=['CanonicalKMSDomainsR4','WeylVacuumCoefficientR2','KMSFiniteSpanR3',
       'WeylStripFromCoefficientR3','CanonicalWeylKMSFiniteR2','KMSFiniteAuditR2']
def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
items=[]
for name in NAMES:
    src=BASE/(name+'.lean');raw=src.read_bytes()
    assert not re.search(rb'\b(sorry|admit|axiom)\b',raw)
    matches=[]
    for rp in (BASE/'attempts').glob('*/RECEIPT.json'):
        sp=rp.parent/src.name
        if sp.exists() and sp.read_bytes()==raw:
            r=json.loads(rp.read_bytes())
            if r['exit_code']==0: matches.append((rp,r))
    assert matches, name
    rp,r=sorted(matches,key=lambda x:str(x[0]))[-1]
    for a in r['artifacts']: assert pin(Path(a['path']))==a
    assert r['readonly_dependencies_unchanged']
    txt=(rp.parent/'AXIOMS.txt').read_text(encoding='utf-8')
    assert 'sorryAx' not in txt
    local=re.findall(r'^LOCAL_DECL\t([^\t\n]+)\t([^\n]*)$',txt,re.M)
    prints=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",txt,re.S)
    assert local or prints
    for _,axioms in local+prints:
        assert set(x.strip() for x in axioms.split(',') if x.strip()) <= {'propext','Classical.choice','Quot.sound'}
    items.append({'module':name,'source':pin(src),'receipt':pin(rp),
        'exit_code':r['exit_code'],'seconds':r['seconds'],'axiom_prints':len(prints),
        'local_declarations':len(local),'artifacts':r['artifacts']})
audit=items[-1]
assert audit['local_declarations']>0
failed=[]
prefixes=['CanonicalKMSDomains','WeylVacuumCoefficient','KMSFiniteSpan',
          'WeylStripFromCoefficient','CanonicalWeylKMSFinite']
for rp in sorted((BASE/'attempts').glob('*/RECEIPT.json')):
    r=json.loads(rp.read_bytes());src=Path(r['source']['path'])
    if r['exit_code'] and any(src.stem.startswith(p) for p in prefixes):
        failed.append({'receipt':pin(rp),'source':pin(src),'artifacts':r['artifacts']})
result={
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'unit':'F1.FECHO_20261015','claim':845,'author':'codex-atrator-skeptic',
 'status':'COMPILED_CANDIDATE_AWAITING_INDEPENDENT_REVIEW',
 'accepted':items,'failed_attempts_preserved':failed,
 'all_local_count':audit['local_declarations'],
 'axioms':['propext','Classical.choice','Quot.sound'],'zero_sorry':True,
 'scope':[
  'Actual canonical half-modular domains of algebra-vacuum and adjoint-vacuum vectors follow from the proved Tomita graph.',
  'Actual W(f)=D(i f) on the same canonical Fock gives the exact vacuum coefficient exp(-norm(f)^2/2-norm(g)^2/2-inner(f,u(g))).',
  'The proved one-particle wedge strip supplies the analytic continuation; the concrete generator output has no KMS or analyticity hypothesis.',
  'Complex bilinearity extends the KMS pair to the finite complex span of the actual Weyl generators.',
  'The physical KMS flow is Gamma(B0(+2*pi*t)); the modular flow has the opposite parameter sign.',
  'The full von Neumann closure is a separate parent construction. No physical realization, empirical validation, deployment or gate change is claimed.'
 ],'production_modified':False,'gate_changed':False,
 'builder':pin(BASE/'build_strip_r1.py'),'assembler':pin(Path(__file__)),
 'root_closure_source_review':pin(BASE/'review_closure/REVISAO_FECHO_KMS_R1.json')}
def save(p,b):
    if isinstance(b,str):b=b.encode('utf-8')
    with p.open('xb') as f:f.write(b)
    assert p.read_bytes()==b
save(BASE/'FINAL_WEYL_KMS_FINITE_RECEIPT_R1.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
save(BASE/'ENTREGA_WEYL_KMS_FINITE_R1.md',
 '# Faixa KMS concreta dos Weyl e da álgebra finita\n\n'
 '[REAL — compilação Lean em sandbox] As cinco candidatas compilam, com axiomas restritos ao trio e sem sorry. '
 f'O auditor de ambiente verificou {audit["local_declarations"]} declarações locais, incluindo auxiliares.\n\n'
 'O coeficiente usa W(f)=D(if), sem reescala por √2. A faixa superior tem fluxo Γ(B0(+2πt)); o fluxo modular usa o sinal oposto. '
 'O consumidor concreto fornece a continuação pelos lemas da cunha, sem hipótese adicional de analiticidade ou KMS. '
 'A extensão por linearidade alcança a álgebra finita dos Weyl. O fecho de von Neumann é construção separada da raiz.\n\n'
 'Candidatas aguardam revisão independente. Todas as tentativas recusadas permanecem pinadas no recibo JSON. '
 'A revisão dos cinco lemas genéricos de fecho da raiz foi somente semântica com conferência dos builds existentes, sem recompilação independente. '
 'Nada canônico foi alterado e nada move o gate.\n')
print(json.dumps(pin(BASE/'FINAL_WEYL_KMS_FINITE_RECEIPT_R1.json')))
