"""Seal this review only after all independent module builds succeeded."""
from pathlib import Path
import hashlib, json, re, datetime as dt, os
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
RUN=BASE/'20261013T215402_817152Z'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return {'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
def save(p,b):
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert p.read_bytes()==b
receipt=json.loads((RUN/'RECOMPILE_RECEIPT.json').read_text())
assert len(receipt['builds'])==9 and all(x['exit_code']==0 for x in receipt['builds'])
original=json.loads((ROOT/'modular_wedge/RESULTADO_MODULAR_R1.json').read_text())
pin_result=json.loads((BASE/'PIN_VERIFICATION_R1.json').read_text())
assert not pin_result['errors']
for pinned in pin_result['pins']:
    assert sha(Path(pinned['path']))==pinned['expected_sha256'], pinned['path']
names=json.loads((ROOT/'modular_wedge/LOCAL_DECLARATIONS.json').read_text())['names']
audit=(RUN/'AuditAll.log').read_text(encoding='utf-8')
for n in names:
    assert "'"+n+"'" in audit, n
assert len(names)==75 and 'sorryAx' not in audit
comparisons=[]
for mod in original['modules']:
    old=Path(mod['source']['path']).with_suffix('.olean')
    new=RUN/(mod['module']+'.olean')
    comparisons.append({'module':mod['module'],'original':pin(old),'rebuilt':pin(new),'byte_identical':old.read_bytes()==new.read_bytes()})
checks=[
 {'id':'M1','status':'PASS','claim':'spectralOutput is a closed term of AuditF13v31.D1a3OutputBGL on canonical H1; no new existence assumptions.','source':'CanonicalOutput.lean:spectralOutput'},
 {'id':'M2','status':'PASS','claim':'TW is positive and self-adjoint; maximal graph multiplication by exp(2*pi^2*xi), not a restricted core.','source':'CanonicalWedge.lean:TW_multiplier,TW_positive,TW_selfadjoint; VectorWedge.lean:T_graph'},
 {'id':'M3','status':'PASS','claim':'Full graph equivalence Delta=S-adjoint S, including both composition domains; the existing generic adjoint is maximal for self-adjoint T.','source':'CanonicalOutput.lean:delta_is_SdagS; VectorSquare.lean:T_double_graph_iff; GenericAntilinearAdjoint.lean:generic_adjoint_maximal'},
 {'id':'M4','status':'PASS','claim':'S is a closed densely defined involution; Fix(S) is StandardSubspace H1 and contains a nonzero vector.','source':'CanonicalWedge.lean:SW_closed,SW_maps,SW_involutive; CanonicalOutput.lean:spectralOutput_nonzero'},
 {'id':'M5','status':'PASS','claim':'The concrete canonical Fubini and partial Fourier intertwiner preserve the original H1 and B0; no arbitrary Hilbert-space replacement.','source':'FubiniL2.lean:canonicalFub,canonical_modularGroupIsBoost'},
 {'id':'M6','status':'PASS','claim':'Jcandidate uses spectral and transverse reflections, complex conjugation and fiber exchange; involutivity is proved.','source':'CanonicalWedge.lean:Jcandidate; GeometricFiberConjugation.lean:transverseGeometricJ_coordinates'},
 {'id':'M7','status':'PASS','claim':'Nine independently rebuilt modules exit zero; all 75 listed modular declarations have axioms within the trio; source has no sorry/admit/new axiom.'}
]
limitations=[
 'The proved ModularGroupIsBoost is the explicit multiplicative phase identity after Fourier. No generic Mathlib imaginary-power functional-calculus API is asserted.',
 'Geometric wedge covariance, all-direction localization and complete four-dimensional LightNetData are not delivered by these modules.',
 'No FockCertificate/MaxwellCertificate inhabitant, device-to-continuum equivalence or derivation of H3 is inferred.',
 'Independent technical review is not c1 acceptance or operator integration authorization.'
]
report='''# Revisão independente da construção modular F1.REDE

Veredito: PASSA no escopo formal declarado, sem achado material. A revisão leu os cinco módulos novos e as definições do contrato e do adjunto genérico. Foram recompiladas cópias de nove módulos, incluindo Fubini e as duas conjugações de fibra, em diretório novo, sem usar os .olean locais do construtor. O cache do Nós aparece apenas como dependência de leitura.

O habitante spectralOutput é concreto no H1 canônico. TW tem grafo maximal, é positivo e auto-adjunto. A prova Delta=S†S contempla o grafo inteiro e os domínios da composição. S é involução fechada densa; K=Fix(S) é padrão e não nulo. A igualdade com o boost é expressa pelo multiplicador de Fourier do contrato. Não há hipótese adicional de existência escondida no habitante.

Os 169 pinos transitivos conferem. As 75 declarações modulares foram impressas novamente e usam somente propext, Classical.choice e Quot.sound. As nove recompilações terminaram com exit 0. Início, fim, tempo, comando e LEAN_PATH literal constam dos logs e do recibo. A comparação binária dos cinco .olean consta no JSON, sem inferir igualdade a partir do sucesso de compilação.

A identificação física da cunha, a covariância completa de Poincaré, a rede em quatro dimensões, Fock/Maxwell e a equivalência com o dispositivo permanecem fora desta entrega. A fase e^{itσ} é o cálculo multiplicativo explícito: não se declara uso de uma API genérica de potência imaginária para operadores ilimitados. Nenhum kernel, original, produção, memória, quadro ou gate foi alterado por esta revisão.
'''
save(BASE/'REVIEW_MODULAR_R1.md',report.encode())
result={'unit':'F1.REDE','status':'PASS_FORMAL_SCOPE__NO_MATERIAL_FINDING','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'reviewer':'codex-independent-modular-review','checks':checks,'limitations':limitations,'checked_pins':pin_result['checked_pin_count'],'rebuilt_modules':len(receipt['builds']),'audited_modular_declarations':len(names),'total_compile_seconds':sum(x['seconds'] for x in receipt['builds']),'olean_comparison':comparisons,'evidence':[pin(ROOT/'modular_wedge/RESULTADO_MODULAR_R1.json'),pin(BASE/'PIN_VERIFICATION_R1.json'),pin(RUN/'RECOMPILE_RECEIPT.json'),pin(BASE/'review_build_r1.py'),pin(BASE/'verify_pins_r1.py'),pin(BASE/'finish_review_r1.py'),pin(BASE/'REVIEW_MODULAR_R1.md')],'production_writes':False}
save(BASE/'REVIEW_MODULAR_R1.json',(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'path':str(BASE/'REVIEW_MODULAR_R1.json'),'sha256':sha(BASE/'REVIEW_MODULAR_R1.json'),'seconds':result['total_compile_seconds'],'olean_identical':sum(x['byte_identical'] for x in comparisons)},ensure_ascii=False))
