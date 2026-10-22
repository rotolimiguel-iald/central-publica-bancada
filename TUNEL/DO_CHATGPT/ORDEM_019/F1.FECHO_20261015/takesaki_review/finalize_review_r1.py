from pathlib import Path
import datetime, hashlib, json, re

B = Path(__file__).resolve().parent
P = B.parent
S = P / 'takesaki_fock'
TRIO = {'propext', 'Classical.choice', 'Quot.sound'}

def pin(p):
    p = Path(p)
    raw = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def put(p, value):
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8') if isinstance(value, dict) else value.encode('utf-8')
    with p.open('xb') as f:
        f.write(raw)
    assert p.read_bytes() == raw

builder_path = S / 'FOCK_REGULAR_CORE_RECEIPT_R1.json'
builder = read(builder_path)
verified = {}

def verify_pins(x):
    if isinstance(x, dict):
        if 'path' in x and 'sha256' in x:
            actual = pin(x['path'])
            assert actual['sha256'] == x['sha256'], x['path']
            if 'bytes' in x:
                assert actual['bytes'] == x['bytes'], x['path']
            verified[actual['path']] = actual
        for y in x.values():
            verify_pins(y)
    elif isinstance(x, list):
        for y in x:
            verify_pins(y)

verify_pins(builder)
builds = []
for name, module in zip(['generic', 'canonical'], builder['modules']):
    rp = B / name / 'RECEIPT_R1.json'
    r = read(rp)
    verify_pins(r)
    assert r['passed'] and r['exit_code'] == 0 and r['source_exact_copy']
    assert r['source']['sha256'] == module['source']['sha256']
    assert set(r['axioms']) == set(module['all_local_axiom_reports'])
    assert all(set(x) <= TRIO for x in r['axioms'].values())
    assert not re.search(r'\b(?:sorry|admit|axiom)\b', re.sub(r'/\-.*?\-/', '', Path(r['source']['path']).read_text(encoding='utf-8'), flags=re.S))
    builds.append({'module': module['module'], 'receipt': pin(rp), 'start_utc': r['start_utc'], 'end_utc': r['end_utc'], 'seconds': r['seconds'], 'exit_code': r['exit_code'], 'all_local_axiom_reports': r['axiom_count'], 'explicit_declarations': len(module['explicit_declarations']), 'theorems': len(module['theorems']), 'olean_identical_to_builder': r['olean_identical_to_accepted'], 'source': r['source'], 'olean': r['olean'], 'log': r['log']})

