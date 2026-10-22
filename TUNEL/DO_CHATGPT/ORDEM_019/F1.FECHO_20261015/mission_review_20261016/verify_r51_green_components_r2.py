from pathlib import Path
import hashlib, importlib.util, json, re
from datetime import datetime, timezone

B = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
REV = B / 'mission_review_20261016'
REF = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
ACTOR = {'id': 'codex-mission-memory-review', 'kind': 'agent'}
def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def pin(p):
    p = Path(p); data = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
def save_new(p, obj):
    assert not p.exists(), f'Preserve existing artifact: {p}'
    data = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    tmp = p.with_name(p.name + '.tmp')
    with tmp.open('xb') as f: f.write(data)
    assert tmp.stat().st_size == len(data)
    tmp.replace(p)
    return pin(p)

spec = importlib.util.spec_from_file_location('r51_review_final_sync', B/'mission_resume_20261016/live_mission_r39.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
assert Path(m.REFERENCE) == REF
result, sync_path = m.call('mission_cli.py', {
    'operation': 'project', 'reference': str(REF), 'actor': ACTOR, 'max_chars': 100000
}, 'R51_GREEN_COMPONENTS_REVIEW_FINAL')
proj = result['projection']

items = [
    ('FiniteProjectionR3', 'takesaki_fock/CanonicalFockFiniteProjectionR3.lean', '20261016T204544_576190Z', 5,
     'takesaki_fock/CANONICAL_FOCK_FINITE_PROJECTION_CANDIDATE_R3.json'),
    ('MatrixCornerR2', 'takesaki_fock/CanonicalFockMatrixCornerR2.lean', '20261016T204338_618085Z', 5,
     'takesaki_fock/CANONICAL_FOCK_MATRIX_CORNER_CANDIDATE_R2.json'),
    ('LocalWickStressIdentificationR3', 'maxwell_global/LocalWickStressIdentificationR3.lean', '20261016T204422_618535Z', 8,
     'maxwell_global/LOCAL_WICK_IDENTIFICATION_REPAIR_R51_R3.json'),
]
checks = {}; measured = {}; components = {}
def walk(o):
    if isinstance(o, dict):
        if isinstance(o.get('path'), str) and isinstance(o.get('sha256'), str):
            key = (o['path'], o['sha256'])
            if key not in checks:
                actual = measured.setdefault(o['path'], pin(o['path']))
                assert actual['sha256'] == o['sha256'], (o, actual)
                if 'bytes' in o: assert actual['bytes'] == o['bytes'], (o, actual)
                checks[key] = actual
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)

for name, rel, attempt, expected, manifest in items:
    source = B/rel; a = B/'orbital_rotation/attempts'/attempt
    receipt = read(a/'RECEIPT.json')
    assert receipt['exit_code'] == 0
    assert receipt['readonly_dependencies_unchanged'] is True
    assert receipt['dependency_cache_unchanged'] is True
    assert pin(source)['sha256'] == receipt['source']['sha256']
    walk(receipt); walk(read(B/manifest)); walk(read(a/'DEPENDENCY_CACHE.json'))
    source_text = source.read_text(encoding='utf-8-sig')
    ax_text = (a/'AXIOMS.txt').read_text(encoding='utf-8-sig')
    axioms = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", ax_text)
    assert len(axioms) == expected, (name, len(axioms))
    assert len(re.findall(r'^#print axioms ', source_text, re.M)) == expected
    assert len({n for n, _ in axioms}) == expected
    for n, values in axioms:
        assert {x.strip() for x in values.split(',')} == {'propext','Classical.choice','Quot.sound'}, (n, values)
    assert not re.search(r'\b(sorry|admit)\b', source_text)
    assert not re.search(r'^\s*(axiom|unsafe)\b', source_text, re.M)
    components[name] = {
        'source': pin(source), 'manifest': pin(B/manifest), 'attempt': str(a),
        'receipt': pin(a/'RECEIPT.json'), 'axioms': pin(a/'AXIOMS.txt'),
        'exit_code': receipt['exit_code'], 'seconds': receipt['seconds'],
        'public_axiom_reports': [{'declaration': n, 'axioms': [x.strip() for x in v.split(',')]} for n,v in axioms],
        'source_equals_attempt': True, 'receipt_and_cache_pins_verified': True,
        'readonly_dependencies_unchanged_reported': receipt['readonly_dependencies_unchanged'],
        'dependency_cache_unchanged_reported': receipt['dependency_cache_unchanged'],
    }

