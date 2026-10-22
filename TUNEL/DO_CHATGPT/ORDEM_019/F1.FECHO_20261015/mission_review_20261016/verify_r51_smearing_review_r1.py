from pathlib import Path
import hashlib, importlib.util, json, re
from datetime import datetime, timezone
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
REV=B/'mission_review_20261016'; MF=B/'maxwell_global'
REF=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
ACTOR={'id':'codex-mission-memory-review','kind':'agent'}
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def pin(p):
    p=Path(p); data=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
def write_new(p,obj):
    assert not p.exists(), str(p)
    data=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8'); tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f: f.write(data)
    assert tmp.stat().st_size==len(data)
    tmp.replace(p); return pin(p)

source=MF/'PointAnnihilationSmearingR4.lean'; old=MF/'PointAnnihilationSmearingR3.lean'
manifest=MF/'POINT_ANNIHILATION_SMEARING_REPAIR_R51_R4.json'
attempt=B/'orbital_rotation/attempts/20261016T205038_032609Z'
receipt=read(attempt/'RECEIPT.json'); meta=read(manifest)
assert receipt['exit_code']==0
assert receipt['readonly_dependencies_unchanged'] and receipt['dependency_cache_unchanged']
assert pin(source)['sha256']==receipt['source']['sha256']
text=source.read_text(encoding='utf-8-sig'); before=old.read_text(encoding='utf-8-sig')
def headers(s): return re.findall(r'^theorem\s+([\s\S]*?):= by',s,re.M)
assert headers(text)==headers(before)
assert re.findall(r'^import .*$',text,re.M)==re.findall(r'^import .*$',before,re.M)
axtext=(attempt/'AXIOMS.txt').read_text(encoding='utf-8-sig')
axioms=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",axtext)
printed=re.findall(r'^#print axioms (.+)$',text,re.M)
assert len(axioms)==11 and [n for n,_ in axioms]==printed
for n,v in axioms: assert {x.strip() for x in v.split(',')}=={'propext','Classical.choice','Quot.sound'}, (n,v)
assert not re.search(r'\b(sorry|admit)\b',text)
assert not re.search(r'^\s*(axiom|unsafe)\b',text,re.M)
checked={}; measured={}
def walk(o):
    if isinstance(o,dict):
        if isinstance(o.get('path'),str) and isinstance(o.get('sha256'),str):
            key=(o['path'],o['sha256'])
            if key not in checked:
                if o['path'] not in measured: measured[o['path']]=pin(o['path'])
                actual=measured[o['path']]
                assert actual['sha256']==o['sha256'], (actual,o)
                if 'bytes' in o: assert actual['bytes']==o['bytes']
                checked[key]=actual
        for v in o.values(): walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
walk(receipt);walk(meta);walk(read(attempt/'DEPENDENCY_CACHE.json'))
vp=write_new(REV/'R51_SMEARING_PIN_VERIFICATION_R1.json',{
    'schema':'iald-independent-pin-verification/v1','actor':ACTOR,'ok':True,
    'verified_unique_path_hash_pairs':len(checked),'pins':list(checked.values()),
    'scope':'Recibo R4, manifesto R4 e dependency_cache; bytes medidos, nenhuma compilação.'})