kernel = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')
related = [kernel / x for x in ['V350RegularDualAction.lean', 'V350L2CharacterMultiplier.lean', 'V350RegularGeneratedAlgebra.lean', 'V350L2OperatorLift.lean']]
findings = [
    {'id': 'T1', 'status': 'REAL', 'result': 'PASSA', 'claim': 'UnitaryFlow exige um grupo unitário fortemente contínuo; as leis da representação regular são derivadas, não campos assumidos.', 'anchor': 'RegularCovariantCoreR3.lean:12,64-108'},
    {'id': 'T2', 'status': 'REAL', 'result': 'PASSA', 'claim': 'core é a álgebra de von Neumann gerada por fibre(M) e Ureg(t); embedding é um homomorfismo estrela unital injetivo, usando fibre_injective. core_minimal prova minimalidade entre álgebras que contêm esses geradores.', 'anchor': 'RegularCovariantCoreR3.lean:110-142'},
    {'id': 'T3', 'status': 'REAL', 'result': 'PASSA', 'claim': 'A ação dual restringe Ad(D_s), D_s f(x)=exp(-isx)f(x), fixa fibre(M) e multiplica Ureg(t) por exp(-ist). Não é conjugação pelo próprio Ureg(s).', 'anchor': 'RegularCovariantCoreR3.lean:144-195; V350L2CharacterMultiplier.lean:21; V350RegularDualAction.lean:18-24'},
    {'id': 'T4', 'status': 'REAL', 'result': 'PASSA', 'claim': 'O consumidor constrói fockFlow=Gamma(B0(-2*pi*t)) no F canônico e usa M=R_field(KWR), com covariância para o fluxo restrito de CanonicalWedgeFlow. Não assume LightNetData nem FockCertificate.', 'anchor': 'CanonicalFockRegularCoreR2.lean:22-36,65-74'},
    {'id': 'T5', 'status': 'REAL', 'result': 'PASSA', 'claim': 'fockFlow_inhabited tem testemunha explícita fockFlow; os operadores e a álgebra concretos são definidos por termos, sem hipótese de existência da própria saída.', 'anchor': 'CanonicalFockRegularCoreR2.lean:22-38'},
    {'id': 'T6', 'status': 'DERIVED', 'result': 'ESCOPO', 'claim': 'No módulo genérico, M não é suposto invariante: a covariância é uma igualdade no ambiente. A estabilidade de M necessária ao consumidor é a do fluxo concreto de cunha já construído. Não interpretar o genérico como teorema universal de produto cruzado para M arbitrário.'},
    {'id': 'T7', 'status': 'OPEN', 'result': 'ESCOPO', 'claim': 'Continuam abertos a identificação deste fluxo com o grupo modular do vácuo, o traço normal semifinito fiel e sua escala neste core, a equivalência com o core V351 da torre e a dualidade de Takesaki completa.'}
]
out = {'verdict': 'PASSA_COM_ESCOPO_CORE_REGULAR_REPRESENTADO', 'material_findings': [], 'unit': 'F1.FECHO_20261015', 'claim_event': 845, 'reviewer': 'codex-atrator-skeptic', 'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'builder_final_receipt': pin(builder_path), 'builds': builds, 'counts': {'modules': len(builds), 'explicit_declarations': sum(x['explicit_declarations'] for x in builds), 'theorems': sum(x['theorems'] for x in builds), 'all_local_axiom_reports': sum(x['all_local_axiom_reports'] for x in builds)}, 'all_axioms_within_trio': True, 'sorry_or_local_axiom': False, 'audit_method': 'Recompilação independente de cópias exatas, com os auditores de todas as declarações locais embutidos nas fontes. Conjuntos de nomes comparados aos do construtor; caches de dependências somente lidos. O consumidor usa o genérico e o fluxo de cunha recompilados pela revisão.', 'findings': findings, 'binary_reproducibility': 'O campo olean_identical_to_builder registra a comparação medida. Diferença binária não foi atribuída a causa não demonstrada; os fontes, enunciados e conjuntos de declarações foram conferidos.', 'related_sources_read': [pin(x) for x in related], 'verified_pins': list(verified.values()), 'script': pin(__file__), 'boundaries': {'canonical_sources_written': False, 'memory_written': False, 'production_written': False, 'observed_data_opened': False, 'providers_called': False, 'gate_changed': False, 'administrative_audited_or_closed_claimed': False}}
put(B / 'REVISAO_TAKESAKI_FOCK_R1.json', out)
rows = '\n'.join(f"| {x['module']} | {x['seconds']:.3f} | {x['exit_code']} | {x['all_local_axiom_reports']} | {x['olean_identical_to_builder']} |" for x in builds)
md = f"""# Revisão independente — core regular da cunha de Fock

**PASSA COM ESCOPO**, sem achado material. Revisão técnica; AUDITADA/FECHADA continua ato da gerência.

| Módulo | segundos | exit | declarações locais/axiomas | .olean idêntico |
|---|---:|---:|---:|---|
{rows}

[REAL] {out['counts']['explicit_declarations']} declarações explícitas, {out['counts']['theorems']} teoremas e {out['counts']['all_local_axiom_reports']} declarações incluindo auxiliares verificadas. Somente propext, Classical.choice e Quot.sound; zero sorry/axioma local. Comando, toolchain Lean 4.31.0, LEAN_PATH literal, início, fim e duração estão nos recibos e BUILD.log de cada compilação. O consumidor importou o genérico recompilado nesta revisão. Diferenças binárias, quando presentes, são declaradas sem causa presumida.

## Conteúdo conferido

[REAL] A representação em L²(ℝ;F) usa Ureg(t)=fibre(Gamma(B0(-2πt)))·shift(t). O core é o bicomutante estrela dos geradores, a inclusão fibre de M é fiel e as leis de grupo, covariância, continuidade forte e minimalidade são derivadas. O M concreto é R_field(KWR) no mesmo F já construído. A testemunha fockFlow é explícita; não há premissa LightNetData/FockCertificate ou existência assumida da saída.

[REAL] A ação dual é Ad(D_s), com D_s f(x)=exp(-isx)f(x); fixa fibre(M) e envia Ureg(t) a exp(-ist)Ureg(t). Não confundir esse caráter com a lei de escala de um traço, que não foi construída nestes dois módulos.

[DERIVED — escopo] O genérico permite M arbitrário e prova covariância no ambiente; o consumidor concreto utiliza a invariância da cunha já provada. O enunciado não é uma equivalência universal de produtos cruzados. A não vacuidade do fluxo decorre do termo fockFlow; a não trivialidade do F permanece sustentada pelo vácuo de norma 1 previamente auditado, sem novo ensaio aqui.

[OPEN] Identificação do boost com o grupo modular do vácuo; traço normal semifinito fiel e escala neste core; equivalência com a torre V351; dualidade de Takesaki completa. Nenhuma confirmação física ou alteração de gate.

Fontes e hashes integrais, âncoras, conjuntos de axiomas e pinos verificados constam de REVISAO_TAKESAKI_FOCK_R1.json. Fontes canônicas, memória e produção permaneceram intactas.
"""
put(B / 'REVISAO_TAKESAKI_FOCK_R1.md', md)
print(json.dumps({'json': pin(B/'REVISAO_TAKESAKI_FOCK_R1.json'), 'md': pin(B/'REVISAO_TAKESAKI_FOCK_R1.md'), 'counts': out['counts'], 'builds': [{'module':x['module'],'seconds':x['seconds'],'olean_identical_to_builder':x['olean_identical_to_builder']} for x in builds]}, ensure_ascii=False))
