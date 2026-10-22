"""Seal a single independent material review of the geometric identification."""
from pathlib import Path
import json, hashlib, datetime as dt, os
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
RUN=BASE/'20261013T221947_732334Z'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return {'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
def save(p,b):
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert p.read_bytes()==b
def jsave(p,x): save(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
manifest=ROOT/'geometric_identification/RESULTADO_GEOMETRIC_R1.json'
assert sha(manifest)=='a11eccfee6020e4f15bfe816a9ce0e6fe8ac02ea7c32ca1193fb1bd177a32e1f'
queue=[manifest]; seen=set(); checks={}
def walk(x):
    if isinstance(x,dict):
        if 'path' in x and 'sha256' in x:
            p=Path(x['path']); actual=pin(p)
            assert actual['sha256']==x['sha256'],str(p)
            if 'bytes' in x: assert actual['bytes']==x['bytes'],str(p)
            checks[(str(p),x['sha256'])]=actual
            if p.suffix.lower()=='.json': queue.append(p)
        for v in x.values(): walk(v)
    elif isinstance(x,list):
        for v in x: walk(v)
while queue:
    p=queue.pop()
    if str(p) not in seen:
        seen.add(str(p)); walk(json.loads(p.read_text(encoding='utf-8-sig')))
receipt=json.loads((RUN/'RECOMPILE_RECEIPT.json').read_text())
assert len(receipt['builds'])==3 and all(x['exit_code']==0 for x in receipt['builds'])
assert len(receipt['declarations'])==22
comparisons=[]
for module,stamp in [('FourierConjugation','20261013T221637_926790Z'),('GeometricIdentification','20261013T221808_560069Z')]:
    old=ROOT/f'geometric_identification/attempts/{stamp}/{module}.olean'; new=RUN/(module+'.olean')
    comparisons.append({'module':module,'original':pin(old),'rebuilt':pin(new),'byte_identical':old.read_bytes()==new.read_bytes()})
report='''# Revisão independente — identificação geométrica de J

PASSA no escopo declarado, sem achado material. Foram lidos integralmente FourierConjugation.lean e GeometricIdentification.lean, e recompiladas cópias dos dois, seguidas pela impressão das 22 declarações. As dependências são as da revisão modular anterior, somente em leitura; não se usaram os .olean novos do construtor.

productJ é definido por reflexão transversal da medida produto, conjugação e troca das duas componentes, sem usar Jcandidate. A igualdade não entra como hipótese: deriva da identidade de Fourier para funções integráveis, da passagem pelo espaço de Schwartz e extensão por densidade em L², depois da fórmula de Fubini das seções. A fórmula quase em toda parte preserva r, envia q a −q e conjuga/troca a fibra. Jcandidate_eq_geometricJ iguala os operadores no H1 canônico.

As três compilações terminaram com exit 0; as 22 declarações usam só propext, Classical.choice e Quot.sound; zero sorry. O JSON contém pinos conferidos, tempos, recibo e comparação binária dos dois .olean. Logs individuais registram comando, toolchain, LEAN_PATH, início e fim.

Isto identifica a fórmula do operador na carta de rapidez. A covariância de Poincaré completa, a localização de todas as cunhas e a rede quadridimensional não são inferidas. Nada foi instalado em produção, nem alterado no kernel, nas memórias, no quadro ou no gate. A revisão técnica não substitui o aceite da c1.
'''
save(BASE/'REVIEW_GEOMETRIC_R1.md',report.encode())
result={'unit':'F1.REDE','status':'PASS_FORMAL_SCOPE__NO_MATERIAL_FINDING','reviewer':'codex-independent-modular-review','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'reviewed_target':'Jcandidate_eq_geometricJ and Jcandidate_rapidity_coordinates','independent_productJ_definition':True,'target_equality_not_assumed':True,'no_new_existence_hypotheses':True,'q_reflected':True,'rapidity_unchanged':True,'fiber_conjugated_and_swapped':True,'compile_count':3,'declaration_count':22,'only_trio':True,'zero_sorry':True,'compile_seconds':sum(x['seconds'] for x in receipt['builds']),'checked_pin_count':len(checks),'pins':list(checks.values()),'olean_comparison':comparisons,'evidence':[pin(manifest),pin(RUN/'RECOMPILE_RECEIPT.json'),pin(BASE/'review_build_r1.py'),pin(BASE/'finish_review_r1.py'),pin(BASE/'REVIEW_GEOMETRIC_R1.md')],'limitations':['Coordinate formula is exact; full Poincare covariance and complete four-dimensional local net remain outside this result.'],'production_writes':False}
jsave(BASE/'REVIEW_GEOMETRIC_R1.json',result)
print(json.dumps({'path':str(BASE/'REVIEW_GEOMETRIC_R1.json'),'sha256':sha(BASE/'REVIEW_GEOMETRIC_R1.json'),'pins':len(checks),'seconds':result['compile_seconds'],'olean_identical':sum(x['byte_identical'] for x in comparisons)}))