spec=importlib.util.spec_from_file_location('r51_smearing_final',B/'mission_resume_20261016/live_mission_r39.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);assert Path(m.REFERENCE)==REF
r,sp=m.call('mission_cli.py',{'operation':'project','reference':str(REF),'actor':ACTOR,'max_chars':100000},'R51_SMEARING_REVIEW_FINAL')
q=r['projection']
review={
    'schema':'iald-independent-component-review/v1','created_utc':datetime.now(timezone.utc).isoformat(),
    'reviewer':ACTOR,'author':meta['author'],'verdict':'PASS_COMPONENT_WITH_SCOPE',
    'requirement':'R8','requirement_satisfied':False,'blocking_findings':[],
    'mission_reference':pin(REF),'final_sync':pin(sp),'revision':q['revision'],'state_sha256':q['state_sha256'],
    'source':pin(source),'manifest':pin(manifest),'receipt':pin(attempt/'RECEIPT.json'),
    'axioms':pin(attempt/'AXIOMS.txt'),'exit_code':0,'seconds':receipt['seconds'],
    'source_matches_attempt':True,'public_theorem_headers_identical':True,
    'public_theorem_header_count':len(headers(text)),
    'public_axiom_reports':[{'declaration':n,'axioms':[x.strip() for x in v.split(',')]} for n,v in axioms],
    'readonly_dependencies_unchanged_reported':True,'dependency_cache_unchanged_reported':True,
    'pin_verification':vp,
    'prior_reviews_by_reference':[pin(REV/'R51_POINT_WICK_REVIEW_R1.json'),pin(REV/'R51_POINT_WICK_REVIEW_R2.json')],
    'findings':[
        {'lines':[39,51],'finding':'Expansão no domínio regular preservada: congrArg da soma e do subtipo, map_smul explícito. Nenhuma mudança de domínio ou enunciado.'},
        {'lines':[53,86],'finding':'Integral de Bochner com valores no Fock ambiente para cada ψ regular fixo. Soma finita de vetores exponenciais fixos vezes coeficientes integráveis fornece integrabilidade; integral_finsetSum recebe essas provas.'},
        {'lines':[88,109],'finding':'Auxiliar privado usa profileWave_pairing_integrable na medida produto e integral_prod_left. A igualdade integral é reassociada por integral_const_mul. RegularLabel fornece RegularProfile; o teorema público não acrescenta premissa.'},
        {'lines':[111,157],'finding':'Teste Schwartz conjugado, sinais métricos, amplitude Fourier e fator 1/2 preservados. pointTestEigenvalue_integrable e pointAnnihilation_test_integrable descarregam a hipótese analítica genérica.'},
        {'lines':[159,184],'finding':'Conclusão é a annihilation já existente aplicada a normalizedPhysicalSmearCLM f e regularDomainInput ψ, igual à integral literal do pointAnnihilation na mesma ψ. A igualdade prévia de eigenvalues com inner fixa o mesmo H1/Fock.'}
    ],
    'A_consumer':{
        'smearing_requires_A':False,
        'calibrated_certificate_still_requires_A':True,
        'source':pin(MF/'LocalWickStressIdentificationR3.lean'), 'lines':[147,153],
        'statement':'localWickStress_eq_calibrated mantém A : RemainingModularCoreInput D. Este componente de smearing não constrói nem elimina A.'},
    'scope_limits':[
        'Identidade para testes Schwartz e vetores no domínio regular; não afirma operador pontual limitado no Fock inteiro, operador de criação pontual ou integral em norma de operadores.',
        'A dependência analítica de integrabilidade é fornecida por regularidade e somas finitas no próprio desenvolvimento; não foi assumida como nova hipótese física final.',
        'Pareceres anteriores usados por remissão, fontes e falhas históricas preservadas. Não revisa split ou montagem final de certificado.',
        'R8 integral aberto; nenhuma aceitação de requisito, fechamento de quadro, alteração de gate ou confirmação física.'
    ],
    'low_findings':[{'line':57,'warning':'MeasureTheory.integrable_finset_sum depreciado; substituto integrable_finsetSum. Baixo, sem bloqueio e sem rodada cosmética.'}],
    'historical_failure':{'source':pin(old),'receipt':pin(B/'orbital_rotation/attempts/20261016T204650_618420Z/RECEIPT.json')},
    'new_builds':0,'provider_calls':0,'production_modified':False,'mission_mutations':False,
    'script':pin(Path(__file__))
}
rp=write_new(REV/'R51_SMEARING_REVIEW_R1.json',review)
print(json.dumps({'ok':True,'revision':q['revision'],'verified_pin_pairs':len(checked),'report':rp,'source':pin(source),'axiom_reports':len(axioms),'public_headers':len(headers(text))},ensure_ascii=False))