prior = REV/'R51_POINT_WICK_REVIEW_R1.json'
old_review = read(prior)
walk(old_review)
verification = {
    'schema':'iald-independent-pin-verification/v1', 'created_utc':datetime.now(timezone.utc).isoformat(),
    'actor':ACTOR, 'ok':True, 'verified_unique_path_hash_pairs':len(checks),
    'coverage':'Pares path/sha256 nos três recibos, respectivos manifestos, caches e parecer anterior RegularPoint. Leitura de bytes; sem rebuild.',
    'pins':list(checks.values()), 'components':components,
}
verification_pin = save_new(REV/'R51_GREEN_COMPONENT_PIN_VERIFICATION_R2.json', verification)
common = {
    'schema':'iald-independent-component-review/v1', 'created_utc':datetime.now(timezone.utc).isoformat(),
    'reviewer':ACTOR, 'verdict':'PASS_COMPONENT_WITH_SCOPE', 'requirement_satisfied':False,
    'mission_reference':pin(REF), 'final_sync':pin(sync_path),
    'revision':proj['revision'], 'state_sha256':proj['state_sha256'],
    'pin_verification':verification_pin, 'new_builds':0, 'provider_calls':0,
    'mission_mutations':False, 'production_modified':False, 'blocking_findings':[],
}
finite_review = dict(common, requirement='R7', components={k:components[k] for k in ['FiniteProjectionR3','MatrixCornerR2']},
    prior_preparatory_review=pin(REV/'R51_FINITE_MATRIX_REVIEW_PREPARATION_R1.json'),
    source_findings=[
        {'path':str(B/items[0][1]), 'lines':[55,70], 'finding':'finite_positive_below consome a semifinitude efetiva value_finite_minorants e fidelidade do mesmo value; a testemunha positiva finita não é premissa.'},
        {'path':str(B/items[0][1]), 'lines':[74,106], 'finding':'Limiar espectral fornece q não nula. value_mono/value_scale demonstram finitude; epsilon*q ≤ Y ≤ e e o lema genérico de suporte dão q*e=q. Instâncias nativas de RegularHilbert Fock são especializadas explicitamente.'},
        {'path':str(B/items[0][1]), 'lines':[109,145], 'finding':'one não nulo fornece projeção finita incondicional; positiveDual(log(value q).toReal) e escala exp(-s) calibram para value=1, preservando IsStarProjection.'},
        {'path':str(B/items[1][1]), 'lines':[33,80], 'finding':'CFC das partes positiva/negativa e a troca por U produzem A+*U nilpotente não nulo; hipóteses do lema genérico são explícitas.'},
        {'path':str(B/items[1][1]), 'lines':[135,197], 'finding':'normalized_pair de Weyl na cunha concreta fornece a troca de sinal; característica do vácuo exclui A=0. fibre injetiva transporta ao core existente; bounded polar já fornecido produz e,v. Não há premissa final de nilpotência, canto ou traço.'},
    ],
    scope=['Mesmo CanonicalFockRegular.core, PositiveInput e inverseSupremum/value existentes.',
           '10 declarações públicas, EXIT0 e somente propext/Classical.choice/Quot.sound.',
           'Projeção finita normalizada e canto ortogonal são componentes. Split ortogonal de traços iguais ainda não aprovado neste parecer.',
           'Não se infere classificação tipo II, montagem RemainingModularCoreInput ou cumprimento integral de R7.'],
    low_findings=['Avisos de depreciação sem efeito material; nenhuma rodada cosmética solicitada.'])
wick_review = dict(common, requirement='R8', components={'LocalWickStressIdentificationR3':components['LocalWickStressIdentificationR3']},
    regular_point_supplier_by_reference={'review':pin(prior),'source':pin(B/'maxwell_global/RegularPointAnnihilationR2.lean'),
        'decision':'Parecer anterior preservado: RegularPointR2 EXIT0, 15 listas trio; fornecedor lido por remissão, sem nova auditoria ampla.'},
    source_findings=[
        {'path':str(B/items[2][1]), 'lines':[20,50], 'finding':'Annihilation pontual é endomorfismo linear algébrico de regularFockDomain. regularWick define a forma bilocal e mantém amplitude²=escala Fourier e fator real 1/2.'},
        {'path':str(B/items[2][1]), 'lines':[52,81], 'finding':'R3 corrige somente transporte ao finiteKernel por congrArg/funext. Continuidade em x,y provém das ondas dos rótulos regulares em soma finita; diagonal é avaliação desta forma.'},
        {'path':str(B/items[2][1]), 'lines':[83,153], 'finding':'Contração Maxwell é construída da forma local e igualada ao tensor Fock já normalizado. Igualdade calibrada mantém A:RemainingModularCoreInput D explícito.'},
        {'path':str(B/items[2][1]), 'lines':[155,161], 'finding':'Relação circular transporta simultaneamente os vetores para regularCircular ψ,χ; não afirma igualdade com estados fixos.'},
    ],
    scope=['8 declarações públicas verificadas nesta rodada; RegularPointR2 15 por remissão.',
           'Forma Wick no domínio regular do mesmo H1/Fock; nenhuma extensão global limitada do campo pontual ou operador de criação pontual demonstrada.',
           'Smearing Bochner de PointAnnihilationSmearingR3 não aprovado neste parecer: aguarda recibo e revisão própria.',
           'R8 integral permanece aberto; A não é fabricado nem dispensado por esta igualdade local.'],
    historical_failure={'source':pin(B/'maxwell_global/LocalWickStressIdentificationR2.lean'),
        'receipt':pin(B/'orbital_rotation/attempts/20261016T204127_892966Z/RECEIPT.json'),'exit_code':1},
    low_findings=['continuous_finset_sum depreciado: sem bloqueio material ou nova rodada cosmética.'])
reports = [save_new(REV/'R51_FINITE_MATRIX_REVIEW_R2.json',finite_review), save_new(REV/'R51_POINT_WICK_REVIEW_R2.json',wick_review)]
print(json.dumps({'ok':True,'revision':proj['revision'],'verified_pin_pairs':len(checks),'reports':reports,'verification':verification_pin},ensure_ascii=False))
