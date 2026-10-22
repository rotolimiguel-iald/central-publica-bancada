"""Read-only source/receipt verification; new independent review artifacts only."""
import ast
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
REFERENCE = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
PYTHON = r'C:\Python314\python.exe'
CLI = r'C:\IALD\MEMORIA_IALD\mission_cli.py'
ACTOR = 'codex-mission-memory-review'

def read(path):
    return json.loads(Path(path).read_bytes())

def pin(path):
    path = Path(path)
    raw = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def fresh(path, value):
    assert not path.exists(), path
    raw = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    temp = path.with_suffix(path.suffix + '.tmp')
    with temp.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw

def embedded(tree):
    return next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets))

def functions(tree):
    return {n.name: ast.dump(n, include_attributes=False) for n in tree.body if isinstance(n, ast.FunctionDef)}

def axioms(text, name):
    found = re.findall(r"'" + re.escape(name) + r"'\s+depends on axioms:\s*\[([^\]]*)\]", text)
    assert found, name
    values = [sorted(x.strip() for x in s.split(',') if x.strip()) for s in found]
    assert all(set(v) <= {'propext', 'Classical.choice', 'Quot.sound'} for v in values), name
    assert all(v == values[0] for v in values), name
    return values[0]

def main():
    initial = read(OUT / 'INITIAL_PIN_CHECK.json')
    checked = []
    for path, entry in initial['pins'].items():
        actual = pin(path)
        assert actual['sha256'] == entry['actual'], path
        checked.append(actual)
    integration = read(BASE / 'INTEGRATION_QUADRATIC_R3.json')
    component = read(BASE / 'quadratic_review/INTEGRATION_REVIEW_R2.json')
    for entry in component['formal_evidence']:
        actual = pin(entry['path'])
        assert actual['sha256'] == entry['sha256'], entry['path']
        checked.append(actual)
    assert component['ladder'] == {'clean': 7171, 'expected': 7171, 'all_verified': True}
    assert component['quadratic_consumer']['all_verified'] is True
    assert component['quadratic_consumer']['runtime']['passed'] is True
    assert len(component['refusal_controls']) == 7 and all(c['passed'] for c in component['refusal_controls'])
    tree = ast.parse(Path(integration['candidate']['path']).read_bytes())
    source = Path(integration['new_source']['path']).read_text(encoding='utf-8')
    assert embedded(tree)['TGLExt/RuleQuadraticResidual.lean'].replace('\r\n', '\n') == source.replace('\r\n', '\n')
    runtime_tree = ast.parse(Path(integration['runtime']['path']).read_bytes())
    runtime_functions = functions(runtime_tree)
    candidate_functions = functions(tree)
    assert len(runtime_functions) == 3
    assert all(candidate_functions[name] == body for name, body in runtime_functions.items())
    quadratic_log = (BASE / 'quadratic_review/build_r2/RuleQuadraticResidual_BUILD.log').read_text(encoding='utf-8')
    quadratic_axioms = {name: axioms(quadratic_log, name) for name in integration['new_flags'].values()}

    h3 = read(BASE / 'R9_H3_SCOPE_R1.json')
    rite = Path(r'C:\IALD\Central de Patentes\work\rite394_20261015\r3')
    receipt = read(rite / 'RITE_RECEIPT.json')
    execution_copy = rite / 'um_v394_final.py'
    execution_pin = pin(execution_copy)
    assert execution_pin['sha256'] == receipt['execution_copy_sha256']
    checked.append(execution_pin)
    h3_embedded = embedded(ast.parse(execution_copy.read_bytes()))
    provenance = read(BASE / 'full_rite/declaration_sources_r3/DECLARATION_SOURCES.json')
    audit = (rite / 'tgl_kernel_audit_capture.txt').read_text(encoding='utf-8')
    h3_checked = []
    for entry in h3['records']:
        name = entry['declaration']
        path = Path(entry['source']['path'])
        relative = 'TGLExt/' + path.name
        body = path.read_text(encoding='utf-8')
        assert provenance[name] == relative
        assert body.replace('\r\n', '\n') == h3_embedded[relative].replace('\r\n', '\n')
        measured_axioms = axioms(audit, name)
        assert set(measured_axioms) == set(entry['axioms'])
        h3_checked.append({'declaration': name, 'source': pin(path), 'line': entry['line'],
                           'executed_embedded_body_matches': True, 'axioms_in_existing_log': measured_axioms})

    raw = subprocess.run([PYTHON, '-B', '-X', 'utf8', CLI],
                         input=json.dumps({'operation': 'project', 'reference': str(REFERENCE), 'max_chars': 60000}),
                         capture_output=True, text=True, encoding='utf-8', check=True)
    sync = json.loads(raw.stdout)
    assert sync['ok'] is True
    projection = sync['result']['projection']
    assert projection['context_id'] == read(REFERENCE)['context_id']
    tasks = {t['id']: t for t in projection['active'] + projection['settled']}
    assert tasks['M0_MEMORIA']['status'] == 'satisfied'
    assert not projection['hold']
    for tid in ('R2', 'R9'):
        assert tasks[tid]['status'] == 'review_pending' and tasks[tid]['submitted_by'] != ACTOR
        for entry in tasks[tid]['evidence']:
            assert pin(entry['path'])['sha256'] == entry['sha256']
    fresh(OUT / 'REVIEW_PROJECT_SNAPSHOT.json', sync)
    machine = {
        'statute': 'REAL', 'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'method': 'SHA256, AST literal extraction and function body comparison; read existing Lean output. No Python candidate execution or Lean compilation.',
        'checked_pins': list({p['path']: p for p in checked}.values()),
        'r2': {'candidate_embedded_source_matches': True, 'runtime_functions_match': list(runtime_functions),
               'compiled_declarations_in_existing_log': quadratic_axioms,
               'existing_ladder': component['ladder'],
               'existing_runtime_checks': component['quadratic_consumer']['runtime']['check_count'],
               'existing_refusal_controls': component['refusal_controls'],
               'main_executed_by_this_review': False},
        'r9': {'declarations': h3_checked, 'execution_copy': execution_pin, 'existing_rite_exit': receipt['exit_code']},
        'script': pin(__file__), 'new_builds': 0, 'provider_calls': 0
    }
    fresh(OUT / 'MECHANICAL_VERIFICATION.json', machine)
    common = {
        'unit': 'F1.FECHO_20261015', 'reviewer': {'id': ACTOR, 'kind': 'agent'},
        'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'mission_reference': pin(REFERENCE), 'context_id': projection['context_id'],
        'projection_at_review': pin(OUT / 'REVIEW_PROJECT_SNAPSHOT.json'),
        'review_revision': projection['revision'],
        'independence': 'Revisor real distinto do construtor/submitter; não reconstruiu os componentes nem simulou outro ator.',
        'method': 'Leitura dos critérios e fontes Lean/Python, exame dos recibos e revisões existentes, hashes atuais e verificações estáticas próprias.',
        'verification': pin(OUT / 'MECHANICAL_VERIFICATION.json'),
        'scope': 'Aceite do requisito no controlador da missão. Não fecha o quadro, não ratifica gate/selo nem confirma física.',
        'new_provider_calls': 0, 'new_builds': 0, 'production_science_modified': False,
        'findings_blocking_criterion': []
    }
    r2 = dict(common, requirement='R2', criterion=tasks['R2']['criterion'],
        evidence=tasks['R2']['evidence'], verdict='PASS_CRITERION_WITH_COMPONENT_SCOPE',
        criterion_mapping=[
            {'clause': 'resíduo nulo iff leitura=âncora', 'result': 'PASS', 'reason': 'residual A X = purityR(Eg X - A); positividade estrita de purityR e sub_eq_zero dão Eg X = A. Domínio M2.'},
            {'clause': 'invariância no fluxo', 'result': 'PASS', 'reason': 'residual_flow usa reading_flow para qualquer A fixa. Continuidade e derivada temporal zero decorrem da constância; não se afirma decaimento do resíduo.'},
            {'clause': 'controles', 'result': 'PASS', 'reason': 'transportedRho é aceito para I/2 apesar de ser estado bruto distinto; projPlus produz resíduo 1/2 e recusa; âncora fora da imagem de Eg tem resíduo positivo.'},
            {'clause': 'consumidor usa prova e fontes', 'result': 'PASS', 'reason': 'Consumidor exige relatório formal válido, 18 declarações com axiomas padrão, fonte embutida pinada, contagem exata 7171 e dependência temporal. Três funções coincidem por AST com a candidata; 7 recusas existentes foram conferidas.'}
        ],
        evidence_counts={'lean_declarations': len(quadratic_axioms), 'existing_runtime_checks': 274, 'existing_refusal_controls': 7},
        preserved_limits=[
            'Eg não é injetiva nos estados brutos; resíduo nulo não prova X=A fora do subtipo de inscrições fixas.',
            'Âncora fixa e modelo finito M2. A função é quadrática afim no estado para âncora não nula; não cria evolução dissipativa de aprendizado.',
            'Tolerâncias numéricas do consumidor são distintas da igualdade exata Lean.',
            'O teste integrado existente é de componente; execução final de main/artigos/selo continua pertencendo a R3 e requer a candidata final corrente.'
        ])
    r9 = dict(common, requirement='R9', criterion=tasks['R9']['criterion'],
        evidence=tasks['R9']['evidence'], verdict='PASS_SCOPE_CLASSIFICATION',
        criterion_mapping=[
            {'clause': 'construções existentes reconhecidas', 'result': 'PASS', 'reason': 'lightH2/lightH3 são termos reais sob certificados nomeados. lightH3 recebe MaxwellCertificate, charge_link, estado regular não trivial, N e G positivo; não se declara ausente a implicação já construída.'},
            {'clause': 'todas as direções', 'result': 'PASS', 'reason': 'NamedAtlasH3 quantifica todas as cartas, pontos e direções nulas não nulas; horizon_einstein_reconstruction recebe pencils universais. Um único horizonte padrão não descarrega esses antecedentes.'},
            {'clause': 'hipótese versus consequência', 'result': 'PASS', 'reason': 'O teorema do atlas recebe hH3 como seta da identidade finita já provada para NamedAtlasH3; isso fornece H3 por aplicação da hipótese, sem derivá-la somente do estado. Conservação, compatibilidade e conexão permitem a conclusão geométrica condicional.'},
            {'clause': 'limite do contraexemplo de relógio', 'result': 'PASS', 'reason': 'state_clock_dichotomy restringe correspondência de quarta ordem na família tipada; a fonte adjacente preserva matching quadrático. Não é impossibilidade universal de Clausius de segunda ordem.'}
        ],
        evidence_counts={'declarations': len(h3_checked), 'distinct_primary_sources': len({r['source']['path'] for r in h3_checked})},
        hypothesis_vs_state_derivation={
            'REAL': 'Existem construtores H2/H3 condicionais e a passagem de H3 geométrica em todas as direções à equação de Einstein sob as hipóteses nomeadas.',
            'INPUT_KNOWN': 'A identificação física com a literatura de Jacobson conserva o estatuto KNOWN registrado; não foi feita nova checagem de literatura por este revisor.',
            'OPEN': 'Estas evidências não fornecem uma realização Maxwell conjunta completa, sua identificação com a fonte em todas as cartas, nem um habitante de H3 geométrica universal derivado apenas do estado.'
        },
        preserved_limits=[
            'O aceite classifica corretamente o alcance de H3; não transforma antecedente em prova de existência física nem encerra R5/R7/R8.',
            'O log do rito anterior é usado somente para proveniência das seis declarações e igualdade das fontes embutidas; não aceita R3 nem a candidata final.',
            'Axiomas padrão sem sorry certificam a prova do enunciado com suas hipóteses; não dispensam os certificados que o enunciado recebe.'
        ])
    fresh(OUT / 'R2_REQUIREMENT_REVIEW.json', r2)
    fresh(OUT / 'R9_REQUIREMENT_REVIEW.json', r9)
    print(json.dumps({'reports': [pin(OUT / 'R2_REQUIREMENT_REVIEW.json'), pin(OUT / 'R9_REQUIREMENT_REVIEW.json')],
                      'pins_checked': len(machine['checked_pins']), 'revision_at_review': projection['revision'],
                      'new_builds': 0, 'provider_calls': 0}, ensure_ascii=False))

if __name__ == '__main__':
    main()
